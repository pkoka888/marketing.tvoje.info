# Provider Models Quick Reference

**Last Updated**: 2026-02-13
**Purpose**: Quick reference for all LLM provider models used in this project

---

## Provider Priority

| Priority | Provider         | Use Case                            | Cost      |
| -------- | ---------------- | ----------------------------------- | --------- |
| 1        | Groq (LiteLLM)   | Primary - Fast inference, free tier | Free/Paid |
| 2        | Kilo Code (z-ai) | Fallback - Built-in free model      | Free      |
| 3        | OpenRouter       | Tertiary - Multiple providers       | Free/Paid |

---

## Groq Models (Primary)

### Verified Models (2026-02-13)

| Model ID                  | Context | Speed   | Pricing ($/1M tokens) | Rate Limits (Dev)                   |
| ------------------------- | ------- | ------- | --------------------- | ----------------------------------- |
| `llama-3.3-70b-versatile` | 131K    | 280 T/s | $0.59 / $0.79         | 30 RPM, 1K RPD, 12K TPM, 100K TPD   |
| `llama-3.1-8b-instant`    | 131K    | 560 T/s | $0.05 / $0.08         | 30 RPM, 14.4K RPD, 6K TPM, 500K TPD |
| `llama-3.1-70b-versatile` | 131K    | 280 T/s | $0.59 / $0.79         | 30 RPM, 1K RPD, 12K TPM, 100K TPD   |

### New Models (Experimental)

| Model ID              | Context | Use Case                  | Rate Limits                      |
| --------------------- | ------- | ------------------------- | -------------------------------- |
| `openai/gpt-oss-120b` | TBD     | Large OpenAI-compatible   | 30 RPM, 1K RPD, 8K TPM, 200K TPD |
| `openai/gpt-oss-20b`  | TBD     | Smaller OpenAI-compatible | TBD                              |
| `groq/compound`       | TBD     | Agentic AI with tools     | 30 RPM, 250 RPD, 70K TPM         |
| `groq/compound-mini`  | TBD     | Lightweight agentic       | TBD                              |

### Recommended Use Cases

| Task              | Recommended Model         | Reason                    |
| ----------------- | ------------------------- | ------------------------- |
| Complex reasoning | `llama-3.3-70b-versatile` | Quality, function calling |
| Simple tasks      | `llama-3.1-8b-instant`    | Fast, cheap               |
| Agentic workflows | `groq/compound`           | Built-in tool use         |
| High volume       | `llama-3.1-8b-instant`    | 500K TPD limit            |

---

## Kilo Code Fallback (z-ai)

### Built-in Model

| Model ID          | Provider  | Use Case               | Cost |
| ----------------- | --------- | ---------------------- | ---- |
| `z-ai/glm4.7`     | Kilo Code | Fallback for all tasks | Free |
| `z-ai/glm-5:free` | Kilo Code | Current default        | Free |

### When to Use

- Groq rate limit exceeded
- Groq API unavailable
- No API key configured
- Cost-sensitive operations

---

## OpenRouter (Tertiary)

### Free Models

| Model ID                                | Provider | Context | Cost |
| --------------------------------------- | -------- | ------- | ---- |
| `minimax/minimax-m2.1:free`             | MiniMax  | 1M      | Free |
| `google/gemma-3-1b-it:free`             | Google   | 32K     | Free |
| `meta-llama/llama-3.2-3b-instruct:free` | Meta     | 128K    | Free |

### Rate Limits (Free Tier)

- Daily limit: 50 prompts per day
- Request timeout: 120 seconds

---

## LiteLLM Proxy Configuration

### Endpoint

```
http://localhost:4000/v1/chat/completions
```

### Example Request

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "groq/llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Configuration File

See: `litellm/proxy_config.yaml`

---

## Rate Limit Handling

### Groq Rate Limit Errors

| Error Code                   | Description      | Action                   |
| ---------------------------- | ---------------- | ------------------------ |
| `rate_limit_exceeded`        | RPM/RPD exceeded | Wait 60s or switch model |
| `tokens_per_minute_exceeded` | TPM exceeded     | Wait 60s                 |
| `tokens_per_day_exceeded`    | TPD exceeded     | Switch to fallback       |

### Fallback Strategy

```python
# Pseudocode for rate limit handling
if error.code == "rate_limit_exceeded":
    if model == "llama-3.3-70b-versatile":
        fallback = "llama-3.1-8b-instant"  # Higher RPD limit
    else:
        fallback = "z-ai/glm4.7"  # Kilo Code fallback
```

---

## Cost Optimization

### Free Tier Strategy

1. **Primary**: Groq free tier (Developer Plan)
2. **Fallback**: Kilo Code z-ai/glm4.7 (unlimited free)
3. **Tertiary**: OpenRouter free models (50/day limit)

### Paid Usage (When Needed)

| Provider | Budget    | Models                  |
| -------- | --------- | ----------------------- |
| Groq     | $20/month | llama-3.3-70b-versatile |
| Gemini   | $20/month | gemini-2.5-pro          |
| OpenAI   | $20/month | gpt-4o                  |

### Kill-Switch

If approaching $20/month on any provider:

1. Stop using paid models immediately
2. Switch all tasks to free alternatives
3. Log in `vscodeportable/research/cost-alerts.md`

---

## Model Selection Matrix

| Task Type         | Primary                   | Fallback                  | Tertiary   |
| ----------------- | ------------------------- | ------------------------- | ---------- |
| Bulk coding       | `llama-3.1-8b-instant`    | `z-ai/glm4.7`             | OpenRouter |
| Research          | `llama-3.3-70b-versatile` | `z-ai/glm4.7`             | OpenRouter |
| Architecture      | `llama-3.3-70b-versatile` | Gemini 2.5 Pro            | -          |
| PM/planning       | `llama-3.1-8b-instant`    | `minimax-m2.1:free`       | -          |
| Complex reasoning | `llama-3.3-70b-versatile` | Gemini 2.5 Pro            | -          |
| Agentic workflows | `groq/compound`           | `llama-3.3-70b-versatile` | -          |

---

## Verification Status

| Model                     | Last Verified | Status          |
| ------------------------- | ------------- | --------------- |
| `llama-3.3-70b-versatile` | 2026-02-13    | ✅ Verified     |
| `llama-3.1-8b-instant`    | 2026-02-13    | ✅ Verified     |
| `llama-3.1-70b-versatile` | 2026-02-13    | ✅ Verified     |
| `openai/gpt-oss-120b`     | 2026-02-13    | ⚠️ Experimental |
| `groq/compound`           | 2026-02-13    | ⚠️ Experimental |
| `z-ai/glm4.7`             | 2026-02-13    | ✅ Verified     |

---

## Related Files

- **LiteLLM Config**: `litellm/proxy_config.yaml`
- **Provider Fallback Skill**: `.kilocode/skills/provider-fallback/SKILL.md`
- **Error Reference**: `.kilocode/skills/provider-fallback/REFERENCE.md`
- **Cost Optimization**: `.kilocode/rules-code/cost-optimization.md`

---

_This file should be updated when new models are added or rate limits change._
