#!/bin/bash
# safe-ssh.sh - Read-only SSH wrapper for server monitoring

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVIDENCE_DIR="${SCRIPT_DIR}/../../evidence"
LOG_FILE="${EVIDENCE_DIR}/ssh-audit.log"

# Server definitions
declare -A SERVERS=(
    ["server60"]="root@192.168.1.60 -p 2260"
    ["server61"]="root@192.168.1.61 -p 2261"
    ["server62"]="root@192.168.1.62 -p 2262"
)

# Forbidden patterns
FORBIDDEN_PATTERNS=(
    "rm\b"
    "del\b"
    "erase\b"
    "mkfs"
    "dd\b"
    "install\b"
    "update\b"
    "upgrade\b"
    "remove\b"
    "restart\b"
    "stop\b"
    "start\b"
    "reboot\b"
    "shutdown\b"
    "chmod\b"
    "chown\b"
    "crontab -e"
    "useradd"
    "usermod"
    "userdel"
    "groupadd"
    "groupmod"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log function
log_action() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] $1" >> "${LOG_FILE}"
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Warning function
warn_action() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] WARNING: $1" >> "${LOG_FILE}"
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Error function
error_action() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] ERROR: $1" >> "${LOG_FILE}"
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validate command for forbidden patterns
validate_command() {
    local cmd="$1"
    
    for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
        if echo "$cmd" | grep -qiE "$pattern"; then
            error_action "Forbidden pattern detected: $pattern in command: $cmd"
            return 1
        fi
    done
    
    # Check for write operations
    if echo "$cmd" | grep -qiE "> /etc/|> /var/|> /root/"; then
        error_action "Write operation detected: $cmd"
        return 1
    fi
    
    log_action "Command validated: $cmd"
    return 0
}

# Execute safe SSH command
execute_safe_ssh() {
    local server="$1"
    local command="$2"
    
    # Validate server exists
    if [[ -z "${SERVERS[$server]:-}" ]]; then
        error_action "Unknown server: $server"
        return 1
    fi
    
    # Validate command
    if ! validate_command "$command"; then
        error_action "Command validation failed for server: $server"
        return 1
    fi
    
    log_action "Executing on $server: $command"
    
    # Execute SSH command
    local ssh_opts="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o BatchMode=yes"
    local server_config="${SERVERS[$server]}"
    
    if ssh $ssh_opts $server_config "$command" 2>&1; then
        log_action "Successfully executed on $server"
        return 0
    else
        warn_action "Command execution had issues on $server"
        return 1
    fi
}

# Main function
main() {
    local server="$1"
    local command="${*:2}"
    
    # Create evidence directory if needed
    mkdir -p "$EVIDENCE_DIR"
    
    # Initialize log file
    touch "$LOG_FILE"
    
    if [[ -z "$server" || -z "$command" ]]; then
        echo "Usage: $0 <server> <command>"
        echo ""
        echo "Available servers:"
        for s in "${!SERVERS[@]}"; do
            echo "  $s (${SERVERS[$s]})"
        done
        return 1
    fi
    
    execute_safe_ssh "$server" "$command"
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
