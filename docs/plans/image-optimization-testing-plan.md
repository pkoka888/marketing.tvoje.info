# 🎯 Image Optimization & Testing Plan

## Current Status

### ✅ Generated Assets (15 images, 2.2MB total)

| Asset            | Count | Avg Size | Format |
| ---------------- | ----- | -------- | ------ |
| Logos            | 5     | 90KB     | PNG    |
| Hero Backgrounds | 5     | 150KB    | JPG    |
| Personal Photos  | 5     | 135KB    | JPG    |
| Special Graphics | 1     | 165KB    | PNG    |

---

## 🚀 Optimization Applied

### 1. Lazy Loading ✅

```html
<!-- Hero backgrounds now lazy load -->
<img src="hero_titan.jpg" loading="lazy" />
```

### 2. Mobile Optimization ✅

```css
/* Backgrounds hidden on mobile, solid colors used instead */
.hidden.lg: block;
```

### 3. Build Size

- Total: 2.2MB for 15 images
- Per theme: ~440KB average
- **Target: <100KB per theme for LCP**

---

## 📋 Optimization Recommendations

### Priority 1: Convert to WebP

```bash
# Convert all JPG to WebP (30-50% smaller)
cwebp -q 80 hero_titan.jpg -o hero_titan.webp
cwebp -q 80 hero_nova.jpg -o hero_nova.webp
# ... etc
```

### Priority 2: Resize for Hero

- Current: 3840×2160 (full 4K)
- Recommended: 1920×1080 (FHD)
- Savings: ~70%

### Priority 3: Compress Photos

- Current: 2000×3000 portrait
- Recommended: 800×1200 thumbnail
- For hero: 400×600

---

## 🧪 Testing Checklist

### Visual Verification Needed

| Test                   | Method                  | Status        |
| ---------------------- | ----------------------- | ------------- |
| Theme switcher works   | Click each theme button | ❌ Needs test |
| Default TITAN loads    | Open page, check hero   | ❌ Needs test |
| CTA visible above fold | Screenshot, check       | ❌ Needs test |
| Mobile layout          | Resize browser          | ❌ Needs test |
| Dark mode toggle       | Click moon/sun          | ❌ Needs test |

### Tools for Testing

1. **Playwright**: Screenshots via MCP
2. **Browser**: Manual testing at localhost:4321
3. **Lighthouse**: Performance audit

---

## 🔄 Image Regeneration Prompts

### Instructions for Gemini/Nano Banana

When regenerating images, use these specifications:

#### Logo (512×512 PNG)

- Minimalist "PK" initials
- Theme-specific colors
- Transparent background
- Vector-style

#### Hero Background (1920×1080 JPG)

- 50% quality for web
- Optimized for above-fold
- Lightweight (target: <50KB)

#### Personal Photo (800×1200 JPG)

- Professional portrait
- Theme-appropriate styling
- Compression: 70%

---

## 📦 File Structure After Optimization

```
public/images/theme/
├── logo_titan.webp        # 10KB
├── logo_nova.webp        # 12KB
├── logo_target.webp      # 15KB
├── logo_spark.webp      # 15KB
├── logo_lux.webp         # 12KB
├── hero_titan.webp      # 40KB
├── hero_nova.webp       # 50KB
├── hero_target.webp     # 35KB
├── hero_spark.webp      # 45KB
├── hero_lux.webp        # 35KB
├── photo_titan.webp     # 60KB
├── photo_nova.webp      # 70KB
├── photo_target.webp    # 65KB
├── photo_spark.webp    # 70KB
└── photo_lux.webp       # 60KB

Total: ~580KB (vs 2.2MB current)
Savings: 75%
```

---

## ⚡ Quick Commands

### Start Dev Server

```bash
npm run dev
```

### Start Preview

```bash
npm run build && npm run preview
```

### Test with Playwright

```bash
# Install Playwright if needed
npx playwright install

# Run visual test
npx playwright test
```

---

## ✅ Next Steps

1. [ ] Test theme switcher in browser
2. [ ] Verify CTA above fold on all themes
3. [ ] Convert images to WebP (optional)
4. [ ] Resize hero images (optional)
5. [ ] Run Lighthouse audit
6. [ ] Generate new photos via Gemini (when available)

---

_Last Updated: 2026-02-16_
