import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/HomePage';
import { PricingPage } from '../pages/PricingPage';
import { StartPage } from '../pages/StartPage';

test.describe('Navigation Tests', () => {
  let homePage: HomePage;
  let pricingPage: PricingPage;
  let startPage: StartPage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
    pricingPage = new PricingPage(page);
    startPage = new StartPage(page);
  });

  test('Homepage loads correctly', async ({ page }) => {
    await homePage.goto();
    await expect(page).toHaveURL(/\//);
    await expect(homePage.heroTitle).toBeVisible();
  });

  test('Navigation links work', async ({ page }) => {
    await homePage.goto();

    // Click projects link
    await page.click('a[href="/projects"]');
    await expect(page).toHaveURL(/projects/);

    // Click services link
    await page.click('a[href="/services"]');
    await expect(page).toHaveURL(/services/);
  });

  test('Language switch works', async ({ page }) => {
    await homePage.goto();

    // Switch to Czech
    const langSwitcher = page.locator('header a:has-text("EN"), header a:has-text("CS")');
    await langSwitcher.click();

    // Should be on Czech version
    await expect(page).toHaveURL(/\/cs/);
  });

  test('Pricing page loads', async ({ page }) => {
    await pricingPage.goto();
    await expect(pricingPage.pricingCards.first()).toBeVisible();
  });

  test('Start page loads with form', async ({ page }) => {
    await startPage.goto();
    await expect(startPage.form).toBeVisible();
    await expect(startPage.projectTypeSelect).toBeVisible();
  });
});

test.describe('Form Tests', () => {
  test('Start form validation', async ({ page }) => {
    const startPage = new StartPage(page);
    await startPage.goto();

    // Try to submit empty form
    await startPage.submitButton.click();

    // Should show validation errors
    const nameInput = page.locator('#name');
    await expect(nameInput).toHaveAttribute('required', '');
  });

  test('Form accepts valid input', async ({ page }) => {
    const startPage = new StartPage(page);
    await startPage.goto();

    await startPage.fillForm({
      projectType: 'seo',
      budget: '10-25k',
      name: 'Test User',
      email: 'test@example.com',
    });

    await expect(startPage.projectTypeSelect).toHaveValue('seo');
    await expect(startPage.nameInput).toHaveValue('Test User');
  });
});

test.describe('Theme Tests', () => {
  test('Theme selector exists', async ({ page }) => {
    await page.goto('/');
    const themeSelector = page.locator('#theme-selector-wrapper');
    await expect(themeSelector).toBeVisible();
  });

  test('Theme switching works', async ({ page }) => {
    await page.goto('/');

    // Open theme dropdown
    await page.click('#theme-selector-trigger');

    // Select a theme
    await page.click('[data-theme="nova"]');

    // Verify theme changed
    const themeName = page.locator('#theme-current-name');
    await expect(themeName).toHaveText('Nova');
  });
});

test.describe('Localization Tests', () => {
  test('English version', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1')).toContainText('Marketing');
  });

  test('Czech version', async ({ page }) => {
    await page.goto('/cs/');
    await expect(page.locator('h1')).toContainText('Marketing');
  });
});
