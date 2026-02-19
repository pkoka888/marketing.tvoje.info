import { test, expect } from '@playwright/test';

/**
 * Theme System Visual Tests
 */

test.describe('Theme System', () => {
  test('should load with TITAN theme by default', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const html = page.locator('html');
    await expect(html).toHaveAttribute('data-site-theme', 'titan');
  });

  test('should apply theme via setSiteTheme function', async ({ page }) => {
    await page.goto('/');

    // Test all themes via JavaScript API
    const themes = ['nova', 'target', 'spark', 'lux', 'obsidian', 'playful'];

    for (const theme of themes) {
      await page.evaluate((t) => (window as any).setSiteTheme(t), theme);
      await page.waitForTimeout(200);

      const html = page.locator('html');
      await expect(html).toHaveAttribute('data-site-theme', theme);
    }
  });

  test('should persist theme in localStorage', async ({ page }) => {
    await page.goto('/');

    // Set theme via JS
    await page.evaluate(() => (window as any).setSiteTheme('nova'));
    await page.waitForTimeout(200);

    // Reload
    await page.reload();
    await page.waitForLoadState('networkidle');

    // Verify persisted
    const html = page.locator('html');
    await expect(html).toHaveAttribute('data-site-theme', 'nova');
  });

  test('should have all 7 themes defined', async ({ page }) => {
    await page.goto('/');

    // Check themes are available in the dropdown
    const themeOptions = page.locator('.theme-option, [data-theme]');
    const count = await themeOptions.count();

    // Should have at least 7 theme options
    expect(count).toBeGreaterThanOrEqual(7);
  });
});
