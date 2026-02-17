# Server Monitor Mode - Strict Read-Only Rules

This document defines the strict read-only rules for the server-monitor mode. All commands must adhere to these rules to ensure safe, non-intrusive server monitoring.

## Core Principle

**READ-ONLY BY DESIGN**: This mode is strictly read-only. No command should modify any server state, install packages, change configurations, or affect running services.

---

## ALLOWED COMMANDS

### System Information (Read-Only)

```bash
# Host identification
hostnamectl
uname -a
uname -mrs
cat /etc/os-release
lsb_release -a
cat /etc/lsb-release

# System uptime and load
uptime
cat /proc/uptime

# Memory information
free -h
cat /proc/meminfo
vmstat

# CPU information
cat /proc/cpuinfo
lscpu

# Disk usage
df -h
df -i
du -sh /var/* 2>/dev/null | head -20

# Load average
cat /proc/loadavg
```

### Package Inventory (Read-Only)

```bash
# Debian/APT packages
dpkg -l
dpkg-query -W -f='${Package} ${Version} ${Status}\n'
apt list --installed
apt list --upgradable

# npm global packages
npm list -g --depth=0
npm list -g --depth=1

# PM2 process manager
pm2 list
pm2 jlist
pm2 monit

# Python packages (if applicable)
pip list
pip3 list

# Ruby gems (if applicable)
gem list --local
```

### Service Status (Read-Only)

```bash
# Systemd services
systemctl status
systemctl list-units --type=service --state=running
systemctl list-units --type=service --all
systemctl list-dependencies

# Process listing
ps aux
ps auxf
ps -ef
ps aux --sort=-%mem | head -20
ps aux --sort=-%cpu | head -20

# Top processes (non-interactive)
top -b -n 1

# Alternative process tools
htop -b -n 1 2>/dev/null || echo "htop not available"
glances 2>/dev/null || echo "glances not available"
```

### Network Information (Read-Only)

```bash
# Network interfaces
ip addr
ip link
ip neigh

# Port listening status
ss -tulpn
netstat -tulpn
netstat -lnpu

# Firewall status
ufw status
ufw status numbered
iptables -L -n
iptables -S

# DNS configuration
cat /etc/resolv.conf
nslookup localhost 2>/dev/null
dig localhost 2>/dev/null

# Routing
ip route
ip route show
route -n

# Connectivity tests
ping -c 1 8.8.8.8 2>/dev/null || echo "ping failed"
curl -s http://localhost:health 2>/dev/null || echo "health check failed"
curl -sI http://localhost 2>/dev/null | head -5

# Tailscale status (if available)
tailscale status 2>/dev/null || echo "tailscale not available"
tailscale ip 2>/dev/null || echo "tailscale ip not available"
```

### Configuration Files (READ ONLY)

```bash
# Nginx configuration
cat /etc/nginx/nginx.conf
cat /etc/nginx/sites-available/*
cat /etc/nginx/sites-enabled/*

# SSH configuration
cat /etc/ssh/sshd_config
cat /etc/ssh/ssh_config

# Environment
cat /etc/environment
cat /etc/profile
cat /var/www/portfolio/.env 2>/dev/null
cat /var/www/portfolio/.env.production 2>/dev/null
cat ~/portfolio/.env 2>/dev/null

# Application configs
cat ecosystem.config.js
cat /var/www/portfolio/package.json 2>/dev/null

# System configs
cat /etc/sysctl.conf
cat /etc/security/limits.conf

# Database configs (read-only)
cat /etc/mysql/mariadb.conf 2>/dev/null
cat /etc/postgresql/pg_hba.conf 2>/dev/null
```

### Log Files (READ ONLY)

```bash
# Nginx logs
tail -n 50 /var/log/nginx/access.log
tail -n 50 /var/log/nginx/error.log
tail -n 100 /var/log/nginx/access.log.1 2>/dev/null

# Authentication logs
tail -n 100 /var/log/auth.log
tail -n 100 /var/log/secure 2>/dev/null
tail -n 50 /var/log/syslog 2>/dev/null

# Application logs
tail -n 100 /var/log/portfolio/error.log 2>/dev/null
tail -n 50 /var/log/pm2.log
cat /root/.pm2/logs/*-out.log 2>/dev/null | tail -n 100

# System logs
dmesg | tail -n 50
journalctl -u nginx 2>/dev/null | tail -n 50
journalctl -u pm2-portfolio 2>/dev/null | tail -n 50
```

### Performance Metrics (Read-Only)

```bash
# System performance
sar 2>/dev/null
sar -u 2>/dev/null
sar -r 2>/dev/null
sar -d 2>/dev/null
iostat 2>/dev/null

# Memory and swap
swapon --show
cat /proc/swaps

# Disk I/O
iotop -b -n 1 2>/dev/null || echo "iotop not available"

# Network statistics
ss -s
ip -s link
```

### File System (Read-Only)

```bash
# Directory listings
ls -la /etc/nginx/
ls -la /var/www/portfolio/ 2>/dev/null
ls -la /var/log/nginx/
ls -la /root/

# File details
stat /etc/nginx/nginx.conf
stat /var/www/portfolio/package.json 2>/dev/null

# Directory sizes
du -sh /var/www/* 2>/dev/null
du -sh /var/log/* 2>/dev/null
```

---

## STRICTLY FORBIDDEN COMMANDS

### File System Destruction

```bash
# These are ALWAYS forbidden
rm -rf /
rm -rf /etc/*
rm -rf /var/*
del
erase
mkfs
mkfs.ext4
mkfs.xfs
dd
shred
```

