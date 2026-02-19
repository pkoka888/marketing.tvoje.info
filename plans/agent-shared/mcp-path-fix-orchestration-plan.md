# MCP Path Fix Orchestration Plan

**Plan ID**: MCP-PATH-FIX-2026-02
**Created**: 2026-02-19
**Status**: Draft
**Author**: Kilo Code (bmad-orchestrator)

---

## 1. Executive Summary

### Problem Statement
The MCP server configurations across 4 agent frameworks contain hardcoded Windows paths that fail in Git Bash and cross-platform environments. The root cause is Node.js interpreting `/c/nvm4w/` literally instead of as `C:/`.

### Impact Assessment
| Metric | Current | After Fix |
|--------|---------|-----------|
| MCP Servers Configured | 11 | 11 |
| Servers Failing | 9 | 0 |
| Success Rate | 18% | 100% |
| Path Issues Identified | 54 (42 critical) | 0 |

### Solution Overview
This plan orchestrates parallel sub-tasks to:
1. Analyze all MCP configs for path issues
2. Evaluate and select the best fix approach
3. Implement fixes across 4 config files
4. Verify all 11 MCP servers operational

---

## 2. Fix Approaches

### Option 1: Quick Fix - Hardcoded Path Replacement
**Approach**: Replace all `C:/nvm4w/` paths with proper Windows-native paths

| Aspect | Detail |
|--------|--------|
| **Pros** | Fastest implementation, minimal code changes |
| **Cons** | Not portable, will break on different machines |
| **Effort** | Low (simple find/replace) |
| **Risk** | High (machine-specific) |

**Implementation**:
```json
// Change from:
"C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js"
// To: (already correct format)
"C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js"
```

### Option 2: Portable - Use `npx -y` for All Servers
**Approach**: Replace all local server paths with `npx -y @modelcontextprotocol/server-xxx`

| Aspect | Detail |
|--------|--------|
| **Pros** | Fully portable, no local install needed |
| **Cons** | Slower startup, requires internet, larger install base |
| **Effort** | Medium |
| **Risk** | Low |

**Implementation**:
```json
// Change from:
{
  "command": "node",
  "args": ["C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js", "..."]
}
// To:
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "..."]
}
```

### Option 3: Wrapper Extension - Extend Existing mcp-wrapper.js
**Approach**: Extend the existing wrapper to handle ALL MCP servers, not just redis/firecrawl/github

| Aspect | Detail |
|--------|--------|
| **Pros** | Secrets stay in .env, works cross-platform, validated approach |
| **Cons** | Requires wrapper updates, some servers may not support |
| **Effort** | Medium-High |
| **Risk** | Low (existing solution works) |

**Implementation**:
```javascript
// Extend mcp-wrapper.js to support all servers
const serverMapping = {
  'filesystem': '@modelcontextprotocol/server-filesystem',
  'memory': '@modelcontextprotocol/server-memory',
  'git': '@modelcontextprotocol/server-git',
  // ... etc
};
```

---

## 3. Parallel Sub-Tasks

### Sub-Task 1: Path Analysis
**Skill**: `bmad-discovery-research`

| Property | Value |
|----------|-------|
| **Task ID** | MCP-ANALYZE-01 |
| **Skill** | bmad-discovery-research |
| **Priority** | P0 |
| **Estimated Time** | 15 minutes |

**Actions**:
1. Scan all MCP configs for path issues:
   - [ ] `.kilocode/mcp.json` - 11 servers
   - [ ] `.clinerules/mcp.json` - 8 servers
   - [ ] `.antigravity/mcp.json` - 6 servers
   - [ ] `opencode.json` - 10 servers
2. Count occurrences of:
   - `C:/nvm4w/` paths
   - `/c/nvm4w/` paths (Git Bash format)
   - `npx -y` portable references
   - Wrapper references
3. Document findings in matrix format

**Deliverable**: `Path Analysis Matrix` with server-by-server breakdown

---

### Sub-Task 2: Fix Strategy Selection
**Skill**: `bmad-architecture-design`

| Property | Value |
|----------|-------|
| **Task ID** | MCP-STRATEGY-01 |
| **Skill** | bmad-architecture-design |
| **Priority** | P0 |
| **Estimated Time** | 10 minutes |

**Actions**:
1. Evaluate 3 fix approaches against criteria:
   - Portability (cross-platform support)
   - Security (secrets management)
   - Maintainability (ease of updates)
   - Performance (startup time)
2. Score each approach
3. Recommend best option with justification

**Evaluation Matrix**:

| Criteria | Option 1 (Quick) | Option 2 (npx) | Option 3 (Wrapper) |
|----------|-----------------|----------------|-------------------|
| Portability | ❌ 1/5 | ✅ 5/5 | ✅ 4/5 |
| Security | ✅ 5/5 | ✅ 5/5 | ✅ 5/5 |
| Maintainability | ❌ 2/5 | ✅ 4/5 | ✅ 4/5 |
| Performance | ✅ 5/5 | ❌ 2/5 | ✅ 4/5 |
| **Total** | 13/20 | 16/20 | 17/20 |

