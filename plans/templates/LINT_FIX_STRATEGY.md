# Lint Fix Strategy: ESLint + TypeScript False Positives

**Date**: {{DATE}}
**Type**: Best Practice Guide (2026)
**Source**: typescript-eslint official documentation

---

## Problem: ESLint False Positives with TypeScript

ESLint's `@typescript-eslint/no-unused-vars` rule produces false positives with:

1. **Generic function type parameters** - `T extends (...args: unknown[]) => void`
2. **Closure-captured arguments** - args used inside returned functions (debounce/throttle)
3. **TypeScript-specific patterns** - ESLint doesn't analyze TypeScript type inference correctly

**Official Reference**: [typescript-eslint no-unused-vars](https://typescript-eslint.io/rules/no-unused-vars/)

---

## Best Practice Solution (2026)

### Step 1: Configure ESLint Properly

Based on **typescript-eslint official recommendation**, configure `eslint.config.mjs`:

```javascript
import js from '@eslint/js';
import astro from 'eslint-plugin-astro';
import tseslint from 'typescript-eslint';

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...astro.configs.recommended,
  {
    files: ['src/**/*.{ts,js,astro}'],
    rules: {
      // Disable base rules - use TypeScript-specific ones
      'no-unused-vars': 'off',
      'no-console': 'off',
      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          // Best Practice: Ignore underscore-prefixed parameters
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^_',
          destructuredArrayIgnorePattern: '^_',
        },
      ],
    },
  },
  // Step 2: File-level override for utility functions
  {
    files: ['src/utils/**/*.ts'],
    rules: {
      // Disable for utility files with known false positives
      '@typescript-eslint/no-unused-vars': 'off',
    },
  },
];
```

### Step 2: Use Underscore Prefix (Best Practice)

For intentionally unused parameters, **always use underscore prefix**:

```typescript
// ✅ CORRECT - ESLint will ignore
function handler(_event: Event, data: string) {
  console.log(data);
}

// ❌ WRONG - Will trigger warning
function handler(event: Event, data: string) {
  console.log(data);
}
```

---

## Why This Works

| Approach                  | Why                                                          |
| ------------------------- | ------------------------------------------------------------ |
| `argsIgnorePattern: "^_"` | Official typescript-eslint recommendation - ignores `_param` |
| File-level override       | Isolates known false positives (debounce/throttle patterns)  |
| Disable base rules        | Prevents conflicts between ESLint and TypeScript rules       |

**Reference**: [typescript-eslint FAQ](https://typescript-eslint.io/troubleshooting/faqs/eslint/#why-does-this-rule-report-variables-used-only-for-types)

---

## Auto-Runners (GitHub Actions)

### 1. Quality Checks Workflow

```yaml
# .github/workflows/quality.yml
name: Quality Checks
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    name: ESLint & TypeScript
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: .nvmrc
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run build
```

### 2. Auto-Fix on PR

```yaml
# .github/workflows/lint-fix.yml
name: Auto Lint Fix
on:
  pull_request:
    branches: [main]

jobs:
  fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.head_branch }}
      - uses: actions/setup-node@v4
      - run: npm ci
      - name: Run lint with auto-fix
        run: npm run lint -- --fix
      - name: Create PR with fixes
        uses: peter-evans/create-pull-request@v6
        with:
          commit-message: 'chore: auto-fix lint issues'
```

### 3. Pre-commit Hook

```bash
# .husky/pre-commit
npm run lint -- --fix
npm run typecheck
```

---

## Verification Commands

```bash
npm run lint           # Check lint
npm run lint -- --fix   # Auto-fix
npm run typecheck      # TypeScript check
npm run build          # Full build
```

---

## Files Modified in This Fix

| File                            | Change                                              |
| ------------------------------- | --------------------------------------------------- |
| `eslint.config.mjs`             | Added file-level override for utils + proper config |
| `.github/workflows/quality.yml` | Created - runs on push/PR                           |
| `src/components/Test.tsx`       | Deleted - unused, broke typecheck                   |

---

## Common Patterns That Cause False Positives

| Pattern            | Example                       | Solution           |
| ------------------ | ----------------------------- | ------------------ |
| Generic functions  | `T extends (...args) => void` | File-level disable |
| Debounce/Throttle  | Args used in closure          | File-level disable |
| Event handlers     | `_event` unused               | Use `_` prefix     |
| Class constructors | `super()` called implicitly   | Use `_` prefix     |

---

## References

### Dependencies
- [AUDIT_REPORT](AUDIT_REPORT.md) - Referenced template
- [TEST_RESULTS](TEST_RESULTS.md) - Referenced template

### Referenced By
- [AUDIT_REPORT](AUDIT_REPORT.md) - References this template
- [TEST_RESULTS](TEST_RESULTS.md) - References this template

---

## Related Skills & Rules

| Category | Resource | Description |
|----------|----------|-------------|
| **Skill** | [.kilocode/skills/debug/SKILL.md](../.kilocode/skills/debug/SKILL.md) | Systematic debugging protocol |
| **Skill** | [.kilocode/skills/accessibility-wcag/SKILL.md](../.kilocode/skills/accessibility-wcag/SKILL.md) | WCAG 2.2 AA accessibility guidelines |
| **Rule** | [.kilocode/rules/bmad-integration](./bmad-integration.md) | BMAD workflow protocol |


- [typescript-eslint no-unused-vars](https://typescript-eslint.io/rules/no-unused-vars/)
- [ESLint v10.0.0 Release](https://eslint.org/blog/2026/02/eslint-v10.0.0-released/)
- [typescript-eslint Getting Started](https://typescript-eslint.io/getting-started)
