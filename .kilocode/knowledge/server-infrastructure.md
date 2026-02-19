# Server Infrastructure Knowledge

**Last Updated**: 2026-02-19

## Server Inventory

| Server | IP           | Purpose         | SSH Port                        | Status             |
| ------ | ------------ | --------------- | ------------------------------- | ------------------ |
| s60    | 192.168.1.60 | Hub/Backup      | 2260 (internal), 20 (Tailscale) | ✅                 |
| s61    | 192.168.1.61 | Gateway/Traefik | 2261 (internal), 20 (Tailscale) | ⚠️ 88% disk        |
| s62    | 192.168.1.62 | Production/Web  | 2262 (internal), 20 (Tailscale) | 🔴 SSH unreachable |

## Deployment Target

- **Server**: s62
- **Path**: `/var/www/portfolio/`
- **Process Manager**: PM2 (`portfolio` process)
- **Web Server**: Nginx (reverse proxy to PM2 on port 4321)
- **SSL**: Let's Encrypt via Traefik (s61)
- **CI/CD**: GitHub Actions → SSH → build → PM2 restart

## Known Issues

1. **s62 SSH port 2262 unreachable** — CRITICAL, blocks all agent operations
2. **s61 disk at 88%** — WARNING, DO NOT attempt remediation
3. **s61 failed containers** (Prometheus, Grafana, Redis dash) — WARNING, requires disk fix first

## Port Registry

| Port   | Service    | Server |
| ------ | ---------- | ------ |
| 4321   | Astro/PM2  | s62    |
| 80/443 | Nginx      | s62    |
| 443    | Traefik    | s61    |
| 3306   | MariaDB    | s61    |
| 5432   | PostgreSQL | s61    |
| 6379   | Redis      | s61    |
| 19999  | Netdata    | s61    |

## Agent Tooling

| Tool                    | Location                              | Purpose               |
| ----------------------- | ------------------------------------- | --------------------- |
| LangGraph evidence flow | `.agent/flows/server_ops.py`          | Parallel SSH evidence |
| LangGraph deploy flow   | `.agent/flows/server_ops.py`          | Safe build→deploy     |
| Health monitor          | `.agent/flows/health_monitor.py`      | Adaptive uptime       |
| Safe deploy script      | `.agent/flows/safe-deploy.py`         | SCP + PM2 restart     |
| Debug workflow          | `.kilocode/workflows/debug-server.md` | Full debug protocol   |