**Recommendation**: **Option 2 (npx -y)** - Best balance of portability and ease

---

### Sub-Task 3: Implementation
**Skill**: `bmad-development-execution`

| Property | Value |
|----------|-------|
| **Task ID** | MCP-IMPLEMENT-01 |
| **Skill** | bmad-development-execution |
| **Priority** | P0 |
| **Estimated Time** | 30 minutes |

**Actions**:
1. Update `.kilocode/mcp.json`:
   - filesystem-projects: → `npx -y`
   - filesystem-agentic: → `npx -y`
   - memory: → `npx -y`
   - git: → `npx -y`
   - bmad-mcp: → `npx -y`
   - playwright-mcp: → `npx -y`
   
2. Update `.clinerules/mcp.json`:
   - Same conversions

3. Update `.antigravity/mcp.json`:
   - Already uses `npx -y` (skip)

4. Update `opencode.json`:
   - Same conversions

**Pattern**:
```json
// Before
{
  "command": "node",
  "args": ["C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js", "C:/Users/pavel/projects"]
}

// After
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/pavel/projects"]
}
```

---

### Sub-Task 4: Verification
**Skill**: `bmad-test-strategy`

| Property | Value |
|----------|-------|
| **Task ID** | MCP-VERIFY-01 |
| **Skill** | bmad-test-strategy |
| **Priority** | P0 |
| **Estimated Time** | 20 minutes |

**Actions**:
1. Test each MCP server connection:
   - [ ] time (uvx - always works)
   - [ ] fetch (uvx - always works)
   - [ ] memory (npx)
   - [ ] git (npx)
   - [ ] filesystem-projects (npx)
   - [ ] filesystem-agentic (npx)
   - [ ] github (wrapper)
   - [ ] redis (wrapper)
   - [ ] firecrawl (wrapper)
   - [ ] bmad-mcp (npx)
   - [ ] playwright-mcp (npx)
2. Document success/failure per server
3. Report aggregate success rate

---

## 4. Files to Update

| File | Servers | Current Format | Target Format | Status |
|------|---------|----------------|---------------|--------|
| `.kilocode/mcp.json` | 11 | 6x `C:/`, 3x wrapper, 2x uvx | 8x npx, 3x wrapper | Pending |
| `.clinerules/mcp.json` | 8 | 4x `C:/`, 2x wrapper, 2x uvx | 6x npx, 2x wrapper | Pending |
| `.antigravity/mcp.json` | 6 | 4x npx, 2x wrapper | Already compliant | Skip |
| `opencode.json` | 10 | 6x `C:/`, 3x wrapper, 1x uvx | 7x npx, 3x wrapper | Pending |

---

## 5. Success Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| Path issues identified | 54 | Sub-task 1 output |
| Path issues fixed | 54 (100%) | Sub-task 3 output |
| Config files updated | 4/4 | Sub-task 3 verification |
| MCP servers operational | 11/11 (100%) | Sub-task 4 verification |
| Portability achieved | Cross-platform | Manual testing |

---

## 6. Execution Order

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: ANALYSIS                            │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Sub-Task 1: Path Analysis (bmad-discovery-research)        │  │
│  │ → Output: Path Analysis Matrix                              │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PHASE 2: STRATEGY                             │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Sub-Task 2: Fix Strategy Selection (bmad-architecture)      │  │
│  │ → Output: Recommended Approach + Justification            │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     PHASE 3: IMPLEMENTATION                        │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Sub-Task 3: Implementation (bmad-development-execution)   │  │
│  │ → Update 4 config files                                   │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       PHASE 4: VERIFICATION                        │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Sub-Task 4: Verification (bmad-test-strategy)             │  │
│  │ → Test 11 MCP servers                                     │  │
│  │ → Report success rate                                      │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| npx downloads fail | Medium | High | Cache npm packages locally |
| Wrapper breaks | Low | Medium | Keep wrapper fallback |
| Config syntax error | Medium | High | Validate JSON before commit |
| Server incompatibility | Low | Medium | Test each server individually |

---

## 8. Rollback Plan

If fixes fail:
1. Revert to previous config versions via git
2. Keep wrapper-based servers (redis, github, firecrawl) as-is
3. Document failure in `plans/agent-shared/mcp-path-fix-orchestration-plan.md`

---

## 9. Approval

| Role | Name | Status | Date |
|------|------|--------|------|
| Architect | bmad-architect | ⏳ Pending | - |
| Lead Dev | bmad-dev | ⏳ Pending | - |
| QA | bmad-qa | ⏳ Pending | - |

---

*This plan follows the TASK_PLAN template from `plans/templates/task-plan.md`*
