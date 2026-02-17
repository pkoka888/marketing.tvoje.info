---
description: Model cost optimization — enforce free-first model routing
---

# Cost Optimization Rule

## Budget (STRICT)

- **Paid**: $20/month max per provider (Gemini, OpenAI)
- **Free**: Unlimited (Kilo z-ai/glm4.7, OpenRouter minimax, Gemini CLI flash)

## Cline-Specific Rules

- Use ONLY OpenRouter free models (minimax/minimax-m2.1:free)
- Daily limit: 50 prompts via OpenRouter free tier
- NEVER use paid models through Cline
- If task exceeds free model capability → delegate to Antigravity

## Routing Matrix

| Task Type         | Agent          | Model             | Cost          |
| ----------------- | -------------- | ----------------- | ------------- |
| Bulk coding       | Kilo CLI       | z-ai/glm4.7       | Free          |
| Research          | Kilo CLI       | z-ai/glm4.7       | Free          |
| PM/planning       | Cline          | minimax-m2.1:free | Free          |
| Architecture      | Antigravity    | Gemini 2.5 Pro    | Paid          |
| Large file review | Gemini CLI     | gemini-2.5-flash  | Free (1M/day) |
| Complex coding    | Codex/OpenCode | o3/GPT-4.1        | Paid          |

## Kill-Switch

If approaching $20/month on any provider:

1. Stop using paid models immediately
2. Switch all tasks to free alternatives
3. Log in `vscodeportable/research/cost-alerts.md`
