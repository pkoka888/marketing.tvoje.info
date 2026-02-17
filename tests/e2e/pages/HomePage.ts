import { type Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
  readonly heroTitle: Locator;
  readonly heroSubtitle: Locator;
  readonly ctaPrimary: Locator;
  readonly ctaSecondary: Locator;
  readonly navLinks: Locator;
  readonly languageSwitcher: Locator;
  readonly themeSelector: Locator;
  readonly sections: Locator;

  constructor(page: import('@playwright/test').Page) {
    super(page);
    this.heroTitle = page.locator('h1');
    this.heroSubtitle = page.locator('section#hero p');
    this.ctaPrimary = page
      .locator('a:has-text("View Projects"), a:has-text("Zobrazit projekty")')
      .first();
    this.ctaSecondary = page.locator('a:has-text("Contact"), a:has-text("Kontaktovat")').first();
    this.navLinks = page.locator('header nav a');
    this.languageSwitcher = page.locator('header a:has-text("EN"), header a:has-text("CS")');
    this.themeSelector = page.locator('#theme-selector-wrapper');
    this.sections = page.locator('section[id]');
  }

  async goto(): Promise<void> {
    await super.goto('/');
    await super.waitForLoad();
  }

  async getHeroText(): Promise<string> {
    return (await this.heroTitle.textContent()) || '';
  }

  async clickPrimaryCTA(): Promise<void> {
    await this.ctaPrimary.click();
  }

  async switchLanguage(): Promise<void> {
    await this.languageSwitcher.click();
  }

  async getSections(): Promise<string[]> {
    return this.sections.allInnerTexts();
  }
}
