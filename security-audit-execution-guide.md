# Security Audit Execution Guide

## Prerequisites

- SSH access to server62 (192.168.1.62)
- Sudo/root privileges on the server
- Basic command line knowledge

## Step 1: Transfer Files to Server

Copy the security audit script to the server:

```bash
# Method 1: Using scp
scp security-audit-server62.sh user@192.168.1.62:/tmp/

# Method 2: Using sftp
sftp user@192.168.1.62
put security-audit-server62.sh /tmp/
exit
```

## Step 2: Connect to Server

```bash
ssh user@192.168.1.62
```

## Step 3: Execute Security Audit

```bash
# Navigate to script location
cd /tmp/

# Make script executable
chmod +x security-audit-server62.sh

# Run with sudo privileges
sudo bash security-audit-server62.sh
```

## Step 4: Collect Results

The script will create a directory with all results:

```bash
# Results will be in: /tmp/security-audit-YYYYMMDD-HHMMSS/
# Example: /tmp/security-audit-20240211-143022/

# Navigate to results directory
cd /tmp/security-audit-*

# View security assessment summary
cat security-assessment.txt

# Create archive for download
tar -czf security-audit-results.tar.gz *
```

## Step 5: Transfer Results Back

```bash
# Method 1: Using scp (from your local machine)
scp user@192.168.1.62:/tmp/security-audit-*/security-audit-results.tar.gz ./

# Method 2: Using sftp (from your local machine)
sftp user@192.168.1.62
get /tmp/security-audit-*/security-audit-results.tar.gz
exit
```

## Step 6: Analyze Results

1. Extract the archive:

```bash
tar -xzf security-audit-results.tar.gz
```

2. Review the security assessment:

```bash
cat security-assessment.txt
```

3. Use the report template to create your comprehensive analysis:

```bash
# Copy the template
cp security-audit-report-template.md server62-security-report.md

# Edit the report with your findings
nano server62-security-report.md
```

## Important Notes

### READ-ONLY Operation

- The audit script is designed to be READ-ONLY
- It only gathers information and makes no system changes
- All commands are non-destructive

### Script Safety

- The script uses only information-gathering commands
- No configuration files are modified
- No services are restarted or changed
- No packages are installed or removed

### Expected Runtime

- The audit typically takes 2-5 minutes to complete
- Larger systems may take longer
- Network-dependent commands may add time

### Troubleshooting

#### Permission Denied

```bash
# Ensure you have sudo privileges
sudo whoami

# If not, contact system administrator
```

#### Command Not Found

```bash
# Some commands may not be available on all systems
# The script handles missing commands gracefully
# Check individual command outputs in the results
```

#### Script Fails

```bash
# Check script syntax
bash -n security-audit-server62.sh

# Run with debug mode
bash -x security-audit-server62.sh
```

## Post-Audit Actions

### Immediate Actions

1. Review the security-assessment.txt file
2. Identify any CRITICAL findings
3. Address critical security issues immediately

### Documentation

1. Complete the security report template
2. Save all audit results for future reference
3. Schedule regular security audits

### Follow-up

1. Implement recommended security improvements
2. Verify changes are effective
3. Update security policies as needed

## Security Best Practices

### During Audit

- Use secure SSH connections
- Verify server identity before connecting
- Keep audit results confidential
- Store results in secure location

### After Audit

- Implement changes in test environment first
- Document all security changes
- Update system documentation
- Train users on new security policies

### Regular Maintenance

- Schedule quarterly security audits
- Monitor security logs regularly
- Keep systems updated
- Review user access periodically

## Contact Information

For questions or issues with the security audit:

- [Your Name]
- [Your Email]
- [Your Phone]
