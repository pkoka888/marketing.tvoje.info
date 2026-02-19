import { test, expect } from '@playwright/test';

const PRODUCTION_URL = 'https://marketing.tvoje.info';

test.describe('Production Verification - New Sections', () => {
  test('ClientLogos section - Trusted By', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    const trustedBy = page.locator('text=Trusted By');
    await expect(trustedBy).toBeVisible();

    const clientLogos = page.locator('section').filter({ has: trustedBy });
    await expect(clientLogos).toBeVisible();
  });

  test('Featured Projects section', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    const projects = page.locator('text=Featured Projects');
    await expect(projects).toBeVisible();
  });

  test('How We Work - Process section', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    const process = page.locator('text=How We Work');
    await expect(process).toBeVisible();
  });

  test('Certifications section', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    // Use more specific locator - target the section heading, not the subsection
    const certifications = page.locator('#certifications h2:has-text("Certifications")');
    await expect(certifications).toBeVisible();
  });

  test('Contact form exists', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    const form = page.locator('#contact-form');
    await expect(form).toBeVisible();

    const nameInput = form.locator('input[name="name"]');
    const emailInput = form.locator('input[name="email"]');
    const messageInput = form.locator('textarea[name="message"]');

    await expect(nameInput).toBeVisible();
    await expect(emailInput).toBeVisible();
    await expect(messageInput).toBeVisible();
  });

  test('Language toggle works (EN -> CS)', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    const csLink = page.locator('a[href="/cs"]').first();
    if (await csLink.isVisible()) {
      await csLink.click();
      await page.waitForURL(/\/cs\//);
      await expect(page.locator('body')).toContainText('Marketing');
    }
  });

  test('Navigation links work', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    const projectsLink = page.locator('nav a[href*="projects"]').first();
    if (await projectsLink.isVisible()) {
      await projectsLink.click();
      await page.waitForLoadState('networkidle');
      const url = page.url();
      expect(url).toContain('projects');
    }
  });
});
