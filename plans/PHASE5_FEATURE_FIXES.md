# Phase 5: Feature Fixes - Plan

**Date**: 2026-02-18
**Status**: Planning

---

## Issue Analysis

### 1. Theme Switcher - BROKEN ❌

**Root Cause:**

- `ThemeSwitcher.astro` references `window.setSiteTheme` which doesn't exist
- `Layout.astro` only defines `toggleTheme` (dark/light toggle)
- 7 themes defined in `themes.css` but no JS to apply them
- Missing: Set `data-site-theme` attribute on `<html>` element

**Files Involved:**

- `src/components/common/ThemeSwitcher.astro`
- `src/layouts/Layout.astro`
- `src/styles/themes.css`

---

### 2. Contact Form - NO DATABASE ❌

**Current State:**

- Only POSTs to Formspree (email only)
- No persistent storage
- No CRM integration

**Requirement:**

- Store submissions in database
- Keep Formspree for email notifications

**Files Involved:**

- `src/components/sections/Contact.astro`
- Need: Database + API endpoint

---

## Solution Design

### Theme Switcher Fix

```javascript
// Add to Layout.astro
function setSiteTheme(theme) {
  document.documentElement.setAttribute('data-site-theme', theme);
  localStorage.setItem('siteTheme', theme);
}
window.setSiteTheme = setSiteTheme;
```

**Stories:**

1. Add `setSiteTheme` function to Layout.astro
2. Initialize theme from localStorage on page load
3. Ensure theme persists across page navigation

### Contact Form with Database

**Architecture:**

```
Contact Form → API Endpoint → Database (SQLite/PostgreSQL)
                ↓
             Formspree (email notification)
```

**Stories:**

1. Create API endpoint `/api/contact` (Astro API route)
2. Set up SQLite database (local) or PostgreSQL (supabase)
3. Store: name, email, message, timestamp, status
4. Keep Formspree integration for email notifications

---

## Stories

### Theme Switcher (3 stories)

| Story   | Description                                | Estimate |
| ------- | ------------------------------------------ | -------- |
| THEME-1 | Add setSiteTheme function to Layout.astro  | 1        |
| THEME-2 | Initialize theme from localStorage on load | 1        |
| THEME-3 | Test all 7 themes work correctly           | 1        |

### Contact Form Database (5 stories)

| Story     | Description                     | Estimate |
| --------- | ------------------------------- | -------- |
| CONTACT-1 | Create SQLite database schema   | 1        |
| CONTACT-2 | Build API endpoint /api/contact | 2        |
| CONTACT-3 | Connect form to API endpoint    | 1        |
| CONTACT-4 | Add success/error handling UI   | 1        |
| CONTACT-5 | Test full submission flow       | 1        |

---

## Subagent Assignment

### Theme Fix → Kilo CLI (free)

- Model: `x-ai/grok-code-fast-1:optimized:free`
- Task: Fix ThemeSwitcher functionality

### Contact DB → OpenCode (free)

- Model: `big-pickle`
- Task: Build database + API endpoint

---

## Deployment

**Target: VPS (not Vercel)**

- Server: s60/s61/s62 via Tailscale VPN
- Deployment: GitHub Actions → VPS (already configured)
- Run `npm run build` locally, then deploy to VPS

```sql
CREATE TABLE contacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  message TEXT,
  language TEXT DEFAULT 'en',
  status TEXT DEFAULT 'new',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  source_url TEXT
);
```

### API Response

```json
{
  "success": true,
  "id": 123,
  "message": "Thank you! We'll be in touch."
}
```

---

## Execution Order

1. THEME-1, THEME-2, THEME-3 (sequential - theme needs base first)
2. CONTACT-1 (database setup)
3. CONTACT-2 (API endpoint)
4. CONTACT-3, CONTACT-4, CONTACT-5 (can parallel after CONTACT-2)

---

## Acceptance Criteria

### Theme Switcher

- [ ] All 7 theme buttons visible
- [ ] Clicking theme changes colors immediately
- [ ] Theme persists after page reload
- [ ] Default theme loads on first visit

### Contact Form

- [ ] Form submits to API
- [ ] Data stored in database
- [ ] Success message shown to user
- [ ] Email still sent via Formspree
