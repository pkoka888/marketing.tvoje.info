# LiteLLM Gap Analysis — Provider Priority Rewrite

**Date**: 2026-02-17
**Agents**: A (Config Auditor) + B (Provider Research)
**Status**: Complete → Remediation in progress

---

## Executive Summary

**Root issue**: Groq (pay-per-token, T4) configured as PRIMARY throughout platform. Must be LAST RESORT.
**Scope**: 4 files, 29+ model references to update.
**Risk**: Every task currently routes to paid Groq before free alternatives.

---

## New Provider Priority Matrix

| Tier                | Provider                    | Models                                                     | Cost          |
| ------------------- | --------------------------- | ---------------------------------------------------------- | ------------- |
| **T1 FREE**         | OpenRouter                  | minimax/minimax-m2.1:free, z-ai/glm4.7, gemma-3-1b-it:free | $0            |
| **T2 FREE COMPLEX** | Gemini API                  | gemini-2.5-flash                                           | $0/1M TPD     |
| **T3 PAID CAPPED**  | OpenAI/Anthropic/Gemini Pro | gpt-4o-mini, claude-haiku-4-5, gemini-2.5-pro              | $20/mo cap    |
| **T4 LAST RESORT**  | Groq                        | llama-3.3-70b-versatile, llama-3.1-8b-instant              | pay-per-token |

---

## File-by-File Gap Analysis

### 1. `litellm/proxy_config.yaml`

**Current**: Groq first, 8 Groq models, 1 outdated Gemini, outdated Claude/OpenAI
**Required**: Full rewrite — T1 free first, T4 Groq last

| Section        | Current                               | Required                               |
| -------------- | ------------------------------------- | -------------------------------------- |
| First model    | `groq/llama-3.3-70b-versatile`        | `openrouter/minimax/minimax-m2.1:free` |
| Gemini         | `gemini-1.5-flash` (3 gen old)        | `gemini/gemini-2.5-flash`              |
| Claude         | `claude-3-haiku-20240307` (7 ver old) | `anthropic/claude-haiku-4-5-20251001`  |
| OpenAI         | `gpt-4o-mini`, `gpt-4o` (outdated)    | `gpt-4o-mini` (keep), `gpt-4.1-mini`   |
| Fallback chain | Groq→Groq→OpenAI                      | T1→T2→T3→T4                            |
| T1 models      | None defined                          | 3 OpenRouter free models               |

### 2. `opencode.json`

**Current**: Global model + all 8 agents = Groq primary
**Required**: OpenRouter free primary, Groq removed

| Field                      | Current                        | Required                               |
| -------------------------- | ------------------------------ | -------------------------------------- |
| `model` (global)           | `groq/llama-3.3-70b-versatile` | `openrouter/minimax/minimax-m2.1:free` |
| `small_model`              | `groq/llama-3.1-8b-instant`    | `openrouter/google/gemma-3-1b-it:free` |
| `agent.coder.model`        | `groq/llama-3.3-70b-versatile` | `openrouter/minimax/minimax-m2.1:free` |
| `agent.researcher.model`   | `groq/llama-3.3-70b-versatile` | `openrouter/z-ai/glm4.7`               |
| `agent.reviewer.model`     | `groq/llama-3.1-8b-instant`    | `openrouter/google/gemma-3-1b-it:free` |
| `agent.orchestrator.model` | `groq/llama-3.3-70b-versatile` | `openrouter/minimax/minimax-m2.1:free` |
| `agent.architect.model`    | `groq/llama-3.3-70b-versatile` | `openrouter/minimax/minimax-m2.1:free` |
| `agent.codex.model`        | `groq/llama-3.3-70b-versatile` | `openrouter/z-ai/glm4.7`               |
| `agent.fallback.model`     | `groq/llama-3.3-70b-versatile` | `openrouter/minimax/minimax-m2.1:free` |

### 3. `.agents/squad.json`

**Current**: 5/7 agents use Groq primary
**Required**: OpenRouter free primary

| Agent            | Current                           | Required                               |
| ---------------- | --------------------------------- | -------------------------------------- |
| roadmap-keeper   | `groq/llama-3.3-70b-versatile`    | `openrouter/minimax/minimax-m2.1:free` |
| cicd-engineer    | `groq/llama-3.3-70b-versatile`    | `openrouter/minimax/minimax-m2.1:free` |
| docs-maintainer  | `groq/llama-3.1-8b-instant`       | `openrouter/google/gemma-3-1b-it:free` |
| debugger         | `groq/llama-3.3-70b-versatile`    | `openrouter/minimax/minimax-m2.1:free` |
| template-factory | `groq/llama-3.3-70b-versatile`    | `openrouter/minimax/minimax-m2.1:free` |
| auditor          | `gemini/gemini-2-5-pro-exp-06-05` | `gemini/gemini-2.5-pro` (stable)       |
| budget.groq      | `<$10/month`                      | T4 pay-per-token (last resort only)    |

### 4. Cost-Optimization Rules (all 4 files)

**Gap**: Groq not mentioned at all. Agents have no guidance on T4 routing.
**Required**: Add T4 Groq section to canonical `.kilocode/rules/cost-optimization` + all mirrors.

---

## Provider Verification (Agent B Findings)

| Provider           | Planned ID                             | Verified Status                        |
| ------------------ | -------------------------------------- | -------------------------------------- |
| OpenRouter minimax | `openrouter/minimax/minimax-m2.1:free` | ✅ Available                           |
| OpenRouter z-ai    | `openrouter/z-ai/glm4.7`               | ✅ Available (glm-4.7 via NVIDIA NIM)  |
| Gemini flash       | `gemini/gemini-2.5-flash`              | ✅ Available, 250 RPD free tier        |
| Imagen-3           | `gemini/imagen-3`                      | ⚠️ Vertex AI only, NOT Gemini API      |
| Claude Haiku 4.5   | `anthropic/claude-haiku-4-5-20251001`  | ✅ Confirmed                           |
| gpt-4o-mini        | `openai/gpt-4o-mini`                   | ⚠️ May be superseded by `gpt-4.1-mini` |

**Imagen-3 note**: Cannot be used via `gemini/imagen-3` in LiteLLM. Requires Vertex AI. Config will note this limitation.

---

## Remediation Checklist

- [x] Gap analysis written (this file)
- [ ] `litellm/proxy_config.yaml` rewritten
- [ ] `opencode.json` updated (9 model fields)
- [ ] `.agents/squad.json` updated (5 agents + budget section)
- [ ] `.kilocode/rules/cost-optimization` + 3 mirrors updated
- [ ] `python scripts/verify_agentic_platform.py` → exit 0
