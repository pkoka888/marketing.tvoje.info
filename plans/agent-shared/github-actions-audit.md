# GitHub Actions Workflow Audit Report

**Date:** 2026-02-19 **Workflows Audited:** 12

---

## Executive Summary

| Category        | Count | Status          |
| --------------- | ----- | --------------- |
| Total Workflows | 12    | -               |
| Critical Issues | 2     | ❌ Must fix     |
| High Priority   | 4     | ⚠️ Should fix   |
| Medium Priority | 6     | 💡 Improvements |
| Low Priority    | 3     | ✅ Optional     |

---

## Critical Issues (Must Fix Immediately)

### 1. **ci.yml - Duplicate `env:` Key** ❌

**Location:** `.github/workflows/ci.yml:84`

**Issue:**

```yaml
        env:
          PUBLIC_SITE_URL: https://portfolio.tvoje.info
        env:  # ← DUPLICATE!
          PUBLIC_SITE_URL: https://portfolio.tvoje.info
```

**Impact:** Workflow will fail to parse

**Fix:** Remove duplicate `env:` block

### 2. **Hardcoded IP Addresses in deploy.yml** ❌

**Location:** `.github/workflows/deploy.yml:33, 47, 89`

**Issue:**

- IP `89.203.173.196` hardcoded
- Internal IP `192.168.1.62` hardcoded
- Port numbers hardcoded (2260, 2262)

**Impact:**

- Security risk (IPs exposed)
- Inflexible (requires workflow edits to change servers)

**Fix:** Move to repository secrets:

```yaml
host: ${{ secrets.VPS_PUBLIC_IP }}
port: ${{ secrets.VPS_PUBLIC_PORT }}
```

---

## High Priority Issues

### 3. **SNYK_TOKEN Secret Not Documented** ⚠️

**Location:** `.github/workflows/security.yml:37`

**Issue:** Workflow requires `SNYK_TOKEN` but not documented in `.env.example`

**Fix:** Add to `.env.example` and setup documentation

### 4. **Agent Workflows Use Deprecated `::set-output`** ⚠️

**Location:** `.github/workflows/agent-verify.yml:181`, `ci-testing.yml:181`

**Issue:**

```yaml
echo "::set-output name=status::" >> $GITHUB_OUTPUT
```

**Fix:** Use environment files instead:

```yaml
echo "status=value" >> $GITHUB_ENV
```

### 5. **Multiple Redundant Workflows** ⚠️

**Issue:** Several workflows have overlapping functionality:

- `ci.yml` + `quality.yml` + `ci-testing.yml` all do lint/build/test
- `bmad.yml` duplicates CI/CD logic
- `deploy.yml` + `bmad.yml` both have deployment steps

**Impact:** Wasted compute resources, longer CI times

**Fix:** Consolidate into 3 main workflows:

1. `ci.yml` - PR checks (lint, test, build)
2. `deploy.yml` - Production deployment
3. `security.yml` - Security scans

### 6. **Version Check Uses Wrong Node Version** ⚠️

**Location:** `.github/workflows/version-check.yml:9`

**Issue:**

```yaml
env:
  NODE_VERSION: '22'
```

But `.nvmrc` specifies different version.

**Fix:** Read from `.nvmrc`:

```yaml
node-version-file: .nvmrc
```

---

## Medium Priority Issues

### 7. **Actions Not Pinned to SHA** 💡

**Location:** Multiple workflows

**Issue:** Using version tags instead of SHA:

```yaml
uses: actions/checkout@v4 # ← Could change
```

**Security Risk:** Supply chain attacks if action is compromised

**Fix:** Pin to SHA:

```yaml
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

### 8. **Slack Webhook URL Hardcoded** 💡

**Location:** `.github/workflows/ci-testing.yml:242`

**Issue:** Using `secrets.SLACK_WEBHOOK_URL` but should verify secret exists
first

### 9. **No Concurrency Controls on Most Workflows** 💡

**Issue:** Only `ci.yml` and `ci-testing.yml` have concurrency blocks

**Impact:** Multiple pushes can overwhelm runners

**Fix:** Add to all workflows:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### 10. **Missing Permissions Scoping** 💡

**Issue:** Most workflows use default permissions (write-all)

**Fix:** Add least-privilege permissions:

```yaml
permissions:
  contents: read
  actions: read
  security-events: write # only for security workflow
