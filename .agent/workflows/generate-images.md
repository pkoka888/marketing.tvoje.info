---
description: 'How to generate theme-specific image assets'
---

# 📸 Workflow: Generate Images (Sally)

This workflow guides the Graphic Designer (Sally) through generating specific assets for the site's theme system.

## 📋 Prerequisites

1. Ensure `GEMINI_API_KEY` is available for `gemini-2.5-flash` (Nano Banana).
2. The `docs/plans/image-generation-prompts-gemini.md` file must exist.

## 🚀 Steps

### 1. Identify Target Asset

Determine which theme and asset type you are working on:

- **Themes**: TITAN, NOVA, TARGET, SPARK, LUX
- **Types**: LOGO, PHOTO, HERO

### 2. Fetch Prompt

Read the specialized prompt from [image-generation-prompts-gemini.md](file:///C:/Users/pavel/projects/marketing.tvoje.info/docs/plans/image-generation-prompts-gemini.md).

### 3. Generate Content

// turbo
Run the generation command (or simulate if using interactive UI):

```powershell
# Example for logo
python scripts/generate_images.py --theme [THEME] --type [TYPE]
```

### 4. Verify & Catalog

1. Save output to `public/images/theme/`.
2. Ensure file naming follows `[type]_[theme].[ext]`.
3. Update the `IMAGE_INDEX.md` (if applicable) with the new asset metadata.

## 🎨 Quality Check

- Does the color palette match the theme in `src/styles/themes.css`?
- Is the lighting/vibe consistent with the theme description?
- Is the resolution correct (8K for BG, 4K for Photos)?
