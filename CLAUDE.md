# marketing.tvoje.info — Claude Code Instructions

## Agent Platform Governance
@AGENTS.md

## Mandatory Reading at Task Start
@.kilocode/rules/rules-architect
@.kilocode/rules/rules-code
@.kilocode/rules/plan-approval-required
@.clinerules/skills/general.md
@.clinerules/skills/kilo-structure.md

## Cross-Agent Rule Synchronization Protocol (MANDATORY)

When modifying ANY file in `.kilocode/`, `.clinerules/`, `.agent/`, `.agents/`, or `.claude/`:

1. **READ** the canonical version in `.kilocode/rules/` FIRST
2. After change, **UPDATE** equivalent files in ALL other agent dirs
3. **RUN** `python scripts/verify_agentic_platform.py` to confirm integrity
4. Canonical store: `.kilocode/rules/` | Governance doc: `AGENTS.md`

## Active Agent Namespaces

| Dir | Agent | Config Files |
|-----|-------|-------------|
| `.agent/` | Antigravity (Gemini orchestrator) | agents.yaml, kilo-alignment.md |
| `.agents/` | BMAD Squad (OpenCode/Groq) | squad.json, rules/ |
| `.claude/` | Claude Code (this agent) | settings.json, hooks/, commands/ |
| `.clinerules/` | Cline | skills/, hooks/, workflows/ |
| `.gemini/` | Gemini-CLI | rules/, settings |
| `.kilocode/` | Kilo Code | agents/, skills/, rules/, workflows/ |

## Cost Routing

- **Free first**: Kilo (z-ai/glm4.7), OpenRouter (minimax-m2.1:free), Gemini-CLI flash
- **Paid budget**: $20/month per provider (Gemini Pro, OpenAI)
- **Kill-switch**: If approaching budget, immediately switch to free models

## 2026 Core Protocol

- **Brevity**: No filler, no hand-holding
- **Evidence-First**: Numbers and data over adjectives
- **Python Preferred**: Python over shell scripts for automation
- **Preservation**: NEVER cleanup server operations without explicit approval
