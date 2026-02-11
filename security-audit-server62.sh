#!/bin/bash

# Comprehensive Security Audit Script for server62 (192.168.1.62)
# READ-ONLY ANALYSIS - This script only gathers information, makes no changes
# Run with: sudo bash security-audit.sh

echo "=============================================="
echo "COMPREHENSIVE SECURITY AUDIT FOR SERVER62"
echo "Timestamp: $(date)"
echo "=============================================="

# Create output directory
AUDIT_DIR="/tmp/security-audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AUDIT_DIR"
cd "$AUDIT_DIR"

echo "Audit results will be saved to: $AUDIT_DIR"
echo ""

# Function to run command and save to file
run_and_save() {
    local cmd="$1"
    local output_file="$2"
    local description="$3"
    
    echo "Running: $description"
    echo "Command: $cmd" > "$output_file"
    echo "" >> "$output_file"
    echo "$description:" >> "$output_file"
    echo "=====================================" >> "$output_file"
    eval "$cmd" >> "$output_file" 2>&1
    echo "Saved to: $output_file"
    echo ""
}

# Function to assess security
assess_security() {
    local check="$1"
    local status="$2"
    local recommendation="$3"
    
    echo "[$status] $check" >> security-assessment.txt
    if [ "$recommendation" != "" ]; then
        echo "  Recommendation: $recommendation" >> security-assessment.txt
    fi
    echo "" >> security-assessment.txt
}

# Initialize security assessment file
echo "SECURITY ASSESSMENT - server62 ($(date))" > security-assessment.txt
echo "=========================================" >> security-assessment.txt
echo "" >> security-assessment.txt

# 1. UFW FIREWALL ANALYSIS
echo "=============================================="
echo "1. UFW FIREWALL ANALYSIS"
echo "=============================================="

run_and_save "ufw status verbose" "01-ufw-status.txt" "UFW Status and Rules"
run_and_save "ufw app list" "01-ufw-apps.txt" "UFW Application Profiles"
run_and_save "cat /etc/ufw/ufw.conf" "01-ufw-config.txt" "UFW Configuration"
run_and_save "cat /etc/ufw/user.rules" "01-ufw-user-rules.txt" "UFW User Rules"
run_and_save "cat /etc/ufw/user6.rules" "01-ufw-user6-rules.txt" "UFW IPv6 User Rules"
run_and_save "ls -la /var/log/ufw* 2>/dev/null || echo 'No UFW logs found'" "01-ufw-logs.txt" "UFW Log Files"

# UFW Security Assessment
if command -v ufw >/dev/null 2>&1; then
    ufw_status=$(ufw status | head -1)
    if [[ "$ufw_status" == *"Status: active"* ]]; then
        assess_security "UFW Firewall" "GOOD" "UFW is active and protecting the system"
    else
        assess_security "UFW Firewall" "CRITICAL" "UFW is not active - enable firewall protection"
    fi
else
    assess_security "UFW Firewall" "NEEDS IMPROVEMENT" "UFW not installed - consider installing and configuring"
fi

# 2. IPTABLES DEEP DIVE
echo "=============================================="
echo "2. IPTABLES DEEP DIVE"
echo "=============================================="

run_and_save "iptables -L -v -n --line-numbers" "02-iptables-filter.txt" "iptables Filter Table"
run_and_save "iptables -t nat -L -v -n --line-numbers" "02-iptables-nat.txt" "iptables NAT Table"
run_and_save "iptables -t mangle -L -v -n --line-numbers" "02-iptables-mangle.txt" "iptables Mangle Table"
run_and_save "iptables -t raw -L -v -n --line-numbers" "02-iptables-raw.txt" "iptables Raw Table"
run_and_save "iptables-save" "02-iptables-rules.txt" "Complete iptables Rules"
run_and_save "ls -la /etc/iptables/ 2>/dev/null || echo 'No iptables directory found'" "02-iptables-config-files.txt" "iptables Configuration Files"

# 3. SSH SERVICE AUDIT
echo "=============================================="
echo "3. SSH SERVICE AUDIT"
echo "=============================================="

run_and_save "cat /etc/ssh/sshd_config" "03-ssh-config.txt" "SSH Daemon Configuration"
run_and_save "systemctl status sshd" "03-ssh-status.txt" "SSH Service Status"
run_and_save "sshd -T" "03-ssh-effective-config.txt" "Effective SSH Configuration"
run_and_save "ls -la /etc/ssh/ssh_host_*_key*" "03-ssh-host-keys.txt" "SSH Host Keys"

