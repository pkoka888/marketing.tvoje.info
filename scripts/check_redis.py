#!/usr/bin/env python3
"""
Redis Health Check Script for MCP Server

This script checks if Redis is running and optionally starts it if not available.
Used as a pre-flight check before spawning the Redis MCP server.

Usage:
    python scripts/check_redis.py [--start-if-down] [--host localhost] [--port 6379]

Exit Codes:
    0 - Redis is running
    1 - Redis is not running (and could not be started if --start-if-down was given)
"""

import argparse
import socket
import subprocess
import sys
import time
from typing import Optional


def check_redis_connection(host: str = "localhost", port: int = 6379, timeout: float = 5.0) -> bool:
    """
    Check if Redis is accepting connections on the specified host and port.

    Args:
        host: Redis host address
        port: Redis port number
        timeout: Connection timeout in seconds

    Returns:
        True if Redis is accepting connections, False otherwise
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error as e:
        print(f"Socket error checking Redis: {e}", file=sys.stderr)
        return False


def ping_redis(host: str = "localhost", port: int = 6379) -> bool:
    """
    Send a PING command to Redis using redis-cli.

    Args:
        host: Redis host address
        port: Redis port number

    Returns:
        True if Redis responds with PONG, False otherwise
    """
    try:
        result = subprocess.run(
            ["redis-cli", "-h", host, "-p", str(port), "ping"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip() == "PONG"
    except FileNotFoundError:
        print("redis-cli not found in PATH", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("Redis ping timed out", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error pinging Redis: {e}", file=sys.stderr)
        return False


def start_redis_windows() -> bool:
    """
    Attempt to start Redis on Windows.

    Returns:
        True if Redis was started successfully, False otherwise
    """
    try:
        # Try to start Redis using redis-server
        # On Windows, Redis typically runs as a service or standalone process
        result = subprocess.run(
            ["redis-server"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # Give Redis time to start
        time.sleep(2)
        return True
    except FileNotFoundError:
        print("redis-server not found in PATH", file=sys.stderr)
        print("Please install Redis or ensure it's in your PATH", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        # This might be expected if redis-server starts as a daemon
        return True
    except Exception as e:
        print(f"Error starting Redis: {e}", file=sys.stderr)
        return False


def check_redis_service_windows() -> bool:
    """
    Check if Redis is running as a Windows service.

    Returns:
        True if Redis service is running, False otherwise
    """
    try:
        result = subprocess.run(
            ["sc", "query", "Redis"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return "RUNNING" in result.stdout
    except Exception as e:
        print(f"Error checking Redis service: {e}", file=sys.stderr)
        return False


def start_redis_service_windows() -> bool:
    """
    Attempt to start Redis as a Windows service.

    Returns:
        True if service was started successfully, False otherwise
    """
    try:
        result = subprocess.run(
            ["sc", "start", "Redis"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # Give service time to start
        time.sleep(2)
        return result.returncode == 0
    except Exception as e:
        print(f"Error starting Redis service: {e}", file=sys.stderr)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Redis availability for MCP server"
    )
    parser.add_argument(
        "--start-if-down",
        action="store_true",
        help="Attempt to start Redis if it's not running"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Redis host address (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6379,
        help="Redis port number (default: 6379)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Connection timeout in seconds (default: 5.0)"
    )

    args = parser.parse_args()

    print(f"Checking Redis at {args.host}:{args.port}...")

    # First check if we can connect to the port
    if check_redis_connection(args.host, args.port, args.timeout):
        print("✓ Redis port is open")

        # Verify with PING command
        if ping_redis(args.host, args.port):
            print("✓ Redis PING successful")
            return 0
        else:
            print("⚠ Redis port is open but PING failed (might require auth)")
            return 0  # Port is open, assume Redis is running

    print("✗ Redis is not responding")

    if args.start_if_down:
        print("Attempting to start Redis...")

        # Try Windows service first
        if sys.platform == "win32":
            if check_redis_service_windows():
                print("Redis service is already running")
            else:
                if start_redis_service_windows():
                    print("✓ Redis service started")
                    time.sleep(2)
                    if check_redis_connection(args.host, args.port, args.timeout):
                        return 0
                else:
                    # Try standalone redis-server
                    if start_redis_windows():
                        print("✓ Redis server started")
                        time.sleep(2)
                        if check_redis_connection(args.host, args.port, args.timeout):
                            return 0
        else:
            # Linux/macOS - try systemctl or redis-server
            try:
                subprocess.run(
                    ["systemctl", "start", "redis"],
                    check=True,
                    timeout=10
                )
                print("✓ Redis service started via systemctl")
                time.sleep(2)
                if check_redis_connection(args.host, args.port, args.timeout):
                    return 0
            except (subprocess.CalledProcessError, FileNotFoundError):
                if start_redis_windows():  # This function name is misleading but works for standalone
                    print("✓ Redis server started")
                    time.sleep(2)
                    if check_redis_connection(args.host, args.port, args.timeout):
                        return 0

    print("✗ Redis is not available")
    print("\nTo fix this issue:")
    print("  1. Install Redis: https://redis.io/download")
    print("  2. Start Redis: redis-server")
    print("  3. Or run this script with --start-if-down flag")
    return 1


if __name__ == "__main__":
    sys.exit(main())
