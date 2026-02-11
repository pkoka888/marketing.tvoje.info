# GitHub Repository Setup and GitHub Actions Plan

**Document Type**: Implementation Plan  
**Status**: Draft  
**Version**: 1.0  
**Date**: 2026-02-11  
**Project**: marketing.tvoje.info (DevOps & AI Developer Portfolio)  
**Repository**: https://github.com/pkoka888/marketing.tvoje.info.git  
**Deployment Target**: Debian 13 VPS (not Vercel)

---

## Executive Summary

This plan documents the setup of the GitHub repository for the DevOps & AI Developer Portfolio. The project uses **Astro 5.0**, **Tailwind CSS 4.0**, and **TypeScript** for a performant, accessible, bilingual portfolio website.

**Deployment Strategy:**
- **Local Development**: Windows testing with `npm run dev`
- **Production**: Debian 13 VPS with PM2 and Nginx
- **CI/CD**: GitHub Actions for builds and security scanning

**Key Differences from Original Plan:**
- ❌ Vercel deployment **REMOVED**
- ✅ VPS deployment via SSH
- ❌ Snyk token **REMOVED** (using GitHub's built-in security)
- ✅ Added SSH deployment to custom VPS

---

## 1. Technology Stack Summary

| Component | Version | Purpose |
|-----------|---------|---------|
| **Framework** | Astro 5.0 | Static site generation |
| **Styling** | Tailwind CSS 4.0 | Utility-first CSS |
| **Language** | TypeScript 5.7 | Type safety |
| **Hosting** | Debian 13 VPS | Custom server |
| **Process Manager** | PM2 | Node.js application management |
| **Web Server** | Nginx | Reverse proxy (optional) |
| **Forms** | Formspree | Contact form backend |
| **Analytics** | Plausible | Privacy-focused analytics |
| **CI/CD** | GitHub Actions | Automation |

---

## 2. GitHub Actions Workflows

### 2.1 CI Workflow (.github/workflows/ci.yml)

```yaml
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

env:
  NODE_VERSION: '20'

jobs:
  quick-checks:
    name: Quick Checks
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Check formatting
        run: npm run format:check
        
      - name: Run linter
        run: npm run lint
        
      - name: Run type check
        run: npm run typecheck

  build:
    name: Build Project
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build project
        run: npm run build
        env:
          PUBLIC_SITE_URL: https://portfolio.tvoje.info
      
      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
          retention-days: 7

  accessibility:
    name: Accessibility Audit
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build project
        run: npm run build
        
      - name: Run accessibility audit
        uses: treosh/lighthouse-ci-action@v11
        with:
          urls: |
            https://portfolio.tvoje.info
            https://portfolio.tvoje.info/cs
          configPath: ./lighthouserc.json
          uploadArtifacts: true
          always-uploadArtifacts: true
```

### 2.2 Deployment Workflow (.github/workflows/deploy.yml)

**Note**: Vercel deployment has been replaced with SSH deployment to your Debian 13 VPS.

```yaml
name: Deploy to VPS

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  NODE_VERSION: '20'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build project
        run: npm run build
        env:
          PUBLIC_SITE_URL: https://portfolio.tvoje.info
        
      - name: Deploy to VPS via SSH
        uses: appleboy/scp-action@v0.1.7
        with:
          host: ${{ secrets.VPS_IP }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          source: "dist/"
          target: "/var/www/portfolio"
          
      - name: SSH - Restart Application
        uses: appleboy/ssh-action@v0.1.9
        with:
          host: ${{ secrets.VPS_IP }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /var/www/portfolio
            npm install --production
            pm2 restart ecosystem.config.js || npm start &
```

### 2.3 Security Workflow (.github/workflows/security.yml)

```yaml
name: Security Scanning

on:
  schedule:
    - cron: 'weekly'
  push:
    branches: [main]
    paths:
      - 'package.json'
      - 'package-lock.json'
  pull_request:
    branches: [main]

jobs:
  dependabot:
    name: Dependency Updates
    runs-on: ubuntu-latest
    steps:
      - name: Check for updates
        uses: dependabot/fetch-updates@v14
        with:
          directory: '/'
          package-ecosystem: 'npm'
          target-branch: 'main'
          commit-message: 'Bump npm dependencies'
          open-pull-requests-limit: 10
      
      - name: Create pull request for updates
        uses: peter-evans/create-pull-request@v7
        with:
          title: 'Bump npm dependencies'
          body: 'Automated dependency updates by GitHub Actions'
          branch: 'dependency-updates'
          delete-branch: true

  code-scanning:
    name: Code Scanning
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: javascript
          queries: security-extended
          
      - name: Build
        run: npm ci && npm run build
        
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: '/language:javascript'

  npm-audit:
    name: NPM Vulnerability Audit
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Run npm audit
        run: npm audit --production --audit-level=high
```

---

## 3. Environment Configuration

### 3.1 Required GitHub Secrets

Configure these in **GitHub Repository → Settings → Secrets and variables → Actions**:

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `VPS_IP` | IP address of your VPS | From your hosting provider |
| `VPS_USER` | SSH username (e.g., root, admin) | Your VPS SSH user |
| `VPS_SSH_KEY` | SSH private key | `ssh-keygen -t ed25519` on local machine |
| `GITHUB_TOKEN` | Automatic (GitHub provides) | No action needed |

**How to generate SSH key for VPS deployment:**

```bash
# On your local Windows machine
ssh-keygen -t ed25519 -C "github-actions@portfolio"

# Copy public key to VPS
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-vps-ip

# Add private key to GitHub Secrets (VPS_SSH_KEY)
cat ~/.ssh/id_ed25519
```

### 3.2 Environment Variables (.env)

```env
# Project Configuration
PROJECT_NAME=marketing-tvoje-info

# Site URL (required for SEO and canonical URLs)
PUBLIC_SITE_URL=https://portfolio.tvoje.info

# Formspree Configuration
# Get your form ID from https://formspree.io/
PUBLIC_FORMSPREE_ID=your_form_id

# Plausible Analytics
# Get your domain ID from https://plausible.io/
PUBLIC_PLAUSIBLE_DOMAIN=portfolio.tvoje.info
PUBLIC_PLAUSIBLE_API_HOST=https://plausible.io
```

---

## 4. Lighthouse CI Configuration (lighthouserc.json)

```json
{
  "ci": {
    "collect": {
      "numberOfRuns": 3,
      "settings": {
        "url": [
          "https://portfolio.tvoje.info",
          "https://portfolio.tvoje.info/cs"
        ]
      }
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.95 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["error", { "minScore": 0.95 }],
        "categories:seo": ["error", { "minScore": 0.95 }],
        "first-contentful-paint": ["warn", { "maxNumericValue": 2000 }],
        "largest-contentful-paint": ["warn", { "maxNumericValue": 2500 }],
        "interactive": ["warn", { "maxNumericValue": 3000 }]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

---

## 5. VPS Setup (Debian 13)

### 5.1 Server Prerequisites

```bash
# Connect to your VPS
ssh user@your-vps-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 process manager
sudo npm install -g pm2

# Install Nginx (optional, for reverse proxy)
sudo apt install nginx -y
```

### 5.2 Directory Setup

```bash
# Create deployment directory
sudo mkdir -p /var/www/portfolio
sudo chown -R $USER:$USER /var/www/portfolio
sudo chmod -R 755 /var/www/portfolio

# Create ecosystem.config.js for PM2
cat > /var/www/portfolio/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'portfolio',
    script: 'npm',
    args: 'start',
    cwd: '/var/www/portfolio',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'production',
      HOST: '0.0.0.0',
      PORT: 4321
    }
  }]
};
EOF

