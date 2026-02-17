# SEO Registration Guide

**Date**: 2026-02-17

---

## 1. Google Search Console

### Step 1: Add Property

1. Go to https://search.google.com/search-console
2. Add property: `https://marketing.tvoje.info`
3. Choose: Domain or URL prefix (recommend URL prefix)

### Step 2: Verify Ownership

**Method A: HTML Tag**

- Copy the meta tag from GSC
- Add to `src/layouts/Layout.astro` in `<head>`

**Method B: Google Analytics** (if already using GA4)

- Already verified if GA4 is working

### Step 3: Submit Sitemap

1. Go to Sitemaps in GSC
2. Submit: `sitemap-index.xml` or `sitemap.xml`
3. Check for errors

### Sitemap Status

- Our site already has sitemap: `https://marketing.tvoje.info/sitemap-index.xml`

---

## 2. Seznam.cz Webmaster

### Step 1: Register

1. Go to https://search.seznam.cz/webmaster
2. Add your site: `marketing.tvoje.info`

### Step 2: Verify Ownership

**Method: Meta tag**

- Copy verification code
- Add to `src/layouts/Layout.astro`

### Step 3: Submit URL

1. Use Seznam's "Add URL" feature
2. Or wait for crawling (usually automatic)

---

## 3. Bing Webmaster

### Step 1: Register

1. Go to https://www.bing.com/webmaster
2. Add your site

### Step 2: Verify

- Use XML file or meta tag method

### Step 3: Submit Sitemap

- Submit: `https://marketing.tvoje.info/sitemap-index.xml`

---

## 4. Verification Checklist

| Item                  | Status | Notes |
| --------------------- | ------ | ----- |
| Google Search Console | ☐      |       |
| Sitemap submitted     | ☐      |       |
| Seznam.cz             | ☐      |       |
| Bing Webmaster        | ☐      |       |
| Meta title verified   | ☐      |       |
| Meta description      | ☐      |       |
| h1 tags               | ☐      |       |
| Open Graph tags       | ☐      |       |

---

## 5. Pre-registration Checklist

Before registering, verify:

- [ ] Title tag: `< 60 chars`
- [ ] Meta description: `< 160 chars`
- [ ] H1: One per page, unique
- [ ] Images: All have alt text
- [ ] Sitemap: Valid XML
- [ ] Robots.txt: Allows crawling

---

## 6. Environment Variables

Ensure these are set:

```
PUBLIC_SITE_URL=https://marketing.tvoje.info
```

---

## 7. Tools for Verification

| Tool                  | URL                  | Purpose            |
| --------------------- | -------------------- | ------------------ |
| Google Search Console | search.google.com    | Google indexing    |
| Seznam Webmaster      | search.seznam.cz     | Seznam indexing    |
| Bing Webmaster        | bing.com/webmaster   | Bing indexing      |
| Google Analytics      | analytics.google.com | Traffic (optional) |
| Plausible             | plausible.io         | Privacy analytics  |

---

## 8. Current Status

| Portal | URL                | Status         |
| ------ | ------------------ | -------------- |
| Google | search.google.com  | NOT registered |
| Seznam | search.seznam.cz   | NOT registered |
| Bing   | bing.com/webmaster | NOT registered |

**Next Steps**: Register each portal manually (requires account creation)
