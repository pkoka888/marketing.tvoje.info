# Parallel Orchestration Workflow

**Purpose**: Free-model-first parallel task orchestration across all 7 agents
**Canonical**: `.clinerules/workflows/orchestrate-parallel.md`

---

See canonical version at `.clinerules/workflows/orchestrate-parallel.md` for
full content.

## Quick Reference

### Model Priority (Free-First 2026)

1. **kilo/minimax/minimax-m2.1:free** — default free (unlimited via OpenRouter)
2. **x-ai/grok-code-fast-1:optimized:free** — bulk coding (Kilo Code free)
3. **big-pickle (OpenCode Zen)** — routine tasks (unlimited)
4. **gemini-2.5-flash** — large context (1M/day free tier)
5. **gemini-2.5-pro** — architecture/complex (T3 orchestrator)
6. **claude-sonnet-4-5 (PAID, $20/mo)** — complex only
7. **openai/o3 (PAID, $20/mo)** — hard algorithms only
8. **groq/llama-3.3-70b (PAID)** — last resort fallback

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

| MCP        | Use For                             |
| ---------- | ----------------------------------- |
| `memory`   | Cross-session state                 |
| `redis`    | Parallel agent coordination         |
| `bmad-mcp` | Feature stories (new features only) |
| `git`      | Pre/post change verification        |
| `fetch`    | Web research                        |

### BMAD MCP

Use: new features, phase transitions, sprint plans Skip: routine edits, single
bug fixes, doc updates

### Cost Guard

Log paid model usage in `.kilocode/rules/cost-optimization` Cap: $20/month per
provider
