# Marketing Website Implementation Plan

## Current State

- ✅ Theme system (5 themes) working
- ✅ Hero section - marketing content OK
- ✅ Services section - marketing content OK
- ✅ Contact section - working
- ✅ About section - FIXED (was DevOps, now Marketing)
- ✅ Meta tags - FIXED (was DevOps, now Marketing)
- ❌ Photos are placeholders (need real photos)

---

## Phase 1: Fix About Section (Priority) - ✅ DONE

### Problem

- About.astro had hardcoded DevOps/AI skills: AWS, Azure, Kubernetes, Docker, Terraform, Python, TensorFlow
- Should have marketing experience/skills instead

### Solution - COMPLETED

Replaced with marketing-focused content:

| Before                            | After                                   |
| --------------------------------- | --------------------------------------- |
| DevOps skills (AWS, K8s, Docker)  | Marketing skills (SEO, PPC, Analytics)  |
| AI/ML skills (Python, TensorFlow) | Creative tools (Figma, HubSpot)         |
| Certifications (AWS, K8s)         | Marketing certs (Google, Meta, HubSpot) |
| Layout meta: "DevOps & AI"        | Layout meta: "Pavel Kašpar - Marketing" |

### Files Modified

- `src/components/sections/About.astro` - Marketing skills
- `src/layouts/Layout.astro` - Meta tags, structured data

---

## Phase 2: Generate Real Photos (Priority)

### Problem

- Current photos in `/public/images/theme/` are placeholders/generated images
- Not real photos of Pavel Kašpar

### Solution

Use Gemini CLI to generate professional marketing photos:

- `photo_titan.webp` - Professional headshot
- `photo_nova.webp` - Friendly/approachable shot
- `photo_target.webp` - Goal-oriented shot
- `photo_spark.webp` - Bold/creative shot
- `photo_lux.webp` - Premium/minimal shot

### Command

```bash
gemini media generate "Professional headshot of a Czech marketing expert, 40s, business attire, clean background, studio lighting" --output public/images/theme/photo_titan.webp
```

---

## Phase 3: Final Verification

### Checklist

- [x] About section shows marketing skills
- [x] Meta tags say "Marketing" not "DevOps"
- [x] Build passes
- [ ] Test in real browser
- [ ] Generate real photos

---

## Ready for Gemini 3 Pro Review

The website is now positioned as a **Marketing Portfolio** instead of DevOps/AI. All sections have appropriate marketing content. Next step is to:

1. Generate real photos with Gemini CLI
2. Visual verification in browser
3. Deploy to production
