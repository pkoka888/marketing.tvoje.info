# marketing.tvoje.info — Antigravity Agent Instructions

## Project Context
Astro 5.0 portfolio site showcasing DevOps & AI expertise. Bilingual CS/EN. Tailwind CSS 3.4, TypeScript, Vercel deployment.

## Agent Behavior

### Plans & Artifacts
- Write actionable plans to `plans/agent-shared/` (not just `~/.gemini/antigravity/brain/`)
- Read shared knowledge from `AGENTS.md` (project root) and `.kilocode/knowledge/`
- Cross-reference `.clinerules/` for project-specific coding standards

### Model Preference
- Primary: `MiniMax-M2.1:free`
- Complex tasks: Use configured default model
- Always prefer the most cost-effective model that can handle the task

### Coordination Protocol
- Before implementing, check `plans/agent-shared/` for existing plans from other agents
- After completing work, update `plans/agent-shared/` with a summary report
- Reference `AGENTS.md` agent registry for role boundaries

### Verification
- Always run `npm run build` after code changes
- Run `npm run test` if test files were modified
- Check `.kilocode/knowledge/project-architecture.md` for component inventory

## Key Directories
| Path | Purpose |
|------|---------|
| `src/` | Astro source (components, pages, layouts, i18n) |
| `.kilocode/` | Kilo Code config (rules, skills, workflows, knowledge) |
| `.agent/workflows/` | Antigravity workflows (dev, build, test, deploy, lint, content) |
| `.clinerules/` | Cline project rules |
| `plans/agent-shared/` | Cross-agent plans and reports |
| `tests/` | Vitest test suite |
