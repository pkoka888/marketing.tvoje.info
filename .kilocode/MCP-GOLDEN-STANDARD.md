# MCP Server Configuration - GOLDEN STANDARD

**⚠️ DO NOT CHANGE THIS FILE WITHOUT APPROVAL ⚠️**

This is the authoritative MCP configuration. All AI agents must use exactly this configuration.

## Current Working Configuration (Tested 2026-02-13)

```json
{
  "mcpServers": {
    "redis": {
      "command": "cmd",
      "args": ["/c", "npx -y @modelcontextprotocol/server-redis"],
      "env": {
        "REDIS_URL": "redis://host.docker.internal:36379",
        "REDIS_HOST": "host.docker.internal",
        "REDIS_PORT": "36379"
      },
      "description": "Official Redis MCP server - Port 36379"
    },
    "memory": {
      "command": "cmd",
      "args": ["/c", "npx -y mcp-memory-keeper"],
      "env": {
        "MEMORY_KEEPER_STORAGE_DIR": "C:/Users/pavel/vscodeportable/agentic/memory-keeper",
        "MEMORY_KEEPER_AUTO_UPDATE": "1"
      },
      "description": "Persistent memory with channels and checkpoints - survives sessions"
    },
    "playwright-mcp": {
      "command": "cmd",
      "args": ["/c", "npx -y @playwright/mcp"],
      "description": "Microsoft Playwright MCP - Windows fix: cmd /c"
    }
  }
}
```

## Critical Rules

### 1. Redis Configuration (NEVER CHANGE)

- Port: **36379** (non-standard)
- Host: **host.docker.internal** (Docker network)
- Command: **cmd /c** (Windows stdio fix)
- Env vars: REDIS_URL, REDIS_HOST, REDIS_PORT

### 2. Memory Configuration (PERSISTENT - CRITICAL)

**IMPORTANT**: Use `mcp-memory-keeper` NOT `@modelcontextprotocol/server-memory`

- `@modelcontextprotocol/server-memory` = **IN-MEMORY** (forgets on session end)
- `mcp-memory-keeper` = **PERSISTENT** (saves to disk, survives restarts)

Features of mcp-memory-keeper:

- Channels for organizing context
- Checkpoints for complete snapshots
- File-based storage
- Auto-save with `MEMORY_KEEPER_AUTO_UPDATE=1`

Storage location: `C:/Users/pavel/vscodeportable/agentic/memory-keeper`

### 3. Package Names (NEVER CHANGE)

- Redis: `@modelcontextprotocol/server-redis`
- Memory: `mcp-memory-keeper` (NOT `@modelcontextprotocol/server-memory`)
- Playwright: `@playwright/mcp` (NOT `@modelcontextprotocol/server-playwright`)

### 4. Windows Fix (REQUIRED)

All npx commands MUST use `cmd /c` wrapper on Windows:

- ✅ `"command": "cmd", "args": ["/c", "npx -y ..."]`
- ❌ `"command": "npx"` (will fail!)

## Validation

Run this to validate:

```bash
npm run validate:mcp
```

Or manually:

```bash
node -e "const mcp = JSON.parse(require('fs').readFileSync('.kilocode/mcp.json')); console.log('Redis port:', mcp.mcpServers.redis.env.REDIS_PORT); console.log('Memory package:', mcp.mcpServers.memory.args.join(' ')); console.log('Playwright cmd:', mcp.mcpServers['playwright-mcp'].command);"
```

Expected output:

```
Redis port: 36379
Memory package: npx -y mcp-memory-keeper
Playwright cmd: cmd
```

## If You Need to Change

1. Document the reason in `plans/mcp-changes.md`
2. Get user approval
3. Update this file AND all references
4. Test thoroughly
5. Update this document with new working config

---

**Last Verified Working:** 2026-02-13 14:15 UTC
