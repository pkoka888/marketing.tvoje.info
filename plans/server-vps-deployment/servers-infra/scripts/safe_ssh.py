#!/usr/bin/env python3
"""
Safe SSH Wrapper — Universal (Project-Agnostic).

Validates commands against a blocklist before execution.
Prevents destructive operations on production servers.
Loads server config from servers.yml.
"""

import re
import sys
import subprocess
from typing import Tuple, Optional, List
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


# Forbidden patterns — blocks destructive commands
FORBIDDEN_PATTERNS: List[str] = [
    r'\brm\b', r'\brmdir\b', r'\bmkfs\b', r'\bdd\b',
    r'\bchmod\b.*7\d{2}', r'\bchown\b', r'\breboot\b',
    r'\bshutdown\b', r'\bhalt\b', r'\bpkill\b', r'\bkillall\b',
    r'\bkill\b\s+-9', r'\bsudo\b',
    r'\bdocker\b.*\brm\b', r'\bdocker\b.*\brmi\b', r'\bdocker\b.*\bprune\b',
    r'\bsystemctl\b.*\bstop\b', r'\bsystemctl\b.*\bdisable\b',
    r'\bapt\b.*\bremove\b', r'\bapt\b.*\bpurge\b',
    r'\bnano\b', r'\bvi\b', r'\bnvim\b',
    r'\bcurl\b.*\|\s*bash', r'\bwget\b.*\|\s*bash',
]

# Sensitive directories — block write operations to these
SENSITIVE_PATHS = ['/etc/', '/root/', '/boot/', '/usr/']


def load_servers() -> dict:
    """Load server configuration from servers.yml."""
    config_path = Path(__file__).resolve().parent.parent / "servers.yml"
    if config_path.exists() and yaml:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f).get('servers', {})
    return {}


def validate_command(command: str) -> Tuple[bool, str]:
    """
    Validate command against forbidden patterns.

    Returns:
        Tuple of (is_valid, message).
    """
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, f"BLOCKED: matches forbidden pattern '{pattern}'"

    # Block write operations to sensitive directories
    for path in SENSITIVE_PATHS:
        if re.search(rf'>\s*{re.escape(path)}', command):
            return False, f"BLOCKED: write to sensitive path '{path}'"

    return True, "OK"


def log_action(message: str, log_file: Optional[str] = None) -> None:
    """Log an action with timestamp."""
    from datetime import datetime
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{ts}] {message}"
    print(entry)
    if log_file:
        try:
            with open(log_file, 'a') as f:
                f.write(entry + '\n')
        except IOError:
            pass


def safe_ssh_exec(
    host: str, port: int, username: str, command: str,
    log_file: Optional[str] = None
) -> Tuple[int, str, str]:
    """Execute SSH command with safety validation."""
    valid, msg = validate_command(command)
    if not valid:
        log_action(f"BLOCKED: {msg} | cmd: {command}", log_file)
        return 1, "", msg

    log_action(f"EXEC: {username}@{host}:{port} → {command}", log_file)

    try:
        result = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no",
             "-o", "UserKnownHostsFile=/dev/null",
             "-o", "LogLevel=ERROR",
             "-o", "BatchMode=yes",
             "-o", "ConnectTimeout=10",
             "-p", str(port),
             f"{username}@{host}", command],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "TIMEOUT"
    except Exception as e:
        return 1, "", str(e)


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 5:
        print("Usage: safe_ssh.py <host> <port> <user> <command>")
        print()
        print("Examples:")
        print("  python safe_ssh.py 100.91.164.109 20 admin 'uptime'")
        print("  python safe_ssh.py 100.91.164.109 20 admin 'df -h'")
        print()
        print("Blocked commands: rm, reboot, shutdown, docker rm, etc.")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    user = sys.argv[3]
    command = " ".join(sys.argv[4:])

    code, stdout, stderr = safe_ssh_exec(host, port, user, command)
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)
    sys.exit(code)


if __name__ == "__main__":
    main()
