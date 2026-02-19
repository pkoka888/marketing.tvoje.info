# Memory Bank - Agent Instructions

**Core Protocol**:

1. **Load**: `QUICK_REFERENCE.md` + `context.md` (Required). `brief.md` (Optional).
2. **Product**: Load `product.md` ONLY for feature work.
3. **Archive**: Do NOT load files from `.archive/` unless stuck.

**Goal**: Minimize context usage (keep < 10KB).

**Updates**:

- Use `QUICK_REFERENCE.md` for tech stack/rules.
- Update `context.md` at start/end of tasks.

---

## DO NOT LOAD

These files are archived or too large:

- tech.md
- architecture.md
- servers.md
- agents-state.md
- verification-history.md
- tasks-queue.md

Research docs (moved to `.kilocode/knowledge/`):

- MEMORY_BANK_AUTOMATION.md
- MEMORY_BANK_BEST_PRACTICES.md

---

## For Specific Tasks

| Task           | Also Load           |
| -------------- | ------------------- |
| Code changes   | AGENTS.md           |
| Config updates | opencode.json       |
| Plans          | plans/PHASE\*.md    |
| Reports        | plans/reports/\*.md |

---

## If Context Exceeds Limit

1. Load only QUICK_REFERENCE.md
2. Load specific plan file needed
3. Use AGENTS.md for rules
