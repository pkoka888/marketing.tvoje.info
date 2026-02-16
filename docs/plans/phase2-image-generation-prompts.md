# 🎨 Image Generation Prompts - Phase 2

**Purpose:** Generate visual assets for 4 themes
**Tool:** Nano Banana / Gemini
**Output:** SVG preferred, PNG fallback

---

## 📦 Asset Checklist

| Asset          | TITAN | NOVA | TARGET | SPARK | LUX |
| -------------- | ----- | ---- | ------ | ----- | --- |
| Logo           | ✅    | ✅   | ✅     | ✅    | ✅  |
| Hero BG        | ✅    | ✅   | ✅     | ✅    | ✅  |
| Personal Photo | ✅    | ✅   | ✅     | ✅    | ✅  |
| Bow/Arrow      | ❌    | ❌   | ✅     | ❌    | ❌  |

---

## 1. LOGO GENERATION

### Common Prompt Template

```
Minimalist logo "PK" (Pavel Kašpar initials), geometric, professional,
[THEME_COLORS], white background, vector, 8k quality
```

### TITAN Logo 🎯

```
Minimalist logo "PK" combined letters, geometric professional style,
blue #4285F4 and green #34A853 gradient, white background,
vector SVG, 8k quality, clean sharp edges
```

### NOVA Logo 💎

```
Minimalist logo "PK" combined letters, gradient effect,
purple #6366F1 to cyan #22D3EE gradient, white background,
vector SVG, 8k quality, soft gradient mesh effect
```

### TARGET Logo 🎯

```
Minimalist logo "PK" with arrow integration, geometric professional style,
deep blue #1E40AF and orange #EA580C accent, white background,
vector SVG, 8k quality, arrow pointing right integrated
```

### SPARK Logo ⚡

```
Minimalist logo "PK" with neon glow effect,
cyan #00D4FF and magenta #FF0080 neon outline, dark transparent background,
vector SVG, 8k quality, glowing cyberpunk style
```

### LUX Logo ✨

```
Minimalist logo "PK" combined letters, elegant thin line style,
black #000000 with gold #B8860B accent, white background,
vector SVG, 8k quality, premium minimal serif-inspired
```

---

## 2. HERO BACKGROUND GENERATION

### TITAN Hero Background 🎯

```
Abstract modern business background for marketing website hero section,
clean geometric shapes in blue tones #4285F4, #34A853, white,
professional corporate style, subtle depth, 8k quality,
suitable for light background, minimal complexity
```

### NOVA Hero Background 💎

```
Abstract modern business background for marketing website hero section,
gradient mesh purple #6366F1 to cyan #22D3EE, soft glowing orbs,
floating gradient circles, glassmorphism inspiration, 8k quality,
suitable for gradient backgrounds, ethereal effect
```

### TARGET Hero Background 🎯

```
Abstract modern business background for marketing website hero section,
white background with orange #EA580C arrow path visualization,
dashed line showing journey from left to right, target/bullseye on right side,
clean professional style, 8k quality, minimal and precise
```

### SPARK Hero Background ⚡

```
Abstract modern business background for marketing website hero section,
deep black #0A0A0A with cyan #00D4FF and magenta #FF0080 neon geometric lines,
cyberpunk lightning bolt shapes, particle dots, glowing wireframe,
8k quality, high contrast, energetic futuristic style
```

### LUX Hero Background ✨

```
Abstract modern business background for marketing website hero section,
off-white #FAFAFA with subtle gold #B8860B horizontal accent lines,
minimalist professional style, editorial fashion aesthetic,
8k quality, clean sophisticated, premium minimal
```

---

## 3. PERSONAL PHOTO GENERATION

### TITAN Photo 🎯

```
Professional portrait of friendly Czech marketing expert man (Pavel Kašpar),
looking at camera with confident direct smile, clean corporate lighting,
white/blue hint background, modern business attire, smart casual,
8k resolution, photorealistic, professional corporate style
```

### NOVA Photo 💎

```
Professional portrait of friendly Czech marketing expert man (Pavel Kašpar),
looking at camera with warm approachable smile, gradient lighting purple to cyan,
soft blurred gradient background, modern business attire, friendly vibe,
8k resolution, photorealistic, warm and welcoming
```

