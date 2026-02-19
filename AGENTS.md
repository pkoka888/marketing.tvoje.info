# AGENTS.md

This file provides the official instructions and structural standards for all AI agents working with this repository. It is the source of truth for the **Unified Agentic Platform 2026**.

## Agent Frameworks (01-Agent-Frameworks)

These agents are based on the official frameworks located in `vscodeportable/agentic/01-agent-frameworks/`:

- **Cline**: `cline/` & `cline_docs/`
- **Kilo Code**: `kilocode/`
- **Antigravity**: Custom orchestrator (You)

---

## Unified Project Structure

### 0. Artifact Standards (MANDATORY)

All agents **MUST** use the standardized templates in `plans/templates/` for complex outputs:

| Template          | Triggers                    | Skills                      |
| ----------------- | --------------------------- | --------------------------- |
| AUDIT_REPORT      | audit, security, compliance | bmad-security-review, debug |
| GAP_ANALYSIS      | gap, missing, analysis      | bmad-discovery-research     |
| RESEARCH_FINDINGS | research, investigate       | bmad-discovery-research     |
| TASK_PLAN         | plan, implement, story      | bmad-story-planning         |
| TEST_RESULTS      | test, QA, results           | bmad-test-strategy, debug   |
| LINT_FIX_STRATEGY | lint, eslint, fix           | debug, accessibility-wcag   |

### 1. Cline Configuration (`.clinerules/`)

All agentic configurations MUST follow this unified hierarchy:

- **`skills/`**: Atomic markdown rules (e.g., `astro.md`, `general.md`).
- **`workflows/`**: Process-oriented guides (e.g., `build.md`, `deploy.md`).
- **`hooks/`**: Python audit scripts (`TaskStart`, `PreToolUse`) — write to `plans/agent-shared/task_audits.log`.

### 2. Kilo Code Configuration (`.kilocode/`)

- **`rules/`**: Canonical rule store. One file per mode: `rules-architect`, `rules-code`, `rules-debug`, `rules-keeper`, `rules-server-monitor`, `rules-sysadmin`. **This is the source of truth.**
- **`skills/`**: Capability definitions (`SKILL.md`, `WORKFLOW.md`, `CHECKLIST.md`).
- **`workflows/`**: Specialized task flows.
- **`agents/`**: JSON definitions for Kilo CLI agents (e.g., `sysadmin.json`). Prompt paths use `file://` and must point to `.kilocode/rules/`.
- **`knowledge/`**: Curated project-long knowledge.
- **`.kilocodemodes`**: YAML extension mode definitions.

### 3. Antigravity Configuration (`.agent/`)

- **`agents.yaml`**: Primary agent registry and delegation rules. Rule `source:` paths must reference existing files.
- **`health-checks.yaml`**: System monitoring and background tasks.
- **`workflows/`**: 10 core workflows mirroring `.clinerules/workflows/` — kept in sync, not consolidated.

### 4. Claude Code Configuration (`.claude/`)

- **`settings.json`**: Project-level permissions and hook wiring.
- **`hooks/pre_tool_use.py`**: Cross-agent sync enforcement — injects sync reminder when writing to any agent config dir.
- **`commands/audit.md`**: `/audit` slash command for platform integrity check.
- **`CLAUDE.md`** (project root): Auto-loaded instructions; uses `@file` imports for canonical rules.

### 5. BMAD Squad Configuration (`.agents/`)

- **`squad.json`**: Squad agent definitions (roadmap-keeper, cicd-engineer, docs-maintainer, auditor, debugger, template-factory, orchestrator).
- **`rules/`**: Agent-specific rules mirroring canonical `.kilocode/rules/` content.

### 6. Gemini-CLI Configuration (`.gemini/`)

- **`rules/`**: Rule files for Gemini-CLI sessions, mirroring canonical `.kilocode/rules/` content.

### 7. OpenCode Configuration (`opencode.json` + `.opencode/`)

