# Comprehensive Testing Plan - Marketing Portfolio

**Created**: 2026-02-16
**Status**: Planning
**Project**: marketing.tvoje.info

---

## Executive Summary

This plan defines a comprehensive testing strategy for the marketing portfolio website, leveraging 2026 best practices with parallel subagent orchestration. The testing framework combines visual regression testing, functional E2E tests, performance benchmarks, and automated CI/CD pipelines.

---

## Research Findings

### 1. Testing Tools (2026 Best Practices)

| Tool                | Purpose                   | Status in Project     |
| ------------------- | ------------------------- | --------------------- |
| **Playwright**      | E2E + Visual testing      | ✅ Already installed  |
| **Vitest**          | Unit tests                | ✅ Already configured |
| **Lighthouse CI**   | Performance/Accessibility | ⏳ To integrate       |
| **Percy/Chromatic** | Visual regression         | Optional              |
| **axe-core**        | Accessibility testing     | ⏳ To integrate       |

### 2. Key Sources

- Playwright built-in `toHaveScreenshot()` for visual regression
- Lighthouse + Playwright integration via Chrome DevTools Protocol
- Page Object Model (POM) for maintainable tests
- Parallel execution with sharding for CI

---

## Testing Architecture

### Test Pyramid

```
         ┌─────────────┐
         │  Visual    │  ← Percy, toHaveScreenshot
         │   Tests    │
        ┌──────────────┐
        │  E2E Tests  │  ← Playwright, Page Object Model
        │  (20 tests) │
       ┌────────────────┐
       │  Integration │  ← API tests, form validation
       │    Tests     │
      ┌──────────────────┐
      │   Unit Tests   │  ← Vitest (10 tests)
      └──────────────────┘
```

---

## Test Categories

### 1. Visual Regression Tests

| Test                | Target            | Method             |
| ------------------- | ----------------- | ------------------ |
| Homepage screenshot | Desktop/Mobile    | toHaveScreenshot() |
| Pricing page        | Desktop/Mobile    | Visual diff        |
| Theme variations    | 5 themes          | Percy or built-in  |
| Component gallery   | All UI components | Percy              |

### 2. Functional E2E Tests

| Test Suite   | Tests | Focus                           |
| ------------ | ----- | ------------------------------- |
| Navigation   | 5     | Menu, links, routing            |
| Forms        | 4     | Contact, onboarding, validation |
| Themes       | 3     | Theme switching, persistence    |
| Localization | 2     | EN/CS routing                   |

### 3. Performance Tests

| Metric        | Target | Tool          |
| ------------- | ------ | ------------- |
| LCP           | <2.5s  | Lighthouse    |
| CLS           | <0.1   | Lighthouse    |
| Performance   | ≥95    | Lighthouse CI |
| Accessibility | ≥95    | Lighthouse CI |
| SEO           | ≥95    | Lighthouse CI |

### 4. Accessibility Tests

| Check                  | Tool         |
| ---------------------- | ------------ |
| WCAG 2.2 AA compliance | axe-core     |
| Keyboard navigation    | Playwright   |
| Screen reader          | Manual + axe |
| Color contrast         | axe-core     |

---

## Subagent Orchestration

### Phase 1: Research & Setup (Parallel)

| Agent       | Task                              | Deliverable                |
| ----------- | --------------------------------- | -------------------------- |
| **Agent 1** | Configure Playwright visual tests | `tests/e2e/visual.spec.ts` |
| **Agent 2** | Set up Lighthouse CI              | `lighthouserc.json`        |
| **Agent 3** | Create Page Objects               | `tests/e2e/pages/`         |
| **Agent 4** | Configure axe accessibility       | `tests/e2e/a11y.spec.ts`   |

### Phase 2: Test Implementation (Parallel)

| Agent       | Task                    | Files                             |
| ----------- | ----------------------- | --------------------------------- |
| **Agent 1** | Visual regression suite | `tests/e2e/visual/`               |
| **Agent 2** | Functional E2E suite    | `tests/e2e/functional/`           |
| **Agent 3** | Performance suite       | `tests/e2e/performance.spec.ts`   |
| **Agent 4** | Accessibility suite     | `tests/e2e/accessibility.spec.ts` |

### Phase 3: CI/CD Integration (Sequential)

| Step | Task                    | File                               |
| ---- | ----------------------- | ---------------------------------- |
| 1    | Update GitHub workflow  | `.github/workflows/test.yml`       |
| 2    | Add Lighthouse CI       | `.github/workflows/lighthouse.yml` |
| 3    | Configure test reports  | `playwright.config.ts`             |
| 4    | Add slack notifications | `.github/workflows/notify.yml`     |

---

## Test Files Structure

```
tests/
├── e2e/
│   ├── pages/
│   │   ├── HomePage.ts
│   │   ├── PricingPage.ts
│   │   ├── StartPage.ts
│   │   └── BasePage.ts
│   ├── visual/
│   │   ├── homepage.spec.ts
│   │   ├── pricing.spec.ts
│   │   └── themes.spec.ts
│   ├── functional/
│   │   ├── navigation.spec.ts
│   │   ├── forms.spec.ts
│   │   └── themes.spec.ts
│   ├── performance.spec.ts
│   ├── accessibility.spec.ts
│   └── smoke.spec.ts
├── unit/
│   └── utils/
│       └── debug.test.ts
├── integration/
│   └── forms.spec.ts
└── fixtures/
    └── users.ts
```

