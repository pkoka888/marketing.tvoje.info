#!/usr/bin/env python3
"""
Service Restart Script — Universal (Project-Agnostic).

Restarts nginx, pm2, and docker services across all servers with proper
validation, logging, and error analysis.
Uses safe_ssh.py infrastructure for command validation.

Usage:
    python restart_all_services.py --servers s60,s62 --services nginx,pm2
    python restart_all_services.py --all
    python restart_all_services.py --servers s62 --services pm2 --check-only
"""

import argparse
import sys
import time
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

# Try to import yaml for server config
try:
    import yaml
except ImportError:
    yaml = None

# Server configuration
SERVERS = {
    "s60": {"host": "192.168.1.60", "port": 20, "user": "admin", "purpose": "Hub/Backup"},
    "s61": {"host": "192.168.1.61", "port": 20, "user": "admin", "purpose": "Gateway/Traefik"},
    "s62": {"host": "192.168.1.62", "port": 20, "user": "admin", "purpose": "Production/Web"},
}

# Services available on each server
SERVER_SERVICES = {
    "s60": ["nginx", "pm2", "docker"],
    "s61": ["nginx", "traefik", "docker"],
    "s62": ["nginx", "pm2", "docker"],
}

# Commands that require human approval (per agent-sysadmin.md)
REQUIRE_APPROVAL = {
    "s61": ["nginx", "traefik", "docker"],  # s61 is critical - all require approval
    "s60": ["nginx", "docker"],
    "s62": ["nginx", "docker"],
}

# Protected containers on s61 (from agent-sysadmin.md)
PROTECTED_CONTAINERS = [
    "traefik", "netbox", "netbox-redis", "netbox-postgres", "homarr-dashboard"
]


def log_action(message: str, log_file: Optional[str] = None) -> None:
    """Log an action with timestamp."""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{ts}] {message}"
    print(entry)
    if log_file:
        try:
            with open(log_file, 'a') as f:
                f.write(entry + '\n')
        except IOError:
            pass


def validate_command(command: str) -> tuple[bool, str]:
    """
    Validate command against forbidden patterns.
    Uses same validation as safe_ssh.py.
    """
    # Forbidden patterns - but specifically allow certain restart commands
    forbidden = [
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

    for pattern in forbidden:
        if re.search(pattern, command, re.IGNORECASE):
            return False, f"BLOCKED: matches forbidden pattern '{pattern}'"

    return True, "OK"


def check_approval_required(server: str, service: str) -> bool:
    """Check if the service restart requires human approval."""
    return service in REQUIRE_APPROVAL.get(server, [])


def run_ssh_command(
    host: str,
    port: int,
    username: str,
    command: str,
    log_file: Optional[str] = None
) -> tuple[int, str, str]:
    """Execute SSH command with validation."""
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
             "-o", "ConnectTimeout=30",
             "-p", str(port),
             f"{username}@{host}", command],
            capture_output=True, text=True, timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "TIMEOUT"
    except Exception as e:
        return 1, "", str(e)


def restart_nginx(server: str, config: dict, log_file: Optional[str] = None) -> bool:
    """Restart nginx service on a server."""
    log_action(f"Restarting nginx on {server}...", log_file)

    # Test config first
    code, stdout, stderr = run_ssh_command(
        config["host"], config["port"], config["user"],
        "sudo nginx -t", log_file
    )

    if code != 0:
        log_action(f"ERROR: nginx config test failed on {server}: {stderr}", log_file)
        return False

    # Reload nginx (safer than restart)
    code, stdout, stderr = run_ssh_command(
        config["host"], config["port"], config["user"],
        "sudo systemctl reload nginx", log_file
    )

    if code != 0:
        log_action(f"ERROR: nginx reload failed on {server}: {stderr}", log_file)
        return False

    log_action(f"SUCCESS: nginx reloaded on {server}", log_file)
    return True


def restart_pm2(server: str, config: dict, project_name: str = "portfolio", log_file: Optional[str] = None) -> bool:
    """Restart PM2 process for a project."""
    log_action(f"Restarting PM2 process '{project_name}' on {server}...", log_file)

    # Check if process exists first
    code, stdout, stderr = run_ssh_command(
        config["host"], config["port"], config["user"],
        f"pm2 describe {project_name}", log_file
    )

    if code != 0:
        log_action(f"WARNING: PM2 process '{project_name}' not found on {server}", log_file)
        return False

    # Restart the process
    code, stdout, stderr = run_ssh_command(
        config["host"], config["port"], config["user"],
        f"pm2 restart {project_name}", log_file
    )

    if code != 0:
        log_action(f"ERROR: PM2 restart failed on {server}: {stderr}", log_file)
        return False

    log_action(f"SUCCESS: PM2 process '{project_name}' restarted on {server}", log_file)
    return True


