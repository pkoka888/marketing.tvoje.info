# Server Preservation Rule - Gemini

## Purpose

Prevent accidental or intentional cleanup/removal operations on production and development servers. This rule is specifically enforced by Gemini-powered agents.

## Rule Statement

When working with server infrastructure:

- **NEVER perform any cleanup operations** (delete, remove, prune, cleanup, purge commands)
- **ALWAYS perform analysis only** (inspect, gather evidence, read logs, check status, diff configurations)
- Document findings but do NOT modify server state

## Scope

This rule applies to:

- All servers (server60, server61, server62)
- All server access methods (SSH, Tailscale, direct access)
- All services and containers
- All configuration files
- All logs and evidence

## Allowed Operations (Analysis Only)

- `docker ps` / `docker ps -a` (list containers)
- `docker logs` (read logs - NO flags that modify state)
- `docker inspect` (read container metadata)
- `systemctl status` (read service status)
- `journalctl` (read logs)
- `cat`, `less`, `tail` (read files)
- `diff` (compare configurations)
- Any read-only investigation commands

## Prohibited Operations

- `docker rm`, `docker rmi`, `docker prune`
- `systemctl stop`, `systemctl disable`
- `rm`, `del`, `erase` commands on server files
- Any command with cleanup, remove, delete, purge intent

## Emergency Override

If cleanup is absolutely required (e.g., security incident):

1. Document the rationale in the commit/message
2. Get explicit user approval BEFORE execution
3. Document the change in `evidence/` folder
4. Update relevant documentation

## Gemini-Specific Notes

- This rule is checked by the AUDITOR agent (gemini/gemini-2-5-pro-exp-06-05)
- Cross-reference with `.agents/rules/server-preservation.md` for consistency
- Weekly consistency check runs via `.agent/workflows/weekly-consistency.py`

## Enforcement

Violations of this rule should be flagged immediately with warning about potential data loss.
