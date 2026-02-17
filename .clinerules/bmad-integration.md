---
description: BMAD v6 integration — agent activation and workflow routing
---

# BMAD v6 Integration Rule

## BMAD Structure (v6.0.0-Beta.8)

| Path                    | Contents                                                                  |
| ----------------------- | ------------------------------------------------------------------------- |
| `_bmad/bmm/config.yaml` | Project config (user_name, language, output_folder)                       |
| `_bmad/bmm/agents/`     | 8 compiled agent personas (analyst, architect, dev, pm, qa, sm, ux, solo) |
| `_bmad/bmm/workflows/`  | 25 workflows (analysis → planning → solutioning → implementation)         |
| `_bmad/bmm/data/`       | Templates and schemas                                                     |
| `_bmad/bmm/teams/`      | Team configurations                                                       |
| `_bmad/core/`           | Core agents, workflows, tasks                                             |
| `_bmad-output/`         | Generated artifacts output                                                |

## Agent Activation

On any BMAD-related task:

1. **Load** `_bmad/bmm/config.yaml` first (get {user_name}, {communication_language})
2. **Select agent** from `_bmad/bmm/agents/` matching the task type
3. **Follow** the agent's activation steps exactly as written
4. **Output** artifacts to `_bmad-output/` (planning or implementation)

## Auto-Detection Keywords

| Keyword Pattern                    | Agent               | Workflow Phase   |
| ---------------------------------- | ------------------- | ---------------- |
| market research, competitive, SWOT | analyst             | 1-analysis       |
| architecture, system design, API   | architect           | 2-planning       |
| implement, code, build, dev story  | dev                 | 4-implementation |
| sprint, backlog, story planning    | pm                  | 3-solutioning    |
| test, QA, validation, quality      | qa                  | 4-implementation |
| UX, wireframe, user flow, design   | ux-designer         | 2-planning       |
| rapid prototype, solo, quick       | quick-flow-solo-dev | all phases       |

## Delegation Rules (Cost-Aware)

| Agent     | Preferred CLI | Model             | Cost |
| --------- | ------------- | ----------------- | ---- |
| analyst   | Kilo CLI      | z-ai/glm4.7       | Free |
| architect | Antigravity   | Gemini 2.5 Pro    | Paid |
| dev       | Kilo CLI      | z-ai/glm4.7       | Free |
| pm        | Cline CLI     | minimax-m2.1:free | Free |
| qa        | Kilo CLI      | z-ai/glm4.7       | Free |
| ux        | Antigravity   | Gemini 2.5 Pro    | Paid |

## BMAD Update Detection

After `npx bmad-method install --action update`:

- Re-check `_bmad/bmm/agents/` for new/changed agents
- Update `.kilocodemodes` if new agents added
- Update `.agent/agents.yaml` for Antigravity alignment
- Health check: `.agent/health-checks.yaml` validates BMAD state
