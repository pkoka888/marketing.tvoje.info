# CI/CD Pipeline Template

## Overview

This template provides a complete CI/CD pipeline for BMAD projects using GitHub Actions + Vercel.

## Files

### 1. GitHub Actions Workflow

**File**: `.github/workflows/bmad.yml`

```yaml
name: BMAD Build & Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

env:
  NODE_VERSION: '20'

jobs:
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run format:check

  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run test -- --coverage

  build:
    name: Build Production
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 7

  deploy-preview:
    name: Deploy Preview
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prebuilt'

  deploy-production:
    name: Deploy Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prebuilt --prod'
```

### 2. Vercel Config

**File**: `vercel.json`

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "astro",
  "installCommand": "npm install",
  "devCommand": "npm run dev"
}
```

---

## Environment Variables

| Variable          | Description            | Required |
| ----------------- | ---------------------- | -------- |
| VERCEL_TOKEN      | Vercel API token       | Yes      |
| VERCEL_ORG_ID     | Vercel organization ID | Yes      |
| VERCEL_PROJECT_ID | Vercel project ID      | Yes      |

---

## Deployment Triggers

| Event           | Action            |
| --------------- | ----------------- |
| Push to main    | Production deploy |
| Push to develop | Preview deploy    |
| PR opened       | Preview deploy    |
| PR merged       | Production deploy |

---

## Rollback

```bash
# Quick rollback
vercel rollback [project] production

# Or revert and push
git revert HEAD
git push origin main
```
