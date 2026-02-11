# Plan E: MVP Implementation

**Document Type:** Implementation Plan  
**Status:** Draft  
**Version:** 1.0  
**Created:** 2026-02-11  
**Project Phase:** MVP Implementation (Phase 5)  

---

## Executive Summary

Plan E represents the final implementation phase of the Marketing Portfolio Web App project. Following the completion of Plans A-D (configuration, setup, testing, and workflows), this plan focuses on executing the MVP development to deliver a production-ready, bilingual portfolio website.

The MVP implementation will transform the existing foundation into a fully functional portfolio showcasing DevOps and AI expertise to Czech and international markets. The implementation follows a structured seven-phase approach, beginning with template imports and concluding with deployment and monitoring.

**Key Objectives:**
- Import 11 critical bmad-skills and 2 rule files from agentic templates
- Populate real content (projects, case studies, testimonials)
- Implement remaining features (dark mode, language toggle, etc.)
- Achieve 95+ Lighthouse scores across all metrics
- Deploy to Debian 13 VPS with PM2 process management
- Configure Plausible analytics for privacy-focused tracking

**Success Criteria:**
- Lighthouse Performance ≥95, Accessibility ≥95, SEO ≥95
- LCP <2.0s, FID <100ms, CLS <0.1
- 10+ monthly contact form submissions
- 500+ monthly visits within 3 months
- Czech traffic representing 30%+ of total visitors

---

## Prerequisites

Before starting MVP implementation, the following prerequisites must be completed:

### Completed Prerequisites (Plans A-D)
- [x] Plan A: Agent Configuration - Kilo Code agents configured
- [x] Plan B: GitHub Setup - Repository initialized with workflows
- [x] Plan C: Keeper Agent - Template synchronization system ready
- [x] Plan D: Testing & Workflows - Vitest configured, Antigravity integrated

### Required Before Phase 1
- [ ] Keeper Agent tested and verified functional
- [ ] Development environment set up (npm install, npm run dev)
- [ ] Build verified (7 pages, exit code 0)
- [ ] Core components confirmed present (Hero, About, Projects, Services, Contact, Testimonials)

### Environment Variables Required
```bash
# Required for deployment
PROJECT_NAME=marketing-portfolio
PUBLIC_SITE_URL=https://marketing.tvoje.info
VPS_IP=<your-vps-ip-address>

# Optional but recommended
FORMSPREE_ENDPOINT=<your-formspree-endpoint>
PLAUSIBLE_API_KEY=<your-plausible-api-key>
```

### Tools and Access
- Node.js 20+ installed
- SSH access to Debian 13 VPS
- PM2 installed on VPS
- Formspree account configured
- Plausible analytics account configured

---

## Phase 1: Template Import

### Overview
Import 11 critical bmad-skills and 2 rule files from the agentic templates directory using the Keeper Agent. These templates provide specialized capabilities for testing, performance optimization, security, UX design, and development execution.

### Skills to Import

| # | Skill Name | Purpose | Priority |
|---|------------|---------|----------|
| 1 | bmad-test-strategy | Comprehensive testing methodology | Critical |
| 2 | bmad-performance-optimization | Performance optimization techniques | Critical |
| 3 | bmad-security-review | Security audit and review processes | Critical |
| 4 | bmad-ux-design | User experience design principles | Important |
| 5 | bmad-story-planning | User story planning and management | Important |
| 6 | bmad-development-execution | Development execution best practices | Critical |
| 7 | bmad-architecture-design | System architecture design patterns | Critical |
| 8 | bmad-observability-readiness | Monitoring and observability setup | Important |
| 9 | bmad-discovery-research | Research and discovery methodologies | Important |
| 10 | bmad-product-planning | Product planning and roadmap | Important |
| 11 | nodejs-runtime | Node.js runtime specific rules | Important |

### Rule Files to Import

| # | Rule File | Purpose | Priority |
|---|-----------|---------|----------|
| 1 | nodejs-runtime.md | Node.js runtime configuration | Critical |
| 2 | astro-portfolio.md | Astro portfolio best practices | Critical |

### Implementation Steps

#### Step 1.1: Verify Keeper Agent Status
```bash
# Test Keeper Agent analyze workflow
# Command: "Keeper analyze all"
```

**Expected Output:**
- List of available templates in `C:\Users\pavel\vscodeportable\agentic\`
- Comparison with local `.kilocode/` configurations
- Identification of missing templates

#### Step 1.2: Import bmad-skills
```bash
# Import all 11 bmad-skills
# Command: "Keeper import bmad-skills"
```

**Actions:**
1. Copy skill files from `C:\Users\pavel\vscodeportable\agentic\bmad-skills\yaml\`
2. Place in `.kilocode/skills/`
3. Verify each skill has proper frontmatter
4. Update skill documentation

**Verification:**
```bash
# List imported skills
ls .kilocode/skills/
```

Expected: 11 new skill directories with SKILL.md files

#### Step 1.3: Import Rule Files
```bash
# Import rule files
# Command: "Keeper import rules"
```

**Actions:**
1. Copy `nodejs-runtime.md` to `.kilocode/rules-code/`
2. Copy `astro-portfolio.md` to `.kilocode/rules-code/`
3. Verify rule file structure
4. Update rule documentation

**Verification:**
```bash
# List imported rules
ls .kilocode/rules-code/
```

Expected: 2 new rule files

#### Step 1.4: Validate Template Integration
```bash
# Run validation tests
npm run typecheck
npm run lint
```

**Success Criteria:**
- No TypeScript errors
- No ESLint warnings
- All skills properly formatted
- All rules properly configured

#### Step 1.5: Document Template Sources
Create `.kilocode/knowledge/template-sources.md`:
```markdown
# Template Sources

## Imported Skills
- bmad-test-strategy: Source C:\Users\pavel\vscodeportable\agentic\bmad-skills\yaml\
- bmad-performance-optimization: Source C:\Users\pavel\vscodeportable\agentic\bmad-skills\yaml\
- [List all 11 skills]

## Imported Rules
- nodejs-runtime.md: Source C:\Users\pavel\vscodeportable\agentic\kilocode-rules\rules-code\
- astro-portfolio.md: Source C:\Users\pavel\vscodeportable\agentic\kilocode-rules\rules-code\

## Import Date
2026-02-11
```

### Phase 1 Deliverables
- [ ] 11 bmad-skills imported to `.kilocode/skills/`
- [ ] 2 rule files imported to `.kilocode/rules-code/`
- [ ] Template sources documented
- [ ] Validation tests passing
- [ ] Keeper Agent import workflow verified

---

## Phase 2: Content Population

### Overview
Populate the portfolio with real, professional content including projects, case studies, testimonials, and service descriptions. Content must be bilingual (Czech/English) and aligned with the target personas.

### Content Structure

```
src/content/
├── projects/
│   ├── cloud-migration.md (existing)
│   ├── ai-implementation.md
│   ├── devops-transformation.md
│   └── performance-optimization.md
├── testimonials/
│   ├── tech-founder.md
│   ├── agency-cto.md
│   └── smb-owner.md
└── services/
    ├── devops-consulting.md
    ├── ai-integration.md
    └── cloud-architecture.md
