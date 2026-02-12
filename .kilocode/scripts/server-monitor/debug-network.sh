#!/bin/bash
# debug-network.sh - Network debugging script with BMAD MCP integration
# Detects local IP, checks connectivity, and helps diagnose network issues

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Server definitions
INTERNAL_SERVERS=("192.168.1.60" "192.168.1.61" "192.168.1.62")
INTERNAL_PORTS=(2260 2261 2262)
TAILSCALE_PREFIX="100.91.164.109"

# Output file for BMAD integration
DEBUG_OUTPUT="${1:-/tmp/network-debug.json}"

echo -e "${BLUE}=== Network Debug Report ===${NC}"
echo "Timestamp: $(date -Iseconds)"
echo ""

# Detect local IP
echo -e "${BLUE}=== Local IP Detection ===${NC}"
LOCAL_IP=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K[0-9.]+' | head -1) || LOCAL_IP="unknown"
echo -e "Local IP: ${GREEN}${LOCAL_IP}${NC}"

# Determine network type
if [[ "$LOCAL_IP" == 100.64.* ]] || [[ "$LOCAL_IP" == 100.65.* ]] || \
   [[ "$LOCAL_IP" == 100.91.* ]] || [[ "$LOCAL_IP" == 100.* ]]; then
    NETWORK_TYPE="tailscale"
    echo -e "Network Type: ${GREEN}Tailscale VPN${NC}"
elif [[ "$LOCAL_IP" == 192.168.1.* ]]; then
    NETWORK_TYPE="internal"
    echo -e "Network Type: ${GREEN}Internal Network (192.168.1.0/24)${NC}"
else
    NETWORK_TYPE="external"
    echo -e "Network Type: ${YELLOW}External/Unknown${NC}"
fi
echo ""

# Check Tailscale status
echo -e "${BLUE}=== Tailscale Status ===${NC}"
if command -v tailscale &> /dev/null; then
    if systemctl is-active --quiet tailscaled 2>/dev/null; then
        echo -e "Tailscale Service: ${GREEN}Running${NC}"
    else
        echo -e "Tailscale Service: ${RED}Not Running${NC}"
    fi
    
    TS_IP=$(tailscale ip 2>/dev/null || echo "")
    if [[ -n "$TS_IP" ]]; then
        echo -e "Tailscale IP: ${GREEN}${TS_IP}${NC}"
    else
        echo -e "Tailscale IP: ${YELLOW}Not assigned${NC}"
    fi
    
    TS_STATUS=$(tailscale status 2>/dev/null || echo "Unable to get status")
    echo "Tailscale Status:"
    echo "$TS_STATUS" | head -20
else
    echo -e "${YELLOW}Tailscale CLI not installed${NC}"
fi
echo ""

# Check internal network connectivity
echo -e "${BLUE}=== Internal Network ===${NC}"
for i in "${!INTERNAL_SERVERS[@]}"; do
    server="${INTERNAL_SERVERS[$i]}"
    if ping -c 1 -W 1 "$server" &> /dev/null; then
        echo -e "✓ ${server}: ${GREEN}reachable${NC}"
    else
        echo -e "✗ ${server}: ${RED}unreachable${NC}"
    fi
done
echo ""

# Check SSH ports
echo -e "${BLUE}=== SSH Port Check ===${NC}"
for i in "${!INTERNAL_SERVERS[@]}"; do
    server="${INTERNAL_SERVERS[$i]}"
    port="${INTERNAL_PORTS[$i]}"
    if nc -z -w 2 "$server" "$port" 2>/dev/null; then
        echo -e "✓ ${server}:${port} (internal): ${GREEN}open${NC}"
    else
        echo -e "✗ ${server}:${port} (internal): ${RED}closed${NC}"
    fi
done

# Check Tailscale SSH ports (port 20)
echo ""
echo -e "${BLUE}=== Tailscale SSH Ports ===${NC}"
for server in "${INTERNAL_SERVERS[@]}"; do
    if nc -z -w 2 "$server" 20 2>/dev/null; then
        echo -e "✓ ${server}:20 (tailscale): ${GREEN}open${NC}"
    else
        echo -e "✗ ${server}:20 (tailscale): ${RED}closed${NC}"
    fi
