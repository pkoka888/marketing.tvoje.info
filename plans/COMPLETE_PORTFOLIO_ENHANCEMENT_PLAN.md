# Complete Portfolio Enhancement Plan - Phase 2

**Created**: 2026-02-16
**Updated**: 2026-02-16 (with research findings)
**Status**: Planning
**Project**: marketing.tvoje.info (Marketing Portfolio)

---

## Executive Summary

Based on comprehensive research of Czech market pricing and best practices, this plan outlines all enhancements needed to create a complete, high-converting marketing portfolio.

---

## Part 1: Research Findings

### 1.1 Czech Market Pricing Research

| Service            | Czech Market Range     | Recommended for Us |
| ------------------ | ---------------------- | ------------------ |
| **Basic Website**  | 400-500 € (10-12K CZK) | Starter            |
| **SEO Audit**      | 3-5K CZK               | Mini SEO           |
| **Growth Website** | 9,900 € (250K CZK)     | -                  |
| **Full SEO + PPC** | 15-50K CZK/měsíc       | Growth             |
| **Enterprise**     | 50K+ CZK/měsíc         | Enterprise         |

**Sources**: Effectix, Webgate, SEOMAKER, Landmark Media, OTON, Madviso

### 1.2 Pricing Page Best Practices (2026 Research)

| Finding                                      | Source                       |
| -------------------------------------------- | ---------------------------- |
| 57% check pricing before product description | Pricing Strategy Report 2024 |
| Top converters: 5-15% conversion rate        | Industry benchmarks          |
| Three-tier pricing optimal                   | SaaS research                |
| "Recommended" highlight increases clicks 34% | A/B testing data             |
| Transparency builds trust                    | Multiple sources             |

### 1.3 Lead Form Best Practices (2026 Research)

| Finding                              | Source              |
| ------------------------------------ | ------------------- |
| Average form abandonment: 68%        | FormSort research   |
| Top performers: 11%+ conversion      | Industry benchmarks |
| 3-5 fields optimal for cold traffic  | HubSpot/Unbounce    |
| Progressive profiling for warm leads | Monday.com          |
| Mobile-first design critical         | Multiple sources    |

---

## Part 2: Recommended Pricing (Based on Research)

### Final Pricing Packages:

| Package     | Price (CZK) | EUR     | Best For                    |
| ----------- | ----------- | ------- | --------------------------- |
| **START**   | 9,900 Kč    | ~€400   | Small businesses, local SEO |
| **ROZVOJ**  | 24,900 Kč   | ~€1,000 | Growth companies, SEO+PPC   |
| **PREMIUM** | 49,900 Kč   | ~€2,000 | Enterprises, full service   |

**Note**: All prices are+VAT. Monthly management available from 4,900 Kč.

### Package Features:

#### START (9,900 Kč)

- SEO audit + basic optimization
- Google Ads setup (až 10,000 Kč kredit)
- Monthly report
- 3-month commitment

#### ROZVOJ (24,900 Kč)

- Full SEO strategy
- PPC management (Google Ads, Sklik)
- Content strategy (4 články/měsíc)
- Weekly reports
- 6-month commitment

#### PREMIUM (49,900 Kč)

- Full digital marketing
- Dedicated account manager
- Custom reporting dashboard
- Monthly strategy calls
- Annual contract

---

## Part 3: Fast Onboarding Form

### Best Practice Implementation:

**Fields** (3-5 max):

1. **Project type** (dropdown) - SEO / PPC / Web / Full-service
2. **Budget** (dropdown) - do 10K / 10-25K / 25-50K / 50K+
3. **Email** (required) - only what's needed for initial contact

**Best Practices Applied**:

- Minimal friction (3 fields only)
- Progressive disclosure for details
- Auto-save draft
- Mobile-optimized
- Clear value proposition above form

**Location**:

- Hero: "Rychlá poptávka" button → /start page
- Footer: Quick contact widget

---

## Part 4: Theme Selector Popup (P0)

### Implementation Required:

| Component           | Status    | Notes                   |
| ------------------- | --------- | ----------------------- |
| ThemeSelector.astro | ⏳ Create | Dropdown with 5 themes  |
| ThemePopup.astro    | ⏳ Create | Modal with timing logic |
| Header.astro        | ⏳ Modify | Add selector to header  |
| Layout.astro        | ⏳ Modify | Add popup + logic       |
| global.css          | ⏳ Modify | Styling                 |

### Features:

- Show after 60 seconds
- Show on exit intent (mouse leaves top)
- Motivational headline: "Najděte svůj styl!" (Find Your Style!)
- Show only once per session
- Theme persists to localStorage

---

## Part 5: Content Gaps

### Current vs Recommended:

