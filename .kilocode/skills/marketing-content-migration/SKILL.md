# Marketing Content Migration Skill

**Skill ID:** `marketing-content-migration`
**Version:** 1.0.0
**Created:** 2026-02-16

## Purpose

Migrate content from DevOps-focused to Marketing-focused using proper copywriting tone of voice.

## Tone of Voice Guidelines

Based on `docs/guides/copywriting-prompting-guide.md`:

### ✅ USE (Customer Language)

- "E-commerce marketing", "Online reklama", "PPC"
- "Potřebujete více zákazníků?"
- Concrete numbers: "+30%", "60k/měsíc"
- **Primary: Czech (CZ)**, Secondary: English (EN)

### ❌ AVOID

- Technical jargon: "MLOps", "AEO", "ROAS", "prémiový"
- "My jsme nejlepší"
- Long paragraphs (max 3 sentences)

## Files to Migrate

### Group 1: Services + Translations

- `src/i18n/translations.ts` - Replace `devops` service with marketing services
- `src/components/sections/Services.astro` - Replace devops service card

### Group 2: Schema + Filters

- `src/content/config.ts` - Update category schema from devops to marketing
- `src/components/sections/Projects.astro` - Update filter categories

### Group 3: Project Content

- `src/content/projects/cloud-migration.md` - Rewrite as marketing project
- `src/content/projects/cicd-automation.md` - Rewrite as marketing project

## Categories Replacement

```
devops → strategy
ai → campaigns
web → content
infrastructure → analytics
```

## Services Replacement

Replace devops service with marketing services:

- SEO optimalizace
- PPC kampaně
- E-commerce marketing
- Obsahový marketing

## Verification

After migration:

1. Run `npm run build` - must pass
2. Run `grep -r "devops" dist/` - should return empty
3. Verify bilingual (CZ + EN) content

## Sub-prompts

See `prompts/` folder for detailed prompts for each file group.
