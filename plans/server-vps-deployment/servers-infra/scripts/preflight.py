#!/usr/bin/env python3
"""
Pre-flight Check Script — Universal (Project-Agnostic).

Runs before any deployment to verify:
- Disk space on target server
- Port availability
- Docker container status (protection of critical containers)
- Service health
- Connection availability

Loads server config from servers.yml.
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

try:
    import yaml
except ImportError:
    yaml = None


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


def ssh_exec(host: str, port: int, user: str, cmd: str, timeout: int = 15) -> Tuple[int, str]:
    """Execute read-only SSH command."""
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
             "-o", "StrictHostKeyChecking=no", "-o", "LogLevel=ERROR",
             "-p", str(port), f"{user}@{host}", cmd],
            capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return 1, "CONNECTION_FAILED"


def check_disk(host: str, port: int, user: str) -> Dict[str, Any]:
    """Check disk usage."""
    code, output = ssh_exec(host, port, user, "df -h / | tail -1 | awk '{print $5}' | tr -d '%'")
    if code == 0 and output.isdigit():
        usage = int(output)
        return {
            "status": "critical" if usage >= 90 else "warning" if usage >= 85 else "ok",
            "usage_pct": usage,
        }
    return {"status": "unknown", "error": output}


def check_port(host: str, port: int, user: str, target_port: int) -> Dict[str, Any]:
    """Check if a port is in use on the target server."""
    code, output = ssh_exec(host, port, user,
                            f"ss -tulpn | grep ':{target_port}' || echo 'PORT_FREE'")
    if "PORT_FREE" in output:
        return {"status": "free", "port": target_port}
    return {"status": "in_use", "port": target_port, "details": output}


def check_docker_containers(host: str, port: int, user: str,
                            protected: List[str]) -> Dict[str, Any]:
    """Check Docker container status and verify protected containers."""
    code, output = ssh_exec(host, port, user,
                            "docker ps --format '{{.Names}}\\t{{.Status}}' 2>/dev/null")
    if code != 0:
        return {"status": "docker_unavailable"}

    running = {}
    for line in output.strip().split('\n'):
        if '\t' in line:
            name, status = line.split('\t', 1)
            running[name] = status

    protected_status = {}
    for container in protected:
        if container in running:
            protected_status[container] = {"running": True, "status": running[container]}
        else:
            protected_status[container] = {"running": False, "status": "NOT RUNNING"}

    return {
        "total_running": len(running),
        "protected": protected_status,
        "all_protected_up": all(p["running"] for p in protected_status.values()),
    }


def check_services(host: str, port: int, user: str,
                    services: List[Dict]) -> Dict[str, Any]:
    """Check critical service status."""
    results = {}
    for svc in services:
        if svc.get("type") == "systemd":
            code, output = ssh_exec(host, port, user,
                                    f"systemctl is-active {svc['name']} 2>/dev/null")
            results[svc["name"]] = {
                "status": output if code == 0 else "inactive",
                "critical": svc.get("critical", False),
            }
    return results


def run_preflight(server_name: str, config: Dict[str, Any],
                  target_port: Optional[int] = None) -> Dict[str, Any]:
    """Run all pre-flight checks for a server."""
    server = config["servers"][server_name]
    host = server["tailscale_ip"]
    port = server["ssh"]["port_tailscale"]
    user = server["ssh"]["users"][0]

    print(f"\n{'='*50}")
    print(f"Pre-flight: {server_name} ({server['purpose']})")
    print(f"{'='*50}")

    results: Dict[str, Any] = {"server": server_name, "checks": {}}

    # 1. Disk check
    disk = check_disk(host, port, user)
    icon = "🔴" if disk["status"] == "critical" else "⚠️" if disk["status"] == "warning" else "✅"
    print(f"  {icon} Disk: {disk.get('usage_pct', '?')}%")
    results["checks"]["disk"] = disk

    # 2. Port check (if specified)
    if target_port:
        port_result = check_port(host, port, user, target_port)
        icon = "✅" if port_result["status"] == "free" else "🔴"
        print(f"  {icon} Port {target_port}: {port_result['status']}")
        results["checks"]["port"] = port_result

    # 3. Docker containers (protected check)
    protected = server.get("protected_containers", [])
    if protected:
        docker = check_docker_containers(host, port, user, protected)
        icon = "✅" if docker.get("all_protected_up") else "🔴"
        print(f"  {icon} Protected containers: {'all up' if docker.get('all_protected_up') else 'SOME DOWN'}")
        results["checks"]["docker"] = docker

    # 4. Service check
    services = server.get("services", [])
    critical_services = [s for s in services if s.get("critical")]
    if critical_services:
        svc_results = check_services(host, port, user, critical_services)
        failed = [name for name, info in svc_results.items()
                  if info["status"] != "active" and info["critical"]]
        icon = "✅" if not failed else "🔴"
        print(f"  {icon} Critical services: {len(critical_services) - len(failed)}/{len(critical_services)} active")
        if failed:
            print(f"      Failed: {', '.join(failed)}")
        results["checks"]["services"] = svc_results

    # Overall verdict
    blockers = []
    if disk.get("status") == "critical":
        blockers.append("disk space critical")
    if target_port and results["checks"].get("port", {}).get("status") == "in_use":
        blockers.append(f"port {target_port} in use")
    if not results["checks"].get("docker", {}).get("all_protected_up", True):
        blockers.append("protected containers down")

    results["verdict"] = "BLOCKED" if blockers else "CLEAR"
    results["blockers"] = blockers

    icon = "✅" if not blockers else "🔴"
    print(f"\n  {icon} VERDICT: {results['verdict']}")
    if blockers:
        print(f"     Blockers: {', '.join(blockers)}")

    return results


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: preflight.py <server> [port]")
        print("  server: s60, s61, s62")
        print("  port:   optional port to check availability")
        print()
        print("Example: python preflight.py s62 4321")
        sys.exit(1)

    config = load_config()
    server = sys.argv[1]
    target_port = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if server not in config.get("servers", {}):
        print(f"ERROR: Unknown server '{server}'. Available: {list(config['servers'].keys())}")
        sys.exit(1)

    result = run_preflight(server, config, target_port)
    sys.exit(0 if result["verdict"] == "CLEAR" else 1)


if __name__ == "__main__":
    main()
