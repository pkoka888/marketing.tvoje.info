---
name: astro-portfolio
description: Guidelines for developing the Astro 5.0 portfolio site (marketing.tvoje.info)
---

# Astro Portfolio Development Skill

## Architecture

This is an **Astro 5.0** static site using island architecture (zero JS by default).

### Key Files
- `astro.config.mjs` — Framework config (site URL, integrations, i18n, markdown)
- `src/pages/` — File-based routing. EN pages at root, CS pages under `cs/`
- `src/layouts/Layout.astro` — Base HTML layout with SEO meta
- `src/components/` — Astro components (`.astro` files, no framework needed)
- `src/content/` — MDX content collections (projects, case studies)
- `src/i18n/translations.ts` — All UI string translations (EN + CS)
- `src/styles/` — Global CSS

## Component Patterns

### Section Components (`src/components/sections/`)
Each section (Hero, About, Projects, Services, Testimonials, Contact) is a self-contained Astro component imported by page files. They should:
- Accept `lang` prop when bilingual content differs
- Use semantic HTML5 elements (`<section>`, `<article>`)
- Include ARIA labels for accessibility
- Use Tailwind utility classes for styling

### UI Primitives (`src/components/ui/`)
Reusable atoms: `Badge.astro`, `Button.astro`, `Card.astro`. Keep these small and composable.

## i18n Pattern

- Default locale: `en` (no URL prefix)
- Czech locale: `/cs/` prefix
- Add new strings to `src/i18n/translations.ts` in both `en` and `cs` objects
- Use `Astro.currentLocale` for locale detection in components

## Content Collections

Projects use MDX content collections defined in `src/content/config.ts`. Each project file in `src/content/projects/` has typed frontmatter.

## Performance Rules

- Zero client-side JS by default — use `client:*` directives only when needed
- Optimize images (WebP/AVIF, lazy loading)
- Keep bundle under 50KB gzipped
- Target Lighthouse 95+ across all categories
