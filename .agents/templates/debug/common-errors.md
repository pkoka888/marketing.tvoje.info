# Debug Templates

Common error scenarios and their automated fixes.

## Heap Memory Overflow

**Scenario**: Node.js heap out of memory during build

**Symptoms**:

- `FATAL ERROR: Reached heap limit Allocation failed`
- Build fails on large projects

**Auto-Fix**:

```bash
# Increase Node memory
NODE_OPTIONS="--max-old-space-size=4096" npm run build

# Or add to package.json
{
  "scripts": {
    "build": "NODE_OPTIONS='--max-old-space-size=4096' astro build"
  }
}
```

**Prevention**:

- Split large components
- Use lazy loading
- Optimize images before build

---

## ESLint/Prettier Conflicts

**Scenario**: Prettier and ESLint fighting over formatting

**Symptoms**:

- ESLint errors about formatting
- Infinite loop of fixes

**Auto-Fix**:

```bash
# Install prettier with eslint
npm install --save-dev prettier eslint-config-prettier

# .eslintrc.json
{
  "extends": ["prettier"]
}
```

---

## TypeScript Errors Blocking Build

**Scenario**: Type errors in production build

**Auto-Fix**:

```bash
# Check type errors without building
npm run typecheck

# Skip type check (temporary)
npm run build -- --skip-ts-check

# Fix common issues
npx tsc --noEmit --skipLibCheck
```

---

## Astro Island Hydration Errors

**Scenario**: Client directives not working

**Symptoms**:

- Components not interactive
- Hydration warnings in console

**Auto-Fix**:

```astro
---
// Correct usage
import InteractiveComponent from './InteractiveComponent.jsx';
---

<!-- Correct client directives -->
<InteractiveComponent client:load />
<InteractiveComponent client:visible />
<InteractiveComponent client:idle />
```

---

## Tailwind CSS Not Updating

**Scenario**: Styles not reflecting changes

**Auto-Fix**:

```bash
# Clear cache
rm -rf node_modules/.cache
rm -rf .astro

# Rebuild
npm run build
```

**Prevention**:

- Add to build script: `"build": "astro build && npx tailwindcss -m ./dist"`
- Use `content` in tailwind.config.js

---

## Vercel Deployment Failures

**Scenario**: Build works locally but fails on Vercel

**Auto-Fix**:

```json
// vercel.json
{
  "buildCommand": "npm run build",
  "installCommand": "npm install",
  "framework": "astro"
}
```

**Common Issues**:

- Node version mismatch → set `engines` in package.json
- Missing dependencies → use `npm ci` not `npm install`
- Output directory wrong → verify `dist/` path

---

## GitHub Actions Timeout

**Scenario**: CI takes too long or times out

**Auto-Fix**:

```yaml
jobs:
  build:
    timeout-minutes: 30 # Increase timeout
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Shallow clone for speed
```

---

## Image Optimization Failures

**Scenario**: Images not loading or too large

**Auto-Fix**:

```astro
---
import { Image } from 'astro:assets';
import myImage from '../assets/image.png';
---

<Image src={myImage} alt="Description" />
```

---

## Formspree Submission Errors

**Scenario**: Contact form not submitting

**Debug**:

1. Check formspree.io form status
2. Verify endpoint URL
3. Check network tab for CORS errors

**Auto-Fix**:

```astro
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <input type="email" name="email" required />
  <button type="submit">Send</button>
</form>
```

---

## Missing Environment Variables

**Scenario**: Build fails due to missing .env

**Auto-Fix**:

# Create .env.example

```
# Copy from .env (never commit actual values)
cp .env .env.example
```

# In code, provide defaults:

const apiKey = import.meta.env.PUBLIC_API_KEY || 'fallback-key';

```

```
