import { type Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class PricingPage extends BasePage {
  readonly pageTitle: Locator;
  readonly pricingCards: Locator;
  readonly starterCard: Locator;
  readonly growthCard: Locator;
  readonly premiumCard: Locator;
  readonly faqSection: Locator;
  readonly faqItems: Locator;

  constructor(page: import('@playwright/test').Page) {
    super(page);
    this.pageTitle = page.locator('h1, h2').first();
    this.pricingCards = page.locator('.pricing-card, [class*="pricing"]');
    this.starterCard = page.locator('text=START, text=Starter').first();
    this.growthCard = page.locator('text=ROZVOJ, text=Growth').first();
    this.premiumCard = page.locator('text=PREMIUM, text=Premium').first();
    this.faqSection = page.locator('section, div').filter({ hasText: /FAQ|Časté dotazy/ });
    this.faqItems = this.faqSection.locator('.faq-item, [class*="faq"]');
  }

  async goto(): Promise<void> {
    await super.goto('/pricing');
    await super.waitForLoad();
  }

  async gotoCs(): Promise<void> {
    await super.goto('/cs/pricing');
    await super.waitForLoad();
  }

  async getPricingCount(): Promise<number> {
    return this.pricingCards.count();
  }

  async clickFaqItem(index: number): Promise<void> {
    await this.faqItems.nth(index).locator('button').click();
  }
}