```

### Implementation Steps

#### Step 2.1: Create Project Content

**Project 1: Cloud Migration (Enhance Existing)**
File: `src/content/projects/cloud-migration.md`

```yaml
---
title: Enterprise Cloud Migration
slug: cloud-migration
date: 2024-01-15
category: DevOps
client: TechCorp Prague
duration: 3 months
technologies:
  - AWS
  - Terraform
  - Kubernetes
  - CI/CD
---
```

**Content Requirements:**
- Problem statement (bilingual)
- Solution approach
- Implementation details
- Results and metrics
- Architecture diagram reference
- Technology stack details

**Project 2: AI Implementation**
File: `src/content/projects/ai-implementation.md`

```yaml
---
title: AI-Powered Analytics Platform
slug: ai-implementation
date: 2024-03-20
category: AI
client: DataFlow Analytics
duration: 4 months
technologies:
  - Python
  - TensorFlow
  - FastAPI
  - Docker
---
```

**Project 3: DevOps Transformation**
File: `src/content/projects/devops-transformation.md`

```yaml
---
title: DevOps Transformation Initiative
slug: devops-transformation
date: 2024-06-10
category: DevOps
client: ScaleUp Startup
duration: 6 months
technologies:
  - GitHub Actions
  - ArgoCD
  - Prometheus
  - Grafana
---
```

**Project 4: Performance Optimization**
File: `src/content/projects/performance-optimization.md`

```yaml
---
title: Performance Optimization Project
slug: performance-optimization
date: 2024-09-05
category: Performance
client: E-commerce Plus
duration: 2 months
technologies:
  - Redis
  - CDN
  - Database Optimization
  - Caching Strategies
---
```

#### Step 2.2: Create Testimonial Content

**Testimonial 1: Tech Founder**
File: `src/content/testimonials/tech-founder.md`

```yaml
---
name: Jan Novak
role: CEO & Founder
company: TechStartup Prague
project: Cloud Migration
rating: 5
---
```

**Content Requirements:**
- Quote (bilingual)
- Project context
- Results achieved
- Recommendation

**Testimonial 2: Agency CTO**
File: `src/content/testimonials/agency-cto.md`

```yaml
---
name: Petr Svoboda
role: CTO
company: Digital Agency Brno
project: DevOps Transformation
rating: 5
---
```

**Testimonial 3: SMB Owner**
File: `src/content/testimonials/smb-owner.md`

```yaml
---
name: Marie Dvorakova
role: Owner
company: Local Business Ostrava
project: Performance Optimization
rating: 5
---
```

#### Step 2.3: Create Service Content

**Service 1: DevOps Consulting**
File: `src/content/services/devops-consulting.md`

```yaml
---
title: DevOps Consulting
slug: devops-consulting
category: Services
pricing: Custom
---
```

**Content Requirements:**
- Service description (bilingual)
- Key features
- Process overview
- Pricing reference
- Case study links

**Service 2: AI Integration**
File: `src/content/services/ai-integration.md`

```yaml
---
title: AI Integration Services
slug: ai-integration
category: Services
pricing: Custom
---
```

**Service 3: Cloud Architecture**
File: `src/content/services/cloud-architecture.md`

```yaml
---
title: Cloud Architecture Design
slug: cloud-architecture
category: Services
pricing: Custom
---
```

#### Step 2.4: Update Translations

File: `src/i18n/translations.ts`

Add translations for:
- New project titles and descriptions
- New testimonials
- New service descriptions
- Navigation items
- Form labels and messages

**Translation Structure:**
```typescript
export const translations = {
  en: {
    // Existing translations
    // Add new translations
    projects: {
      cloudMigration: {
        title: "Enterprise Cloud Migration",
        description: "Complete cloud infrastructure migration..."
      },
      aiImplementation: {
        title: "AI-Powered Analytics Platform",
        description: "Machine learning integration for data analytics..."
      },
      // ... more projects
    },
    testimonials: {
      techFounder: {
        quote: "Exceptional technical expertise and communication...",
        // ... more fields
      },
      // ... more testimonials
    },
    services: {
      devopsConsulting: {
        title: "DevOps Consulting",
        description: "Comprehensive DevOps transformation services...",
        // ... more fields
      },
      // ... more services
    }
  },
  cs: {
    // Czech translations for all new content
  }
};
```

#### Step 2.5: Create About Section Content

File: `src/content/about/bio.md`

```yaml
---
title: About Me
slug: about
---
```

**Content Requirements:**
- Professional bio (bilingual)
- Career timeline
- Certifications
- Skills matrix
- Contact information

### Phase 2 Deliverables
- [ ] 4 project case studies (bilingual)
- [ ] 3 client testimonials (bilingual)
- [ ] 3 service descriptions (bilingual)
- [ ] About section content (bilingual)
- [ ] Updated translations file
- [ ] Content validation (no broken links, proper formatting)

---

## Phase 3: Feature Implementation

### Overview
Implement remaining MVP features including dark mode toggle, language toggle, form integration, and interactive components.

### Feature List

| # | Feature | Status | Priority |
|---|---------|--------|----------|
| 1 | Dark Mode Toggle | Pending | Critical |
| 2 | Language Toggle | Pending | Critical |
| 3 | Formspree Integration | Pending | Critical |
| 4 | Project Filtering | Pending | Important |
| 5 | Smooth Scrolling | Pending | Important |
| 6 | Mobile Navigation | Pending | Critical |
| 7 | Loading States | Pending | Important |

### Implementation Steps

#### Step 3.1: Dark Mode Toggle

**Component:** `src/components/common/DarkModeToggle.astro`

```astro
---
const isDark = false; // Will be reactive
---

<button
  id="dark-mode-toggle"
  aria-label="Toggle dark mode"
  class="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
>
  <span class="dark:hidden">🌙</span>
  <span class="hidden dark:inline">☀️</span>
</button>

<script>
  // Dark mode logic
  const toggle = document.getElementById('dark-mode-toggle');
  const html = document.documentElement;
  
  // Check system preference
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedTheme = localStorage.getItem('theme');
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    html.classList.add('dark');
  }
  
  toggle?.addEventListener('click', () => {
    html.classList.toggle('dark');
    localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
  });
