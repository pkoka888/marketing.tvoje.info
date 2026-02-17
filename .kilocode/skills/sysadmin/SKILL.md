# SysAdmin Skills

System administration and server management capabilities with read-only and command execution support. Provides comprehensive server monitoring, analysis, and management capabilities while following strict server preservation rules.

## Server Preservation Rule

When working with server infrastructure:

- **NEVER perform cleanup operations** (delete, remove, prune, purge commands)
- **ALWAYS perform analysis only** unless explicitly approved
- Document findings but do NOT modify server state

## Allowed Operations

- `docker ps` / `docker ps -a` (list containers)
- `docker logs` (read logs)
- `docker inspect` (read container metadata)
- `systemctl status` (read service status)
- `journalctl` (read logs)
- `cat`, `less`, `tail` (read files)
- `diff` (compare configurations)

## Prohibited Operations

- `docker rm`, `docker rmi`, `docker prune`
- `systemctl stop`, `systemctl disable`
- `rm`, `del`, `erase` commands on server files

## Server Inventory

| Server   | Hostname | IP           | Purpose            |
| -------- | -------- | ------------ | ------------------ |
| Server60 | server60 | 192.168.1.60 | Infrastructure/VPS |
| Server61 | server61 | 192.168.1.61 | Gateway/Traefik    |
| Server62 | server62 | 192.168.1.62 | Production/Web     |
