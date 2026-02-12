# Server Inventory

This document provides a comprehensive inventory of all servers in the infrastructure, their access details, and configuration specifications.

## Server Overview

| Server | Hostname | IP Address | Port | Purpose | Role |
|--------|----------|------------|------|---------|------|
| Server60 | infra60 | 192.168.1.60 | 2260 | Infrastructure/VPS | Primary Infrastructure |
| Server61 | gw61 | 192.168.1.61 | 2261 | Gateway/Traefik | Reverse Proxy Gateway |
| Server62 | prod62 | 192.168.1.62 | 2262 | Production/Web | Web Application Server |

## Access Information

### Primary Access Method: Tailscale VPN
- **Tailscale IP**: 100.91.164.109/32
- **SSH Port via Tailscale**: 20
- **Authentication**: SSH key-based (no password authentication)

### Fallback Access: Direct SSH
- **Server60**: 192.168.1.60:2260
- **Server61**: 192.168.1.61:2261
- **Server62**: 192.168.1.62:2262

### SSH Configuration
- **User**: root (default administrative access)
- **SSH Key**: Stored in SSH agent or `~/.ssh/id_rsa`
- **Connection Timeout**: 30 seconds
- **Retry Attempts**: 3

---

## Server Specifications

### Server60 - Infrastructure/VPS

#### Hardware Profile
| Component | Specification |
|-----------|---------------|
| CPU | [To be discovered] |
| Memory | [To be discovered] |
| Storage | [To be discovered] |
| Network | 1Gbps ethernet |

#### Operating System
- **Distribution**: [To be discovered]
- **Kernel**: [To be discovered]
- **Architecture**: x86_64 (expected)

#### Services Expected
- [ ] PM2 process manager
- [ ] Node.js runtime
- [ ] Nginx (possibly)
- [ ] Docker (possibly)

#### Key Configuration Paths
| Path | Purpose |
|------|---------|
| `/etc/nginx/` | Nginx configuration (if installed) |
| `/var/www/` | Web root directory |
| `/root/` | Home directory |
| `/var/log/` | Log directory |

---

### Server61 - Gateway/Traefik

#### Hardware Profile
| Component | Specification |
|-----------|---------------|
| CPU | [To be discovered] |
| Memory | [To be discovered] |
| Storage | [To be discovered] |
| Network | 1Gbps ethernet |

#### Operating System
- **Distribution**: [To be discovered]
- **Kernel**: [To be discovered]
- **Architecture**: x86_64 (expected)

#### Services Expected
- [ ] Traefik (reverse proxy)
- [ ] UFW (firewall)
- [ ] Tailscale (VPN)
- [ ] Nginx (possibly, for specific routes)

#### Key Configuration Paths
| Path | Purpose |
|------|---------|
| `/etc/traefik/` | Traefik configuration |
| `/etc/nginx/` | Nginx configuration |
| `/var/log/traefik/` | Traefik logs |
| `/etc/ufw/` | Firewall rules |

---

### Server62 - Production/Web

#### Hardware Profile
| Component | Specification |
|-----------|---------------|
| CPU | [To be discovered] |
| Memory | [To be discovered] |
| Storage | [To be discovered] |
| Network | 1Gbps ethernet |

#### Operating System
- **Distribution**: [To be discovered]
- **Kernel**: [To be discovered]
- **Architecture**: x86_64 (expected)

#### Services Expected
- [x] PM2 process manager (primary)
- [ ] Node.js runtime
- [x] Nginx (web server)
- [ ] Tailscale (VPN)

#### Application Details
| Component | Value |
|-----------|-------|
| Application | Marketing Portfolio |
| Node.js Version | [To be discovered] |
| PM2 App Name | [To be discovered] |
| Port | [To be discovered] |

#### Key Configuration Paths
| Path | Purpose |
|------|---------|
| `/var/www/portfolio/` | Application root |
| `/var/www/portfolio/.env` | Environment variables |
| `ecosystem.config.js` | PM2 configuration |
| `/etc/nginx/sites-available/` | Nginx site configs |
| `/var/log/nginx/` | Nginx logs |

---

## Documentation References