# Start PM2 and save configuration
cd /var/www/portfolio
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### 5.3 Nginx Configuration (Optional)

```bash
# Create nginx configuration
sudo cat > /etc/nginx/sites-available/portfolio << 'EOF'
server {
    server_name portfolio.tvoje.info www.portfolio.tvoje.info;
    
    location / {
        proxy_pass http://localhost:4321;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# Enable configuration
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5.4 SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d portfolio.tvoje.info -d www.portfolio.tvoje.info
```

---

## 6. Local Development (Windows)

### 6.1 Prerequisites

- **Node.js 20+**: https://nodejs.org/
- **Git**: https://git-scm.com/
- **VS Code**: Recommended IDE

### 6.2 Setup

```bash
# Clone repository
git clone https://github.com/pkoka888/marketing.tvoje.info.git
cd marketing.tvoje.info

# Install dependencies
npm install

# Start development server
npm run dev

# Site available at http://localhost:4321
```

### 6.3 Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |
| `npm run typecheck` | Run TypeScript checks |
| `npm run format` | Format code with Prettier |
| `npm run format:check` | Check code formatting |

---

## 7. Deployment Workflow

### 7.1 Automatic Deployment (GitHub Actions)

1. Push code to `main` branch
2. GitHub Actions runs:
   - CI checks (lint, typecheck, build)
   - Lighthouse accessibility audit
   - Security scans (CodeQL, npm audit)
