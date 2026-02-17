import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for E2E testing
 * Enhanced with parallel execution, sharding, and visual regression
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,

  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['list'],
    ['json', { outputFile: 'playwright-report/test-results.json' }],
  ],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:4321',
    trace: 'on-first-retry',
    video: 'on-first-retry',
    screenshot: 'only-on-failure',

    // Browser context options
    contextOptions: {
      viewport: { width: 1280, height: 720 },
      deviceScaleFactor: 1,
    },

    // Accessibility settings
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  projects: [
    // Desktop browsers
    {
      name: 'chromium-desktop',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 },
      },
    },
    {
      name: 'firefox-desktop',
      use: {
        ...devices['Desktop Firefox'],
        viewport: { width: 1920, height: 1080 },
      },
    },
    {
      name: 'webkit-desktop',
      use: {
        ...devices['Desktop Safari'],
        viewport: { width: 1920, height: 1080 },
      },
    },

    // Mobile browsers
    {
      name: 'chromium-mobile',
      use: {
        ...devices['Pixel 5'],
      },
    },
    {
      name: 'iphone-12',
      use: {
        ...devices['iPhone 12'],
      },
    },

    // Tablet
    {
      name: 'ipad-pro',
      use: {
        ...devices['iPad Pro 11'],
      },
    },
  ],

  webServer: process.env.BASE_URL ? undefined : {
    command: 'npm run preview',
    url: 'http://localhost:4321',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },

  // Timeout configurations
  timeout: 30000,
  expect: {
    timeout: 10000,
  },

  // Output directories
  outputDir: 'test-results',

  // Sharding
  shard: process.env.SHARD
    ? {
        current: parseInt(process.env.SHARD.split('/')[0]),
        total: parseInt(process.env.SHARD.split('/')[1]),
      }
    : undefined,
});
