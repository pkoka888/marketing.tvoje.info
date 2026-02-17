---
name: astro-portfolio
description: Use when building or modifying Astro 5.0 portfolio/marketing site components, pages, or styles
---

## Use This When

- Adding or modifying Astro `.astro` components
- Working with Tailwind CSS v4 styles
- Updating site sections: Hero, ClientLogos, Certifications, Process, Team, Testimonials
- Configuring Astro integrations (sitemap, mdx, image optimization)

## Astro 5.0 Patterns

- Use `Astro.props` with TypeScript interfaces for component props
- Prefer `<Image>` component from `astro:assets` over raw `<img>`
- Use `content collections` for structured data (testimonials, team members)
- Islands architecture: add `client:load` only when interactivity is required
- SEO: use `<meta>` in `<Layout>` + JSON-LD schema in page components

## Tailwind CSS v4 Rules

- Use CSS variables for theme colors: `var(--color-brand)`
- No `tailwind.config.js` needed — configure via `@theme` in CSS
- Use `@apply` sparingly — prefer utility classes in templates

## File Structure

```
src/
  components/     # Reusable .astro components
  pages/          # Route-based pages
  layouts/        # Page layout wrappers
  content/        # Content collections (YAML/Markdown)
  assets/         # Images optimized via astro:assets
  styles/         # Global CSS with @theme
```

## References

- `.clinerules/skills/kilo-structure.md` — project dir standards
- `C:/Users/pavel/vscodeportable/agentic/ai-prompts/prompts/astro-4/rule-astro-coding-standards.md`
- `C:/Users/pavel/vscodeportable/agentic/ai-prompts/prompts/tailwind-4/rule-tailwind-v4.md`
