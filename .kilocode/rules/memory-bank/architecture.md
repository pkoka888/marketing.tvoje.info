# System Architecture

## Architecture Overview

The Marketing Portfolio Web App follows a modern static site architecture using
Astro 5.0's island architecture for optimal performance and minimal JavaScript
delivery.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Content Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  Markdown/MDX Files  │  Components  │  Data (JSON/YAML)         │
│  - Blog posts        │  - Reusable  │  - Project metadata       │
│  - Case studies      │    UI blocks │  - Testimonial data      │
│  - Pages             │  - Sections  │  - Navigation config     │
│  - Translations      │  - Layouts   │  - SEO configurations   │
└──────────────────────────┬────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Build Layer (Astro 5.0)                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │ Zero-JS     │  │ Island      │  │ Image & Asset       │     │
│  │ Architecture│  │ Architecture│  │ Optimization        │     │
│  │ - Static    │  │ - Interactive│ │ - WebP/AVIF        │     │
│  │   HTML      │  │   components│ │ - Lazy loading     │     │
│  │ - Minimal   │  │ - Hydration │ │ - Responsive img   │     │
│  │   JS        │  │   on demand │ │ - CDN delivery     │     │
│  └─────────────┘  └─────────────┘  └─────────────────────┘     │
└──────────────────────────┬────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Hosting Layer (Vercel)                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │ Edge        │  │ CDN         │  │ Preview             │     │
│  │ Network     │  │ Caching     │  │ Deployments         │     │
│  └─────────────┘  └─────────────┘  └─────────────────────┘     │
└──────────────────────────┬────────────────────────────────────────┘
```

## Key Technical Decisions

### Framework Choice: Astro 5.0

- **Reason**: Zero-JS by default, excellent performance, island architecture
- **Alternative considered**: Next.js - overkill for static content
- **Trade-off**: Limited dynamic features, but perfect for portfolio

### Styling: Tailwind CSS 4.0

- **Reason**: Utility-first, small bundle size, easy customization
- **Alternative considered**: Plain CSS - less maintainable at scale
- **Configuration**: Custom color palette, responsive breakpoints

### Hosting: Vercel

- **Reason**: Native Astro support, edge network, preview deployments
- **Alternative considered**: Netlify - similar features
- **Trade-off**: Platform lock-in, but excellent DX

### Forms: Formspree

- **Reason**: No backend required, spam protection, email notifications
- **Alternative considered**: Custom backend - unnecessary complexity
- **Trade-off**: Third-party dependency, but low maintenance

### Analytics: Plausible

- **Reason**: Privacy-focused, GDPR compliant, no cookie consent needed
- **Alternative considered**: Google Analytics - privacy concerns
- **Trade-off**: Limited features compared to GA, but aligned with values

## Component Architecture

### Component Hierarchy

```
Layout (src/layouts/)
├── Header (src/components/common/)
├── Footer (src/components/common/)
└── PageContent
    ├── Hero (src/components/sections/)
    ├── About (src/components/sections/)
    ├── Projects (src/components/sections/)
    ├── Services (src/components/sections/)
    ├── Testimonials (src/components/sections/)
    ├── Contact (src/components/sections/)
    └── UI Components (src/components/ui/)
```

### Content Structure

```
src/
├── content/
│   └── projects/
│       └── cloud-migration.md
├── i18n/
│   └── translations.ts
├── pages/
│   ├── index.astro (English)
│   ├── cs/
│   │   └── index.astro (Czech)
│   └── projects/
│       ├── index.astro
│       └── [slug].astro
└── styles/
    └── global.css
```

## Data Flow

### Static Generation

1. Content (MDX) → Astro build → Static HTML/CSS/JS
2. Images optimized → WebP/AVIF formats
3. Bundles minified → Deployed to Vercel

### User Request Flow

1. User requests page → Vercel Edge
2. CDN serves cached content (if available)
3. Static HTML delivered
4. Islands hydrate on interaction

## Security Architecture

### Transport Security

- HTTPS enforced through Vercel
- CSP headers configured
- Secure cookies for any future auth

### Data Protection

- No PII storage in static files
- Formspree handles form data
- Plausible analytics (no cookies, no PII)

### Content Security

- CSP headers configured
- No inline scripts
- Sanitized user inputs

## Performance Strategy

### Core Web Vitals Targets

- LCP: <2.0s
- FID: <100ms
- CLS: <0.1
- Bundle Size: <50KB gzipped

### Optimization Techniques

- Astro island architecture
- Image optimization (WebP/AVIF)
- Lazy loading below-fold content
- Font subsetting and optimization
- Critical CSS inlining
- CDN delivery through Vercel
- Prefetching for internal links