</script>
```

**Integration:**
- Add to Header component
- Configure Tailwind dark mode in `tailwind.config.mjs`
- Add CSS variables for theme colors

#### Step 3.2: Language Toggle

**Component:** `src/components/common/LanguageToggle.astro`

```astro
---
const currentLang = 'en'; // Will be reactive
const languages = [
  { code: 'en', label: 'EN', flag: '🇬🇧' },
  { code: 'cs', label: 'CS', flag: '🇨🇿' }
];
---

<div class="flex items-center gap-2">
  {languages.map(lang => (
    <button
      class={`px-3 py-1 rounded-md transition-colors ${
        currentLang === lang.code
          ? 'bg-blue-600 text-white'
          : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600'
      }`}
      aria-label={`Switch to ${lang.label}`}
      data-lang={lang.code}
    >
      <span class="mr-1">{lang.flag}</span>
      {lang.label}
    </button>
  ))}
</div>

<script>
  // Language toggle logic
  const buttons = document.querySelectorAll('[data-lang]');
  
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.dataset.lang;
      localStorage.setItem('language', lang);
      // Navigate to language-specific route
      window.location.href = lang === 'cs' ? '/cs/' : '/';
    });
  });
</script>
```

**Integration:**
- Add to Header component
- Configure routing for language switching
- Persist language preference in localStorage

#### Step 3.3: Formspree Integration

**Component:** `src/components/sections/Contact.astro` (Update)

```astro
---
const formEndpoint = import.meta.env.FORMSPREE_ENDPOINT || 'https://formspree.io/f/your-form-id';
---

<form
  action={formEndpoint}
  method="POST"
  class="max-w-2xl mx-auto space-y-6"
>
  <div>
    <label for="name" class="block text-sm font-medium mb-2">
      Name / Jméno
    </label>
    <input
      type="text"
      id="name"
      name="name"
      required
      class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
    />
  </div>
  
  <div>
    <label for="email" class="block text-sm font-medium mb-2">
      Email
    </label>
    <input
      type="email"
      id="email"
      name="email"
      required
      class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
    />
  </div>
  
  <div>
    <label for="message" class="block text-sm font-medium mb-2">
      Message / Zpráva
    </label>
    <textarea
      id="message"
      name="message"
      rows="5"
      required
      class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
    ></textarea>
  </div>
  
  <div>
    <label class="flex items-start gap-2">
      <input
        type="checkbox"
        name="gdpr-consent"
        required
        class="mt-1"
      />
      <span class="text-sm">
        I consent to the processing of my personal data according to GDPR.
        / Souhlasím se zpracováním osobních údajů podle GDPR.
      </span>
    </label>
  </div>
  
  <button
    type="submit"
    class="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors"
  >
    Send Message / Odeslat zprávu
  </button>
</form>
```

**Configuration:**
- Set `FORMSPREE_ENDPOINT` in `.env`
- Configure Formspree account
- Set up email notifications
- Configure spam protection

#### Step 3.4: Project Filtering

**Component:** `src/components/sections/Projects.astro` (Update)

```astro
---
import { getCollection } from 'astro:content';

const projects = await getCollection('projects');
const categories = ['All', ...new Set(projects.map(p => p.data.category))];
---

<div class="mb-8">
  <div class="flex flex-wrap gap-2">
    {categories.map(category => (
      <button
        class="filter-btn px-4 py-2 rounded-full border transition-colors"
        data-category={category}
      >
        {category}
      </button>
    ))}
  </div>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {projects.map(project => (
    <article
      class="project-card"
      data-category={project.data.category}
    >
      <!-- Project card content -->
    </article>
  ))}
</div>

