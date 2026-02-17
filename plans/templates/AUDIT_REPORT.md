# Audit Report: [Subject/Component]

**Date**: {{DATE}}
**Agent**: {{AGENT_NAME}} ({{MODEL}})
**Framework**: Agentic Platform 2026

## 1. Executive Summary

_Concise overview of the audit scope, critical findings, and overall health score (0-100%)._

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