```

### 11. **Inconsistent Node Version Specification** 💡

**Issue:** Some workflows use `node-version: '20'`, others use `.nvmrc`

**Fix:** Standardize on `.nvmrc` everywhere

### 12. **backend-ci.yml References Non-Existent Backend** 💡

**Issue:** Workflow assumes `backend/` directory exists

**Fix:** Verify backend exists or remove workflow

---

## Low Priority / Recommendations

### 13. **Workflow Names Not Descriptive** ✅

Some workflows could have clearer names in GitHub UI

### 14. **Missing Workflow Documentation** ✅

Add comments explaining:

- What triggers the workflow
- What each job does
- Required secrets

### 15. **Unused Workflows** ✅

Consider if these are needed:

- `bmad.yml` (overlaps with ci.yml + deploy.yml)
- `ai-audit.yml` (uses Groq which may not be reliable)

---

## Security Audit Summary

| Check                  | Status | Notes                    |
| ---------------------- | ------ | ------------------------ |
| Secrets used correctly | ⚠️     | Some hardcoded IPs/ports |
| Permissions scoped     | ❌     | Using defaults           |
| Actions pinned         | ❌     | Using version tags       |
| CodeQL enabled         | ✅     | security.yml             |
| Snyk enabled           | ⚠️     | Requires token           |
| Dependabot             | ✅     | Enabled                  |

---

## Recommended Action Plan

### Phase 1: Critical (Do Today)

1. [ ] Fix duplicate `env:` in `ci.yml`
2. [ ] Move hardcoded IPs to secrets
3. [ ] Commit fixes

### Phase 2: High Priority (This Week)

4. [ ] Consolidate redundant workflows
5. [ ] Fix deprecated `::set-output` syntax
6. [ ] Standardize Node version to `.nvmrc`

### Phase 3: Medium Priority (Next Sprint)

7. [ ] Pin all actions to SHA
8. [ ] Add concurrency controls
9. [ ] Scope permissions per workflow
10. [ ] Verify backend directory exists

### Phase 4: Low Priority (Ongoing)

11. [ ] Document workflows
12. [ ] Review and remove unused workflows

---

## Workflow Consolidation Proposal

**Current:** 12 workflows **Proposed:** 5 workflows

1. **`ci.yml`** - Pull request checks
   - lint, typecheck, test, build
   - Runs on PR + push to main/develop

2. **`deploy.yml`** - Production deployment
   - Build + deploy to VPS
   - Runs on push to main

3. **`security.yml`** - Security scanning
   - CodeQL, Snyk, npm audit
   - Runs on schedule + PR

4. **`e2e.yml`** - End-to-end tests
   - Playwright tests against production
   - Runs on schedule

5. **`version-check.yml`** - Dependency health
   - Weekly version checks
   - Outdated packages audit

**Remove/Archive:**

- `bmad.yml` (duplicate)
- `quality.yml` (duplicate)
- `ci-testing.yml` (consolidate into ci.yml)
- `backend-ci.yml` (if no backend)
- `agent-verify.yml` (unreliable Groq)
- `ai-audit.yml` (unreliable Groq)
- `deploy-litellm.yml` (if not using LiteLLM)

---

## Files with Issues

- [ ] `.github/workflows/ci.yml` - Duplicate env key
- [ ] `.github/workflows/deploy.yml` - Hardcoded IPs
- [ ] `.github/workflows/agent-verify.yml` - Deprecated syntax
- [ ] `.github/workflows/ci-testing.yml` - Deprecated syntax
- [ ] `.github/workflows/version-check.yml` - Wrong Node version
- [ ] `.github/workflows/backend-ci.yml` - May reference non-existent dir
- [ ] All workflows - Need concurrency controls
- [ ] All workflows - Should pin actions to SHA

---

_Report generated: 2026-02-19_
