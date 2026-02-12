#!/usr/bin/env python3
"""
Network Debugging Script — Cross-Platform (Windows + Linux).

Checks network connectivity using SSH config aliases.
Uses Python's socket module instead of nc/ping for portability.
"""

import socket
import subprocess
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional


# Server inventory — uses SSH config aliases from ~/.ssh/config
SERVERS = {
    "s60": {
        "aliases": {
            "tailscale": "s60pa",
            "public": "s60pa-pub",
            "internal": "s60pa-int",
        },
        "tailscale_ip": "100.111.141.111",
        "public_ip": "89.203.173.196",
        "internal_ip": "192.168.1.60",
        "ssh_port_tailscale": 20,
        "ssh_port_public": 2260,
        "purpose": "Hub/Backup",
    },
    "s61": {
        "aliases": {
            "tailscale": "s61pa",
            "public": "s61pa-pub",
            "internal": "s61pa-int",
        },
        "tailscale_ip": "100.111.141.112",
        "public_ip": "89.203.173.196",
        "internal_ip": "192.168.1.61",
        "ssh_port_tailscale": 20,
        "ssh_port_public": 2261,
        "purpose": "Gateway/Traefik",
    },
    "s62": {
        "aliases": {
            "tailscale": "s62pa",
            "public": "s62pa-pub",
            "internal": "s62pa-int",
        },
        "tailscale_ip": "100.91.164.109",
        "public_ip": "89.203.173.196",
        "internal_ip": "192.168.1.62",
        "ssh_port_tailscale": 20,
        "ssh_port_public": 2262,
        "purpose": "Production/Web",
    },
}


def check_port(host: str, port: int, timeout: int = 3) -> bool:
    """Check if a TCP port is reachable using Python socket (cross-platform)."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def check_tailscale() -> Dict[str, Any]:
    """Check Tailscale status (cross-platform)."""
    result = {"running": False, "ip": None, "peers": []}
    try:
        # Works on both Windows and Linux
        status = subprocess.run(
            ["tailscale", "status", "--json"],
            capture_output=True, text=True, timeout=5
        )
        if status.returncode == 0:
            data = json.loads(status.stdout)
            result["running"] = True
            # Get self IP
            self_node = data.get("Self", {})
            ts_ips = self_node.get("TailscaleIPs", [])
            if ts_ips:
                result["ip"] = ts_ips[0]
            # Get peer count
            peers = data.get("Peer", {})
            result["peers"] = list(peers.keys())[:5]
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    return result


def get_local_ip() -> str:
    """Get local IP (cross-platform, no external commands needed)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "unknown"


def test_ssh_alias(alias: str, timeout: int = 5) -> bool:
    """Test SSH connectivity using config alias (cross-platform)."""
    try:
        result = subprocess.run(
            ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "BatchMode=yes",
             alias, "echo ok"],
            capture_output=True, text=True, timeout=timeout + 5
        )
        return result.returncode == 0 and "ok" in result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def detect_best_route() -> str:
    """Detect which network path works best."""
    local_ip = get_local_ip()
    if local_ip.startswith("100."):
        return "tailscale"
    elif local_ip.startswith("192.168.1."):
        return "internal"
    return "public"


def generate_report() -> Dict[str, Any]:
    """Generate full network debug report."""
    local_ip = get_local_ip()
    tailscale = check_tailscale()
    best_route = detect_best_route()

    # Check all servers via all methods
    server_results = {}
    for name, info in SERVERS.items():
        srv = {"purpose": info["purpose"], "methods": {}}

        # Check Tailscale path
        srv["methods"]["tailscale"] = {
            "host": info["tailscale_ip"],
            "port": info["ssh_port_tailscale"],
            "reachable": check_port(info["tailscale_ip"], info["ssh_port_tailscale"]),
            "alias": info["aliases"]["tailscale"],
        }

        # Check public path
        srv["methods"]["public"] = {
            "host": info["public_ip"],
            "port": info["ssh_port_public"],
            "reachable": check_port(info["public_ip"], info["ssh_port_public"]),
            "alias": info["aliases"]["public"],
        }

        # Check internal path (only if we're on internal network)
        if local_ip.startswith("192.168.1."):
            srv["methods"]["internal"] = {
                "host": info["internal_ip"],
                "port": info["ssh_port_tailscale"],
                "reachable": check_port(info["internal_ip"], info["ssh_port_tailscale"]),
                "alias": info["aliases"]["internal"],
            }

        # Find best working method
        srv["best_alias"] = None
        for method in [best_route, "tailscale", "public", "internal"]:
            if method in srv["methods"] and srv["methods"][method]["reachable"]:
                srv["best_alias"] = info["aliases"][method]
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
    report = generate_report()

    print("=== Network Debug Report ===")
    print(f"Platform: {report['platform']}")
    print(f"Local IP: {report['local_ip']}")
    print(f"Best route: {report['detected_route']}")
    print(f"Tailscale: {'✓ running' if report['tailscale']['running'] else '✗ not running'}")
    if report["tailscale"]["ip"]:
        print(f"Tailscale IP: {report['tailscale']['ip']}")
    print()

    print("Server Connectivity:")
    for name, srv in report["servers"].items():
        best = srv["best_alias"] or "UNREACHABLE"
        icon = "✓" if srv["best_alias"] else "✗"
        print(f"  {icon} {name} ({srv['purpose']}): best={best}")
        for method, info in srv["methods"].items():
            status = "✓" if info["reachable"] else "✗"
            print(f"      {status} {method}: {info['host']}:{info['port']} ({info['alias']})")

    # Save JSON report
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "evidence")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "network-debug.json")
    try:
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nSaved to: {output_file}")
    except IOError as e:
        print(f"\nCould not save: {e}")


if __name__ == "__main__":
    main()
