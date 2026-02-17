# Task Plan: Accessibility Test

**Date**: 2026-02-17
**Executor**: Cline or Kilo
**Model**: groq-code-fast-1:optimized:free
**Priority**: MEDIUM

## 1. Goal

Verify WCAG 2.2 AA compliance.

## 2. Context

- **Production URL**: https://marketing.tvoje.info
- **Standard**: WCAG 2.2 AA

## 3. Audit Checklist

### 3.1 Keyboard Navigation

- [ ] All interactive elements focusable
- [ ] Tab order logical
- [ ] No keyboard traps
- [ ] Skip links present

### 3.2 Screen Reader

- [ ] Semantic HTML (header, main, footer)
- [ ] ARIA labels on icons/buttons
- [ ] Form labels present
- [ ] Alt text on images

### 3.3 Color & Contrast

- [ ] Text contrast 4.5:1 minimum
- [ ] Large text contrast 3:1
- [ ] Not color-only information

### 3.4 Forms

- [ ] Labels associated with inputs
- [ ] Error messages descriptive
- [ ] Required fields marked
- [ ] Focus visible

## 4. Tools

- axe DevTools
- WAVE
- Chrome Lighthouse (Accessibility tab)

## 5. Deliverable

Create: `plans/reports/ACCESSIBILITY_AUDIT.md`

Include:

- Issues found
- WCAG criteria violated
- Fix recommendations
