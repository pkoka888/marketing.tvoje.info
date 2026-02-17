# Marketing Portfolio - Comprehensive Verification Plan

**Last Updated:** 2026-02-16
**Status:** READY FOR EXECUTION
**Orchestrator:** Antigravity (Gemini 3 Pro)

---

## Overview

This plan orchestrates subagents to verify the marketing portfolio is fully functional, deployed, and ready for production use.

### Provider Strategy

| Task Type            | Primary Provider               | Fallback             | Notes              |
| -------------------- | ------------------------------ | -------------------- | ------------------ |
| Complex verification | Groq (llama-3.3-70b-versatile) | LiteLLM (if running) | Free, fast         |
| Simple checks        | Kilo Code                      | OpenRouter           | Free tier          |
| Visual verification  | Playwright                     | Manual               | Browser automation |
| Build verification   | npm (local)                    | GitHub Actions       | Static site        |

---

## Verification Checklist

### Phase 1: Build & Code Quality

| #   | Check                        | Agent | Provider | Status |
| --- | ---------------------------- | ----- | -------- | ------ |
| 1.1 | `npm run build` passes       | Cline | npm      | ⏳     |
| 1.2 | `npm run lint` passes        | Cline | npm      | ⏳     |
| 1.3 | No TypeScript errors         | Cline | npm      | ⏳     |
| 1.4 | All pages generated in dist/ | Cline | npm      | ⏳     |

### Phase 2: Content & SEO

| #   | Check                                | Agent     | Provider | Status |
| --- | ------------------------------------ | --------- | -------- | ------ |
| 2.1 | Homepage title = "Pavel Kašpar"      | Kilo Code | Direct   | ⏳     |
| 2.2 | About section has marketing skills   | Kilo Code | Direct   | ⏳     |
| 2.3 | Services page has marketing content  | Kilo Code | Direct   | ⏳     |
| 2.4 | No "DevOps" references in built HTML | Kilo Code | Direct   | ⏳     |
| 2.5 | Bilingual support (EN + CS) works    | Kilo Code | Direct   | ⏳     |

### Phase 3: Theme System

| #   | Check                          | Agent      | Provider | Status |
| --- | ------------------------------ | ---------- | -------- | ------ |
| 3.1 | All 5 theme photos exist       | Kilo Code  | npm      | ⏳     |
| 3.2 | Theme switcher renders         | Kilo Code  | npm      | ⏳     |
| 3.3 | Theme CSS variables defined    | Kilo Code  | npm      | ⏳     |
| 3.4 | TITAN theme displays correctly | Playwright | Browser  | ⏳     |

### Phase 4: Deployment

| #   | Check                        | Agent          | Provider | Status |
| --- | ---------------------------- | -------------- | -------- | ------ |
| 4.1 | Push to main triggers deploy | GitHub Actions | CI/CD    | ⏳     |
| 4.2 | Deploy to VPS succeeds       | GitHub Actions | CI/CD    | ⏳     |
| 4.3 | Live site accessible         | Kilo Code      | curl     | ⏳     |
| 4.4 | Nginx serves static files    | Kilo Code      | curl     | ⏳     |

### Phase 5: LiteLLM/Groq Verification (Optional)

| #   | Check                               | Agent | Provider   | Status |
| --- | ----------------------------------- | ----- | ---------- | ------ |
| 5.1 | GROQ_API_KEY is valid               | Groq  | Direct API | ⏳     |
| 5.2 | LiteLLM proxy (port 4000) responds  | Groq  | Local      | ⏳     |
| 5.3 | Model llama-3.3-70b-versatile works | Groq  | Direct API | ⏳     |
| 5.4 | Provider fallback works             | Groq  | Direct API | ⏳     |

---

## Subagent Assignments

### Agent 1: Build Validator (Cline)

**Purpose:** Verify build and code quality\*\*
**Provider:** npm (local)
**Commands:**

```bash
npm run build
npm run lint
npm run typecheck
```

### Agent 2: Content Checker (Kilo Code)

**Purpose:** Verify marketing content and SEO
**Provider:** Direct (npm/curl)
**Tasks:**

1. Check built HTML for "Pavel Kašpar"
2. Verify no "DevOps" references remain
3. Test /cs/ route returns Czech content

### Agent 3: Theme Tester (Playwright)

**Purpose:** Visual verification of theme system
**Provider:** Browser automation
**Tasks:**

1. Launch browser
2. Navigate to localhost:4321
3. Click each theme button
4. Screenshot each theme
5. Verify no console errors

### Agent 4: Deployment Monitor (GitHub Actions)

**Purpose:** Verify deployment pipeline
**Provider:** CI/CD
**Trigger:** Push to main
**Monitor:** Check Actions tab for success

### Agent 5: Groq Verifier (Groq)

**Purpose:** Verify LiteLLM/Groq functionality
**Provider:** Direct API
**Commands:**

```bash
curl -s -H "Authorization: Bearer $GROQ_API_KEY" \
  https://api.groq.com/openai/v1/models
```

---

## Execution Order

```
Phase 1 (Build) → Phase 2 (Content) → Phase 3 (Themes)
                                                    ↓
                              Phase 5 (Groq) ← Phase 4 (Deploy)
```

**Parallel Execution:**

- Phase 1 and Phase 2 can run in parallel
- Phase 3 depends on Phase 1 (build)
- Phase 4 depends on Phase 1-3 (must pass first)
- Phase 5 is independent (optional)

---

## Success Criteria

| Metric                | Target           |
| --------------------- | ---------------- |
| Build passes          | 100%             |
| No lint errors        | 0                |
| No "DevOps" in output | Yes              |
| Live site responds    | Yes              |
| All 5 themes work     | Yes              |
| Groq API works        | Yes (if checked) |

---

## If Issues Found

### Build Fails

- Check Node.js version (need 20+)
- Run `npm install` fresh
- Check for TypeScript errors

### Content Issues

- Edit `src/pages/index.astro`
- Edit `src/i18n/translations.ts`
- Rebuild and verify

### Theme Issues

- Check `src/styles/themes.css`
- Check `src/components/common/ThemeSwitcher.astro`
- Check images in `public/images/theme/`

### Deployment Fails

- Check GitHub secrets are set
- Check VPS credentials
- Check Nginx is running on server62

### Groq Issues

- Verify GROQ_API_KEY in GitHub secrets
- Check rate limits at console.groq.com
- Use fallback to Kilo Code/OpenRouter

---

## Manual Verification Steps

If agents fail, verify manually:

```bash
# 1. Build
cd /c/Users/pavel/projects/marketing.tvoje.info
npm run build

# 2. Check for DevOps in output
grep -r "DevOps" dist/ || echo "Clean!"

# 3. Check theme photos
ls -la public/images/theme/photo_*.webp

# 4. Preview locally
npm run preview

# 5. Test Groq
curl -H "Authorization: Bearer $GROQ_API_KEY" \
  https://api.groq.com/openai/v1/models
```

---

## Next Steps After Verification

1. ✅ If all pass: Deploy to production
2. 🔧 If issues: Fix and re-run verification
3. 📊 If partial: Prioritize critical issues, defer non-critical
4. 🚀 Ready: Share link with potential clients
