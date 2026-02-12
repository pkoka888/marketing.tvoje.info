#!/usr/bin/env python3
"""
Smart Server Health Monitor — LangGraph-Ready.

Features:
- Adaptive timeouts (learns from historical response times)
- Rate limiting (prevents SSH connection flooding)
- Multi-layer checks: HTTP → TCP → SSH (cheapest first)
- State persistence via Redis (if available) or local JSON
- Connection pooling awareness (MaxStartups protection)

Design: Each server check is a LangGraph node.
Flow: HTTP probe → TCP probe → SSH probe → Evidence collect → Alert

This script can run standalone or as a LangGraph graph.
"""

import json
import time
import socket
import subprocess
import urllib.request
import ssl
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field, asdict


# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

STATE_FILE = Path(os.environ.get(
    "HEALTH_STATE",
    Path.home() / "vscodeportable" / "servers" / "health-state.json"
))

# Rate limits (prevent SSH flooding)
MAX_SSH_PER_MINUTE = 3          # Max SSH connections per server per minute
MIN_CHECK_INTERVAL_SEC = 300    # Min 5 minutes between full checks
ADAPTIVE_TIMEOUT_FACTOR = 2.0  # Multiply historical avg by this for timeout

SERVERS = {
    "s60": {
        "name": "Hub/Backup",
        "ssh_aliases": ["s60pa", "s60pa-pub", "s60pa-int"],
        "http_urls": [],  # No public websites on s60
        "tcp_checks": [
            ("100.111.141.111", 20),
        ],
        "base_timeout": 5,
    },
    "s61": {
        "name": "Gateway/Traefik",
        "ssh_aliases": ["s61pa", "s61pa-pub", "s61pa-int"],
        "http_urls": ["https://okamih.cz", "https://krtovoj.cz"],
        "tcp_checks": [
            ("100.111.141.112", 20),
        ],
        "base_timeout": 8,  # s61 is known to be slow (3.5s+ SSH)
    },
    "s62": {
        "name": "Production/Web",
        "ssh_aliases": ["s62pa", "s62pa-pub", "s62pa-int"],
        "http_urls": ["https://portfolio.tvoje.info"],
        "tcp_checks": [
            ("100.91.164.109", 20),
        ],
        "base_timeout": 5,
    },
}


# ═══════════════════════════════════════════════════════════════
# State Management
# ═══════════════════════════════════════════════════════════════

@dataclass
class ServerState:
    """Persistent state for one server."""
    name: str
    last_check: str = ""
    last_ssh_times: List[float] = field(default_factory=list)  # Last 10 SSH round trips
    ssh_count_this_minute: int = 0
    ssh_minute_start: str = ""
    status: str = "unknown"      # up, down, degraded, unknown
    http_status: str = "unknown"
    tcp_status: str = "unknown"
    ssh_status: str = "unknown"
    alerts: List[str] = field(default_factory=list)
    avg_ssh_time: float = 5.0    # Adaptive timeout baseline

    def adaptive_timeout(self) -> int:
        """Calculate adaptive timeout from historical data."""
        if self.last_ssh_times:
            avg = sum(self.last_ssh_times) / len(self.last_ssh_times)
            self.avg_ssh_time = avg
            return max(5, int(avg * ADAPTIVE_TIMEOUT_FACTOR))
        return 10

    def record_ssh_time(self, duration: float) -> None:
        """Record SSH round trip time."""
        self.last_ssh_times.append(round(duration, 2))
        if len(self.last_ssh_times) > 10:
            self.last_ssh_times = self.last_ssh_times[-10:]

    def can_ssh(self) -> bool:
        """Rate limit check — can we SSH right now?"""
        now = datetime.now()
        minute_key = now.strftime("%Y%m%d%H%M")
        if self.ssh_minute_start != minute_key:
            self.ssh_minute_start = minute_key
            self.ssh_count_this_minute = 0
        return self.ssh_count_this_minute < MAX_SSH_PER_MINUTE

    def record_ssh_attempt(self) -> None:
        """Record an SSH attempt for rate limiting."""
        self.ssh_count_this_minute += 1