### Existing Documentation
| Document | Location | Purpose |
|----------|----------|---------|
| Server62 Security Audit | `SERVER62_SECURITY_AUDIT.md` | Security configuration audit |
| Server62 Deployment Guide | `SERVER62_DEPLOYMENT_GUIDE.md` | Deployment procedures |
| NAT Analysis | `NAT_ANALYSIS.md` | Network address translation |
| Security Audit Script | `security-audit-server62.sh` | Automated security audit |
| Ecosystem Config | `ecosystem.config.js` | PM2 configuration |
| Infrastructure Knowledge | `SERVER_INFRASTRUCTURE_KNOWLEDGE_BASE.md` | Infrastructure documentation |

---

## Baseline Configurations

### Expected Nginx Configuration
```
/etc/nginx/
├── nginx.conf              # Main nginx configuration
├── sites-available/
│   ├── default            # Default site
│   └── portfolio          # Portfolio site configuration
└── sites-enabled/
    ├── default -> ../sites-available/default
    └── portfolio -> ../sites-available/portfolio
```

### Expected PM2 Configuration (ecosystem.config.js)
```javascript
module.exports = {
  apps: [{
    name: 'portfolio',
    script: 'npm',
    args: 'start',
    cwd: '/var/www/portfolio',
    instances: 1,
    autorestart: true,
    watch: false,
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    }
  }]
};
```

### Expected Environment Variables
| Variable | Purpose | Example Value |
|----------|---------|---------------|
| `NODE_ENV` | Environment mode | production |
| `PORT` | Application port | 3000 |
| `PUBLIC_SITE_URL` | Site URL | marketing.tvoje.info |
| `VPS_IP` | Server IP | 192.168.1.62 |

---

## Comparison Points

### Package Versions to Track

| Package | Server60 | Server61 | Server62 | Baseline |
|---------|----------|----------|----------|----------|
| nginx | [ ] | [ ] | [ ] | [ ] |
| nodejs | [ ] | [ ] | [ ] | [ ] |
| npm | [ ] | [ ] | [ ] | [ ] |
| pm2 | [ ] | [ ] | [ ] | [ ] |
| openssh | [ ] | [ ] | [ ] | [ ] |
| ufw | [ ] | [ ] | [ ] | [ ] |

### Service States to Compare

| Service | Server60 | Server61 | Server62 | Status |
|---------|----------|----------|----------|--------|
| nginx | [ ] | [ ] | [ ] | running/not |
| pm2 | [ ] | [ ] | [ ] | running/not |
| traefik | [ ] | [ ] | [ ] | running/not |
| ufw | [ ] | [ ] | [ ] | active/not |
| tailscale | [ ] | [ ] | [ ] | running/not |

### Network Configurations to Compare

| Setting | Server60 | Server61 | Server62 |
|---------|----------|----------|----------|
| Listening ports | [ ] | [ ] | [ ] |
| Firewall rules | [ ] | [ ] | [ ] |
| DNS servers | [ ] | [ ] | [ ] |
| Default gateway | [ ] | [ ] | [ ] |

---

## Evidence Collection Checklist

### Pre-Collection
- [ ] Verify Tailscale VPN connection
- [ ] Verify SSH key availability
- [ ] Verify evidence directory exists
- [ ] Create timestamp directory

### Collection Steps
- [ ] **Server60 Evidence**
  - [ ] System information
  - [ ] Package inventory
  - [ ] Service status
  - [ ] Network configuration
  - [ ] Configuration files
  - [ ] Log files
- [ ] **Server61 Evidence**
  - [ ] System information
  - [ ] Package inventory
  - [ ] Service status
  - [ ] Network configuration
  - [ ] Configuration files
  - [ ] Log files
- [ ] **Server62 Evidence**
  - [ ] System information
  - [ ] Package inventory
  - [ ] Service status
  - [ ] Network configuration
  - [ ] Configuration files
  - [ ] Log files

### Post-Collection
- [ ] Generate summary report
- [ ] Create latest symlinks
- [ ] Verify all files collected
- [ ] Generate comparison report
- [ ] Document any anomalies

---

## Known Issues and Anomalies

| Server | Issue | Status | Notes |
|--------|-------|--------|-------|
| [To be discovered] | [ ] | [ ] | [ ] |

---

## Update Schedule

This inventory should be updated:
- After any server configuration change
- After any package installation/update
- Monthly as part of regular audits
- Immediately after any security incident

Last Updated: [To be filled after first collection]
Next Scheduled Update: [To be determined]
