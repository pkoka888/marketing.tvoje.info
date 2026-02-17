# Server Monitor Skills

This document defines the skills available in the server-monitor mode for safe server evidence gathering and comparison.

## Skill Overview

| Skill                    | Purpose                               | Risk Level       |
| ------------------------ | ------------------------------------- | ---------------- |
| System Info Gathering    | Collect OS, kernel, hardware info     | None (read-only) |
| Package Inventory        | List all installed packages           | None (read-only) |
| Service Status           | Document running services             | None (read-only) |
| Network Configuration    | Network interfaces, firewall, routing | None (read-only) |
| Configuration Audit      | Read and document config files        | None (read-only) |
| Log Analysis             | Extract recent errors and warnings    | None (read-only) |
| Performance Metrics      | CPU, memory, disk, network usage      | None (read-only) |
| Configuration Comparison | Compare configs across servers        | None (read-only) |

---

## Skill 1: System Information Gathering

### Description

Collect comprehensive system information including operating system details, kernel version, hardware specifications, and system metrics.

### Commands Executed

#### Operating System

```bash
hostnamectl
cat /etc/os-release
lsb_release -a
uname -a
uname -mrs
```

#### Hardware Information

```bash
# CPU
cat /proc/cpuinfo
lscpu

# Memory
free -h
cat /proc/meminfo

# Disk
df -h
df -i

# Load
cat /proc/loadavg
uptime
```

#### System Metrics

```bash
# Disk usage by directory
du -sh /var/* 2>/dev/null | head -20
du -sh /etc/* 2>/dev/null | head -20

# Swap usage
cat /proc/swaps
swapon --show
```

### Output Files Generated

- `system-info.txt` - OS, hostname, kernel details
- `hardware-info.txt` - CPU, memory, disk specifications
- `system-metrics.txt` - Load averages, disk usage, memory usage

### Evidence Categories

1. OS Distribution and Version
2. Kernel Version and Architecture
3. Hostname and Domain
4. CPU Model and Core Count
5. Memory Total and Available
6. Disk Space Total and Used
7. System Load Averages

---

## Skill 2: Package Inventory

### Description

Enumerate all installed packages across different package managers for complete software inventory.

### Commands Executed

#### APT/Debian Packages

```bash
dpkg -l
dpkg-query -W -f='${Package} ${Version} ${Status}\n'
apt list --installed
apt list --upgradable
```

#### npm Global Packages

```bash
npm list -g --depth=0
npm list -g --depth=1
```

#### PM2 Processes

```bash
pm2 list
pm2 jlist
pm2 monit
```

#### Python Packages (if applicable)

```bash
pip list 2>/dev/null
pip3 list 2>/dev/null
```

### Output Files Generated

- `packages-apt.txt` - All APT packages
- `packages-npm.txt` - Global npm packages
- `packages-pm2.txt` - PM2 process list
- `packages-upgradable.txt` - Packages with updates available

### Evidence Categories

1. Installed APT Packages (name, version, status)
2. Global npm Packages (name, version)
3. PM2 Managed Applications (name, status, restart count)
4. Available Package Updates

---

## Skill 3: Service Status

### Description

Document all running services, their states, and process information.

### Commands Executed

#### Systemd Services

```bash
systemctl status
systemctl list-units --type=service --state=running
systemctl list-units --type=service --all
systemctl list-dependencies
```

#### Process Information

```bash
ps aux
ps auxf
ps -ef
ps aux --sort=-%mem | head -20
ps aux --sort=-%cpu | head -20
```

#### Top Processes (non-interactive)

```bash
top -b -n 1
```

### Output Files Generated

- `services-systemd.txt` - All systemd services status
- `services-running.txt` - Currently running services
- `processes.txt` - All running processes
- `processes-by-memory.txt` - Top 20 processes by memory
- `processes-by-cpu.txt` - Top 20 processes by CPU

### Evidence Categories

1. Systemd Services (name, active state, sub state)
2. Running Processes (PID, user, CPU%, MEM%, command)
3. Process Tree
4. Service Dependencies

---

## Skill 4: Network Configuration

### Description

Gather network interface details, firewall rules, and network connectivity information.

### Commands Executed

#### Network Interfaces

```bash
ip addr
ip link
ip neigh
```

#### Port Listening Status

```bash
ss -tulpn
netstat -tulpn
```

#### Firewall Status

```bash
ufw status
ufw status numbered
iptables -L -n
```

#### DNS Configuration

```bash
cat /etc/resolv.conf
nslookup localhost 2>/dev/null
```

#### Routing

```bash
ip route
ip route show
route -n
```

#### Connectivity Tests

```bash
ping -c 1 8.8.8.8 2>/dev/null || echo "ping failed"
curl -sI http://localhost 2>/dev/null | head -5
```

### Output Files Generated

- `network-interfaces.txt` - IP addresses, interfaces
- `network-ports.txt` - Listening ports
- `network-firewall.txt` - UFW and iptables rules
- `network-dns.txt` - DNS configuration
- `network-routing.txt` - Routing table
- `network-connectivity.txt` - Connectivity tests

### Evidence Categories

1. Network Interfaces (name, state, IP addresses, MAC addresses)
2. Listening Ports (port, protocol, process)
3. Firewall Rules (action, source, destination, port)
4. DNS Servers
5. Routing Table
6. Neighbor Discovery

---

## Skill 5: Configuration Audit

### Description

Read and document all configuration files for system and application components.

### Commands Executed

#### Nginx Configuration

