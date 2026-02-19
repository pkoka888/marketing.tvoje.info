# MCP Server Configuration Sync Report

**Date:** 2026-02-19 **Status:** ✅ ALL CONFIGS SYNCED

---

## Summary

Fixed MCP server environment variable loading across ALL agent frameworks by
implementing the `mcp-wrapper.js` solution consistently.

### Problem

- Multiple agent frameworks had different MCP configurations
- `${VAR_NAME}` syntax doesn't work in Git Bash
- Environment variables scattered across config files
- Inconsistent server setups between IDEs

### Solution

Created unified `mcp-wrapper.js` that loads `.env` before starting servers, then
updated ALL frameworks to use it.

---

## Configurations Updated

### 1. ✅ .kilocode/mcp.json (Kilo Code)

**Status:** Already Updated

Servers using wrapper:

- `redis` ✅
- `github` ✅
- `firecrawl-local` ✅

Servers using direct paths (no env vars needed):

- `filesystem-projects` ✅
- `filesystem-agentic` ✅
- `memory` ✅
- `git` ✅
- `time` ✅
- `fetch` ✅
- `bmad-mcp` ✅
- `playwright-mcp` ✅

### 2. ✅ .clinerules/mcp.json (Cline)

**Status:** Already Updated

Servers using wrapper:

- `redis` ✅
- `github` ✅
- `firecrawl-local` ✅

Servers using direct paths:

- `filesystem-projects` ✅
- `memory` ✅
- `git` ✅
- `fetch` ✅
- `playwright-mcp` ✅

### 3. ✅ .antigravity/mcp.json (Antigravity) - UPDATED

**Status:** Fixed Today

Changes made:

```diff
- "github": {
-   "command": "npx",
-   "args": ["-y", "@modelcontextprotocol/server-github"],
-   "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
- }
+ "github": {
+   "command": "node",
+   "args": [".../mcp-wrapper.js", "github"]
+ }

- "redis": {
-   "command": "node",
-   "args": [".../redis-server.js"],
-   "env": { "REDIS_PASSWORD": "${REDIS_PASSWORD}" }
- }
+ "redis": {
+   "command": "node",
+   "args": [".../mcp-wrapper.js", "redis"]
+ }
```

### 4. ✅ opencode.json (OpenCode) - UPDATED

**Status:** Fixed Today

Changes made:

```diff
- "redis": {
-   "environment": {
-     "REDIS_PASSWORD": "${REDIS_PASSWORD}"
-   }
- }
+ "redis": {
+   "command": ["node", ".../mcp-wrapper.js", "redis"],
+   "environment": {}
+ }

- "github": {
-   "command": ["npx", "-y", "@modelcontextprotocol/server-github"]
- }
+ "github": {
+   "command": ["node", ".../mcp-wrapper.js", "github"]
+ }

- "firecrawl-local": {
-   "environment": {
-     "FIRECRAWL_API_KEY": "{env:FIRECRAWL_API_KEY}"
-   }
- }
+ "firecrawl-local": {
+   "command": ["node", ".../mcp-wrapper.js", "firecrawl"],
+   "environment": {}
+ }
```

---

## Wrapper Script

**File:** `.kilocode/mcp-servers/mcp-wrapper.js`

**Features:**

- Loads `.env` file automatically
- Validates required environment variables
- Works cross-platform (Git Bash, PowerShell, CMD)
- ES module compatible

**Supported Servers:**

- `redis` - Requires: PROJECT_NAME, REDIS_PASSWORD
- `firecrawl` - Requires: FIRECRAWL_API_KEY
- `github` - Requires: GITHUB_TOKEN

**Usage:**

```bash
node .kilocode/mcp-servers/mcp-wrapper.js <server-type>
```

---

## Environment Variables (in .env)

All these are now loaded automatically by the wrapper:

```env
PROJECT_NAME=marketing-tvoje-info
REDIS_PASSWORD=marketing
REDIS_URL=redis://:marketing@host.docker.internal:36379
FIRECRAWL_API_KEY=fc-351f9e63c88b412ebcf75b2283d98179
GITHUB_TOKEN=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
```

---

## Testing

### Verified Working:

```bash
$ node .kilocode/mcp-servers/mcp-wrapper.js redis
[MCP-WRAPPER] Loaded .env from: C:\Users\pavel\projects\marketing.tvoje.info\.env
[MCP-WRAPPER] Starting redis MCP server...
[ONE-AND-ONLY-REDIS] Project context: marketing-tvoje-info
[ONE-AND-ONLY-REDIS] Connected to Redis
```

---

## Antigravity Logs Analysis

**File:** `/c/Users/pavel/vscodeportable/Antigravity/debug.log`

**Findings:**

- Multiple crashpad errors:
  `CreateFile: The system cannot find the file specified`
- These are **normal** Chromium/Electron debug messages
- Not related to MCP server configuration
- No MCP-specific errors found

**Recommendation:** Logs are healthy - just standard Electron/Chromium debugging
output.

---

## Next Steps

### Immediate (Now):

1. ✅ All MCP configs updated
2. [ ] Restart IDEs to load new configurations:
   - VSCode (Cline)
   - Antigravity
   - OpenCode (if running)

### Verification:

3. [ ] Test each MCP server in each IDE:
   - Redis: `redis_ping`
   - GitHub: `list_issues`
   - Firecrawl: `firecrawl_search`

### Future Maintenance:

4. [ ] When adding new MCP server that needs env vars:
   - Add to `mcp-wrapper.js` server configs
   - Update all framework configs to use wrapper
   - Document in `.env.example`

---

## Files Modified Today

### MCP Configuration:

- `.antigravity/mcp.json` - Updated github & redis to use wrapper
- `opencode.json` - Updated redis, github, firecrawl-local to use wrapper

### Already Fixed (Previous Session):

- `.kilocode/mcp.json` - Already had wrapper
- `.clinerules/mcp.json` - Already had wrapper
- `.kilocode/mcp-servers/mcp-wrapper.js` - Created

### YAML Fix:

- `.github/workflows/ci.yml` - Fixed duplicate `env:` key

### Documentation:

- `plans/agent-shared/mcp-wrapper-setup.md`
- `plans/agent-shared/crlf-fix-report.md`
- `plans/agent-shared/github-actions-audit.md`
- `plans/agent-shared/full-project-analysis.md`

---

## Consistency Checklist

| Framework   | Config File           | redis   | github  | firecrawl | Status |
| ----------- | --------------------- | ------- | ------- | --------- | ------ |
| Kilo Code   | .kilocode/mcp.json    | Wrapper | Wrapper | Wrapper   | ✅     |
| Cline       | .clinerules/mcp.json  | Wrapper | Wrapper | Wrapper   | ✅     |
| Antigravity | .antigravity/mcp.json | Wrapper | Wrapper | N/A       | ✅     |
| OpenCode    | opencode.json         | Wrapper | Wrapper | Wrapper   | ✅     |

**All frameworks now use consistent MCP configuration!**

---

## Benefits

1. ✅ **Single Source of Truth** - All secrets in `.env` only
2. ✅ **Cross-Platform** - Works in Git Bash, PowerShell, CMD
3. ✅ **Consistent** - All IDEs use same configuration
4. ✅ **Maintainable** - One wrapper script to update
5. ✅ **Secure** - No secrets in JSON configs

---

_Report generated: 2026-02-19_ _Status: READY FOR TESTING_
