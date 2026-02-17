# Task Plan: Performance Audit

**Date**: 2026-02-17
**Executor**: Kilo Code
**Model**: groq-code-fast-1:optimized:free
**Priority**: MEDIUM

## 1. Goal

Run Lighthouse audit on production to verify 95+ performance.

## 2. Context

- **Production URL**: https://marketing.tvoje.info
- **Target**: 95+ Lighthouse score

## 3. Audit Checklist

### 3.1 Performance Metrics

- [ ] Lighthouse Performance score
- [ ] LCP (Largest Contentful Paint) < 2.5s
- [ ] TBT (Total Blocking Time) < 200ms
- [ ] CLS (Cumulative Layout Shift) < 0.1

### 3.2 Accessibility

- [ ] Lighthouse Accessibility score
- [ ] ARIA labels present
- [ ] Color contrast OK
- [ ] Keyboard navigation works

### 3.3 Best Practices

- [ ] Lighthouse Best Practices score
- [ ] HTTPS enforced
- [ ] No console errors
- [ ] Images optimized

### 3.4 SEO

- [ ] Lighthouse SEO score
- [ ] Meta tags present
- [ ] Document has title
- [ ] Links are crawlable

## 4. Tools

Use:

- Chrome DevTools Lighthouse
- Or: `lhci autorun` if configured

## 5. Deliverable

Create: `plans/reports/PERFORMANCE_AUDIT.md`

Include:

- Lighthouse scores per category
- Specific recommendations
- Fixes needed (if any)
