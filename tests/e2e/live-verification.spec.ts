import { expect, test } from '@playwright/test';

test.describe('Live Production Verification', () => {
  const LIVE_URL = process.env.BASE_URL || 'https://marketing.tvoje.info';

  test('Should have correct marketing title and meta description', async ({ page }) => {
    await page.goto(LIVE_URL);
    await expect(page).toHaveTitle(/Pavel Kašpar - Marketing/);

    const metaDescription = await page.locator('meta[name="description"]').getAttribute('content');
    expect(metaDescription).toContain('Marketing');
    expect(metaDescription).not.toContain('DevOps');
  });

  test('Should display marketing skills in About section', async ({ page }) => {
    await page.goto(`${LIVE_URL}/#about`);
    const aboutContent = await page.textContent('#about');
    expect(aboutContent).toContain('SEO');
    expect(aboutContent).toContain('PPC');
    expect(aboutContent).toContain('Analytics');
    expect(aboutContent).not.toContain('Docker');
    expect(aboutContent).not.toContain('Kubernetes');
  });

  test.skip('Should load theme-specific photos', async ({ page }) => {
    await page.goto(LIVE_URL);

    // Check for one of the theme photos
    const titanPhoto = page.locator('img[src*="photo_titan.jpg"]');
    // Note: It might be hidden or conditional, but should exist in the DOM
    await expect(titanPhoto).toBeAttached();
  });

  test('Should have working language toggle', async ({ page }) => {
    await page.goto(LIVE_URL);

    // Toggle to Czech
    const csLink = page.locator('a[href="/cs/"]');
    if (await csLink.isVisible()) {
      await csLink.click();
      await expect(page).toHaveURL(/.*\/cs\//);
      await expect(page.locator('h1')).toContainText(/Marketing/);
    }
  });
});
