#!/bin/bash
# collect-evidence.sh - Comprehensive evidence collection script with Auto-Detection
# Automatically detects local IP and chooses best connection method (Tailscale vs Internal)

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVIDENCE_BASE="${SCRIPT_DIR}/../../evidence"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="${EVIDENCE_BASE}/collection.log"

# Server definitions - Internal IPs
declare -A INTERNAL_IPS=(
    ["server60"]="192.168.1.60"
    ["server61"]="192.168.1.61"
    ["server62"]="192.168.1.62"
)

# Server definitions - Tailscale IPs (configure these when discovered)
declare -A TAILSCALE_IPS=(
    ["server60"]=""
    ["server61"]=""
    ["server62"]=""
)

# Server SSH user
declare -A SSH_USERS=(
    ["server60"]="admin"
    ["server61"]="admin"
    ["server62"]="admin"
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

# Detect local network type
detect_network() {
    local local_ip
    local_ip=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K[0-9.]+' | head -1) || local_ip="unknown"
    
    log "Detected local IP: ${local_ip}"
    
    if [[ "$local_ip" == 100.64.* ]] || [[ "$local_ip" == 100.65.* ]] || [[ "$local_ip" == 100.66.* ]] || \
       [[ "$local_ip" == 100.67.* ]] || [[ "$local_ip" == 100.68.* ]] || [[ "$local_ip" == 100.69.* ]] || \
       [[ "$local_ip" == 100.70.* ]] || [[ "$local_ip" == 100.71.* ]] || [[ "$local_ip" == 100.72.* ]] || \
       [[ "$local_ip" == 100.73.* ]] || [[ "$local_ip" == 100.74.* ]] || [[ "$local_ip" == 100.75.* ]] || \
       [[ "$local_ip" == 100.76.* ]] || [[ "$local_ip" == 100.77.* ]] || [[ "$local_ip" == 100.78.* ]] || \
       [[ "$local_ip" == 100.79.* ]] || [[ "$local_ip" == 100.80.* ]] || [[ "$local_ip" == 100.81.* ]] || \
       [[ "$local_ip" == 100.82.* ]] || [[ "$local_ip" == 100.83.* ]] || [[ "$local_ip" == 100.84.* ]] || \
       [[ "$local_ip" == 100.85.* ]] || [[ "$local_ip" == 100.86.* ]] || [[ "$local_ip" == 100.87.* ]] || \
       [[ "$local_ip" == 100.88.* ]] || [[ "$local_ip" == 100.89.* ]] || [[ "$local_ip" == 100.90.* ]] || \
       [[ "$local_ip" == 100.91.* ]] || [[ "$local_ip" == 100.92.* ]] || [[ "$local_ip" == 100.93.* ]] || \
       [[ "$local_ip" == 100.94.* ]] || [[ "$local_ip" == 100.95.* ]]; then
        echo "tailscale"
    elif [[ "$local_ip" == 192.168.1.* ]]; then
        echo "internal"
    else
        echo "external"
    fi
}

# Get SSH host for a server based on network
get_ssh_host() {
    local server=$1
    local network=$2
    
    if [[ "$network" == "tailscale" ]] && [[ -n "${TAILSCALE_IPS[$server]:-}" ]]; then
        echo "${TAILSCALE_IPS[$server]}"
    else
        echo "${INTERNAL_IPS[$server]}"
    fi
}

# Get SSH port based on network and server
get_ssh_port() {
    local server=$1
    local network=$2
    
    if [[ "$network" == "tailscale" ]]; then
        # Tailscale typically uses standard SSH port 20
        echo "20"
    else
        # Internal network uses specific ports
        case $server in
            server60) echo "2260" ;;
            server61) echo "2261" ;;
            server62) echo "2262" ;;
            *) echo "22" ;;
        esac
    fi
}

# Get SSH user
get_ssh_user() {
    local server=$1
    echo "${SSH_USERS[$server]:-admin}"
}

# SSH execution wrapper with auto-detection
ssh_exec() {
    local server=$1
    local cmd="$2"
    local network="${3:-$(detect_network)}"
    local host
    local port
    local user
    
    host=$(get_ssh_host "$server" "$network")
    port=$(get_ssh_port "$server" "$network")
    user=$(get_ssh_user "$server")
    
    ssh $SSH_OPTS -p $port ${user}@${host} "$cmd" 2>&1 || true
}

