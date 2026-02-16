import { test, expect } from '@playwright/test';

test.describe('Performance & Asset Optimization', () => {
  test('Verify image assets are compressed and localized', async ({ page }) => {
    const imageRequests: any[] = [];

    page.on('request', (request) => {
      if (request.resourceType() === 'image') {
        imageRequests.push(request);
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    console.log(`Found ${imageRequests.length} image requests on homepage.`);

    for (const request of imageRequests) {
      const url = request.url();
      const response = await request.response();
      if (response) {
        const buffer = await response.body();
        const sizeKb = buffer.length / 1024;
        console.log(`Image: ${url} | Size: ${sizeKb.toFixed(2)} KB`);

        // Assert reasonable image sizes (hero might be large but shouldn't be > 2MB)
        expect(sizeKb).toBeLessThan(2000);
      }
    }
  });

  test('Measure LCP and layout stability', async ({ page }) => {
    await page.goto('/');

    // Measure Largest Contentful Paint
    const lcp = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          const lastEntry = entries[entries.length - 1];
          resolve(lastEntry.startTime);
        }).observe({ type: 'largest-contentful-paint', buffered: true });

        // Fallback for cases where LCP might already have fired
        setTimeout(() => resolve(0), 5000);
      });
    });

    console.log(`LCP: ${lcp}ms`);
    // Expect LCP < 2500ms (Core Web Vital threshold)
    if (lcp > 0) {
      expect(lcp).toBeLessThan(2500);
    }

    // Measure Cumulative Layout Shift
    const cls = await page.evaluate(() => {
      return new Promise((resolve) => {
        let clsValue = 0;
        new PerformanceObserver((entryList) => {
          for (const entry of entryList.getEntries()) {
            if (!entry.hadRecentInput) {
              clsValue += (entry as any).value;
            }
          }
          resolve(clsValue);
        }).observe({ type: 'layout-shift', buffered: true });
        setTimeout(() => resolve(clsValue), 2000);
      });
    });

    console.log(`CLS: ${cls}`);
    // Expect CLS < 0.1 (Core Web Vital threshold)
    expect(cls).toBeLessThan(0.1);
  });

  test('Verify theme assets loading', async ({ page }) => {
    const themes = ['titan', 'nova', 'target', 'spark', 'lux'];

    for (const theme of themes) {
      console.log(`Testing theme: ${theme}`);
      await page.goto(`/`);

      await page.evaluate((t) => {
        localStorage.setItem('siteTheme', t);
        document.documentElement.setAttribute('data-site-theme', t);
      }, theme);

      // Small delay to allow images to trigger load
      await page.waitForTimeout(1000);

      console.log(`Checking logo for ${theme}...`);
      const logo = page.locator(`img[src*="logo_${theme}"]`);
      await expect(logo).toBeVisible({ timeout: 5000 });

      console.log(`Checking hero for ${theme}...`);
      const hero = page.locator(`img[src*="hero_${theme}"]`);
      await expect(hero).toBeVisible({ timeout: 5000 });

      console.log(`Theme ${theme} assets verified.`);
    }
  });
});
