---
description: Astro 5.0 specific rules for the Marketing Portfolio project
author: Project
version: 1.0
category: "Astro Portfolio"
tags: ["astro", "portfolio", "static-site"]
globs: ["**/*.astro", "astro.config.mjs"]
alwaysApply: true
---

# Astro 5.0 Portfolio Rules

## Project Context
This is a marketing portfolio website built with:
- **Framework:** Astro 5.0
- **Styling:** Tailwind CSS 4.0
- **Language:** TypeScript
- **Hosting:** Vercel
- **Content:** MDX for projects

## Component Structure

### Required Directory Structure
```
src/
├── components/
│   ├── common/          # Header, Footer
│   ├── sections/         # Hero, About, Projects, Services
│   └── ui/              # Button, Card, Badge
├── content/
│   └── projects/        # MDX project content
├── i18n/               # Translations
├── layouts/            # Page layouts
├── pages/              # Astro pages
│   ├── cs/             # Czech pages
│   └── projects/       # Project detail pages
└── styles/             # Global styles
```

### Component Guidelines

#### Astro Components (.astro)
```astro
---
// Import types and utilities
import type { Props } from '../types';

// Define props interface
interface Props {
  title: string;
  description?: string;
}

// Destructure props
const { title, description = "Default" } = Astro.props;
---

<!-- HTML template with Tailwind classes -->
<section class="py-16">
  <h2 class="text-3xl font-bold">{title}</h2>
  {description && <p class="mt-4">{description}</p>}
  <slot />
</section>
```

#### UI Components
- Keep components simple and reusable
- Use TypeScript interfaces for props
- Use Tailwind utility classes
- Export from `src/components/index.ts`

#### Section Components
- Hero, About, Projects, Services, Contact, Testimonials
- Each section should be self-contained
- Include bilingual support (CZ/EN)

## MDX Content

### Project Content Structure
```markdown
---
title: "Project Title"
description: "Brief description"
tags: ["DevOps", "AI", "Cloud"]
publishDate: 2026-02-11
---

# Project Title

## Overview
Description of the project...

## Results
- Metric 1
- Metric 2
```

## Performance Rules

### Astro Island Architecture
- Use `client:load` only for interactive components
- Use `client:visible` for below-fold components
- Default to static HTML (no hydration)

### Image Optimization
```astro
import { Image } from 'astro:assets';
<Image src={myImage} alt="Description" width={800} format="webp" />
```

### Bundle Optimization
- Minimize client-side JavaScript
- Use Astro's built-in image optimization
- Lazy load images below the fold

## SEO Rules

### Meta Tags
Always include for every page:
```astro
<title>Page Title | marketing.tvoje.info</title>
<meta name="description" content="Page description" />
<link rel="alternate" hreflang="cs" href="https://..." />
<link rel="alternate" hreflang="en" href="https://..." />
```

### Structured Data
Use Schema.org markup for:
- Person (for About section)
- Organization (for the business)
- Service (for Services section)
- WebSite (for the site)

## Internationalization

### Translation Keys
```typescript
// src/i18n/translations.ts
export const translations = {
  cs: { hero_title: "Vítejte", ... },
  en: { hero_title: "Welcome", ... }
};
```

### Hreflang
```
/                     -> en
/cs/                  -> cs
```