# SSH Security Assessment
if [ -f /etc/ssh/sshd_config ]; then
    # Check for root login
    if grep -q "^PermitRootLogin.*yes" /etc/ssh/sshd_config; then
        assess_security "SSH Root Login" "CRITICAL" "Disable root login in sshd_config"
    else
        assess_security "SSH Root Login" "GOOD" "Root login appears to be disabled"
    fi
    
    # Check for password authentication
    if grep -q "^PasswordAuthentication.*yes" /etc/ssh/sshd_config; then
        assess_security "SSH Password Authentication" "NEEDS IMPROVEMENT" "Consider using key-based authentication only"
    else
        assess_security "SSH Password Authentication" "GOOD" "Password authentication appears to be disabled"
    fi
    
    # Check for empty passwords
    if grep -q "^PermitEmptyPasswords.*yes" /etc/ssh/sshd_config; then
        assess_security "SSH Empty Passwords" "CRITICAL" "Disable empty passwords immediately"
    else
        assess_security "SSH Empty Passwords" "GOOD" "Empty passwords are disabled"
    fi
fi

# 4. NETWORK CONFIGURATION
echo "=============================================="
echo "4. NETWORK CONFIGURATION"
echo "=============================================="

run_and_save "ip addr show" "04-network-interfaces.txt" "Network Interfaces"
run_and_save "ip route show" "04-routing-table.txt" "Routing Table"
run_and_save "cat /etc/resolv.conf" "04-dns-config.txt" "DNS Configuration"
run_and_save "cat /etc/hosts" "04-hosts-file.txt" "Hosts File"
run_and_save "netstat -tulnp" "04-network-connections.txt" "Network Connections"
run_and_save "ss -tulnp" "04-network-connections-ss.txt" "Network Connections (ss)"
run_and_save "systemctl status networking 2>/dev/null || systemctl status NetworkManager 2>/dev/null || echo 'Network service not found'" "04-network-service.txt" "Network Service Status"

# 5. FAIL2BAN REVIEW
echo "=============================================="
echo "5. FAIL2BAN REVIEW"
echo "=============================================="

run_and_save "systemctl status fail2ban 2>/dev/null || echo 'fail2ban not installed or running'" "05-fail2ban-status.txt" "fail2ban Service Status"

if command -v fail2ban-client >/dev/null 2>&1; then
    run_and_save "fail2ban-client status" "05-fail2ban-client-status.txt" "fail2ban Client Status"
    run_and_save "fail2ban-client status sshd 2>/dev/null || echo 'SSH jail not configured'" "05-fail2ban-ssh-status.txt" "fail2ban SSH Jail Status"
    run_and_save "cat /etc/fail2ban/jail.conf 2>/dev/null" "05-fail2ban-jail-config.txt" "fail2ban Jail Configuration"
    run_and_save "cat /etc/fail2ban/jail.local 2>/dev/null || echo 'No jail.local found'" "05-fail2ban-jail-local.txt" "fail2ban Local Configuration"
    run_and_save "fail2ban-client banned" "05-fail2ban-banned.txt" "Currently Banned IPs"
    run_and_save "tail -50 /var/log/fail2ban.log 2>/dev/null || tail -50 /var/log/fail2ban.log.1 2>/dev/null || echo 'fail2ban log not found'" "05-fail2ban-recent-logs.txt" "Recent fail2ban Logs"
    
    # fail2ban Security Assessment
    assess_security "fail2ban" "GOOD" "fail2ban is installed and configured"
else
    assess_security "fail2ban" "NEEDS IMPROVEMENT" "Consider installing fail2ban for brute force protection"
fi

# 6. SSH KEYS & AUTHENTICATION
echo "=============================================="
echo "6. SSH KEYS & AUTHENTICATION"
echo "=============================================="

run_and_save "ls -la /home/" "06-user-homes.txt" "User Home Directories"

# Get all user accounts with home directories
for user in $(ls /home/ 2>/dev/null); do
    if [ -d "/home/$user" ]; then
        run_and_save "ls -la /home/$user/.ssh/ 2>/dev/null || echo 'No .ssh directory for $user'" "06-ssh-$user-dir.txt" "SSH Directory for $user"
        run_and_save "cat /home/$user/.ssh/authorized_keys 2>/dev/null || echo 'No authorized_keys for $user'" "06-ssh-$user-keys.txt" "Authorized Keys for $user"
        run_and_save "find /home/$user/.ssh/ -type f -exec ls -la {} \; 2>/dev/null" "06-ssh-$user-permissions.txt" "SSH File Permissions for $user"
    fi
done

# Check root SSH keys
run_and_save "ls -la /root/.ssh/ 2>/dev/null || echo 'No root .ssh directory'" "06-ssh-root-dir.txt" "Root SSH Directory"
run_and_save "cat /root/.ssh/authorized_keys 2>/dev/null || echo 'No root authorized_keys'" "06-ssh-root-keys.txt" "Root Authorized Keys"

