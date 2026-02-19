---
description: Create new plans using standardized templates with automatic keyword-based template selection
subtask: true
model: big-pickle
---

Create a new plan using standardized templates with automatic keyword-based template selection.

## Options

- `--list`, `-l`: List all available templates
- `--template <name>`, `-t <name>`: Select a specific template
- `--auto <text>`, `-a <text>`: Auto-select template based on task description
- `--help`, `-h`: Show help message

## Usage

List templates:
!`python scripts/new_plan.py --list`

Auto-select by description:
!`python scripts/new_plan.py --auto "audit redis security"`
!`python scripts/new_plan.py -a "test QA results"`

Select specific template:
!`python scripts/new_plan.py --template TASK_PLAN`

## Templates

| Template | Trigger Keywords |
|----------|-----------------|
| AUDIT_REPORT | audit, security, compliance |
| TASK_PLAN | plan, implement, story |
| TEST_RESULTS | test, QA, results |
| LINT_FIX_STRATEGY | lint, eslint, fix |
| GAP_ANALYSIS | gap, missing, analysis |
| RESEARCH_FINDINGS | research, investigate |

## Examples

### Auto-select for security audit
Input: `!`python scripts/new_plan.py --auto "audit redis security"`
Output: Selects AUDIT_REPORT template

### Auto-select for implementation plan
Input: `!`python scripts/new_plan.py --auto "implement new feature"`
Output: Selects TASK_PLAN template

### List all templates
Input: `!`python scripts/new_plan.py --list`
Output: Shows all available templates with descriptions