done
echo ""

# Generate JSON output for BMAD integration
echo -e "${BLUE}=== Generating BMAD Output ===${NC}"
cat > "$DEBUG_OUTPUT" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "local_ip": "$LOCAL_IP",
  "network_type": "$NETWORK_TYPE",
  "tailscale": {
    "installed": $(command -v tailscale &> /dev/null && echo "true" || echo "false"),
    "running": $(systemctl is-active --quiet tailscaled 2>/dev/null && echo "true" || echo "false"),
    "ip": "${TS_IP:-null}"
  },
  "servers": {
    "server60": {
      "internal_ip": "192.168.1.60",
      "internal_port": 2260,
      "tailscale_port": 20,
      "internal_reachable": $(ping -c 1 -W 1 192.168.1.60 &> /dev/null && echo "true" || echo "false"),
      "internal_port_open": $(nc -z -w 2 192.168.1.60 2260 2>/dev/null && echo "true" || echo "false"),
      "tailscale_port_open": $(nc -z -w 2 192.168.1.60 20 2>/dev/null && echo "true" || echo "false")
    },
    "server61": {
      "internal_ip": "192.168.1.61",
      "internal_port": 2261,
      "tailscale_port": 20,
      "internal_reachable": $(ping -c 1 -W 1 192.168.1.61 &> /dev/null && echo "true" || echo "false"),
      "internal_port_open": $(nc -z -w 2 192.168.1.61 2261 2>/dev/null && echo "true" || echo "false"),
      "tailscale_port_open": $(nc -z -w 2 192.168.1.61 20 2>/dev/null && echo "true" || echo "false")
    },
    "server62": {
      "internal_ip": "192.168.1.62",
      "internal_port": 2262,
      "tailscale_port": 20,
      "internal_reachable": $(ping -c 1 -W 1 192.168.1.62 &> /dev/null && echo "true" || echo "false"),
      "internal_port_open": $(nc -z -w 2 192.168.1.62 2262 2>/dev/null && echo "true" || echo "false"),
      "tailscale_port_open": $(nc -z -w 2 192.168.1.62 20 2>/dev/null && echo "true" || echo "false")
    }
  },
  "recommended_connection": {
    "method": "$NETWORK_TYPE",
    "ssh_port": $([[ "$NETWORK_TYPE" == "tailscale" ]] && echo "20" || echo "2260/2261/2262")
  }
}
EOF

echo "Debug output saved to: $DEBUG_OUTPUT"
echo ""

# Summary and recommendations
echo -e "${BLUE}=== Summary & Recommendations ===${NC}"
echo "Current Network: $NETWORK_TYPE"
echo ""
if [[ "$NETWORK_TYPE" == "tailscale" ]]; then
    echo -e "${GREEN}Recommended SSH Configuration:${NC}"
    echo "  Host: 192.168.1.60 (or 192.168.1.61, 192.168.1.62)"
    echo "  Port: 20"
    echo "  User: admin"
    echo ""
    echo "Run collect-evidence.sh with:"
    echo "  bash .kilocode/scripts/server-monitor/collect-evidence.sh all"
elif [[ "$NETWORK_TYPE" == "internal" ]]; then
    echo -e "${GREEN}Recommended SSH Configuration:${NC}"
    echo "  Host: 192.168.1.60"
    echo "  Port: 2260"
    echo "  User: admin"
    echo ""
    echo "Run collect-evidence.sh with:"
    echo "  bash .kilocode/scripts/server-monitor/collect-evidence.sh all"
else
    echo -e "${YELLOW}Warning: Not connected to Tailscale or Internal network${NC}"
    echo ""
    echo -e "${YELLOW}To connect:${NC}"
    echo "  1. Connect to Tailscale VPN, OR"
    echo "  2. Use a machine on the 192.168.1.0/24 network"
    echo ""
    echo "For Tailscale:"
    echo "  - Install Tailscale: https://tailscale.com/download"
    echo "  - Authenticate with your organization"
    echo "  - Verify connection: tailscale status"
fi
echo ""

echo -e "${BLUE}=== Debug Complete ===${NC}"