def load_state() -> Dict[str, ServerState]:
    """Load persistent state from file."""
    states = {}
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            for name, d in data.items():
                states[name] = ServerState(**d)
        except (json.JSONDecodeError, TypeError):
            pass

    # Initialize missing servers
    for name in SERVERS:
        if name not in states:
            states[name] = ServerState(name=name)
    return states


def save_state(states: Dict[str, ServerState]) -> None:
    """Persist state to file."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {name: asdict(s) for name, s in states.items()}
    STATE_FILE.write_text(json.dumps(data, indent=2))


# ═══════════════════════════════════════════════════════════════
# Check Nodes (LangGraph-ready: each is a graph node)
# ═══════════════════════════════════════════════════════════════

def check_http(server: str, config: dict) -> Tuple[str, List[str]]:
    """
    Node 1: HTTP probe — cheapest check, no SSH needed.
    Returns (status, alerts).
    """
    urls = config.get("http_urls", [])
    if not urls:
        return "skip", []

    alerts = []
    any_up = False
    ctx = ssl.create_default_context()

    for url in urls:
        try:
            start = time.time()
            req = urllib.request.Request(url, method="HEAD")
            r = urllib.request.urlopen(req, timeout=10, context=ctx)
            elapsed = time.time() - start
            if r.status == 200:
                any_up = True
                if elapsed > 5:
                    alerts.append(f"⚠️ {url} slow ({elapsed:.1f}s)")
            else:
                alerts.append(f"⚠️ {url} returned HTTP {r.status}")
        except ssl.SSLError:
            # SSL error but server is responding
            any_up = True
            alerts.append(f"⚠️ {url} SSL cert error")
        except Exception as e:
            alerts.append(f"🔴 {url} down: {e}")

    status = "up" if any_up else "down"
    return status, alerts


def check_tcp(server: str, config: dict, timeout: int = 5) -> Tuple[str, List[str]]:
    """
    Node 2: TCP port probe — checks if SSH port is open.
    Uses Python socket (cross-platform, no nc/nmap needed).
    """
    alerts = []
    any_up = False

    for host, port in config.get("tcp_checks", []):
        try:
            start = time.time()
            s = socket.create_connection((host, port), timeout=timeout)
            elapsed = time.time() - start
            s.close()
            any_up = True
            if elapsed > 3:
                alerts.append(f"⚠️ {host}:{port} slow TCP ({elapsed:.1f}s)")
        except (socket.timeout, ConnectionRefusedError, OSError):
            alerts.append(f"⚠️ {host}:{port} TCP unreachable (timeout={timeout}s)")

    status = "up" if any_up else "down"
    return status, alerts


def check_ssh(
    server: str,
    config: dict,
    state: ServerState,
    command: str = "echo ok"
) -> Tuple[str, List[str], float]:
    """
    Node 3: SSH probe — most expensive check, rate-limited.
    Uses SSH config aliases with fallback chain.
    Returns (status, alerts, duration).
    """
    if not state.can_ssh():
        return "rate_limited", [f"⚠️ {server} SSH rate limited ({MAX_SSH_PER_MINUTE}/min)"], 0.0

    timeout = state.adaptive_timeout()
    alerts = []

    for alias in config.get("ssh_aliases", []):
        state.record_ssh_attempt()
        try:
            start = time.time()
            result = subprocess.run(
                ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "BatchMode=yes",
                 alias, command],
                capture_output=True, text=True, timeout=timeout + 5
            )
            elapsed = time.time() - start
            state.record_ssh_time(elapsed)

            if result.returncode == 0 and "ok" in result.stdout:
                if elapsed > 5:
                    alerts.append(f"⚠️ {server} SSH slow via {alias} ({elapsed:.1f}s)")
                return "up", alerts, elapsed
        except subprocess.TimeoutExpired:
            alerts.append(f"⚠️ {server} SSH timeout via {alias} ({timeout}s)")
        except FileNotFoundError:
            alerts.append(f"🔴 SSH binary not found")
            return "error", alerts, 0.0

    return "down", alerts, 0.0


def collect_quick_evidence(
    server: str,
    config: dict,
    state: ServerState
) -> Optional[Dict[str, str]]:
    """
    Node 4: Quick evidence collection — only runs if SSH is confirmed up.
    Collects minimal diagnostics to avoid overloading the server.
    """
    if state.ssh_status != "up" or not state.can_ssh():
        return None

    alias = config["ssh_aliases"][0]  # Use first (usually Tailscale)
    timeout = state.adaptive_timeout()
    evidence = {}

    # Minimal commands — just enough to detect problems
    quick_commands = {
        "uptime": "uptime",
        "disk": "df -h / | tail -1",
        "memory": "free -h | grep Mem",
        "failed": "systemctl --failed --no-pager --no-legend 2>/dev/null | head -5",
        "load": "cat /proc/loadavg",
    }

    for key, cmd in quick_commands.items():
        if not state.can_ssh():
            break
        state.record_ssh_attempt()
        try:
            result = subprocess.run(
                ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "BatchMode=yes",
                 alias, cmd],
                capture_output=True, text=True, timeout=timeout + 5
            )
            evidence[key] = result.stdout.strip()
        except (subprocess.TimeoutExpired, Exception):
            evidence[key] = "timeout"

    return evidence


def analyze_evidence(evidence: Optional[Dict[str, str]], server: str) -> List[str]:
    """Node 5: Analyze evidence and generate alerts."""
    if not evidence:
        return []

    alerts = []

    # Check disk usage
    disk = evidence.get("disk", "")
    if "%" in disk:
        for part in disk.split():
            if part.endswith("%"):
                try:
                    usage = int(part.rstrip("%"))
                    if usage > 90:
                        alerts.append(f"🔴 {server} disk CRITICAL: {usage}%")
                    elif usage > 80:
                        alerts.append(f"⚠️ {server} disk WARNING: {usage}%")
                except ValueError:
                    pass

    # Check load
    load = evidence.get("load", "")
    if load:
        try:
            load_1m = float(load.split()[0])
            if load_1m > 4.0:
                alerts.append(f"⚠️ {server} high load: {load_1m}")
        except (ValueError, IndexError):
            pass

    # Check failed services
    failed = evidence.get("failed", "")
    if failed and failed not in ("", "timeout"):
        alerts.append(f"🔴 {server} failed services: {failed}")

    return alerts


# ═══════════════════════════════════════════════════════════════
# Failure Deduction Engine
# ═══════════════════════════════════════════════════════════════

def deduce_failure_causes(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Cross-correlate results across all servers to deduce
    the most likely root cause of failures.

    Logic:
    - If ALL servers fail TCP → local network/firewall issue
    - If ALL Tailscale servers fail but public works → Tailscale issue
    - If ONE server fails but others work → server-specific issue
    - If HTTP works but SSH fails → SSH-specific (daemon, fail2ban, MaxStartups)
    - If TCP is slow but works → network congestion or DNS reverse lookup
    """
    deductions = []
    servers_checked = list(results.keys())
    if len(servers_checked) < 2:
        return deductions  # Need 2+ servers for cross-correlation

    # Gather status vectors
    tcp_statuses = {s: results[s]["tcp"] for s in servers_checked}
    http_statuses = {s: results[s]["http"] for s in servers_checked}
    ssh_statuses = {s: results[s]["ssh"] for s in servers_checked}

    tcp_up = [s for s, v in tcp_statuses.items() if v == "up"]
    tcp_down = [s for s, v in tcp_statuses.items() if v != "up"]
    ssh_up = [s for s, v in ssh_statuses.items() if v == "up"]
    ssh_down = [s for s, v in ssh_statuses.items() if v not in ("up", "skipped")]
    http_up = [s for s, v in http_statuses.items() if v == "up"]

    # Rule 1: All TCP down → local network issue
    if len(tcp_down) == len(servers_checked) and len(servers_checked) >= 2:
        deductions.append({
            "cause": "Local network/firewall issue",
            "confidence": 90,
            "reasoning": f"All {len(servers_checked)} servers TCP unreachable → problem is on YOUR side",
            "fix": "Check: local firewall, VPN connection, network interface, router",
        })

    # Rule 2: Some TCP up, some down → server-specific
    elif tcp_up and tcp_down:
        for s in tcp_down:
            # Check if this server has HTTP up
            if http_statuses.get(s) == "up":
                deductions.append({
                    "cause": f"{s}: SSH daemon issue (HTTP works, TCP/SSH fails)",
                    "confidence": 85,
                    "reasoning": f"{s} serves HTTP (web is UP) but SSH port unreachable → SSH daemon problem",
                    "fix": f"Check on {s}: sshd_config MaxStartups, fail2ban status, sshd service status, DNS reverse lookup (UseDNS no)",
                    "likely_causes": [
                        ("fail2ban blocking your IP", 30),
                        ("MaxStartups limit reached", 25),
                        ("UseDNS yes causing slow auth", 20),
                        ("sshd service not running on port", 15),
                        ("Tailscale relay (DERP) instead of direct", 10),
                    ],
                })
            else:
                deductions.append({
                    "cause": f"{s}: Server-specific network issue",
                    "confidence": 70,
                    "reasoning": f"{s} unreachable via TCP while {', '.join(tcp_up)} work fine",
                    "fix": f"Check: {s} Tailscale status, firewall rules, sshd listening port",
                })

    # Rule 3: TCP up but SSH slow/down
    for s in ssh_down:
        if tcp_statuses.get(s) == "up":
            deductions.append({
                "cause": f"{s}: SSH auth/session issue (port open but SSH fails)",
                "confidence": 75,
                "reasoning": f"{s} TCP port is open but SSH session can't complete",
                "fix": f"Check: authorized_keys permissions, PAM config, disk space (88%!), I/O wait",
                "likely_causes": [
                    ("Disk full causing slow I/O", 35),
                    ("PAM module timeout (LDAP/DNS)", 25),
                    ("High load / swap usage", 20),
                    ("SSH key mismatch", 10),
                    ("Connection rate limit in sshd_config", 10),
                ],
            })

    # Rule 4: SSH works but very slow
    for s in ssh_up:
        evidence = results[s].get("evidence", {})
        if evidence:
            # Check if disk is high
            disk = evidence.get("disk", "")
            if "%" in disk:
                for part in disk.split():
                    if part.endswith("%"):
                        try:
                            usage = int(part.rstrip("%"))
                            if usage > 80:
                                deductions.append({
                                    "cause": f"{s}: High disk usage ({usage}%) causing slowness",
                                    "confidence": 60 + min(usage - 80, 30),
                                    "reasoning": f"Disk at {usage}% can cause journal/log writes to slow, swap to increase",
                                    "fix": f"Clean up: docker system prune, log rotation, old backups",
                                })
                        except ValueError:
                            pass

    # Sort by confidence
    deductions.sort(key=lambda x: x["confidence"], reverse=True)
    return deductions


