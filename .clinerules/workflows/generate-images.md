# Workflow: Generate Image

Generate images using AI providers via `scripts/generate_images.py`.

## Providers

| Provider | Model | Cost | Key |
|----------|-------|------|-----|
| nvidia | Stable Diffusion XL | Free | `NVIDIA_API_KEY` |
| openai | DALL-E 3 | Paid | `OPENAI_API_KEY` |

## Usage

```bash
# Free (default — NVIDIA SDXL)
python scripts/generate_images.py \
    --prompt "Marketing infographic for web performance" \
    --output public/images/infographic.png

# Paid (DALL-E 3)
python scripts/generate_images.py \
    --prompt "Hero image for portfolio landing page" \
    --output public/images/hero.png \
    --provider openai
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--prompt` | Yes | — | Image generation prompt |
| `--output` | Yes | — | Output file path |
| `--provider` | No | `nvidia` | `nvidia` or `openai` |

## Notes

- Output directory is created automatically
- NVIDIA SDXL generates 1024x1024 images
- DALL-E 3 generates 1024x1024 standard quality
- Keys loaded from `.env` in project root
