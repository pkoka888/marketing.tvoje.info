---
description: Server preservation — no cleanup/delete operations on servers without explicit approval
---

# Server Preservation Rule

## Mandate

When working with server infrastructure:

- NEVER perform cleanup operations (delete, remove, prune, cleanup, purge)
- ALWAYS perform analysis only (inspect, gather evidence, read logs, check status, diff)
- Document findings but do NOT modify server state

## Scope

Applies to: server60, server61, server62 (all access methods)

## Allowed Operations

- `docker ps`, `docker logs`, `docker inspect`
- `systemctl status`, `journalctl`
- `cat`, `less`, `tail`, `diff`
- Any read-only investigation command

## Prohibited Operations

- `docker rm`, `docker rmi`, `docker prune`
- `systemctl stop`, `systemctl disable`
- `rm`, `del`, `erase` on server files

## Emergency Override

1. Document rationale
2. Get explicit user approval BEFORE execution
3. Document in `evidence/` folder

## Canonical Version

`.kilocode/rules/server-preservation`
