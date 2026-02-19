# Full Functionality Brainstorm - Agentic Platform Recovery

**Date**: 2026-02-19 **Status**: Critical Infrastructure Recovery **Goal**:
Complete analysis of what's needed for 100% functionality

---

## Current State Summary

### ✅ Working Now

- **Redis MCP**: PONG verified, project namespace active
- **Path fixes**: All MCP configs converted to Git Bash format (`/c/`)
- **bmad-mcp**: Corrected from Python module to Node.js server path
- **Core tools**: Node, npm, Python, uvx available in Git Bash

### ⚠️ Partially Working

- **MCP Server Startup**: Paths fixed but need runtime testing
- **opencode.json**: All paths updated, needs validation
- **Agent orchestration**: Framework exists but needs activation

### ❌ Known Broken

- **Kilo CLI**: Not in Git Bash PATH (Windows-only currently)
- **Cline CLI**: Not in Git Bash PATH
- **Swarm audit**: Failing due to missing CLI tools
- **Parallel orchestration**: Disabled without working agents

---

## 7-Layer Full Functionality Stack

### Layer 1: Foundation (Shell & PATH)

**Status**: 60% Complete

**Requirements**:

- [x] Git Bash as primary shell
- [x] Node.js v22+ accessible
- [x] Python 3.13+ accessible
- [x] uvx for Python MCP servers
- [ ] Kilo CLI in PATH
- [ ] Cline CLI in PATH
- [ ] Opencode CLI in PATH (if separate)

**Action Items**:

```bash
# Add to ~/.bashrc
echo 'export PATH="$PATH:/c/Users/pavel/AppData/Roaming/npm"' >> ~/.bashrc
echo 'export PATH="$PATH:/c/nvm4w/nodejs"' >> ~/.bashrc
source ~/.bashrc

# Verify
which kilo cline opencode
```

---

### Layer 2: MCP Server Infrastructure

**Status**: 70% Complete (Paths fixed, need runtime test)

**10 MCP Servers to Verify**:

| Server              | Type       | Status         | Test Command           |
| ------------------- | ---------- | -------------- | ---------------------- |
| filesystem-projects | Node       | ✅ Paths fixed | Read project files     |
| filesystem-agentic  | Node       | ✅ Paths fixed | Read agentic framework |
| memory              | Node       | ✅ Paths fixed | Read graph             |
| git                 | Node       | ✅ Paths fixed | Git status             |
| github              | Node       | ✅ Paths fixed | List issues            |
| fetch               | Python/uvx | ✅ Available   | Fetch URL              |
| redis               | Node       | ✅ Working     | Ping                   |
| bmad-mcp            | Node       | ✅ Path fixed  | Workflow status        |
| firecrawl-local     | Node       | ✅ Paths fixed | Scrape URL             |
| playwright-mcp      | Node       | ✅ Paths fixed | Browser snapshot       |

**Action Items**:

1. Create comprehensive MCP test suite
2. Validate each server can start and respond
3. Document any authentication requirements (GitHub token, Firecrawl key)

---

### Layer 3: Agent CLI Tools

**Status**: 30% Complete

**Required Tools**:

| Tool          | Purpose       | Install Status | PATH Status        |
| ------------- | ------------- | -------------- | ------------------ |
| kilo          | Kilo Code CLI | ✅ Global npm  | ❌ Not in Git Bash |
| cline         | Cline CLI     | ✅ Global npm  | ❌ Not in Git Bash |
| opencode      | Opencode CLI  | ?              | ?                  |
| @kilocode/cli | Kilo CLI      | ✅ Global npm  | ❌ Not in Git Bash |

**Action Items**:

```bash
# Check actual installation locations
ls -la /c/Users/pavel/AppData/Roaming/npm/ | grep -E "kilo|cline"
ls -la /c/nvm4w/nodejs/ | grep -E "kilo|cline"

# Create symlinks or update PATH
# Option 1: Add to PATH
echo 'export PATH="$PATH:/c/Users/pavel/AppData/Roaming/npm"' >> ~/.bashrc

# Option 2: Create wrapper scripts
mkdir -p ~/bin
cat > ~/bin/kilo << 'EOF'
#!/bin/bash
/c/Users/pavel/AppData/Roaming/npm/kilo "$@"
EOF
chmod +x ~/bin/kilo
```

---

### Layer 4: BMAD Workflow Orchestration

**Status**: 50% Complete (bmad-mcp fixed, needs integration)

