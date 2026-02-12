---
description: Keeper onboard — bootstrap a project with good practices from template
---

# Keeper Onboard Rule

## Trigger
When user says: `Keeper onboard {project-name}` or `Keeper setup {project-name}`

## Onboarding Process

### 1. Pre-flight Check
- Verify project exists in `C:\Users\pavel\projects\{project-name}`
- Check if project already has `.kilocode/` (partial setup)
- Read project's `package.json` / `pyproject.toml` to detect tech stack

### 2. Copy Baseline Configs (skip if exists)

From `projects/template/`:
```
.kilocode/rules/           → if not present
.kilocode/rules-architect/  → if not present
.kilocode/rules-code/       → if not present
.kilocode/rules-debug/      → if not present
.kilocode/rules-ask/        → if not present
.kilocode/workflows/        → if not present
.kilocode/knowledge/        → if not present
```

From `vscodeportable/`:
```
.clinerules/                → copy global + project-specific
GEMINI.md                   → project-level variant
CONVENTIONS.md              → reference copy
.pre-commit-config.yaml     → adapt to project tech stack
scripts/validate.sh         → copy
```

Custom files to generate:
```
AGENTS.md                   → generate from AGENTS.md template
plans/agent-shared/         → create 3 subdirs
```

### 3. Fix Known Bugs
- **Check for duplicate frontmatter** in all `.kilocode/rules-*/` files
- Remove any second `---` block with `alwaysApply: true`
- Delete junk files: `mydatabase.db`, `redis.json`, `*-security.json`

### 4. Adapt to Tech Stack

| Tech Stack | Additions |
|-----------|-----------|
| Astro | Copy `astro-portfolio` skill |
| Node.js | Copy `nodejs-runtime` debug rule, vitest config |
| Python | Adapt pre-commit to Python (black, ruff) |
| Docker | Add docker-compose validation workflow |

### 5. Validation
Run: `scripts/validate.sh quick`
Report result to user.

## Safety
- NEVER overwrite existing project source code
- NEVER overwrite customized rules (check git status first)
- Always show diff of what will be copied before proceeding
- Require user confirmation for first-time onboarding