### Package Management

```bash
# Forbidden - these modify the system
sudo apt install
sudo apt update
sudo apt upgrade
sudo apt remove
sudo apt purge
sudo dpkg -i

npm install -g
npm install
npm remove -g
npm uninstall

pip install
pip install --upgrade
pip uninstall

gem install
gem uninstall

# Package manager services
sudo systemctl restart apt*
sudo systemctl stop apt*
```

### Service Management

```bash
# Forbidden - these modify service state
systemctl restart
systemctl stop
systemctl start
systemctl reload
systemctl enable
systemctl disable
systemctl kill

service restart
service stop
service start

pm2 restart
pm2 stop
pm2 start
pm2 delete
pm2 kill
pm2 resurrect
```

### System Operations

```bash
# Forbidden - these affect the system
reboot
shutdown
halt
poweroff
init 0
init 6
telinit 0
telinit 6

# Kernel modifications
sysctl -w
sysctl -p (with file argument)

# Module loading
modprobe
modprobe -r
```

### Permission Changes

```bash
# Forbidden - these change permissions
chmod
chown
chgrp
setfacl
setfattr

# On sensitive directories
chmod -R /etc/
chmod -R /var/www/
chown -R /etc/
chown -R /var/www/
```

### Configuration Editing

```bash
# Any command that writes to config files
echo "..." > /etc/*
cat > /etc/*
tee /etc/*
sed -i
vim /etc/*
nano /etc/*
nano /etc/ssh/sshd_config

# Environment variable modifications
export VAR=value
set -x VAR=value

# Cron modifications
crontab -e
echo "..." >> /etc/cron.d/*
```

### User Management

```bash
# Forbidden - these modify users/groups
useradd
usermod
userdel
groupadd
groupmod
groupdel
passwd
gpasswd

# Shadow file modifications
vipw
vigr
```

### Network Modifications

```bash
# Forbidden - these change network state
ip addr add
ip addr del
ip link set
ip link set down
ip route add
ip route del

# Firewall modifications
ufw enable
ufw disable
ufw delete
ufw allow
ufw deny
iptables -A
iptables -D
iptables -I

# SSH modifications
ssh-keygen
ssh-copy-id
```

### Database Operations

```bash
# Forbidden database commands
DROP DATABASE
DROP TABLE
DELETE FROM
TRUNCATE
UPDATE (with modifications)
INSERT INTO
ALTER TABLE
DROP TABLE
```

### Process Killing

```bash
# Forbidden - these can disrupt services
kill -9 (any PID)
killall
pkill
killall5

# Exceptions (may be allowed with explicit approval)
kill -TERM (for graceful shutdown of non-critical processes)
```

### Script Execution

```bash
# Scripts from untrusted sources
curl | bash
wget -O- | bash
bash <(curl ...)
source <(curl ...)

# Any script that could modify system state
./install.sh
./setup.sh
./deploy.sh
```

---

## COMMAND VALIDATION RULES

### Before Executing Any Command

1. **Check for forbidden keywords**: The command must not contain any forbidden keywords listed above.

2. **Check command purpose**: Verify the command is read-only and does not modify system state.

3. **Check file paths**: Ensure paths being accessed are within allowed directories for reading.

4. **Check output redirection**: If redirecting output, verify destination is local evidence directory.

5. **Review all arguments**: Verify all arguments are read-only flags.

### Validation Algorithm

```
function validateCommand(command):
    forbidden = [
        "rm", "del", "erase", "mkfs", "dd", "shred",
        "install", "update", "upgrade", "remove", "purge",
        "restart", "stop", "start", "reload", "enable", "disable",
        "reboot", "shutdown", "halt", "poweroff",
        "chmod", "chown", "chgrp",
        "crontab -e",
        "useradd", "usermod", "userdel", "groupadd", "groupmod",
        "-i", "-w"
    ]

    for keyword in forbidden:
        if keyword in command:
            return false, "Command contains forbidden keyword: ${keyword}"

    # Additional checks for specific patterns
    if matchesPattern(command, "* > /etc/*"):
        return false, "Cannot write to /etc/"
    if matchesPattern(command, "* > /var/www/*"):
        return false, "Cannot write to /var/www/"
    if matchesPattern(command, "* >> /etc/*"):
        return false, "Cannot append to /etc/"
    if matchesPattern(command, "* >> /var/www/*"):
        return false, "Cannot append to /var/www/"

    return true, "Command is valid"
```

---

## EMERGENCY BREAK-GLASS PROCEDURES

In case of accidental execution of a forbidden command:

1. **Immediately disconnect** from the server
2. **Document the incident** in the evidence collection
3. **Notify the operator** of the accidental execution
4. **Do not attempt remediation** - leave system as-is for forensic analysis
5. **Document all actions** taken before and after the incident

---

## REPORTING VIOLATIONS

If a command is attempted that violates these rules:

1. **Reject the command** immediately
2. **Log the attempted command** with timestamp
3. **Explain why it was rejected**
4. **Suggest alternative read-only approach** if applicable

---

## APPROVAL CHAIN FOR EMERGENCY OPERATIONS

If absolutely necessary to perform a potentially dangerous operation:

1. **Request verbal confirmation** from operator
2. **Document the justification** for the operation
3. **Wait for explicit approval** ("Proceed with caution")
4. **Execute the minimum required command**
5. **Document the outcome** immediately

---

## References

- Server Inventory: `.kilocode/skills/server-monitor/server-inventory.md`
- Safe SSH Scripts: `.kilocode/scripts/server-monitor/`
- Workflows: `.kilocode/workflows/server-monitor/`
