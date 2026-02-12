---
description: Keeper version-check — detect version mismatches and outdated dependencies
---

# Keeper Version Check Rule

## Trigger
When user says: `Keeper version-check` or `Keeper check versions`

## What to Check

### 1. Node.js Version Alignment
- Read `.nvmrc` for expected version
- Compare with `node -v` output
- Check CI workflows (`.github/workflows/*.yml`) for `NODE_VERSION`
- All must match the same major version

### 2. Package Dependencies
- Run `npm outdated` → report stale packages
- Run `npm audit` → report vulnerabilities
- Check `package.json` engines field

### 3. CLI Tools
- Run `python scripts/check-versions.py` if present
- Report any missing or outdated CLIs

### 4. GitHub Actions Versions
- Check for pinned SHA vs tag versions
- Report available updates for actions

### 5. Template Drift
- Compare project `.kilocode/` with `projects/template/.kilocode/`
- Report any drift from template baseline
- Check for duplicate frontmatter bug (alwaysApply: true)

## Output
Generate report to `plans/agent-shared/validation-reports/versions-YYYY-MM-DD.md`

## Safety
- Read-only checks only
- Never auto-update dependencies
- Report findings, let user decide on updates
