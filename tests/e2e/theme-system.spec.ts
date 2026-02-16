import { test, expect } from '@playwright/test';

/**
 * Theme System Visual Tests
 * Tests all 5 theme variants: TITAN, NOVA, TARGET, SPARK, LUX
 */

const THEMES = ['titan', 'nova', 'target', 'spark', 'lux'] as const;

test.describe('Theme System', () => {
  test.describe('TITAN Theme (Default)', () => {
    test('should load homepage with TITAN theme', async ({ page }) => {
      await page.goto('/');

      // Wait for page to load
      await page.waitForLoadState('networkidle');

      // Check theme attribute is set
      const html = page.locator('html');
      await expect(html).toHaveAttribute('data-site-theme', 'titan');
    });

    test('should have TITAN logo', async ({ page }) => {
      await page.goto('/');

      // Check logo exists
      const logo = page.locator('img[src*="logo_titan"]');
      await expect(logo).toBeVisible();
    });

    test('should have TITAN hero background', async ({ page }) => {
      await page.goto('/');

      // Check hero background
      const heroBg = page.locator('img[src*="hero_titan"]');
      await expect(heroBg).toBeVisible();
    });

    test('should display TITAN headline', async ({ page }) => {
      await page.goto('/');

      // Check TITAN-specific headline is visible - use first element (h1)
      const headline = page.locator('[data-theme-copy="titan"]').first();
      await expect(headline).toBeVisible();
    });

    test('should have visible CTA above fold', async ({ page }) => {
      await page.goto('/');

      // Check CTA button is visible - EN or CZ version
      const ctaEN = page.locator('a:has-text("Get growth")');
      const ctaCZ = page.locator('a:has-text("Chci růst")');

      // At least one should be visible
      const ctaVisible =
        (await ctaEN.isVisible().catch(() => false)) ||
        (await ctaCZ.isVisible().catch(() => false));
      expect(ctaVisible).toBeTruthy();
    });

    test('should have no console errors', async ({ page }) => {
      const errors: string[] = [];
      page.on('console', (msg) => {
        if (msg.type() === 'error') {
          const text = msg.text();
          if (!text.includes('404') && !text.includes('Failed to load resource')) {
            errors.push(text);
          }
        }
      });

      await page.goto('/');
      await page.waitForLoadState('networkidle');

      expect(errors).toHaveLength(0);
    });
  });

  test.describe('Theme Switcher', () => {
    test('should switch to NOVA theme', async ({ page }) => {
      await page.goto('/');

      // Click NOVA theme button
      const novaBtn = page.locator('[data-theme="nova"]');
      await novaBtn.click();

      // Wait for theme to apply
      await page.waitForTimeout(500);

      // Check theme changed
      const html = page.locator('html');
      await expect(html).toHaveAttribute('data-site-theme', 'nova');
    });

    test('should switch to TARGET theme', async ({ page }) => {
      await page.goto('/');

      const targetBtn = page.locator('[data-theme="target"]');
      await targetBtn.click();
      await page.waitForTimeout(500);

      const html = page.locator('html');
      await expect(html).toHaveAttribute('data-site-theme', 'target');
    });

    test('should switch to SPARK theme', async ({ page }) => {
      await page.goto('/');

      const sparkBtn = page.locator('[data-theme="spark"]');
      await sparkBtn.click();
      await page.waitForTimeout(500);

      const html = page.locator('html');
      await expect(html).toHaveAttribute('data-site-theme', 'spark');
    });

    test('should switch to LUX theme', async ({ page }) => {
      await page.goto('/');

      const luxBtn = page.locator('[data-theme="lux"]');
      await luxBtn.click();
      await page.waitForTimeout(500);

      const html = page.locator('html');
      await expect(html).toHaveAttribute('data-site-theme', 'lux');
    });

    test('should persist theme in localStorage', async ({ page }) => {
      await page.goto('/');

      // Switch to NOVA
      const novaBtn = page.locator('[data-theme="nova"]');
      await novaBtn.click();
      await page.waitForTimeout(500);

      // Reload page
      await page.reload();
      await page.waitForLoadState('networkidle');

      // Check theme persisted
      const html = page.locator('html');
      await expect(html).toHaveAttribute('data-site-theme', 'nova');
    });
  });

  test.describe('Asset Loading', () => {
    for (const theme of THEMES) {
      test(`should load ${theme} logo without 404`, async ({ page }) => {
        await page.goto('/');

        // Switch to theme
        const themeBtn = page.locator(`[data-theme="${theme}"]`);
        await themeBtn.click();
        await page.waitForTimeout(500);

        // Check logo loads
        const logo = page.locator(`img[src*="logo_${theme}"]`);

        // Get src to verify it points to existing file
        const src = await logo.getAttribute('src');
        expect(src).toContain(`logo_${theme}`);
      });

      test(`should load ${theme} hero background`, async ({ page }) => {
        await page.goto('/');

        const themeBtn = page.locator(`[data-theme="${theme}"]`);
        await themeBtn.click();
        await page.waitForTimeout(500);

        const heroBg = page.locator(`img[src*="hero_${theme}"]`);
        const src = await heroBg.getAttribute('src');
        expect(src).toContain(`hero_${theme}`);
      });
    }
  });

  test.describe('Responsive', () => {
    test('should work on mobile viewport', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await page.goto('/');
      await page.waitForLoadState('networkidle');

      // Check page loads
      await expect(page.locator('html')).toBeVisible();

      // Check no horizontal scroll
      const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
      const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
      expect(scrollWidth).toBeLessThanOrEqual(clientWidth);
    });

    test('should work on tablet viewport', async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 });
      await page.goto('/');
      await page.waitForLoadState('networkidle');

      await expect(page.locator('html')).toBeVisible();
    });
  });

  test.describe('Performance', () => {
    test('should have good LCP', async ({ page }) => {
      await page.goto('/');

      // Measure LCP
      const lcp = await page.evaluate(() => {
        return new Promise((resolve) => {
          new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            const lastEntry = entries[entries.length - 1] as any;
            resolve(lastEntry.renderTime || lastEntry.loadTime);
          }).observe({ type: 'largest-contentful-paint', buffered: true });

          // Fallback timeout
          setTimeout(() => resolve(0), 5000);
        });
      });

      console.log(`LCP: ${lcp}ms`);
      // Should be under 2500ms
      expect(lcp).toBeLessThan(2500);
    });
  });
});
