import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    files: ['src/**/*.{ts,js}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'warn',
    },
  },
  {
    ignores: ['dist/', 'node_modules/', '.astro/', 'bak/'],
  },
];