**BMAD Components**:

- [x] bmad-mcp server installed globally
- [x] bmad-mcp path corrected in all configs
- [ ] BMAD workflow directory initialized (`_bmad/`)
- [ ] Agent role definitions loaded
- [ ] Workflow state management tested

**Architecture**:

```
User Request
    ↓
Orchestrator (Antigravity/OpenCode)
    ↓
bmad-mcp (Workflow State Manager)
    ↓
┌─────────────┬─────────────┬─────────────┐
↓             ↓             ↓             ↓
PO          Architect     Developer     QA
(Claude)    (Claude)      (Kilo)        (Cline)
    ↓             ↓             ↓             ↓
PRD         Arch Doc      Code          Tests
    ↓             ↓             ↓             ↓
└─────────────┴─────────────┴─────────────┘
    ↓
Artifacts → _bmad-output/
```

**Action Items**:

1. Initialize BMAD workflow directory structure
2. Test bmad-mcp with `bmad-task action="status"`
3. Verify agent-to-bmad-mcp communication
4. Create sample workflow (PO → Architect → Dev → QA)

---

### Layer 5: Parallel Orchestration

**Status**: 20% Complete (Framework exists, needs CLI tools)

**Components**:

| Component             | Status    | Notes                         |
| --------------------- | --------- | ----------------------------- |
| Swarm audit script    | ✅ Exists | Needs working CLIs            |
| Orchestrate swarms    | ✅ Exists | Needs parallel execution test |
| Agent tools (Python)  | ✅ Exists | For Groq API access           |
| Parallel workflow def | ✅ Exists | In `.kilocode/workflows/`     |

**Required for Full Functionality**:

- [ ] Working Kilo CLI
- [ ] Working Cline CLI
- [ ] Groq API access (for Flash/Analyst)
- [ ] Parallel execution tested with 3+ agents
- [ ] Redis coordination for agent state

**Test Scenario**:

```python
# scripts/swarm_audit.py should successfully:
1. Spawn Analyst (Groq/Flash) - analyze codebase
2. Spawn Developer (Kilo) - list agents/implement
3. Spawn QA (Cline) - verify/test
4. Aggregate results to Redis
5. Generate audit report
```

---

### Layer 6: Cross-Agent Configuration Sync

**Status**: 60% Complete (MCP configs synced, rule sync needed)

**Configuration Files** (Must Stay Synchronized):

| File                    | Purpose                 | Sync Status          |
| ----------------------- | ----------------------- | -------------------- |
| `.kilocode/mcp.json`    | Kilo MCP config         | ✅ Fixed             |
| `.clinerules/mcp.json`  | Cline MCP config        | ✅ Fixed             |
| `.antigravity/mcp.json` | Antigravity MCP         | ✅ Fixed             |
| `opencode.json`         | Opencode MCP + settings | ✅ Fixed             |
| `.kilocode/rules/*`     | Canonical rules         | ⚠️ Need verification |
| `.clinerules/skills/*`  | Cline skills            | ⚠️ Need verification |
| `AGENTS.md`             | Master documentation    | ⚠️ May need updates  |

**Rule Sync Requirements**:

- Memory bank instructions
- Cost optimization rules
- Server preservation rules
- Python-preferred rules
- MCP alignment rules

**Action Items**:

```bash
# Run verification script
python scripts/verify_agentic_platform.py

# Check rule parity
python scripts/validate_kilo_configs.py
```

---

### Layer 7: Environment & Secrets

**Status**: 40% Complete

**Required Environment Variables**:

| Variable             | Purpose        | Status       | Source        |
| -------------------- | -------------- | ------------ | ------------- |
| `OPENROUTER_API_KEY` | LLM API access | ?            | User-provided |
| `GITHUB_TOKEN`       | GitHub MCP     | ?            | User-provided |
| `REDIS_PASSWORD`     | Redis MCP      | ✅ Hardcoded | Config        |
| `FIRECRAWL_API_KEY`  | Firecrawl MCP  | ?            | User-provided |
| `PROJECT_ROOT`       | BMAD MCP       | ✅ Set       | Config        |
| `GROQ_API_KEY`       | Groq/Analyst   | ?            | User-provided |

**Security Improvements**:

- [ ] Move secrets to `.env` file
- [ ] Add `.env` to `.gitignore`
- [ ] Create `.env.example` template
- [ ] Document required secrets in SETUP.md

