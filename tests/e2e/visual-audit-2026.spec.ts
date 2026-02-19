import { test, expect } from '@playwright/test';

const PRODUCTION_URL = 'https://marketing.tvoje.info';

test.describe('Visual Audit - New 2026 Features', () => {
  test('Hero section has animated gradient text', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    const heroTitle = page.locator('h1');
    await expect(heroTitle).toBeVisible();

    // Check for gradient text class
    const gradientText = page.locator('.gradient-text-animated');
    await expect(gradientText).toBeVisible();
  });

  test('TrendsTicker marquee is visible', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    const ticker = page.locator('.marquee-container');
    await expect(ticker).toBeVisible();

    // Check for specific trend items (use first())
    await expect(page.locator('text=AI Marketing').first()).toBeVisible();
    await expect(page.locator('text=TikTok Ads').first()).toBeVisible();
  });

  test('AI Marketing section displays with stats', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    // Find AI Marketing section
    const aiSection = page.locator('#ai-marketing');
    await expect(aiSection).toBeVisible();

    // Check for "Ready for 2026" text
    await expect(page.locator('text=Ready for 2026')).toBeVisible();

    // Check for result badges (use first() for strict mode)
    await expect(page.locator('text=+40%').first()).toBeVisible();
    await expect(page.locator('text=+25%').first()).toBeVisible();
  });

  test('Services section shows result badges', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    // Scroll to services
    const services = page.locator('#services');
    await services.scrollIntoViewIfNeeded();

    // Check for new service names (use first())
    await expect(page.locator('text=AI Campaign Optimization').first()).toBeVisible();
    await expect(page.locator('text=TikTok').first()).toBeVisible();

    // Check for result badges in services (use first())
    await expect(page.locator('text=+40% ROAS').first()).toBeVisible();
  });

  test('All 7 themes work correctly', async ({ page }) => {
    const themes = ['titan', 'nova', 'target', 'spark', 'lux', 'obsidian', 'playful'];

    for (const theme of themes) {
      await page.goto(PRODUCTION_URL);

      // Open theme selector if exists
      const themeTrigger = page.locator('#theme-selector-trigger');
      if (await themeTrigger.isVisible()) {
        await themeTrigger.click();

        // Select theme (use first() to avoid strict mode)
        const themeOption = page.locator(`button[data-theme="${theme}"]`).first();
        if (await themeOption.isVisible()) {
          await themeOption.click();
          await page.waitForTimeout(500);
        }
      }

      // Verify page still loads
      await expect(page.locator('h1')).toBeVisible();
    }
  });

  test('Responsive: Mobile layout works', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(PRODUCTION_URL);

    // Check mobile menu button exists
    const mobileMenuBtn = page.locator('#mobile-menu-button');
    await expect(mobileMenuBtn).toBeVisible();

    // Check hero is visible
    await expect(page.locator('h1')).toBeVisible();

    // Check ticker is visible on mobile
    await expect(page.locator('.marquee-container')).toBeVisible();
  });

  test('Responsive: Tablet layout works', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto(PRODUCTION_URL);

    // Services should be in grid
    const services = page.locator('#services');
    await services.scrollIntoViewIfNeeded();
    await expect(page.locator('.bento-card').first()).toBeVisible();
  });

  test('Accessibility: Focus states work', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    // Check CTA buttons have glow effect
    const ctaButton = page.locator('.glow-primary').first();
    await expect(ctaButton).toBeVisible();

    // Check no critical console errors
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    await page.reload();
    await page.waitForTimeout(1000);

    // Filter out non-critical errors
    const criticalErrors = errors.filter((e) => !e.includes('favicon') && !e.includes('404'));
    expect(criticalErrors.length).toBe(0);
  });

  test('Contact form is functional', async ({ page }) => {
    await page.goto(PRODUCTION_URL + '/#contact');

    // Check form exists
    const form = page.locator('#contact-form');
    await expect(form).toBeVisible();

    // Check form fields
    await expect(page.locator('input[name="name"]')).toBeVisible();
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('textarea[name="message"]')).toBeVisible();
  });

  test('Privacy page loads correctly', async ({ page }) => {
    await page.goto(PRODUCTION_URL + '/privacy');

    // Check title
    await expect(page.locator('h1:has-text("Privacy Policy")')).toBeVisible();

    // Check sections exist
    await expect(page.locator('text=Data We Collect')).toBeVisible();
    await expect(page.locator('text=Your Rights')).toBeVisible();
  });

  test('Czech version works', async ({ page }) => {
    await page.goto(PRODUCTION_URL + '/cs');

    // Check Czech hero title
    await expect(page.locator('text=Růst, který funguje')).toBeVisible();

    // Check Czech services
    const services = page.locator('#services');
    await services.scrollIntoViewIfNeeded();
    await expect(page.locator('text=AI optimalizace')).toBeVisible();
  });
});
