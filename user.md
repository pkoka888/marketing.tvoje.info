# User Manual: Agentic Platform 2026

## 1. Quick Start - Model Selection

| Task              | Tool       | Model                             | Command            |
| ----------------- | ---------- | --------------------------------- | ------------------ |
| Bulk Coding       | Kilo       | `grok-code-fast-1:optimized:free` | Use Kilo extension |
| Standard Tasks    | OpenCode   | `big-pickle`                      | `opencode` CLI     |
| Routine Fixes     | Cline      | `minimax-m2.1:free`               | Cmd+K in VS Code   |
| Complex Analysis  | Gemini CLI | `gemini-2.5-pro`                  | `gemini` CLI       |
| External Research | Gemini     | `gemini-2.5-flash`                | Conserve quota!    |

**Resource Rule**: NEVER use Gemini for internal searches. Use grok-code-fast-1.

## 2. Orchestration & Parallel Agents

### Quick Agent Templates

Use these simplified prompts:

#### Run Research (OpenCode @researcher)

```
@researcher Research [TOPIC] in [FILES/FOLDER]. Focus on [WHAT TO FIND]. Deliver: [OUTPUT FORMAT]
```

#### Run Code Audit (OpenCode @codex)

```
@codex Audit [FILE/FOLDER] for [ISSUE TYPE]. Do NOT fix - just identify. Deliver: findings list
```

#### Run Code Review (OpenCode @reviewer)

```
@reviewer Review [FILE] for [CRITERIA]. Focus on [WHAT TO CHECK]. Deliver: approved/issues
```

#### Run Multiple in Parallel

```
[PARALLEL EXECUTION]
@researcher: Research [topic]
@codex: Audit [file]
@reviewer: Review [file]
AGGREGATE: Combine findings into [OUTPUT FILE]
```

#### Use BMAD Flow

```
Use BMAD flow:
1. Analyst: Research [requirements] → plans/reqs/[feature].md
2. Architect: Design [solution] → plans/arch/[feature].md
3. Dev: Implement
4. QA: Test
GATE: Each phase passes before next
```

### Prompting Strategies

**Bad**: "Fix the bugs in the app."
**Good**: "Scan `src/libs/` for TypeScript errors. Fix only `any` type issues. Do NOT change logic."

**Bad**: "Make it look better."
**Good**: "Apply Neon Future design from `design-system.md` to Hero. Use Tailwind `bg-slate-900 text-teal-400`."

---

## 3. Advanced Prompting Strategies (2026)

### Parallel Swarms

Use this pattern:

```
Run 3 agents in PARALLEL:
- @researcher: Research [topic]
- @codex: Audit [file]
- @reviewer: Identify a11y issues
AGGREGATE: Combine into plans/hero-upgrade.md
```

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

| Issue                   | Solution                                                     |
| ----------------------- | ------------------------------------------------------------ |
| "Agent Context Full"    | Switch to Gemini CLI or start new session                    |
| "Redis Connection Fail" | Run `python scripts/verify_redis.py`                         |
| "Deployment Failed"     | Check GitHub Actions logs. Vercel fail = ignore (we use VPS) |
| Model Not Found         | Check `.kilocode/models.json` for valid model names          |
| MCP Server Error        | Run `python scripts/verify_agentic_platform.py`              |

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
