# Plan: Parallel Orchestration for E2E Testing & CI/CD

**Date**: 2026-02-17
**Agent**: Antigravity (Orchestrator)
**Status**: Planning

## 1. Goal

Implement a robust, authorized E2E testing strategy using parallel agent orchestration to fix current configuration gaps and integrate with CI/CD, adhering to 2026 best practices (Critical Path focus, Blocking CI).

## 2. Problem Analysis & Research Findings

### Problems

- **E2E Tests**: Point to old URL (`portfolio.tvoje.info`) instead of `marketing.tvoje.info`.
- **CI/CD**: Missing E2E integration; no blocking gate for deployments.
- **Linting**: False positives for Astro files.

### 2026 Best Practices (Research)

- **Scope**: Focus on **Critical Paths** (login, checkout, core navigation). avoid "full coverage" to reduce flakiness.
- **CI Strategy**: **Blocking** for critical path tests. Fail build if critical flows break.
- **Frequency**:
  - **On Push**: Fast smoke tests (Critical Path).
  - **On Deploy**: Full regression suite (Staging/Production).

## 3. Implementation Plan (Parallel Orchestration)

We will use the **BMAD** agent structure to parallelize execution where possible.

### Phase 1: Configuration Fixes (Sequential)

_Responsible: `bmad-dev` (or `groq-coder` via `codex` alias)_

1.  **Update E2E Target**:
    - Modify `tests/e2e/live-verification.spec.ts` (or similar) to use `BASE_URL` env var.
    - Set default `BASE_URL = 'https://marketing.tvoje.info'`.
2.  **Linting Fix**:
    - Install `eslint-plugin-astro`.
    - Update `.eslintrc.cjs` to include Astro integration.

### Phase 2: CI/CD Integration (Parallel)

_Responsible: `bmad-dev` / `bmad-architect`_

1.  **Create E2E Workflow (`.github/workflows/e2e.yml`)**:
    - Trigger: `push` (branches) and `workflow_dispatch`.
    - Steps: Install deps -> Build -> Run Playwright (Smoke).
2.  **Update Deploy Workflow (`.github/workflows/deploy.yml`)**:
    - Add "Verify" job after deployment.
    - Run Critical Path tests against live URL.
    - **Blocking**: Fail workflow if tests fail.

### Phase 3: Verification

_Responsible: `bmad-qa` / `server-monitor`_

1.  **Manual Trigger**: Run `npx playwright test` locally against `marketing.tvoje.info`.
2.  **CI Trigger**: Push changes and verify GitHub Actions execution.

## 4. Agent Orchestration

| Agent             | Role      | Task                                                     | Model             |
| ----------------- | --------- | -------------------------------------------------------- | ----------------- |
| **@codex** (Groq) | Dev       | Fix `playwright.config.ts` & `live-verification.spec.ts` | `groq-fast-agent` |
| **@codex** (Groq) | Dev       | Fix ESLint validation for Astro                          | `groq-fast-agent` |
| **@reviewer**     | Architect | Author `.github/workflows/e2e.yml`                       | `llama-3.1-405b`  |

## 5. Verification Commands

```bash
# Local Verification
npm run lint
BASE_URL=https://marketing.tvoje.info npx playwright test

# CI Verification
# (Trigger via git push)
```