<script>
  // Filtering logic
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');
  
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const category = btn.dataset.category;
      
      // Update active button
      filterBtns.forEach(b => b.classList.remove('bg-blue-600', 'text-white'));
      btn.classList.add('bg-blue-600', 'text-white');
      
      // Filter projects
      projectCards.forEach(card => {
        if (category === 'All' || card.dataset.category === category) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
</script>
```

#### Step 3.5: Smooth Scrolling

**CSS:** `src/styles/global.css`

```css
html {
  scroll-behavior: smooth;
}

/* Offset for fixed header */
section {
  scroll-margin-top: 80px;
}
```

#### Step 3.6: Mobile Navigation

**Component:** `src/components/common/MobileNav.astro`

```astro
---
const isOpen = false;
---

<button
  id="mobile-menu-toggle"
  aria-label="Toggle menu"
  class="md:hidden p-2"
>
  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
  </svg>
</button>

<nav
  id="mobile-menu"
  class="hidden md:hidden fixed inset-0 bg-white dark:bg-gray-900 z-50"
>
  <div class="flex flex-col p-6 space-y-4">
    <!-- Navigation links -->
  </div>
</nav>

<script>
  const toggle = document.getElementById('mobile-menu-toggle');
  const menu = document.getElementById('mobile-menu');
  
  toggle?.addEventListener('click', () => {
    menu?.classList.toggle('hidden');
  });
</script>
```

#### Step 3.7: Loading States

**Component:** `src/components/ui/LoadingSpinner.astro`

```astro
---
---

<div class="flex items-center justify-center">
  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
</div>
```

### Phase 3 Deliverables
- [ ] Dark mode toggle implemented
- [ ] Language toggle implemented
- [ ] Formspree form integrated
- [ ] Project filtering functional
- [ ] Smooth scrolling enabled
- [ ] Mobile navigation working
- [ ] Loading states added
- [ ] All features tested

---

## Phase 4: Performance Optimization

### Overview
Optimize the portfolio to achieve 95+ Lighthouse scores across all metrics. This phase focuses on Core Web Vitals, bundle size reduction, and asset optimization.

### Performance Targets

| Metric | Target | Current | Gap |
|--------|--------|---------|-----|
| Lighthouse Performance | ≥95 | TBD | TBD |
| Lighthouse Accessibility | ≥95 | TBD | TBD |
| Lighthouse SEO | ≥95 | TBD | TBD |
| LCP | <2.0s | TBD | TBD |
| FID | <100ms | TBD | TBD |
| CLS | <0.1 | TBD | TBD |
| Bundle Size | <50KB | TBD | TBD |

### Implementation Steps

#### Step 4.1: Image Optimization

**Actions:**
1. Convert all images to WebP/AVIF format
2. Implement lazy loading for below-fold images
3. Add responsive image sources
4. Optimize image sizes

**Implementation:**

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---

<picture>
  <source srcset={heroImage.src} type="image/avif" />
  <source srcset={heroImage.src} type="image/webp" />
  <Image
    src={heroImage}
    alt="Hero image"
    loading="eager"
    width={1200}
    height={600}
    class="w-full h-auto"
  />
</picture>
```

**Configuration:** `astro.config.mjs`

```javascript
export default defineConfig({
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
    },
    sharp: {
      formats: ['webp', 'avif', 'jpeg'],
    },
  },
});
```

#### Step 4.2: Code Splitting

**Actions:**
1. Implement Astro island architecture
2. Lazy load non-critical components
3. Use dynamic imports for heavy libraries

**Implementation:**

```astro
---
// Lazy load interactive components
const InteractiveMap = await import('../components/InteractiveMap.astro');
---

<InteractiveMap.client:load />
```

#### Step 4.3: CSS Optimization

**Actions:**
1. Purge unused CSS
2. Minify CSS
3. Inline critical CSS
4. Use CSS containment

**Configuration:** `tailwind.config.mjs`

```javascript
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      // Custom theme
    },
  },
  plugins: [],
};
```

#### Step 4.4: Font Optimization

**Actions:**
1. Subset fonts to include only used characters
2. Use font-display: swap
3. Preload critical fonts
4. Implement font loading strategy

**Implementation:** `src/layouts/Layout.astro`

```astro
<link
  rel="preload"
  href="/fonts/inter-subset.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>

<style>
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/inter-subset.woff2') format('woff2');
    font-display: swap;
  }
</style>
```

#### Step 4.5: JavaScript Optimization

**Actions:**
1. Minify JavaScript
2. Remove unused code
3. Use tree shaking
4. Implement code splitting

**Configuration:** `astro.config.mjs`

```javascript
export default defineConfig({
  build: {
    minify: 'esbuild',
  },
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom'],
          },
        },
      },
    },
  },
});
```

#### Step 4.6: Caching Strategy

**Actions:**
1. Implement browser caching headers
2. Use CDN caching
3. Implement service worker for offline support
4. Cache API responses

**Configuration:** `public/_headers`

```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin

/*.js
  Cache-Control: public, max-age=31536000, immutable

/*.css
  Cache-Control: public, max-age=31536000, immutable

/*.woff2
  Cache-Control: public, max-age=31536000, immutable

/*.webp
  Cache-Control: public, max-age=31536000, immutable

/*.avif
  Cache-Control: public, max-age=31536000, immutable
```

#### Step 4.7: Performance Monitoring

**Actions:**
1. Implement Web Vitals monitoring
2. Set up Lighthouse CI
3. Configure performance budgets
4. Create performance dashboard

**Configuration:** `lighthouserc.json`

```json
{
  "ci": {
    "collect": {
      "staticDistDir": "./dist",
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.95 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:seo": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["error", { "minScore": 0.95 }]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

### Phase 4 Deliverables
- [ ] All images optimized (WebP/AVIF)
- [ ] Lazy loading implemented
- [ ] Code splitting configured
- [ ] CSS purged and minified
- [ ] Fonts optimized
- [ ] JavaScript minified
- [ ] Caching strategy implemented
- [ ] Performance monitoring configured
- [ ] Lighthouse scores ≥95

---

## Phase 5: Testing & QA

### Overview
Comprehensive testing using bmad-test-strategy skill to ensure quality, accessibility, and performance standards are met.

### Testing Strategy

Based on bmad-test-strategy skill, implement:

1. **Unit Testing** - Test individual components and functions
2. **Integration Testing** - Test component interactions
3. **E2E Testing** - Test user flows
4. **Accessibility Testing** - WCAG 2.2 AA compliance
5. **Performance Testing** - Core Web Vitals
6. **Security Testing** - Vulnerability scanning
7. **Cross-Browser Testing** - Browser compatibility
8. **Responsive Testing** - Mobile-first design

### Implementation Steps

#### Step 5.1: Unit Testing

**Framework:** Vitest (already configured)

**Test Files:**
- `tests/unit/components/Button.test.ts`
- `tests/unit/components/Card.test.ts`
- `tests/unit/utils/i18n.test.ts`
- `tests/unit/utils/formatters.test.ts`

**Example Test:**

```typescript
// tests/unit/components/Button.test.ts
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Button from '../../src/components/ui/Button.astro';

describe('Button Component', () => {
  it('renders with correct text', () => {
    const { getByText } = render(Button, { props: { text: 'Click me' } });
    expect(getByText('Click me')).toBeInTheDocument();
  });

  it('applies correct variant classes', () => {
    const { container } = render(Button, { props: { variant: 'primary' } });
    expect(container.firstChild).toHaveClass('bg-blue-600');
  });

  it('is accessible with keyboard', () => {
    const { getByRole } = render(Button, { props: { text: 'Submit' } });
    const button = getByRole('button');
    expect(button).toHaveAttribute('type', 'button');
  });
});
```

#### Step 5.2: Integration Testing

**Test Files:**
- `tests/integration/navigation.test.ts`
- `tests/integration/language-toggle.test.ts`
- `tests/integration/form-submission.test.ts`
- `tests/integration/project-filtering.test.ts`

**Example Test:**

```typescript
// tests/integration/language-toggle.test.ts
import { describe, it, expect } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import LanguageToggle from '../../src/components/common/LanguageToggle.astro';

describe('Language Toggle Integration', () => {
  it('switches language on click', () => {
    const { getByLabelText } = render(LanguageToggle);
    const csButton = getByLabelText('Switch to CS');
    
    fireEvent.click(csButton);
    
    expect(localStorage.getItem('language')).toBe('cs');
  });

  it('persists language preference', () => {
    localStorage.setItem('language', 'cs');
    const { getByLabelText } = render(LanguageToggle);
    const csButton = getByLabelText('Switch to CS');
    
    expect(csButton).toHaveClass('bg-blue-600');
  });
});
```

#### Step 5.3: E2E Testing

**Framework:** Playwright

**Test Files:**
- `tests/e2e/user-journey.spec.ts`
- `tests/e2e/contact-form.spec.ts`
- `tests/e2e/project-viewing.spec.ts`

**Example Test:**

```typescript
// tests/e2e/user-journey.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Journey', () => {
  test('complete user flow from landing to contact', async ({ page }) => {
    await page.goto('/');
    
    // Navigate to projects
    await page.click('text=Projects');
    await expect(page).toHaveURL('/projects');
    
    // View project details
    await page.click('text=Cloud Migration');
    await expect(page.locator('h1')).toContainText('Enterprise Cloud Migration');
    
    // Navigate to contact
    await page.click('text=Contact');
    await expect(page).toHaveURL('/#contact');
    
    // Fill form
    await page.fill('input[name="name"]', 'Test User');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('textarea[name="message"]', 'Test message');
    await page.check('input[name="gdpr-consent"]');
    
    // Submit form
    await page.click('button[type="submit"]');
    await expect(page.locator('.success-message')).toBeVisible();
  });
});
```

#### Step 5.4: Accessibility Testing

**Tools:**
- axe-core
- Lighthouse Accessibility
- WAVE
- Keyboard navigation testing

**Test Files:**
- `tests/accessibility/a11y.test.ts`
- `tests/accessibility/keyboard.test.ts`
- `tests/accessibility/contrast.test.ts`

**Example Test:**

```typescript
// tests/accessibility/a11y.test.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage has no accessibility violations', async ({ page }) => {
    await page.goto('/');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('all interactive elements are keyboard accessible', async ({ page }) => {
    await page.goto('/');
    
    const buttons = await page.$$('button, a, input, select, textarea');
    
    for (const button of buttons) {
      await button.focus();
      expect(await button.evaluate(el => document.activeElement === el)).toBe(true);
    }
  });
});
```

#### Step 5.5: Performance Testing

**Tools:**
- Lighthouse CI
- WebPageTest
- Chrome DevTools

**Test Files:**
- `tests/performance/lighthouse.test.ts`
- `tests/performance/core-web-vitals.test.ts`

**Example Test:**

```typescript
// tests/performance/lighthouse.test.ts
import { test, expect } from '@playwright/test';

