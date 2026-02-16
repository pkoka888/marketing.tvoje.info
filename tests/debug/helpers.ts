import { test as base, Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const EVIDENCE_DIR = process.env.EVIDENCE_DIR || 'evidence';

export interface DebugOptions {
  console?: boolean;
  network?: boolean;
  screenshots?: boolean;
}

export async function setupDebugHelpers(page: Page, options: DebugOptions = {}): Promise<void> {
  const consoleCapture = options.console ?? true;
  const networkCapture = options.network ?? false;
  const autoScreenshot = options.screenshots ?? false;

  if (consoleCapture) {
    page.on('console', (msg) => {
      const msgType = msg.type();
      const text = msg.text();
      console.log(`[Browser Console ${msgType}]: ${text}`);
    });
  }

  if (networkCapture) {
    page.on('request', (request) => {
      console.log(`[Network Request]: ${request.method()} ${request.url()}`);
    });
    page.on('response', (response) => {
      console.log(`[Network Response]: ${response.status()} ${response.url()}`);
    });
  }

  if (autoScreenshot) {
    page.on('pageerror', async (error) => {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filename = `error-${timestamp}.png`;
      await page.screenshot({ path: path.join(EVIDENCE_DIR, 'debug-screenshots', filename) });
      console.log(`[Screenshot captured on error]: ${filename}`);
    });
  }
}

export async function captureEvidence(page: Page, name: string, subdir = ''): Promise<string> {
  const dir = subdir ? path.join(EVIDENCE_DIR, subdir) : EVIDENCE_DIR;

  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const filename = `${name}-${Date.now()}.png`;
  const filepath = path.join(dir, filename);

  await page.screenshot({ path: filepath, fullPage: true });
  console.log(`[Evidence captured]: ${filepath}`);

  return filepath;
}

export async function getConsoleLogs(): Promise<string[]> {
  const logs: string[] = [];
  return logs;
}

export async function evaluateWithResult<T>(page: Page, fn: () => T | Promise<T>): Promise<T> {
  const result = await page.evaluate(fn);
  console.log(`[Evaluate result]: ${JSON.stringify(result, null, 2)}`);
  return result;
}

export function createDebugTest() {
  return base.extend<{
    debugPage: Page;
    captureEvidence: (name: string, subdir?: string) => Promise<string>;
  }>({
    debugPage: async ({ page }, use) => {
      await setupDebugHelpers(page, { console: true, screenshots: true });
      await use(page);
    },
    captureEvidence: async ({ page }, use) => {
      await use(async (name: string, subdir = '') => captureEvidence(page, name, subdir));
    },
  });
}

export { EVIDENCE_DIR };
