---
description: Show remaining free-tier capacity for all AI providers
subtask: true
model: groq/llama-3.1-8b-instant
---

Report current free-tier AI model capacity status.

## Free Tier Limits

| Provider | Model | Daily Limit | Notes |
|----------|-------|-------------|-------|
| Groq | llama-3.3-70b-versatile | 100K tokens/day | Best quality free |
| Groq | llama-3.1-8b-instant | 500K tokens/day | Fast bulk tasks |
| Groq | compound-beta | ~2M tokens/day | Agentic workflows |
| OpenRouter | minimax/minimax-m2.1:free | 50 req/day | Low-context tasks |
| Gemini CLI | gemini-2.5-flash | 1M tokens/day | Large context |
| Kilo | z-ai/glm4.7 | Unlimited | Always-on fallback |

## Instructions

Check `.kilocode/rules/cost-optimization` for current budget status.
Report which free models are recommended for today's tasks.
Flag if any paid model usage is approaching the $20/month cap.