def restart_docker_container(
    server: str,
    config: dict,
    container_name: str,
    log_file: Optional[str] = None
) -> bool:
    """Restart a specific Docker container."""
    # Check if container is protected
    if container_name in PROTECTED_CONTAINERS:
        log_action(f"ERROR: Cannot restart protected container '{container_name}' on {server}", log_file)
        return False

    log_action(f"Restarting Docker container '{container_name}' on {server}...", log_file)

    # Check if container exists
    code, stdout, stderr = run_ssh_command(
        config["host"], config["port"], config["user"],
        f"docker ps --filter name={container_name} --format '{{{{.Names}}}}'", log_file
    )

    if container_name not in stdout:
        log_action(f"WARNING: Container '{container_name}' not found on {server}", log_file)
        return False

    # Restart the container
    code, stdout, stderr = run_ssh_command(
        config["host"], config["port"], config["user"],
        f"docker restart {container_name}", log_file
    )

    if code != 0:
        log_action(f"ERROR: Docker restart failed for '{container_name}' on {server}: {stderr}", log_file)
        return False

    log_action(f"SUCCESS: Docker container '{container_name}' restarted on {server}", log_file)
    return True


def analyze_logs(
    server: str,
    config: dict,
    services: list[str],
    log_file: Optional[str] = None
) -> list[dict]:
    """Analyze logs after restart for errors."""
    errors = []

    for service in services:
        log_action(f"Analyzing {service} logs on {server}...", log_file)

        if service == "nginx":
            # Check nginx error log
            cmd = "sudo tail -n 50 /var/log/nginx/error.log | grep -i error || true"
            code, stdout, stderr = run_ssh_command(
                config["host"], config["port"], config["user"], cmd, log_file
            )
            if stdout.strip():
                errors.append({
                    "server": server,
                    "service": service,
                    "type": "error",
                    "message": stdout.strip()[:500]
                })

        elif service == "pm2":
            # Check PM2 logs for errors
            cmd = "pm2 logs --nostream --err --lines 20 --no-auto-restart 2>/dev/null || true"
            code, stdout, stderr = run_ssh_command(
                config["host"], config["port"], config["user"], cmd, log_file
            )
            if stdout.strip():
                errors.append({
                    "server": server,
                    "service": service,
                    "type": "error",
                    "message": stdout.strip()[:500]
                })

        elif service == "docker":
            # Check Docker daemon logs
            cmd = "sudo journalctl -u docker --no-pager -n 20 | grep -i error || true"
            code, stdout, stderr = run_ssh_command(
                config["host"], config["port"], config["user"], cmd, log_file
            )
            if stdout.strip():
                errors.append({
                    "server": server,
                    "service": service,
                    "type": "error",
                    "message": stdout.strip()[:500]
                })

    return errors


def verify_service_health(
    server: str,
    config: dict,
    service: str,
    log_file: Optional[str] = None
) -> bool:
    """Verify a service is running after restart."""
    log_action(f"Verifying {service} health on {server}...", log_file)

    if service == "nginx":
        cmd = "sudo systemctl is-active nginx"
    elif service == "pm2":
        cmd = "pm2 jlist | grep -q . && echo 'running' || echo 'stopped'"
    elif service == "docker":
        cmd = "sudo systemctl is-active docker"
    elif service == "traefik":
        cmd = "docker ps --filter name=traefik --format '{{.Status}}' | grep -q Up && echo 'running' || echo 'stopped'"
    else:
        return True  # Unknown service, skip

    code, stdout, stderr = run_ssh_command(
        config["host"], config["port"], config["user"], cmd, log_file
    )

    is_healthy = code == 0 and "running" in stdout.lower()

    if is_healthy:
        log_action(f"SUCCESS: {service} is healthy on {server}", log_file)
    else:
        log_action(f"WARNING: {service} may not be healthy on {server}", log_file)

    return is_healthy


