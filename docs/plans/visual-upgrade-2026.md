# Visual & Content Upgrade Plan 2026 ("10x Performance")

**Goal:** Transform the MVP into a "10x" visually stunning, immersive, and high-converting marketing platform.
**Target Audience:** SME Business Owners & E-commerce Managers.
**Key Trends:** Glassmorphism, Gradient Meshes, Authentic Personal Branding, Buyer Enablement.

---

## 🎨 1. Design System & The "Design Switcher"

We will implement a dynamic **Design Switcher** (Top Right) with 8 distinct themes (4 Light, 4 Dark).

### Architecture

- **Tech:** React Context (`ThemeContext`) + Tailwind CSS Variables (`CSS Custom Properties`).
- **Location:** Floating or Fixed Header component next to Dark Mode toggle.

### Theme Variants

#### Light Modes

1.  **Google Modern (Default)**: Clean, white/gray backgrounds, primary Google Blue (#4285F4), high whitespace.
2.  **Glass Morphism**: Frosted glass cards, vivid gradient mesh background (Blue/Purple), soft shadows.
3.  **Neo-Playful**: Soft pastel colors (Peach/Mint), rounded 32px corners, bouncy animations.
4.  **Expert Minimal**: Stark black/white contrast, serif typography (Editorial style), minimal color.

#### Dark Modes

1.  **Cyber Depth**: Deep blue/black backgrounds, neon accents (Cyan/Magenta), glowing borders.
2.  **Obsidian Glass**: Pure black glass, subtle white borders, gold/yellow accents (#FBBC05).
3.  **Professional Dim**: Slate grays (#1e293b), muted blue accents, low contrast for eye comfort.
4.  **Midnight Mesh**: Deep purple/black gradient mesh, floating 3D elements.

---

## 🆔 2. Branding & Identity

**Brand Name:** tvoje.info (Personal) / expc.cz (Platform)
**Concept:** "Marketingový Expert" (Marketing Expert)

### Logo Concepts ("EX")

- **Symbol:** "EX" intertwined or stylized.
  - _Express_: Speed, automation.
  - _Expert_: Knowledge, authority.
  - _Exclusive_: Premium service.
- **Personal Brand (tvoje.info):** "M" (Marketing) dominant, with "EX" as a exponent or subscript.
- **Platform Brand (expc.cz):** "EX" dominant, bold, structural.

### Logo Prompts (to be generated)

> "Minimalist modern logo for marketing agency, letters 'EX' combined, geometric, vector style, blue and orange gradient, white background"
> "Personal brand logo letter 'M' with subtle 'EX' integration, professional, serif font, luxurious feel"

### Personal Photo

**Concept:** "The Visionary Expert"

- **Pose:** Looking at the horizon (optimism/future), 3/4 profile, slight confident smile (kind but professional).
- **Style:** Cinematic lighting, shallow depth of field, modern office or abstract tech background.
- **Prompt:**
  > "Professional portfolio portrait of a friendly AI marketing expert man, looking at horizon, golden hour lighting, modern blurred office background, confident smile, smart casual, 8k resolution, photorealistic."

---

## ✍️ 3. Copywriting & "Hooks"

**Headline Strategy:** "Hook > Value > Proof"

### New Headlines (Variants)

- **Variant A (Direct):** "Marketingový expert k Vašim službám."
- **Variant B (Benefit):** "Pozvedněte tvoje.info na světovou úroveň."
- **Variant C (Provocative - 2026 Trend):** "Přestaňte pálit peníze za reklamu. Nechte AI vydělávat."

### Call to Action (CTA)

- _Old:_ "Connect Shop"
- _New:_ "Spustit Růstový Motor" (Start Growth Engine) / "Analyzovat Můj Byznys Hned"

---

## 🛠️ 4. "Real Tools" (Buyer Enablement)

To show the "full vision" and prevent the "just a landing page" feel, we will add interactive **Mock Tools**:

1.  **Ads Manager (Simulator)**:
    - Shows "Live" ad spend vs. ROAS.
    - "AI Optimizing..." status indicators.
2.  **Smart Merchant Center**:
    - Product feed health score (e.g., "98% Healthy").
    - "Fix 3 Errors" button.
3.  **Analytics Dashboard**:
    - Traffic sources breakdown (3D Pie Chart).
    - Conversion rate trend (Line Chart).

---

## 📅 Implementation Steps

1.  **Assets**: Generate Logos & Personal Photo (Gemini/Nano Banana).
2.  **Code**: Refactor `tailwind.config.mjs` for CSS variables.
3.  **Code**: Build `ThemeSwitcher` component.
4.  **Code**: Update `DashboardLayout` to use new variables.
5.  **Code**: Implement "Real Tools" components (skeletons/mocks).
6.  **Content**: Update Landing Page copy.
