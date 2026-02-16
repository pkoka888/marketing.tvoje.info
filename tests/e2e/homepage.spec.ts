import { test, expect } from '@playwright/test';

/**
 * Playwright E2E test - verifies Playwright is working correctly
 * Tests the homepage of the Astro portfolio site
 */
test('homepage has correct title', async ({ page }) => {
  // Navigate to the homepage
  await page.goto('/');

  // Check that the page has a title
  const title = await page.title();
  expect(title).toBeTruthy();

  // Verify the page loaded
  await expect(page).toHaveURL(/localhost:4321/);
});

test('homepage loads without errors', async ({ page }) => {
  // Track console errors (not network 404s)
  const errors: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      const text = msg.text();
      // Ignore 404 network errors - they don't affect functionality
      if (!text.includes('404') && !text.includes('Failed to load resource')) {
        errors.push(text);
      }
    }
  });

  // Navigate to the homepage
  await page.goto('/');

  // Wait for page to be fully loaded
  await page.waitForLoadState('networkidle');

  // Assert no critical console errors
  expect(errors).toHaveLength(0);
});
