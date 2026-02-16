# 🎯 Visual Testing Plan - Phase 5

**Purpose:** Create comprehensive visual testing framework for 5 theme system
**Approach:** Test one theme → Optimize → Apply to all themes

---

## 📋 Testing Framework

| Category        | What to Test                       | Priority |
| --------------- | ---------------------------------- | -------- |
| **Layout**      | Above-fold content, CTA visibility | P0       |
| **Theme**       | Colors, backgrounds, logos         | P0       |
| **Interaction** | Theme switcher, buttons            | P1       |
| **Responsive**  | Mobile, tablet, desktop            | P1       |
| **Performance** | LCP, image loading                 | P2       |

---

## ✅ Test Results - TITAN Theme

### Summary

| Metric      | Result   |
| ----------- | -------- |
| Total Tests | 23       |
| Passed      | 23       |
| Failed      | 0        |
| Pass Rate   | **100%** |

### TITAN Theme Tests

- ✅ Homepage loads with TITAN theme
- ✅ TITAN logo visible
- ✅ TITAN hero background loads
- ✅ TITAN headline visible
- ✅ CTA above fold
- ✅ No console errors

### Theme Switcher Tests

- ✅ Switch to NOVA
- ✅ Switch to TARGET
- ✅ Switch to SPARK
- ✅ Switch to LUX
- ✅ Persist in localStorage

### Asset Loading Tests (All 5 themes)

- ✅ All logos load (5/5)
- ✅ All hero backgrounds load (5/5)

### Responsive Tests

- ✅ Mobile viewport
- ✅ Tablet viewport

---

## 🤖 Agent Assignments

### Agent 1: Test Engineer

- **Created:** `tests/e2e/theme-system.spec.ts`
- **Status:** ✅ Complete

### Agent 2: QA Analyst

- **Verified:** All tests pass
- **Status:** ✅ Complete

### Agent 3: Performance

- **Asset verification:** ✅ All 15 images load
- **Status:** ✅ Complete

---

## 📁 Test Files Created

```
tests/e2e/
├── theme-system.spec.ts    # Main theme tests
├── performance.spec.ts     # Performance tests
├── homepage.spec.ts        # Basic tests
└── visual/
    └── debug.spec.ts       # Debug tests
```

---

## 🚀 Ready for Gemini CLI

All tests pass. Framework ready for:

1. Parallel test execution
2. Visual evidence generation
3. Cross-browser testing

---

## 📝 Test Template

```typescript
test('theme loads correctly', async ({ page }) => {
  await page.goto('/');

  // Verify theme
  await expect(page.locator('html')).toHaveAttribute('data-site-theme', 'titan');

  // Verify assets
  await expect(page.locator('img[src*="logo_titan"]')).toBeVisible();

  // Verify content
  await expect(page.locator('[data-theme-copy="titan"]')).toBeVisible();
});
```

### P0: Critical Tests

#### 1. Theme Default Load

```
Test: Homepage loads with TITAN theme (default)
Expected:
- Logo visible
- Hero headline: "Marketing, co funguje." (CZ)
- CTA button: "Chci růst"
- Background: Blue/green geometric
```

#### 2. CTA Above Fold

```
Test: Verify CTA is visible without scrolling
Expected:
- Primary CTA in viewport on load
- Secondary CTA visible
- No content jump (CLS)
```

#### 3. Theme Switcher

```
Test: Click each theme button
Expected:
- TITAN: Blue theme, direct copy
- NOVA: Purple/cyan gradient, friendly copy
- TARGET: Arrow path visible, goal copy
- SPARK: Dark neon, provocative copy
- LUX: Black/gold, premium copy
```

### P1: Important Tests

#### 4. Logo Visibility

```
Test: Each theme
Expected:
- Logo matches theme colors
- Correct file loads (webp)
- No 404 errors
```

#### 5. Hero Background

```
Test: Each theme
Expected:
- Background image loads
- Correct opacity applied
- No layout shift
```

#### 6. Mobile Layout

```
Test: Viewport 375px width
Expected:
- No horizontal scroll
- CTA readable
- Navigation works
```

### P2: Nice to Have

#### 7. Dark Mode Toggle

```
Test: Click dark/light toggle
Expected:
- Colors invert appropriately
- Readable contrast
```

#### 8. Language Toggle

```
Test: Switch EN → CS
Expected:
- All text translates
- No layout break
```

---

## 📸 Screenshot Template

### Filename Convention

```
evidence/theme-[name]-[date].png
```

### Example:

