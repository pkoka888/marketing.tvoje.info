# Services Migration Prompt

## Task
Migrate services content from DevOps to Marketing focus.

## Files to Update
1. `src/i18n/translations.ts` - Replace `devops` service translations
2. `src/components/sections/Services.astro` - Replace devops service card

## Tone of Voice
- **Primary: Czech (CZ)**, Secondary: English (EN)
- Use customer language: "E-commerce marketing", "Online reklama", "PPC"
- Avoid: technical jargon, "My jsme nejlepší"

## Changes Required

### translations.ts
Replace the `devops` service object with marketing services:

```typescript
// BEFORE (remove)
devops: {
  title: 'Marketing Automation',
  subtitle: 'Jak mohu pomoci vašemu podnikání růst',
  description: '...',
  items: ['...']
}

// AFTER (add these 4 services)
seo: {
  title: 'SEO optimalizace',
  subtitle: 'Více návštěvníků z vyhledávačů',
  description: 'Pomůžeme vám být vidět...',
  items: ['Analýza klíčových slov', 'On-page SEO', 'Technická SEO', 'Link building']
},
ppc: {
  title: 'PPC kampaně',
  subtitle: 'Reklamy co se vyplatí',
  description: 'Effektivní kampaně...',
  items: ['Google Ads', 'Facebook/Instagram', 'Retargeting', 'Analýza ROI']
},
ecommerce: {
  title: 'E-commerce',
  subtitle: 'Více prodejů z e-shopu',
  description: 'Optimalizace e-shopu...',
  items: ['Konverze', 'Produktové stránky', 'Košík', 'Mobilní verze']
},
content: {
  title: 'Obsahový marketing',
  subtitle: 'Obsah, který prodává',
  description: 'Blog, newsletter...',
  items: ['Blogové články', 'Newslettery', 'Popisy produktů', 'Sociální sítě']
}
```

### Services.astro
Replace the devops service card with marketing services:
- Remove devops service entry
- Add 4 marketing service cards (or update existing to show marketing services)

## Verification
After changes:
1. `npm run build` - must pass
2. Check CZ and EN versions work
