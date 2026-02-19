# IMAGE_AGENTS_REFERENCE.md

> Compact reference for AI image generation options, scripts, and update
> procedures. Part of AGENTS.md ecosystem - governed by same synchronization
> protocol.

---

## 1. Image Generation Options

### Free Providers (Use First)

| Provider   | Model           | Cost              | Quality     | Best For                        |
| ---------- | --------------- | ----------------- | ----------- | ------------------------------- |
| NVIDIA     | SDXL 1.0        | 1000-5000 credits | High        | Hero images, marketing graphics |
| Gemini     | 2.5 Flash Image | Daily free tier   | Medium-High | Quick prototypes, testing       |
| Cloudflare | FLUX.1          | 10k neurons/day   | High        | Bulk generation                 |

### Paid Providers (Requires Approval)

| Provider | Model    | Cost            | Quality | Best For            |
| -------- | -------- | --------------- | ------- | ------------------- |
| OpenAI   | DALL-E 3 | ~0.04 USD/image | Highest | Client deliverables |
| OpenAI   | DALL-E 2 | ~0.02 USD/image | High    | Budget-conscious    |

### Self-Hosted Options

| Tool                 | Cost | GPU Required | Quality | Best For                |
| -------------------- | ---- | ------------ | ------- | ----------------------- |
| Stable Diffusion 3.5 | Free | Yes (8GB+)   | High    | Full control, no limits |
| FLUX.1               | Free | Yes (12GB+)  | Highest | Professional quality    |
| ComfyUI              | Free | Yes          | Highest | Custom workflows        |

---

## 2. Scripts and Commands

### Image Generation Scripts

List available models: python scripts/generate_images_advanced.py --list-models

Generate with NVIDIA (FREE - default): python
scripts/generate_images_advanced.py --prompt "hero image" --output image.png

Generate with specific provider: python scripts/generate_images_advanced.py
--prompt "hero" --output img.png --provider nvidia python
scripts/generate_images_advanced.py --prompt "hero" --output img.png --provider
gemini python scripts/generate_images_advanced.py --prompt "hero" --output
img.png --provider cloudflare python scripts/generate_images_advanced.py
--prompt "hero" --output img.png --provider openai

### Orchestration Scripts

Image generation research: python scripts/orchestrate_image_generation.py --list
python scripts/orchestrate_image_research.py --list

Batch image generation: python scripts/generate_images_advanced.py --batch
prompts.txt --output-dir output/images

Convert to WebP: node scripts/convert-to-webp.cjs

---

## 3. Update Frequency

### When to Refresh

| Trigger                 | Action                      | Who       |
| ----------------------- | --------------------------- | --------- |
| New model released      | Run --list-models to verify | Any agent |
| Provider pricing change | Update this document        | Kilo Code |
| Free tier exhausted     | Switch provider             | Any agent |
| Monthly                 | Run update_free_models.py   | Kilo Code |

### Update Commands

Update free models: python scripts/update_free_models.py

Preview changes: python scripts/update_free_models.py --dry-run

---

## 4. Model Priority

1. NVIDIA SDXL (FREE) - Primary for marketing graphics
2. Cloudflare FLUX (FREE) - Secondary for bulk
3. Gemini (FREE) - Quick tests only
4. DALL-E 3 (PAID) - Client deliverables only

---

## 5. Quick Reference

| Task               | Provider   | Command               |
| ------------------ | ---------- | --------------------- |
| Quick test         | Gemini     | --provider gemini     |
| Marketing hero     | NVIDIA     | --provider nvidia     |
| Bulk assets        | Cloudflare | --provider cloudflare |
| Client deliverable | OpenAI     | --provider openai     |

---

Last Updated: 2026-02-19
