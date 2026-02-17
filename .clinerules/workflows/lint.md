---
description: Run linting and formatting checks
---
// turbo-all

## Steps

1. Run ESLint:
```bash
npx eslint src/ --config eslint.config.mjs
```

2. Check formatting:
```bash
npm run format:check
```

3. Auto-fix formatting issues:
```bash
npm run format
```

## Notes
- ESLint config: `eslint.config.mjs` (flat config format)
- Prettier config: `.prettierrc`
- Prettier has Astro plugin for `.astro` file support
