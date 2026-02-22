# FINAL CONSOLIDATED PLAN - Memory & MCP Unification

**Generated**: 2026-02-22 **Based on**: All previous plans
(memory-mcp-unification-plan.md, memory-mcp-unification-plan-v2.md,
UPDATED-PARALLEL-PLAN-2026-02-21.md)

---

## PART A: COMPLETED ✅

| Task                 | Status | Notes                           |
| -------------------- | ------ | ------------------------------- |
| Junctions created    | ✅     | .kilocode → .agent working      |
| MCP discovery script | ✅     | scripts/discover_mcp_configs.py |
| Memory research      | ✅     | UNIFIED-MEMORY-ARCHITECTURE.md  |
| Config report        | ✅     | report-mcp-configs-20260222.md  |

---

## PART B: NEW ACTION ITEMS

### TASK 1: KILOCODE - Disable Memory MCP

**Priority**: HIGH | **Agent**: @coder

```bash
# Edit .kilocode/mcp.json - REMOVE memory server:
{
  "mcpServers": {
    // REMOVE THIS:
    "memory": {
      "command": "node",
      "args": ["C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-memory/dist/index.js"]
    }
    // KEEP ALL OTHERS
  }
}
```

**Why**: Saves ~200K tokens, junctions already give file access

---

### TASK 2: CLINE - Add Missing Servers

**Priority**: HIGH | **Agent**: @coder

Add to `.clinerules/mcp.json`:

```json
{
  "time": {
    "command": "uvx",
    "args": ["mcp-server-time"]
  },
  "bmad-mcp": {
    "command": "node",
    "args": ["C:/nvm4w/nodejs/node_modules/bmad-mcp/dist/index.js"],
    "env": { "PROJECT_ROOT": "." }
  }
}
```

---

### TASK 3: ANTIGRAVITY - Document as Single Source

**Priority**: MEDIUM | **Agent**: @coder

Create `.antigravity/README.md`:

```markdown
# Antigravity MCP Configuration

This is the SINGLE SOURCE OF TRUTH for MCP configurations.

## Servers (12)

- filesystem-projects, filesystem-agentic, filesystem-vscodeportable
- memory, git, github, time, fetch, redis
- bmad-mcp, firecrawl-local, playwright-mcp

## Alignment

All other agent configs (.kilocode, .clinerules) should reference or copy from
this file.
```

---

### TASK 4: OPENCODE - Optional Minimal MCP

**Priority**: LOW | **Agent**: @coder (if requested)

Current config (no MCP) is OPTIMAL for context:

- ~50-70KB context from instructions
- No Memory MCP overhead
- Direct filesystem access

Add ONLY if Redis rate limiting needed:

```json
"redis": {
  "type": "local",
  "command": ["node", "./.kilocode/mcp-servers/mcp-wrapper.js", "redis"]
}
```

---

### TASK 5: MEMORY ARCHITECTURE - Implement Surgical Loading

**Priority**: MEDIUM | **Agent**: @architect

Current structure:

```
.agent/memory/canonical/    (8 files - OK)
.agent/memory/contexts/      (3 files - OK)
.agent/memory/sessions/      (cross-session)
```

**Implementation**:

1. Keep `.agent/memory/canonical/` as single source (~300 lines)
2. Create tiered loading:
   - MINIMAL: brief.md + context.md (~5KB)
   - STANDARD: + product.md + tech.md (~15KB)
   - FULL: + all canonical + sessions (~50KB)

---

### TASK 6: PUSH TO REMOTE

**Priority**: HIGH | **Agent**: @codex

After tasks 1-5:

```bash
git add .
git commit -m "fix: disable memory MCP in kilocode, add missing servers to cline"
git push origin develop
```

---

## SUMMARY

| Task | Agent      | Priority | Action                          |
| ---- | ---------- | -------- | ------------------------------- |
| 1    | @coder     | HIGH     | Disable memory MCP in .kilocode |
| 2    | @coder     | HIGH     | Add time/bmad-mcp to cline      |
| 3    | @coder     | MEDIUM   | Document antigravity as source  |
| 4    | @coder     | LOW      | OpenCode stays as-is            |
| 5    | @architect | MEDIUM   | Implement surgical loading      |
| 6    | @codex     | HIGH     | Push to remote                  |

---

## ROLLBACK

If issues:

```bash
git revert HEAD  # Undo all changes
```

---

**Plan Version**: 2.0 **Status**: Ready for execution **Confirm**: Reply "yes
execute" to proceed
