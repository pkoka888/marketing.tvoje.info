# Test Results: [Suite Name]

**Date**: {{DATE}} **Agent**: {{AGENT_NAME}} ({{MODEL}}) **Command**:
`{{COMMAND}}`

## 1. Summary

| Metric   | Value        |
| -------- | ------------ |
| Total    | {{TOTAL}}    |
| Passed   | {{PASSED}}   |
| Failed   | {{FAILED}}   |
| Skipped  | {{SKIPPED}}  |
| Duration | {{DURATION}} |

## 2. Results by Category

| Category     | Pass | Fail | Notes   |
| ------------ | ---- | ---- | ------- |
| [Category A] | 0/0  | 0    | [Notes] |

## 3. Failures

| Test        | Error       | Root Cause | Fix      |
| ----------- | ----------- | ---------- | -------- |
| [test_name] | [error_msg] | [cause]    | [action] |

## 4. Environment

- **OS**: {{OS}}
- **Runtime**: {{RUNTIME}}
- **Config**: {{CONFIG_FILE}}
- **API Keys**: [List which keys are set/missing]

## 5. Artifacts

- JSON results: `{{JSON_PATH}}`
- Logs: `{{LOG_PATH}}`

## References

### Dependencies

- [LINT_FIX_STRATEGY](LINT_FIX_STRATEGY.md) - Referenced template

### Referenced By

- [AUDIT_REPORT](AUDIT_REPORT.md) - References this template
- [LINT_FIX_STRATEGY](LINT_FIX_STRATEGY.md) - References this template

---

## Related Skills & Rules

| Category  | Resource                                                                                        | Description                      |
| --------- | ----------------------------------------------------------------------------------------------- | -------------------------------- |
| **Skill** | [.kilocode/skills/bmad-test-strategy/SKILL.md](../.kilocode/skills/bmad-test-strategy/SKILL.md) | Test strategy and ATDD scenarios |
| **Skill** | [.kilocode/skills/debug/SKILL.md](../.kilocode/skills/debug/SKILL.md)                           | Systematic debugging protocol    |
| **Rule**  | [.kilocode/rules/bmad-integration](./bmad-integration.md)                                       | BMAD workflow protocol           |
