# Verification & Testing Guide

## E2E Testing (Production)

We test directly against the production environment to ensure accurate verification of the deployed artifact.

**Target**: `https://marketing.tvoje.info`

### Playwright Tests

Tests are located in `tests/e2e/`.

```bash
# Run all tests
npm run test:e2e

# Run specific test
npx playwright test tests/e2e/homepage.spec.ts
```

### Critical Paths to Verify

1.  **Homepage Load**: < 200ms LCP (Lightweight, Astro-static).
2.  **Navigation**: All header links (Services, Projects, About) work.
3.  **Forms**: Contact form submission (mocked or verified via Formspree).
4.  **Visuals**: No layout shifts (CLS < 0.1).

## Platform Verification

Run the comprehensive platform integrity check before any major commit.

```bash
python scripts/verify_agentic_platform.py
```

**Checks Performed**:

- ✅ Agent Configuration (`AGENTS.md`, `opencode.json`)
- ✅ Directory Structure (`.kilocode`, `.clinerules`)
- ✅ Redis Availability (Verification Script)
- ✅ Free Model Priority Compliance

## Redis Caching Verification

Ensure your local environment allows Redis for agent context caching.

```bash
python scripts/verify_redis.py
```

- Requires: Docker running (`docker ps`) or local Redis service.
- Port: `6379` (Default) or as set in `.env` (`REDIS_URL`).
- Namespace: `marketing_tvoje_info:`