---

## Implementation Templates

### Template 1: Page Object Model

```typescript
// tests/e2e/pages/HomePage.ts
import { type Page, type Locator } from '@playwright/test';

export class HomePage {
  readonly page: Page;
  readonly heroTitle: Locator;
  readonly ctaButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.heroTitle = page.locator('h1');
    this.ctaButton = page.locator('a:has-text("View Projects")');
  }

  async goto(): Promise<void> {
    await this.page.goto('/');
  }

  async clickCTA(): Promise<void> {
    await this.ctaButton.click();
  }
}
```

### Template 2: Visual Test

```typescript
// tests/e2e/visual/homepage.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression - Homepage', () => {
  test('desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage-desktop.png');
  });

  test('mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage-mobile.png');
  });
});
```

### Template 3: Lighthouse Performance Test

```typescript
// tests/e2e/performance.spec.ts
import { test, expect } from '@playwright/test';
import { chromium } from '@playwright/test';

test('Lighthouse performance', async ({ page }) => {
  await page.goto('/');

  const client = await page.context().newCDPSession(page);
  const { metrics } = await client.send('Performance.getMetrics');

  expect(metrics.find((m) => m.name === 'FirstContentfulPaint').value).toBeLessThan(2500);
});
```

### Template 4: GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test

      - name: Run E2E tests
        run: npx playwright test --shard=${{ matrix.shard }}/3

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-${{ matrix.shard }}
          path: test-results/
```

---

## Parallel Execution Strategy

### Playwright Sharding

```json
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['list'],
  ],
});
```

### Test Execution Matrix

| Runner | Tests | Parallel  | Time |
| ------ | ----- | --------- | ---- |
| Local  | 20    | 4 workers | ~30s |
| CI     | 20    | 3 shards  | ~45s |
| Local  | 50    | 8 workers | ~1m  |
| CI     | 50    | 5 shards  | ~2m  |

---

## Quality Gates

| Gate                     | Condition    | Action      |
| ------------------------ | ------------ | ----------- |
| Unit Tests               | 100% pass    | Block merge |
| E2E Tests                | 100% pass    | Block merge |
| Visual Diffs             | 0 unexpected | Block merge |
| Lighthouse Performance   | ≥95          | Warning     |
| Lighthouse Accessibility | ≥95          | Warning     |
| Lighthouse SEO           | ≥95          | Warning     |

---

## Current Test Status

| Category      | Tests | Status       |
| ------------- | ----- | ------------ |
| Unit          | 10    | ✅ Passing   |
| Performance   | 9     | ✅ Passing   |
| Visual        | 0     | ⏳ To create |
| Functional    | 2     | ✅ Basic     |
| Accessibility | 0     | ⏳ To create |

---

## Implementation Tasks

### Task Group 1: Visual Testing

| #   | Task                                 | Files                           |
| --- | ------------------------------------ | ------------------------------- |
| V1  | Install Playwright screenshot plugin | package.json                    |
| V2  | Create visual test suite             | tests/e2e/visual/               |
| V3  | Configure baseline screenshots       | tests/e2e/visual/baselines/     |
| V4  | Add theme visual tests               | tests/e2e/visual/themes.spec.ts |

### Task Group 2: Functional Testing

| #   | Task                  | Files                                   |
| --- | --------------------- | --------------------------------------- |
| F1  | Create Page Objects   | tests/e2e/pages/                        |
| F2  | Navigation test suite | tests/e2e/functional/navigation.spec.ts |
| F3  | Forms test suite      | tests/e2e/functional/forms.spec.ts      |
| F4  | Theme switching tests | tests/e2e/functional/themes.spec.ts     |

### Task Group 3: Performance & A11y

| #   | Task                 | Files                           |
| --- | -------------------- | ------------------------------- |
| P1  | Lighthouse CI config | lighthouserc.json               |
| P2  | Performance suite    | tests/e2e/performance.spec.ts   |
| P3  | Accessibility suite  | tests/e2e/accessibility.spec.ts |
| P4  | CI/CD integration    | .github/workflows/              |

### Task Group 4: Reporting

| #   | Task                | Files                        |
| --- | ------------------- | ---------------------------- |
| R1  | HTML report config  | playwright.config.ts         |
| R2  | Test results viewer | -                            |
| R3  | Slack notifications | .github/workflows/notify.yml |

---

## Timeline Estimate

| Phase            | Tasks | Duration |
| ---------------- | ----- | -------- |
| Setup            | 4     | 15 min   |
| Visual Tests     | 4     | 20 min   |
| Functional Tests | 4     | 25 min   |
| Performance/A11y | 4     | 20 min   |
| CI/CD            | 4     | 20 min   |

**Total**: ~100 minutes

---

## Questions for User

1. Should visual tests use Percy (cloud) or Playwright built-in (local)?
2. What slack channel for test notifications?
3. Should we add browserstack/cross-browser testing?
4. What is the target test count (currently ~30, target ~50)?

---

## Success Criteria

| Metric            | Current | Target |
| ----------------- | ------- | ------ |
| Unit Tests        | 10      | 15+    |
| E2E Tests         | 2       | 30+    |
| Visual Tests      | 0       | 15+    |
| Performance Tests | 9       | 15+    |
| Test Coverage     | ?       | 80%+   |
| CI Runtime        | -       | <5 min |

---

_Plan Status: READY FOR EXECUTION_
