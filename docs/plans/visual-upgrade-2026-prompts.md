# 🎨 Visual Upgrade 2026 - PROMPT SET (for Groq/Nano Banana)

**Generated:** 2026-02-13
**Purpose:** Generate 4 visual variants for AB testing
**Target:** SME B2B Marketing Website (1:1, not 100-person agency)

---

## 📋 CONTEXT

### Contact Info

| Field   | Value        |
| ------- | ------------ |
| Jméno   | Pavel Kašpar |
| Telefon | 773 445 227  |
| IČO     | 28098579     |
| Město   | Teplice      |
| Web     | tvoje.info   |

### Bonus Offer

**Headline:** "Automation vašeho digitálního života ZDARMA"
**Mechanic:** Zákazník zanechá email/phone → Pick 1 bonus:

- Automatický report (týdenní přehled konkurence)
- SEO audit (50 stránek zdarma)
- E-mail šablony (10 ready-to-use)
- Chatbot setup (základní nastavení)

---

## 🎯 4 BRANDED THEME VARIANTS

### Theme 1: TITAN ⚡

**Tone:** Direct, Professional, Results-focused
**Target:** E-commerce managers who know marketing, want efficiency
**Tagline:** "Práce. Výsledky. Bez řečí."

**Colors:**

- Primary: #4285F4 (Google Blue)
- Secondary: #34A853 (Success Green)
- Background: #FFFFFF / #F8F9FA

**Headlines:**
| CZ | EN |
|----|-----|
| "Marketing, co funguje." | "Marketing that works." |
| "Víc zákazníků. Měřitelné výsledky." | "More customers. Measurable results." |

**CTA:** "Chci růst"

---

### Theme 2: NOVA 💎

**Tone:** Friendly-Expert, Warm, Partnership
**Target:** SME owners who want relationship, not transaction
**Tagline:** "Váš růst je můj cíl."

**Colors:**

- Primary: #6366F1 (Indigo/Purple)
- Secondary: #22D3EE (Cyan)
- Background: Gradient mesh (Purple → Cyan)

**Headlines:**
| CZ | EN |
|----|-----|
| "Pojďme to posunout." | "Let's take it to the next level." |
| "Od 50+ projektů vím, co funguje." | "From 50+ projects, I know what works." |

**CTA:** "Nezávazná konzultace"

---

### Theme 3: SPARK ⚡🔥

**Tone:** Provocative, Bold, Urgent
**Target:** Business owners frustrated with current results
**Tagline:** "Změna. Teď. Hned."

**Colors:**

- Primary: #00D4FF (Cyan neon)
- Secondary: #FF0080 (Magenta neon)
- Background: #0A0A0A (Deep black)

**Headlines:**
| CZ | EN |
|----|-----|
| "Přestaňte pálit peníze za reklamu." | "Stop burning money on ads." |
| "Vaše konkurence to dělá líp. Změňme to." | "Your competitors do it better. Let's change that." |

**CTA:** "Chci změnu"

---

### Theme 4: LUX ✨

**Tone:** Minimal-Professional, Editorial, Premium
**Target:** High-end clients, conservative industries
**Tagline:** "Strategie. Implementace. Výsledky."

**Colors:**

- Primary: #000000 (Black)
- Secondary: #666666 (Gray)
- Accent: #B8860B (Gold)
- Background: #FFFFFF / #FAFAFA

**Headlines:**
| CZ | EN |
|----|-----|
| "Strategie. Implementace. Výsledky." | "Strategy. Implementation. Results." |
| "Marketing pro ty, kdo to myslí vážně." | "Marketing for those who mean business." |

**CTA:** "Kontaktovat"

---

## 🖼️ IMAGE GENERATION PROMPTS (for Nano Banana / Gemini)

### Logo Set (all themes)

```
Minimalist logo "PK" (Pavel Kašpar initials), geometric, professional,
[THEME_COLORS], white background, vector style, 8k quality
```

**Per theme:**

