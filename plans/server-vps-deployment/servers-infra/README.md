# Universal Server Infrastructure Package

**Version:** 1.0 **Created:** 2026-02-19 **Purpose:** Project-agnostic
deployment & management toolkit for AI agent sysadmins.

## Quick Start (for Orchestrator Agents)

```bash
# 1. Read servers.yml to understand the infrastructure
# 2. Read agent-sysadmin.md for safety rules
# 3. Run pre-flight checks before ANY change:
ansible-playbook -i inventory.yml playbooks/preflight-check.yml -e "target_server=s62"

# 4. Deploy a static site:
ansible-playbook -i inventory.yml playbooks/deploy-static.yml \
  -e "target_server=s62 project_name=myproject deploy_path=/var/www/projects/myproject dist_dir=./dist"

# 5. Verify health after deployment:
ansible-playbook -i inventory.yml playbooks/health-check.yml
```

## Server Overview

```
┌─────────────────────────────────────────────────────────┐
│                    FIREWALL / NAT                       │
│  Public IP: 89.203.173.196                              │
│  Port Forwarding: 2260→s60, 2261→s61, 2262→s62(!)     │
└────────┬──────────────┬──────────────┬──────────────────┘
         │              │              │
   ┌─────▼─────┐  ┌────▼─────┐  ┌────▼─────┐
   │  s60      │  │  s61     │  │  s62     │
   │ Hub/Backup│  │ GATEWAY  │  │ Web/Prod │
   │           │  │ ⚠CRITICAL│  │          │
   │ *.expc.cz │  │ Traefik  │  │*.tvoje.  │
   │ subdomains│  │ 80/443   │  │  info    │
   │ rsnapshot │  │ okamih.cz│  │          │
   │ ansible   │  │ okamih.sk│  │ Astro    │
   │ borgmatic │  │ PrestaShop│ │ PM2/Node │
   │           │  │ MariaDB  │  │ Nginx    │
   │ Jump host │  │ Redis    │  │ Docker   │
   │ for CI/CD │  │ Docker   │  │          │
   └───────────┘  └──────────┘  └──────────┘
   192.168.1.60   192.168.1.61  192.168.1.62
   SSH: 2260/20   SSH: 2261/20  SSH: 2262/20
```

## Safety Rules (Summary)

| Rule       | Description                                                |
| ---------- | ---------------------------------------------------------- |
| **Never**  | Restart Traefik/Docker/Nginx on s61 without human approval |
| **Never**  | Delete files outside your project's deploy path            |
| **Never**  | Change firewall rules without explicit permission          |
| **Always** | Run `preflight-check.yml` before any deployment            |
| **Always** | Run `health-check.yml` after any deployment                |
| **Always** | Check port conflicts before exposing new ports             |
| **Always** | Verify okamih.cz/sk accessibility after any s61 change     |

## Known Issues

See [known-issues.md](known-issues.md) for current infrastructure issues.

## Files

| File                | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| `servers.yml`       | Master server registry (single source of truth)  |
| `inventory.yml`     | Ansible inventory                                |
| `agent-sysadmin.md` | Agent role definition & safety rules             |
| `known-issues.md`   | Current infrastructure issues                    |
| `playbooks/`        | Ansible playbooks for deployment & checks        |
| `scripts/`          | Python utilities (safe SSH, preflight, evidence) |
| `templates/`        | Jinja2 templates for Nginx, PM2, GitHub Actions  |

## Service Restart Protocol

**IMPORTANT:** After ANY service change (config, deployment, package), agents
MUST follow the restart protocol.

### Using `restart_all_services.py`

```bash
# Restart nginx and PM2 on production server (s62)
python scripts/restart_all_services.py --servers s62 --services nginx,pm2

# Restart all services (s60, s62) - excludes critical s61
python scripts/restart_all_services.py --all

# Check-only mode (shows what would happen)
python scripts/restart_all_services.py --servers s62 --services nginx --check-only
```

### Protocol Steps

1. **Restart** - Script restarts specified services
2. **Wait 30s** - Automatic stabilization wait
3. **Analyze logs** - Script checks for errors in nginx, PM2, Docker logs
4. **Verify health** - Health checks confirm services are running
5. **Document errors** - All issues reported and escalated

### Approval Requirements

| Server | Services Requiring Approval |
| ------ | --------------------------- |
| s60    | nginx, docker               |
| s61    | ALL (critical server)       |
| s62    | nginx, docker               |

**s61 (Gateway/Traefik) requires human approval for ANY service restart.**

### Protected Containers

The following containers are protected and should NEVER be restarted without
explicit approval:

- `traefik`, `netbox`, `netbox-redis`, `netbox-postgres`, `homarr-dashboard`

See `agent-sysadmin.md` for full protocol details.
