# User Manual: Agentic Platform 2026

## 1. Quick Start

- **Bulk Coding**: Use Kilo `z-ai/glm4.7` (Free/Unlimited).
- **High Context / Research**: Use Gemini CLI (1M tokens free).
- **Architecture / Orchestration**: Use Antigravity (Gemini Pro).
- **Complex Logic**: Use OpenCode (`@codex`) with OpenAI o3 (Paid).

## 2. Orchestration & Parallel Agents

How to run agents in parallel for maximum efficiency:

### The "Swarms" Approach

When you have a complex feature, do NOT ask one agent to do it all.

1. **Architect** (Antigravity): "Plan the feature. Break it into 3 sub-tasks: Frontend, Backend, Database."
2. **Assign**:
   - "Kilo, take the Database schema task."
   - "OpenCode, take the Backend API task."
   - "Cline, take the Frontend Component task."
3. **Review**:
   - "OpenCode `@reviewer`, review the PRs from Kilo and Cline."
4. **Merge**:
   - "Antigravity, verify integration and merge."

### Prompting Strategies

**Bad**: "Fix the bugs in the app."
**Good**: "Scan the `src/libs` folder for TypeScript errors. Fix only the `any` type usage issues. Do not change logic."

**Bad**: "Make it look better."
**Good**: "Apply the 'Neon Future' design language from `design-system.md` to the `Hero` component. Use Tailwind classes `bg-slate-900` and `text-teal-400`."

## 3. Advanced Prompting Strategies (2026)

### Parallel Swarms

Use this pattern to orchestrate multiple agents simultaneously:

> **"Run 3 agents in PARALLEL:**
>
> - **@researcher**: Research Tailwind CSS 4.0 best practices for 'Glassmorphism'.
> - **@codex**: Audit `src/components/Hero.astro` for current implementation gaps.
> - **@reviewer**: Identify accessibility (a11y) issues in the current Hero.
>   **AGGREGATE**: Summarize findings into a single `plans/implementation/hero-upgrade.md`."

### Complex Feature Flow (BMAD)

> "**Use BMAD flow**: Analyst → Architect → Dev → QA.
>
> 1. **Analyst**: Create requirements in `plans/reqs/feature.md`.
> 2. **Architect**: Design system in `plans/arch/feature.md`.
> 3. **Dev**: Implement.
> 4. **QA**: Write tests.
>    **GATE**: Each phase must PASS validation before proceeding."

## 4. Core Documentation & Architecture

- **Tech Stack**: Astro 5.0, Tailwind 4.0, TypeScript.
- **Infrastructure**: VPS (s60/s62) via SSH.
- **Knowledge Base**: `.kilocode/knowledge/`
- **Rules**: `.kilocode/rules/` (Canonical Source).

## 4. Git & Selective Commits

### Atomic Commits Principle

Each commit should represent ONE logical change that can be built/tested independently.

### Commit Categories (Conventional Commits)

```
feat:     New feature
fix:      Bug fix
docs:     Documentation only
refactor: Code restructuring (no feature change)
chore:    Maintenance, deps, configs
test:     Adding tests
```

### Selective Commit Workflow

```bash
# 1. Check what changed
git status

# 2. Stage specific files (not all)
git add src/components/Hero.astro
git add docs/Hero-design.md

# 3. Commit with scope
git commit -m "feat(hero): add glassmorphism effect"

# 4. Remaining changes - new commit
git add src/styles/
git commit -m "chore(styles): add glassmorphism utilities"
```

### When to Split vs Bundle

| Scenario                                  | Action                                    |
| ----------------------------------------- | ----------------------------------------- |
| Related changes (feature + tests + docs)  | **Bundle** in one commit                  |
| Independent changes (fix A + feature B)   | **Split** into separate commits           |
| Platform configs (agent rules, workflows) | **Bundle** together (maintains integrity) |
| Bugfix + unrelated feature                | **Split** - bugfix first, feature second  |

### Verification Before Commit

Always run before committing:

```bash
npm run build    # Must pass
npm run typecheck  # Must pass
git diff --stat  # Review what changed
```

## 5. Troubleshooting

- **"Agent Context Full"**: Switch to Gemini CLI or start a new session.
- **"Redis Connection Fail"**: Run `python scripts/verify_redis.py`.
- **"Deployment Failed"**: Check GitHub Actions logs. If Vercel fails, ignore (we use VPS).

## 6. Parallel Task Orchestration

### ASSESS → SPLIT → ASSIGN → AGGREGATE → VALIDATE

**Pattern** (2026 best practice):

1. **ASSESS**: Is task simple/standard/complex?
2. **SPLIT**: Can parts run in parallel?
3. **ASSIGN**: Route to free models first
4. **AGGREGATE**: Collect results via MCP
5. **VALIDATE**: Run verification scripts

### Parallel-Safe Tasks

- Code + Tests (can run together)
- Research + Documentation
- Multi-server SSH checks
- Lint + Build + Typecheck

### Sequential Gates (Must wait)

- Research → Architecture → Implementation
- Build → Test → Deploy

### Example: Multi-Section Website Update

```
ASSESS: Homepage needs 4 new sections → Complex
SPLIT:
  [PARALLEL]
    - Research: Best practices for each section
    - Audit: Current component implementations
    - Tests: Write Playwright tests
  [GATE] → Implement all sections
  [PARALLEL]
    - Lint check
    - Build check
    - Accessibility check
ASSIGN:
  - Research: @researcher (groq/free)
  - Audit: @codex (groq/free)
  - Tests: @reviewer (groq/free)
AGGREGATE: Memory MCP for shared context
VALIDATE: npm run build && npm run typecheck
```

## 7. Deployment

- **Production**: Push to `main` triggers `deploy.yml` (VPS).
- **Preview**: Open a PR triggers `deploy-preview` (Vercel).