---

## Critical Path to Full Functionality

### Phase 1: Foundation (Today - P0)

**Goal**: Make all CLI tools accessible

**Tasks**:

1. [ ] Fix Git Bash PATH for kilo/cline/opencode
2. [ ] Verify all CLI tools respond to `--version`
3. [ ] Test basic agent commands

**Validation**:

```bash
which kilo && kilo --version
which cline && cline --version
which opencode && opencode --version
```

### Phase 2: MCP Runtime (Today - P0)

**Goal**: All 10 MCP servers operational

**Tasks**:

1. [ ] Create MCP test suite
2. [ ] Test each MCP server startup
3. [ ] Document authentication requirements
4. [ ] Fix any runtime errors

**Validation**:

```bash
python scripts/test_mcp_servers.py
# All 10 servers: ✅
```

### Phase 3: BMAD Integration (This Week - P1)

**Goal**: Working BMAD workflow orchestration

**Tasks**:

1. [ ] Initialize BMAD workflow directory
2. [ ] Test bmad-mcp status command
3. [ ] Run sample workflow (PO → Dev)
4. [ ] Verify artifact generation

**Validation**:

```bash
# bmad-mcp responds to workflow commands
# Artifacts appear in _bmad-output/
```

### Phase 4: Parallel Orchestration (This Week - P1)

**Goal**: Working 3-agent parallel execution

**Tasks**:

1. [ ] Fix swarm audit script
2. [ ] Test parallel agent spawning
3. [ ] Implement Redis coordination
4. [ ] Generate swarm audit report

**Validation**:

```bash
python scripts/swarm_audit.py
# All 3 agents: ✅
```

### Phase 5: Production Readiness (Next Week - P2)

**Goal**: Production-ready agentic platform

**Tasks**:

1. [ ] Environment secrets management
2. [ ] Cross-agent config verification
3. [ ] Documentation updates
4. [ ] Error handling & recovery
5. [ ] Performance optimization

---

## Decision Points

### 1. Shell Strategy

**Option A**: Pure Git Bash (Current)

- Pros: Consistent Unix-style paths
- Cons: Windows CLIs may need wrappers

**Option B**: Windows Terminal + PowerShell

- Pros: Native Windows CLI support
- Cons: Different path formats

**Option C**: Hybrid (Git Bash + Windows where needed)

- Pros: Flexibility
- Cons: Complexity

**Recommendation**: Stick with Option A (Git Bash) and create proper wrappers

### 2. Agent Model Strategy

**Current**: 7-layer model with fallbacks **Issue**: Cline credits depleted
($0.01)

**Options**:

1. Replenish Cline credits
2. Route all through OpenCode/Kilo free models
3. Use Groq as fallback for complex tasks

**Recommendation**: Option 2 - Consolidate on free models (Kilo/OpenCode) + Groq
for complex tasks

### 3. BMAD Scope

**Option A**: Full BMAD (9 agents) **Option B**: bmad-mcp subset (5 agents)
**Option C**: Custom workflow

**Recommendation**: Option B for now, expand to A when stable

---

## Success Metrics

| Metric              | Current | Target | How to Measure               |
| ------------------- | ------- | ------ | ---------------------------- |
| MCP Servers Online  | 1/10    | 10/10  | `test_mcp_servers.py`        |
| CLI Tools Available | 0/3     | 3/3    | `which kilo cline opencode`  |
| BMAD Workflow       | ❌      | ✅     | Run sample workflow          |
| Parallel Agents     | ❌      | ✅     | `swarm_audit.py` passes      |
| Config Sync         | 60%     | 100%   | `verify_agentic_platform.py` |
| Secrets Management  | ❌      | ✅     | `.env` file exists           |

---

## Immediate Next Actions

1. **Fix PATH** - Add npm global to Git Bash PATH
2. **Test MCPs** - Run comprehensive MCP test suite
3. **Verify CLIs** - Confirm kilo/cline/opencode accessible
4. **Test BMAD** - Run bmad-mcp status command
5. **Run Swarm** - Execute parallel agent audit

**Estimated Time**: 2-4 hours for full functionality

---

## Questions for User

1. Do you have API keys for: OpenRouter, GitHub, Firecrawl, Groq?
2. Should we consolidate on Git Bash or consider Windows Terminal?
3. What's the priority: BMAD workflows or parallel orchestration first?
4. Do you want to replenish Cline credits or route everything through free
   models?
