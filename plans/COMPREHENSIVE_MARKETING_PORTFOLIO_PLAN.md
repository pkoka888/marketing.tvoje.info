# Comprehensive Marketing Portfolio Implementation Plan

## Executive Summary

Based on research of:

1. **Top Czech marketing agencies** (Effectix, WeBetter, YYY, Symbio)
2. **React/Modern UI boilerplates** (100+ templates analyzed)
3. **10x Design Principles** from leading agencies

This plan outlines a complete implementation using **Astro 5.x** with Content Collections, featuring 10x design patterns and professional UX.

---

## ✅ ALREADY COMPLETED

### Theme Upgrade (Completed by Gemini)

| Task                     | Status | Files Modified                              |
| ------------------------ | ------ | ------------------------------------------- |
| New `shad-light` theme   | ✅     | `src/styles/themes.css`                     |
| New `shad-dark` theme    | ✅     | `src/styles/themes.css`                     |
| Card component styles    | ✅     | `src/styles/themes.css`                     |
| Button component updates | ✅     | `src/components/ui/Button.astro`            |
| ThemeSwitcher updates    | ✅     | `src/components/common/ThemeSwitcher.astro` |
| Tailwind config          | ✅     | `tailwind.config.mjs`                       |
| Build verification       | ✅     | 24 pages built                              |

**New Themes:**

- `shad-light` - Clean, minimal ShadCN/UI inspired
- `shad-dark` - Professional dark mode with muted colors

---

## Phase 1: Research & Analysis ✅ COMPLETED

### 1.1 Competitor Research (Czech Market)

**Top Czech Marketing Agencies Analyzed:**

- Effectix (effectixgroup.cz) - Full-service, 15+ years, 2500+ projects
- WeBetter (webetter.cz) - Creative digital agency, case studies focus
- YYY (yyy.cz) - Brand agency, strategic approach
- Symbio (symbio.agency) - Award-winning, enterprise clients

### 1.2 UI/UX Boilerplate Research (Feb 2026)

**Key Templates Analyzed:**
| Template | Focus | Relevant Patterns |
|----------|-------|-------------------|
| ShadCN/UI (via Next.js templates) | Component library | Radix primitives, accessible |
| traik06/nextjs-template-starter | Modern Next 15 + ShadCN | Clean component patterns |
| riipandi/vite-react-template | Production React | Tailwind, React Hook Form + Zod |
| brocoders/extensive-react-boilerplate | Enterprise i18n | MUI, Auth, Forms |
| kriasoft/react-starter-kit | Full-stack | Monorepo, tRPC, Stripe |

**Key Patterns to Adapt for Astro:**

1. **Component Architecture** - Atomic Design (atoms → molecules → organisms)
2. **Form Handling** - React Hook Form + Zod validation patterns
3. **UI Primitives** - Radix-style accessible components
4. **Type Safety** - Strict TypeScript throughout

### 1.3 Benchmark Comparison

| Feature                   | Effectix | WeBetter | YYY | Symbio | Our Site   |
| ------------------------- | -------- | -------- | --- | ------ | ---------- |
| Clear service categories  | ✅       | ✅       | ✅  | ✅     | ✅ Done    |
| Case studies with results | ✅       | ✅       | ✅  | ✅     | ✅ Done    |
| Client logos/social proof | ✅       | ✅       | ✅  | ✅     | ⏳ Pending |
| Team/About section        | ✅       | ✅       | ✅  | ✅     | ⏳ Pending |
| Certifications            | ✅       | ✅       | ❌  | ✅     | ⏳ Pending |
| Blog/Thought leadership   | ✅       | ✅       | ✅  | ✅     | ⏳ Pending |
| Process/workflow          | ✅       | ✅       | ✅  | ✅     | ⏳ Pending |
| Pricing transparency      | ✅       | ✅       | ✅  | ✅     | ✅ Done    |
| Professional Themes       | ✅       | ✅       | ✅  | ✅     | ✅ DONE    |

---

## Current Status Summary

### ✅ Completed

- Research (Czech competitors, boilerplates)
- Content Collections setup (projects, services, testimonials, faqs)
- Professional themes (shad-light, shad-dark) - Built Feb 2026
- Build passes (24 pages)
- Canonical URLs fixed (marketing.tvoje.info)
- Email fixed (hello@marketing.tvoje.info)

### ⏳ Remaining Gaps

1. Client Logos section
2. Team/About page
3. Certifications section
4. Blog section
5. Process/workflow section
6. Detailed service pages

---

## Phase 1.5: Content Collections ✅ DONE

### Gap 1: Client Logos & Social Proof ❌

**Solution:** Create Client Logos component with:

