# 🚀 Phase 4: Performance Optimization & Testing Plan

**Based on:** Performance Audit Results (LCP: 484ms ✅ | CLS: 0.00 ✅)

---

## 📊 Current Status

| Metric       | Current      | Target  | Status       |
| ------------ | ------------ | ------- | ------------ |
| LCP          | 484ms        | <2500ms | ✅ Excellent |
| CLS          | 0.00         | <0.1    | ✅ Excellent |
| Asset Health | All 5 themes | No 404s | ✅ Pass      |

---

## 🎯 Optimizations to Implement

| #   | Optimization                | Impact               | Agent        |
| --- | --------------------------- | -------------------- | ------------ |
| 1   | WebP/AVIF Conversion        | -30-50% size         | Image Agent  |
| 2   | Astro `<Image />` Component | Auto optimization    | Dev Agent    |
| 3   | Critical Font Preload       | Eliminate font flash | Dev Agent    |
| 4   | Playwright Visual Tests     | Verify all themes    | Tester Agent |

---

## 🤖 Agent Assignments (Parallel)

### Agent 1: Image Optimizer

**Task:** Convert all images to WebP format

```bash
# Convert command template
cwebp -q 80 input.png -o output.webp

# Files to convert:
# public/images/theme/
# - logo_*.png → logo_*.webp
# - hero_*.jpg → hero_*.webp
# - photo_*.jpg → photo_*.webp
```

**Skills needed:**

- Image compression
- WebP format
- Batch processing

---

### Agent 2: Astro Developer

**Task:** Replace `<img>` with Astro's `<Image />` component

**Files to modify:**

1. `src/components/sections/Hero.astro` - Hero backgrounds + photos
2. `src/components/common/Header.astro` - Logo images

**Code changes:**

```astro
// Before
<img src="/images/theme/hero_titan.jpg" />

// After import {Image} from 'astro:assets';
<Image src={heroTitan} alt="" />
```

**Also add:**

- Font preload in `src/layouts/Layout.astro`
- Critical CSS optimization

---

### Agent 3: QA Tester

**Task:** Visual verification with Playwright

**Test scenarios:**

1. Load homepage → Verify TITAN theme (default)
2. Click each theme button → Verify switch works
3. Screenshot each theme → Save to `evidence/`
4. Verify CTA visible above fold
5. Mobile responsive test

**Tools:**

- Playwright MCP
- Screenshot comparison

---

## 📋 Execution Checklist

### Before Starting

- [ ] Backup current images
- [ ] Verify build passes
- [ ] Test server running

### Parallel Tasks

#### Task 1: WebP Conversion (Image Agent)

- [ ] Convert 5 logos to WebP
- [ ] Convert 5 hero backgrounds to WebP
- [ ] Convert 5 photos to WebP
- [ ] Verify quality (no visible loss)
- [ ] Update Hero.astro to use .webp
- [ ] Update Header.astro to use .webp

#### Task 2: Astro Image Component (Dev Agent)

- [ ] Import Image in Hero.astro
- [ ] Import Image in Header.astro
- [ ] Configure astro.config.mjs for images
- [ ] Add font preload in Layout.astro
- [ ] Run build → verify no errors

#### Task 3: Visual Testing (Tester Agent)

- [ ] Run Playwright tests
- [ ] Screenshot TITAN theme
- [ ] Screenshot NOVA theme
- [ ] Screenshot TARGET theme
- [ ] Screenshot SPARK theme
- [ ] Screenshot LUX theme
- [ ] Verify all CTAs visible

#### Task 4: Performance Re-check (Tester Agent)

- [ ] Run Lighthouse audit
- [ ] Verify LCP < 500ms
- [ ] Verify CLS < 0.1
- [ ] Check bundle size

---

## 🔧 Commands

### Start Dev Server

```bash
npm run dev
```

### Run Tests

```bash
npm run test
```

### Build

```bash
npm run build
```

### Visual Test (Playwright)

```bash
npx playwright test tests/e2e/performance.spec.ts
```

---

## 📁 Evidence Files

Save test results to:

```
evidence/
├── theme-titan.png
├── theme-nova.png
├── theme-target.png
├── theme-spark.png
├── theme-lux.png
└── performance-audit.md
```

---

## ✅ Success Criteria

| Criteria        | Target      |
| --------------- | ----------- |
| LCP             | < 500ms     |
| CLS             | < 0.1       |
| Image sizes     | -40% (WebP) |
| All themes load | 5/5         |
| CTA visible     | Above fold  |
| Build passes    | Exit 0      |

---

## 🚦 Readiness Check

Before running parallel agents:

- [ ] Build verified ✅
- [ ] All images exist ✅
- [ ] Theme system working ✅
- [ ] Dev server can start ✅

**Ready for execution?**
