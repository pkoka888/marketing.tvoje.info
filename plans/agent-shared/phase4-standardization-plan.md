# Phase 4 Implementation Plan: Standardization & Audit

## Goal Description

Standardize agent outputs using 2026-compliant Markdown templates for Audits, Research, and Planning. Use these templates to facilitate a comprehensive deep-dive audit by Kilo Code.

## User Review Required

> [!TIP]
> **standardization**: We are moving away from ad-hoc text outputs to structured artifacts (`.md` templates). This ensures that when Kilo, OpenCode, or Cline run a task, the output is machine-readable by Antigravity (me).

## Proposed Changes

### Template Standardization

#### [NEW] `plans/templates/` Hierarchy

- `AUDIT_REPORT.md`: For deep-dive code/process verification.
- `RESEARCH_FINDINGS.md`: For web/docs research summaries.
- `TASK_PLAN.md`: For breaking down user requests (Micro-planning).
- `GAP_ANALYSIS.md`: For comparing current state vs. desired state.

#### [MODIFY] `AGENTS.md`

- Add section "Artifact Standards": "All agents MUST use templates from `plans/templates/` for complex outputs."

### Kilo Code Audit Prep

#### [NEW] `prompts/kilo-audit.md`

- A comprehensive prompt file that the user can copy-paste or pipe to Kilo.
- Instructions:
  1. Read `AGENTS.md`, `opencode.json`, `bmad.yml`.
  2. Audit against "2026 Agentic Standards" (File structure, Naming conventions, Redis safety, Model hierarchy).
  3. Fill `plans/templates/AUDIT_REPORT.md`.
  4. Save to `plans/reports/audit-kilo-phase4.md`.

## Verification Plan

### Automated Tests

- Validate template syntax (Markdown linter).

### Manual Verification

- Run the Kilo Audit prompt (via `kilo run ...`) and verify the output matches the template structure.
