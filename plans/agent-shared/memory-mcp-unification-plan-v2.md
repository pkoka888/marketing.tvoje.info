# Memory & MCP Unification Plan v2.0 (REVISED)

## Executive Summary

Updated plan based on user feedback:
- **Junctions**: Keep as-is (working properly)
- **Redis MCP**: Configure with existing port 36379, password "marketing"
- **Memory MCP**: Keep enabled, configure properly, test on OpenCode first
- **BMAD**: Keep alwaysAllow: ["*"]
- **Rule**: Never remove files - move to /archive/ instead

---

## 1. Junction Status

### Current Status: ✅ FUNCTIONAL

```
.kilocode/knowledge -> .agent/knowledge  [JUNCTION]
.kilocode/rules     -> .agent/rules      [JUNCTION]
```

### Pros of Junctions:
- No admin rights required
- Minimal performance overhead
- Works with Windows apps
- Survives reboots

### Cons:
- Windows-only (invisible on Linux/WSL)
- Git doesn't preserve junctions
- Some backup software duplicates content

**Decision**: Keep junctions, they work for Antigravity/Kilo in this project

---

## 2. Redis MCP Configuration

### Current Settings:
- **Host**: localhost
- **External Port**: 36379
- **Internal Port**: 6379
- **Password**: marketing

### Recommended Configuration for .agent/mcp.json:

```json
"redis": {
  "command": "node",
  "args": [
    "./.kilocode/mcp-servers/mcp-wrapper.js",
    "redis"
  ],
  "alwaysAllow": [
    "redis_get",
    "redis_set", 
    "redis_del",
    "redis_keys",
    "redis_exists",
    "redis_ttl",
    "redis_expire",
    "redis_ping",
    "redis_info",
    "redis_list_projects"
  ],
  "env": {
    "REDIS_URL": "redis://:marketing@localhost:36379",
    "REDIS_PASSWORD": "marketing"
  },
  "description": "Redis for rate limiting and coordination (project: marketing_tvoje_info)"
}
```

---

## 3. Memory MCP Configuration

### Decision: KEEP ENABLED (per user request)

### Issue: Memory MCP causes high memory usage in Kilo

### Solution: Configure properly + test on OpenCode

Recommended config for opencode.json (test first):

```json
"memory": {
  "type": "local",
  "command": [
    "node",
    "C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-memory/dist/index.js"
  ],
  "env": {
    "MEMORY_FILE_PATH": "C:/Users/pavel/projects/marketing.tvoje.info/.opencode/memory/memory.jsonl"
  }
}
```

### Optimization Strategies:
1. **Surgical loading**: Only load memory entities when needed
2. **Hierarchical structure**: Use entity types (project, task, user)
3. **Periodic cleanup**: Clear old entities regularly

---

## 4. BMAD MCP - Keep alwaysAllow: ["*"]

**Confirmed**: Keep as-is, no changes needed

---

## 5. Archive Rule Implementation

### Rule: Never remove - always move to archive/

Create `.agent/rules/AGENT-DIRECTORY-PROTECTION.md`:

```markdown
# Agent Directory Protection Rule

## Golden Rule
**NEVER delete files - always move to archive/**

### Implementation
- If file needs removal: `mv file archive/agent-memory/filename`
- Never use `rm` or `delete` on agent config files
- Exception: temp files in /tmp/ can be cleaned

### Archive Structure
archive/
├── agent-memory/     # Deprecated agent configs
├── plans/           # Old plans
└── knowledge/       # Deprecated knowledge
```

---

## 6. Parallel Subagents Audit

### Current Subagents (from previous run):

| Subagent | Focus | Status |
|----------|-------|--------|
| memory-architect | Memory locations | ✅ Complete |
| config-reviewer | MCP security | ✅ Complete |
| skills-auditor | Skills analysis | ✅ Complete |

### Audit Results Summary:

**Memory Locations**: 6 locations found
- `.kilocode/rules/memory-bank/` (12 files)
- `.kilocode/knowledge/memory-bank/` (3 files - DUPLICATE)
- `.agent/rules/memory-bank/` (12 files - DUPLICATE)
- `.agent/memory/canonical/` (8 files)

**MCP Servers**:
- Kilo: 12 servers
- Cline: 10 servers  
- Agent: 12 servers

**Skills**:
- Kilo: 22 skills
- Cline: 21 skills
- Agent: 24 skills

---

## 7. Implementation Checklist

- [x] Junctions created and functional
- [ ] Configure Redis MCP with port 36379
- [ ] Configure Memory MCP for OpenCode test
- [ ] Keep BMAD alwaysAllow: ["*"]
- [ ] Create archive rule file
- [ ] Test on OpenCode first
- [ ] Verify all agents see unified memory

---

## Files Created

| File | Purpose |
|------|---------|
| `plans/agent-shared/memory-mcp-unification-plan-v2.md` | This plan |
| `evidence/memory-audit/` | Audit results |
| `.agent/mcp.json` | Canonical MCP config |

---

**Status**: Ready for execution
**Last Updated**: 2026-02-22
