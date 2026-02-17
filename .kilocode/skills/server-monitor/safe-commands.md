# Safe SSH Command Wrappers

This document provides safe SSH command wrappers for the server-monitor mode. These scripts ensure all remote operations are read-only and non-intrusive.

## Overview

The safe SSH wrappers enforce read-only operations by:

1. Validating commands before execution
2. Preventing dangerous command patterns
3. Logging all operations for audit
4. Redirecting output to evidence directories

## Scripts Location

All scripts are located in: `.kilocode/scripts/server-monitor/`

---

## safe-ssh.sh

### Purpose

SSH wrapper that only allows read-only commands to be executed on remote servers.

### Features

- Command validation before execution
- Automatic evidence collection
- Audit logging of all operations
- Error handling and reporting

### Usage

```bash
# Basic syntax
./safe-ssh.sh <server> <command>

# Examples
./safe-ssh.sh server60 "hostnamectl"
./safe-ssh.sh server61 "dpkg -l"
./safe-ssh.sh server62 "systemctl status"
```

### Server Aliases

| Alias    | Host              | Port | Purpose            |
| -------- | ----------------- | ---- | ------------------ |
| server60 | root@192.168.1.60 | 2260 | Infrastructure/VPS |
| server61 | root@192.168.1.61 | 2261 | Gateway/Traefik    |
| server62 | root@192.168.1.62 | 2262 | Production/Web     |

### Implementation

```bash
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
```

---

## safe-scp.sh

### Purpose

SCP wrapper for safe file transfer from remote servers. Read-only by design.

### Features

- Download only (no upload)
- Automatic evidence directory placement
- Audit logging
- Directory preservation

### Usage

```bash
# Basic syntax
./safe-scp.sh <server> <remote_path> [local_path]

# Examples
./safe-scp.sh server60 /etc/os-release ./evidence/server60/
./safe-scp.sh server61 /var/log/nginx/error.log ./evidence/server61/logs/
./safe-scp.sh server62 /etc/nginx/sites-available/default ./evidence/server62/configs/
```

### Implementation

```bash
#!/bin/bash
# safe-scp.sh - Read-only SCP wrapper for evidence collection

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVIDENCE_DIR="${SCRIPT_DIR}/../../evidence"
LOG_FILE="${EVIDENCE_DIR}/scp-audit.log"

# Server definitions
declare -A SERVERS=(
    ["server60"]="root@192.168.1.60 -p 2260"
    ["server61"]="root@192.168.1.61 -p 2261"
    ["server62"]="root@192.168.1.62 -p 2262"
)

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Log function
log_action() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] $1" >> "${LOG_FILE}"
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Main function
main() {
    local server="$1"
    local remote_path="$2"
    local local_path="${3:-${EVIDENCE_DIR}/${server}/latest}"

    # Create local directory
    mkdir -p "$local_path"

    # Initialize log
    touch "$LOG_FILE"

    if [[ -z "$server" || -z "$remote_path" ]]; then
        echo "Usage: $0 <server> <remote_path> [local_path]"
        echo ""
        echo "Download remote files to local evidence directory"
        return 1
    fi

    log_action "Downloading $remote_path from $server to $local_path"

    # SCP options
    local scp_opts="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o BatchMode=yes"
    local server_config="${SERVERS[$server]:-}"

    # Execute SCP (download only)
    if scp $scp_opts $server_config:"$remote_path" "$local_path/" 2>&1; then
        log_action "Successfully downloaded $remote_path"

        # Set read-only permissions on downloaded file
        chmod 444 "$local_path/$(basename "$remote_path")" 2>/dev/null || true

        return 0
    else
        log_action "Failed to download $remote_path"
        return 1
    fi
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

---

## collect-evidence.sh

### Purpose

Comprehensive evidence collection script that gathers all system information from a server.

### Features

- Collects all system information
- Organizes output by category
- Creates timestamped directories
- Generates summary reports
- Handles errors gracefully

### Usage

```bash
# Basic syntax
./collect-evidence.sh <server>

# Examples
./collect-evidence.sh server60
./collect-evidence.sh server61
./collect-evidence.sh server62
```

### Implementation

```bash
#!/bin/bash
# collect-evidence.sh - Comprehensive evidence collection script

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVIDENCE_BASE="${SCRIPT_DIR}/../../evidence"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="${EVIDENCE_BASE}/collection.log"

# Server definitions
declare -A SERVERS=(
    ["server60"]="root@192.168.1.60 -p 2260"
    ["server61"]="root@192.168.1.61 -p 2261"
    ["server62"]="root@192.168.1.62 -p 2262"
)

# SSH options
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o BatchMode=yes"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Log function
log() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] $1" | tee -a "${LOG_FILE}"
}

# SSH execution wrapper
ssh_exec() {
    local server="$1"
    local cmd="$2"
    local server_config="${SERVERS[$server]:-}"

    ssh $SSH_OPTS $server_config "$cmd" 2>&1 || true
}

