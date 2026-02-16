# 🎨 Design Prompting Guide

**Pro změny vzhledu webu**
_Generated: 2026-02-13_

---

## 🎯 Základní design systém

### Barevná paleta (Google-inspired)

```css
/* Hlavní barvy */
--primary: #4285f4; /* Modrá - důvěra, růst */
--primary-dark: #3367d6;
--primary-light: #8ab4f8;

/* Sekundární */
--secondary: #ea4335; /* Červená - akce, pozornost */
--secondary-dark: #d33426;

/* Akcent */
--accent: #fbbc05; /* Žlutá - energie */
--accent-dark: #f9a825;

/* Úspěch */
--success: #34a853; /* Zelená - růst, úspěch */

/* Neutrální */
--dark: #202124; /* Hlavní text */
--dark-medium: #5f6368; /* Sekundární text */
--light: #ffffff; /* Pozadí */
--light-gray: #f8f9fa; /* Sekundární pozadí */
--border: #dadce0; /* Okraje */
```

### Alternativní palety

**Modern SaaS (Stripe-inspired):**

```css
--primary: #6366f1; /* Indigo */
--secondary: #22d3ee; /* Cyan */
--accent: #f97316; /* Orange */
--success: #22c55e; /* Emerald */
```

**E-commerce Friendly:**

```css
--primary: #f97316; /* Oranžová - energie */
--secondary: #22c55e; /* Zelená - důvěra */
--accent: #3b82f6; /* Modrá - akce */
```

---

## 🖼️ Typy prvků

### 1. Hero sekce

- Gradient mesh pozadí
- Velký nadpis (48-64px)
- Podtitulek (18-24px)
- CTA tlačítko

### 2. Karty služeb

- Bílé pozadí
- 16px border-radius
- Hover: lift + shadow
- Ikony nahoře

### 3. Statistiky

- Velká čísla (64px+)
- Icon nebo grafika
- Krátký popis

### 4. CTA sekce

- Výrazná barva
- Krátký text
- Jedno tlačítko

---

## ✨ Efekty (2026 trendy)

### Gradient mesh

```css
background:
  radial-gradient(at 40% 20%, #4285f4 0px, transparent 50%),
  radial-gradient(at 80% 0%, #ea4335 0px, transparent 50%),
  radial-gradient(at 0% 50%, #34a853 0px, transparent 50%), #f8f9fa;
```

### Glassmorphism

```css
backdrop-filter: blur(10px);
background: rgba(255, 255, 255, 0.8);
border: 1px solid rgba(255, 255, 255, 0.3);
```

### Hover efekty

```css
/* Button */
transition:
  transform 0.2s,
  box-shadow 0.2s;
:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(66, 133, 244, 0.3);
}

/* Card */
:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}
```

### Scroll animace

```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## 📝 Jak psát prompty pro design

### 1. Změna barev

**Jednoduše:**

```text
Změň primární barvu na modrou (#4285F4).
```

**Podrobně:**

```text
Aktualizuj barevnou škálu:
- Primární: #4285F4 (modrá)
- Sekundární: #EA4335 (červená)
- Akcent: #FBBC05 (žlutá)
- Použij v celém webu
```

---

### 2. Nová Hero sekce

**Prompt:**

```text
Vytvoř novou hero sekci:
- Pozadí: gradient mesh (modrá + červená + žlutá)
- Nadpis: "Potřebujete více zákazníků?" (64px, bold)
- Podtitulek: "My vám je přivedeme." (24px)
- CTA tlačítko: "Chci více zákazníků" (primary barva)
- Výplň: glassmorphism karta
- Animace: fade-in při načtení
```

---

### 3. Service karty

**Prompt:**

```text
Vytvoř 4 karty služeb:
- Layout: grid 4 sloupce (mobile: 1, tablet: 2)
- Každá karta:
  - Ikona nahoře (line art, 48px)
  - Název (24px, bold)
  - Popis (16px, max 2 věty)
  - Hover: lift efekt + shadow
- Barvy: primární pro ikony
- Mezery: 24px mezi kartami
```

---

### 4. Infografika / Statistiky

**Prompt:**

```text
Vytvoř sekci s výsledky:
- 3 statistiky v řadě:
  1. "50+" dokončených projektů
  2. "+30%" průměrný růst
  3. "99%" spokojených klientů
- Velká čísla: 64px, bold, primární barva
- Pod text: 14px, šedý
- Pozadí: light-gray
- Ikony: geometric shapes
```

---

### 5. CTA sekce

**Prompt:**

```text
Vytvoř CTA sekci:
- Text: "Připraveni růst?"
- Podtext: "Domluvme si nezávaznou konzultaci."
- Tlačítko: "Domluvit schůzku" (accent barva)
- Pozadí: gradient mesh
- Layout: center, max-width 600px
```

---

### 6. Animace / Effekty

**Přidat scroll animace:**

```text
Přidej na stránku scroll-triggered animace:
- Fade-in pro sekce
- Stagger pro karty (100ms delay)
- Použij Intersection Observer
- Duration: 0.6s
- Easing: ease-out
```

---

## 📋 Šablony pro prompty

### Základní

```text
[Akce] [Prvek] [Styl]
Příklad:
Vytvoř novou hero sekci s gradient pozadím.
```

### Podrobná

```text
[Akce]: [Co vytvořit/změnit]
[Styl]: [Barvy, fonty, efekty]
[Layout]: [Grid, pozicování]
[Responsive]: [Mobile/tablet/desktop]
[Animace]: [Jaké efekty]
```

**Příklad:**

```text
Vytvoř: sekci s službami
Styl: glassmorphism karty, primary barva pro ikony
Layout: 3-sloupcový grid (mobile: 1)
Responsive: mobile-first
Animace: hover lift + fade-in při scroll
```

---

## 🔧 Praktické příklady

### "Chci tmavý režim"

```text
Přidej dark mode:
- Pozadí: #0F172A
- Text: #F8FAFC
- Karty: #1E293B s glassmorphism
- Toggle v navigaci
- Ulož do localStorage
```

### "Chci nové ikony"

```text
Změň ikony na:
- Line art styl (ne filled)
- Primární barva
- 24px velikost
- Použij Heroicons nebo Phosphor icons
```

### "Chci animované pozadí"

```text
Přidej animated gradient pozadí:
- Barvy: primary + secondary + accent
- Pomalu se měnící (20s cyklus)
- Subtle motion (ne rušivé)
- Použij CSS animations
```

---

## ✅ Checklist před odesláním

- [ ] Použita správná barevná paleta?
- [ ] Kontrast dostatečný (4.5:1)?
- [ ] Responzivní design?
- [ ] Hover stavy fungují?
- [ ] Animace plynulé (60fps)?
- [ ] Žádné layout shifts?

---

## 📚 Reference

- `.agents/agents/designer.md` - Designer agent specifikace
- `docs/prd-data/scrap/companies/website-analysis.md` - Analýza konkurentů
- `tailwind.config.mjs` - Aktuální Tailwind config

---

## 🚀 Rychlý start

1. **Vyber** prvek co chceš změnit
2. **Napiš** prompt podle šablony
3. **Spusť** agenta (Kilo Code / OpenCode)
4. **Zkontroluj** v prohlížeči
5. **Iteruj** dokud to není perfect
