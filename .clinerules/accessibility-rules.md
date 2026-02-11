---
description: WCAG 2.2 AA accessibility rules for the Marketing Portfolio
author: Project
version: 1.0
category: "Accessibility"
tags: ["accessibility", "wcag", "a11y"]
globs: ["**/*.astro", "**/*.html", "**/*.md"]
alwaysApply: true
---

# WCAG 2.2 AA Accessibility Rules

## Accessibility Requirements

### Color Contrast
- **Normal text:** 4.5:1 minimum ratio
- **Large text (18pt+ or 14pt+ bold):** 3:1 minimum ratio
- **UI components:** 3:1 minimum ratio

### Semantic HTML
```astro
<!-- ✅ Good - Semantic structure -->
<header>
  <nav>
    <main>
      <article>
        <section>
          <footer>

<!-- ❌ Bad - Non-semantic -->
<div class="header">
  <div class="nav">
    <div class="main">
      <div class="content">
```

### ARIA Labels
```astro
<!-- Buttons -->
<button aria-label="Open navigation menu">
  <svg>...</svg>
</button>

<!-- Links with icons -->
<a href="/about" aria-label="Learn more about us">
  <span>About</span>
</a>

<!-- Form inputs -->
<label for="email">Email</label>
<input id="email" type="email" aria-describedby="email-help" />
<span id="email-help" class="text-sm">We'll never share your email</span>
```

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Focus order must follow logical reading sequence
- Visible focus indicators on all interactive elements

```css
/* Focus styles */
:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* Skip link for keyboard users */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### Skip Links
```astro
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <header>...</header>
  <main id="main-content">
```

### Form Accessibility
```astro
<form>
  <div class="form-group">
    <label for="name">Name <span aria-hidden="true">*</span></label>
    <input 
      id="name" 
      type="text" 
      required 
      aria-required="true"
      aria-invalid="false"
    />
    <div role="alert" class="error-message"></div>
  </div>
  
  <button type="submit">Submit</button>
</form>
```

### Image Alt Text
```astro
<!-- Decorative images -->
<img src="decoration.svg" alt="" role="presentation" />

<!-- Informative images -->
<img src="team-photo.jpg" alt="Team photo with 5 members" />

<!-- Complex images -->
<img src="chart.png" alt="Bar chart showing 40% improvement" />
```

### Testing Checklist
- [ ] Run axe DevTools audit
- [ ] Test keyboard navigation
- [ ] Verify color contrast ratios
- [ ] Check screen reader output
- [ ] Test with NVDA/VoiceOver
