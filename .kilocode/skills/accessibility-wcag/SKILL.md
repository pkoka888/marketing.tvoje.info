---
name: accessibility-wcag
description: WCAG 2.2 AA accessibility guidelines for the portfolio site
---

# WCAG 2.2 AA Accessibility Skill

## Required Standards

All pages must meet **WCAG 2.2 Level AA** compliance.

### Semantic HTML
- One `<h1>` per page, proper heading hierarchy (h1 → h2 → h3)
- Use `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`
- Use `<button>` for actions, `<a>` for navigation

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Visible focus indicators on all focusable elements
- Logical tab order matching visual order
- Skip link to main content

### Color & Contrast
- Normal text: minimum 4.5:1 contrast ratio
- Large text (18px+ or 14px+ bold): minimum 3:1 contrast ratio
- Never rely on color alone to convey information
- Both light and dark modes must meet contrast requirements

### Images & Media
- Descriptive `alt` text for all informational images
- `alt=""` for decorative images
- No auto-playing media

### Forms
- All inputs must have associated `<label>` elements
- Error messages must be programmatically associated with inputs
- ARIA `aria-describedby` for help text
- `aria-invalid="true"` for invalid fields
- Required fields marked with `aria-required="true"`

### ARIA
- Use ARIA landmarks: `role="banner"`, `role="navigation"`, `role="main"`, `role="contentinfo"`
- `aria-label` for interactive elements without visible text
- `aria-expanded` for expandable sections
- `aria-current="page"` for active navigation items

## Testing
- Run axe DevTools on every page
- Manual keyboard navigation test
- Screen reader test (NVDA or VoiceOver)
