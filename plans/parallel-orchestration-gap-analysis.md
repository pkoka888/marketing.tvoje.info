# Parallel Orchestration Gap Analysis

## Goal

Achieve fully autonomous parallel execution of sub-agents (Kilo, OpenCode, Cline) orchestrated by Antigravity (Gemini Pro), using Redis for state coordination and a 7-layer model hierarchy.

## Current State Analysis (Phase 3 Start)

### ✅ Strengths

- **Governance**: `AGENTS.md` and `opencode.json` are aligned with 2026 standards.
- **Model Hierarchy**: 7-layer priority (Gemini/Free first) is defined.
- **Infrastructure**: Redis verification script and hooks are implemented.
- **Agent Definitions**: BMAD squad and OpenCode agents are defined.

### ⚠️ Gaps (To Be Addressed)

#### 1. Lack of "Swarm" Runner

- **Issue**: We have `orchestrator-parallel.md` (workflow/doc) but no executable script to _spawn_ these agents in parallel.
- **Risk**: Orchestration remains manual (User copy-pasting instructions).
- **Solution**: Need a `scripts/swarm_runner.py` or `kilo run swarm` capability that can spin up multiple CLI sessions (e.g., `cline --task "..."` or `opencode --task "..."`) in background threads/processes.

#### 2. Redis State Schema

- **Issue**: We verify Redis exists, but we haven't defined the _schema_ for inter-agent communication.
- **Risk**: Agents might overwrite each other's data even with namespaces if keys aren't structured (e.g., `task:123:status`).
- **Solution**: Define a JSON schema for `marketing_tvoje_info:shared_state` in `.kilocode/rules/memory-bank/agents-state.md`.

#### 3. Sub-Agent Feedback Loop

- **Issue**: If Kilo fails a task, how does Antigravity know?
- **Risk**: Silent failures in background agents.
- **Solution**: Agents must write strict status logs to `plans/agent-shared/` or update Redis keys that the Orchestrator monitors.

## Action Plan (Next Parallel Plan)

1.  **Define Shared State Schema**: Create strict JSON structure for Redis keys.
2.  **Create Swarm CLI**: e.g., `python scripts/orchestrate.py --plan phase3.md`.
3.  **Implement Status Reporting**: Agents write `completion.json` at end of task.
