---
description: Czech/English bilingual content rules for the Marketing Portfolio
author: Project
version: 1.0
category: "Internationalization"
tags: ["i18n", "localization", "bilingual", "cz", "en"]
globs: ["**/*.ts", "**/*.astro", "src/i18n/**/*"]
alwaysApply: true
---

# Bilingual Content Rules (CZ/EN)

## Language Structure

### URL Structure
```
/                  -> English (default)
/cs/               -> Czech
```

### Translation Files
```typescript
// src/i18n/translations.ts
export const translations = {
  cs: {
    // Czech translations
    hero_title: "Vítejte",
    hero_subtitle: "DevOps & AI Specialista",
    nav_about: "O mně",
    nav_projects: "Projekty",
    nav_services: "Služby",
    nav_contact: "Kontakt",
  },
  en: {
    // English translations
    hero_title: "Welcome",
    hero_subtitle: "DevOps & AI Specialist",
    nav_about: "About",
    nav_projects: "Projects",
    nav_services: "Services",
    nav_contact: "Contact",
  }
};
```

## Content Management

### Section-Specific Keys
```typescript
export const sectionKeys = {
  hero: {
    cs: {
      title: "hero_title",
      subtitle: "hero_subtitle",
      cta: "hero_cta",
    },
    en: {
      title: "hero_title",
      subtitle: "hero_subtitle",
      cta: "hero_cta",
    }
  },
  about: {
    cs: { title: "about_title", bio: "about_bio" },
    en: { title: "about_title", bio: "about_bio" }
  },
  projects: {
    cs: { title: "projects_title", filter: "projects_filter" },
    en: { title: "projects_title", filter: "projects_filter" }
  },
  services: {
    cs: { title: "services_title", cta: "services_cta" },
    en: { title: "services_title", cta: "services_cta" }
  },
  contact: {
    cs: { title: "contact_title", form: "contact_form" },
    en: { title: "contact_title", form: "contact_form" }
  }
};
```

## Translation Guidelines

### Czech Specifics
- Use proper Czech diacritics (ě, š, č, ř, ž, ý, á, í, é, ú, ů)
- Formal address (Vy form) for business content
- Czech date formats: d. m. yyyy
- Czech currency: Kč

### English Specifics
- American or British English consistently
- Date formats: Month Day, Year
- Currency: USD, EUR (clarify in context)

### Content Length Considerations
- German is ~30% longer than English
- Czech is ~20% longer than English
- Design for variable content length
- Use `min-height` instead of fixed heights

## Best Practices

### Do's
- ✅ Use translation keys for all UI text
- ✅ Keep translations in separate files
- ✅ Support right-to-left for future languages
- ✅ Test both languages in design
- ✅ Use semantic HTML `lang` attribute

### Don'ts
- ❌ Don't hardcode text in templates
- ❌ Don't mix languages in content
- ❌ Don't assume equal length for both languages
- ❌ Forget to update translations when adding features
