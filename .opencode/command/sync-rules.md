---
description: Sync canonical rules to all agent directories after a rule change
subtask: true
model: groq/llama-3.1-8b-instant
---

Sync canonical rules from `.kilocode/rules/` to all agent directories.

## Canonical Rules to Sync

Critical rules that must exist in ALL agent dirs:
- `server-preservation`
- `python-preferred`
- `cost-optimization`
- `bmad-integration`

## Target Directories

| Agent | Rules Dir | Format |
|-------|-----------|--------|
| Kilo Code | `.kilocode/rules/` | plain text (canonical) |
| BMAD Squad | `.agents/rules/` | `.md` files |
| Cline | `.clinerules/skills/` | `.md` with YAML frontmatter |
| Claude Code | N/A (uses @-imports to canonical) | |

## Steps

1. Read each canonical rule from `.kilocode/rules/`
2. Check equivalent exists in `.agents/rules/` and `.clinerules/skills/`
3. If missing or outdated, update the target file
4. Run verify: `python scripts/verify_agentic_platform.py`
5. Report sync status for each rule × directory combination
