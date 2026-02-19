# MCP Server Environment Wrapper

## Overview

Created cross-platform wrapper scripts to load `.env` file before starting MCP
servers. This keeps all secrets centralized in `.env` only, avoiding duplication
in config files.

## Files Created

### `.kilocode/mcp-servers/mcp-wrapper.js`

Main Node.js wrapper that:

- Loads `.env` file from project root
- Validates required environment variables
- Spawns MCP server with loaded environment
- Supports: `redis`, `firecrawl`, `github`

### `.kilocode/mcp-servers/wrapper.sh`

Bash backup wrapper (not currently used)

### `.kilocode/mcp-servers/wrapper.bat`

Windows batch backup wrapper (not currently used)

## Updated Configurations

### `.kilocode/mcp.json`

Changed servers to use wrapper:

- `redis` → uses `mcp-wrapper.js redis`
- `firecrawl-local` → uses `mcp-wrapper.js firecrawl`
- `github` → uses `mcp-wrapper.js github`

### `.clinerules/mcp.json`

Same changes as above for Cline compatibility

## Environment Variables Loaded

From `.env`:

- `PROJECT_NAME=marketing-tvoje-info`
- `REDIS_PASSWORD=marketing`
- `REDIS_URL=redis://:marketing@host.docker.internal:36379`
- `FIRECRAWL_API_KEY=fc-...`
- `GITHUB_TOKEN=ghp_...`

## Testing

```bash
# Test wrapper loads .env correctly
node .kilocode/mcp-servers/mcp-wrapper.js redis

# Output should show:
# [MCP-WRAPPER] Loaded .env from: ...
# [MCP-WRAPPER] Starting redis MCP server...
# [ONE-AND-ONLY-REDIS] Project context: marketing-tvoje-info
```

## Next Steps

1. Restart your IDE to reload MCP servers with new configuration
2. The servers will now automatically load `.env` on startup
3. No more `${VAR_NAME}` syntax issues in Git Bash

## Benefits

✅ Secrets stay in `.env` only (not in config files) ✅ Works with Git Bash,
PowerShell, and CMD ✅ Cross-platform (Node.js handles platform differences) ✅
Validates required variables before starting ✅ No changes needed when rotating
API keys
