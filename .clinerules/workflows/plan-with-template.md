# Plan with Template

## Purpose

Generate task plans using standardized templates from `plans/templates/`.

## Usage

### List Available Templates

```bash
python scripts/new_plan.py --list
```

### Select Specific Template

```bash
python scripts/new_plan.py --template TASK_PLAN "Implement feature X"
```

### Auto-Select by Keywords

```bash
python scripts/new_plan.py --auto "audit redis security"
```

## Templates

| Template          | Trigger Keywords            |
| ----------------- | --------------------------- |
| AUDIT_REPORT      | audit, security, compliance |
| TASK_PLAN         | plan, implement, story      |
| RESEARCH_FINDINGS | research, investigate       |
| GAP_ANALYSIS      | gap, missing, analysis      |
| TEST_RESULTS      | test, QA, results           |
| LINT_FIX_STRATEGY | lint, eslint, fix           |

## Integration

This workflow integrates with the BMAD workflow system:

1. Agent detects task type from keywords
2. Auto-selects appropriate template
3. Generates artifact using template structure
4. Outputs to `_bmad-output/` directory