# Check if server is reachable
check_server() {
    local server=$1
    local network="${2:-$(detect_network)}"
    local host
    local port
    
    host=$(get_ssh_host "$server" "$network")
    port=$(get_ssh_port "$server" "$network")
    
    if nc -z -w 2 "$host" "$port" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Collect system information
collect_system_info() {
    local server="$1"
    local output_dir="$2"
    local network="${3:-$(detect_network)}"
    
    log "Collecting system info from $server (network: $network)..."
    
    {
        echo "=== SYSTEM INFORMATION ==="
        echo "Timestamp: ${TIMESTAMP}"
        echo "Server: $server"
        echo "Network: $network"
        echo ""
        echo "--- Hostname and OS ---"
        ssh_exec "$server" "hostnamectl" "$network"
        echo ""
        echo "--- Kernel Version ---"
        ssh_exec "$server" "uname -a" "$network"
        echo ""
        echo "--- OS Release ---"
        ssh_exec "$server" "cat /etc/os-release" "$network"
        echo ""
        echo "--- Uptime ---"
        ssh_exec "$server" "uptime" "$network"
        echo ""
        echo "--- Memory Info ---"
        ssh_exec "$server" "free -h" "$network"
        echo ""
        echo "--- Disk Usage ---"
        ssh_exec "$server" "df -h" "$network"
        echo ""
        echo "--- CPU Info ---"
        ssh_exec "$server" "cat /proc/cpuinfo | head -20" "$network"
    } > "${output_dir}/system-info.txt"
    
    log "System info collected"
}

# Collect package inventory
collect_packages() {
    local server="$1"
    local output_dir="$2"
    local network="${3:-$(detect_network)}"
    
    log "Collecting package inventory from $server..."
    
    {
        echo "=== PACKAGE INVENTORY ==="
        echo "Timestamp: ${TIMESTAMP}"
        echo "Server: $server"
        echo "Network: $network"
        echo ""
        echo "--- APT Packages ---"
        ssh_exec "$server" "dpkg -l" "$network"
        echo ""
        echo "--- npm Global Packages ---"
        ssh_exec "$server" "npm list -g --depth=0 2>/dev/null || echo 'npm not available'" "$network"
        echo ""
        echo "--- PM2 Processes ---"
        ssh_exec "$server" "pm2 jlist 2>/dev/null || echo 'PM2 not available'" "$network"
    } > "${output_dir}/packages.txt"
    
    log "Package inventory collected"
}

# Collect service status
collect_services() {
    local server="$1"
    local output_dir="$2"
    local network="${3:-$(detect_network)}"
    
    log "Collecting service status from $server..."
    
    {
        echo "=== SERVICE STATUS ==="
        echo "Timestamp: ${TIMESTAMP}"
        echo "Server: $server"
        echo "Network: $network"
        echo ""
        echo "--- Running Services ---"
        ssh_exec "$server" "systemctl list-units --type=service --state=running" "$network"
        echo ""
        echo "--- All Services ---"
        ssh_exec "$server" "systemctl list-units --type=service --all 2>/dev/null | head -100" "$network"
        echo ""
        echo "--- Process List ---"
        ssh_exec "$server" "ps aux" "$network"
    } > "${output_dir}/services.txt"
    
    log "Service status collected"
}

# Collect network configuration
collect_network() {
    local server="$1"
    local output_dir="$2"
    local network="${3:-$(detect_network)}"
    
    log "Collecting network configuration from $server..."
    
    {
        echo "=== NETWORK CONFIGURATION ==="
        echo "Timestamp: ${TIMESTAMP}"
        echo "Server: $server"
        echo "Network: $network"
        echo ""
        echo "--- Network Interfaces ---"
        ssh_exec "$server" "ip addr" "$network"
        echo ""
        echo "--- Listening Ports ---"
        ssh_exec "$server" "ss -tulpn" "$network"
        echo ""
        echo "--- Firewall Status ---"
        ssh_exec "$server" "ufw status" "$network"
        echo ""
        echo "--- DNS Configuration ---"
        ssh_exec "$server" "cat /etc/resolv.conf" "$network"
    } > "${output_dir}/network.txt"
    
    log "Network configuration collected"
}

# Collect configuration files
collect_configs() {
    local server="$1"
    local output_dir="$2"
    local configs_dir="${output_dir}/configs"
    local network="${3:-$(detect_network)}"
    
    mkdir -p "$configs_dir"
    
    log "Collecting configuration files from $server..."
    
    # Collect configs
    ssh_exec "$server" "cat /etc/nginx/nginx.conf" "$network" > "${configs_dir}/nginx.conf" 2>/dev/null || true
    ssh_exec "$server" "cat /etc/ssh/sshd_config" "$network" > "${configs_dir}/sshd_config" 2>/dev/null || true
    ssh_exec "$server" "ufw status" "$network" > "${configs_dir}/ufw.status" 2>/dev/null || true
    ssh_exec "$server" "cat /var/www/portfolio/.env 2>/dev/null" "$network" > "${configs_dir}/app.env" 2>/dev/null || true
    ssh_exec "$server" "cat ecosystem.config.js 2>/dev/null" "$network" > "${configs_dir}/ecosystem.config.js" 2>/dev/null || true
    
    log "Configuration files collected"
}

# Collect log files
collect_logs() {
    local server="$1"
    local output_dir="$2"
    local logs_dir="${output_dir}/logs"
    local network="${3:-$(detect_network)}"
    
    mkdir -p "$logs_dir"
    
    log "Collecting log files from $server..."
    
    # Collect logs (last 50-100 lines)
    ssh_exec "$server" "tail -n 50 /var/log/nginx/access.log" "$network" > "${logs_dir}/access.log" 2>/dev/null || true
    ssh_exec "$server" "tail -n 50 /var/log/nginx/error.log" "$network" > "${logs_dir}/error.log" 2>/dev/null || true
    ssh_exec "$server" "tail -n 100 /var/log/auth.log" "$network" > "${logs_dir}/auth.log" 2>/dev/null || true
    
    log "Log files collected"
}

# Generate summary report
generate_summary() {
    local server="$1"
    local evidence_dir="$2"
    local network="${3:-$(detect_network)}"
    
    log "Generating summary for $server..."
    
    {
        echo "=== EVIDENCE COLLECTION SUMMARY ==="
        echo "Server: $server"
        echo "Timestamp: ${TIMESTAMP}"
        echo "Network: $network"
        echo ""
        echo "Files collected:"
        find "$evidence_dir" -type f -name "*.txt" | while read -r f; do
            echo "  - $f"
        done
        echo ""
        echo "Total files: $(find "$evidence_dir" -type f | wc -l)"
    } > "${evidence_dir}/summary.txt"
}

# Collect evidence from a single server
collect_server() {
    local server="$1"
    local network="${2:-$(detect_network)}"
    local host
    local port
    
    host=$(get_ssh_host "$server" "$network")
    port=$(get_ssh_port "$server" "$network")
    
    log "=== Starting evidence collection for $server ==="
    log "Network: $network"
    log "Connection: ${host}:${port}"
    
    # Create output directory
    local output_dir="${EVIDENCE_BASE}/${server}/${TIMESTAMP}"
    mkdir -p "$output_dir"
    mkdir -p "${output_dir}/configs"
    mkdir -p "${output_dir}/logs"
    
    # Check if server is reachable
    if ! check_server "$server" "$network"; then
        log "WARNING: Server $server not reachable at ${host}:${port}"
        echo "Server unreachable - skipping detailed collection" > "${output_dir}/error.txt"
        return 1
    fi
    
    # Collect all evidence
    collect_system_info "$server" "$output_dir" "$network"
    collect_packages "$server" "$output_dir" "$network"
    collect_services "$server" "$output_dir" "$network"
    collect_network "$server" "$output_dir" "$network"
    collect_configs "$server" "$output_dir" "$network"
    collect_logs "$server" "$output_dir" "$network"
    generate_summary "$server" "$output_dir" "$network"
    
    log "Evidence collection complete for $server"
    log "Output: ${output_dir}"
}

# Usage function
usage() {
    echo "Usage: $0 <server60|server61|server62|all|detect>"
    echo ""
    echo "Commands:"
    echo "  server60     Collect evidence from server60"
    echo "  server61     Collect evidence from server61"
    echo "  server62     Collect evidence from server62"
    echo "  all          Collect evidence from all servers"
    echo "  detect       Only detect network and show connection info"
    echo ""
    echo "Options:"
    echo "  --network <tailscale|internal|external>  Force network type"
    echo "  --help                                  Show this help"
    echo ""
    echo "The script automatically detects your local IP and selects"
    echo "the best connection method:"
    echo "  - Tailscale (100.64.0.0/10): Uses port 20"
    echo "  - Internal (192.168.1.0/24): Uses ports 2260/2261/2262"
    echo "  - External: Fallback, may not work"
}

# Main function
main() {
    local target_server="${1:-}"
    local forced_network=""
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --network)
                forced_network="$2"
                shift 2
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            *)
                target_server="$1"
                shift
                ;;
        esac
    done
    
    # Ensure evidence directory exists
    mkdir -p "$EVIDENCE_BASE"
    
    # Detect or use forced network
    local network
    if [[ -n "$forced_network" ]]; then
        network="$forced_network"
        log "Forcing network type: $network"
    else
        network=$(detect_network)
    fi
    
    log "=== Server Evidence Collection Started ==="
    log "Network detected: $network"
    log "Timestamp: $TIMESTAMP"
    
    # Handle different commands
    case "${target_server}" in
        detect)
            echo "=== Network Detection ==="
            echo "Local IP: $(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K[0-9.]+' | head:1)"
            echo "Network: $network"
            echo ""
            echo "Connection methods:"
            for server in server60 server61 server62; do
                local host port user
                host=$(get_ssh_host "$server" "$network")
                port=$(get_ssh_port "$server" "$network")
                user=$(get_ssh_user "$server")
                echo "  $server: ${user}@${host}:${port}"
            done
            exit 0
            ;;
        server60|server61|server62)
            collect_server "$target_server" "$network"
            ;;
        all)
            collect_server "server60" "$network"
            collect_server "server61" "$network"
            collect_server "server62" "$network"
            ;;
        "")
            usage
            exit 1
            ;;
        *)
            echo "Unknown server: ${target_server}"
            usage
            exit 1
            ;;
    esac
    
    log "=== Server Evidence Collection Complete ==="
}

# Run main function
main "$@"