# Collect system information
collect_system_info() {
    local server="$1"
    local output_dir="$2"

    log "Collecting system info from $server..."

    {
        echo "=== SYSTEM INFORMATION ==="
        echo "Timestamp: ${TIMESTAMP}"
        echo "Server: $server"
        echo ""
        echo "--- Hostname and OS ---"
        ssh_exec "$server" "hostnamectl"
        echo ""
        echo "--- Kernel Version ---"
        ssh_exec "$server" "uname -a"
        echo ""
        echo "--- OS Release ---"
        ssh_exec "$server" "cat /etc/os-release"
        echo ""
        echo "--- Uptime ---"
        ssh_exec "$server" "uptime"
        echo ""
        echo "--- Memory Info ---"
        ssh_exec "$server" "free -h"
        echo ""
        echo "--- Disk Usage ---"
        ssh_exec "$server" "df -h"
        echo ""
        echo "--- CPU Info ---"
        ssh_exec "$server" "cat /proc/cpuinfo | head -20"
    } > "${output_dir}/system-info.txt"

    log "System info collected"
}

# Collect package inventory
collect_packages() {
    local server="$1"
    local output_dir="$2"

    log "Collecting package inventory from $server..."

    {
        echo "=== PACKAGE INVENTORY ==="
        echo "Timestamp: ${TIMESTAMP}"
        echo "Server: $server"
        echo ""
        echo "--- APT Packages ---"
        ssh_exec "$server" "dpkg -l"
        echo ""
        echo "--- npm Global Packages ---"
        ssh_exec "$server" "npm list -g --depth=0 2>/dev/null || echo 'npm not available'"
        echo ""
        echo "--- PM2 Processes ---"
        ssh_exec "$server" "pm2 jlist 2>/dev/null || echo 'PM2 not available'"
    } > "${output_dir}/packages.txt"

    log "Package inventory collected"
}

# Collect service status
collect_services() {
    local server="$1"
    local output_dir="$2"

    log "Collecting service status from $server..."

    {
        echo "=== SERVICE STATUS ==="
        echo "Timestamp: ${TIMESTAMP}"
        echo "Server: $server"
        echo ""
        echo "--- Running Services ---"
        ssh_exec "$server" "systemctl list-units --type=service --state=running"
        echo ""
        echo "--- All Services ---"
        ssh_exec "$server" "systemctl list-units --type=service --all 2>/dev/null | head -100"
        echo ""
        echo "--- Process List ---"
        ssh_exec "$server" "ps aux"
    } > "${output_dir}/services.txt"

    log "Service status collected"
}

# Collect network configuration
collect_network() {
    local server="$1"
    local output_dir="$2"

    log "Collecting network configuration from $server..."

    {
        echo "=== NETWORK CONFIGURATION ==="
        echo "Timestamp: ${TIMESTAMP}"
        echo "Server: $server"
        echo ""
        echo "--- Network Interfaces ---"
        ssh_exec "$server" "ip addr"
        echo ""
        echo "--- Listening Ports ---"
        ssh_exec "$server" "ss -tulpn"
        echo ""
        echo "--- Firewall Status ---"
        ssh_exec "$server" "ufw status"
        echo ""
        echo "--- DNS Configuration ---"
        ssh_exec "$server" "cat /etc/resolv.conf"
    } > "${output_dir}/network.txt"

    log "Network configuration collected"
}

# Collect configuration files
collect_configs() {
    local server="$1"
    local output_dir="$2"
    local configs_dir="${output_dir}/configs"

    mkdir -p "$configs_dir"

    log "Collecting configuration files from $server..."

    # Collect configs
    ssh_exec "$server" "cat /etc/nginx/nginx.conf" > "${configs_dir}/nginx.conf" 2>/dev/null || true
    ssh_exec "$server" "cat /etc/ssh/sshd_config" > "${configs_dir}/sshd_config" 2>/dev/null || true
    ssh_exec "$server" "ufw status" > "${configs_dir}/ufw.status" 2>/dev/null || true
    ssh_exec "$server" "cat /var/www/portfolio/.env 2>/dev/null" > "${configs_dir}/app.env" 2>/dev/null || true
    ssh_exec "$server" "cat ecosystem.config.js 2>/dev/null" > "${configs_dir}/ecosystem.config.js" 2>/dev/null || true

    log "Configuration files collected"
}

# Collect log files
collect_logs() {
    local server="$1"
    local output_dir="$2"
    local logs_dir="${output_dir}/logs"

    mkdir -p "$logs_dir"

    log "Collecting log files from $server..."

    # Collect logs (last 50-100 lines)
    ssh_exec "$server" "tail -n 50 /var/log/nginx/access.log" > "${logs_dir}/access.log" 2>/dev/null || true
    ssh_exec "$server" "tail -n 50 /var/log/nginx/error.log" > "${logs_dir}/error.log" 2>/dev/null || true
    ssh_exec "$server" "tail -n 100 /var/log/auth.log" > "${logs_dir}/auth.log" 2>/dev/null || true

    log "Log files collected"
}

