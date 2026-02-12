#!/usr/bin/env python3
"""
Safe SSH Wrapper Module.

This module provides safe SSH command execution with command validation
to prevent destructive operations.
"""

import re
import sys
from typing import Tuple, Optional, List


# Forbidden patterns for destructive operations
FORBIDDEN_PATTERNS: List[str] = [
    r'\brm\b', r'\brmdir\b', r'\bmkfs\b', r'\bdd\b',
    r'\bchmod\b.*7\d{2}', r'\bchown\b', r'\breboot\b',
    r'\bshutdown\b', r'\bhalt\b', r'\bpkill\b', r'\bkillall\b',
    r'\bsudo\b.*-E?', r'\bnano\b', r'\bvi\b', r'\bnvim\b',
    r'\bdocker\b.*rm\b', r'\bdocker\b.*rmi\b',
    r'\bsystemctl\b.*stop\b', r'\bsystemctl\b.*disable\b',
]


def validate_command(command: str) -> Tuple[bool, str]:
    """
    Validate command doesn't contain forbidden patterns.

    Args:
        command: The command to validate.

    Returns:
        Tuple of (is_valid, message).
    """
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, f"Command contains forbidden pattern: {pattern}"

    # Check for write operations to sensitive directories
    write_pattern = r'> /etc/|> /var/|> /root/'
    if re.search(write_pattern, command, re.IGNORECASE):
        return False, "Write operation detected to sensitive directory"

    return True, "OK"


def log_action(
    message: str,
    log_file: Optional[str] = None
) -> None:
    """Log an action to console and optionally to a file."""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)

    if log_file:
        try:
            with open(log_file, 'a') as f:
                f.write(log_entry + '\n')
        except IOError:
            pass


def safe_ssh_exec(
    host: str,
    port: int,
    username: str,
    command: str,
    log_file: Optional[str] = None
) -> Tuple[int, str, str]:
    """
    Execute SSH command with validation.

    Args:
        host: SSH host.
        port: SSH port.
        username: SSH username.
        command: Command to execute.
        log_file: Optional file to log actions.

    Returns:
        Tuple of (exit_code, stdout, stderr).
    """
    # Validate command
    valid, msg = validate_command(command)
    if not valid:
        log_action(f"BLOCKED: {msg}", log_file)
        log_action(f"Command: {command}", log_file)
        return 1, "", msg

    log_action(f"Executing: {command}", log_file)

    try:
        import paramiko
    except ImportError:
        # Fallback to subprocess if paramiko not available
        import subprocess
        ssh_cmd = [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "LogLevel=ERROR",
            "-o", "BatchMode=yes",
            "-p", str(port),
            f"{username}@{host}",
            command
        ]
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr

    # Use paramiko
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, timeout=30)

        stdin, stdout, stderr = ssh.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()
        return exit_code, output, error
    except Exception as e:
        return 1, "", str(e)


def main() -> None:
    """Main entry point for CLI usage."""
    if len(sys.argv) < 5:
        print("Usage: safe_ssh.py <host> <port> <user> <command> [log_file]")
        print()
        print("Example:")
        print("  python safe_ssh.py 192.168.1.60 2260 admin 'uptime'")
        print("  python safe_ssh.py 192.168.1.60 2260 admin 'df -h'")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    user = sys.argv[3]
    command = " ".join(sys.argv[4:])
    log_file = sys.argv[-1] if sys.argv[-1].startswith('/') else None

    exit_code, output, error = safe_ssh_exec(
        host, port, user, command, log_file
    )

    if output:
        print(output)
    if error:
        print(error, file=sys.stderr)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
