#!/usr/bin/env python3
"""
Network Debugging Script — Universal (Project-Agnostic).

Checks network connectivity to all servers via all methods.
Loads server config from servers.yml.
Cross-platform (Windows + Linux).
"""

import os
import sys
import json
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

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


def check_port(host: str, port: int, timeout: int = 3) -> bool:
    """Check TCP port reachability (cross-platform)."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def check_tailscale() -> Dict[str, Any]:
    """Check Tailscale status."""
    result = {"running": False, "ip": None, "peers": []}
    try:
        status = subprocess.run(
            ["tailscale", "status", "--json"],
            capture_output=True, text=True, timeout=5
        )
        if status.returncode == 0:
            data = json.loads(status.stdout)
            result["running"] = True
            self_node = data.get("Self", {})
            ts_ips = self_node.get("TailscaleIPs", [])
            if ts_ips:
                result["ip"] = ts_ips[0]
            peers = data.get("Peer", {})
            result["peers"] = list(peers.keys())[:5]
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    return result


def get_local_ip() -> str:
    """Get local IP (cross-platform)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "unknown"


def detect_best_route(local_ip: str) -> str:
    """Detect which network path works best."""
    if local_ip.startswith("100."):
        return "tailscale"
    elif local_ip.startswith("192.168.1."):
        return "internal"
    return "public"


def generate_report(config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate full network debug report from servers.yml config."""
    local_ip = get_local_ip()
    tailscale = check_tailscale()
    best_route = detect_best_route(local_ip)
    public_ip = config.get("network", {}).get("public_ip", "unknown")

    server_results = {}
    for name, info in config.get("servers", {}).items():
        srv = {"purpose": info["purpose"], "methods": {}}

        # Tailscale
        srv["methods"]["tailscale"] = {
            "host": info["tailscale_ip"],
            "port": info["ssh"]["port_tailscale"],
            "reachable": check_port(info["tailscale_ip"], info["ssh"]["port_tailscale"]),
        }

        # Public
        srv["methods"]["public"] = {
            "host": public_ip,
            "port": info["ssh"]["port_public"],
            "reachable": check_port(public_ip, info["ssh"]["port_public"]),
        }

        # Internal (only if on the same LAN)
        if local_ip.startswith("192.168.1."):
            srv["methods"]["internal"] = {
                "host": info["internal_ip"],
                "port": info["ssh"]["port_tailscale"],
                "reachable": check_port(info["internal_ip"], info["ssh"]["port_tailscale"]),
            }

        # Find best working method
        srv["best_method"] = None
        for method in [best_route, "tailscale", "public", "internal"]:
            if method in srv["methods"] and srv["methods"][method]["reachable"]:
                srv["best_method"] = method
                break

        server_results[name] = srv

    return {
        "timestamp": datetime.now().isoformat(),
        "platform": sys.platform,
        "local_ip": local_ip,
        "detected_route": best_route,
        "tailscale": tailscale,
        "servers": server_results,
    }


def main() -> None:
    """Main entry point."""
    config = load_config()
    report = generate_report(config)

    print("=== Network Debug Report ===")
    print(f"Platform: {report['platform']}")
    print(f"Local IP: {report['local_ip']}")
    print(f"Best route: {report['detected_route']}")
    ts = report["tailscale"]
    print(f"Tailscale: {'✓ running' if ts['running'] else '✗ not running'}")
    if ts["ip"]:
        print(f"Tailscale IP: {ts['ip']}")
    print()

    print("Server Connectivity:")
    for name, srv in report["servers"].items():
        best = srv["best_method"] or "UNREACHABLE"
        icon = "✓" if srv["best_method"] else "✗"
        print(f"  {icon} {name} ({srv['purpose']}): best={best}")
        for method, info in srv["methods"].items():
            status = "✓" if info["reachable"] else "✗"
            print(f"      {status} {method}: {info['host']}:{info['port']}")

    # Save JSON report
    output_dir = Path(__file__).resolve().parent.parent.parent / "evidence"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "network-debug.json"
    try:
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nSaved to: {output_file}")
    except IOError as e:
        print(f"\nCould not save: {e}")


if __name__ == "__main__":
    main()
