# Gemini Image Generation Plan

**Datum:** 13. února 2026
**Účel:** Generování marketingových vizuálů pro web
**Nástroj:** Gemini CLI / Google AI Studio

---

## 🎯 Cíl

Vytvořit sadu profesionálních marketingových obrázků pro nový web v moderním 2026 stylu.

---

## 📋 Typy obrázků

### 1. Hero Illustrations

- **Popis:** Abstraktní ilustrace pro hero sekci
- **Styl:** 3D, gradienty, moderní
- **Použití:** Homepage hero section

### 2. Team/Týmové obrázky

- **Popis:** Abstraktní reprezentace týmu
- **Styl:** Ilustrace, ne fotografie
- **Použití:** About stránka

### 3. Infografiky

- **Typy:**
  - Growth charts (růstové grafy)
  - Funnel graphics (funnel diagramy)
  - Process steps (procesní kroky)
  - Statistics (čísla, procenta)
- **Použití:** Services, landing pages

### 4. Grafy a Charts

- **Typy:**
  - Bar charts
  - Line charts
  - Pie charts
  - Funnel diagrams
- **Použití:** Case studies, statistiky

### 5. Background Patterns

- **Typy:**
  - Gradient meshes
  - Geometric patterns
  - Abstract shapes
- **Použití:** Sekce pozadí

### 6. Service Icons

- **Styl:** Minimalistické, line art
- **Použití:** Service karty

### 7. CTA Illustrations

- **Popis:** Abstraktní vizuály pro výzvy k akci
- **Použití:** Button areas, CTAs

---

## 🎨 Design Specifikace

### Color Palette

```
Primary:    #4285F4 (Google Blue)
Secondary:  #EA4335 (Google Red)
Accent:     #FBBC05 (Google Yellow)
Success:    #34A853 (Google Green)
Background: #F8F9FA (Light)
Dark:       #202124
```

### Styl

- 2026 moderní: odvážné barvy, čisté linky, lehký 3D efekt
- Konzistentní s vybranou barevnou paletou
- Profesionální ale přístupný
- Bilingual labels (CZ/EN)

---

## 📁 Výstupní struktura

```
assets/
└── images/
    └── generated/
        ├── hero-illustrations/
        │   ├── hero-growth.svg
        │   ├── hero-team.svg
        │   └── hero-analytics.svg
        ├── team/
        │   ├── team-abstract-1.svg
        │   └── team-abstract-2.svg
        ├── infographics/
        │   ├── growth-chart.svg
        │   ├── funnel.svg
        │   └── process-3steps.svg
        ├── graphs/
        │   ├── bar-chart.svg
        │   ├── line-chart.svg
        │   └── pie-chart.svg
        ├── backgrounds/
        │   ├── gradient-mesh-1.svg
        │   ├── gradient-mesh-2.svg
        │   └── geometric-pattern.svg
        └── icons/
            ├── ecommerce.svg
            ├── ppc.svg
            ├── social.svg
            └── content.svg
```

---

## 🔧 Nástroje

### Gemini CLI

```bash
# Ověření API klíče
gemini --status

# Generování obrázku
gemini --image "prompt" -o output.svg
```

### Google AI Studio

- Alternativa přes webové rozhraní
- Více kontrol nad výstupem

---

## 📝 Prompts pro generování

### Hero Illustration

```
Create a modern 3D-style illustration showing business growth and digital marketing.
Use Google-inspired color palette: blue (#4285F4), red (#EA4335), yellow (#FBBC05), green (#34A853).
Clean lines, gradient background, professional business style.
Aspect ratio 16:9. Vector format preferred.
```

### Team Illustration

```
Abstract team illustration in modern corporate style.
Minimalist human figures in geometric shapes.
Colors: blue and green tones.
Clean, professional, not too literal.
```

### Growth Chart Infographic

```
Infographic showing business growth metrics.
Bar chart style with upward trend.
Colors: green (#34A853) for positive growth.
Clean, modern, business-appropriate.
```

### Funnel Graphic

```
Marketing funnel diagram with 4 stages: Awareness, Interest, Decision, Action.
Modern flat design with gradient fills.
Blue to green color progression.
Clean labels, professional style.
```

### Background Pattern

```
Abstract gradient mesh background.
Colors: blue (#4285F4) and purple (#6366F1) blend.
Subtle, not overwhelming. Tileable.
```

---

## 🚀 Generování (příkazy)

### 1. Hero Illustrations

```bash
gemini --image "Modern 3D business growth illustration, blue red yellow colors, abstract, vector style, 16:9" -o assets/images/generated/hero-growth.svg
```

### 2. Team

```bash
gemini --image "Abstract team illustration, minimalist geometric shapes, blue tones, corporate style" -o assets/images/generated/team/team-1.svg
```

### 3. Infographics

```bash
gemini --image "Business growth bar chart infographic, green positive trend, modern flat design" -o assets/images/generated/infographics/growth-chart.svg
```

### 4. Backgrounds

```bash
gemini --image "Abstract gradient mesh background, blue purple, subtle, tileable" -o assets/images/generated/backgrounds/mesh-1.svg
```

---

## ✅ Checklist před generováním

- [ ] Ověřit Gemini API klíč
- [ ] Připravit výstupní adresář
- [ ] Nastavit správné aspect ratio
- [ ] Zvolit formát (SVG pro vektory, PNG pro rastry)
- [ ] Naplánovat pořadí generování

---

## 📦 Dodatečné zdroje

### Alternativní nástroje

- **Midjourney** - pro fotorealistické
- **DALL-E 3** - pro ilustrace
- **Leonardo.ai** - pro styly

### Stock photo zdroje

- Unsplash (free)
- Pexels (free)
- Flaticon (icons)

---

## 📝 Další kroky

1. **Spustit Gemini CLI** s API klíčem
2. **Generovat testovací obrázky** - 2-3 varianty
3. **Vybrat nejlepší** - konzistence stylu
4. **Převést do formátu** - SVG preferováno
5. **Optimalizovat** - pro web (webp, komprese)
6. **Implementovat** - do Astro komponent

---

## 💡 Tipy

- **Start simple** - první pokusy jednodušší
- **Iterate** - postupné vylepšování
- **Consistency** - držet se jednoho stylu
- **Test sizes** - různé varianty pro různé use case
- **Fallback** - mít záložní stock fotky
