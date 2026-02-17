---
description: Model cost optimization — enforce free-first model routing
---

# Cost Optimization Rule

## Budget (STRICT)

- **Paid**: $20/month max per provider (Gemini, OpenAI)
- **Free**: Unlimited (Kilo grok-code-fast-1:optimized:free, OpenCode big-pickle, OpenRouter minimax)

## Kilo Code Specific Rules

- Use ONLY `x-ai/grok-code-fast-1:optimized:free` for bulk coding
- NEVER use paid models through Kilo Code
- Internal code searches: ALWAYS use grok-code-fast-1:optimized (NOT Gemini - resource conservation)

## Cline-Specific Rules

- Use ONLY OpenRouter free models (minimax/minimax-m2.1:free)
- Daily limit: 50 prompts via OpenRouter free tier
- NEVER use paid models through Cline
- If task exceeds free model capability → delegate to Antigravity

## Routing Matrix

| Task Type         | Agent          | Model                                | Cost          |
| ----------------- | -------------- | ------------------------------------ | ------------- |
| Bulk coding       | Kilo CLI       | x-ai/grok-code-fast-1:optimized:free | Free          |
| Research          | OpenCode       | big-pickle                           | Free          |
| PM/planning       | Cline          | minimax-m2.1:free                    | Free          |
| Architecture      | Antigravity    | Gemini 2.5 Pro (free tier)           | Free          |
| Large file review | Gemini CLI     | gemini-2.5-pro                       | Free (1M/day) |
| Complex coding    | Codex/OpenCode | x-ai/grok-code-fast-1:optimized:free | Free          |

## Resource Conservation (MANDATORY)

- **NEVER use Gemini for internal code searches** (codesearch, grep, file search)
- Use `x-ai/grok-code-fast-1:optimized:free` for all internal search operations
- Reserve Gemini 2.5 Pro/Flash for: external web research, complex architecture only

## Kill-Switch

If approaching $20/month on any provider:

1. Stop using paid models immediately
2. Switch all tasks to free alternatives
3. Log in `vscodeportable/research/cost-alerts.md`

## Groq (T4 — Last Resort, Pay-Per-Token)

- **Status**: Last resort ONLY — never primary, never default
- **Cost**: $0.59/$0.79 per 1M tokens (llama-3.3-70b), $0.05/$0.08 (llama-3.1-8b)
- **Rate limits**: 30 RPM, 1K RPD, 100K TPD (llama-3.3-70b)
- **Use when**: T1 free (grok-code-fast-1 + big-pickle) + T2 (Gemini flash) + T3 all fail
- **DO NOT use for**: Bulk coding, docs, testing — use T1 free instead
