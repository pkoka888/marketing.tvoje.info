import { test, expect } from '@playwright/test';

test.describe('Visual Regression - Homepage', () => {
  test('desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveScreenshot('homepage-desktop.png', { maxDiffPixels: 100 });
  });

  test('mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveScreenshot('homepage-mobile.png', { maxDiffPixels: 100 });
  });

  test('tablet', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveScreenshot('homepage-tablet.png', { maxDiffPixels: 100 });
  });
});

test.describe('Visual Regression - Pricing Page', () => {
  test('desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/pricing');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveScreenshot('pricing-desktop.png', { maxDiffPixels: 100 });
  });

  test('mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/pricing');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveScreenshot('pricing-mobile.png', { maxDiffPixels: 100 });
  });
});

test.describe('Visual Regression - Start Page', () => {
  test('desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/start');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveScreenshot('start-desktop.png', { maxDiffPixels: 100 });
  });
});

test.describe('Visual Regression - Theme Variations', () => {
  const themes = ['titan', 'nova', 'target', 'spark', 'lux'];

  for (const theme of themes) {
    test(`theme ${theme}`, async ({ page }) => {
      await page.goto('/');
      await page.waitForLoadState('networkidle');

      // Apply theme via localStorage
      await page.evaluate((t) => {
        localStorage.setItem('siteTheme', t);
        document.documentElement.setAttribute('data-site-theme', t);
      }, theme);

      await page.reload();
      await page.waitForLoadState('networkidle');

      await expect(page).toHaveScreenshot(`theme-${theme}.png`, { maxDiffPixels: 200 });
    });
  }
});
