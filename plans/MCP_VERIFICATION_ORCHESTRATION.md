# MCP Verification & System Health Orchestration Plan

**Date**: 2026-02-19 **Status**: In Progress **Objective**: Parallel
verification of all tools, MCP servers, and system health

---

## Current State

### Tool Versions (Verified Working)

- ✅ npm: 10.9.4
- ✅ npx: 10.9.4
- ✅ node: v22.22.0
- ✅ python: 3.13.7
- ✅ uvx: 0.10.0
- ✅ git: 2.51.0.windows.1
- ✅ redis: PONG verified

### MCP Servers Status

**Installed in `/c/nvm4w/nodejs/node_modules/`:**

- ✅ @modelcontextprotocol/server-filesystem
- ✅ @modelcontextprotocol/server-github
- ✅ @modelcontextprotocol/server-memory
- ✅ @modelcontextprotocol/server-postgres
- ✅ @modelcontextprotocol/server-puppeteer
- ✅ @modelcontextprotocol/server-redis
- ✅ @modelcontextprotocol/server-sequential-thinking
- ✅ git-mcp
- ✅ bmad-mcp
- ✅ @playwright/mcp
- ✅ firecrawl-mcp

**Missing/Needs Verification:**

- ⚠️ mcp-server-fetch (Python/uvx)
- ⚠️ firecrawl-local path validity
- ⚠️ redis-server.js custom server

---

## Parallel Subagent Tasks

### Task 1: Tool Chain Verification (@researcher)

**Skill**: `system-verification`

**Objective**: Verify all CLI tools work correctly in Git Bash

**Commands to execute:**

```bash
# Version checks
node --version && npm --version && npx --version
python --version && pip --version
uvx --version
git --version

# Path verification
echo "PATH entries:"
echo $PATH | tr ':' '\n' | grep -E "npm|node|python"

# Which checks
which node npm npx python uvx git

# Git bash compatibility
type node
type npm
type python
```

**Deliverable**: Report with version matrix and any PATH issues

---

### Task 2: MCP Server Runtime Test (@codex)

**Skill**: `mcp-testing`

**Objective**: Test all 10 MCP servers can start and respond

**Test approach**: Create test script that:

1. Attempts to start each MCP server
2. Sends ListTools request
3. Validates response
4. Reports success/failure

**Servers to test:**

1. filesystem-projects
2. filesystem-agentic
3. memory
4. git
5. github
6. fetch
7. redis
8. bmad-mcp
9. firecrawl-local
10. playwright-mcp

**Deliverable**: MCP server status report with pass/fail for each

---

### Task 3: Antigravity Log Analysis (@debugger)

**Skill**: `log-analysis`

**Objective**: Find and analyze any Antigravity error logs

**Search locations:**

```bash
# Common log locations
find . -name "*.log" -type f 2>/dev/null | grep -i antigravity
find ~/.antigravity -name "*.log" 2>/dev/null
find /tmp -name "*antigravity*" 2>/dev/null
ls -la ~/.cache/antigravity/ 2>/dev/null
```

**Also check:**

- VSCode extension logs
- Windows Event Viewer (if accessible)
- Any crash dumps or error files

**Deliverable**: Log analysis report with any errors found

---

### Task 4: Missing MCP Installation (@architect)

**Skill**: `infrastructure-setup`

**Objective**: Install missing MCP servers and fix configuration

**Required actions:**

1. Install mcp-server-fetch via uvx if needed
2. Verify firecrawl-local path exists
3. Check redis-server.js is functional
4. Update opencode.json with any corrections
5. Create missing directories

**Deliverable**: Installation report and updated configs

---

### Task 5: Integration & Health Check (@orchestrator)

**Skill**: `system-integration`

**Objective**: Full system integration test

**Test scenarios:**

1. Redis read/write
2. Filesystem access (projects + agentic)
3. Memory graph operations
4. Git operations
5. GitHub API (if token available)
6. Fetch a URL
7. BMAD workflow check
8. Playwright browser launch

**Deliverable**: Integration test report

---

## Execution Order

```
Phase 1 (PARALLEL):
├── Task 1: Tool Chain Verification
├── Task 2: MCP Server Runtime Test
├── Task 3: Antigravity Log Analysis
└── Task 4: Missing MCP Installation

Phase 2 (SEQUENTIAL after Phase 1):
└── Task 5: Integration & Health Check
    (depends on Tasks 1-4 completing)

Phase 3 (FINAL):
└── Aggregate Results & Update Plan
```

---

## Success Criteria

- [ ] All 10 MCP servers respond to ListTools
- [ ] All CLI tools accessible in Git Bash PATH
- [ ] No critical errors in logs
- [ ] Redis integration working
- [ ] Full integration test passes

---

## Risk Mitigation

| Risk                      | Mitigation                        |
| ------------------------- | --------------------------------- |
| Missing API keys          | Document which require env vars   |
| PATH issues               | Create symlink or wrapper scripts |
| Windows-specific problems | Document workarounds              |
| Firecrawl path invalid    | Update to correct path or install |

---

## Output Location

All subagent reports go to: `plans/agent-shared/mcp-verification-results.md`

Final orchestration report: `plans/MCP_VERIFICATION_COMPLETE.md`