```bash
cat /etc/nginx/nginx.conf
cat /etc/nginx/sites-available/*
cat /etc/nginx/sites-enabled/*
```

#### SSH Configuration

```bash
cat /etc/ssh/sshd_config
cat /etc/ssh/ssh_config
```

#### Environment Files

```bash
cat /etc/environment
cat /etc/profile
cat /var/www/portfolio/.env 2>/dev/null
cat ~/portfolio/.env 2>/dev/null
cat ecosystem.config.js
```

#### Application Configuration

```bash
cat /var/www/portfolio/package.json 2>/dev/null
cat /etc/sysctl.conf
cat /etc/security/limits.conf
```

### Output Files Generated

- `config-nginx.txt` - Nginx configuration
- `config-ssh.txt` - SSH daemon configuration
- `config-env.txt` - Environment variables
- `config-app.txt` - Application configuration
- `config-system.txt` - System configurations

### Evidence Categories

1. Nginx Server Blocks
2. SSH Settings (port, authentication methods, permit settings)
3. Environment Variables
4. Application Configuration
5. System Limits

---

## Skill 6: Log Analysis

### Description

Extract and analyze recent logs for errors, warnings, and system events.

### Commands Executed

#### Nginx Logs

```bash
tail -n 50 /var/log/nginx/access.log
tail -n 50 /var/log/nginx/error.log
tail -n 100 /var/log/nginx/access.log.1 2>/dev/null
```

#### Authentication Logs

```bash
tail -n 100 /var/log/auth.log
tail -n 100 /var/log/secure 2>/dev/null
tail -n 50 /var/log/syslog 2>/dev/null
```

#### Application Logs

```bash
tail -n 100 /var/log/portfolio/error.log 2>/dev/null
tail -n 50 /var/log/pm2.log
cat /root/.pm2/logs/*-out.log 2>/dev/null | tail -n 100
```

#### System Logs

```bash
dmesg | tail -n 50
journalctl -u nginx 2>/dev/null | tail -n 50
journalctl -u pm2-portfolio 2>/dev/null | tail -n 50
```

### Output Files Generated

- `logs-nginx-access.txt` - Nginx access log (recent)
- `logs-nginx-error.txt` - Nginx error log
- `logs-auth.txt` - Authentication logs
- `logs-app.txt` - Application logs
- `logs-system.txt` - System logs

### Evidence Categories

1. Recent HTTP Requests (last 50 lines)
2. Error Log Entries (last 50 lines)
3. Authentication Attempts (last 100 lines)
4. Application Errors (last 100 lines)
5. System Events (last 50 lines)

---

## Skill 7: Performance Metrics

### Description

Collect performance metrics including CPU usage, memory usage, disk I/O, and network statistics.

### Commands Executed

#### CPU and Memory

```bash
cat /proc/loadavg
free -h
cat /proc/meminfo
```

#### Disk Usage

```bash
df -h
df -i
du -sh /var/www/* 2>/dev/null | head -20
```

#### Network Statistics

```bash
ss -s
ip -s link
```

#### System Activity (if available)

```bash
sar -u 2>/dev/null
sar -r 2>/dev/null
iostat 2>/dev/null
```

### Output Files Generated

- `perf-cpu-memory.txt` - CPU and memory metrics
- `perf-disk.txt` - Disk usage and I/O
- `perf-network.txt` - Network statistics
- `perf-sar.txt` - System activity report

### Evidence Categories

1. Load Average (1, 5, 15 minute)
2. Memory Usage (total, used, free, available)
3. Disk Space (total, used, available, inodes)
4. Network Connections (established, listening)
5. Network Interface Statistics

---

## Skill 8: Configuration Comparison

### Description

Compare configurations, package versions, and settings across multiple servers to identify drift.

### Commands Executed

#### Cross-Server Package Comparison

```bash
# Collect package versions from all servers
dpkg -l | grep "^ii" | awk '{print $2, $3}'
npm list -g --depth=0
pm2 list
```

#### Cross-Server Service Comparison

```bash
# Collect running services from all servers
systemctl list-units --type=service --state=running
```

#### Cross-Server Network Comparison

```bash
# Collect listening ports from all servers
ss -tulpn
ufw status
```

### Output Files Generated

- `comparison-packages.md` - Package version comparison
- `comparison-services.md` - Service status comparison
- `comparison-network.md` - Network configuration comparison
- `comparison-configs.md` - Configuration drift analysis
- `drift-report.md` - Comprehensive drift report

### Evidence Categories

1. Package Version Differences
2. Missing Packages (per server)
3. Service State Differences
4. Port Listening Differences
5. Configuration Drift
6. Security Setting Differences

---

## Skill Usage Guidelines

### Prerequisites

1. SSH access to target servers configured
2. Valid SSH key for authentication
3. Tailscale VPN connection (or direct network access)

### Execution Order

1. **System Info Gathering** - Baseline system information
2. **Network Configuration** - Verify connectivity first
3. **Package Inventory** - Dependencies for services
4. **Service Status** - Running processes
5. **Configuration Audit** - Configuration files
6. **Log Analysis** - Recent events
7. **Performance Metrics** - Current state
8. **Configuration Comparison** - Cross-server analysis

### Error Handling

- Skip commands that fail (log error, continue)
- Retry connection attempts up to 3 times
- Document partial failures in evidence
- Generate incomplete evidence if critical commands fail

### Output Preservation

- All evidence stored in `evidence/{server}/{timestamp}/`
- Create symlink `evidence/{server}/latest` to latest timestamp
- Generate summary markdown for quick review
- Maintain evidence for audit trail
