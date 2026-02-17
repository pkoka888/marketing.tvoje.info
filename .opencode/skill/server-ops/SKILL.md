---
name: server-ops
description: Use when performing any server operations on s60/s61/s62 — enforces read-only analysis and server preservation rules
---

## Use This When

- Checking server status on s60 (Infrastructure), s61 (Gateway/Traefik), s62 (Production)
- Collecting evidence or logs via SSH
- Troubleshooting deployment or container issues

## Server Access Pattern

Access via Tailscale jumphost:
```bash
ssh -J sugent@s60 sugent@s62   # Access s62 via s60 jumphost
ssh sugent@s60                  # Direct s60 access (Tailscale needs sudo)
```

## MANDATORY: Server Preservation Rule

Read `.kilocode/rules/rules-sysadmin` before ANY server operation.

**NEVER perform:**
- `docker rm`, `docker rmi`, `docker prune`
- `systemctl stop`, `systemctl disable`
- `rm`, `del`, `erase` on server files

**ALWAYS allowed:**
- `docker ps`, `docker logs`, `docker inspect`
- `systemctl status`, `journalctl`
- `cat`, `less`, `tail`, `diff`

## Emergency Override

1. Document rationale
2. Get explicit user approval BEFORE execution
3. Document in `evidence/` folder

## Servers

| Server | Role | Access |
|--------|------|--------|
| s60 | Infrastructure/VPS + jumphost | Direct Tailscale |
| s61 | Gateway + Traefik reverse proxy | Via s60 |
| s62 | Production/Web (marketing site) | Via s60 |
