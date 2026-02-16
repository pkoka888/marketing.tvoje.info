/**
 * Vitest setup file for Astro testing
 *
 * This file is executed before each test file.
 * Configure global test utilities and environment setup here.
 */

// Set test environment
process.env.NODE_ENV = 'test';

// Global test timeout
const TEST_TIMEOUT = 10000;

// Polyfill for TextEncoder/TextDecoder if needed
if (typeof TextEncoder === 'undefined') {
  global.TextEncoder = require('util').TextEncoder;
}
if (typeof TextDecoder === 'undefined') {
  global.TextDecoder = require('util').TextDecoder;
}

// Console suppression for clean test output (optional)
// Uncomment to suppress console logs during tests
// global.console = {
//   ...console,
//   log: vi.fn(),
//   debug: vi.fn(),
//   info: vi.fn(),
//   warn: vi.fn(),
// };

export { TEST_TIMEOUT };
