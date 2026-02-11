---
description: Tailwind CSS 4.0 rules and patterns for the Marketing Portfolio
author: Project
version: 1.0
category: "Tailwind CSS"
tags: ["tailwind", "css", "styling"]
globs: ["**/*.astro", "**/*.ts", "**/*.tsx", "tailwind.config.mjs"]
alwaysApply: true
---

# Tailwind CSS 4.0 Rules

## Design System

### Color Palette
```javascript
// tailwind.config.mjs
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          blue: '#2563eb',    // Brand trust
          purple: '#7c3aed',  // Innovation
        },
        accent: {
          green: '#10b981',   // Success metrics
        },
        neutral: {
          slate: {
            900: '#0f172a',   // Dark backgrounds
            800: '#1e293b',   // Dark surfaces
            400: '#94a3b8',   // Muted text
          }
        }
      }
    }
  }
}
```

### Typography
```javascript
{
  fontFamily: {
    sans: ['Inter', 'sans-serif'],        // Primary - body text
    mono: ['JetBrains Mono', 'monospace'], // Code examples
  }
}
```

### Dark Mode
```javascript
// Enable class-based dark mode
export default {
  darkMode: 'class',
  // ...
}
```

## Utility Classes

### Spacing Scale
- Use `py-16` (4rem) for section vertical padding
- Use `gap-6` to `gap-8` for consistent gaps
- Use `space-y-4` to `space-y-6` for vertical rhythm

### Responsive Breakpoints
- `default`: Mobile (<640px)
- `sm`: Tablet (640px+)
- `md`: Laptop (768px+)
- `lg`: Desktop (1024px+)
- `xl`: Wide (1280px+)

### Common Patterns

#### Card Component
```astro
<div class="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6">
  <!-- Content -->
</div>
```

#### Button Variants
```astro
<!-- Primary -->
<button class="bg-primary-blue text-white px-6 py-3 rounded-lg hover:bg-blue-700">
  CTA
</button>

<!-- Secondary -->
<button class="border border-slate-600 px-6 py-3 rounded-lg hover:bg-slate-800">
  Secondary
</button>
```

#### Section Pattern
```astro
<section class="py-16 md:py-24 px-4 md:px-8 max-w-7xl mx-auto">
  <!-- Content -->
</section>
```

## Tailwind Best Practices

### Do's
- ✅ Use semantic colors (primary, accent, neutral)
- ✅ Keep classes in logical order (layout → spacing → visual → interactive)
- ✅ Use `dark:` prefix for dark mode styles
- ✅ Use `group` and `group-hover` for parent-child interactions
- ✅ Use `container` class for responsive containers

### Don'ts
- ❌ Don't use arbitrary values like `[#123456]`
- ❌ Don't mix Tailwind with custom CSS
- ❌ Don't use `!important` (use `!` prefix sparingly)
- ❌ Don't hardcode colors - use design tokens
- ❌ Don't skip mobile-first approach

### Custom Utilities
Add to `tailwind.config.mjs`:
```javascript
{
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    }
  }
}
```

## Performance

### CSS Optimization
- Use `@tailwindcss/forms` plugin for form styling
- Use `@tailwindcss/typography` for prose content
- Purge unused styles in production (Astro does this automatically)

### Recommended Plugins
- `@tailwindcss/forms` - Form normalization
- `@tailwindcss/typography` - Markdown/MDX styling
- `@tailwindcss/aspect-ratio` - Aspect ratio utilities
