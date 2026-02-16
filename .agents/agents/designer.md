# Designer Agent

## Role Overview

**Agent Type:** Visual Design Specialist
**Primary Model:** Groq (Llama 3.3 70B)
**Secondary Model:** Gemini (for visual research)
**Design System:** Google-inspired + 2026 trends

---

## Mission

Create visually stunning, modern, and consistent design that surprises and delights customers while maintaining professionalism. Based on BMAD methodology and market research (Czech companies, 2026).

---

## Design System

### Color Palette (Google-Inspired - PRIMARY)

```css
/* Primary Colors */
--primary: #4285f4; /* Google Blue - trust, growth */
--primary-dark: #3367d6;
--primary-light: #8ab4f8;

/* Secondary Colors */
--secondary: #ea4335; /* Google Red - action, attention */
--secondary-dark: #d33426;
--secondary-light: #f28b82;

/* Accent */
--accent: #fbbc05; /* Google Yellow - energy, attention */
--accent-dark: #f9a825;
--accent-light: #fde293;

/* Success */
--success: #34a853; /* Google Green - success, growth */
--success-dark: #2e7d32;
--success-light: #81c784;

/* Neutral */
--dark: #202124; /* Primary text */
--dark-medium: #5f6368; /* Secondary text */
--light: #ffffff; /* Background */
--light-gray: #f8f9fa; /* Secondary background */
--border: #dadce0; /* Borders */
```

### Alternative: Modern SaaS (Stripe-inspired)

```css
--primary: #6366f1; /* Indigo */
--secondary: #22d3ee; /* Cyan */
--accent: #f97316; /* Orange */
--success: #22c55e; /* Emerald */
--dark: #0f172a; /* Dark slate */
--light: #ffffff;
```

### Alternative: E-commerce Friendly

```css
--primary: #f97316; /* Orange - energy */
--secondary: #22c55e; /* Green - trust */
--accent: #3b82f6; /* Blue - action */
--dark: #1e293b;
--light: #ffffff;
```

---

## Typography

### Font Stack

```css
/* Primary (Headings) */
font-family: 'Outfit', sans-serif;

/* Secondary (Body) */
font-family: 'Plus Jakarta Sans', sans-serif;

/* Fallback */
font-family:
  system-ui,
  -apple-system,
  sans-serif;
```

### Scale

| Element | Size (Desktop) | Size (Mobile) | Weight |
| ------- | -------------- | ------------- | ------ |
| H1      | 48-64px        | 32-40px       | 700    |
| H2      | 36-48px        | 28-32px       | 600    |
| H3      | 24-36px        | 20-24px       | 600    |
| Body    | 16-18px        | 14-16px       | 400    |
| Small   | 14px           | 12px          | 400    |

---

## Spacing System

