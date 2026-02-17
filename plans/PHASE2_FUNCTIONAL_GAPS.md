# Functional Gaps Analysis

**Date**: 2026-02-17
**Status**: Audit Complete

---

## 1. Form Functionality ✅

### Contact Form

- **Status**: Implemented
- **Provider**: Formspree
- **Form ID**: `xpwzgvry` (in FastOnboarding.astro)
- **GDPR**: Consent checkbox implemented ✅
- **Validation**: HTML5 + JS validation ✅
- **Success/Error States**: Implemented ✅

### Issues

- None identified

---

## 2. Analytics ✅

### Plausible Analytics

- **Status**: Configured
- **Location**: `src/layouts/Layout.astro`
- **Script**: Plausible script included ✅

### Environment Variables Needed

- `PUBLIC_SITE_URL`: Should be set
- Check `.env` for `PLAUSIBLE_API_KEY` if needed

---

## 3. Theme Switcher ✅

### ThemeSelector Component

- **Status**: Implemented
- **Themes**: 7 themes (Titan, Lux, Nova, Spark, Target, Obsidian, Playful)
- **Persistence**: localStorage ✅
- **Popup**: ThemePopup.astro with delay + exit intent ✅

### Verified Files

- `src/components/common/ThemeSelector.astro`
- `src/components/common/ThemePopup.astro`

---

## 4. Search Portals Registration

### Status: NOT COMPLETE

| Portal                | URL                  | Status             | Action Needed  |
| --------------------- | -------------------- | ------------------ | -------------- |
| Google Search Console | search.google.com    | ❌ Not registered  | Submit sitemap |
| Seznam.cz             | search.seznam.cz     | ❌ Not registered  | Submit URL     |
| Bing Webmaster        | bing.com/webmaster   | ❌ Not registered  | Submit sitemap |
| Google Analytics      | analytics.google.com | ⚠️ Using Plausible | Consider GA4   |

### Required Actions

1. Submit `sitemap-0.xml` to Google Search Console
2. Register at Seznam.cz webmaster tools
3. Verify ownership for all properties

---

## 5. Ads Tracking

### Status: NOT IMPLEMENTED

| Platform              | Status     | Priority | Notes                   |
| --------------------- | ---------- | -------- | ----------------------- |
| Facebook Pixel        | ❌ Missing | Medium   | Add to Layout           |
| Google Ads Conversion | ❌ Missing | Medium   | Add conversion tracking |
| Google Remarketing    | ❌ Missing | Low      | For future              |
| LinkedIn Insight      | ❌ Missing | Low      | B2B focus               |

### Recommended Implementation

1. Add FB Pixel to Layout.astro
2. Add Google Ads conversion tags
3. Create conversion events in Google Ads

---

## 6. Environment Variables Checklist

| Variable            | Status   | Notes           |
| ------------------- | -------- | --------------- |
| PUBLIC_SITE_URL     | ⚠️ Check | Should be set   |
| PUBLIC_FORMSPREE_ID | ✅ Set   | xpwzgvry        |
| PLAUSIBLE_API_KEY   | Optional | Using Plausible |

---

## Action Items

### Immediate (P0)

- [ ] Register Google Search Console
- [ ] Submit sitemap to Google

### Short-term (P1)

- [ ] Register Seznam.cz
- [ ] Add FB Pixel

### Long-term (P2)

- [ ] Google Ads conversion tracking
- [ ] LinkedIn Insight tag
