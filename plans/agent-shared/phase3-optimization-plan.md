# Phase 3 Implementation Plan: Optimization & Orchestration

## Goal Description

Optimize the agentic platform model hierarchy for maximum cost-efficiency, implement safe Redis namespace isolation for context caching, and formalize parallel orchestration protocols.

## User Review Required

> [!IMPORTANT]
> **New 7-Layer Model Hierarchy**:
>
> 1. **Gemini CLI** (Gemini 2.5/3 Pro): Primary for high-context / complex logic.
> 2. **OpenCode** (Official Free): Code generation default.
> 3. **Kilo** (`z-ai/glm4.7`): Unlimited free fallback.
> 4. **Cline** (Free Provider): Routine tasks.
> 5. **NVIDIA / OpenRouter** (Free): Additional free tier capacity.
> 6. **OpenAI** (API Key): Only for complex tasks / high-context needs.
> 7. **Groq** (`llama-3.3-70b`): Logic fallback (now paid/limited).

> [!WARNING]
> **Redis Security**: `scripts/verify_redis.py` will now enforce:
>
> - **Authentication**: Password required.
> - **Isolation**: Project-specific key prefix (`marketing_tvoje_info:`) or separate DB index to prevent data collision.
> - **Port Safety**: Default `6379` check + collision detection.

## Proposed Changes

### Strategy & Governance

#### [MODIFY] [AGENTS.md](file:///c:/Users/pavel/projects/marketing.tvoje.info/AGENTS.md)

- Update "Model Priority" section with the new 7-layer hierarchy.
- Update "MCP Server Usage Matrix" with Redis namespace requirements.

#### [MODIFY] [opencode.json](file:///c:/Users/pavel/projects/marketing.tvoje.info/opencode.json)

- Set default model to OpenCode's free tier.
- Add `agent.fallback` configurations for OpenRouter/NVIDIA.

### Infrastructure & Caching

#### [NEW] [scripts/verify_redis.py](file:///c:/Users/pavel/projects/marketing.tvoje.info/scripts/verify_redis.py)

- **Checks**:
  - Connection to `localhost:6379` (or `REDIS_URL`).
  - Auth/Password verification.
  - Write/Read test with `marketing_tvoje_info:test_key`.
  - Check for "noisy neighbors" (keys without prefix).

#### [MODIFY] [PreToolUse Hook]

- Run `verify_redis.py` (cached) and export `REDIS_PREFIX="marketing_tvoje_info:"` env var for agents.

### Workflow & Orchestration

#### [MODIFY] [.github/workflows/bmad.yml](file:///c:/Users/pavel/projects/marketing.tvoje.info/.github/workflows/bmad.yml)

- Disable `deploy-production` job (Vercel) to resolve conflict with VPS deployment.

#### [NEW] [user.md](file:///c:/Users/pavel/projects/marketing.tvoje.info/user.md)

- **Prompting Manual**: "How to Orchestrate Parallel Agents".
- **Documentation**: Core project architecture.

#### [NEW] [plans/parallel-orchestration-gap-analysis.md](file:///c:/Users/pavel/projects/marketing.tvoje.info/plans/parallel-orchestration-gap-analysis.md)

- BMAD analysis of current agent framework gaps vs. parallel orchestration goals.

## Verification Plan

### Automated Tests

- `python scripts/verify_redis.py`: Must pass locally (if Docker Redis is up).
- `python scripts/verify_agentic_platform.py`: Must confirm config validity.

### Manual Verification

- Verify `AGENTS.md` reflects the 7-layer hierarchy.
- Confirm `bmad.yml` no longer deploys to Vercel production.
