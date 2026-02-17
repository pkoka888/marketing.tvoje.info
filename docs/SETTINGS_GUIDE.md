# VS Code & Agent Settings Guide

**Date**: 2026-02-17
**Project**: Marketing Portfolio (marketing.tvoje.info)

---

## Overview

This document describes the VS Code and agent configuration for the project, aligned with 2026 best practices for AI-driven development.

---

## VS Code Settings

### Location: `.vscode/settings.json`

**Key Features**:

- **ESLint** enabled with TypeScript and Astro support
- **TypeScript** configured with project SDK
- **Prettier** as default formatter for all languages
- **Git visibility** enabled (`.git` not hidden)
- **Telemetry disabled** for privacy
- **File associations** for project-specific files (YAML, MD, AGENTS.md)

### Settings Categories

| Category   | Settings                        | Purpose                  |
| ---------- | ------------------------------- | ------------------------ |
| Editor     | formatOnSave, codeActionsOnSave | Auto-format on save      |
| ESLint     | validate array                  | TypeScript/Astro linting |
| TypeScript | tsdk                            | Project TypeScript SDK   |
| Prettier   | defaultFormatter                | Consistent formatting    |
| Search     | exclude patterns                | Faster search            |

---

## Agent Configurations

### `.agent/agents.yaml`

BMAD-aligned agent definitions:

| Agent          | Model             | Purpose         |
| -------------- | ----------------- | --------------- |
| bmad-analyst   | z-ai/glm4.7       | Market research |
| bmad-architect | gemini-2.5-pro    | System design   |
| bmad-dev       | z-ai/glm4.7       | Implementation  |
| bmad-pm        | minimax-m2.1:free | Sprint planning |
| bmad-qa        | z-ai/glm4.7       | Testing         |
| bmad-ux        | gemini-2.5-pro    | Design          |

### `.claude/settings.json`

Claude Code hooks configured:

- PreToolUse hook for rule synchronization
- Bash permissions for npm, python, git

### `.gemini/settings.json`

Context files for Gemini CLI:

- `GEMINI.md`
- `.agent/agents.yaml`
- `.agent/health-checks.yaml`
- `_bmad/bmm/config.yaml`

---

## Git Ignore Strategy

### Kept in Repo (Tracked)

| Pattern                 | Reason        |
| ----------------------- | ------------- |
| `.vscode/settings.json` | Team settings |
| `.vscode/tasks.json`    | Shared tasks  |
| `test-results/`         | CI visibility |
| `playwright-report/`    | CI visibility |

### Excluded (Local Only)

| Pattern         | Reason       |
| --------------- | ------------ |
| `.env`          | Secrets      |
| `node_modules/` | Dependencies |
| `dist/`         | Build output |
| `credentials/`  | Secrets      |

---

## Best Practices Applied

1. **Free Models First**: All BMAD agents use free models (Kilo, OpenRouter)
2. **Privacy**: Telemetry disabled, secrets in .env
3. **Team Collaboration**: Shared VS Code settings
4. **CI/CD Visibility**: Test results tracked
5. **Agent Alignment**: All agents follow BMAD methodology

---

## Verification Commands

```bash
# VS Code Settings
cat .vscode/settings.json | python -m json.tool > /dev/null && echo "Valid JSON"

# Agent Config
python -c "import yaml; yaml.safe_load(open('.agent/agents.yaml'))" && echo "Valid YAML"

# Platform Verification
python scripts/verify_agentic_platform.py
```
