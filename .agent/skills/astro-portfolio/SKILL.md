---
name: astro-portfolio
description: Must read this skill when building or modifying Astro 5.0 portfolio components, pages, or styles.
---

# Astro Portfolio Development Skill

Use this skill when developing for the `marketing.tvoje.info` project.

## When to Use

- Adding or modifying Astro `.astro` components
- Working with Tailwind CSS v4 styles
- Updating site sections: Hero, ClientLogos, Certifications, Process, Team, Testimonials
- Configuring Astro integrations (sitemap, mdx, image optimization)

## Core Principles (Astro 5.0)

1.  **Strict TypeScript**: Always define interfaces for component props.
    ```typescript
    interface Props {
      title: string;
      description?: string;
    }
    const { title, description } = Astro.props;
    ```
2.  **Image Optimization**: Always use `<Image />` from `astro:assets`.
    ```astro
    import {Image} from 'astro:assets'; import myImage from '../assets/my-image.png';
    <Image src={myImage} alt="Description" />
    ```
3.  **Content Collections**: Use `src/content/` for structured data (testimonials, team).
4.  **Islands Architecture**: Only adding `client:*` directives when interactivity is absolutely required. Default to static (0 JS).

## Tailwind CSS v4 Rules

1.  **Theme Variables**: Use CSS variables for colors (e.g., `var(--color-brand)`).
2.  **No Config File**: Tailwind is configured via `@theme` in CSS, not `tailwind.config.js`.
3.  **Utility First**: Use utility classes in templates. Avoid `@apply` unless creating a reusable component class.

## Project Structure

- `src/components/`: Reusable UI components
- `src/layouts/`: Page wrappers (Layout.astro)
- `src/pages/`: File-based routing
- `src/content/`: Data collections
- `src/assets/`: Optimized images

## Related Resources

- **Project Rules**: `.clinerules/skills/kilo-structure.md`
