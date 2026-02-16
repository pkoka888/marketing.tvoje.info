# Security Audit Template

## Overview

This template provides a checklist for security and quality audits on BMAD projects.

## When to Run

| Phase      | Timing            | Required    |
| ---------- | ----------------- | ----------- |
| Phase 2+   | After MVP         | Optional    |
| Phase 3    | Post-MVP          | Required    |
| Pre-launch | Before production | Required    |
| Monthly    | Ongoing           | Recommended |

---

## Audit Checklist

### 1. Dependency Security

```bash
# Check for vulnerabilities
npm audit

# Check for outdated packages
npm outdated

# Run Snyk
npx snyk test
```

**Pass Criteria**:

- [ ] No critical vulnerabilities
- [ ] No high vulnerabilities (or documented exceptions)
- [ ] All dependencies up to date (minor versions)

---

### 2. Environment Variables

**Pass Criteria**:

- [ ] No secrets in `.env` committed to git
- [ ] `.env.example` exists with placeholder values
- [ ] All required env vars documented
- [ ] Production env vars use Vercel secrets

---

### 3. Authentication & Authorization

**Checklist**:

- [ ] No hardcoded credentials
- [ ] API keys use environment variables
- [ ] Form submissions use CSRF protection
- [ ] Rate limiting on forms (Formspree handles this)

---

### 4. Data Privacy (GDPR)

**Checklist**:

- [ ] Cookie consent implemented (if needed)
- [ ] Analytics uses cookie-free solution (Plausible)
- [ ] No personal data in logs
- [ ] Privacy policy exists
- [ ] Contact forms have privacy notice

---

### 5. Code Quality

```bash
# Run all checks
npm run lint
npm run typecheck
npm run test
```

**Pass Criteria**:

- [ ] ESLint passes with no errors
- [ ] TypeScript compiles without errors
- [ ] All tests pass
- [ ] Code coverage > 70%

---

### 6. Performance

**Checklist**:

- [ ] Lighthouse score > 90 (Performance)
- [ ] Lighthouse score > 90 (Accessibility)
- [ ] Lighthouse score > 90 (Best Practices)
- [ ] Lighthouse score > 90 (SEO)
- [ ] Images optimized
- [ ] No render-blocking resources

---

### 7. Accessibility

**Checklist**:

- [ ] All images have alt text
- [ ] Semantic HTML used
- [ ] Color contrast meets WCAG AA
- [ ] Focus states visible
- [ ] ARIA labels on interactive elements
- [ ] Keyboard navigation works

---

### 8. SEO

**Checklist**:

- [ ] Meta title and description present
- [ ] Open Graph tags for social
- [ ] Canonical URLs set
- [ ] Sitemap.xml exists
- [ ] Robots.txt exists
- [ ] Structured data (JSON-LD) for organization

---

## Automated Audit Script

```bash
#!/bin/bash
# audit.sh

echo "=== BMAD Security Audit ==="

echo "1. Checking dependencies..."
npm audit --audit-level=high || true

echo "2. Checking for secrets..."
git diff --cached | grep -E "(API_KEY|SECRET|PASSWORD)" || echo "No secrets found"

echo "3. Running tests..."
npm test

echo "4. Checking build..."
npm run build

echo "5. Checking types..."
npm run typecheck

echo "=== Audit Complete ==="
```

---

## Audit Report Template

```
# Security Audit Report
Date: [DATE]
Project: [PROJECT NAME]
Auditor: [NAME]

## Summary
[Pass/Fail] - [X] Critical, [Y] High, [Z] Medium issues

## Issues Found

### Critical
| Issue | Location | Fix |
|-------|----------|-----|
| - | - | - |

### High
| Issue | Location | Fix |
|-------|----------|-----|
| - | - | - |

### Medium
| Issue | Location | Fix |
|-------|----------|-----|
| - | - | - |

## Recommendations
1. [Recommendation]
2. [Recommendation]

## Sign-off
- [ ] Security audit passed
- [ ] Ready for production
- [ ] Date: ___________
```

---

## Lighthouse CI Integration

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on: [push]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci && npm run build
      - uses: treosh/lighthouse-ci-action@v11
        with:
          urls: |
            https://yoursite.com
          uploadArtifacts: true
          temporaryPublicStorage: true
```
