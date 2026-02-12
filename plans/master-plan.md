# Project Master Plan: Marketing Portfolio & Agentic Infrastructure

**Date:** 2026-02-12
**Status:** Active/Consolidated

## Executive Summary
This Master Plan consolidates the **MVP Implementation** (Features) and **Infrastructure Optimization** (Agents/Tools) into a single roadmap. It reflects the completed audit of Redis, BMAD, and Memory Bank systems.

## 1. Infrastructure & Governance (Foundation)

### Status: ✅ Mostly Complete
| Component | Status | Config Location | Notes |
|-----------|--------|-----------------|-------|
| **Redis** | ✅ Active | `.kilocode/mcp.json` | Running via `shared-redis`, connected via MCP. |
| **BMAD** | ✅ Integrated | `_bmad/README.md` | Agents installed. `bmad-mcp` configured. |
| **Memory Bank** | ⚠️ Sync Ready | `.kilocode/rules/memory-bank` | `scripts/sync-memory-bank.js` created for validation. |
| **MCP Servers** | ✅ Configured | `.kilocode/mcp.json` | Redis, BMAD, Git, Filesystem enabled. |

### Next Steps (Infrastructure)
- [ ] Run `node scripts/sync-memory-bank.js` to validate current state.
- [ ] Execute `npx bmad-method update` if needed to refresh agent templates.

## 2. MVP Implementation (Features)

**Source:** `plans/plan-e-mvp-implementation.md` (Phase 5)

### Phase 1: Template Import (Status: Pending)
- Import `bmad-skills` (testing, performance, security) via Keeper.
- Import `rules-code` (nodejs, astro).

### Phase 2: Content Population (Status: Next Up)
- **Projects**: Cloud Migration, AI Implementation, DevOps Transformation.
- **Service Pages**: DevOps Consulting, AI Integration.
- **i18n**: Translations for CS/EN toggles.

### Phase 3: Features & Polish
- Dark Mode / Language Toggle.
- Formspree Integration.
- Lighthouse Score Optimization (>95).

## 3. Operational Workflows

### Agent Usage
- **Antigravity**: Orchestrator (Plans & Infrastructure).
- **Kilo/Cline**: Builders (Features & Content).
    - Use `rules-architect` for planning.
    - Use `rules-code` for implementation.
- **BMAD**: Methodology (via `npx bmad-method` or MCP).

## 4. Immediate Action Items
1. **Validate Infrastructure**: Run `scripts/sync-memory-bank.js` and fix any reported issues.
2. **Execute Phase 1 (MVP)**: Use Keeper agent (Kilo) to import skills.
3. **Start Phase 2 (Content)**: Begin content population in `src/content/`.
