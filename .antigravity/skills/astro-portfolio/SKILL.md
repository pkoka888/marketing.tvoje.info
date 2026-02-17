# Astro Portfolio Skill

This skill provides specialized instructions for building and modifying the marketing portfolio website using Astro 5.0 and Tailwind CSS 4.0.

## When to Use

- Creating new components in `src/components/`
- Adding new pages in `src/pages/`
- Modifying layouts in `src/layouts/`
- Working with content collections in `src/content/`
- Implementing i18n (Czech/English)
- Styling with Tailwind CSS

## Project Context

### Tech Stack

- **Framework**: Astro 5.0 (island architecture)
- **Styling**: Tailwind CSS 4.0
- **Language**: TypeScript
- **Hosting**: Debian 13 VPS with PM2
- **Forms**: Formspree
- **Analytics**: Plausible

### Key Directories

```
src/
├── components/
│   ├── common/     # Header, Footer, ThemeSelector
│   ├── sections/   # Hero, About, Projects, Services, Contact
│   └── ui/         # Button, Card, Badge
├── content/
│   └── projects/   # MDX project case studies
├── i18n/           # Translations (Czech + English)
├── layouts/        # Layout.astro, PageLayout.astro
└── pages/
    ├── cs/         # Czech language pages
    └── projects/   # Project pages
```

## Instructions

### Component Creation

1. Follow existing component patterns in `src/components/`
2. Use TypeScript for all props
3. Use Tailwind CSS classes for styling
4. Support bilingual content via i18n

### Page Creation

1. Create English page in `src/pages/`
2. Create Czech translation in `src/pages/cs/`
3. Add translations to `src/i18n/translations.ts`
4. Use consistent layout components

### Tailwind Patterns

```astro
<!-- Buttons -->
<button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
  <!-- Cards -->
  <div class="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg">
    <!-- Sections -->
    <section class="py-16 md:py-24 px-4 md:px-8"></section>
  </div></button
>
```

### i18n Usage

```typescript
import { getLangFromUrl, useTranslations } from '../i18n/utils';

const lang = getLangFromUrl(Astro.url);
const t = useTranslations(lang);
```

## Examples

### Creating a New Section Component

```astro
---
interface Props {
  title: string;
  description: string;
}

const { title, description } = Astro.props;
---

<section class="py-16">
  <div class="max-w-4xl mx-auto">
    <h2 class="text-3xl font-bold mb-4">{title}</h2>
    <p class="text-gray-600 dark:text-gray-300">{description}</p>
  </div>
</section>
```

### Adding a New Project

Create `src/content/projects/my-project.md`:

```markdown
---
title: 'Project Title'
description: 'Brief description'
tags: ['astro', 'typescript']
image: '/images/project.jpg'
---

## Problem

Description of the problem solved...

## Solution

How it was implemented...

## Results

- 50% performance improvement
- 95+ Lighthouse score
```

## Commands

| Action     | Command             |
| ---------- | ------------------- |
| Dev server | `npm run dev`       |
| Build      | `npm run build`     |
| Preview    | `npm run preview`   |
| Lint       | `npm run lint`      |
| Typecheck  | `npm run typecheck` |

## Notes

- Keep components small and focused
- Use semantic HTML for accessibility
- Follow WCAG 2.2 AA guidelines
- Optimize images for performance
- Test responsive layouts
