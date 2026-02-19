# Audit Plan: API Key Verification Script (Antigravity Work)

**Date**: 2026-02-19
**Auditor**: Kilo Code (bmad-qa)
**Original Agent**: Antigravity (Gemini 2.5 Pro)
**Skill**: `bmad-quality-assurance`

---

## 1. Scope

Audit the 4 fixes applied to `scripts/verify_api_keys.py` and `docs/SECURITY_ARCHITECTURE.md` by Antigravity on 2026-02-19. Verify correctness, security, and code quality.

## 2. Files to Audit

| File                                                                                                           | Changes                                       | Lines |
| -------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ----- |
| [verify_api_keys.py](file:///c:/Users/pavel/projects/marketing.tvoje.info/scripts/verify_api_keys.py)          | 4 bug fixes, new `source` flag logic          | 223   |
| [SECURITY_ARCHITECTURE.md](file:///c:/Users/pavel/projects/marketing.tvoje.info/docs/SECURITY_ARCHITECTURE.md) | Status table updates, infra keys reclassified | ~167  |
| [.env](file:///c:/Users/pavel/projects/marketing.tvoje.info/.env)                                              | Read-only — check for exposure risk           | 64    |

## 3. Audit Checklist

### 3.1 Fix #1: Gemini Endpoint (v1 → v1beta + param auth)

- [ ] Verify `v1beta` is correct for current Gemini API (Feb 2026)
- [ ] Verify `param` auth with `?key=` is supported
- [ ] Check if `v1` endpoint should also be supported as fallback
- [ ] Confirm the key in `.env` is valid (script returns 200)

**Findings:**

> _[PLACEHOLDER: Kilo Code audit findings for Fix #1]_

---

### 3.2 Fix #2: NVIDIA Endpoint (nvcf → integrate.api.nvidia.com)

- [ ] Verify `integrate.api.nvidia.com/v1/models` is current NVIDIA NIM endpoint
- [ ] Check if `api.nvcf.nvidia.com` is fully deprecated or still partially active
- [ ] Confirm the key returns 200 on the new endpoint
- [ ] Verify `Bearer` auth is correct for NVIDIA NIM

**Findings:**

> _[PLACEHOLDER: Kilo Code audit findings for Fix #2]_

---

### 3.3 Fix #3: Kilo Code (presence_only)

- [ ] Confirm no public Kilo Code API verification endpoint exists
- [ ] Verify JWT structure is valid (`eyJhbG...` prefix, 3 segments)
- [ ] Check JWT expiration claim (currently set to 2031)
- [ ] Consider: should script validate JWT structure (decode header/payload without verification)?

**Findings:**

> _[PLACEHOLDER: Kilo Code audit findings for Fix #3]_

---

### 3.4 Fix #4: load_dotenv override=True

- [ ] Verify `override=True` is safe (won't break other scripts that rely on system env vars)
- [ ] Check if any CI/CD workflows source this script (override would conflict with GH Actions env)
- [ ] Confirm the stale system `GEMINI_API_KEY` (`AIzaSyAu...leyw`) should be removed
- [ ] Check for other env vars that may also be shadowed

**Findings:**

> _[PLACEHOLDER: Kilo Code audit findings for Fix #4]_

---

### 3.5 Infrastructure Keys (github_secrets source)

- [ ] Verify all 6 infra keys exist in GitHub Secrets (via `gh secret list`)
- [ ] Confirm `source: "github_secrets"` logic correctly returns `True` even when key is absent
- [ ] Check if any local scripts actually need TS_OAUTH or VPS keys
- [ ] Verify the ⏭️ emoji renders correctly across terminals

**Findings:**

> _[PLACEHOLDER: Kilo Code audit findings for infra keys]_

---

### 3.6 Code Quality

- [ ] No hardcoded secrets in script
- [ ] Error handling covers network timeouts, DNS failures
- [ ] Key masking is adequate (first 8 + last 4 chars)
- [ ] Script returns proper exit codes (0 = all pass, 1 = any fail)
- [ ] Dead code: `auth_type: "header"` path still exists but no key uses it — should it be removed?
- [ ] `os.system("pip install ...")` on import failure — security risk?

**Findings:**

> _[PLACEHOLDER: Kilo Code code quality findings]_

---

### 3.7 Security Review

- [ ] `.env` is in `.gitignore`
- [ ] `.env` was never committed to git history (`git log --all --diff-filter=A -- .env`)
- [ ] `GITHUB_TOKEN` (`ghp_`) is classic PAT — recommend migration to fine-grained
- [ ] KILOCODE JWT expiry 2031 — acceptable or too long?
- [ ] Key masking in output doesn't leak enough for reconstruction

**Findings:**

> _[PLACEHOLDER: Kilo Code security findings]_

---

## 4. Verification Commands

```bash
# Run the verification script
python scripts/verify_api_keys.py

# Check .env is gitignored
git check-ignore .env

# Check if .env was ever committed
git log --all --diff-filter=A -- .env

# List GitHub Secrets (requires gh CLI)
gh secret list

# Check for stale system env vars
python -c "import os; [print(f'{k}={v[:8]}...') for k,v in os.environ.items() if 'API_KEY' in k or 'TOKEN' in k]"
```

## 5. Post-Audit Actions

After completing the audit, create a report at:
`plans/agent-shared/audit-reports/api-key-verification-audit-2026-02-19.md`

Then suggest a **final implementation plan** for parallel subagent execution to address any remaining findings.

---

## 6. Suggested Subagent Implementation Plan (Post-Audit)

> **Instruction to Kilo Code:** After completing the audit above, create a final implementation plan at `plans/agent-shared/api-key-verification-final-plan.md` using the template below. Assign tasks to subagents based on findings.

### Template for Final Plan

```markdown
# Final Implementation Plan: API Key Verification Hardening

**Date**: 2026-02-19
**Orchestrator**: Kilo Code (bmad-pm)

## Parallel Tasks

| #   | Task                 | Agent   | Skill   | Model   | Priority |
| --- | -------------------- | ------- | ------- | ------- | -------- |
| 1   | [From audit finding] | [Agent] | [Skill] | [Model] | P1/P2/P3 |
| 2   | ...                  | ...     | ...     | ...     | ...      |

## Sequential Gates

- Task X must complete before Task Y

## Suggested Assignments

- **Security fixes** → Antigravity (Gemini 2.5 Pro) — paid, high-accuracy
- **Code cleanup** → Kilo CLI (z-ai/glm4.7) — free, unlimited
- **Documentation** → Cline (minimax-m2.1:free) — free, good for text
- **Testing** → Gemini CLI (flash) — free, 1M/day

## Cost Estimate

- Paid: $X
- Free: $0
- Total: $X
```
