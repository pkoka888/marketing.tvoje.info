---
name: i18n-content
description: Bilingual content management guidelines for Czech + English portfolio
---

# i18n Content Management Skill

## Architecture

The site uses Astro's built-in i18n with:
- **Default locale**: `en` (no URL prefix)
- **Czech locale**: `cs` (URL prefix `/cs/`)
- Config in `astro.config.mjs` → `i18n` section

## File Structure

```
src/
├── pages/
│   ├── index.astro          # English homepage
│   ├── services.astro       # English services
│   ├── projects/            # English project pages
│   └── cs/
│       ├── index.astro      # Czech homepage
│       ├── sluzby.astro     # Czech services (localized URL)
│       └── projekty/        # Czech project pages
├── i18n/
│   └── translations.ts      # All UI string translations
└── content/
    └── projects/             # MDX content (language-neutral or per-locale)
```

## Adding Translations

1. Open `src/i18n/translations.ts`
2. Add keys to both `en` and `cs` objects
3. Use consistent key naming: `section.element.description` pattern

## Content Guidelines

### Czech Content
- Use formal Czech ("Vy" form) for business communication
- Czech-specific terminology for DevOps/AI concepts
- Include Czech date formatting (DD.MM.YYYY)
- Use Czech number formatting (space as thousands separator, comma for decimals)

### English Content
- Professional, concise technical writing
- International date formatting (YYYY-MM-DD or Month DD, YYYY)
- Standard number formatting

## SEO Requirements
- `hreflang` tags for all page pairs
- Localized meta titles and descriptions
- Language-specific URLs where appropriate
- `lang` attribute on `<html>` element
