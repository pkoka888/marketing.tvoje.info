---
description: How to add new content (projects, case studies, blog posts) to the portfolio
---

## Adding a New Project

1. Create a new MDX file in `src/content/projects/`:
```
src/content/projects/my-project.mdx
```

2. Include required frontmatter:
```yaml
---
title: "Project Title"
description: "Brief description"
tags: ["DevOps", "AI", "Cloud"]
image: "/images/projects/my-project.png"
client: "Client Name"
date: 2026-01-01
featured: true
---
```

3. Write the case study body in MDX format with:
   - Problem description
   - Solution implementation
   - Results with metrics
   - Technology stack used

## Bilingual Content

- English content goes in the default pages (`src/pages/`)
- Czech content goes in `src/pages/cs/`
- Translations are in `src/i18n/translations.ts`
- When adding new UI strings, add both `en` and `cs` values to the translations file

## Images

- Place images in `public/images/` organized by type
- Use WebP or AVIF format for optimal performance
- Provide descriptive `alt` text for accessibility