- Grid of client logos (from research: Kooperativa, inSPORTline, JTI, L'Occitane, CCC, DHL, MetLife, etc.)
- Hover effects similar to ShadCN component patterns
- Lazy loading for performance (matching riipandi/vite-react-template patterns)

**Implementation:**

- New component: `src/components/sections/ClientLogos.astro`
- Content collection: `src/content/clients/` (JSON with logo, name, description)
- Hover: scale + opacity transition

### Gap 2: Team/About Section ❌

**Solution:** Create Team section with:

- Profile cards (photo, name, role, expertise)
- Bio with experience years
- Social links
- Similar to YYY agency "People" page

**Implementation:**

- New component: `src/components/sections/Team.astro`
- Content collection: `src/content/team/` (JSON profiles)

### Gap 3: Certifications ❌

**Solution:** Create Trust/Certifications bar:

- Google Premier Partner badge
- Google Ads, Analytics, HubSpot certifications
- Partner badges (similar to Effectix)
- Animated on scroll (AOS integration)

**Implementation:**

- New component: `src/components/sections/Certifications.astro`
- SVG badges with hover tooltips

### Gap 4: Blog Section ❌

**Solution:** Create SEO blog:

- Content collections for blog posts
- Categories: SEO, PPC, Social, Strategy
- Related posts functionality
- Reading time estimate

**Implementation:**

- New collection: `src/content/blog/`
- Pages: `/blog/`, `/blog/:slug/`, `/cs/blog/`

### Gap 5: Process/Workflow Section ❌

**Solution:** Create Process section:

- 4-phase visualization (Discovery → Strategy → Implementation → Optimization)
- Timeline with icons
- Duration estimates
- Similar to WeBetter's "Jak pracujeme"

**Implementation:**

- New component: `src/components/sections/Process.astro`
- Animated timeline with scroll triggers

### Gap 6: Detailed Service Pages ❌

**Solution:** Create individual service pages:

- `/services/paid-media/`
- `/services/seo/`
- `/services/brand/`
- Each with: description, process, pricing options, case studies, FAQ

**Implementation:**

- New pages: `src/pages/services/[service].astro`
- Reuse components from shadcn-style patterns

### Gap 7: Case Studies Enhancement ❌

**Solution:** Improve case studies with:

- Before/After metrics
- Challenge → Solution → Results structure
- Client quote integration
- Related projects

---

## Phase 3: 10x Design Implementation

### 3.1 Design Principles (Based on Research)

**From Effectix:**

- Bold typography (similar to their "Effective online marketing" hero)
- Clear value proposition above fold
- Trust signals (certifications) prominently displayed

**From WeBetter:**

- Bold, action-oriented messaging
- Case study focus with real results
- Modern gradients and effects

**From ShadCN/UI Patterns:**

- Accessible components (Radix primitives)
- Consistent spacing (4px grid)
- Clear visual hierarchy
- Subtle animations

### 3.2 Component Architecture (Atomic Design)

```
src/components/
├── atoms/           # Basic elements
│   ├── Button.astro
│   ├── Badge.astro
│   ├── Icon.astro
│   └── Typography/
├── molecules/       # Combinations
│   ├── Card.astro
│   ├── FormField.astro
│   └── StatBlock.astro
├── organisms/       # Complex sections
│   ├── Hero.astro
│   ├── ProjectCard.astro
│   └── TestimonialCard.astro
└── templates/       # Page layouts
    ├── BaseLayout.astro
    └── PageLayout.astro
```

### 3.3 Type Safety (Based on Boilerplate Research)

Following patterns from:

- `riipandi/vite-react-template` (React Hook Form + Zod)
- Strict TypeScript throughout

**Implementation:**

- Zod schemas for all forms
- Type-safe content collections
- Strict null checks

---

## Phase 4: Implementation Tasks

### Subagent 1: Content & Research (Skills: copywriter, research)

- [ ] Research 10 more Czech marketing case studies
- [ ] Create 5 additional project case studies
- [ ] Add 10 client logos/descriptions
- [ ] Create certification badges content
- [ ] Research competitor pricing (Czech market)
- [ ] Write 5 blog post topics (SEO-optimized)

### Subagent 2: Component Development (Skills: astro, tailwind)

**Priority 1 - Essential Components:**

- [ ] `ClientLogos.astro` - Social proof section
- [ ] `Certifications.astro` - Trust badges
- [ ] `Team.astro` - About/team section
- [ ] `Process.astro` - Workflow visualization

**Priority 2 - Enhancement:**

- [ ] Service detail pages (3 pages)
- [ ] Blog listing + post template
- [ ] Enhanced case study layout

**Priority 3 - Polish:**

- [ ] Advanced animations (AOS integration)
- [ ] Micro-interactions (hover states)
- [ ] Loading states

### Subagent 3: Content Collections (Skills: astro)

- [ ] Add `clients` collection (logos, descriptions)
- [ ] Add `team` collection (profiles)
- [ ] Add `certifications` collection (badges)
- [ ] Add `process` collection (workflow steps)
- [ ] Add `blog` collection (posts)
- [ ] Migrate Services to collections
- [ ] Migrate Testimonials to collections

### Subagent 4: Testing & QA (Skills: playwright, lighthouse)

- [ ] Run E2E tests (dev)
- [ ] Run E2E tests (production)
- [ ] Lighthouse audit (all pages)
- [ ] Accessibility audit (WCAG 2.2)
- [ ] Cross-browser testing
- [ ] Mobile responsive testing

### Subagent 5: Deployment (Skills: devops, github-actions)

- [ ] Production build
- [ ] Pre-deployment tests
- [ ] Deploy to VPS
- [ ] Post-deployment smoke tests
- [ ] Monitoring setup

---

## Phase 5: Content Collections Schema

### Already Created ✅

```typescript
// src/content/config.ts
- projects: Case studies (Markdown)
- services: Services (JSON)
- testimonials: Testimonials (JSON)
- faqs: FAQ items (JSON)
```

### To Create

```typescript
// src/content/config.ts additions
const clients = defineCollection({
  type: 'data',
  schema: z.object({
    name: z.string(),
    logo: z.string(),
    description: z.string().optional(),
    industry: z.string(),
    website: z.string().optional(),
  }),
});

const team = defineCollection({
  type: 'data',
  schema: z.object({
    name: z.string(),
    role: z.string(),
    bio: z.string(),
    photo: z.string(),
    expertise: z.array(z.string()),
    social: z
      .object({
        linkedin: z.string().optional(),
        github: z.string().optional(),
      })
      .optional(),
  }),
});

const certifications = defineCollection({
  type: 'data',
  schema: z.object({
    name: z.string(),
    badge: z.string(),
    year: z.number(),
    description: z.string().optional(),
  }),
});

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date(),
    author: z.string(),
    tags: z.array(z.string()),
    category: z.string(),
    image: z.string(),
    readingTime: z.number().optional(),
    draft: z.boolean().default(false),
  }),
});
```

---

## Phase 6: Page Structure

### Current → Target

| Page           | Current | Target     | Action                           |
| -------------- | ------- | ---------- | -------------------------------- |
| Homepage       | ✅      | ✅ Enhance | Add Client Logos, Certifications |
| Projects       | ⚠️      | ✅ Enhance | Better case study layout         |
| Project Detail | ✅      | ✅ Enhance | Add metrics, quotes              |
| Services       | ⚠️      | ✅ New     | Create detail pages              |
| Pricing        | ✅      | ✅         | Keep                             |
| About/Team     | ❌      | ✅ New     | Create                           |
| Case Studies   | ✅      | ✅ Enhance | Better layout                    |
| FAQ            | ✅      | ✅         | Keep                             |
| Start          | ✅      | ✅         | Keep                             |
| Blog           | ❌      | ✅ New     | Create                           |
| Blog Post      | ❌      | ✅ New     | Create                           |

---

## Phase 7: Quality Gates

### Pre-Deployment Checklist

- [ ] Build passes (24+ pages)
- [ ] All E2E tests pass (11+ tests)
- [ ] Lighthouse Performance ≥90
- [ ] Lighthouse Accessibility ≥95
- [ ] Lighthouse SEO ≥95
- [ ] No broken links
- [ ] Canonical URLs correct
- [ ] Bilingual (EN + CS) complete
- [ ] Forms functional
- [ ] Mobile verified

---

## Timeline Estimate

| Week | Phase               | Tasks                                      | Status  |
| ---- | ------------------- | ------------------------------------------ | ------- |
| -    | Research            | Czech competitors, boilerplates            | ✅ Done |
| -    | Content Collections | Schema, files, components                  | ✅ Done |
| -    | Theme Upgrade       | shad-light, shad-dark themes               | ✅ Done |
| 1    | Components          | ClientLogos, Team, Certifications, Process | ⏳ Next |
| 2    | Blog + Services     | Blog pages, detailed service pages         | ⏳ Next |
| 3    | Testing             | Subagent 4: E2E, Lighthouse, Accessibility | ⏳ Next |
| 4    | Deploy + Fix        | Subagent 5: Deploy + bug fixes             | ⏳ Next |

**Remaining: ~3-4 weeks**

---

## Key Research Sources

### Competitor Analysis

- effectixgroup.cz - Services, certifications, process
- webetter.cz - Case studies, creative approach
- yyy.cz - Brand strategy, team presentation
- symbio.agency - Award-winning case studies

### UI/Component Patterns

- traik06/nextjs-template-starter - ShadCN patterns
- riipandi/vite-react-template - Production React patterns
- brocoders/extensive-react-boilerplate - i18n, forms
- ShadCN UI (radix-ui.com) - Accessible primitives

---

## Completed Work Log

### Session 1: Content Collections (OpenCode)

- Created `src/content.config.ts` with Zod schemas
- Created 9 project MD files (5 marketing, 4 devops)
- Created 3 services JSON, 3 testimonials JSON, 6 FAQ JSON
- Updated Projects.astro and [slug].astro to use collections
- Fixed canonical URLs and email

### Session 2: Theme Upgrade (Gemini)

- Added `shad-light` and `shad-dark` themes
- Updated `src/styles/themes.css` with new color palettes
- Updated Card component styles
- Updated Button component
- Updated ThemeSwitcher.astro
- Verified build passes (24 pages)

---

## Next Steps

1. **Approve this plan**
2. **Execute Subagent 2** - Components (ClientLogos, Team, Certifications, Process)
3. **Execute Subagent 1** - Blog + Content (parallel)
4. **Execute Subagent 4** - Testing
5. **Execute Subagent 5** - Deployment