### TARGET Photo 🎯

```
Professional portrait of determined Czech marketing expert man (Pavel Kašpar),
looking to side with goal-focused expression, dramatic blue rim lighting,
dark navy background, professional business attire, determined confident,
8k resolution, photorealistic, action-oriented
```

### SPARK Photo ⚡

```
Professional portrait of bold Czech marketing expert man (Pavel Kašpar),
looking at camera with provocative confident expression,
neon cyan rim lighting on dark background, edgy modern business attire,
8k resolution, photorealistic, bold disruptive energy
```

### LUX Photo ✨

```
Professional portrait of sophisticated Czech marketing expert man (Pavel Kašpar),
looking at camera with subtle professional smile, warm golden hour lighting,
neutral studio background with gold accent, premium business attire,
editorial fashion photography style, 8k resolution, photorealistic, timeless
```

---

## 4. SPECIAL: BOW & ARROW ILLUSTRATION (TARGET Theme Only)

### Bow and Arrow SVG

```
Minimalist bow and arrow illustration, side view facing right,
bow at left side with arrow drawn and aiming at target,
orange #EA580C and deep blue #1E40AF colors, clean vector style,
white background, 8k quality, professional icon style,
target bullseye on right side with three rings
```

### Arrow Path Animation (CSS/SVG)

```
Animated arrow path showing journey from left to right,
dashed line animation, arrow moving along path,
orange gradient #EA580C to #F97316,
white background, clean professional style
```

---

## 5. SERVICE ICONS (5 services × 4 themes = 20 icons)

### Services:

1. E-commerce marketing
2. Online advertising (PPC)
3. Social media management
4. Content marketing
5. Analytics & reporting

### Prompt Template

```
Minimalist line icon for [SERVICE_NAME], [THEME_STYLE],
clean vector, 64x64px, professional business, white background
```

### Per Theme:

**TITAN:**

- Style: Solid filled, clean
- Color: #4285F4 primary

**NOVA:**

- Style: Line with soft glow
- Colors: Gradient purple to cyan

**TARGET:**

- Style: Arrow-integrated
- Accent: Orange #EA580C

**SPARK:**

- Style: Neon outline
- Colors: Cyan glow #00D4FF

**LUX:**

- Style: Minimal line
- Color: Black with gold accent

---

## 🚀 EXECUTION COMMANDS

### Generate All Assets (Parallel)

Use Nano Banana / Gemini with these prompts:

```
Agent 1: Generate TITAN assets
- Logo: [TITAN prompt above]
- Hero BG: [TITAN hero prompt]
- Photo: [TITAN photo prompt]

Agent 2: Generate NOVA assets
- Logo: [NOVA prompt above]
- Hero BG: [NOVA hero prompt]
- Photo: [NOVA photo prompt]

Agent 3: Generate TARGET assets
- Logo: [TARGET prompt above]
- Hero BG: [TARGET hero prompt]
- Photo: [TARGET photo prompt]
- Bow/Arrow: [SPECIAL prompt above]

Agent 4: Generate SPARK assets
- Logo: [SPARK prompt above]
- Hero BG: [SPARK hero prompt]
- Photo: [SPARK photo prompt]
```

### Output Directory

```
public/images/theme/
├── logo_pk_titan.svg
├── logo_nova.svg
├── logo_target.svg
├── logo_spark.svg
├── logo_lux.svg
├── hero_titan.svg
├── hero_nova.svg
├── hero_target.svg
├── hero_spark.svg
├── hero_lux.svg
├── bow_arrow.svg
└── service-icons/
    ├── titan/
    │   ├── ecommerce.svg
    │   ├── ppc.svg
    │   ├── social.svg
    │   ├── content.svg
    │   └── analytics.svg
    ├── nova/
    ├── target/
    └── spark/
```

---

## ✅ Delivery Checklist

- [ ] 5 Logo SVGs
- [ ] 5 Hero Background SVGs
- [ ] 5 Personal Photo descriptions (for photoshoot/generation)
- [ ] 1 Bow & Arrow illustration
- [ ] 20 Service Icons (5 services × 4 themes)