def restart_services(
    servers: list[str],
    services: list[str],
    project_name: str = "portfolio",
    wait_seconds: int = 30,
    check_only: bool = False,
    log_file: Optional[str] = None
) -> dict:
    """
    Main function to restart services across servers.

    Returns:
        dict with 'success', 'errors', and 'warnings' keys
    """
    results = {
        "success": True,
        "errors": [],
        "warnings": [],
        "restarts": []
    }

    # Validate servers
    for server in servers:
        if server not in SERVERS:
            results["errors"].append(f"Unknown server: {server}")
            results["success"] = False
            return results

    # Validate services
    valid_services = ["nginx", "pm2", "docker", "traefik"]
    for service in services:
        if service not in valid_services:
            results["errors"].append(f"Unknown service: {service}")
            results["success"] = False
            return results

    # Check approval requirements
    for server in servers:
        for service in services:
            if check_approval_required(server, service):
                results["warnings"].append(
                    f"⚠️ {server}/{service} requires human approval - skipping auto-restart"
                )
                # Remove from services to restart
                if service in services:
                    services.remove(service)

    if check_only:
        log_action("Check-only mode: skipping actual restarts", log_file)
        return results

    # Perform restarts
    for server in servers:
        config = SERVERS[server]
        log_action(f"\n{'='*50}", log_file)
        log_action(f"Processing server: {server} ({config['purpose']})", log_file)

        for service in services:
            # Skip services not available on this server
            if service not in SERVER_SERVICES.get(server, []):
                results["warnings"].append(f"{server}: {service} not available")
                continue

            log_action(f"\n--- Restarting {service} on {server} ---", log_file)

            success = False
            if service == "nginx":
                success = restart_nginx(server, config, log_file)
            elif service == "pm2":
                success = restart_pm2(server, config, project_name, log_file)
            elif service == "docker":
                # Docker daemon restart - skip individual containers
                success = True  # Just verify docker is running
            elif service == "traefik":
                success = restart_docker_container(server, config, "traefik", log_file)

            if success:
                results["restarts"].append(f"{server}/{service}")
            else:
                results["errors"].append(f"Failed to restart {service} on {server}")
                results["success"] = False

    # Wait after restarts
    if results["restarts"]:
        log_action(f"\nWaiting {wait_seconds} seconds for services to stabilize...", log_file)
        time.sleep(wait_seconds)

    # Analyze logs and verify health
    for server in servers:
        config = SERVERS[server]

        # Analyze logs
        errors = analyze_logs(server, config, services, log_file)
        if errors:
            results["errors"].extend([e["message"] for e in errors])
            results["success"] = False

        # Verify health
        for service in services:
            if not verify_service_health(server, config, service, log_file):
                results["warnings"].append(f"{server}/{service} health check failed")

    return results


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Restart services across servers with validation and logging"
    )
    parser.add_argument(
        "--servers", "-s",
        help="Comma-separated list of servers (e.g., s60,s62)"
    )
    parser.add_argument(
        "--services",
        help="Comma-separated list of services (e.g., nginx,pm2)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Restart all services on s60 and s62 (excludes s61)"
    )
    parser.add_argument(
        "--project",
        default="portfolio",
        help="PM2 project name (default: portfolio)"
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=30,
        help="Seconds to wait after restart (default: 30)"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check what would be restarted, don't execute"
    )
    parser.add_argument(
        "--log-file",
        help="Path to log file"
    )

    args = parser.parse_args()

    # Determine servers
    if args.all:
        servers = ["s60", "s62"]  # Exclude s61 by default
    elif args.servers:
        servers = [s.strip() for s in args.servers.split(",")]
    else:
        print("Error: Must specify --servers or --all")
        parser.print_help()
        sys.exit(1)

    # Determine services
    if args.services:
        services = [s.strip() for s in args.services.split(",")]
    else:
        services = ["nginx", "pm2"]  # Default services

    # Run restart
    log_action(f"\n{'#'*60}", args.log_file)
    log_action(f"Service Restart - Servers: {servers}, Services: {services}", args.log_file)

    results = restart_services(
        servers=servers,
        services=services,
        project_name=args.project,
        wait_seconds=args.wait,
        check_only=args.check_only,
        log_file=args.log_file
    )

    # Print summary
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    print(f"Restarts: {results['restarts']}")

    if results['warnings']:
        print("\nWARNINGS:")
        for w in results['warnings']:
            print(f"  ⚠️  {w}")

    if results['errors']:
        print("\nERRORS:")
        for e in results['errors']:
            print(f"  ❌  {e}")

    if results['success']:
        print("\n✅ Service restart completed successfully")
        sys.exit(0)
    else:
        print("\n❌ Service restart completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
