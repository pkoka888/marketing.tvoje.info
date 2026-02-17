# Task Plan: CSS/Visual Quality Audit

**Date**: 2026-02-17
**Executor**: Cline
**Model**: minimax-m2.1:free
**Priority**: HIGH

## 1. Goal

Audit CSS effects, gradients, shadows, animations across all themes and pages.

## 2. Context

- **Production URL**: https://marketing.tvoje.info
- **Themes**: 7 themes (Titan, Lux, Nova, Spark, Target, Obsidian, Playful)
- **Pages**: 24 pages (EN + CZ)

## 3. Audit Checklist

### 3.1 Theme Effects

- [ ] Gradient backgrounds on all themes
- [ ] Box shadows consistency
- [ ] Border radius uniformity
- [ ] Color palette consistency

### 3.2 Hover/Transition Effects

- [ ] Button hover states
- [ ] Card hover effects
- [ ] Link animations
- [ ] Menu transitions

### 3.3 Mobile Responsiveness

- [ ] Hamburger menu works
- [ ] No horizontal scroll
- [ ] Touch-friendly tap targets
- [ ] Images scale properly

### 3.4 Dark Mode

- [ ] Contrast ratios OK
- [ ] No white flashes
- [ ] Theme persists on reload
- [ ] All elements visible

### 3.5 Performance

- [ ] No layout shifts (CLS)
- [ ] Smooth animations (no jank)
- [ ] Images lazy load

## 4. Deliverable

Create: `plans/reports/CSS_VISUAL_AUDIT.md`

Include:

- Screenshots of issues
- CSS selectors that need fixing
- Priority (P0/P1/P2)