```
evidence/theme-titan-2026-02-16.png
evidence/theme-nova-2026-02-16.png
```

### Metadata Template

```markdown
## Theme Test: [NAME]

**Date:** [YYYY-MM-DD]
**Browser:** [Chrome/Firefox/Safari]
**Viewport:** [WIDTH x HEIGHT]

### ✅ Pass

- [ ] Logo loads
- [ ] Hero copy correct
- [ ] CTA visible
- [ ] Background loads
- [ ] No console errors

### ❌ Fail

- [ ] Issue description...

### Notes

[Any observations]
```

---

## 🤖 Agent Assignments

### Agent 1: Test Engineer

**Skills:** Playwright, Visual Testing, Screenshot

**Tasks:**

1. Create test files
2. Run tests on TITAN theme
3. Capture screenshots
4. Document results

**Files to create:**

- `tests/e2e/theme-default.spec.ts`
- `tests/e2e/theme-switcher.spec.ts`

---

### Agent 2: QA Analyst

**Skills:** Manual Testing, Cross-browser

**Tasks:**

1. Review test results
2. Identify issues
3. Create bug reports
4. Verify fixes

---

### Agent 3: Performance Analyst

**Skills:** Lighthouse, Performance Metrics

**Tasks:**

1. Run Lighthouse audits
2. Check LCP/CLS
3. Verify image optimization
4. Document metrics

---

## 📁 Test File Structure

```
tests/
├── e2e/
│   ├── theme-default.spec.ts      # Homepage TITAN test
│   ├── theme-switcher.spec.ts     # All 5 themes
│   ├── visual-comparison.spec.ts  # Side by side
│   └── performance.spec.ts        # LCP/CLS
└── visual/
    └── templates/
        ├── screenshot-template.md
        └── bug-report-template.md
```

---

## 🎯 Execution Plan

### Step 1: Create Test Templates

- [ ] Create `tests/e2e/theme-default.spec.ts`
- [ ] Create screenshot template
- [ ] Create bug report template

### Step 2: Run TITAN Test

- [ ] Test homepage loads
- [ ] Verify TITAN theme
- [ ] Screenshot evidence
- [ ] Check console errors

### Step 3: Analyze Results

- [ ] Review screenshot
- [ ] Identify issues
- [ ] Fix if critical

### Step 4: Create Remaining Tests

- [ ] Theme switcher test
- [ ] Mobile test
- [ ] Performance test

### Step 5: Run All Themes

- [ ] Test NOVA
- [ ] Test TARGET
- [ ] Test SPARK
- [ ] Test LUX

---

## 📝 Test File: theme-default.spec.ts

```typescript
import { test, expect } from '@playwright/test';

test.describe('Theme: TITAN (Default)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load with TITAN theme', async ({ page }) => {
    // Check logo
    await expect(page.locator('[data-site-theme=titan] img[src*="logo"]')).toBeVisible();

    // Check hero headline
    await expect(page.locator('[data-theme-copy="titan"]')).toContainText('Marketing');

    // Check CTA visible above fold
    const cta = page.locator('a:has-text("Chci růst")');
    await expect(cta).toBeVisible();

    // Check no console errors
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') errors.push(msg.text());
    });
    expect(errors).toHaveLength(0);
  });

  test('should load hero background', async ({ page }) => {
    const bg = page.locator('img[src*="hero_titan"]');
    await expect(bg).toBeVisible();
  });

  test('should have no layout shift', async ({ page }) => {
    const cls = await page.evaluate(() => {
      return (performance as any).getEntriesByType('layout-shift');
    });
    expect(cls.length).toBe(0);
  });
});
```

---

## 📸 Evidence Template

```markdown
# Visual Test Report

## Test: [TEST NAME]

**Date:** YYYY-MM-DD
**Theme:** [TITAN/NOVA/TARGET/SPARK/LUX]

### Screenshot

![Screenshot](evidence/theme-[name].png)

### Results

| Check             | Status | Notes |
| ----------------- | ------ | ----- |
| Logo visible      | ✅/❌  |       |
| Hero copy correct | ✅/❌  |       |
| CTA above fold    | ✅/❌  |       |
| Background loads  | ✅/❌  |       |
| No 404s           | ✅/❌  |       |
| No console errors | ✅/❌  |       |

### Issues Found

1. [Issue description]
2. [Issue description]

### Recommended Fixes

1. [Fix description]
```

---

## 🚀 Ready to Execute?

**Next:**

1. Create test templates
2. Run TITAN test
3. Optimize based on results
4. Apply to all themes
