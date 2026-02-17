# Rule: MCP Configuration Alignment

**ID:** `RULE-MCP-ALIGN-01`
**Severity:** CRITICAL
**Applies To:** All AI Agents (Kilo Code, Cline, OpenCode, Antigravity)

---

## Overview

All AI agents must use consistent MCP server configurations. This rule ensures that MCP servers are configured identically across all agent frameworks to prevent conflicts, restarts, and errors.

## Unified MCP Configuration

All agents must reference the same MCP servers. The authoritative config is:

**Primary:** `.kilocode/mcp.json`

### Current Validated Servers

| Server Name         | Type | Port  | Config Location    |
| ------------------- | ---- | ----- | ------------------ |
| redis               | npx  | 36379 | .kilocode/mcp.json |
| filesystem-projects | npx  | N/A   | .kilocode/mcp.json |
| filesystem-agentic  | npx  | N/A   | .kilocode/mcp.json |
| memory              | npx  | N/A   | .kilocode/mcp.json |
| git                 | npx  | N/A   | .kilocode/mcp.json |
| github              | npx  | N/A   | .kilocode/mcp.json |
| time                | uvx  | N/A   | .kilocode/mcp.json |
| fetch               | uvx  | N/A   | .kilocode/mcp.json |
| bmad-mcp            | npx  | N/A   | .kilocode/mcp.json |
| playwright-mcp      | npx  | N/A   | .kilocode/mcp.json |
| firecrawl-mcp       | npx  | N/A   | .kilocode/mcp.json |

## Port Rules

### Non-Standard Ports (Required)

- Redis: **36379** (never change!)
- Range: 30000-65535

### Standard Ports (Documented)

- LiteLLM: 4000
- Astro Dev: 4321

## Configuration Constraints

### DO:

- ✅ Use `.kilocode/mcp.json` as the source of truth
- ✅ Keep port 36379 for Redis
- ✅ Run `node -e "JSON.parse(require('fs').readFileSync('.kilocode/mcp.json'))"` to validate

### DO NOT:

- ❌ Add duplicate MCP server entries
- ❌ Change Redis port from 36379
- ❌ Create separate MCP configs for different agents
- ❌ Use custom MCP servers without testing

## Agent-Specific Notes

### Kilo Code

- Config: `.kilocode/mcp.json`
- Already aligned

### Cline

- Uses rules in `.clinerules/`
- Reference: `.clinerules/mcp-port-preservation.md`

### OpenCode

- Config: `opencode.json`
- Should reference rules, not duplicate MCP config

### Antigravity

- VSCode settings-based
- Should use same `.kilocode/mcp.json` if possible

## Validation

Before any work involving MCP servers:

```bash
# Validate JSON
node -e "JSON.parse(require('fs').readFileSync('.kilocode/mcp.json'))"

# Check for duplicates
grep -c "playwright" .kilocode/mcp.json
```

## Related Documents

- `.kilocode/mcp.json` (Authoritative)
- `.clinerules/mcp-port-preservation.md`
- `plans/mcp-fix-and-alignment-plan.md`