- **TITAN:** blue #4285F4 + green #34A853 gradient
- **NOVA:** purple #6366F1 + cyan #22D3EE gradient
- **SPARK:** cyan #00D4FF + magenta #FF0080 neon glow
- **LUX:** black #000000 + gold #B8860B accent

### Personal Photo

```
Professional portrait of friendly AI marketing expert man (Czech features),
looking at horizon with confident smile, [THEME_STYLE],
golden hour lighting, modern blurred office background,
smart casual business attire, 8k resolution, photorealistic
```

**Per theme:**

- **TITAN:** Clean corporate lighting, white background hint
- **NOVA:** Warm gradient lighting, purple/cyan tones
- **SPARK:** Dramatic neon lighting, dark with cyan rim light
- **LUX:** Premium editorial lighting, warm gold tones

### Hero Backgrounds

```
Abstract modern business background for marketing website hero section,
[THEME_ELEMENTS], professional, clean, 8k quality, suitable for dark and light mode
```

**Per theme:**

- **TITAN:** Geometric shapes, blue tones, clean professional
- **NOVA:** Gradient mesh, purple to cyan, soft glowing orbs
- **SPARK:** Neon geometric, cyberpunk elements, glowing lines
- **LUX:** Minimalist lines, gold accents, editorial fashion

### Service Icons (per theme)

```
Minimalist line icon for [SERVICE_NAME], [THEME_STYLE],
clean vector, 64x64px, professional business
```

**Services to generate icons for:**

- E-commerce marketing
- Online advertising (PPC)
- Social media management
- Content marketing
- Analytics & reporting

---

## 🔧 THEME SWITCHER - TECHNICAL SETUP

**Location:** Header (top-right, next to dark mode toggle)
**UI:** [T | N | S | L] buttons

### Current Issue - NEEDS FIX

The theme switcher is NOT working. Current implementation:

- HTML buttons exist with data-theme attributes
- JavaScript `setSiteTheme()` function exists
- CSS has theme-specific styles

### What's NOT working:

1. Click events not firing
2. `data-site-theme` attribute not updating on `<html>`
3. Visual theme changes not applying

### Files to check/fix:

1. `src/components/common/Header.astro` - Theme buttons
2. `src/layouts/Layout.astro` - JavaScript functions
3. `src/styles/global.css` - Theme CSS variables

### Required fixes:

1. Ensure JavaScript runs AFTER DOM is ready
2. Add console.log for debugging
3. Verify onclick handlers are attached
4. Check if localStorage is working

---

## 📝 COPYWRITING PROMPTS (for Groq Agent)

### Landing Page Copy - Per Theme

**Prompt Template:**

```
Rewrite the landing page copy for theme [TITAN/NOVA/SPARK/LUX]:

TONE: [direct/friendly/provocative/minimal]
TARGET: [audience description]
TAGLINE: "[theme tagline]"

REQUIREMENTS:
- Use customer language from job market research
- Focus on outcomes, not processes
- Avoid: "AI-powered", "innovative", "premium", technical jargon
- Use: "e-commerce", "online reklama", "víc zákazníků", concrete numbers

OUTPUT:
- Hero headline (CZ + EN)
- Hero subtitle (CZ + EN)
- 3 service card descriptions
- CTA button text
- Footer tagline
```

### Service Descriptions

**Prompt:**

```
Write service descriptions for marketing agency website:

SERVICE: [name]
CUSTOMER_BENEFIT: [what customer gets]
THEME_TONE: [TITAN/NOVA/SPARK/LUX]

Write in Czech (primary) with English translation notes.
Keep it short (2-3 sentences per section).
Focus on results, not features.
```

---

## 🎯 GROQ AGENT COMMANDS

### For Image Generation (Nano Banana)

```
Generate [type] for theme [TITAN/NOVA/SPARK/LUX]:
[detailed prompt from above]
Output format: SVG preferred, PNG fallback
```

### For Code Updates (Design Agent)