test.describe('Performance', () => {
  test('homepage meets Lighthouse performance targets', async ({ page }) => {
    await page.goto('/');
    
    const metrics = await page.evaluate(() => {
      return {
        lcp: performance.getEntriesByType('largest-contentful-paint')[0]?.startTime,
        fid: performance.getEntriesByType('first-input')[0]?.processingStart,
        cls: performance.getEntriesByType('layout-shift')
          .reduce((sum, entry) => sum + (entry.value || 0), 0),
      };
    });
    
    expect(metrics.lcp).toBeLessThan(2000);
    expect(metrics.fid).toBeLessThan(100);
    expect(metrics.cls).toBeLessThan(0.1);
  });
});
```

#### Step 5.6: Security Testing

**Tools:**
- npm audit
- Snyk
- OWASP ZAP

**Test Files:**
- `tests/security/dependencies.test.ts`
- `tests/security/headers.test.ts`
- `tests/security/xss.test.ts`

**Example Test:**

```typescript
// tests/security/dependencies.test.ts
import { describe, it, expect } from 'vitest';
import { execSync } from 'child_process';

describe('Security', () => {
  it('has no high-severity vulnerabilities', () => {
    const result = execSync('npm audit --json', { encoding: 'utf-8' });
    const audit = JSON.parse(result);
    
    const highVulns = audit.vulnerabilities?.high || 0;
    const criticalVulns = audit.vulnerabilities?.critical || 0;
    
    expect(highVulns).toBe(0);
    expect(criticalVulns).toBe(0);
  });
});
```

#### Step 5.7: Cross-Browser Testing

**Browsers:**
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

**Test Matrix:**

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | Latest | ✅ |
| Firefox | Latest | ✅ |
| Safari | Latest | ✅ |
| Edge | Latest | ✅ |

#### Step 5.8: Responsive Testing

**Viewports:**
- Mobile: 375x667 (iPhone SE)
- Tablet: 768x1024 (iPad)
- Desktop: 1920x1080 (Full HD)

**Test Files:**
- `tests/responsive/mobile.test.ts`
- `tests/responsive/tablet.test.ts`
- `tests/responsive/desktop.test.ts`

### Phase 5 Deliverables
- [ ] Unit tests passing (80%+ coverage)
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Accessibility tests passing (WCAG 2.2 AA)
- [ ] Performance tests passing (95+ Lighthouse)
- [ ] Security tests passing
- [ ] Cross-browser tests passing
- [ ] Responsive tests passing
- [ ] Test documentation complete

---

## Phase 6: Deployment

### Overview
Deploy the portfolio to Debian 13 VPS with PM2 process management. Configure SSL, set up monitoring, and establish CI/CD pipeline.

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Main Branch │  │ Pull Request│  │ GitHub Actions      │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼──────────────┘
          │                │                       │
          ▼                ▼                       ▼
    ┌──────────┐    ┌──────────┐          ┌──────────────┐
    │  Build   │    │   Test   │          │   Deploy     │
    │  (npm)   │    │ (Vitest) │          │   (SSH)      │
    └────┬─────┘    └────┬─────┘          └──────┬───────┘
         │                │                       │
         └────────────────┴───────────────────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │      Debian 13 VPS          │
              │  ┌───────────────────────┐  │
              │  │  PM2 Process Manager  │  │
              │  │  ┌─────────────────┐  │  │
              │  │  │  Astro Server   │  │  │
              │  │  │  (Port 4321)    │  │  │
              │  │  └─────────────────┘  │  │
              │  └───────────────────────┘  │
              │  ┌───────────────────────┐  │
              │  │  Nginx Reverse Proxy  │  │
              │  │  (Port 80/443)        │  │
              │  └───────────────────────┘  │
              └─────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │  marketing.tvoje.info       │
              │  (SSL Certificate)          │
              └─────────────────────────────┘
```

### Implementation Steps

#### Step 6.1: VPS Preparation

**Actions:**
1. Update system packages
2. Install Node.js 20+
3. Install PM2
4. Install Nginx
5. Configure firewall
6. Set up SSH keys

**Commands:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 20+
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install PM2
sudo npm install -g pm2

# Install Nginx
sudo apt install -y nginx

# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

#### Step 6.2: Application Setup

**Actions:**
1. Clone repository
2. Install dependencies
3. Build application
4. Configure environment variables
5. Test locally

**Commands:**

```bash
# Clone repository
cd /var/www
sudo git clone https://github.com/pkoka888/marketing.tvoje.info.git
cd marketing.tvoje.info

# Install dependencies
npm install

# Build application
npm run build

# Create .env file
sudo nano .env
```

**.env Template:**

```bash
PROJECT_NAME=marketing-portfolio
PUBLIC_SITE_URL=https://marketing.tvoje.info
VPS_IP=<your-vps-ip>
FORMSPREE_ENDPOINT=<your-formspree-endpoint>
PLAUSIBLE_API_KEY=<your-plausible-api-key>
```

#### Step 6.3: PM2 Configuration

**File:** `ecosystem.config.cjs`

```javascript
module.exports = {
  apps: [{
    name: 'marketing-portfolio',
    script: 'node',
    args: './dist/server/entry.mjs',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PORT: 4321
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true
  }]
};
```

**Commands:**

```bash
# Start application with PM2
pm2 start ecosystem.config.cjs

# Save PM2 configuration
pm2 save

# Setup PM2 startup script
pm2 startup
```

#### Step 6.4: Nginx Configuration

**File:** `/etc/nginx/sites-available/marketing.tvoje.info`