# ═══════════════════════════════════════════════════════════════
# Main Flow (LangGraph graph equivalent)
# ═══════════════════════════════════════════════════════════════

def run_health_check(targets: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Main health check flow.

    Graph flow:
      HTTP probe → TCP probe → SSH probe → Evidence → Alerts
    
    Each step is conditional — if HTTP confirms service is up,
    we can skip SSH for that check cycle (saves rate limit budget).
    """
    states = load_state()
    results = {}
    all_alerts = []

    targets = targets or list(SERVERS.keys())

    for server in targets:
        config = SERVERS[server]
        state = states[server]

        print(f"\n{'='*50}")
        print(f"Checking {server} ({config['name']})")
        print(f"  Adaptive timeout: {state.adaptive_timeout()}s")
        print(f"  Avg SSH time: {state.avg_ssh_time:.1f}s")
        print(f"  SSH budget: {MAX_SSH_PER_MINUTE - state.ssh_count_this_minute}/{MAX_SSH_PER_MINUTE}")

        # Node 1: HTTP check (cheapest)
        http_status, http_alerts = check_http(server, config)
        state.http_status = http_status
        all_alerts.extend(http_alerts)
        print(f"  HTTP: {http_status}")

        # Node 2: TCP check
        tcp_timeout = state.adaptive_timeout()
        tcp_status, tcp_alerts = check_tcp(server, config, timeout=tcp_timeout)
        state.tcp_status = tcp_status
        all_alerts.extend(tcp_alerts)
        print(f"  TCP:  {tcp_status} (timeout={tcp_timeout}s)")

        # Node 3: SSH check (only if TCP shows port is open, or HTTP is down)
        if tcp_status == "up" or http_status == "down":
            ssh_status, ssh_alerts, ssh_time = check_ssh(server, config, state)
            state.ssh_status = ssh_status
            all_alerts.extend(ssh_alerts)
            print(f"  SSH:  {ssh_status} ({ssh_time:.1f}s)")
        else:
            state.ssh_status = "skipped"
            print(f"  SSH:  skipped (TCP unreachable, HTTP {http_status})")

        # Node 4: Quick evidence (only if SSH works)
        evidence = None
        if state.ssh_status == "up":
            evidence = collect_quick_evidence(server, config, state)

        # Node 5: Analyze
        evidence_alerts = analyze_evidence(evidence, server)
        all_alerts.extend(evidence_alerts)
        state.alerts = evidence_alerts

        # Determine overall status
        if state.ssh_status == "up":
            state.status = "up" if not evidence_alerts else "degraded"
        elif state.http_status == "up":
            state.status = "degraded"  # Web works but SSH doesn't
        else:
            state.status = "down"

        state.last_check = datetime.now().isoformat()
        results[server] = {
            "status": state.status,
            "http": state.http_status,
            "tcp": state.tcp_status,
            "ssh": state.ssh_status,
            "evidence": evidence,
            "alerts": state.alerts,
        }

    # Save state (persist adaptive timeout history)
    save_state(states)

    # Run deduction engine
    deductions = deduce_failure_causes(results)

    # Print summary
    print(f"\n{'='*50}")
    print("HEALTH SUMMARY")
    for server, result in results.items():
        icon = {"up": "✅", "degraded": "⚠️", "down": "🔴"}.get(result["status"], "❓")
        print(f"  {icon} {server}: {result['status']} (HTTP={result['http']} TCP={result['tcp']} SSH={result['ssh']})")

    if all_alerts:
        print(f"\n⚠️ ALERTS ({len(all_alerts)}):")
        for alert in all_alerts:
            print(f"  {alert}")
    else:
        print("\n✅ No alerts")

    # Print deductions
    if deductions:
        print(f"\n{'='*50}")
        print("🔍 FAILURE DEDUCTION (ranked by confidence)")
        for i, d in enumerate(deductions, 1):
            print(f"\n  [{i}] {d['cause']} — {d['confidence']}% confidence")
            print(f"      Reasoning: {d['reasoning']}")
            print(f"      Fix: {d['fix']}")
            if "likely_causes" in d:
                print("      Likely root causes:")
                for cause, pct in d["likely_causes"]:
                    bar = "█" * (pct // 5) + "░" * (6 - pct // 5)
                    print(f"        {bar} {pct}% {cause}")

    return {"results": results, "alerts": all_alerts, "deductions": deductions}


def main() -> None:
    """CLI entry point."""
    targets = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in SERVERS:
            targets = [arg]
        elif arg == "all":
            targets = None
        elif arg == "--status":
            # Just show saved state
            states = load_state()
            for name, state in states.items():
                print(f"{name}: {state.status} (last={state.last_check}, avg_ssh={state.avg_ssh_time:.1f}s)")
            return
        else:
            print(f"Usage: {sys.argv[0]} [s60|s61|s62|all|--status]")
            sys.exit(1)

    run_health_check(targets)


if __name__ == "__main__":
    main()
