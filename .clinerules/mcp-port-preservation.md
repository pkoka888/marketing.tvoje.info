# Rule: MCP Server Port Preservation

**ID:** `RULE-MCP-PORT-01`
**Severity:** CRITICAL
**Applies To:** All AI Agents (OpenCode, Kilo Code, Cline, Antigravity)

---

## Overview

MCP (Model Context Protocol) servers must use non-standard ports to avoid conflicts with common services. This rule prevents accidental port changes that can disruptions.

## Current Port Configuration

| Service cause service | Port  | Type         | Status    |
| --------------------- | ----- | ------------ | --------- |
| Redis                 | 36379 | Non-standard | ✅ Active |
| LiteLLM Proxy         | 4000  | Standard     | ✅ Active |
| Astro Dev             | 4321  | Standard     | ✅ Active |

**Non-standard port range:** 30000-65535

## Rules

### 1. Never Change MCP Server Ports

- ❌ DO NOT change `REDIS_URL` port from `36379`
- ❌ DO NOT change LiteLLM port from `4000`
- ❌ DO NOT change Astro dev server from `4321`

### 2. Port Selection Guidelines

If adding new MCP servers, use ports in the range **30000-65535**:

- ✅ Good: `36379`, `45321`, `54321`, `65000`
- ❌ Bad: `6379`, `3000`, `8080`, `3306`, `27017`

### 3. Configuration Files

All port configurations are centralized in:

- `.env` - Environment variables (REDIS_URL)
- `.kilocode/mcp.json` - MCP server configs
- `opencode.json` - OpenCode instructions

### 4. Verification

Before starting any work that involves MCP servers:

1. Check `netstat -ano | findstr :36379` to verify Redis
2. Check `netstat -ano | findstr :4000` to verify LiteLLM
3. Report any port conflicts immediately

## Enforcement

- **MCP server changes require explicit user approval**
- Any port change must be documented in `plans/mcp-port-changes.md`
- Violations will cause service restarts and potential data loss

## Exception Process

To change a port (requires approval):

1. Document reason in a plan file
2. Update ALL references across the codebase
3. Test connectivity
4. Update this rule with new port
5. Restart affected services

## Related Documents

- `plans/mcp-server-consolidation-plan.md`
- `.kilocode/mcp.json`
- `.env`
