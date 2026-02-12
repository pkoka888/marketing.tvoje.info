# Server Infrastructure Documentation

## Overview

This document provides comprehensive documentation of the server infrastructure for the marketing.tvoje.info project.

## Server Inventory

### Server60 (Infrastructure/VPS)
| Property | Value |
|----------|-------|
| Hostname | server60 |
| IP Address | 192.168.1.60 |
| SSH Port (Tailscale) | 20 |
| SSH Port (Internal) | 2260 |
| Purpose | Infrastructure/VPS |
| Status | Operational |
| Primary Services | PM2, Nginx, Docker |

### Server61 (Gateway/Traefik)
| Property | Value |
|----------|-------|
| Hostname | server61 |
| IP Address | 192.168.1.61 |
| SSH Port (Tailscale) | 20 |
| SSH Port (Internal) | 2261 |
| Purpose | Gateway/Traefik |
| Status | Operational |
| Primary Services | Traefik, Nginx, Docker |

### Server62 (Production/Web)
| Property | Value |
|----------|-------|
| Hostname | server62 |
| IP Address | 192.168.1.62 |
| SSH Port (Tailscale) | 20 |
| SSH Port (Internal) | 2262 |
| Purpose | Production/Web |
| Status | Operational |
| Primary Services | PM2, Nginx, Docker, Portfolio |

## Network Architecture

### Access Methods

| Method | Status | Notes |
|--------|--------|-------|
| Tailscale VPN (100.91.164.109/32) | ✅ Primary | Reliable, always available |
| Internal Network (192.168.1.0/24) | ✅ Backup | Fallback access method |
| Direct Public IP | ❌ Blocked | ISP/Router issues |

### Port Forwarding Status

| Port | Target | Status |
|------|--------|--------|
| 2260 | server60 | ✅ Working |
| 2261 | server61 | ✅ Working |
| 2262 | server62 | ❌ Not forwarded externally |

## Server Access Credentials

### SSH Configuration
- **User**: admin (or project-specific user)
- **Auth Method**: SSH key-based authentication
- **Primary Access**: Tailscale VPN via port 20
- **Fallback Access**: Internal network via ports 2260/2261/2262

## Services by Server

### Server60
- PM2 (process manager)
- Nginx (web server)
- Docker (container runtime)
- Node.js 20+ (runtime environment)

### Server61
- Traefik (reverse proxy/gateway)
- Nginx (web server)
- Docker (container runtime)

### Server62
- PM2 (process manager - portfolio application)
- Nginx (web server)
- Docker (container runtime)
- Node.js 20+ (runtime environment)

## Deployment Configuration

### PM2 Ecosystem Configuration
Located at: `ecosystem.config.js`
- Application: portfolio
- Working Directory: /var/www/portfolio
- Environment: production
- Node.js: 20+

### Application Stack
- **Framework**: Astro 5.0 (static site generator)
- **Runtime**: Node.js 20+
- **Process Manager**: PM2
- **Web Server**: Nginx (reverse proxy)
- **SSL**: Let's Encrypt certificates
- **Hosting**: Custom VPS (Debian 13)

## Security Configuration

### Firewall Status
- **UFW**: Active on all servers
- **iptables**: Configured for additional security
- **Fail2ban**: NOT INSTALLED (critical vulnerability)

### SSH Hardening
- Key-based authentication enabled
- Root login disabled
- Modern ciphers configured

## Monitoring & Logging

### Log Locations
- `/var/log/nginx/access.log` - Web access logs
- `/var/log/nginx/error.log` - Web error logs
- `/var/www/portfolio/.pm2/logs/` - Application logs
- `/var/log/auth.log` - SSH authentication logs

### Monitoring Tools
- PM2 process monitoring
- System resource monitoring
- Nginx status monitoring

## Related Documentation

- `SERVER62_SECURITY_AUDIT.md` - Security assessment findings
- `SERVER62_DEPLOYMENT_GUIDE.md` - Deployment procedures
- `NAT_ANALYSIS.md` - Network connectivity analysis
- `SERVER_INFRASTRUCTURE_KNOWLEDGE_BASE.md` - Comprehensive knowledge base

## Last Updated
Date: 2026-02-12
Version: 1.0
