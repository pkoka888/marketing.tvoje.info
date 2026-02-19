#!/usr/bin/env python3
"""
Server Evidence Collection Script — Universal (Project-Agnostic).

Collects read-only evidence from all servers via SSH.
Loads server config from servers.yml.
Cross-platform (Windows + Linux).
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None


# Evidence commands (all read-only, safe to run on any server)
EVIDENCE_COMMANDS: Dict[str, str] = {
    "system-info.txt": (
        "hostname -f && uname -a && cat /etc/os-release && uptime && free -h && df -h"
    ),
    "packages.txt": "dpkg -l 2>/dev/null | head -200 || echo 'dpkg not found'",
    "services.txt": (
        "systemctl list-units --type=service --state=running --no-pager "
        "2>/dev/null || echo 'systemctl not found'"
    ),
    "network.txt": (
        "ip addr && ip route && ss -tulpn 2>/dev/null || echo 'network tools not found'"
    ),
    "users.txt": "cat /etc/passwd | grep -v nologin | grep -v '/bin/false'",
    "processes.txt": "ps auxf --sort=-%mem | head -30",
    "docker.txt": (
        "docker ps -a --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}' "
        "2>/dev/null || echo 'docker not available'"
    ),
    "disk-usage.txt": (
        "df -h && echo '---' && "
        "du -sh /var/www/*/ /home/*/ /opt/*/ 2>/dev/null | sort -rh | head -15"
    ),
    "nginx.txt": (
        "ls -la /etc/nginx/sites-enabled/ 2>/dev/null && "
        "nginx -T 2>/dev/null | head -100 || echo 'no nginx'"
    ),
    "failed.txt": "systemctl --failed --no-pager 2>/dev/null || echo 'none'",
    "timers.txt": "systemctl list-timers --no-pager 2>/dev/null || echo 'no timers'",
    "pm2.json": "pm2 jlist 2>/dev/null || echo '[]'",
}


def load_config() -> Dict[str, Any]:
    """Load servers.yml configuration."""
    config_path = Path(__file__).resolve().parent.parent / "servers.yml"
    if not config_path.exists():
        print(f"ERROR: {config_path} not found")
        sys.exit(1)
    if not yaml:
        print("ERROR: PyYAML not installed. Run: pip install pyyaml")
        sys.exit(1)
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def log(message: str) -> None:
    """Log message with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {message}")


def try_ssh(host: str, port: int, user: str, timeout: int = 10) -> bool:
    """Test SSH connectivity."""
    try:
        result = subprocess.run(
            ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "BatchMode=yes",
             "-o", "StrictHostKeyChecking=no", "-o", "LogLevel=ERROR",
             "-p", str(port), f"{user}@{host}", "echo ok"],
            capture_output=True, text=True, timeout=timeout + 5
        )
        return result.returncode == 0 and "ok" in result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def find_connection(server: Dict[str, Any]) -> Optional[Tuple[str, int, str]]:
    """Find a working SSH connection to the server. Returns (host, port, user) or None."""
    user = server["ssh"]["users"][0]
    # Try Tailscale first, then public, then internal
    attempts = [
        (server["tailscale_ip"], server["ssh"]["port_tailscale"]),
        (server.get("internal_ip", ""), server["ssh"].get("port_internal", 0)),
    ]

    # Add public if reachable flag is true
    public_ip = "89.203.173.196"  # From config
    if server["ssh"].get("public_reachable", False):
        attempts.insert(1, (public_ip, server["ssh"]["port_public"]))

    for host, port in attempts:
        if host and port:
            if try_ssh(host, port, user):
                return host, port, user
    return None


def ssh_exec(host: str, port: int, user: str, cmd: str, timeout: int = 30) -> Tuple[int, str]:
    """Execute command via SSH."""
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
             "-o", "StrictHostKeyChecking=no", "-o", "LogLevel=ERROR",
             "-p", str(port), f"{user}@{host}", cmd],
            capture_output=True, text=True, timeout=timeout
        )
        output = result.stdout
        if result.stderr and result.returncode != 0:
            output += f"\n[STDERR]: {result.stderr}"
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return 1, "TIMEOUT"
    except Exception as e:
        return 1, f"ERROR: {e}"


def collect_server_evidence(name: str, host: str, port: int, user: str,
                            output_dir: Path) -> bool:
    """Collect evidence from a single server."""
    server_dir = output_dir / name
    server_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    for filename, cmd in EVIDENCE_COMMANDS.items():
        code, output = ssh_exec(host, port, user, cmd)
        filepath = server_dir / filename
        filepath.write_text(output, encoding="utf-8")
        status = "✓" if code == 0 else "⚠"
        log(f"  {status} {filename}")
        if code == 0:
            success_count += 1

    log(f"  → {success_count}/{len(EVIDENCE_COMMANDS)} commands succeeded")
    return success_count > 0


def check_alerts(output_dir: Path) -> list:
    """Check collected evidence for alerts."""
    alerts = []
    for server_dir in output_dir.iterdir():
        if not server_dir.is_dir():
            continue
        server = server_dir.name

        disk_file = server_dir / "disk-usage.txt"
        if disk_file.exists():
            for line in disk_file.read_text().split("\n"):
                if "%" in line and "/" in line:
                    for part in line.split():
                        if part.endswith("%"):
                            try:
                                usage = int(part.rstrip("%"))
                                if usage > 85:
                                    alerts.append(f"🔴 {server}: disk {usage}%")
                                elif usage > 70:
                                    alerts.append(f"⚠️  {server}: disk {usage}%")
                            except ValueError:
                                pass

        failed_file = server_dir / "failed.txt"
        if failed_file.exists():
            content = failed_file.read_text().strip()
            if content and content != "none" and "0 loaded" not in content:
                alerts.append(f"🔴 {server}: failed services detected")

    return alerts


def main() -> None:
    """Main entry point."""
    config = load_config()
    servers = config.get("servers", {})

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    evidence_base = Path(__file__).resolve().parent.parent.parent / "evidence"
    output_dir = evidence_base / timestamp

    # Allow targeting specific server
    targets = list(servers.keys())
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if target in servers:
            targets = [target]
        elif target == "all":
            pass
        else:
            print(f"Unknown target: {target}")
            print(f"Usage: {sys.argv[0]} [s60|s61|s62|all]")
            sys.exit(1)

    print(f"Server Evidence Collection — {timestamp}")
    print(f"Targets: {', '.join(targets)}")
    print("=" * 50)

    results = {}
    for name in targets:
        server = servers[name]
        log(f"=== {name} ({server['purpose']}) ===")
        log(f"Finding route to {name}...")

        conn = find_connection(server)
        if conn:
            host, port, user = conn
            log(f"  Connected via: {host}:{port}")
            results[name] = collect_server_evidence(name, host, port, user, output_dir)
        else:
            log(f"  ✗ {name}: ALL routes failed")
            results[name] = False

    # Check alerts
    alerts = check_alerts(output_dir) if output_dir.exists() else []

    # Save summary
    summary = {
        "collected_at": timestamp,
        "results": {s: "success" if ok else "failed" for s, ok in results.items()},
        "alerts": alerts,
    }
    if output_dir.exists():
        (output_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    print("\n" + "=" * 50)
    print("Summary:")
    for server, ok in results.items():
        print(f"  {'✓' if ok else '✗'} {server}")
    if alerts:
        print(f"\n⚠️  ALERTS ({len(alerts)}):")
        for alert in alerts:
            print(f"  {alert}")
    else:
        print("\n✅ No alerts")
    if output_dir.exists():
        print(f"\nEvidence: {output_dir}")


if __name__ == "__main__":
    main()
