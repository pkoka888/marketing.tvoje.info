# Audit Report: [Subject/Component]

**Date**: {{DATE}} **Agent**: {{AGENT_NAME}} ({{MODEL}}) **Framework**: Agentic
Platform 2026

## 1. Executive Summary

_Concise overview of the audit scope, critical findings, and overall health
score (0-100%)._

## 2. Scope & Objectives

- **Target**: [List files, directories, or systems audited]
- **Standards**:
  - [ ] `AGENTS.md` Governance
  - [ ] `opencode.json` Configuration
  - [ ] Redis Namespace Isolation (`marketing_tvoje_info:`)
  - [ ] Project-Specific Rules (`.kilocode/rules/`)

## 3. Critical Findings (Severity: High)

| ID     | Finding             | Impact           | Recommendation |
| ------ | ------------------- | ---------------- | -------------- |
| CRL-01 | [Issue Description] | [Why it matters] | [Fix action]   |

## 4. Compliance Checklist

- [ ] **File Structure**: Follows `.kilocode/` and `.clinerules/` hierarchy?
- [ ] **Naming Conventions**: Kebab-case filenames?
- [ ] **Security**: No hardcoded secrets? Redis auth used?
- [ ] **Model Usage**: Free models prioritized?

## 5. Code Quality & Gaps

### Strengths

- [Item 1]
- [Item 2]

### Weaknesses / Tech Debt

- [Item 1]
- [Item 2]

## 6. Action Plan

1. [Step 1]
2. [Step 2]

## References

### Dependencies

- [GAP_ANALYSIS](GAP_ANALYSIS.md) - Referenced template
- [LINT_FIX_STRATEGY](LINT_FIX_STRATEGY.md) - Referenced template
- [RESEARCH_FINDINGS](RESEARCH_FINDINGS.md) - Referenced template
- [TASK_PLAN](TASK_PLAN.md) - Referenced template
- [TEST_RESULTS](TEST_RESULTS.md) - Referenced template

### Referenced By

- [GAP_ANALYSIS](GAP_ANALYSIS.md) - References this template
- [LINT_FIX_STRATEGY](LINT_FIX_STRATEGY.md) - References this template
- [RESEARCH_FINDINGS](RESEARCH_FINDINGS.md) - References this template

---

## Related Skills & Rules

| Category  | Resource                                                                                            | Description                   |
| --------- | --------------------------------------------------------------------------------------------------- | ----------------------------- |
| **Skill** | [.kilocode/skills/bmad-security-review/SKILL.md](../.kilocode/skills/bmad-security-review/SKILL.md) | Security audit and compliance |
| **Skill** | [.kilocode/skills/debug/SKILL.md](../.kilocode/skills/debug/SKILL.md)                               | Debugging and troubleshooting |
| **Rule**  | [.kilocode/rules/server-preservation](./server-preservation.md)                                     | Server preservation protocols |
