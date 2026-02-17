---
name: devops
description: Must read this skill when performing any server operations or analyzing infrastructure.
---

# DevOps & Server Operations Skill

Use this skill when interacting with the project's server infrastructure (`s60`, `s61`, `s62`).

## Core Principle: READ-ONLY BY DEFAULT

**Antigravity agents are strictly prohibited from modifying server state without explicit user approval.**

## Allowed Operations (Analysis Only)

- `docker ps`, `docker logs` (no state modification)
- `systemctl status`, `journalctl`
- `cat`, `less`, `tail` (read files)
- `df -h`, `free -h`, `top -b -n 1`
- `curl -I` (header checks)

## Prohibited Operations (Unless Explicitly Approved)

- `docker rm`, `docker stop`, `docker prune`
- `systemctl restart`, `systemctl stop`
- `rm`, `del` (file deletion)
- Editing config files directly on server
- `apt-get install`, `npm install -g`

## Approval Protocol

If a modification is required:

1.  **Analyze** the problem using read-only commands.
2.  **Plan** the exact command sequence.
3.  **Request Approval** from the user via `notify_user`.
4.  **Execute** only after approval.

## Infrastructure Context

- **s60**: Hub/Backup (2.5T, 94Gi RAM)
- **s61**: Production (237G, 23Gi RAM)
- **s62**: Marketing (93G, 3.8Gi RAM) - **Target for this project**

## References

- `.kilocode/rules/rules-sysadmin` (Canonical source)
- `.kilocode/rules/rules-server-monitor` (Detailed allowed commands)
