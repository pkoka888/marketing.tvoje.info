---
description: Plan watcher — auto-validate new plans in plans/agent-shared/
---

# Plan Watcher Rule

## Trigger
At the **start of every task**, check `plans/agent-shared/` for:
- New `.md` files (not previously validated)
- Updated plans (modified since last check)

## Validation Steps

For each new/updated plan:

### 1. Format Check
- Has clear title and date
- Uses markdown with proper headings
- Follows `CONVENTIONS.md` naming rules

### 2. Scope Check
- Aligns with `AGENTS.md` agent registry — is the right agent assigned?
- References correct knowledge sources
- No duplicate of existing plan

### 3. BMAD Skill Check
If the plan involves:
- Architecture changes → check for `bmad-architecture-design` skill
- Security changes → check for `bmad-security-review` skill
- Performance work → check for `bmad-performance-optimization` skill
- UX/UI changes → check for `bmad-ux-design` skill
- Test strategy → check for `bmad-test-strategy` skill

Recommend loading the relevant BMAD skill before implementation.

### 4. Safety Check
- No destructive commands without confirmation
- No hardcoded secrets
- Build/test commands present in verification section

## Report
Write validation result to `plans/agent-shared/validation-reports/` as:
```
YYYY-MM-DD-plan-review-{plan-name}.md
```
