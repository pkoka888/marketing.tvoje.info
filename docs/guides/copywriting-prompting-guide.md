# 💡 Copywriting Prompting Guide

**Pro měnění textů na webu**
_Generated: 2026-02-13_

---

## 🎯 Základní pravidla

### Používej (z analýzy trhu):

- ✅ "E-commerce marketing" - nejvíc žádané
- ✅ "Online reklama" / "PPC"
- ✅ "Sociální sítě"
- ✅ "Obsah" / "Content"
- ✅ "Potřebuji více zákazníků"
- ✅ Konkrétní čísla: "+30%", "60k/měsíc"

### Vyhýbej se:

- ❌ Technickému žargonu: "MLOps", "AEO", "ROAS", "prémiový"
- ❌ "My jsme nejlepší" - zákazníky to nezajímá
- ❌ Akademickému jazyku
- ❌ Dlouhým odstavcům

### Jazyk:

- **Primárně Čeština** (CZ)
- **Sekundárně Angličtina** (EN)

---

## 📝 Jak psát prompty

### 1. Změna Hero sekce

**Prompt:**

```
Změň hero sekci na homepage:
- Nový headline: "Potřebujete více zákazníků?"
- Podtitulek: "My vám je přivedeme. Bez zbytečných výdajů za reklamu."
- Jazyk: Česky
- Styl: Přímý, zákaznický, bez žargonu
```

**Nebo jednodušeji:**

```
Rewrite hero section to be more customer-focused.
Use question format. Avoid technical jargon.
```

---

### 2. Změna služeb

**Prompt:**

```
Přepiš sekci služeb:
- Název: "Co pro vás můžeme udělat" (místo "Služby")
- Služby jako karty s výsledky, ne procesy
- Použij zákaznický jazyk z analýzy
```

**Konkrétní příklad pro E-commerce:**

```
Změň popis služby "E-commerce" na:
"Pomůžeme vám prodávat více z e-shopu.
- Optimalizace pro vyhledávače
- PPC kampaně co se vyplatí
- E-mail marketing, co nakupuje"

Místo:
"E-commerce řešení s využitím AI-powered analytics..."
```

---

### 3. Nová stránka / sekce

**Prompt:**

```
Vytvoř novou sekci "Jak to funguje":
- 3 kroky: 1) Analýza, 2) Strategie, 3) Růst
- Krátké popisky (max 2 věty na krok)
- CTA: "Chcete vědět víc?"
- Jazyk: CZ
```

---

### 4. Formulář / CTA

**Prompt:**

```
Změň CTA tlačítka:
- Místo "Odeslat" použij "Chci nezávaznou konzultaci"
- Místo "Kontaktovat" použij "Domluvit schůzku"
- Formulář: "Co vás zajímá?" jako dropdown
```

---

### 5. Blog / Obsah

**Prompt:**

```
Napiš blog post:
- Téma: "Jak zvýšit tržby e-shopu v roce 2026"
- Keywords: e-commerce marketing, online reklama, SEO
- Délka: 800-1000 slov
- Jazyk: Česky
- Styl: Praktický, konkrétní, bez marketingových frází
```

---

## 📋 Šablony pro prompty

### Základní struktura:

```
[Akce] [Co] [Jak] [Jazyk]

Příklad:
Změň popis služby "PPC" tak, aby zněl lidsky a konkrétně.
```

### Pokročilá struktura:

```
[Akce]: [Co měnit]
[Kontext]: [Proč / pro koho]
[Styl]: [Jak má znít]
[Omezení]: [Co nepoužívat]
[Jazyk]: [CZ/EN]
```

**Příklad:**

```
Změň: hero sekce
Kontext: pro malé e-shopy, co chtějí růst
Styl: přímý, zákaznický, výsledky
Omezení: žádný žargon, žádné "my jsme nejlepší"
Jazyk: CZ
```

---

## 🔤 Klíčová slova k použití

### Z analýzy (TOP 10):

1. Marketing
2. E-commerce
3. Online reklama
4. Sociální sítě
5. PPC / Google Ads
6. Obsah / Content
7. Zákazníci
8. Růst
9. Výsledky
10. Prodeje

### Pro SEO:

- "marketingové služby praha"
- "e-commerce marketing"
- "jak zvýšit prodeje e-shopu"
- "online reklama pro firmy"

---

## 📞 Příklady hotových promptů

### "Chci změnit headline na homepage"

```
Rewrite homepage hero headline to:
"Potřebujete více zákazníků?"
with subtitle:
"Váš e-shop může vydělávat více. Bez zbytečných výdajů za reklamu."
Keep it in Czech. Customer-focused, not self-promotional.
```

### "Chci přepsat sekci služeb"

```
Rewrite services section with these requirements:
- Use customer language from job market research
- Focus on outcomes, not processes
- Avoid: "AI-powered", "innovative", "premium"
- Use: "e-commerce", "online reklama", "víc zákazníků"
- Language: Czech primary
- Format: Cards with icon + title + benefit
```

### "Chci novou sekci s výsledky"

```
Create a "Results" / "Výsledky" section:
- Include 3-4 metrics with real numbers
- Format: large number + what it means
- Example: "+47% tržeb" not "significant growth"
- Language: Czech
- Style: Professional but human
```

---

## ✅ Checklist před odesláním

- [ ] Používám zákaznický jazyk?
- [ ] Jsou tam konkrétní čísla?
- [ ] Žádný technický žargon?
- [ ] Žádné "my jsme nejlepší"?
- [ ] Krátké odstavce (max 3 věty)?
- [ ] Jasné CTA?

---

## 📚 Reference

- `docs/prd-data/scrap/job-keywords-analysis.md` - Analýza klíčových slov
- `docs/prd-data/scrap/copy-draft-from-jobs.md` - Draft copy
- `src/i18n/translations.ts` - Existující překlady

---

## 🚀 Rychlý start

1. **Otevři** soubor co chceš změnit
2. **Napiš** prompt podle šablony výše
3. **Použij** agenta (Kilo Code / OpenCode)
4. **Zkontroluj** podle checklistu
5. **Implementuj** do kódu
