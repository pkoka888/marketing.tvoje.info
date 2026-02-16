# Marketing Portfolio - Implementation Plan

**Last Updated:** 2026-02-16
**Project:** Marketing Portfolio for Pavel Kašpar
**Status:** Clean & Ready for Deployment

---

## Project Overview

A bilingual (Czech/English) marketing portfolio website built with Astro 5.0. Focus: showcasing marketing services, projects, and client testimonials.

---

## Technology Stack

| Category  | Technology           | Notes                              |
| --------- | -------------------- | ---------------------------------- |
| Framework | Astro 5.0            | Static site, zero JS by default    |
| Styling   | Tailwind CSS 3.4     | Utility-first                      |
| Language  | TypeScript           | Type safety                        |
| Hosting   | VPS (server62)       | Nginx static files                 |
| Domain    | marketing.tvoje.info | From previous portfolio.tvoje.info |
| Analytics | Plausible            | Privacy-focused                    |
| Forms     | Formspree            | No backend needed                  |

---

## Current Status

### ✅ Completed

- [x] Theme system (5 themes: TITAN, NOVA, TARGET, SPARK, LUX)
- [x] Hero section - marketing content
- [x] About section - marketing skills (not DevOps)
- [x] Services section - marketing services
- [x] Contact section - Formspree integration
- [x] Bilingual support (EN + CS)
- [x] Meta tags updated (Pavel Kašpar - Marketing)
- [x] 5 theme photos generated
- [x] Build system cleaned up (removed PM2/backend)
- [x] Deploy script fixed (static file copy only)

### ⏳ Pending

- [ ] Deploy to production
- [ ] Verify live site at marketing.tvoje.info
- [ ] Test all 5 themes in production

---

## File Structure

```
marketing.tvoje.info/
├── src/
│   ├── components/
│   │   ├── common/         # Header, Footer
│   │   ├── sections/        # Hero, About, Services, Projects, Contact
│   │   └── ui/              # Button, Card, Badge
│   ├── content/projects/    # MDX project case studies
│   ├── i18n/               # Translations (EN/CS)
│   ├── layouts/             # Page layouts
│   ├── pages/               # Astro pages
│   │   ├── index.astro     # Homepage (EN)
│   │   ├── cs/             # Czech pages
│   │   └── projects/       # Project pages
│   └── styles/             # Global styles
├── public/
│   └── images/theme/       # Theme photos & logos
├── dist/                   # Production build output
├── archive/                # Archived DevOps materials
└── .github/workflows/     # CI/CD
```

---

## Commands

### Development

```bash
npm run dev          # Start dev server at localhost:4321
npm run build        # Build to dist/
npm run preview      # Preview production build
```

### Deployment

```bash
# Manual (local)
npm run build
# Files in dist/ are copied to VPS via GitHub Actions

# Automatic (GitHub Actions)
git push main        # Triggers deploy.yml
```

---

## Deployment Flow

1. **Push to main** → GitHub Actions
2. **Build** → `npm run build` creates `dist/`
3. **Deploy** → SCP `dist/` to VPS `/var/www/portfolio`
4. **Serve** → Nginx serves static files

---

## Key Decisions

### Why Static Site?

- Simplicity - no backend needed
- Performance - pre-rendered HTML
- Security - no server-side code exposure
- Cost - Nginx serves files cheaply

### Why 5 Themes?

- Visual variety for different client preferences
- TITAN: Professional/Direct
- NOVA: Friendly/Expert
- TARGET: Goal-focused
- SPARK: Bold/Creative
- LUX: Premium/Minimal

---

## Maintenance

### Regular Tasks

1. Update project case studies in `src/content/projects/`
2. Add new testimonials
3. Update translations in `src/i18n/translations.ts`
4. Add new theme photos if needed

### Testing Checklist

- [ ] Build passes: `npm run build`
- [ ] No lint errors: `npm run lint`
- [ ] All pages load (EN + CS)
- [ ] Theme switcher works
- [ ] Contact form submits

---

## Archived Materials

See `archive/README.md` for details on DevOps materials that were archived.

---

## Next Steps

1. Push changes to main
2. Verify GitHub Actions deploys successfully
3. Check live site at marketing.tvoje.info
4. Test theme switching
5. Share with potential clients
