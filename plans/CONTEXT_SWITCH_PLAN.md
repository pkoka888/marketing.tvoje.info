# Context Switch Plan: From Marketing to Automatizace

**Target**: `automatizace.expc.cz`
**Source**: `marketing.tvoje.info` (Template Origin)

## 1. Context Injection

- The Orchestrator for `automatizace` must adopt the "DevOps & AI Automation" persona.
- **Action**: Import `plans/optimization-plan.md` and `plan-e-mvp-implementation.md` (from Marketing archive) into `automatizace`'s active plans.

## 2. Infrastructure Separation

- **Redis**:
  - Current: `shared-redis` container.
  - Action: Configure a separate Redis logical database (e.g., DB 1) or key prefix (`auto:`) for `automatizace`.
  - Update `.kilocode/mcp.json` in `automatizace` to point to the specific Redis instance/DB.

## 3. Content Restoration

- **Codebase**: Ensure `src/content` and `src/components` in `automatizace` reflect the "DevOps" branding (restoring what was "cleaned" from Marketing).
- **Knowledge**:
  - `knowledge/project-architecture.md`: Ensure "DevOps Consulting" remains the core service.

## 4. Orchestrator Handoff

- This document serves as the trigger for the `automatizace` Orchestrator to:
  1. Scan `vscodeportable/research` for "CLI Orchestration" and "Server Ops".
  2. Implement the "Hub-and-Spoke" architecture defined in `2026-02-11-cli-orchestration.md`.
