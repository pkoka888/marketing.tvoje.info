# Parallel Orchestration Workflow

**Purpose**: Free-model-first parallel task orchestration across all 7 agents
**Canonical**: `.clinerules/workflows/orchestrate-parallel.md`

---

## Overview

This workflow implements the 2026 best-practice ASSESS→SPLIT→ASSIGN→AGGREGATE→VALIDATE pattern for orchestrating complex tasks using free AI models first, paid models only when necessary.

## Model Priority Order

| Priority | Model                             | Provider    | Limit       | Use For                                               |
| -------- | --------------------------------- | ----------- | ----------- | ----------------------------------------------------- | --- |
| 1 (FREE) | **Gemini CLI** (Gemini 2.5/3 Pro) | Google      | 1M TPD      | **Primary**: High context, complex logic, research    |
| 2 (FREE) | **OpenCode Default** (Flash/Kilo) | OpenCode    | Daily Limit | **Primary**: Code generation, standard tasks          |
| 3 (FREE) | **Kilo** (`z-ai/glm4.7`)          | Kilo/NVIDIA | Unlimited   | **Fallback**: Bulk coding, always-on availability     |
| 4 (FREE) | **Cline Provider**                | Cline       | -           | **Fallback**: Routine tasks, extension integration    |
| 5 (FREE) | **NVIDIA / OpenRouter**           | Mixed       | Varied      | **Fallback**: Extra capacity when others exhausted    |
| 6 (PAID) | **OpenAI** (`o3`)                 | OpenAI      | Paid        | **Complex**: Hard algorithms, critical reasoning only |
| 7 (PAID) | **Groq** (`llama-3.3-70b`)        | Groq        | Paid/Limit  | **Fallback**: Logic/Reasoning (demoted from free)     |
| 8 (PAID) | **Claude** (`sonnet-4.5`)         | Anthropic   | Paid        | **Deep Audit**: Architecture reviews                  |
| 9 (PAID) | **Antigravity** (Gemini Pro)      | Google      | Paid        | **Orchestration**: Project-wide coordination          |     |

## Orchestration Pattern

### 1. ASSESS

Determine task complexity:

- **Simple** (1 agent, free): Single-file change, doc update, config fix
- **Standard** (1-2 agents, free): Feature implementation, debug cycle
- **Complex** (parallel agents, free+): Multi-component, research+implement
- **Critical** (paid + review): Architecture decisions, security-sensitive

### 2. SPLIT

Decompose into subtasks:

**Safe to run in PARALLEL:**

- Code implementation + test writing
- Research + documentation drafting
- Multi-server SSH checks (s60, s61, s62 simultaneously)
- Lint + type check + build

**Must run SEQUENTIALLY (gates):**

- Research → Architecture → Implementation
- Build → Test → Deploy
- Analyze → Plan → Execute → Verify

### 3. ASSIGN

Agent routing matrix:

| Task Type         | Agent/Mode               | Model              | Justification Required |
| ----------------- | ------------------------ | ------------------ | ---------------------- |
| Bulk coding       | Kilo `bmad-dev`          | z-ai/glm4.7        | No                     |
| PM/planning       | Cline `bmad-pm`          | minimax:free       | No                     |
| Research/docs     | OpenCode `@researcher`   | groq/llama-3.3-70b | No                     |
| Code review       | OpenCode `@reviewer`     | groq/llama-3.1-8b  | No                     |
| Orchestration     | OpenCode `@orchestrator` | groq/llama-3.3-70b | No                     |
| Large file review | Gemini CLI               | gemini-2.5-flash   | No                     |
| Architecture      | Antigravity              | gemini-2.5-pro     | YES — document why     |
| Complex coding    | OpenCode `@codex`        | openai/o3          | YES — document why     |
| Deep audit        | Claude Code              | claude-sonnet-4-5  | YES — document why     |

### 4. AGGREGATE

Collect outputs using MCP:

| MCP Server            | When to Use                                                        |
| --------------------- | ------------------------------------------------------------------ |
| `memory`              | Persist state between sub-agent sessions                           |
| `redis`               | Coordinate parallel agents, track rate limits                      |
| `bmad-mcp`            | Break features into stories, BMAD phase transitions                |
| `git`                 | Status/diff checks before/after changes                            |
| `github`              | PR creation, issue tracking (affects shared state — confirm first) |
| `fetch`               | Web research (via researcher agent)                                |
| `filesystem-projects` | All file I/O for agent outputs                                     |
| `filesystem-agentic`  | Read framework docs (read-only)                                    |

**BMAD MCP — use when:**

- Starting a new feature that needs user stories
- Transitioning between BMAD phases (research→arch→dev→qa)
- Creating sprint plans

**BMAD MCP — do NOT use when:**

- Making routine code edits
- Fixing single bugs
- Updating documentation

### 5. VALIDATE

After every orchestration run:

```bash
python scripts/verify_agentic_platform.py
```

Expected: exit 0, 0 failures.

## Cost Guard Protocol

Before using any paid model (priority 7-9):

1. Is this task truly beyond groq/llama-3.3-70b capability?
2. Document justification in task notes
3. Log usage in `.kilocode/rules/cost-optimization`
4. Monitor against $20/month cap per provider

## Example: Feature Implementation

```
ASSESS: Multi-file Astro component + i18n + tests → Complex
SPLIT:
  [PARALLEL] research existing patterns + write tests
  [GATE] → implement component
  [PARALLEL] lint + build + a11y check
  [GATE] → visual verify (Playwright)
ASSIGN:
  research: OpenCode @researcher (groq/llama-3.3-70b, free)
  tests: OpenCode @coder (groq/llama-3.3-70b, free)
  implement: Kilo bmad-dev (z-ai/glm4.7, free)
  review: OpenCode @reviewer (groq/llama-3.1-8b, free)
AGGREGATE: memory MCP for shared state
VALIDATE: python scripts/verify_agentic_platform.py
```

## Example: Server Debugging

```
ASSESS: Server s62 unreachable → Complex, server issue
SPLIT:
  [PARALLEL] ssh s60 status check + ssh s62 status check
  [PARALLEL] docker logs + journalctl analysis
  [GATE] → root cause synthesis
  [GATE] → fix (requires human approval per server-preservation rule)
ASSIGN: Kilo sysadmin mode (read-only, all free models)
VALIDATE: evidence/ directory + verify_agentic_platform.py
```

## Handoff Protocol (2026)

When Agent A delegates to Agent B, strict structured communication is required.

### 1. Delegation Format (Agent A Output)

```json
{
  "target_agent": "kilo",
  "task_type": "implementation",
  "context": {
    "goal": "Implement Redis caching",
    "constraints": ["Use marketing_tvoje_info: prefix", "Handle connection errors"]
  },
  "artifacts": ["plans/technical/redis-schema.md", "scripts/verify_redis.py"],
  "acceptance_criteria": ["Passes verify_redis.py", "Handles timeout gracefully"]
}
```

### 2. Acknowledgment (Agent B Start)

Agent B must parse the JSON and confirm:

> "Received delegation for 'Redis caching'. Constraints accepted. Starting work..."

### 3. Completion Handoff (Agent B Output)

```json
{
  "status": "success",
  "outputs": ["src/lib/redis.ts", "tests/redis.test.ts"],
  "verification_result": "All tests passed",
  "next_steps": "Review PR #123"
}
```

### 4. Integration (Agent A Resume)

Agent A validates Agent B's output against acceptance criteria before closing the task.
