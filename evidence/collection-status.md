# Server Evidence Collection Status

**Collection Date**: 2026-02-12 00:35 UTC
**Collection Attempted By**: Kilo Code (VS Code Extension)

## Auto-Detection Features (NEW)

The evidence collection system now includes automatic network detection:

### Network Detection

The scripts automatically detect your local IP and select the best connection method:

| Local IP Range | Network Type | SSH Port Used |
|----------------|--------------|---------------|
| 100.64.0.0/10  | Tailscale VPN | 20 |
| 192.168.1.0/24 | Internal Network | 2260/2261/2262 |
| Other          | External (fallback) | May not work |

### New Commands

```bash
# Detect network and show connection info
bash .kilocode/scripts/server-monitor/collect-evidence.sh detect

# Force network type
bash .kilocode/scripts/server-monitor/collect-evidence.sh all --network tailscale
bash .kilocode/scripts/server-monitor/collect-evidence.sh all --network internal

# Network debugging with BMAD integration
bash .kilocode/scripts/server-monitor/debug-network.sh
```

## Network Debugging Script

A new `debug-network.sh` script provides:
- Local IP detection
- Tailscale status check
- Internal network connectivity test
- SSH port verification
- BMAD MCP server integration (JSON output)
- Recommendations based on detected network

### Run Debug Script

```bash
# Basic debug output
bash .kilocode/scripts/server-monitor/debug-network.sh

# Save to custom location
bash .kilocode/scripts/server-monitor/debug-network.sh /tmp/my-debug.json
```

## Connection Configuration

### Server Access Matrix

| Server | Internal IP | Tailscale IP | Internal Port | Tailscale Port |
|--------|-------------|--------------|---------------|----------------|
| server60 | 192.168.1.60 | (configure) | 2260 | 20 |
| server61 | 192.168.1.61 | (configure) | 2261 | 20 |
| server62 | 192.168.1.62 | (configure) | 2262 | 20 |

### SSH User
All servers use `admin` user with SSH key authentication.

## Scripts Available

- `.kilocode/scripts/server-monitor/collect-evidence.sh` - Main collection script with auto-detection
- `.kilocode/scripts/server-monitor/debug-network.sh` - Network debugging script
- `.kilocode/scripts/server-monitor/safe-ssh.sh` - Safe SSH wrapper
- `.kilocode/scripts/server-monitor/safe-scp.sh` - Safe SCP wrapper

## Usage Examples

### Auto-detect network and collect all
```bash
bash .kilocode/scripts/server-monitor/collect-evidence.sh all
```

### Collect from specific server
```bash
bash .kilocode/scripts/server-monitor/collect-evidence.sh server60
```

### Debug network issues
```bash
bash .kilocode/scripts/server-monitor/debug-network.sh
```

### Force Tailscale mode
```bash
bash .kilocode/scripts/server-monitor/collect-evidence.sh all --network tailscale
```

## Expected Evidence Structure

When successfully executed, evidence will be saved to:

```
evidence/
├── server60/
│   ├── {timestamp}/
│   │   ├── system-info.txt
│   │   ├── packages.txt
│   │   ├── services.txt
│   │   ├── network.txt
│   │   ├── configs/
│   │   │   ├── nginx.conf
│   │   │   ├── sshd_config
│   │   │   └── ufw.status
│   │   ├── logs/
│   │   │   ├── access.log
│   │   │   ├── error.log
│   │   │   └── auth.log
│   │   └── summary.txt
│   └── error.txt (if server unreachable)
├── server61/
│   └── {timestamp}/
│       └── ...
└── server62/
    └── {timestamp}/
        └── ...
```

## Collection Commands Reference

### System Information
```bash
hostnamectl
uname -a
cat /etc/os-release
uptime
free -h
df -h
cat /proc/cpuinfo
```

### Package Inventory
```bash
dpkg -l
npm list -g --depth=0
pm2 jlist
```

### Service Status
```bash
systemctl list-units --type=service --state=running
systemctl list-units --type=service --all
ps aux
```

### Network Configuration
```bash
ip addr
ss -tulpn
ufw status
cat /etc/resolv.conf
```

### Configuration Files
```bash
cat /etc/nginx/nginx.conf
cat /etc/ssh/sshd_config
ufw status numbered
cat ecosystem.config.js
```

### Log Files
```bash
tail -n 50 /var/log/nginx/access.log
tail -n 50 /var/log/nginx/error.log
tail -n 100 /var/log/auth.log
```

## Next Steps

1. **Establish Network Access**: Connect to Tailscale VPN or use a machine on the internal network
2. **Run Debug Script**: `bash .kilocode/scripts/server-monitor/debug-network.sh`
3. **Execute Collection**: `bash .kilocode/scripts/server-monitor/collect-evidence.sh all`
4. **Generate Report**: Run the comparison script to generate `evidence/comparison/report.md`
5. **Review Findings**: Analyze the comparison report for configuration drift and security issues

## BMAD MCP Server Integration

The debug script generates JSON output compatible with BMAD MCP server:

```json
{
  "timestamp": "2026-02-12T00:35:00+00:00",
  "local_ip": "100.91.164.109",
  "network_type": "tailscale",
  "tailscale": {
    "installed": true,
    "running": true,
    "ip": "100.91.164.109"
  },
  "servers": {
    "server60": {
      "internal_ip": "192.168.1.60",
      "internal_port": 2260,
      "tailscale_port": 20,
      "internal_reachable": true,
      "internal_port_open": true,
      "tailscale_port_open": true
    }
  },
  "recommended_connection": {
    "method": "tailscale",
    "ssh_port": 20
  }
}
```

## Related Documentation

- Memory Bank: `.kilocode/rules/memory-bank/servers.md`
- Collection Script: `.kilocode/scripts/server-monitor/collect-evidence.sh`
- Debug Script: `.kilocode/scripts/server-monitor/debug-network.sh`
- Safe SSH Wrapper: `.kilocode/scripts/server-monitor/safe-ssh.sh`
