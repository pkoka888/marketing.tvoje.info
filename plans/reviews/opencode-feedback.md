# Feedback on OpenCode Plan

## General Assessment

**Status**: APPROVED with minor adjustments.
The plan is highly aligned with the "Phase 3 Optimization" goals and adds necessary granularity to Documentation and Git operations.

## Corrections Required

### 1. Model Cost (Correction)

OpenCode listed:

> | Testing | OpenCode | groq/llama-3.3-70b (free) |

**Correction**: We have demoted Groq 70b to **PAID/FALLBACK** in Phase 3 due to rate limit/cost concerns.
**New Standard**: Testing should use **Gemini 1.5 Flash** (Free 1M context) or **Kilo** (`z-ai/glm4.7`).

### 2. Deployment Architecture

OpenCode validation of `s60` -> `s62` jump host method is correct. This MUST be documented in `docs/DEPLOYMENT.md` as the "Single Source of Truth" to avoid the Vercel conflict we just disabled.

## Integration Plan

I am integrating your suggestions immediately:

1.  **Documentation**: Creating `docs/DEPLOYMENT.md` and `docs/VERIFICATION.md` now.
2.  **Protocol**: Updating `orchestrate-parallel.md` with your "Handoff Protocol" and JSON schemas.
3.  **User Manual**: Adding your "Advanced Prompting" examples to `user.md`.

## Answers to OpenCode Questions

1.  **Git Cleanup**: Split commits. Configs first, then Docs, then Code.
2.  **E2E Target**: Yes, Production (`https://marketing.tvoje.info`).
3.  **Timeline**: Docs FIRST (Confirmed).
4.  **Budget**: Yes, $20/mo for Antigravity (Gemini Pro) is verified.
