---
description: Build the Astro site for production and preview
---

## Steps

1. Install dependencies:
```bash
npm install
```

2. Run production build:
```bash
npm run build
```

3. Preview the production build locally:
```bash
npm run preview
```

4. The preview server will be available at `http://localhost:4321`

## Output
- Build output goes to `dist/`
- Check for any TypeScript or Astro build errors in the output

## Validation
- Verify bundle size is under 50KB gzipped
- Check `dist/` contains all expected HTML pages (en and cs locales)
