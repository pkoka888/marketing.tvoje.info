---
name: memory-bank
description: Must read this skill at the start of every task to load project context from the Memory Bank.
---

# Memory Bank Skill

The **Memory Bank** is the single source of truth for project context, architectural decisions, and active tasks.

## Core Protocol

## 1. Load Memory Bank

At the start of **EVERY** task, you must read the following core files to establish context:

1.  `QUICK_REFERENCE.md` (Critical constraints & map)
2.  `context.md` (Active task status)
3.  `brief.md` (Project goals - Optional if well understood)

**DO NOT** load `product.md` unless specifically working on feature planning.
**DO NOT** search for archived files (`tech.md`, `architecture.md`) unless you hit a specific blocker.

```xml
<memory_bank_core>
<file path=".kilocode/rules/memory-bank/QUICK_REFERENCE.md" />
<file path=".kilocode/rules/memory-bank/context.md" />
</memory_bank_core>
```

## Updates

- If you make significant architectural changes, suggest updating `architecture.md`.
- If you complete a major phase, suggest updating `context.md`.
- **Do not modify** the Memory Bank without explicit user approval or a clear mandate.

## Deprecation Notice

- Do **NOT** use "Antigravity Knowledge" or other disparate context sources if they conflict with the Memory Bank.
- The Memory Bank supersedes all other documentation.
