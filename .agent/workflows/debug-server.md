# Debug Server Workflow

**Purpose**: Server issue specific debugging workflow
**Mode**: Debug

---

## Overview

This workflow provides a specialized approach to debugging server and infrastructure issues on s60/s61/s62. All analysis is read-only per the server preservation rule.

## Server Infrastructure

| Server | Role | Access |
|--------|------|--------|
| s60 | Infrastructure/VPS + jumphost | Direct Tailscale |
| s61 | Gateway/Traefik | Via s60 |
| s62 | Production/Web | Via s60 |

Access: `ssh -J sugent@s60 sugent@s62`

## MANDATORY: Server Preservation Rule

Read `.kilocode/rules/rules-sysadmin` before ANY operation.

**Never perform**: `docker rm/rmi/prune`, `systemctl stop/disable`, `rm/del/erase`
**Always allowed**: `docker ps/logs/inspect`, `systemctl status`, `journalctl`, `cat/tail/diff`

## Step-by-Step Workflow

### Step 1: Issue Detection
1. Identify affected server
2. Create evidence directory: `mkdir -p evidence/{timestamp}/server-{id}`
3. Document symptoms

### Step 2: Parallel Analysis
Execute Server Analyzer and Log Analyzer in parallel:
- **Server Analyzer**: health, resources, containers, network (read-only)
- **Log Analyzer**: system logs, service logs, auth logs

### Step 3: Evidence Collection
```bash
docker ps -a > evidence/{timestamp}/server-{id}/docker-ps.txt
df -h > evidence/{timestamp}/server-{id}/disk-usage.txt
free -m > evidence/{timestamp}/server-{id}/memory-usage.txt
journalctl -p err -n 100 > evidence/{timestamp}/server-{id}/system-errors.log
```

### Step 4: Configuration Check (if confidence < 0.85)
Run Configuration Validator:
1. Check service config files
2. Verify environment variables

### Step 5: Report and Request Approval
Document findings + proposed fix. Get explicit user approval before any remediation.

## Confidence Threshold: 0.85

Server issues have production impact — higher threshold required.

## Related Files

- **General Debug**: `.agent/workflows/debug-issue.md`
- **Build Debug**: `.agent/workflows/debug-build.md`
- **Orchestrator Template**: `.agent/workflows/orchestrator-debug.md`
- **Server Rules**: `.kilocode/rules/rules-sysadmin`
