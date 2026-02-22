# FINAL RECOMMENDATION - Memory Architecture (2026-02-22)

## VERIFIED: Junctions ARE Working ✅

```
.kilocode/knowledge → .agent/knowledge  [SYMLINK - WORKING]
.kilocode/rules     → .agent/rules      [SYMLINK - WORKING]
```

This means KiloCode CAN already see `.agent/` files via junctions!

---

## COMPARISON: All Three Approaches

| Approach          | Pros                                  | Cons                | Best For              |
| ----------------- | ------------------------------------- | ------------------- | --------------------- |
| **My Analysis**   | Comprehensive, covers all angles      | Too complex         | General guidance      |
| **Cline Plan v1** | Disables Memory MCP, surgical loading | Loses entity memory | KiloCode specifically |
| **Cline Plan v2** | Keeps junctions, configures Redis     | Keeps Memory MCP    | OpenCode testing      |

---

## ROOT CAUSE: Why KiloCode Has Context Issues

```
┌─────────────────────────────────────────────────────────┐
│ KiloCode Context Usage                                  │
├─────────────────────────────────────────────────────────┤
│ • Memory MCP enabled: +200K tokens                     │
│ • Skills (22): ~50KB                                   │
│ • Knowledge (via junction): ~100KB                     │
│ • Rules: ~30KB                                         │
│                                                         │
│ TOTAL: ~380KB+ (exceeds most context limits!)          │
├─────────────────────────────────────────────────────────┤
│ Cline Context Usage                                     │
├─────────────────────────────────────────────────────────┤
│ • Memory MCP: DISABLED (0 tokens)                      │
│ • Skills: ~20KB                                        │
│ • Direct file loading: ~50KB                            │
│                                                         │
│ TOTAL: ~70KB (fits easily)                             │
└─────────────────────────────────────────────────────────┘
```

---

## RECOMMENDATION FOR KILOCODE

### Option A: Disable Memory MCP (RECOMMENDED FOR KILOCODE)

In `.kilocode/mcp.json`, remove the memory server:

```json
// REMOVE THIS:
"memory": {
  "command": "node",
  "args": [".../server-memory/dist/index.js"]
}
```

**Why:**

- Saves ~200K tokens
- Junctions already give access to `.agent/knowledge`
- KiloCode will still see files via symlinks

### Option B: Keep Memory MCP But Use Smaller File

```json
"memory": {
  "command": "node",
  "args": [".../server-memory/dist/index.js"],
  "env": {
    "MEMORY_FILE_PATH": "./.agent/memory/canonical/memory-small.jsonl"
  }
}
```

Create a small memory file with only essential entities.

---

## RECOMMENDATION FOR OPENCODE

The user removed all MCP servers from OpenCode. This is actually GOOD for
context:

**Current OpenCode (no MCP):**

- Loads instructions (~15 files)
- No Memory MCP
- No Redis MCP
- Uses filesystem directly

**This is optimal!** OpenCode will have:

- ~50-70KB context from instructions
- No Memory MCP overhead
- Direct file access via filesystem-projects

**Add back ONLY if needed:**

- Redis (for rate limiting) - can add later
- Memory MCP - NOT recommended (adds 200K tokens)

---

## ACTION ITEMS

### For KiloCode:

1. Edit `.kilocode/mcp.json` - comment out or remove memory MCP
2. Test - context should drop significantly

### For OpenCode:

1. Current config is GOOD (minimal MCP)
2. Add Redis ONLY if you need rate limiting
3. Do NOT add Memory MCP

### For Both:

1. Junctions are working ✅
2. Both agents can see `.agent/` files via symlinks
3. No further consolidation needed

---

## FILES TO MODIFY

```bash
# KiloCode - disable memory MCP
edit_file(".kilocode/mcp.json", remove "memory" server)

# Test by running KiloCode and checking context
```

---

**Status**: Ready to execute **Priority**: HIGH for KiloCode context reduction
