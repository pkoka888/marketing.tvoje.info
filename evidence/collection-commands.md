# Server Evidence Collection Commands

This document provides a comprehensive list of commands for collecting evidence from the server infrastructure.

## Server Inventory

| Server   | Hostname | IP Address   | SSH Port                        | Purpose            |
| -------- | -------- | ------------ | ------------------------------- | ------------------ |
| server60 | server60 | 192.168.1.60 | 2260 (internal), 20 (Tailscale) | Infrastructure/VPS |
| server61 | server61 | 192.168.1.61 | 2261 (internal), 20 (Tailscale) | Gateway/Traefik    |
| server62 | server62 | 192.168.1.62 | 2262 (internal), 20 (Tailscale) | Production/Web     |

## SSH Access

```bash
# Internal network access
ssh admin@192.168.1.60 -p 2260
ssh admin@192.168.1.61 -p 2261
ssh admin@192.168.1.62 -p 2262

# Tailscale VPN access
ssh admin@192.168.1.60 -p 20
ssh admin@192.168.1.61 -p 20
ssh admin@192.168.1.62 -p 20
```

## System Information Commands

### Basic System Info

```bash
# Hostname and OS details
hostnamectl

# Kernel and system info
uname -a
uname -r

# OS release information
cat /etc/os-release
cat /etc/lsb-release 2>/dev/null || echo "lsb-release not available"

# System uptime
uptime
cat /proc/uptime

# Current date/time
date
timedatectl
```

### Hardware Information

```bash
# CPU information
cat /proc/cpuinfo
nproc  # Number of available processing units

# Memory information
free -h
cat /proc/meminfo

# Disk information
df -h
lsblk
cat /proc/partitions

# Load average
cat /proc/loadavg
```

## Package Inventory Commands

### System Packages (Debian/Ubuntu)

```bash
# List all installed packages
dpkg -l

# List installed packages (alternative)
dpkg --get-selections

# Show package versions for specific packages
dpkg -l | grep -E "(nginx|docker|nodejs|pm2|ssh)"
```

### Node.js Packages

```bash
# Global npm packages
npm list -g --depth=0

# Node.js version
node --version
npm --version

# PM2 process list
pm2 jlist
pm2 list
pm2 info all
```

### Python Packages (if applicable)

```bash
# pip list if Python is installed
pip list 2>/dev/null || pip3 list 2>/dev/null || echo "pip not available"
```

## Service Status Commands

### Systemd Services

```bash
# Running services
systemctl list-units --type=service --state=running
systemctl list-units --type=service --state=running --no-pager

# All services (including failed)
systemctl list-units --type=service --all --no-pager

# Specific service status
systemctl status nginx
systemctl status docker
systemctl status ssh
systemctl status pm2-admin 2>/dev/null || echo "pm2-admin service not found"

# Service failed status
systemctl --failed --type=service
```

### Process Information

```bash
# All running processes
ps aux

# Top processes by CPU/memory
top -bn1 | head -20

# PM2 processes
pm2 monit  # Interactive monitoring
pm2 jlist  # JSON output
pm2 desc <process_id>  # Process details
```

### Docker Containers

```bash
# Running containers
docker ps

# All containers (including stopped)
docker ps -a

# Docker images
docker images

# Docker system info
docker system df
docker info
```

## Network Configuration Commands

### Network Interfaces

```bash
# IP addresses
ip addr
ip a

# Network interface statistics
ip -s link

# Routing table
ip route
ip route show

# ARP table
ip neigh
```

### Port and Socket Information

```bash
# Listening ports
ss -tulpn
ss -tulpn | grep LISTEN

# All connections
ss -tan

# Network statistics
ss -s

# Firewall status
ufw status
ufw status numbered
ufw verbose
```

### DNS Configuration

```bash
# DNS resolvers
cat /etc/resolv.conf

# DNS lookup test
nslookup google.com 2>/dev/null || echo "nslookup not available"
dig google.com +short 2>/dev/null || echo "dig not available"
host google.com 2>/dev/null || echo "host not available"
```

## Configuration File Commands

### Nginx Configuration

```bash
# Main nginx configuration
cat /etc/nginx/nginx.conf

# Nginx sites-enabled
cat /etc/nginx/sites-enabled/*
cat /etc/nginx/sites-available/*

# Nginx configuration test
nginx -t
nginx -T  # Show all configuration
```

### SSH Configuration

```bash
# SSH daemon configuration
cat /etc/ssh/sshd_config

# SSH configuration test
sshd -t

# SSH authorized keys (user-specific)
cat ~/.ssh/authorized_keys 2>/dev/null || echo "No authorized_keys found"
ls -la ~/.ssh/ 2>/dev/null || echo ".ssh directory not found"
```

### Firewall Configuration

```bash
# UFW status
ufw status

# UFW rules (numbered)
ufw status numbered

# iptables rules (if used)
iptables -L -n -v
iptables -S
```

### PM2 Configuration