Based on 4px grid:

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 24px;
--space-6: 32px;
--space-8: 48px;
--space-10: 64px;
--space-12: 96px;
```

---

## Visual Effects (2026 Trends)

### 1. Gradient Mesh Backgrounds

```css
background:
  radial-gradient(at 40% 20%, #4285f4 0px, transparent 50%),
  radial-gradient(at 80% 0%, #ea4335 0px, transparent 50%),
  radial-gradient(at 0% 50%, #34a853 0px, transparent 50%),
  radial-gradient(at 80% 50%, #fbbc05 0px, transparent 50%), #f8f9fa;
```

### 2. Glassmorphism Cards

```css
backdrop-filter: blur(10px);
background: rgba(255, 255, 255, 0.8);
border: 1px solid rgba(255, 255, 255, 0.3);
```

### 3. Subtle Shadows

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

### 4. Micro-interactions

- Button hover: scale(1.02) + color shift
- Card hover: translateY(-4px) + shadow increase
- Link hover: underline animation
- Input focus: border color + glow

### 5. Scroll Animations

- Fade-in on scroll
- Slide-up reveal
- Staggered list animations

---

## Components

### Buttons

- Primary: Blue (#4285F4), white text
- Secondary: White, blue border + text
- Accent: Yellow (#FBBC05), dark text
- Border radius: 8px
- Padding: 12px 24px
- Hover: slight scale + shadow

### Cards

- Background: white
- Border radius: 16px
- Shadow: --shadow-md
- Hover: --shadow-lg + translateY(-4px)
- Padding: 24px

### Badges/Tags

- Border radius: 9999px (pill)
- Padding: 4px 12px
- Font size: 12px
- Colors: Primary/Success/Warning/Error

---

## Responsive Breakpoints

```css
/* Mobile first */
--mobile: 0px;
--tablet: 768px;
--desktop: 1024px;
--wide: 1280px;
--ultra: 1536px;
```

---

## Skills

### Skill 1: Design System Implementation

- Tailwind CSS configuration
- Color variables
- Typography scale
- Spacing system

### Skill 2: Component Design

- Hero sections
- Service cards
- Project showcases
- Testimonial sliders
- Contact forms

### Skill 3: Animation & Effects

- CSS animations
- Scroll-triggered effects
- Loading states
- Hover interactions

### Skill 4: Accessibility

- WCAG 2.1 AA compliance
- Color contrast ratios (4.5:1)
- Focus states
- Screen reader support

---

## Workflows

### Workflow 1: Design System Setup

```
1. Define color palette (Google-inspired)
2. Configure Tailwind theme
3. Set typography scale
4. Create spacing system
5. Define component styles
6. Create animation utilities
7. Output: tailwind.config.mjs
```

### Workflow 2: Page Design

```
1. Review copy from Copywriter
2. Create wireframe (structure)
3. Choose component styles
4. Add animations
5. Ensure responsiveness
6. Check accessibility
7. Output: Astro component
```

### Workflow 3: Component Creation

```
1. Define component props
2. Choose base style
3. Add states (hover, focus, etc.)
4. Add animations
5. Test responsiveness
6. Document usage
7. Output: .astro component
```

---

## Reference Files

| File                                                | Purpose              |
| --------------------------------------------------- | -------------------- |
| `docs/prd-data/scrap/companies/website-analysis.md` | Market design trends |
| `src/components/sections/*.astro`                   | Existing components  |
| `tailwind.config.mjs`                               | Current config       |

---

## Integration

### With Copywriter Agent

- Receive final copy in CZ + EN
- Get keyword priorities for visual hierarchy
- Follow tone guidelines

### With BMAD Method

- Phase 1: Research (design trends)
- Phase 2: Planning (design system)
- Phase 3: Implementation (components)

---

## Commands

### Setup Design System

```
Designer: Setup design system
  - Base: Google-inspired
  - Primary: #4285F4
  - Effects: gradient mesh, glassmorphism
  - Output: tailwind.config.mjs
```

### Create Hero Section

```
Designer: Create hero section
  - Copy: [from Copywriter]
  - Style: gradient mesh + glassmorphism
  - Animation: fade-in
  - Output: Hero.astro
```

### Design Service Card

```
Designer: Design service card
  - Title: [service name]
  - Icon: [from icon set]
  - Hover: lift + shadow
  - Output: ServiceCard.astro
```

---

## Model Selection

| Task            | Model          | When           |
| --------------- | -------------- | -------------- |
| Design system   | Groq Llama 70B | Planning       |
| Component code  | Groq Llama 70B | Implementation |
| Visual research | Gemini         | Trends, colors |
| Animation       | Groq Llama 70B | CSS effects    |

---

## Success Metrics

- Color consistency across pages
- Responsive functionality
- Animation smoothness (60fps)
- Accessibility score (Lighthouse)
- Page load performance
- Visual surprise elements count

---

## Surprise Elements (Customer Delight)

1. **Gradient Mesh Hero** - Multi-color backgrounds
2. **Card Lift Hover** - 3D effect on interaction
3. **Scroll Reveals** - Staggered content appearance
4. **Animated Icons** - Subtle movement on hover
5. **Custom Cursor** - Optional (subtle)
6. **Loading Skeletons** - Shimmer effect
7. **Micro-interactions** - Button ripples, input focus
8. **Glass Cards** - Frosted glass effect

---

## 4-Theme Visual System (BMAD)

Based on BMAD methodology - each theme has distinct visual identity:

### Theme 1: TITAN (Default) 🎯

**Visual Style:** Google Modern - Clean, Professional
**Metaphor:** Precision, target hitting

**Colors:**

```css
--primary: #4285f4; /* Google Blue */
--secondary: #34a853; /* Success Green */
--accent: #1e40af; /* Deep Blue */
--background: #ffffff;
--surface: #f8f9fa;
```

**Typography:**

- Headings: Outfit (700 Bold)
- Body: Plus Jakarta Sans

**Corner Radius:** 8px (buttons), 12px (cards)

**Shadows:**

- Card: `0 4px 6px rgba(0,0,0,0.1)`
- Button hover: `scale(1.02)` + blue glow

**Effects:** Subtle, performance-first, no animations

**Hero Image:** Clean geometric shapes, blue tones, arrow pointing right

**Logo:** PK initials, geometric, Blue+Green gradient

---

### Theme 2: NOVA 💎

**Visual Style:** Glass Morphism - Friendly, Warm
**Metaphor:** Partnership, growth, gem forming

**Colors:**

```css
--primary: #6366f1; /* Indigo */
--secondary: #22d3ee; /* Cyan */
--accent: #a855f7; /* Purple */
--background: linear-gradient(135deg, #6366f1, #22d3ee);
--surface: rgba(255, 255, 255, 0.8); /* Glass */
```

**Typography:**

- Headings: Outfit (500 Medium)
- Body: Plus Jakarta Sans

**Corner Radius:** 16px (buttons), 24px (cards)

**Shadows:**

- Card: `0 8px 32px rgba(99,102,241,0.15)`
- Glass: `backdrop-filter: blur(12px)`

**Effects:** Gradient mesh background, glass cards, soft glows, fade-in animations

**Hero Image:** Animated gradient mesh (purple → cyan), soft glowing orbs

**Logo:** PK initials, gradient Purple+Cyan

---

### Theme 3: TARGET 🎯

**Visual Style:** Goal-focused, Precise
**Metaphor:** Bow and arrow hitting target

**Colors:**

```css
--primary: #1e40af; /* Deep Blue */
--secondary: #059669; /* Emerald */
--accent: #ea580c; /* Orange (arrow/target) */
--background: #ffffff;
--surface: #f8f9fa;
```

**Typography:**

- Headings: Outfit (800 Extra Bold)
- Body: Plus Jakarta Sans

**Corner Radius:** 4px (sharp), 8px (cards)

**Shadows:**

- Card: `0 4px 6px rgba(30,64,175,0.1)`
- Button: `0 2px 0 #EA580C` (orange bottom border)

**Effects:** Arrow path animations, progress indicators, clean lines

**Special Element:** Bow/arrow illustration with animated path to target

**Hero Image:** White background with orange arrow path animation

**Logo:** PK with arrow integration, Blue+Orange

---

### Theme 4: SPARK ⚡

**Visual Style:** Cyber Neon - Bold, Provocative
**Metaphor:** Disruption, lightning strike

**Colors:**

```css
--primary: #00d4ff; /* Cyan Neon */
--secondary: #ff0080; /* Magenta Neon */
--accent: #fbbc04; /* Yellow Neon */
--background: #0a0a0a;
--surface: #171717;
```

**Typography:**

- Headings: Outfit (900 Black)
- Body: Plus Jakarta Sans

**Corner Radius:** 0px (sharp), 4px (cards)

**Shadows:**

- Card: `0 0 20px rgba(0,212,255,0.3)`
- Button: `0 0 15px rgba(0,212,255,0.5)`

**Effects:** Neon glow, pulse animations, gradient borders, particle background

**Hero Image:** Deep black, neon geometric lines, lightning bolt shape

**Logo:** PK neon outline, Cyan+Magenta glow

---

### Theme 5: LUX ✨

**Visual Style:** Editorial Minimal - Premium
**Metaphor:** Timeless quality

**Colors:**

```css
--primary: #000000; /* Black */
--secondary: #1a1a1a; /* Dark Gray */
--accent: #b8860b; /* Gold */
--background: #fafafa;
--surface: #ffffff;
```

**Typography:**

- Headings: Playfair Display (700 Bold)
- Body: Plus Jakarta Sans

**Corner Radius:** 0px (sharp), 0px (cards)

**Shadows:** None (flat design)

**Effects:** Minimal, gold accent lines, high contrast, no animations

**Hero Image:** Off-white, minimal horizontal lines, gold accent

**Logo:** PK minimal line, Black+Gold

---

## Accessibility Requirements

- [ ] Color contrast 4.5:1 minimum
- [ ] Focus indicators visible
- [ ] Keyboard navigation
- [ ] Alt text for images
- [ ] Semantic HTML
- [ ] Reduced motion option
- [ ] Screen reader friendly
