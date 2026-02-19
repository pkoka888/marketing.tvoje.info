---
name: devops
description:
  Must read this skill when performing any server operations or analyzing
  infrastructure.
---

# DevOps & Server Operations Skill

Use this skill when interacting with the project's server infrastructure (`s60`,
`s61`, `s62`).

## Core Principle: READ-ONLY BY DEFAULT

**Antigravity agents are strictly prohibited from modifying server state without
explicit user approval.**

## Server Inventory

| Server  | IP           | Purpose         | Resources                 | Domains              |
| ------- | ------------ | --------------- | ------------------------- | -------------------- |
| **s60** | 192.168.1.60 | Hub/Backup      | 2.5T, 94Gi RAM            | \*.expc.cz           |
| **s61** | 192.168.1.61 | Gateway/Traefik | 237G, 23Gi RAM ⚠️88% disk | okamih.cz, okamih.sk |
| **s62** | 192.168.1.62 | Production/Web  | 93G, 3.8Gi RAM            | marketing.tvoje.info |

## SSH Access

| Method            | Config           | Status         |
| ----------------- | ---------------- | -------------- |
| Tailscale VPN     | Port 20          | ✅ Primary     |
| Internal (s60)    | Port 2260        | ✅ Working     |
| Internal (s61)    | Port 2261        | ✅ Working     |
| Internal (s62)    | Port 2262        | 🔴 UNREACHABLE |
| ProxyJump s60→s62 | Via s60 internal | ⚠️ Untested    |

```bash
# SSH Aliases (from ~/.ssh/config)
# s60pa → admin@192.168.1.60 -p 20
# s61pa → admin@192.168.1.61 -p 20
# s62pa → admin@192.168.1.62 -p 20 (or ProxyJump via s60pa)
```

## Known Issues

| Issue                                                         | Severity    | Status                                   |
| ------------------------------------------------------------- | ----------- | ---------------------------------------- |
| s62 Port 2262 unreachable                                     | 🔴 CRITICAL | Open — blocks all s62 operations         |
| s61 Disk at 88%                                               | ⚠️ WARNING  | Document only — DO NOT remediate         |
| s61 Failed monitoring containers (Prometheus, Grafana, Redis) | ⚠️ WARNING  | Do not restart — disk space needed first |

## Allowed Operations (Analysis Only)

- `docker ps`, `docker logs`, `docker inspect` (no state modification)
- `systemctl status`, `journalctl`
- `cat`, `less`, `tail`, `head` (read files)
- `df -h`, `free -h`, `top -b -n 1`
- `curl -I` (header checks)
- `ss -tlnp`, `netstat -tlnp` (network status)

## Prohibited Operations (Unless Explicitly Approved)

- `docker rm`, `docker stop`, `docker prune`
- `systemctl restart`, `systemctl stop`
- `rm`, `del` (file deletion)
- Editing config files directly on server
- `apt-get install`, `npm install -g`

## Approval Protocol

If a modification is required:

1. **Analyze** the problem using read-only commands.
2. **Plan** the exact command sequence.
3. **Request Approval** from the user via `notify_user`.
4. **Execute** only after approval.
5. **Document** all changes in evidence directory.

## LangGraph Flows

| Flow                | File                             | Purpose                                |
| ------------------- | -------------------------------- | -------------------------------------- |
| Evidence Collection | `.agent/flows/server_ops.py`     | Parallel SSH evidence from all servers |
| Safe Deploy         | `.agent/flows/server_ops.py`     | Build → lint → SCP → PM2 restart       |
| Health Monitor      | `.agent/flows/health_monitor.py` | Adaptive uptime & deduction            |

## Kilo Code Integration

| Resource             | Location                                           |
| -------------------- | -------------------------------------------------- |
| Rules (canonical)    | `.kilocode/rules/rules-sysadmin`                   |
| Server Monitor rules | `.kilocode/rules/rules-server-monitor` (539 lines) |
| Preservation rules   | `.kilocode/rules/server-preservation`              |
| Debug workflow       | `.kilocode/workflows/debug-server.md` (590 lines)  |
| Mode (Kilo UI)       | `.kilocodemodes` → `server-monitor`, `sysadmin`    |

## References

- `.kilocode/rules/rules-sysadmin` (Canonical source)
- `.kilocode/rules/rules-server-monitor` (Detailed allowed commands)
- `.kilocode/workflows/debug-server.md` (Full debug workflow)
- `plans/server-vps-deployment/servers-structure.md` (Infrastructure manual)
