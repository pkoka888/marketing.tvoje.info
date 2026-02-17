# Project Content Migration Prompt

## Task

Rewrite DevOps project files as Marketing projects.

## Files to Update

1. `src/content/projects/cloud-migration.md` - Rewrite as marketing project
2. `src/content/projects/cicd-automation.md` - Rewrite as marketing project

## Tone of Voice

- **Primary: Czech (CZ)**, Secondary: English (EN)
- Use customer language: "E-commerce", "Online reklama", "PPC"
- Focus on business outcomes, not technical processes
- Use concrete numbers: "+30%", "60k/měsíc"
- Avoid: technical jargon, "My jsme nejlepší"

## cloud-migration.md → Marketing Project

Rewrite to marketing campaign/strategy project:

```yaml
---
title: "E-commerce růst strategie"
description: "Komplexní marketingová strategie pro růst e-shopu"
tags: ["SEO", "PPC", "E-commerce", "Analytics"]
category: "strategy"
client: "TechStartup s.r.o."
publishDate: 2024-01-15
---

# E-commerce Růst Strategie

## Výzva
E-shop potřeboval zvýšit tržby a získat více kvalitních zákazníků.

## Řešení
- SEO optimalizace pro klíčové produkty
- PPC kampaně na Google a Facebook
- Analytika a A/B testování

## Výsledky
- **+47%** návštěvnosti z vyhledávačů
- **+62%** konverzí
- **ROI 320%** z PPC kampaní
```

## cicd-automation.md → Marketing Project

Rewrite to marketing automation/content project:

```yaml
---
title: "Marketing automatizace"
description: "Automatizace e-mail marketingu a retargetingu"
tags: ["E-mail", "Automation", "E-commerce", "Conversion"]
category: "campaigns"
client: "E-commerce Solutions a.s."
publishDate: 2024-02-20
---

# Marketing Automatizace

## Výzva
E-shop měl nízkou retenci zákazníků a málo opakovaných nákupů.

## Řešení
- E-mail automatizace (welcome sequence, abandoned cart)
- Retargeting kampaně
- Personalizované nabídky

## Výsledky
- **+35%** opakovaných nákupů
- **+28%** průměrné hodnoty objednávky
- **2.4x** návratnost investice do e-mailu
```

## Key Changes

- Replace technical tags (AWS, Kubernetes, Docker) with marketing tags (SEO, PPC, Analytics)
- Replace `category: "devops"` with marketing categories
- Replace technical descriptions with business outcomes
- Add concrete metrics/ROI numbers
- Use Czech language with marketing focus

## Verification

After changes:

1. `npm run build` - must pass
2. Verify category is marketing (not devops)
3. Check all tags are marketing-related