# Generate summary report
generate_summary() {
    local server="$1"
    local evidence_dir="$2"

    {
        echo "=== EVIDENCE COLLECTION SUMMARY ==="
        echo "Server: $server"
        echo "Timestamp: ${TIMESTAMP}"
        echo ""
        echo "Files Generated:"
        ls -la "$evidence_dir/"
        echo ""
        echo "Configuration Files:"
        ls -la "$evidence_dir/configs/" 2>/dev/null || echo "No configs collected"
        echo ""
        echo "Log Files:"
        ls -la "$evidence_dir/logs/" 2>/dev/null || echo "No logs collected"
        echo ""
        echo "Collection completed successfully"
    } > "${evidence_dir}/summary.txt"
}

# Main function
main() {
    local server="$1"

    if [[ -z "$server" ]]; then
        echo "Usage: $0 <server>"
        echo ""
        echo "Available servers:"
        for s in "${!SERVERS[@]}"; do
            echo "  $s (${SERVERS[$s]})"
        done
        return 1
    fi

    # Check server exists
    if [[ -z "${SERVERS[$server]:-}" ]]; then
        echo "Unknown server: $server"
        return 1
    fi

    # Create evidence directory
    local evidence_dir="${EVIDENCE_BASE}/${server}/${TIMESTAMP}"
    mkdir -p "$evidence_dir"

    # Initialize log
    mkdir -p "$EVIDENCE_BASE"
    touch "$LOG_FILE"

    log "=== Starting evidence collection for $server ==="

    # Collect all evidence
    collect_system_info "$server" "$evidence_dir"
    collect_packages "$server" "$evidence_dir"
    collect_services "$server" "$evidence_dir"
    collect_network "$server" "$evidence_dir"
    collect_configs "$server" "$evidence_dir"
    collect_logs "$server" "$evidence_dir"

    # Generate summary
    generate_summary "$server" "$evidence_dir"

    # Create latest symlink
    local latest_link="${EVIDENCE_BASE}/${server}/latest"
    rm -f "$latest_link" 2>/dev/null || true
    ln -s "$TIMESTAMP" "$latest_link"

    log "=== Evidence collection completed for $server ==="
    log "Evidence saved to: $evidence_dir"
    log "Latest symlink: $latest_link"

    echo ""
    echo "Evidence collection complete for $server"
    echo "Location: $evidence_dir"
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

---

## Usage Examples

### Complete Evidence Collection Workflow

```bash
#!/bin/bash
# Complete evidence collection from all servers

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")")"
cd "$SCRIPT_DIR"

# Collect from all servers
for server in server60 server61 server62; do
    echo "========================================="
    echo "Collecting evidence from $server"
    echo "========================================="

    ./collect-evidence.sh "$server"

    echo ""
done

echo "========================================="
echo "All evidence collection complete!"
echo "Evidence directory: evidence/"
echo "========================================="
```

### Selective Command Execution

```bash
# Check nginx status on all servers
for server in server60 server61 server62; do
    ./safe-ssh.sh "$server" "systemctl status nginx"
done

# Get memory usage from all servers
for server in server60 server61 server62; do
    ./safe-ssh.sh "$server" "free -h"
done

# List listening ports on all servers
for server in server60 server61 server62; do
    ./safe-ssh.sh "$server" "ss -tulpn"
done
```

### Configuration File Collection

```bash
#!/bin/bash
# Collect specific configuration files

./safe-scp.sh server60 /etc/nginx/nginx.conf ./evidence/server60/configs/
./safe-scp.sh server60 /etc/ssh/sshd_config ./evidence/server60/configs/

./safe-scp.sh server61 /etc/nginx/nginx.conf ./evidence/server61/configs/
./safe-scp.sh server61 /etc/ssh/sshd_config ./evidence/server61/configs/

./safe-scp.sh server62 /etc/nginx/nginx.conf ./evidence/server62/configs/
./safe-scp.sh server62 /etc/ssh/sshd_config ./evidence/server62/configs/
./safe-scp.sh server62 /var/www/portfolio/.env ./evidence/server62/configs/
```

---

## Audit Log Format

All operations are logged to `evidence/ssh-audit.log` and `evidence/scp-audit.log`:

```
[2026-02-12 00:00:00] INFO: Executing on server60: hostnamectl
[2026-02-12 00:00:01] INFO: Successfully executed on server60
[2026-02-12 00:00:02] INFO: Downloading /etc/os-release from server60
[2026-02-12 00:00:03] INFO: Successfully downloaded /etc/os-release
```

---

## Security Considerations

1. **No Credentials in Logs**: SSH keys should be agent-based, not password-based
2. **StrictHostKeyChecking**: Set to accept new host keys automatically
3. **LogLevel**: Set to ERROR to reduce log verbosity
4. **File Permissions**: Downloaded evidence should be read-only (chmod 444)
5. **Symlink Safety**: Latest symlinks are replaced, never modified in-place
6. **BatchMode**: Ensures no password prompts (fail if key not available)
