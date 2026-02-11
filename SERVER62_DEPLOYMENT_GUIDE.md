# Server62 Deployment Setup Guide

## Overview

Complete guide for deploying the marketing portfolio to server62 (89.203.173.196:2262) using GitHub Actions.

## Prerequisites

### SSH Key Access

Ensure you have SSH key access to server62. The deployment uses SSH key authentication for security.

### Required GitHub Secrets

Configure these secrets in your GitHub repository settings:

```yaml
VPS_IP: '89.203.173.196' # Public IP address
VPS_SSH_PORT: '2262' # SSH port for server62
VPS_USER: 'your-username' # SSH username on server62
VPS_SSH_KEY: '-----BEGIN OPENSSH...' # Private SSH key content
```

## Server62 Configuration

### 1. Create Web Directory

```bash
# Create deployment directory
sudo mkdir -p /var/www/portfolio
sudo chown $USER:$USER /var/www/portfolio
```

### 2. Install Node.js & PM2

```bash
# Install Node.js 20+ if not present
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 globally
sudo npm install -g pm2
```

### 3. Setup Web Server (Nginx)

```bash
# Install Nginx
sudo apt update && sudo apt install nginx

# Create site configuration
sudo bash -c 'cat > /etc/nginx/sites-available/portfolio << EOF
server {
    listen 80;
    server_name portfolio.tvoje.info www.portfolio.tvoje.info;

    root /var/www/portfolio/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ =404;
    }

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/xml;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF'

# Enable site
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 4. SSL Certificate Setup

```bash
# Install Certbot for Let's Encrypt
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d portfolio.tvoje.info -d www.portfolio.tvoje.info --agree-tos --email your@email.com

# Auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

## GitHub Actions Configuration

### Deployment Workflow Features

- **SSH Key Authentication**: Secure key-based login
- **Custom Port Support**: Configurable SSH port (2262)
- **Timeout Handling**: 300s total, 60s per command
- **PM2 Integration**: Automatic process management
- **Rollback Support**: Built-in deployment recovery

### Environment Variables

The deployment automatically sets:

- `NODE_ENV=production`
- `PUBLIC_SITE_URL=https://portfolio.tvoje.info`

## Testing Deployment

### 1. Manual Test

```bash
# Test SSH connectivity
ssh -p 2262 user@89.203.173.196 "hostname && whoami"

# Test directory creation
ssh -p 2262 user@89.203.173.196 "sudo mkdir -p /var/www/portfolio"
```

### 2. GitHub Actions Test

1. Push a small change to trigger deployment
2. Monitor GitHub Actions workflow execution
3. Verify build and deployment steps complete successfully

### 3. Post-Deployment Verification

```bash
# Check PM2 status
ssh -p 2262 user@89.203.173.196 "pm2 status"

# Check website accessibility
curl -I https://portfolio.tvoje.info

# Test both HTTP and HTTPS
curl -I http://portfolio.tvoje.info
curl -I https://portfolio.tvoje.info
```

## Security Configuration

### SSH Hardening (Recommended)

```bash
# Install fail2ban (CRITICAL)
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Configure fail2ban for custom SSH port
sudo bash -c 'cat > /etc/fail2ban/jail.local << EOF
[sshd]
enabled = true
port = 20,2262
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
EOF'

sudo systemctl restart fail2ban
```

### Firewall Rules

```bash
# Ensure UFW allows required ports
sudo ufw allow 2262/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

## Monitoring & Maintenance

### PM2 Monitoring

```bash
# View process status
ssh -p 2262 user@89.203.173.196 "pm2 monit"

# View logs
ssh -p 2262 user@89.203.173.196 "pm2 logs portfolio"

# Restart if needed
ssh -p 2262 user@89.203.173.196 "pm2 restart portfolio"
```

### Log Management

```bash
# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# PM2 application logs
ssh -p 2262 user@89.203.173.196 "tail -f /var/www/portfolio/.pm2/logs/portfolio-out.log"

# System logs
sudo journalctl -u nginx -f
```

## Troubleshooting

### Common Issues

#### SSH Connection Failed

- **Check**: NAT port forwarding on router
- **Verify**: SSH key permissions (600)
- **Test**: Internal connectivity first (192.168.1.62:2262)
- **Debug**: `ssh -vvv` for verbose output

#### Build Failures

- **Check**: Node.js version (`node --version`)
- **Verify**: Dependencies (`npm ci`)
- **Logs**: GitHub Actions build logs
- **Fix**: Update dependencies or Node version

#### Nginx Configuration Errors

- **Test**: `nginx -t` before reloading
- **Check**: File permissions in `/var/www/portfolio/`
- **Verify**: Domain DNS resolution
- **Debug**: `nginx -T` for detailed config

#### PM2 Process Issues

- **Restart**: `pm2 restart portfolio`
- **Check**: `pm2 status` for process status
- **Monitor**: `pm2 logs` for error messages
- **Reset**: `pm2 delete portfolio && pm2 start ecosystem.config.js`

## Performance Optimization

### Nginx Caching

- Static assets cached for 1 year
- Gzip compression enabled
- Security headers configured
- CDN ready for static assets

### Application Performance

- PM2 cluster mode available
- Memory limits: 1GB per process
- Auto-restart on crashes
- Zero-downtime deployments

## Backup Strategy

### Application Backup

```bash
# Backup deployment directory
ssh -p 2262 user@89.203.173.196 "sudo tar -czf /var/backups/portfolio-$(date +%Y%m%d-%H%M%S).tar.gz /var/www/portfolio"

# Backup PM2 configuration
ssh -p 2262 user@89.203.173.196 "cp /var/www/portfolio/ecosystem.config.js /var/backups/ecosystem-$(date +%Y%m%d-%H%M%S).js"
```

### Database Backup (if applicable)

```bash
# MySQL backup example
mysqldump -u user -p database_name | gzip > database_backup.sql.gz

# PostgreSQL backup example
pg_dump database_name | gzip > database_backup.sql.gz
```

## Contact Information

### Domain Setup

- **Primary Domain**: portfolio.tvoje.info
- **Alternative**: www.portfolio.tvoje.info
- **Public IP**: 89.203.173.196
- **SSH Port**: 2262
- **Server Location**: Internal network (192.168.1.62)

### Support Channels

- **Documentation**: This setup guide
- **GitHub Issues**: Repository issues
- **Monitoring**: PM2 logs + Nginx access logs
- **Security**: fail2ban logs + UFW status

---

## Deployment Checklist

- [ ] GitHub secrets configured
- [ ] Server62 SSH key access verified
- [ ] Web directory created (`/var/www/portfolio`)
- [ ] Node.js 20+ installed
- [ ] PM2 installed globally
- [ ] Nginx configured and enabled
- [ ] SSL certificate obtained and configured
- [ ] UFW firewall rules updated
- [ ] fail2ban installed and configured
- [ ] Test deployment completed successfully
- [ ] Monitoring and logging operational
- [ ] Backup procedures documented and tested

---

**Next Steps**: Follow this guide to complete server62 deployment setup and test the GitHub Actions deployment pipeline.
