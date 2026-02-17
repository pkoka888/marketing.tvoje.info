# Antigravity Agent Alignment Rules

This file defines how the Antigravity (Gemini) orchestrator interacts with subagents (Kilo, Cline) and maintains structural integrity.

## 1. Task Delegation
- **Orchestrator**: Primarily for complex reasoning, planning, and high-level architecture.
- **Kilo**: Primary executor for bulk coding, research, and infrastructure auditing.
- **Cline**: Specialized execution for UI refinement, localized tasks, and OpenRouter-specific model access.

## 2. Resource Access
- Agents MUST use MCP servers defined in `.kilocode/mcp.json`.
- `filesystem-agentic` is READ-ONLY. Do not attempt to write to frameworks/repos outside the project root.

## 3. Structural Enforcement
- Antigravity MUST enforce the `.kilocode/` hierarchy.
- When creating artifacts, ensure they are placed in `<appDataDir>/brain/<conversation-id>`.
- Project plans SHOULD be mirrored or summarized in `plans/agent-shared/` for cross-agent visibility.

## 4. Cost Optimization (STRICT)
- ALWAYS prefer a free model (Kilo z-ai/glm4.7 or OpenRouter minimax-m2.1:free) for non-critical tasks.
- Monitor provider budgets ($20/month per provider).
- Record overage risks in `vscodeportable/research/cost-alerts.md`.

## 5. Verification Protocol
- Standard verification flow: `Research → Plan → Approve → Execute → Validate → Report`.
- Run health checks defined in `.agent/health-checks.yaml` periodically.
