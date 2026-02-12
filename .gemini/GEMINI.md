# Project: marketing.tvoje.info

## Project Context
- **Type**: Astro + TypeScript marketing portfolio
- **Deployment**: VPS s62 via GitHub Actions (Tailscale primary, SSH fallback)
- **URL**: https://portfolio.tvoje.info

## BMAD Integration (v6.0.0-Beta.8)
This project uses the BMAD-METHOD for structured agent workflows.
- **Agents**: `_bmad/bmm/agents/` (analyst, architect, dev, pm, qa, sm, ux, solo)
- **Workflows**: `_bmad/bmm/workflows/` (25 workflows across 4 phases)
- **Config**: `_bmad/bmm/config.yaml` — ALWAYS load on agent activation
- **Output**: `_bmad-output/` for planning and implementation artifacts

## Agent Registry
- **Kilo Code**: `.kilocodemodes` — 9 custom modes (8 BMAD + server-monitor)
- **Cline**: `.clinerules/` — 10 rule files (bmad-integration, cost-optimization, etc.)
- **Antigravity**: `.agent/agents.yaml` — full agent registry with delegation targets
- **Health Checks**: `.agent/health-checks.yaml` — 15 checks, IDE startup trigger

## Cost Rules
See global `~/.gemini/GEMINI.md` Section 6 for full rules. Summary:
- **Paid** ($20/mo each): Gemini 2.5 Pro (this agent), OpenAI o3/GPT-4.1 (Codex)
- **Free**: Kilo z-ai/glm4.7, OpenRouter minimax-m2.1:free, Gemini CLI flash (1M/day)
- **Never exceed** $20/month per provider

## Server Infrastructure
- **s60**: Hub/Backup (2.5T, 94Gi RAM) — Ansible, rsnapshot
- **s61**: Production (237G, 23Gi RAM) — PrestaShop, okamih.cz ⚠️88% disk
- **s62**: Marketing (93G, 3.8Gi RAM) — this project, Traefik, borgmatic
- **Evidence**: `vscodeportable/servers/evidence.md`
- **SSH**: Tailscale VPN + port forwarding (s60:2260, s61:2261, s62:2262)

## MCP Servers Available
Configured in `.kilocode/mcp.json`:
- `filesystem-projects` — R/W to ~/projects/
- `filesystem-agentic` — Read-only agentic repos
- `memory` — In-memory knowledge graph
- `git` — Git operations
- `github` — Issues, PRs, code search
- `time` — Timezone operations
- `fetch` — HTTP requests

## Research & Knowledge
- `vscodeportable/research/` — dated research documents
- `vscodeportable/servers/` — server evidence knowledge base
- `.kilocode/knowledge/` — Kilo-indexed knowledge

## Script Policy: Python-First
**ALWAYS use Python (.py) for scripts** — never .sh, .ps1, .cmd, .bat.
- Policy: `.agent/python-policy.md` and `.clinerules/python-preferred.md`
- Evidence scripts: `vscodeportable/servers/scripts/collect_evidence.py`
- Exceptions: CI/CD YAML, npm lifecycle, system binaries

## Key Files
| File | Purpose |
|------|---------|
| `.env` | Non-secret project config only (secrets in GH Secrets) |
| `.kilocodemodes` | Kilo custom modes (BMAD + operational) |
| `.clinerules/` | Cline agent rules (10 files) |
| `.agent/agents.yaml` | Antigravity agent registry |
| `.agent/health-checks.yaml` | Background agent health checks |
| `.agent/flows/server_ops.py` | LangGraph server operations |
| `.vscode/tasks.json` | IDE startup tasks (health check) |
| `_bmad/` | BMAD-METHOD v6 installation |
