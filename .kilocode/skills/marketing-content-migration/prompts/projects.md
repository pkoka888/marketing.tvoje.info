# Projects Schema Migration Prompt

## Task
Migrate project categories from DevOps to Marketing focus.

## Files to Update
1. `src/content/config.ts` - Update category schema
2. `src/components/sections/Projects.astro` - Update filter categories

## Tone of Voice
- **Primary: Czech (CZ)**, Secondary: English (EN)
- Use customer language: "E-commerce marketing", "Online reklama"
- Avoid: technical jargon, "My jsme nejlepší"

## Changes Required

### config.ts
Replace category enums:

```typescript
// BEFORE
category: z.enum(['devops', 'ai', 'web', 'infrastructure'])

// AFTER
category: z.enum(['strategy', 'campaigns', 'content', 'analytics'])
```

Also update services schema:
```typescript
// BEFORE
category: z.enum(['devops', 'ai', 'cloud', 'consulting'])

// AFTER
category: z.enum(['strategy', 'campaigns', 'content', 'analytics', 'ecommerce'])
```

### Projects.astro
Replace filter categories:

```typescript
// BEFORE
{ key: 'devops', label: t.projects.categories.devops }

// AFTER
{ key: 'strategy', label: t.projects.categories.strategy }
{ key: 'campaigns', label: t.projects.categories.campaigns }
{ key: 'content', label: t.projects.categories.content }
{ key: 'analytics', label: t.projects.categories.analytics }
```

Also update translations.ts with new category labels:
```typescript
projects: {
  categories: {
    all: 'Vše',
    strategy: 'Strategie',
    campaigns: 'Kampaně',
    content: 'Obsah',
    analytics: 'Analytika',
  }
}
```

## Verification
After changes:
1. `npm run build` - must pass
2. Category filters work correctly
