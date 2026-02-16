import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['tests/**/*.{test,spec}.{ts,js,astro}'],
    exclude: ['tests/e2e/**', 'tests/integration/**', 'node_modules/**', 'dist/**'],
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      include: ['src/**/*.{ts,astro}'],
      exclude: [
        'src/**/*.d.ts',
        'src/**/*.astro',
        'src/content/**',
        'src/pages/**',
        'src/layouts/**',
        'src/styles/**',
        'src/i18n/**',
        '.kilocode/**',
        'tests/**',
        'dist/**',
        'node_modules/**',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
    setupFiles: ['tests/setup.ts'],
    reporters: ['default', 'hanging-process'],
    testTimeout: 10000,
  },
});
