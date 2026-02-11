---
description: Deploy to Vercel (production builds are auto-deployed on push to main)
---

## Automated Deployment
- **Preview**: Deploys automatically on every PR to GitHub
- **Production**: Deploys automatically on push to `main` branch
- GitHub Actions workflow: `.github/workflows/deploy.yml`

## Manual Deployment Steps

1. Build the site:
```bash
npm run build
```

2. Deploy using Vercel CLI (if installed):
```bash
npx vercel --prod
```

## Pre-deployment Checklist
- [ ] All tests pass (`npm run test`)
- [ ] Build succeeds without errors (`npm run build`)
- [ ] Lighthouse scores ≥95 on preview
- [ ] Bilingual content verified (EN + CS)
- [ ] Contact form endpoint configured in `.env`
