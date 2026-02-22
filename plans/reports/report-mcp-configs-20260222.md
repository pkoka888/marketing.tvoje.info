# MCP CONFIGURATION DISCOVERY REPORT

**Generated**: 2026-02-22 02:15 **Discovery Script**:
scripts/discover_mcp_configs.py

---

## EXECUTIVE SUMMARY

| Metric                       | Value                                                           |
| ---------------------------- | --------------------------------------------------------------- |
| Total MCP config files found | 37                                                              |
| Unique MCP servers           | 17                                                              |
| Main agent configs           | 5 (.agent, .antigravity, .kilocode, .clinerules, opencode.json) |
| Duplicate server entries     | 14 servers duplicated 3-6x                                      |

---

## CONFIG FILES DISCOVERY

### Primary MCP Configs (5 files)

| Agent           | File                    | Servers                 | Status                    |
| --------------- | ----------------------- | ----------------------- | ------------------------- |
| **ANTIGRAVITY** | `.antigravity/mcp.json` | 12                      | ✅ Complete               |
| .agent          | `.agent/mcp.json`       | 12                      | ✅ Complete               |
| KILOCODE        | `.kilocode/mcp.json`    | 12                      | ⚠️ Has Memory MCP         |
| CLINE           | `.clinerules/mcp.json`  | 10                      | ⚠️ Missing time, bmad-mcp |
| OPENCODE        | `opencode.json`         | 0 (MCP REMOVED BY USER) | ⚠️ No MCP                 |

### Server Availability Matrix

| Server                    | ANTIGRAVITY | .AGENT | KILOCODE   | CLINE | OPENCODE |
| ------------------------- | ----------- | ------ | ---------- | ----- | -------- |
| bmad-mcp                  | ✅          | ✅     | ✅         | ❌    | ❌       |
| fetch                     | ✅          | ✅     | ✅         | ✅    | ❌       |
| filesystem-agentic        | ✅          | ✅     | ✅         | ✅    | ❌       |
| filesystem-projects       | ✅          | ✅     | ✅         | ✅    | ❌       |
| filesystem-vscodeportable | ✅          | ✅     | ✅         | ✅    | ❌       |
| firecrawl-local           | ✅          | ✅     | ✅         | ✅    | ❌       |
| git                       | ✅          | ✅     | ✅         | ✅    | ❌       |
| github                    | ✅          | ✅     | ✅         | ✅    | ❌       |
| **memory**                | ✅          | ✅     | ✅ (ISSUE) | ✅    | ❌       |
| playwright-mcp            | ✅          | ✅     | ✅         | ✅    | ❌       |
| redis                     | ✅          | ✅     | ✅         | ✅    | ❌       |
| time                      | ✅          | ❌     | ✅         | ❌    | ❌       |

---

## ISSUES IDENTIFIED

### 1. DUPLICATIONS (14 servers x 3-6 locations)

Every main server is duplicated across 3-6 config files:

- filesystem-projects: 5 locations
- memory: 6 locations
- github: 6 locations
- redis: 5 locations

### 2. INCONSISTENCIES

| Issue         | Detail                                |
| ------------- | ------------------------------------- |
| CLINE missing | `time`, `bmad-mcp`                    |
| KILOCODE      | Has Memory MCP causing context issues |
| OPENCODE      | User removed ALL MCP - no servers     |

### 3. MEMORY MCP ISSUE (PRIMARY)

| Agent    | Memory MCP | Context Impact  |
| -------- | ---------- | --------------- |
| KILOCODE | ✅ ENABLED | +200K tokens ❌ |
| CLINE    | ✅ ENABLED | ~70KB total     |
| OPENCODE | ❌ REMOVED | 0 tokens ✅     |

---

## RECOMMENDATIONS

### A. SINGLE SOURCE OF TRUTH: .antigravity

Make `.antigravity/mcp.json` the canonical source and align all others:

```
.antigravity/mcp.json (12 servers)
    ↓ COPY/REFERENCE
.agent/mcp.json      → remove, use reference
.kilocode/mcp.json  → remove memory MCP, use reference
.clinerules/mcp.json → add missing time, bmad-mcp
opencode.json       → OPTIONAL: add minimal MCP if needed
```

### B. MEMORY MCP CONFIGURATION

Based on previous research (UNIFIED-MEMORY-ARCHITECTURE.md):

**Option 1: Disable (RECOMMENDED for KILOCODE)**

- Remove memory MCP from KILOCODE config
- Use file-based via junctions instead
- Saves ~200K tokens

**Option 2: Configure Properly (If Needed)**

```json
"memory": {
  "command": "node",
  "args": ["C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-memory/dist/index.js"],
  "env": {
    "MEMORY_FILE_PATH": "./.agent/memory/canonical/memory.jsonl"
  }
}
```

- Use smaller memory file
- Keep only essential entities

### C. FOR OPENCODE

Current state (no MCP) is actually OPTIMAL:

- ~50-70KB context from instructions only
- No Memory MCP overhead
- Direct file access

Add back ONLY if needed:

- Redis (for rate limiting) - optional

---

## ACTION ITEMS

### Priority 1: Align KILOCODE

1. Remove Memory MCP from `.kilocode/mcp.json`
2. Keep reference to .antigravity config

### Priority 2: Fix CLINE

1. Add `time` server to `.clinerules/mcp.json`
2. Add `bmad-mcp` server to `.clinerules/mcp.json`

### Priority 3: Document Single Source

1. Create `.antigravity/README.md` documenting it as source
2. Add symlink/junction notes

---

## MEMORY SOLUTION RESEARCH (From UNIFIED-MEMORY-ARCHITECTURE.md)

### Top 2026 Solutions:

| Solution                   | Best For              | Complexity | Recommendation |
| -------------------------- | --------------------- | ---------- | -------------- |
| **Agent-Zero (FAISS)**     | Large semantic search | High       | Too complex    |
| **Everything-Claude-Code** | File-based simplicity | Low        | ✅ Use this    |
| **Hybrid**                 | Both worlds           | Medium     | ✅ Use this    |

### Recommended Approach:

1. **File-based** for small, frequent data (`.agent/memory/canonical/`)
2. **Session-based** for continuity (`.agent/memory/sessions/`)
3. **Surgical loading** - only load what's needed

---

**Report Generated**: 2026-02-22 02:15 **Script**:
scripts/discover_mcp_configs.py
