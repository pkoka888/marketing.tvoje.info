---
name: memory-bank
description: Must read this skill at the start of every task to load project context from the Memory Bank.
---

# Memory Bank Skill

The **Memory Bank** is the single source of truth for project context, architectural decisions, and active tasks.

## Core Protocol

1.  **Mandatory Load**: At the start of **EVERY** task, you MUST read the core Memory Bank files.
2.  **Location**: `.kilocode/rules/memory-bank/`
3.  **No Exceptions**: Even if you think you know the context, you must verify against the Memory Bank.

## Instructions

When starting a new task:

1.  List the files in `.kilocode/rules/memory-bank/`.
2.  Read the content of the following **Core Files**:
    - `brief.md` (Project goals)
    - `product.md` (Product vision)
    - `context.md` (Current work focus)
    - `activeContext.md` (if present)
    - `tech.md` (Technology stack)
    - `architecture.md` (System architecture)

## Updates

- If you make significant architectural changes, suggest updating `architecture.md`.
- If you complete a major phase, suggest updating `context.md`.
- **Do not modify** the Memory Bank without explicit user approval or a clear mandate.

## Deprecation Notice

- Do **NOT** use "Antigravity Knowledge" or other disparate context sources if they conflict with the Memory Bank.
- The Memory Bank supersedes all other documentation.