```nginx
server {
    listen 80;
    server_name marketing.tvoje.info www.marketing.tvoje.info;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name marketing.tvoje.info www.marketing.tvoje.info;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/marketing.tvoje.info/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/marketing.tvoje.info/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://plausible.io; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://plausible.io https://formspree.io;" always;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json application/javascript;

    # Proxy to Astro
    location / {
        proxy_pass http://localhost:4321;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://localhost:4321;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Commands:**

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/marketing.tvoje.info /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

#### Step 6.5: SSL Certificate Setup

**Commands:**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d marketing.tvoje.info -d www.marketing.tvoje.info

# Setup auto-renewal
sudo certbot renew --dry-run
```

#### Step 6.6: CI/CD Pipeline

**File:** `.github/workflows/deploy.yml`

```yaml
name: Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build application
        run: npm run build
        env:
          PUBLIC_SITE_URL: https://marketing.tvoje.info
      
      - name: Deploy to VPS
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_IP }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/marketing.tvoje.info
            git pull origin main
            npm install
            npm run build
            pm2 restart marketing-portfolio
```

**GitHub Secrets Required:**
- `VPS_IP`
- `VPS_USER`
- `SSH_PRIVATE_KEY`

#### Step 6.7: Monitoring Setup

**PM2 Monitoring:**

```bash
# Install PM2 Plus (optional)
pm2 plus

# Monitor application
pm2 monit
```

**Log Monitoring:**

```bash
# View logs
pm2 logs marketing-portfolio

# Setup log rotation
pm2 install pm2-logrotate
```

### Phase 6 Deliverables
- [ ] VPS configured and secured
- [ ] Application deployed with PM2
- [ ] Nginx reverse proxy configured
- [ ] SSL certificate installed
- [ ] CI/CD pipeline active
- [ ] Monitoring configured
- [ ] Backup strategy implemented
- [ ] Documentation complete

---

## Phase 7: Monitoring & Analytics

### Overview
Configure Plausible analytics for privacy-focused tracking and set up monitoring dashboards for performance and uptime.

### Analytics Configuration

#### Step 7.1: Plausible Setup

**Account Setup:**
1. Create Plausible account
2. Add site: `marketing.tvoje.info`
3. Get tracking script
4. Configure goals

**Integration:** `src/layouts/Layout.astro`

```astro
---
const plausibleDomain = import.meta.env.PUBLIC_SITE_URL || 'marketing.tvoje.info';
---

<script
  defer
  data-domain={plausibleDomain}
  src="https://plausible.io/js/script.js"
></script>
```

**Environment Variable:**

```bash
# .env
PUBLIC_SITE_URL=https://marketing.tvoje.info
PLAUSIBLE_API_KEY=<your-api-key>
```

#### Step 7.2: Goals Configuration

**Plausible Goals:**
1. Contact form submission
2. Project detail view
3. Service page view
4. External link click
5. Scroll depth (50%, 75%, 100%)

**Implementation:**

```astro
---
// Contact form submission
---

<form
  action={formEndpoint}
  method="POST"
  data-event="contact-form-submit"
>
  <!-- Form fields -->
</form>

<script>
  // Track form submission
  const form = document.querySelector('form[data-event="contact-form-submit"]');
  form?.addEventListener('submit', () => {
    window.plausible('contact-form-submit');
  });
</script>
```

#### Step 7.3: Custom Events

**Events to Track:**
- `project-view` - When user views project details
- `service-view` - When user views service details
- `language-switch` - When user switches language
- `dark-mode-toggle` - When user toggles dark mode
- `external-link-click` - When user clicks external link

**Implementation:**

```astro
---
// Project view tracking
---

<script>
  // Track project view
  window.plausible('project-view', {
    props: {
      project: 'cloud-migration',
      category: 'DevOps'
    }
  });
</script>
```

### Monitoring Setup

#### Step 7.4: Uptime Monitoring

**Tools:**
- UptimeRobot (free tier)
- Pingdom (paid)
- StatusCake (free tier)

**Configuration:**

```yaml
# UptimeRobot configuration
monitors:
  - name: Marketing Portfolio
    url: https://marketing.tvoje.info
    interval: 300
    alert_contacts:
      - email: admin@tvoje.info
```

#### Step 7.5: Performance Monitoring

**Tools:**
- Lighthouse CI
- WebPageTest
- PageSpeed Insights API

**Configuration:**

```javascript
// lighthouserc.json
{
  "ci": {
    "collect": {
      "staticDistDir": "./dist",
      "numberOfRuns": 3
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

#### Step 7.6: Error Monitoring

**Tools:**
- Sentry (optional)
- LogRocket (optional)
- Custom error logging

**Implementation:**

```astro
---
// Error boundary
---

<script>
  // Global error handler
  window.addEventListener('error', (event) => {
    console.error('Error:', event.error);
    // Send to error tracking service
  });

  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    // Send to error tracking service
  });
</script>
```

#### Step 7.7: Dashboard Setup

**Metrics to Track:**
- Page views
- Unique visitors
- Bounce rate
- Average session duration
- Top pages
- Traffic sources
- Device breakdown
- Geographic distribution
- Conversion rate

**Dashboard Tools:**
- Plausible dashboard
- Google Data Studio (optional)
- Custom Grafana dashboard (optional)

### Phase 7 Deliverables
- [ ] Plausible analytics configured
- [ ] Goals and events set up
- [ ] Uptime monitoring active
- [ ] Performance monitoring configured
- [ ] Error monitoring set up
- [ ] Dashboard configured
- [ ] Reports scheduled
- [ ] Documentation complete

---

## Timeline & Milestones

### Phase Timeline

| Phase | Duration | Start Date | End Date | Status |
|-------|----------|------------|----------|--------|
| Phase 1: Template Import | 1 day | TBD | TBD | Pending |
| Phase 2: Content Population | 3 days | TBD | TBD | Pending |
| Phase 3: Feature Implementation | 4 days | TBD | TBD | Pending |
| Phase 4: Performance Optimization | 3 days | TBD | TBD | Pending |
| Phase 5: Testing & QA | 3 days | TBD | TBD | Pending |
| Phase 6: Deployment | 2 days | TBD | TBD | Pending |
| Phase 7: Monitoring & Analytics | 1 day | TBD | TBD | Pending |
| **Total** | **17 days** | **TBD** | **TBD** | **Pending** |

### Milestones

| Milestone | Description | Target Date | Status |
|-----------|-------------|-------------|--------|
| M1: Templates Imported | All 11 bmad-skills and 2 rule files imported | TBD | Pending |
| M2: Content Complete | All bilingual content created and validated | TBD | Pending |
| M3: Features Implemented | All MVP features functional | TBD | Pending |
| M4: Performance Targets Met | Lighthouse scores ≥95 | TBD | Pending |
| M5: Testing Complete | All tests passing | TBD | Pending |
| M6: Deployed to Production | Live on marketing.tvoje.info | TBD | Pending |
| M7: Monitoring Active | Analytics and monitoring configured | TBD | Pending |

### Dependencies

```
Phase 1 (Template Import)
    ↓
