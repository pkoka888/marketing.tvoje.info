# BMAD Story: Portfolio Image Generation

# Story ID: IMG-001

# Priority: HIGH

# Status: READY FOR DELEGATION

## Story

As a portfolio site owner, I need compelling visual content for case studies and
social sharing so that visitors can immediately understand my work and the site
looks professional when shared on social media.

## Business Value

- **Credibility**: Real visuals increase trust by 65% (Nielsen Norman Group)
- **Social Sharing**: OG images increase click-through rates by 40%
- **Portfolio Quality**: Case studies with visuals convert 3x better
- **SEO**: Image search traffic for portfolio keywords

## Acceptance Criteria

- [ ] Generate 10 project case study images (1024x1024 or 1200x630)
- [ ] Generate 5 OG/social images for main pages
- [ ] All images use consistent style (tech/devops theme)
- [ ] Images optimized for web (< 200KB each)
- [ ] Alt text and metadata included
- [ ] Images committed to `public/images/projects/`

## Technical Details

### Missing Images (CRITICAL GAP)

Projects referencing non-existent images:

1. `/images/projects/ai-chatbot.jpg` - AI chatbot case study
2. `/images/projects/marketing-automation.jpg` - Automation workflow
3. `/images/projects/brand-identity.jpg` - Branding project
4. `/images/projects/ecommerce-seo.jpg` - SEO results
5. `/images/projects/growth-funnel.jpg` - Funnel optimization
6. `/images/projects/kubernetes-management.jpg` - K8s infrastructure
7. `/images/projects/cloud-migration.jpg` - Cloud migration
8. `/images/projects/cicd-automation.jpg` - CI/CD pipeline
9. `/images/projects/ai-ml-infrastructure.jpg` - ML infrastructure

OG Images needed:

1. Homepage OG (1200x630)
2. Services OG (1200x630)
3. Projects OG (1200x630)
4. Contact OG (1200x630)
5. About OG (1200x630)

### Generation Script

**File:** `scripts/generate_images_advanced.py` **Provider:** NVIDIA SDXL
(FREE - 1000-5000 credits) **Command:**

```bash
python scripts/generate_images_advanced.py \
  --prompt "Professional tech visualization: [description]" \
  --output public/images/projects/[name].jpg \
  --provider nvidia
```

### Image Style Guidelines

- **Theme**: Modern, professional, tech-focused
- **Colors**: Blue (#3b82f6), Purple (#8b5cf6), Dark backgrounds
- **Style**: Clean vector illustrations, isometric diagrams, abstract tech
- **Mood**: Innovative, trustworthy, cutting-edge

## Prompts Template

### Project Images (1024x1024)

```
"Professional isometric illustration of [topic],
modern tech company style, blue and purple color scheme,
clean lines, dark background, professional lighting,
high quality render, 3D visualization"
```

### OG Images (1200x630)

```
"Wide banner image for [topic], professional tech company,
modern minimalist design, text-safe area in center,
blue gradient background, subtle tech patterns,
LinkedIn/Twitter social media optimized"
```

## Delegation Plan

### To: Kilo Code (Free Model)

**Tasks:**

1. Execute `generate_images_advanced.py` with provided prompts
2. Optimize images for web (compress to < 200KB)
3. Verify images exist in `public/images/projects/`
4. Update project MD files if paths changed

### Prompts to Generate (Delegate to Kilo)

**Batch 1: DevOps Projects**

```bash
python scripts/generate_images_advanced.py --provider nvidia \
  --prompt "Isometric Kubernetes cluster visualization, containers and pods, blue purple gradient, modern tech illustration, clean professional style" \
  --output public/images/projects/kubernetes-management.jpg

python scripts/generate_images_advanced.py --provider nvidia \
  --prompt "Cloud migration concept, servers moving to cloud, AWS Azure GCP symbols, isometric 3D illustration, tech company style, blue tones" \
  --output public/images/projects/cloud-migration.jpg

python scripts/generate_images_advanced.py --provider nvidia \
  --prompt "CI/CD pipeline visualization, automated deployment, GitHub Actions workflow, modern tech diagram, blue and purple, clean minimal" \
  --output public/images/projects/cicd-automation.jpg
```

**Batch 2: AI Projects**

```bash
python scripts/generate_images_advanced.py --provider nvidia \
  --prompt "AI chatbot interface, customer support automation, modern UI design, ChatGPT integration visual, professional tech style" \
  --output public/images/projects/ai-chatbot.jpg

python scripts/generate_images_advanced.py --provider nvidia \
  --prompt "Machine learning infrastructure, ML pipelines, data flow visualization, neural network diagram, tech company style, purple blue" \
  --output public/images/projects/ai-ml-infrastructure.jpg

python scripts/generate_images_advanced.py --provider nvidia \
  --prompt "Marketing automation workflow, email sequences, CRM integration, lead nurturing diagram, modern tech illustration" \
  --output public/images/projects/marketing-automation.jpg
```

**Batch 3: Marketing Projects**

```bash
python scripts/generate_images_advanced.py --provider nvidia \
  --prompt "E-commerce SEO optimization, search rankings visualization, organic traffic growth chart, modern tech style, professional" \
  --output public/images/projects/ecommerce-seo.jpg

python scripts/generate_images_advanced.py --provider nvidia \
  --prompt "Growth funnel optimization, conversion rate improvement, marketing funnel diagram, modern professional style, blue gradient" \
  --output public/images/projects/growth-funnel.jpg

python scripts/generate_images_advanced.py --provider nvidia \
  --prompt "Brand identity design system, logo variations, color palette, typography showcase, professional branding agency style" \
  --output public/images/projects/brand-identity.jpg
```

## Definition of Done

- [ ] All 9 project images generated
- [ ] All 5 OG images generated
- [ ] Images optimized and < 200KB
- [ ] Images committed to git
- [ ] Site builds without image errors
- [ ] Visual regression tests pass

## Dependencies

- ✅ NVIDIA_API_KEY in .env
- ✅ generate_images_advanced.py script ready
- ⏳ Kilo Code delegation

## Estimation

- **Kilo Code execution**: 30 minutes (parallel generation)
- **Optimization**: 15 minutes
- **Total**: 45 minutes

## Notes

- Use `--provider nvidia` for FREE generation
- If NVIDIA fails, fallback to `--provider gemini` (also free)
- Keep prompts consistent for cohesive look
- Generate at 1024x1024, downscale for web
