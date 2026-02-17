# Parallel Orchestration Workflow (OpenCode)

**Purpose**: Free-model-first parallel task orchestration for OpenCode
**Canonical**: `.clinerules/workflows/orchestrate-parallel.md`

---

See canonical version at `.clinerules/workflows/orchestrate-parallel.md` for full content.

## OpenCode-Specific Usage

### Sub-Agent Invocation
Invoke agents with `@agent-name`:
- `@coder` — groq/llama-3.3-70b, bulk implementation
- `@researcher` — groq/llama-3.3-70b, research + memory MCP
- `@reviewer` — groq/llama-3.1-8b-instant, read-only review
- `@orchestrator` — groq/llama-3.3-70b, task decomposition
- `@architect` — claude-sonnet-4-5 (PAID, justify required)
- `@codex` — openai/o3 (PAID, hard algorithms only)

### Parallel Execution in OpenCode
OpenCode can run multiple `@agent` calls in sequence, each inheriting the shared context window. Use `memory` MCP to pass state between agents.

### Command Shortcuts
- `/audit` — run verify_agentic_platform.py
- `/sync-rules` — sync canonical rules to all agent dirs
- `/free-status` — check remaining free-tier capacity
- `/deploy` — deploy marketing site via s60 jumphost

### Model Priority
1. groq/llama-3.3-70b (100K TPD) — OpenCode default
2. groq/llama-3.1-8b (500K TPD) — reviewer/small tasks
3. claude-sonnet-4-5 (PAID) — `@architect` only
4. openai/o3 (PAID) — `@codex` only

### MCP in OpenCode
OpenCode has 4 MCP servers configured in `opencode.json`:
- `filesystem-projects` — file I/O
- `memory` — cross-agent state
- `git` — version control checks
- `fetch` — web research

### Cost Guard
Check `/free-status` before starting any complex task.
Log paid usage in `.kilocode/rules/cost-optimization`.