Phase 2 (Content Population)
    ↓
Phase 3 (Feature Implementation)
    ↓
Phase 4 (Performance Optimization)
    ↓
Phase 5 (Testing & QA)
    ↓
Phase 6 (Deployment)
    ↓
Phase 7 (Monitoring & Analytics)
```

### Critical Path

1. Template Import → Content Population → Feature Implementation
2. Feature Implementation → Performance Optimization → Testing
3. Testing → Deployment → Monitoring

---

## Success Metrics

### Performance Metrics

| Metric | Target | Measurement Tool | Frequency |
|--------|--------|------------------|----------|
| Lighthouse Performance | ≥95 | Lighthouse CI | Per build |
| Lighthouse Accessibility | ≥95 | Lighthouse CI | Per build |
| Lighthouse SEO | ≥95 | Lighthouse CI | Per build |
| LCP | <2.0s | PageSpeed Insights | Daily |
| FID | <100ms | PageSpeed Insights | Daily |
| CLS | <0.1 | PageSpeed Insights | Daily |
| Bundle Size | <50KB | Bundle analyzer | Per build |

### Engagement Metrics

| Metric | Target | Measurement Tool | Frequency |
|--------|--------|------------------|----------|
| Monthly Visits | 500+ | Plausible | Monthly |
| Average Time on Page | 3+ min | Plausible | Monthly |
| Bounce Rate | <40% | Plausible | Monthly |
| Scroll Depth | >70% | Plausible | Monthly |
| Pages per Session | 3+ | Plausible | Monthly |

### Conversion Metrics

| Metric | Target | Measurement Tool | Frequency |
|--------|--------|------------------|----------|
| Contact Form Submissions | 10+/month | Formspree | Monthly |
| Consultation Requests | 5+/month | Formspree | Monthly |
| Portfolio Views | 2000+/month | Plausible | Monthly |
| Conversion Rate | 5% | Plausible | Monthly |

### Reach Metrics

| Metric | Target | Measurement Tool | Frequency |
|--------|--------|------------------|----------|
| Domain Authority | 20+ | Moz | Monthly |
| Backlinks | 50+ | Ahrefs | Monthly |
| Social Shares | 100+/month | Social media | Monthly |
| Brand Mentions | 10+/month | Google Alerts | Monthly |
| Organic Keywords | 50+ | Google Search Console | Monthly |
| Referral Visits | 100+/month | Plausible | Monthly |

### Czech-Specific Metrics

| Metric | Target | Measurement Tool | Frequency |
|--------|--------|------------------|----------|
| Google.cz Ranking | Top 10 | Google Search Console | Monthly |
| Seznam.cz Ranking | Top 20 | Seznam Search Console | Monthly |
| Czech Traffic | 30%+ | Plausible | Monthly |
| Czech Keywords | 20+ | Google Search Console | Monthly |

### Technical Metrics

| Metric | Target | Measurement Tool | Frequency |
|--------|--------|------------------|----------|
| Uptime | 99.9% | UptimeRobot | Continuous |
| Response Time | <200ms | Pingdom | Continuous |
| Error Rate | <0.1% | PM2 logs | Continuous |
| Build Success Rate | 100% | GitHub Actions | Per build |

---

## Risk Assessment

### Risk Matrix

| Risk | Probability | Impact | Severity | Mitigation Strategy |
|------|-------------|--------|----------|-------------------|
| Template Import Failure | Low | High | Medium | Test Keeper Agent before Phase 1, have manual fallback |
| Content Translation Errors | Medium | Medium | Medium | Use professional translation, peer review |
| Performance Targets Not Met | Medium | High | High | Early performance testing, optimization buffer |
| Testing Failures | Medium | Medium | Medium | Incremental testing, parallel development |
| Deployment Issues | Low | High | Medium | Staging environment, rollback plan |
| VPS Downtime | Low | High | Medium | Redundancy, monitoring, backup |
| Security Vulnerabilities | Low | High | Medium | Regular audits, dependency updates |
| Analytics Configuration Errors | Low | Medium | Low | Test in staging, documentation |
| Third-Party Service Outage | Low | Medium | Low | Service level agreements, alternatives |
| Scope Creep | Medium | Medium | Medium | Clear requirements, change control |

### Detailed Risk Analysis

#### Risk 1: Template Import Failure

**Description:** Keeper Agent fails to import templates from agentic directory.

**Probability:** Low  
**Impact:** High  
**Severity:** Medium

**Mitigation:**
1. Test Keeper Agent thoroughly before Phase 1
2. Have manual import procedure documented
3. Keep backup of existing configurations
4. Verify template sources are accessible

**Contingency:**
- Manual copy of template files
- Use alternative import method
- Skip non-critical templates

#### Risk 2: Content Translation Errors

**Description:** Czech translations contain errors or cultural misunderstandings.

**Probability:** Medium  
**Impact:** Medium  
**Severity:** Medium

**Mitigation:**
1. Use professional translation service
2. Peer review by native Czech speaker
3. Cultural validation by Czech market expert
4. A/B testing of translated content

**Contingency:**
- Post-launch corrections
- User feedback collection
- Iterative improvements

#### Risk 3: Performance Targets Not Met

**Description:** Lighthouse scores below 95 or Core Web Vitals not met.

**Probability:** Medium  
**Impact:** High  
**Severity:** High

**Mitigation:**
1. Early performance baseline measurement
2. Incremental optimization with testing
3. Performance budget enforcement
4. Regular Lighthouse CI runs

**Contingency:**
- Extended optimization phase
- Feature scope reduction
- Alternative optimization techniques

#### Risk 4: Testing Failures

**Description:** Tests fail blocking deployment.

**Probability:** Medium  
**Impact:** Medium  
**Severity:** Medium

**Mitigation:**
1. Incremental testing during development
2. Parallel test and feature development
3. Test-driven development approach
4. Regular test suite reviews

**Contingency:**
- Bug fixes and retesting
- Test suite adjustments
- Deployment with known issues (documented)

#### Risk 5: Deployment Issues

**Description:** Deployment to VPS fails or causes downtime.

**Probability:** Low  
**Impact:** High  
**Severity:** Medium

**Mitigation:**
1. Staging environment for testing
2. Rollback plan documented
3. Blue-green deployment strategy
4. Deployment checklist

**Contingency:**
- Immediate rollback
- Hotfix deployment
- Extended maintenance window

#### Risk 6: VPS Downtime

**Description:** VPS experiences extended downtime.

**Probability:** Low  
**Impact:** High  
**Severity:** Medium

**Mitigation:**
1. Redundant backup server
2. Monitoring and alerting
3. Regular backups
4. Disaster recovery plan

**Contingency:**
- Failover to backup
- Emergency maintenance
- Communication plan

#### Risk 7: Security Vulnerabilities

**Description:** Security vulnerabilities discovered in dependencies or code.

**Probability:** Low  
**Impact:** High  
**Severity:** Medium

**Mitigation:**
1. Regular security audits
2. Automated dependency scanning
3. Code review process
4. Security best practices

**Contingency:**
- Immediate patching
- Security advisory
- Incident response plan

#### Risk 8: Analytics Configuration Errors

**Description:** Plausible analytics not tracking correctly.

**Probability:** Low  
**Impact:** Medium  
**Severity:** Low

**Mitigation:**
1. Test in staging environment
2. Verify tracking script
3. Validate goals and events
4. Documentation

**Contingency:**
- Reconfiguration
- Alternative analytics tool
- Manual tracking

#### Risk 9: Third-Party Service Outage

**Description:** Formspree or Plausible experiences outage.

**Probability:** Low  
**Impact:** Medium  
**Severity:** Low

**Mitigation:**
1. Service level agreements
2. Alternative services identified
3. Graceful degradation
4. User communication

**Contingency:**
- Switch to alternative
- Temporary disable feature
- Extended outage communication

#### Risk 10: Scope Creep

**Description:** Additional features requested during implementation.

**Probability:** Medium  
**Impact:** Medium  
**Severity:** Medium

**Mitigation:**
1. Clear requirements document
2. Change control process
3. Stakeholder alignment
4. Regular progress reviews

**Contingency:**
- Feature deferral to v1.1
- Scope reduction
- Timeline extension

### Risk Monitoring

**Weekly Risk Review:**
- Update risk status
- Assess new risks
- Review mitigation effectiveness
- Update contingency plans

**Risk Escalation:**
- High severity risks → Project lead
- Critical issues → Stakeholders
- Blockers → Emergency meeting

---

## Appendix

### A. File Structure Reference

```
marketing.tvoje.info/
├── .kilocode/
│   ├── skills/                    # Imported bmad-skills
│   │   ├── bmad-test-strategy/
│   │   ├── bmad-performance-optimization/
│   │   ├── bmad-security-review/
│   │   ├── bmad-ux-design/
│   │   ├── bmad-story-planning/
│   │   ├── bmad-development-execution/
│   │   ├── bmad-architecture-design/
│   │   ├── bmad-observability-readiness/
│   │   ├── bmad-discovery-research/
│   │   ├── bmad-product-planning/
│   │   └── nodejs-runtime/
│   ├── rules-code/                # Imported rules
│   │   ├── nodejs-runtime.md
│   │   └── astro-portfolio.md
│   ├── rules-keeper/              # Keeper Agent
│   │   ├── analyze.md
│   │   └── sync.md
│   ├── workflows/                 # Workflows
│   │   ├── keeper-analyze.md
│   │   ├── keeper-import.md
│   │   └── keeper-sync.md
│   └── knowledge/                 # Documentation
│       ├── keeper-sources.md
│       └── template-sources.md
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.astro
│   │   │   ├── Footer.astro
│   │   │   ├── DarkModeToggle.astro
│   │   │   ├── LanguageToggle.astro
│   │   │   └── MobileNav.astro
│   │   ├── sections/
│   │   │   ├── Hero.astro
│   │   │   ├── About.astro
│   │   │   ├── Projects.astro
│   │   │   ├── Services.astro
│   │   │   ├── Testimonials.astro
│   │   │   └── Contact.astro
│   │   └── ui/
│   │       ├── Button.astro
│   │       ├── Card.astro
│   │       ├── Badge.astro
│   │       └── LoadingSpinner.astro
│   ├── content/
│   │   ├── projects/
│   │   │   ├── cloud-migration.md
│   │   │   ├── ai-implementation.md
│   │   │   ├── devops-transformation.md
│   │   │   └── performance-optimization.md
│   │   ├── testimonials/
│   │   │   ├── tech-founder.md
│   │   │   ├── agency-cto.md
│   │   │   └── smb-owner.md
│   │   ├── services/
│   │   │   ├── devops-consulting.md
│   │   │   ├── ai-integration.md
│   │   │   └── cloud-architecture.md
│   │   └── about/
│   │       └── bio.md
│   ├── i18n/
│   │   └── translations.ts
│   ├── layouts/
│   │   └── Layout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── cs/
│   │   │   └── index.astro
│   │   └── projects/
│   │       ├── index.astro
│   │       └── [slug].astro
│   └── styles/
│       └── global.css
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── accessibility/
│   ├── performance/
│   ├── security/
│   └── responsive/
├── public/
│   ├── fonts/
│   ├── images/
│   └── _headers
├── plans/
│   └── plan-e-mvp-implementation.md
├── .github/
│   └── workflows/
│       └── deploy.yml
├── ecosystem.config.cjs
├── astro.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
├── vitest.config.ts
├── lighthouserc.json
├── package.json
└── .env
```

### B. Command Reference

**Development Commands:**
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run typecheck    # Run TypeScript checks
npm run format       # Format code with Prettier
npm test             # Run all tests
```

