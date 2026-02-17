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