# SSH Key Security Assessment
for user in $(ls /home/ 2>/dev/null); do
    if [ -f "/home/$user/.ssh/authorized_keys" ]; then
        perms=$(stat -c "%a" "/home/$user/.ssh/authorized_keys" 2>/dev/null)
        if [ "$perms" != "600" ] && [ "$perms" != "640" ]; then
            assess_security "SSH Keys - $user" "NEEDS IMPROVEMENT" "Set authorized_keys permissions to 600"
        fi
    fi
done

# 7. FILE PERMISSIONS & SECURITY
echo "=============================================="
echo "7. FILE PERMISSIONS & SECURITY"
echo "=============================================="

run_and_save "find / -type f -perm /4000 -exec ls -la {} \; 2>/dev/null" "07-suid-files.txt" "SUID Files"
run_and_save "find / -type f -perm /2000 -exec ls -la {} \; 2>/dev/null" "07-sgid-files.txt" "SGID Files"
run_and_save "find / -type f -perm /0002 -exec ls -la {} \; 2>/dev/null | head -50" "07-world-writable.txt" "World-Writable Files"
run_and_save "ls -la /etc/passwd /etc/shadow /etc/group /etc/gshadow" "07-critical-files.txt" "Critical System Files"
run_and_save "find /home/ -type d -perm /777 2>/dev/null" "07-world-writable-homes.txt" "World-Writable Home Directories"

# Check critical file permissions
if [ -f /etc/shadow ]; then
    shadow_perms=$(stat -c "%a" /etc/shadow 2>/dev/null)
    if [ "$shadow_perms" = "000" ] || [ "$shadow_perms" = "600" ]; then
        assess_security "/etc/shadow Permissions" "GOOD" "Shadow file has secure permissions"
    else
        assess_security "/etc/shadow Permissions" "CRITICAL" "Shadow file has insecure permissions"
    fi
fi

# 8. SYSTEM SECURITY
echo "=============================================="
echo "8. SYSTEM SECURITY"
echo "=============================================="

run_and_save "apt list --upgradable 2>/dev/null || yum check-update 2>/dev/null || dnf check-update 2>/dev/null || echo 'Package manager not found'" "08-package-updates.txt" "Available Package Updates"
run_and_save "systemctl list-units --type=service --state=running" "08-running-services.txt" "Running Services"
run_and_save "netstat -tlnp 2>/dev/null | grep LISTEN" "08-listening-ports.txt" "Listening Ports"
run_and_save "ss -tlnp 2>/dev/null | grep LISTEN" "08-listening-ports-ss.txt" "Listening Ports (ss)"
run_and_save "last -n 50" "08-last-logins.txt" "Last Login Activity"
run_and_save "tail -100 /var/log/auth.log 2>/dev/null || tail -100 /var/log/secure 2>/dev/null || echo 'Authentication log not found'" "08-auth-logs.txt" "Recent Authentication Logs"

# 9. USER ACCOUNTS
echo "=============================================="
echo "9. USER ACCOUNTS"
echo "=============================================="

run_and_save "cat /etc/passwd" "09-user-accounts.txt" "All User Accounts"
run_and_save "cat /etc/group" "09-groups.txt" "All Groups"
run_and_save "cat /etc/sudoers 2>/dev/null" "09-sudoers.txt" "Sudo Configuration"
run_and_save "ls -la /etc/sudoers.d/ 2>/dev/null" "09-sudoers-d.txt" "Sudoers.d Directory"

# Get users with sudo access
run_and_save "getent group sudo 2>/dev/null || getent group wheel 2>/dev/null || echo 'No sudo group found'" "09-sudo-users.txt" "Users with Sudo Access"

# User account security assessment
for user in $(cat /etc/passwd | cut -d: -f1); do
    if id "$user" >/dev/null 2>&1; then
        # Check if user has no password
        if passwd -S "$user" 2>/dev/null | grep -q "NP"; then
            assess_security "User Account - $user" "CRITICAL" "User $user has no password set"
        fi
    fi
done

# System information
run_and_save "uname -a" "00-system-info.txt" "System Information"
run_and_save "cat /etc/os-release" "00-os-info.txt" "Operating System Information"
run_and_save "uptime" "00-uptime.txt" "System Uptime"

echo "=============================================="
echo "AUDIT COMPLETED"
echo "=============================================="
echo "All results saved to: $AUDIT_DIR"
echo "Security assessment summary saved to: $AUDIT_DIR/security-assessment.txt"
echo ""
echo "To review the security assessment:"
echo "cat $AUDIT_DIR/security-assessment.txt"
echo ""
echo "To create a tar archive of all results:"
echo "tar -czf security-audit-$(hostname)-$(date +%Y%m%d).tar.gz $AUDIT_DIR"

# Display security assessment summary
echo ""
echo "SECURITY ASSESSMENT SUMMARY:"
echo "============================"
cat "$AUDIT_DIR/security-assessment.txt"