| Page          | Current | Recommended                    |
| ------------- | ------- | ------------------------------ |
| Homepage      | ✅      | Expand with trust signals      |
| /cs/          | ✅      | Same                           |
| /projects     | ✅      | Move to /case-studies          |
| /services     | ✅      | Move to pricing page           |
| /theme-test   | ✅      | Keep or remove                 |
| /pricing      | ❌      | **CREATE**                     |
| /start        | ❌      | **CREATE** - Fast onboarding   |
| /case-studies | ❌      | **CREATE** - Detailed projects |
| /faq          | ❌      | **CREATE**                     |
| /about        | ❌      | **ENHANCE**                    |
| /blog         | ❌      | **CREATE** - Later             |

---

## Part 6: Detailed Implementation Tasks

### Task Group 1: Theme Selector (P0)

| #    | Task                          | Files               |
| ---- | ----------------------------- | ------------------- |
| T1.1 | Create ThemeSelector dropdown | ThemeSelector.astro |
| T1.2 | Create ThemePopup modal       | ThemePopup.astro    |
| T1.3 | Add timing logic (60s + exit) | Layout.astro        |
| T1.4 | Style components              | global.css          |
| T1.5 | Integrate in Header           | Header.astro        |

### Task Group 2: Pricing & Onboarding (P1)

| #    | Task                                         | Files                             |
| ---- | -------------------------------------------- | --------------------------------- |
| T2.1 | Create Pricing page with Czech market prices | pricing.astro, Pricing.astro      |
| T2.2 | Create Fast Onboarding form (/start)         | start.astro, FastOnboarding.astro |
| T2.3 | Add pricing to translations                  | translations.ts                   |
| T2.4 | Create Czech versions                        | cs/pricing.astro, cs/start.astro  |

### Task Group 3: Trust & Conversion (P1)

| #    | Task                            | Files             |
| ---- | ------------------------------- | ----------------- |
| T3.1 | Add client logos section        | ClientLogos.astro |
| T3.2 | Enhance Hero with trust signals | Hero.astro        |
| T3.3 | Add certification badges        | About.astro       |
| T3.4 | Update CTAs across site         | Various           |

### Task Group 4: Content Pages (P2)

| #    | Task                      | Files              |
| ---- | ------------------------- | ------------------ |
| T4.1 | Create Case Studies index | case-studies.astro |
| T4.2 | Create FAQ page           | faq.astro          |
| T4.3 | Enhance About section     | About.astro        |

---

## Part 7: Files to Create/Modify

### New Files:

```
src/components/common/ThemeSelector.astro
src/components/common/ThemePopup.astro
src/components/sections/Pricing.astro
src/components/sections/FastOnboarding.astro
src/components/sections/ClientLogos.astro
src/pages/pricing.astro
src/pages/cs/pricing.astro
src/pages/start.astro
src/pages/cs/start.astro
src/pages/case-studies.astro
src/pages/cs/case-studies.astro
src/pages/faq.astro
src/pages/cs/faq.astro
```

### Modify Files:

```
src/components/common/Header.astro
src/layouts/Layout.astro
src/styles/global.css
src/i18n/translations.ts
src/components/sections/Hero.astro
src/components/sections/Services.astro
src/components/sections/About.astro
```

---

## Part 8: Subagent Orchestration

### Phase 1: Theme Selector (Parallel)

```
Agent 1: Create ThemeSelector.astro
Agent 2: Create ThemePopup.astro
Agent 3: Update Header + Layout
Agent 4: Add global styles
```

### Phase 2: Pricing & Onboarding (Parallel)

```
Agent 1: Create pricing page (EN + CS)
Agent 2: Create fast onboarding form
Agent 3: Add pricing to translations
Agent 4: Create pricing component
```

### Phase 3: Trust Signals (Parallel)

```
Agent 1: Client logos section
Agent 2: Hero enhancements
Agent 3: About badges
Agent 4: CTA updates
```

### Phase 4: Content Pages (Sequential)

```
Step 1: Case Studies
Step 2: FAQ
Step 3: About enhancement
```

---

## Success Criteria

| Metric                   | Current | Target |
| ------------------------ | ------- | ------ |
| Pages                    | 5       | 15+    |
| Lighthouse Performance   | 100     | 95+    |
| Lighthouse Accessibility | 93      | 95+    |
| Form Conversion          | ?       | 5%+    |
| Bounce Rate              | ?       | <40%   |

---

## Questions Answered by Research

| Question            | Answer                                                   |
| ------------------- | -------------------------------------------------------- |
| Pricing format      | **Ranges** - Market expects transparency but flexibility |
| Onboarding location | **Separate page** (/start) - Better for conversion       |
| Case studies        | **Separate pages** - SEO value, detailed metrics         |
| Price points        | **Based on Czech market** - 9.9K/24.9K/49.9K CZK         |

---

## Timeline Estimate

| Phase   | Focus                | Duration |
| ------- | -------------------- | -------- |
| Phase 1 | Theme Selector       | 20 min   |
| Phase 2 | Pricing + Onboarding | 40 min   |
| Phase 3 | Trust Signals        | 20 min   |
| Phase 4 | Content Pages        | 30 min   |

**Total**: ~110 minutes

---

_Plan Status: READY FOR EXECUTION_
_Last Updated: 2026-02-16_
