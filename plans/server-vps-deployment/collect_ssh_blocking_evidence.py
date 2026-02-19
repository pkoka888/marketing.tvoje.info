#!/usr/bin/env python3
"""
SSH Port Blocking Evidence Collector
Run this script on target servers to collect all evidence for SSH port blocking investigation.

Usage:
    python3 collect_ssh_blocking_evidence.py [--server s60|s61|s62]
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

SERVER = os.environ.get("SERVER_NAME", "unknown")
OUTPUT_DIR = Path(f"/tmp/ssh-blocking-evidence-{SERVER}")
OUTPUT_DIR.mkdir(exist_ok=True)


def run_cmd(cmd: str) -> tuple[str, str]:
    """Run command and return (stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)


def write_file(filename: str, content: str):
    """Write content to file"""
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
        f.write(content)
    print(f"  ✓ {filename}")


def collect_firewall():
    """Collect firewall evidence"""
    print("\n[1] Firewall (iptables)")

    # iptables
    stdout, _ = run_cmd("sudo iptables -L -n -v --line-numbers 2>/dev/null")
    write_file("iptables-input.txt", stdout)

    stdout, _ = run_cmd("sudo iptables -L FORWARD -n -v --line-numbers 2>/dev/null")
    write_file("iptables-forward.txt", stdout)

    stdout, _ = run_cmd("sudo iptables -t nat -L -n -v 2>/dev/null")
    write_file("iptables-nat.txt", stdout)


def collect_ufw():
    """Collect UFW evidence"""
    print("\n[2] UFW Firewall")

    stdout, _ = run_cmd("sudo ufw status verbose 2>/dev/null")
    write_file("ufw-status.txt", stdout)

    stdout, _ = run_cmd("sudo ufw status numbered 2>/dev/null")
    write_file("ufw-status-numbered.txt", stdout)

    # UFW config files
    for f in ["ufw.conf", "default/ufw", "default/input", "default/forward"]:
        path = f"/etc/{f}"
        if os.path.exists(path):
            stdout, _ = run_cmd(f"sudo cat {path}")
            write_file(f.replace("/", "-"), stdout)


def collect_ssh():
    """Collect SSH evidence"""
    print("\n[3] SSH Daemon")

    # sshd_config
    stdout, _ = run_cmd("sudo cat /etc/ssh/sshd_config")
    write_file("sshd_config.txt", stdout)

    # sshd_config.d
    stdout, _ = run_cmd("sudo ls -la /etc/ssh/sshd_config.d/ 2>/dev/null")
    write_file("sshd_config_d-list.txt", stdout)

    # Individual files in sshd_config.d
    stdout, _ = run_cmd("sudo cat /etc/ssh/sshd_config.d/*.conf 2>/dev/null")
    write_file("sshd_config_d-content.txt", stdout)

    # Listening ports
    stdout, _ = run_cmd('sudo ss -tlnp | grep -E "ssh|22|226"')
    write_file("ss-listening.txt", stdout)

    # SSH auth logs
    stdout, _ = run_cmd("sudo tail -500 /var/log/auth.log 2>/dev/null | grep -i ssh")
    write_file("auth-log-ssh.txt", stdout)


def collect_fail2ban():
    """Collect fail2ban evidence"""
    print("\n[4] Fail2ban")

    stdout, _ = run_cmd("sudo fail2ban-client status 2>/dev/null")
    write_file("fail2ban-status.txt", stdout)

    stdout, _ = run_cmd("sudo fail2ban-client get sshd banip 2>/dev/null")
    write_file("fail2ban-banned.txt", stdout)

    stdout, _ = run_cmd("sudo fail2ban-client get sshd failregex 2>/dev/null")
    write_file("fail2ban-failregex.txt", stdout)

    stdout, _ = run_cmd("sudo cat /etc/fail2ban/jail.local 2>/dev/null")
    write_file("fail2ban-jail-local.txt", stdout)

    stdout, _ = run_cmd("sudo ls -la /etc/fail2ban/jail.d/ 2>/dev/null")
    write_file("fail2ban-jail-d-list.txt", stdout)

    stdout, _ = run_cmd("sudo tail -1000 /var/log/fail2ban.log 2>/dev/null")
    write_file("fail2ban-log.txt", stdout)


def collect_network():
    """Collect network evidence"""
    print("\n[5] Network")

    stdout, _ = run_cmd("ip addr")
    write_file("ip-addr.txt", stdout)

    stdout, _ = run_cmd("ip route")
    write_file("ip-route.txt", stdout)

    stdout, _ = run_cmd("ip neigh")
    write_file("ip-neigh.txt", stdout)

    stdout, _ = run_cmd("cat /etc/resolv.conf")
    write_file("resolv-conf.txt", stdout)

    stdout, _ = run_cmd("cat /etc/hosts")
    write_file("hosts.txt", stdout)


def collect_system():
    """Collect system evidence"""
    print("\n[6] System")

    stdout, _ = run_cmd(
        "systemctl status sshd 2>/dev/null || systemctl status ssh 2>/dev/null"
    )
    write_file("systemd-ssh-status.txt", stdout)

    stdout, _ = run_cmd("sudo getenforce 2>/dev/null")
    write_file("selinux-status.txt", stdout)

    stdout, _ = run_cmd("sudo aa-status 2>/dev/null")
    write_file("apparmor-status.txt", stdout)

    stdout, _ = run_cmd("cat /etc/security/limits.conf")
    write_file("limits-conf.txt", stdout)

    stdout, _ = run_cmd("sudo ss -tlnp 2>/dev/null")
    write_file("ss-all-listening.txt", stdout)


def collect_docker():
    """Collect Docker evidence"""
    print("\n[7] Docker")

    stdout, _ = run_cmd("sudo docker network ls 2>/dev/null")
    write_file("docker-network-ls.txt", stdout)

    stdout, _ = run_cmd("sudo iptables -L DOCKER -n -v 2>/dev/null")
    write_file("iptables-docker.txt", stdout)


def collect_tcpwrappers():
    """Collect TCP wrappers evidence"""
    print("\n[8] TCP Wrappers")

    stdout, _ = run_cmd("cat /etc/hosts.allow 2>/dev/null")
    write_file("hosts-allow.txt", stdout)

    stdout, _ = run_cmd("cat /etc/hosts.deny 2>/dev/null")
    write_file("hosts-deny.txt", stdout)


def main():
    print(f"SSH Port Blocking Evidence Collector")
    print(f"Server: {SERVER}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Started: {datetime.now().isoformat()}")

    # Create summary
    summary = f"""SSH Port Blocking Evidence - {SERVER}
========================================
Collected: {datetime.now().isoformat()}

This evidence was collected to investigate why SSH port 2262 is not 
accessible from public IP but works via jumphost.

Evidence categories:
1. Firewall (iptables)
2. UFW
3. SSH Daemon
4. Fail2ban
5. Network
6. System
7. Docker
8. TCP Wrappers
"""
    write_file("README.txt", summary)

    collect_firewall()
    collect_ufw()
    collect_ssh()
    collect_fail2ban()
    collect_network()
    collect_system()
    collect_docker()
    collect_tcpwrappers()

    print(f"\n✓ Evidence collected to: {OUTPUT_DIR}")
    print(f"\nTo copy evidence:")
    print(f"  scp -r -P 2260 <user>@89.203.173.196:{OUTPUT_DIR} .")


if __name__ == "__main__":
    main()
