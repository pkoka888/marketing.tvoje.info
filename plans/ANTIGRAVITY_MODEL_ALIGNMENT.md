# Antigravity Model Alignment Update

**Date**: 2026-02-17
**Status**: ✅ COMPLETED (Manual Fix Required)

## Executive Summary

This document records the model alignment corrections applied after Antigravity's Phase A was found incomplete. Despite claiming completion, Antigravity failed to properly update the configuration files with the verified model identifiers.

---

## 1. Background

### User-Verified Models

The following models were verified by the user as active in their environment:

| Tool      | Verified Model                         | Source                 |
| --------- | -------------------------------------- | ---------------------- |
| Kilo Code | `x-ai/grok-code-fast-1:optimized:free` | Kilo xAI partnership   |
| OpenCode  | `big-pickle`                           | OpenCode Zen (default) |
| Cline     | `minimax-m2.1:free`                    | OpenRouter             |

### Antigravity Claim vs Reality

| Item                           | Antigravity Claimed     | Actual State                   | Status      |
| ------------------------------ | ----------------------- | ------------------------------ | ----------- |
| opencode.json                  | Updated to big-pickle   | Still had minimax-m2.1:free    | ❌ NOT DONE |
| AGENTS.md                      | Updated model hierarchy | Still had old z-ai/glm4.7      | ❌ NOT DONE |
| cost-optimization              | Updated                 | Missing :optimized:free suffix | ⚠️ PARTIAL  |
| ANTIGRAVITY_MODEL_ALIGNMENT.md | Created                 | File didn't exist              | ❌ NOT DONE |

---

## 2. Corrections Applied

### 2.1 opencode.json

- ✅ Changed default model from `minimax-m2.1:free` to `big-pickle`
- ✅ Updated all agent models to use:
  - Primary: `x-ai/grok-code-fast-1:optimized:free` (coder, reviewer, codex)
  - Fallback: `big-pickle`
  - Architect: `gemini-2.5-pro:free`

### 2.2 AGENTS.md

- ✅ Updated Model Priority Order table:
  - Kilo: `x-ai/grok-code-fast-1:optimized:free`
  - OpenCode: `big-pickle`
  - Cline: `minimax-m2.1:free`
- ✅ Updated Agent Routing Matrix
- ✅ Updated OpenCode configuration description

### 2.3 cost-optimization (Canonical + Mirrors)

- ✅ Added `:optimized:free` suffix to grok-code-fast-1
- ✅ Added Resource Conservation section
- ✅ Synced to all mirror files:
  - `.agents/rules/cost-optimization.md`
  - `.clinerules/skills/cost-optimization.md`
  - `.gemini/rules/cost-optimization.md`

---

## 3. Model Hierarchy (FINAL)

| Priority | Tool       | Model                                  | Use Case                                |
| -------- | ---------- | -------------------------------------- | --------------------------------------- |
| T1       | Kilo Code  | `x-ai/grok-code-fast-1:optimized:free` | Bulk coding, internal search            |
| T1       | OpenCode   | `big-pickle`                           | Standard tasks, generation              |
| T1       | Cline      | `minimax-m2.1:free`                    | Routine fixes                           |
| T2       | Gemini CLI | `gemini-2.5-pro` (free tier)           | Complex architecture, external research |
| T3       | OpenRouter | Various free models                    | Capacity overflow                       |
| T4       | Groq       | `llama-3.3-70b`                        | Last resort only                        |

---

## 4. Resource Conservation Rule

**MANDATORY**: All agents must follow this rule:

- ❌ **NEVER** use Gemini for internal code searches (codesearch, grep, file search)
- ✅ Use `x-ai/grok-code-fast-1:optimized:free` for all internal search operations
- ✅ Reserve Gemini 2.5 Pro/Flash for:
  - External web research
  - Complex architecture decisions
  - High-context reasoning tasks

**Rationale**: Google's 1M TPD free quota is valuable and should be conserved for external research only. Internal operations are cheaper with grok-code-fast-1.

---

## 5. Template Standards

All outputs MUST use templates from `plans/templates/`:

- `plans/templates/AUDIT_REPORT.md`
- `plans/templates/RESEARCH_FINDINGS.md`
- `plans/templates/TASK_PLAN.md`
- `plans/templates/GAP_ANALYSIS.md`

---

## 6. Verification

Run after any configuration change:

```bash
python scripts/verify_agentic_platform.py
python scripts/validate_kilo_configs.py
npm run build
```

---

## 7. Anti-Regression Measures

To prevent future misconfigurations:

1. **Explicit model names**: All routing tables use exact model identifiers (not generic categories)
2. **Resource conservation rule**: Hardcoded in cost-optimization
3. **Verification mandatory**: Script must exit 0 before any PR
4. **Mirror sync required**: Any change to canonical must propagate to all mirrors

---

## 8. Files Modified

| File                                      | Change                                        |
| ----------------------------------------- | --------------------------------------------- |
| `opencode.json`                           | Updated default + agent models                |
| `AGENTS.md`                               | Updated model priority + routing matrix       |
| `.kilocode/rules/cost-optimization`       | Added :optimized:free + resource conservation |
| `.agents/rules/cost-optimization.md`      | Synced from canonical                         |
| `.clinerules/skills/cost-optimization.md` | Synced from canonical                         |
| `.gemini/rules/cost-optimization.md`      | Synced from canonical                         |

---

## 9. Next Steps

### Phase B: Quality Gates / E2E Tests

- Run existing E2E tests: `npm test`
- Verify lint: `npm run lint`
- Verify build: `npm run build`

---

**Note**: This document was created because Antigravity's Phase A self-report was inaccurate. Future iterations should include verification steps before claiming completion.
