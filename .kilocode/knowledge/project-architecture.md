# Project Architecture Knowledge

**Last Updated:** 2026-02-11

## Tech Stack Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | Astro | 5.0 |
| Styling | Tailwind CSS | 3.4 |
| Language | TypeScript | 5.7 |
| Content | MDX | via @astrojs/mdx |
| Testing | Vitest | latest |
| Hosting | Vercel | auto-deploy |
| Forms | Formspree | external |
| Analytics | Plausible | privacy-first |
| CI/CD | GitHub Actions | 3 workflows |
| Linting | ESLint 9 + Prettier | flat config |

## Component Inventory

### Sections (src/components/sections/)
| Component | Size | Purpose |
|-----------|------|---------|
| Hero.astro | 5KB | Landing CTA with value proposition |
| About.astro | 7KB | Bio, career timeline, certifications |
| Projects.astro | 10KB | Portfolio showcase grid |
| Services.astro | 5KB | Service offerings cards |
| Testimonials.astro | 4KB | Client testimonial carousel |
| Contact.astro | 10KB | Formspree contact form |

### Common (src/components/common/)
| Component | Size | Purpose |
|-----------|------|---------|
| Header.astro | 6KB | Navigation + language toggle |
| Footer.astro | 7KB | Footer links + social |

### UI Primitives (src/components/ui/)
| Component | Size | Purpose |
|-----------|------|---------|
| Badge.astro | 1KB | Tag/skill badges |
| Button.astro | 2KB | CTA buttons |
| Card.astro | 1KB | Content cards |

## Pages

| Page | Path | Language |
|------|------|----------|
| Home | `/` | EN |
| Services | `/services` | EN |
| Projects | `/projects/` | EN |
| Home | `/cs/` | CS |
| (Czech pages) | `/cs/*` | CS |

## Agent Systems

| System | Location | Purpose |
|--------|----------|---------|
| Kilo Code | `.kilocode/` | Rules, skills, workflows, MCP |
| Antigravity | `.agent/` | Dev/build/test/deploy workflows |
| Cline | `.clinerules/` | Project-specific rules |
| Memory Bank | `.kilocode/rules/memory-bank/` | Persistent project context |