3. If all checks pass:
   - SSH deploys `dist/` to VPS
   - PM2 restarts application
4. Site updates automatically

### 7.2 Manual Deployment (Backup)

```bash
# On your local machine
npm run build

# Copy to VPS
scp -r dist/* user@your-vps-ip:/var/www/portfolio

# SSH to VPS and restart
ssh user@your-vps-ip
cd /var/www/portfolio
npm install --production
pm2 restart all
```

---

## 8. Performance Targets

| Metric | Target | Tool |
|--------|--------|------|
| Lighthouse Performance | ≥95 | Lighthouse CI |
| Lighthouse Accessibility | ≥95 | Lighthouse CI |
| Lighthouse Best Practices | ≥95 | Lighthouse CI |
| Lighthouse SEO | ≥95 | Lighthouse CI |
| LCP | <2.5s | PageSpeed Insights |
| FID | <100ms | PageSpeed Insights |
| CLS | <0.1 | PageSpeed Insights |

---

## 9. Implementation Checklist

### Phase 1: Local Setup ✅
- [x] Repository cloned
- [x] Dependencies installed
- [x] Development server running
- [x] Code formatting configured

### Phase 2: GitHub Configuration ⏳
- [ ] Configure GitHub Secrets (VPS_IP, VPS_USER, VPS_SSH_KEY)
- [ ] Verify CI workflow runs successfully
- [ ] Verify deployment workflow works

### Phase 3: VPS Setup ⏳
- [ ] Prepare Debian 13 server
- [ ] Install Node.js and PM2
- [ ] Create deployment directory
- [ ] Configure PM2 ecosystem
- [ ] Set up Nginx (optional)
- [ ] Get SSL certificate (optional)

### Phase 4: Testing ⏳
- [ ] Test deployment workflow
- [ ] Verify site accessible at portfolio.tvoje.info
- [ ] Test contact form submission
- [ ] Verify Plausible analytics
- [ ] Run Lighthouse audit

---

## 10. Troubleshooting

### Build Fails

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

### PM2 Not Restarting

```bash
# Check PM2 logs
pm2 logs

# Check ecosystem configuration
pm2 ecosystem

# Restart manually
pm2 restart all
```

### SSH Connection Failed

```bash
# Verify SSH key is added to VPS
ssh user@your-vps-ip

# Check GitHub secret format
# VPS_SSH_KEY should be the FULL private key including -----BEGIN OPENSSH PRIVATE KEY-----
```

### Lighthouse Scores Low

```bash
# Run Lighthouse locally
npx lighthouse https://portfolio.tvoje.info --output json

# Check for suggestions in the report
```

---

## 11. References

| Resource | URL |
|----------|-----|
| Astro Documentation | https://docs.astro.build/ |
| Tailwind CSS | https://tailwindcss.com/docs |
| PM2 Documentation | https://pm2.keymetrics.io/docs/usage/quick-start/ |
| Nginx Documentation | https://nginx.org/en/docs/ |
| GitHub Actions | https://docs.github.com/en/actions |
| Lighthouse CI | https://github.com/marketplace/actions/lighthouse-ci-action |
| Formspree | https://formspree.io/docs |
| Plausible | https://plausible.io/docs |
| TypeScript | https://www.typescriptlang.org/docs |

---

**Document Version**: 1.0  
**Created**: 2026-02-11  
**Status**: Ready for Implementation  
**Deployment Target**: Debian 13 VPS

## Next Steps

1. ⏳ Configure GitHub Secrets for VPS deployment
2. ⏳ Prepare Debian 13 server
3. ⏳ Test deployment workflow
4. ⏳ Verify production deployment
5. ⏳ Monitor performance and security
