# Task Plan: Deploy to Production

**Date**: 2026-02-17
**Executor**: Git (Manual)
**Priority**: HIGH

## 1. Goal

Deploy the marketing portfolio to production VPS.

## 2. Pre-deployment Checklist

- [ ] Verify build passes: `npm run build`
- [ ] Verify tests pass: `npm test`
- [ ] Check lint: `npm run lint`
- [ ] Verify all 24 pages build

## 3. Execution

```bash
git add .
git commit -m "chore: Phase 2 complete - visual tests, FB pixel, gap analysis"
git push origin main
```

## 4. Post-deployment

- [ ] GitHub Actions triggers deploy.yml
- [ ] Verify at: https://marketing.tvoje.info

## 5. Verification

- [ ] Homepage loads
- [ ] Theme switcher works
- [ ] Contact form works
- [ ] All pages accessible
