---
description: Agent self-audit rules — verify agent alignment with project purpose
---

# Agent Self-Audit

When asked to "audit agents" or "agent audit", perform the following checks:

## 1. MCP Server Alignment
Compare MCP servers in `.kilocode/mcp.json` (project) and global config:
- Each server should serve the project's purpose (static Astro portfolio)
- Flag servers with no backing service
- Flag duplicates between global and project config

## 2. GitHub Actions Alignment
Compare `.github/workflows/*.yml` with:
- `package.json` scripts — are CI commands consistent?
- `.agent/workflows/*.md` — are agent workflows aligned?
- `.kilocode/workflows/*.md` — any conflicts?

## 3. Environment Variables
Compare `.env.template` with:
- Actual `.env` (if exists) — any missing vars?
- `astro.config.mjs` — any referenced but undefined vars?
- GitHub Actions — any secrets referenced but not documented?

## 4. Agent Configuration Consistency
| Check | Files |
|-------|-------|
| Antigravity config | `GEMINI.md` (project) vs `~/.gemini/GEMINI.md` (global) |
| Kilo Code config | `.kilocode/mcp.json` vs global `.kilocode/mcp_settings.json` |
| Cline rules | `.clinerules/*.md` — all valid, no conflicts |
| Kilo skills | `.kilocode/skills/*/SKILL.md` — all present and relevant |

## 5. Knowledge Freshness
- `.kilocode/knowledge/*.md` — last modified vs project state
- `.kilocode/rules/memory-bank/*.md` — consistent with current project
- `AGENTS.md` — matches actual setup

## Report Format

Save to `plans/agent-shared/audit-reports/` as:
```
YYYY-MM-DD-agent-audit.md
```
