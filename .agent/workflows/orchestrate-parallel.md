# Parallel Orchestration Workflow

**Purpose**: Free-model-first parallel task orchestration across all 7 agents
**Canonical**: `.clinerules/workflows/orchestrate-parallel.md`

---

See canonical version at `.clinerules/workflows/orchestrate-parallel.md` for full content.

## Quick Reference

### Model Priority
1. groq/llama-3.3-70b (100K TPD) — default free
2. groq/llama-3.1-8b (500K TPD) — bulk/fast
3. z-ai/glm4.7 (unlimited) — always-on fallback
4. gemini-2.5-flash (1M/day) — large context
5. claude-sonnet-4-5 (PAID, $20/mo) — complex only
6. gemini-2.5-pro (PAID, $20/mo) — architecture only
7. openai/o3 (PAID, $20/mo) — hard algorithms only

### Pattern
ASSESS → SPLIT → ASSIGN → AGGREGATE → VALIDATE

### Parallel-safe tasks
- Code + tests
- Research + docs
- Multi-server checks (s60, s61, s62)
- Lint + build + a11y

### Sequential gates
- Research → Architecture → Implementation
- Build → Test → Deploy

### MCP Usage
| MCP | Use For |
|-----|---------|
| `memory` | Cross-session state |
| `redis` | Parallel agent coordination |
| `bmad-mcp` | Feature stories (new features only) |
| `git` | Pre/post change verification |
| `fetch` | Web research |

### BMAD MCP
Use: new features, phase transitions, sprint plans
Skip: routine edits, single bug fixes, doc updates

### Antigravity Delegation
Antigravity orchestrates via subagents using `.agent/` dir:
- `.agent/agents.yaml`: 7 sub-agents with role definitions
- `.agent/workflows/`: task workflows for each agent
- Subagents invoked by role (architect, debugger, orchestrator, etc.)

### Cost Guard
Log paid model usage in `.kilocode/rules/cost-optimization`
Cap: $20/month per provider
