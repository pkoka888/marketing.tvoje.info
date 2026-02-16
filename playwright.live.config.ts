import { defineConfig, devices } from '@playwright/test';
import baseConfig from './playwright.config';

export default defineConfig({
  ...baseConfig,
  use: {
    ...baseConfig.use,
    baseURL: 'https://portfolio.tvoje.info',
  },
  // Disable webserver for live tests
  webServer: undefined,
});