- **`opencode.json`**: Project-level config — free-model-first (`big-pickle`), 8 MCP servers, 6 agent model overrides.
- **`.opencode/agent/`**: Sub-agent persona definitions (`coder.md`, `researcher.md`, `reviewer.md`, `orchestrator.md`, `architect.md`, `codex.md`).
- **`.opencode/command/`**: Slash commands (`audit.md`, `deploy.md`, `sync-rules.md`, `free-status.md`).
- **`.opencode/skill/`**: Skill definitions (`astro-portfolio/SKILL.md`, `server-ops/SKILL.md`).
- **`.opencode/workflows/`**: OpenCode-specific workflow adaptations.
- Reads `AGENTS.md` natively at startup.
- Sub-agents invoked with `@agent-name` syntax; inherit shared context window.

---

## Parallel Orchestration Protocol (Free-Model-First)

All agents follow the **ASSESS→SPLIT→ASSIGN→AGGREGATE→VALIDATE** pattern.

### Model Priority Order

| Priority | Model                      | Provider     | Limit      | Use For                                                 |
| -------- | -------------------------- | ------------ | ---------- | ------------------------------------------------------- |
| 1 (FREE) | **Kilo Code**              | xAI          | Unlimited  | **Bulk Coding**: `x-ai/grok-code-fast-1:optimized:free` |
| 2 (FREE) | **OpenCode**               | OpenCode Zen | Unlimited  | **Standard**: `big-pickle`                              |
| 3 (FREE) | **Cline**                  | OpenRouter   | Unlimited  | **Routine**: `minimax-m2.1:free`                        |
| 4 (FREE) | **Gemini CLI**             | Google       | 1M TPD     | **Analysis**: `gemini-2.5-pro` (free tier)              |
| 5 (PAID) | **OpenAI** (`o3`)          | OpenAI       | $20 cap    | **Complex**: Hard algorithms, critical reasoning only   |
| 6 (PAID) | **Groq** (`llama-3.3-70b`) | Groq         | Paid/Limit | **Fallback**: Logic/Reasoning (Last Resort)             |

**Cost guard**: Log all paid usage in `.kilocode/rules/cost-optimization`. Cap: $20/month per provider.

### Parallel-Safe vs Sequential Gates

**Safe to run in PARALLEL**: code + tests, research + docs, multi-server SSH checks, lint + build + a11y

**Must run SEQUENTIALLY (gates)**: research → architecture → implementation → build → test → deploy

### MCP Server Usage Matrix

| MCP                   | Use For                                                  | Skip When                                                                 |
| --------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------- |
| `memory`              | Cross-session state, knowledge graph                     | Ephemeral one-off data                                                    |
| `redis`               | Parallel agent coordination, rate limit tracking         | Simple single-agent tasks. **MUST USE NAMESPACE `marketing_tvoje_info:`** |
| `bmad-mcp`            | Feature stories, BMAD phase transitions, sprint planning | Routine code edits, single bugs                                           |
| `git`                 | Status/diff/log before and after changes                 | (always useful, low cost)                                                 |
| `github`              | PR creation, issue tracking                              | Confirm first — affects shared state                                      |
| `fetch`               | Web research (via researcher agent)                      | Authenticated/private URLs                                                |
| `filesystem-projects` | All file I/O for agent outputs                           | (always available)                                                        |
| `filesystem-agentic`  | Read framework docs from vscodeportable                  | Writing (read-only)                                                       |

### Agent Routing Matrix

