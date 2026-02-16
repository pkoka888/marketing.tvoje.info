# MCP Server Consolidation & Alignment Plan

**Status:** Plan (Ready for Implementation)
**Created:** 2026-02-13
**Goal:** Fix Redis/Playwright MCP restarts and align configs across all agents

---

## Current Issues Analysis

### 1. Redis MCP Failure (Critical)

**Error:** `ERR_MODULE_NOT_FOUND: Cannot find module '@modelcontextprotocol/sdk/dist/esm/types'`

**Root Cause:** The custom `redis-server.js` uses ESM imports (`@modelcontextprotocol/sdk`) but the SDK's export structure has changed. The MCP SDK v1.x uses different import paths.

**Solution:** Replace custom Redis MCP with official npx version OR fix import paths.

### 2. Playwright MCP Issues

**Error:** `Failed to get Chrome DevTools MCP URL: command 'antigravity.getChromeDevtoolsMcpUrl' not found`

**Root Cause:** This is an Antigravity-specific issue. The Chrome DevTools MCP integration requires a specific extension command that isn't available.

**Solution:** Remove Playwright MCP from Antigravity config or use native Playwright testing instead.

### 3. Port Configuration

- Redis: Moved to **36379** (non-standard)
- LiteLLM: **4000** (standard)
- Astro: **4321** (standard)

---

## Agent Configuration Comparison

| Agent           | Config Location      | MCP Config Format  | Status              |
| --------------- | -------------------- | ------------------ | ------------------- |
| **Kilo Code**   | `.kilocode/mcp.json` | JSON with env vars | ⚠️ Has custom Redis |
| **Cline**       | `.clinerules/`       | Rules files        | ✅ Rules aligned    |
| **OpenCode**    | `opencode.json`      | JSON               | ✅ Updated          |
| **Antigravity** | VSCode settings      | JSON               | ❌ Duplicate issues |

---

## Implementation Tasks

### Task 1: Fix Redis MCP (Priority: Critical)

**Option A: Use Official npx Redis MCP**

```json
{
  "redis": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-redis",
      "--url",
      "redis://host.docker.internal:36379"
    ]
  }
}
```

**Option B: Fix Custom Server Import**
Update `redis-server.js` to use CommonJS or fix ESM paths.

### Task 2: Remove Duplicate Playwright MCP (Priority: High)

Remove duplicate `playwright-mcp` entry from `.kilocode/mcp.json`.

### Task 3: Create Unified MCP Config (Priority: High)

Create a single source of truth for MCP servers that all agents reference:

**`mcp-config.json` (root of project):**

```json
{
  "servers": {
    "redis": { "port": 36379, "url": "redis://host.docker.internal:36379" },
    "filesystem": { "paths": ["C:/Users/pavel/projects"] },
    "github": { "auth": "token" }
  },
  "rules": {
    "no_port_changes": true,
    "require_approval_for_changes": true
  }
}
```

### Task 4: Update Agent Rules (Priority: Medium)

Add to all agent rule directories:

- `.clinerules/mcp-alignment.md`
- `.agents/rules/mcp-alignment.md`
- `.kilocode/rules/mcp-alignment.md`

---

## MCP Port Registry

| Service   | Port  | Range                 | Config File                  |
| --------- | ----- | --------------------- | ---------------------------- |
| Redis     | 36379 | Non-standard (30000+) | `.env`, `.kilocode/mcp.json` |
| LiteLLM   | 4000  | Standard              | External                     |
| Astro Dev | 4321  | Standard              | `package.json`               |

---

## Enforcement Strategy

### 1. Single Source of Truth

All MCP configs should reference a common definition file.

### 2. Port Preservation Rule

Created: `.clinerules/mcp-port-preservation.md`
Status: ✅ Active

### 3. Config Validation Script

Create a validation script that checks:

- No duplicate server names
- Ports in allowed range
- All required env vars defined

---

## Files to Update

| File                             | Action                                     |
| -------------------------------- | ------------------------------------------ |
| `.kilocode/mcp.json`             | Fix Redis MCP, remove duplicate playwright |
| `.env`                           | Already updated with port 36379            |
| `opencode.json`                  | Already updated with port rules            |
| `.clinerules/mcp-alignment.md`   | Create new rule                            |
| `.agents/rules/mcp-alignment.md` | Create new rule                            |

---

## Next Steps

1. **Fix Redis MCP** - Replace with official npx version or fix import
2. **Remove duplicates** - Clean up .kilocode/mcp.json
3. **Create alignment rules** - Add to all agent directories
4. **Test** - Verify no more restarts
5. **Document** - Update AGENTS.md with findings
