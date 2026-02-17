# Task Plan: Theme Functionality Test

**Date**: 2026-02-17
**Executor**: Cline
**Model**: minimax-m2.1:free
**Priority**: HIGH

## 1. Goal

Verify all 7 themes work correctly on production.

## 2. Context

- **Production URL**: https://marketing.tvoje.info
- **Themes**: Titan, Lux, Nova, Spark, Target, Obsidian, Playful

## 3. Test Checklist

### 3.1 Theme Switcher

- [ ] Theme dropdown opens
- [ ] All 7 themes selectable
- [ ] Theme preview shows correct colors
- [ ] Click outside closes dropdown

### 3.2 Theme Application

- [ ] Titan applies correctly
- [ ] Lux applies correctly
- [ ] Nova applies correctly
- [ ] Spark applies correctly
- [ ] Target applies correctly
- [ ] Obsidian applies correctly
- [ ] Playful applies correctly

### 3.3 Persistence

- [ ] Theme persists on page reload
- [ ] Theme persists after closing browser
- [ ] Different pages use same theme

### 3.4 Mobile Theme

- [ ] Theme selector works on mobile
- [ ] All themes render on mobile
- [ ] No overflow issues

### 3.5 Theme Popup

- [ ] Welcome popup shows on first visit
- [ ] Can select theme from popup
- [ ] Popup closes after selection
- [ ] Doesn't reappear on reload

## 4. Deliverable

Create: `plans/reports/THEME_TEST_AUDIT.md`

Include:

- Test results per theme
- Any bugs found
- Screenshots