**Deployment Commands:**
```bash
pm2 start ecosystem.config.cjs    # Start with PM2
pm2 restart marketing-portfolio   # Restart application
pm2 stop marketing-portfolio      # Stop application
pm2 logs marketing-portfolio      # View logs
pm2 monit                          # Monitor application
```

**VPS Commands:**
```bash
sudo systemctl restart nginx      # Restart Nginx
sudo nginx -t                     # Test Nginx config
sudo certbot renew                # Renew SSL certificate
```

### C. Environment Variables

```bash
# Required
PROJECT_NAME=marketing-portfolio
PUBLIC_SITE_URL=https://marketing.tvoje.info
VPS_IP=<your-vps-ip>

# Optional
FORMSPREE_ENDPOINT=<your-formspree-endpoint>
PLAUSIBLE_API_KEY=<your-plausible-api-key>
```

### D. Useful Resources

**Documentation:**
- [Astro Documentation](https://docs.astro.build)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Vitest Documentation](https://vitest.dev)
- [PM2 Documentation](https://pm2.keymetrics.io/docs)
- [Nginx Documentation](https://nginx.org/en/docs)

**Tools:**
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Plausible Analytics](https://plausible.io)
- [Formspree](https://formspree.io)
- [Playwright](https://playwright.dev)

**Standards:**
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/)
- [Core Web Vitals](https://web.dev/vitals/)
- [GDPR](https://gdpr.eu/)

### E. Contact Information

**Project Lead:** [Your Name]  
**Email:** admin@tvoje.info  
**GitHub:** https://github.com/pkoka888/marketing.tvoje.info  
**VPS:** marketing.tvoje.info

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-11 | Kilo Code | Initial Plan E creation |

---

**End of Plan E: MVP Implementation**