| Task Type       | Agent                  | Model                                | Justification       |
| --------------- | ---------------------- | ------------------------------------ | ------------------- |
| Bulk coding     | Kilo `bmad-dev`        | x-ai/grok-code-fast-1:optimized:free | Free, unlimited     |
| Research        | OpenCode `@researcher` | big-pickle                           | Free, 200K context  |
| Code review     | OpenCode `@reviewer`   | x-ai/grok-code-fast-1:optimized:free | Free, unlimited     |
| PM/planning     | Cline `bmad-pm`        | minimax-m2.1:free                    | Free                |
| Server ops      | Kilo `sysadmin`        | minimax-m2.1:free                    | Read-only, free     |
| Large context   | Gemini CLI             | gemini-2.5-pro                       | Free, 1M tokens     |
| Architecture    | Antigravity            | gemini-2.5-pro                       | PAID — document why |
| Hard algorithms | OpenCode `@codex`      | x-ai/grok-code-fast-1:optimized:free | Free - use first    |
| Deep audit      | Claude Code            | claude-sonnet-4-5                    | PAID — document why |

See `.clinerules/workflows/orchestrate-parallel.md` for full canonical workflow.

---

## Cross-Agent Rule Synchronization Protocol (MANDATORY)

**Canonical store**: `.kilocode/rules/`

When ANY agent modifies rule files in any agent config directory:

1. **READ** the canonical version from `.kilocode/rules/` first
2. **PROPAGATE** changes to equivalent files in ALL other agent rule dirs:
   - `.agents/rules/` (BMAD Squad)
   - `.clinerules/skills/` (Cline)
   - `.gemini/rules/` (Gemini-CLI)
3. **RUN** `python scripts/verify_agentic_platform.py` after changes — must exit 0
4. Hooks in `.clinerules/hooks/PreToolUse` and `.claude/hooks/pre_tool_use.py` enforce this at write-time

**Critical rules that must exist in ALL agent rule directories:**

| Rule                     | Purpose                                           |
| ------------------------ | ------------------------------------------------- |
| `server-preservation`    | No cleanup/delete ops on servers without approval |
| `python-preferred`       | Python over shell scripts for automation          |
| `cost-optimization`      | Free models first; $20/month paid budget cap      |
| `bmad-integration`       | BMAD workflow protocol and agent detection        |
| `plan-approval-required` | Cost control for expensive AI models              |

---

## Agent Personas & Protocols (2026 STRICT)

| Feature             | Standard                                                                  |
| :------------------ | :------------------------------------------------------------------------ |
| **Brevity**         | Soul of wit. No filler, no hand-holding. Summarize when needed.           |
| **Evidence-First**  | No adjectives (e.g., no "blazingly fast"). Use numbers and data.          |
| **Gender-Specific** | Refer to Cline and automation agents as **'him'**.                        |
| **Delegation**      | Routing: Kilo (Free) for bulk coding, Antigravity (Pro) for architecture. |

---

## Integrated Tooling & Commands

```bash
npm install                           # Install dependencies
npm run dev                           # Start dev server (localhost:4321)
npm run build                         # Production build to dist/
npm run test                          # Run Vitest suite
npx kilo agents list                  # Verify Kilo CLI agent discovery
python scripts/verify_agentic_platform.py  # Full cross-agent integrity check
```

---

## Verification Protocol

Before finalization, all agents must fulfill the **Unified Verification Plan**:

1. Run `python scripts/verify_agentic_platform.py` — must exit 0 (includes broken ref, parity, and Claude Code checks).
2. Run `python scripts/validate_kilo_configs.py` (YAML/JSON schema check).
3. Verify `CLAUDE.md` is present at project root and `.claude/settings.json` is configured.
4. Ensure both EN and CS translations are consistent.

---

## Strategic Knowledge Locations

- **`AGENTS.md`**: Platform governance and repository mapping.
- **`CLAUDE.md`**: Claude Code per-project instructions (auto-loaded).
- **`kilocode.json`**: Project-level model and token governance.
- **`.kilocode/rules/`**: Canonical rule store — source of truth for all agents.
- **`.kilocode/knowledge/`**: Technical architecture and research index.
- **`.kilocode/rules/memory-bank/`**: Persistent project memory (brief, context, architecture, tech, servers).

---

> [!IMPORTANT]
> Change the persona to **Senior Model-driven Architect**. Be proactive, be succinct, and always refer to official repositories in `vscodeportable\agentic\` when researching framework capabilities.
