# Playwright Visual Testing Best Practices 2026

**Date**: 2026-02-17
**Research**: Web Search

---

## Key Findings

### 1. Built-in Playwright Visual Testing

Playwright has built-in visual testing via `toHaveScreenshot()`:

- No plugins required
- Uses pixelmatch for comparison
- Stores baselines in Git

### 2. Best Practices

| Practice                    | Details                                              |
| --------------------------- | ---------------------------------------------------- |
| **Threshold tuning**        | Use `maxDiffPixelRatio: 0.01` to allow 1% difference |
| **Disable animations**      | Set `animations: "disabled"` in config               |
| **Mask dynamic content**    | Hide timestamps, random content                      |
| **Single browser**          | Run visual tests in Chromium only                    |
| **Environment consistency** | Use Docker for CI to match local rendering           |

### 3. Configuration Example

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
  },
  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.01,
      threshold: 0.1,
    },
  },
});
```

### 4. Visual Test Organization

```
tests/
  visual/
    homepage.spec.ts
    services.spec.ts
    components/
      button.spec.ts
      card.spec.ts
```

### 5. CI Integration

```yaml
# .github/workflows/visual.yml
name: Visual Tests
on: [pull_request]
jobs:
  visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npx playwright test --project=chromium
```

---

## Recommendations for Our Project

### Current Setup

- ✅ We have 23 visual regression tests
- ✅ Using Playwright with toHaveScreenshot()
- ✅ Desktop + Mobile viewports

### Improvements Needed

1. **Add threshold config** - reduce false positives
2. **Disable animations** - for consistent screenshots
3. **Mask dynamic content** - dates, random elements
4. **Organize by feature** - separate page tests from component tests
5. **Add CI workflow** - run on PR

---

## Resources

- Playwright Docs: https://playwright.dev/docs/test-snapshots
- Best Practices: Use maxDiffPixelRatio for font rendering differences
- Tool Comparison: Playwright (free) vs Percy/Chromatic (paid)

---

## Next Steps

1. Update playwright.config.ts with threshold settings
2. Add animation disable for visual tests
3. Create dedicated visual test workflow