```bash
# PM2 ecosystem config
cat /var/www/portfolio/ecosystem.config.js 2>/dev/null || echo "Ecosystem config not found in default location"

# PM2 logs directory
ls -la /var/www/portfolio/.pm2/logs/ 2>/dev/null || echo "PM2 logs not found"
```

## Log File Commands

### Authentication Logs

```bash
# SSH authentication attempts
tail -n 100 /var/log/auth.log
grep -i ssh /var/log/auth.log
grep -i "failed password" /var/log/auth.log

# Last login information
last
lastlog
```

### Nginx Logs

```bash
# Access log
tail -n 100 /var/log/nginx/access.log
tail -n 100 /var/log/nginx/access.log | grep -v "127.0.0.1"  # Exclude local

# Error log
tail -n 100 /var/log/nginx/error.log
tail -n 50 /var/log/nginx/error.log | grep -i error

# Other web server logs
tail -n 100 /var/log/apache2/access.log 2>/dev/null || echo "Apache not installed"
tail -n 100 /var/log/apache2/error.log 2>/dev/null || echo "Apache not installed"
```

### Application Logs

```bash
# PM2 logs
tail -n 100 /var/www/portfolio/.pm2/logs/pm2-out.log
tail -n 100 /var/www/portfolio/.pm2/logs/pm2-err.log

# Application-specific logs
ls -la /var/www/portfolio/logs/ 2>/dev/null || echo "Application logs directory not found"
```

### System Logs

```bash
# System journal
journalctl -xe --no-pager -n 50

# Kernel messages
dmesg | tail -n 50

# Syslog
tail -n 100 /var/log/syslog 2>/dev/null || echo "Syslog not available"
tail -n 100 /var/log/messages 2>/dev/null || echo "Messages not available"
```

## Performance Metrics Commands

### Disk Usage

```bash
# Disk usage by filesystem
df -h

# Disk usage by directory (top 20)
du -sh /var/* 2>/dev/null | sort -hr | head -20
du -sh /var/www/* 2>/dev/null | sort -hr | head -20
du -sh /var/www/portfolio/* 2>/dev/null | sort -hr | head -20
```

### Memory Usage

```bash
# Memory and swap usage
free -h

# Detailed memory info
cat /proc/meminfo | grep -E "(MemTotal|MemFree|MemAvailable|SwapTotal|SwapFree)"

# Memory usage by process
ps aux --sort=-%mem | head -15
```

### CPU Usage

```bash
# CPU load averages
cat /proc/loadavg
uptime

# CPU info
lscpu 2>/dev/null || cat /proc/cpuinfo | head -20
```

### I/O Statistics

```bash
# I/O statistics
iostat 2>/dev/null || echo "iostat not available"
iotop 2>/dev/null || echo "iotop not available"

# Disk I/O
cat /proc/diskstats
```

## Security Commands

### User Management

```bash
# List users
cat /etc/passwd | grep -v nologin

# List groups
cat /etc/group

# Last users logged in
last | head -20

# Currently logged in users
who
w
```

### File Permissions

```bash
# Critical file permissions
ls -la /etc/passwd /etc/shadow /etc/group
ls -la /etc/ssh/sshd_config
ls -la /var/www/portfolio/ecosystem.config.js 2>/dev/null

# SUID files
find / -type f -perm -4000 2>/dev/null | head -10
```

### OpenSSL/Security

```bash
# SSL certificate info
openssl x509 -in /etc/ssl/certs/server.crt -text -noout 2>/dev/null || echo "Server cert not found"
openssl s_client -connect localhost:443 -servername localhost 2>/dev/null | head -20 || echo "SSL check failed"

# Security updates
apt list --upgradable 2>/dev/null | grep security
```

## Docker-Specific Commands

### Container Management

```bash
# List all containers with status
docker ps -a --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# Container resource usage
docker stats --no-stream

# Container logs
docker logs --tail 100 <container_name_or_id>

# Inspect container
docker inspect <container_name_or_id>
```

### Image Management

```bash
# List all images with sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"

# Docker system disk usage
docker system df -v
```

## Collection Script

### Automated Collection (if available)

```bash
# If the collection script is deployed
./collect-evidence.sh <server_hostname>

# Or run specific modules
./collect-evidence.sh system-info
./collect-evidence.sh packages
./collect-evidence.sh services
./collect-evidence.sh network
./collect-evidence.sh configs
./collect-evidence.sh logs
./collect-evidence.sh performance
```

## Output Redirection

For evidence collection, redirect output to files:

```bash
# Example: Collect system info
hostnamectl > system-info.txt
uname -a >> system-info.txt
cat /etc/os-release >> system-info.txt

# Example: Collect all services
systemctl list-units --type=service --all --no-pager > services.txt
```

## File Transfer Commands

### SCP (Secure Copy)

```bash
# Download evidence from server
scp -P 2260 admin@192.168.1.60:/path/to/evidence.txt ./evidence/
scp -P 2260 admin@192.168.1.60:/var/log/nginx/access.log ./evidence/
```

### Rsync (for larger transfers)

```bash
# Sync evidence directory
rsync -avz -e "ssh -p 2260" admin@192.168.1.60:/path/to/evidence/ ./evidence/
```
