#!/usr/bin/env python3
"""
Server Evidence Collection Script — Cross-Platform.

Uses SSH config aliases from ~/.ssh/config for connection.
Automatically tries Tailscale → Public → Internal routes.
All commands are read-only for safe evidence gathering.
"""

import os
import sys
import socket
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


# Server configuration — matches ~/.ssh/config aliases
SERVERS: Dict[str, Dict[str, Any]] = {
    "s60": {
        "aliases": ["s60pa", "s60pa-pub", "s60pa-int"],
        "purpose": "Hub/Backup",
        "tailscale_ip": "100.111.141.111",
        "ssh_port": 20,
    },
    "s61": {
        "aliases": ["s61pa", "s61pa-pub", "s61pa-int"],
        "purpose": "Gateway/Traefik",
        "tailscale_ip": "100.111.141.112",
        "ssh_port": 20,
    },
    "s62": {
        "aliases": ["s62pa", "s62pa-pub", "s62pa-int"],
        "purpose": "Production/Web",
        "tailscale_ip": "100.91.164.109",
        "ssh_port": 20,
    },
}

# Evidence commands (all read-only)
EVIDENCE_COMMANDS: Dict[str, str] = {
    "system-info.txt": "hostname -f && uname -a && cat /etc/os-release && uptime && free -h && df -h",
    "packages.txt": "dpkg -l 2>/dev/null | head -200 || echo 'dpkg not found'",
    "services.txt": "systemctl list-units --type=service --state=running --no-pager 2>/dev/null || echo 'systemctl not found'",
    "network.txt": "ip addr && ip route && ss -tulpn 2>/dev/null || echo 'network tools not found'",
    "users.txt": "cat /etc/passwd | grep -v nologin | grep -v '/bin/false'",
    "processes.txt": "ps auxf --sort=-%mem | head -30",
    "docker.txt": "docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null || echo 'docker not available'",
    "crontab.txt": "crontab -l 2>/dev/null; for u in $(cut -d: -f1 /etc/passwd); do echo \"--- $u ---\"; sudo crontab -u $u -l 2>/dev/null; done",
    "disk-usage.txt": "df -h && echo '---' && du -sh /var/www/*/ /home/*/ /opt/*/ 2>/dev/null | sort -rh | head -15",
    "nginx.txt": "ls -la /etc/nginx/sites-enabled/ 2>/dev/null && nginx -T 2>/dev/null | head -100 || echo 'no nginx'",
    "failed.txt": "systemctl --failed --no-pager 2>/dev/null || echo 'none'",
    "timers.txt": "systemctl list-timers --no-pager 2>/dev/null || echo 'no timers'",
}

# Evidence output directory
EVIDENCE_DIR = Path(os.environ.get(
    "EVIDENCE_DIR",
    Path(__file__).resolve().parent.parent.parent.parent / "evidence"
))


def log(message: str) -> None:
    """Log message with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {message}")


def find_working_alias(server: str) -> Optional[str]:
    """Try SSH aliases in order until one works. Returns working alias or None."""
    info = SERVERS[server]
    for alias in info["aliases"]:
        try:
            result = subprocess.run(
                ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes",
                 alias, "echo ok"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and "ok" in result.stdout:
                return alias
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    return None


def ssh_exec(alias: str, command: str, timeout: int = 30) -> Tuple[int, str]:
    """Execute command via SSH using config alias."""
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
             alias, command],
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


def collect_server_evidence(server: str, alias: str, output_dir: Path) -> bool:
    """Collect evidence from a single server."""
    log(f"=== {server} ({SERVERS[server]['purpose']}) via {alias} ===")

    server_dir = output_dir / server
    server_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    for filename, cmd in EVIDENCE_COMMANDS.items():
        code, output = ssh_exec(alias, cmd)
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

        # Check disk usage
        disk_file = server_dir / "disk-usage.txt"
        if disk_file.exists():
            for line in disk_file.read_text().split("\n"):
                if "%" in line and ("/" in line):
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

        # Check failed services
        failed_file = server_dir / "failed.txt"
        if failed_file.exists():
            content = failed_file.read_text().strip()
            if content and content != "none" and "0 loaded" not in content:
                alerts.append(f"🔴 {server}: failed services detected")

    return alerts


def main() -> None:
    """Main entry point."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = EVIDENCE_DIR / timestamp

    # Allow targeting specific server
    targets = list(SERVERS.keys())
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if target in SERVERS:
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
    for server in targets:
        log(f"Finding route to {server}...")
        alias = find_working_alias(server)
        if alias:
            log(f"  Connected via: {alias}")
            results[server] = collect_server_evidence(server, alias, output_dir)
        else:
            log(f"  ✗ {server}: ALL routes failed (Tailscale, Public, Internal)")
            results[server] = False

    # Check alerts
    if output_dir.exists():
        alerts = check_alerts(output_dir)
    else:
        alerts = []

    # Save summary
    summary = {
        "collected_at": timestamp,
        "results": {s: "success" if ok else "failed" for s, ok in results.items()},
        "alerts": alerts,
    }

    if output_dir.exists():
        summary_file = output_dir / "summary.json"
        summary_file.write_text(json.dumps(summary, indent=2))

    # Print summary
    print("\n" + "=" * 50)
    print("Summary:")
    for server, ok in results.items():
        icon = "✓" if ok else "✗"
        print(f"  {icon} {server}")

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