```
Update website for theme [THEME_NAME]:

1. Apply color palette from theme spec
2. Update hero section with theme-specific copy
3. Add theme-specific background effects
4. Update CTA buttons with theme colors
5. Apply hover states and animations
6. Test responsive design

Reference: docs/plans/visual-upgrade-2026-4-variants.md
```

### For Copy Updates (Copywriter Agent)

```
Rewrite copy for theme [THEME_NAME]:

- Use [TONE] tone
- Target: [AUDIENCE]
- Include tagline: "[TAGLINE]"
- Update all sections: Hero, Services, About, Contact

Reference: docs/guides/copywriting-prompting-guide.md
```

---

## 🔄 PARALLEL EXECUTION WORKFLOW

### Phase 1: Generate All Assets (Parallel)

```
Agent 1 (Nano Banana): Generate TITAN assets
Agent 2 (Nano Banana): Generate NOVA assets
Agent 3 (Nano Banana): Generate SPARK assets
Agent 4 (Nano Banana): Generate LUX assets
```

### Phase 2: Apply to Code (Sequential - per theme)

```
Design Agent: Apply TITAN theme to code
→ Screenshot → UX Designer review
→ Fix if needed

Design Agent: Apply NOVA theme to code
→ Screenshot → UX Designer review
→ Fix if needed

Design Agent: Apply SPARK theme to code
→ Screenshot → UX Designer review
→ Fix if needed

Design Agent: Apply LUX theme to code
→ Screenshot → UX Designer review
→ Fix if needed
```

### Phase 3: QA & Launch

- Verify all 4 themes work
- Test theme switcher
- Check responsive design
- Launch AB test

---

## 📚 REFERENCE FILES

| File                                           | Purpose              |
| ---------------------------------------------- | -------------------- |
| `docs/plans/visual-upgrade-2026-4-variants.md` | Theme specifications |
| `docs/prd-data/scrap/job-keywords-analysis.md` | Customer language    |
| `docs/prd-data/scrap/copy-draft-from-jobs.md`  | Copy drafts          |
| `.agents/agents/designer.md`                   | Design system        |
| `.agents/agents/copywriter.md`                 | Copy guidelines      |
| `docs/guides/copywriting-prompting-guide.md`   | Copy prompts         |
| `docs/guides/design-prompting-guide.md`        | Design prompts       |

---

## ✅ EXECUTION CHECKLIST

### Before Starting

- [ ] Review all 4 theme specifications
- [ ] Confirm logo initials: "PK" (Pavel Kašpar)
- [ ] Prepare image generation prompts
- [ ] Test dev server is running

### Asset Generation

- [ ] Generate 4 logo variants
- [ ] Generate 4 personal photo variants
- [ ] Generate 4 hero background variants
- [ ] Generate service icons (5 icons × 4 themes)

### Code Application

- [ ] Fix theme switcher (PRIORITY - not working!)
- [ ] Apply TITAN theme → screenshot → review
- [ ] Apply NOVA theme → screenshot → review
- [ ] Apply SPARK theme → screenshot → review
- [ ] Apply LUX theme → screenshot → review

### Final QA

- [ ] Test theme switcher works
- [ ] Test responsive design
- [ ] Test dark mode compatibility
- [ ] Verify all CTAs work

---

## 🚀 QUICK START

**Step 1:** Fix theme switcher (ask for help if needed)

```
Theme switcher in header is not working.
Check: src/components/common/Header.astro
Check: src/layouts/Layout.astro
```

**Step 2:** Generate assets

```
Use Nano Banana / Gemini to generate:
- 4× Logo (PK initials, theme colors)
- 4× Personal photo (theme-styled)
- 4× Hero background
- 20× Service icons (5 services × 4 themes)
```

**Step 3:** Apply themes

```
Run Design Agent for each theme:
"Apply [THEME] theme with colors from visual-upgrade-2026-4-variants.md"
```

**Step 4:** Screenshots & Review

```
After each theme, take screenshot:
→ Review with team
→ Fix if needed
→ Repeat for all 4 themes
```
