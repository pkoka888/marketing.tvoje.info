import { test, expect } from '@playwright/test';
import { setupDebugHelpers, captureEvidence } from '../../debug/helpers';

test.describe('Debug & Visual Verification', () => {
  test('homepage debug - capture console and screenshot', async ({ page }) => {
    await setupDebugHelpers(page, {
      console: true,
      screenshots: true,
    });

    await page.goto('/');

    const title = await page.title();
    console.log(`Page title: ${title}`);

    await captureEvidence(page, 'homepage-debug', 'debug');
  });

  test('capture Czech version screenshot', async ({ page }) => {
    await page.goto('/cs');

    await captureEvidence(page, 'homepage-cs', 'visual');
  });

  test('capture mobile view screenshot', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    await captureEvidence(page, 'homepage-mobile', 'visual');
  });

  test('projects page visual check', async ({ page }) => {
    await page.goto('/projects');

    const projectCards = await page.locator('[class*="card"], [class*="project"]').count();
    console.log(`Found ${projectCards} project cards`);

    await captureEvidence(page, 'projects-page', 'visual');
  });

  test('services page visual check', async ({ page }) => {
    await page.goto('/services');

    await captureEvidence(page, 'services-page', 'visual');
  });

  test('capture all pages sequentially', async ({ page }) => {
    const pages = ['/', '/cs', '/projects', '/services', '/cs/projects', '/cs/services'];

    for (const url of pages) {
      await page.goto(url);
      const safeName = url.replace(/[\/]/g, '-').replace(/^-/, '');
      await captureEvidence(page, safeName, 'full-site-audit');
    }
  });
});
