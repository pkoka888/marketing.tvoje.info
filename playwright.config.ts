import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for E2E testing
 * Enhanced with Chromium debugging and visual verification
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html', { outputFolder: 'playwright-report' }], ['list']],
  use: {
    baseURL: 'http://localhost:4321',
    trace: 'on-first-retry',
    video: 'on-first-retry',
    screenshot: 'only-on-failure',

    // Browser context options for visual verification
    contextOptions: {
      viewport: { width: 1280, height: 720 },
      deviceScaleFactor: 1,
    },
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
    {
      name: 'chromium-mobile',
      use: {
        ...devices['Pixel 5'],
      },
    },
    {
      name: 'chromium-debug',
      use: {
        ...devices['Desktop Chrome'],
        launchOptions: {
          headless: false,
        },
      },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:4321',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },

  // Timeout configurations
  timeout: 30000,
  expect: {
    timeout: 5000,
  },

  // Output directories
  outputDir: 'playwright-output',
});
