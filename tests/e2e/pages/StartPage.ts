import { type Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class StartPage extends BasePage {
  readonly form: Locator;
  readonly projectTypeSelect: Locator;
  readonly budgetSelect: Locator;
  readonly timelineSelect: Locator;
  readonly companySizeSelect: Locator;
  readonly nameInput: Locator;
  readonly emailInput: Locator;
  readonly companyInput: Locator;
  readonly messageInput: Locator;
  readonly gdprCheckbox: Locator;
  readonly submitButton: Locator;

  constructor(page: import('@playwright/test').Page) {
    super(page);
    this.form = page.locator('form');
    this.projectTypeSelect = page.locator('#project-type');
    this.budgetSelect = page.locator('#budget');
    this.timelineSelect = page.locator('#timeline');
    this.companySizeSelect = page.locator('#company-size');
    this.nameInput = page.locator('#name');
    this.emailInput = page.locator('#email');
    this.companyInput = page.locator('#company');
    this.messageInput = page.locator('#message');
    this.gdprCheckbox = page.locator('#gdpr');
    this.submitButton = this.form.locator('button[type="submit"]');
  }

  async goto(): Promise<void> {
    await super.goto('/start');
    await super.waitForLoad();
  }

  async gotoCs(): Promise<void> {
    await super.goto('/cs/start');
    await super.waitForLoad();
  }

  async fillForm(data: {
    projectType?: string;
    budget?: string;
    timeline?: string;
    name?: string;
    email?: string;
    company?: string;
  }): Promise<void> {
    if (data.projectType) await this.projectTypeSelect.selectOption(data.projectType);
    if (data.budget) await this.budgetSelect.selectOption(data.budget);
    if (data.timeline) await this.timelineSelect.selectOption(data.timeline);
    if (data.name) await this.nameInput.fill(data.name);
    if (data.email) await this.emailInput.fill(data.email);
    if (data.company) await this.companyInput.fill(data.company);
  }

  async submitForm(): Promise<void> {
    await this.gdprCheckbox.check();
    await this.submitButton.click();
  }
}
