# Agent Templates Index

This directory contains reusable templates for AI agents working on this project.

## Templates

### PRD (Product Requirements Document)

| File                  | Description        | When to Use                      |
| --------------------- | ------------------ | -------------------------------- |
| `prd/standard-prd.md` | Basic PRD template | Simple features, quick docs      |
| `prd/detailed-prd.md` | Comprehensive PRD  | Complex features, team alignment |

### Marketing

| File                 | Description    | When to Use             |
| -------------------- | -------------- | ----------------------- |
| `marketing-brief.md` | Campaign brief | New marketing campaigns |

### CI/CD

| File                         | Description             | When to Use           |
| ---------------------------- | ----------------------- | --------------------- |
| `ci-cd/pipeline-template.md` | GitHub Actions + Vercel | Setting up deployment |

### Debug

| File                     | Description           | When to Use            |
| ------------------------ | --------------------- | ---------------------- |
| `debug/common-errors.md` | Common errors & fixes | Troubleshooting issues |

### Audit

| File                      | Description        | When to Use       |
| ------------------------- | ------------------ | ----------------- |
| `audit/security-audit.md` | Security checklist | Pre-launch audits |

### Feature

| File                         | Description          | When to Use           |
| ---------------------------- | -------------------- | --------------------- |
| `feature/feature-request.md` | Feature request form | New feature proposals |

### Sprint

| File                        | Description     | When to Use           |
| --------------------------- | --------------- | --------------------- |
| `sprint/sprint-planning.md` | Sprint planning | Agile sprint planning |

### Progress

| File                          | Description   | When to Use            |
| ----------------------------- | ------------- | ---------------------- |
| `progress/progress-report.md` | Status report | Weekly/monthly updates |

---

## How to Use

### For OpenCode

Reference in your prompt:

```
Use the PRD template at .agents/templates/prd/detailed-prd.md
```

### For Antigravity / Other Agents

Copy relevant template to project or reference directly.

---

## BMAD Squad

See `.agents/squad.json` for the 7-agent squad configuration:

- ROADMAP-KEEPER
- CI/CD-ENGINEER
- DOCS-MAINTAINER
- AUDITOR
- DEBUGGER
- TEMPLATE-FACTORY
- ORCHESTRATOR

---

## GitHub Workflows

See `.github/workflows/bmad.yml` for the main CI/CD pipeline.

---

## Sources

Templates adapted from:

- `C:\Users\pavel\vscodeportable\library\coding-templates\claude-code-skill-factory\`
- `C:\Users\pavel\vscodeportable\library\ai-starter-templates\rulebook-ai\`
- BMAD orchestration best practices
