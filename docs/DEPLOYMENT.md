# Deployment Documentation (2026)

## Overview

- **Production URL**: `https://marketing.tvoje.info`
- **Primary Target**: VPS `s62` (Internal Marketing Server)
- **Gateway**: VPS `s60` (Public Jump Host)
- **CI/CD**: GitHub Actions (`.github/workflows/deploy.yml`)

## Infrastructure

The deployment uses a **Jump Host Strategy** to reach the internal server `s62` which is not directly exposed to the public internet on the SSH port used by CI/CD.

### Topology

```mermaid
graph LR
    GH[GitHub Actions] -->|SSH :2260| S60[s60 (89.203.173.196)]
    S60 -->|SCP/SSH :2262| S62[s62 (192.168.1.62)]
    S62 -->|Serve| WWW[Public Internet]
```

## Deployment Flow

1.  **Build**: `npm run build` runs on `ubuntu-latest` (GitHub runner).
2.  **Transfer 1**: Artifacts (`dist/`) are SCP'd to `s60:/tmp/portfolio-deploy`.
3.  **Transfer 2**: `s60` executes a script to SCP artifacts to `s62:/var/www/portfolio/`.
4.  **Verification**: SSH check runs `ls -la` on `s62` to confirm file update.

## Manual Deployment (Emergency)

If GitHub Actions is down, you can deploy manually from a local machine with SSH access to `s60`.

```bash
# 1. Build locally
npm run build

# 2. SCP to s60
scp -P 2260 -r dist/* sugent@89.203.173.196:/tmp/portfolio-deploy/

# 3. SSH to s60 and deploy to s62
ssh -p 2260 sugent@89.203.173.196
# (On s60)
scp -P 2262 -r /tmp/portfolio-deploy/* sugent@192.168.1.62:/var/www/portfolio/
```

## Troubleshooting

- **Permission Denied**: Check `sugent` user permissions on `/var/www/portfolio` on `s62`.
- **Timeout**: Large asset files might time out during SCP. Check network speed.
- **Vercel Conflict**: Vercel deployment is **DISABLED** for production. Do not re-enable in `bmad.yml`.
