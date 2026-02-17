# User Action Plan - Search Portal Registration

**Date**: 2026-02-17
**Status**: Pending Manual Action Required

---

## 1. Google Search Console Registration

### Step 1: Go to Google Search Console

**URL**: https://search.google.com/search-console

### Step 2: Add Property

- Enter: `https://marketing.tvoje.info`
- Click "Continue"

### Step 3: Verify Ownership

**Recommended: HTML Tag Method**

1. Copy the meta tag provided
2. I'll add it to the site - just confirm when done

### Step 4: Submit Sitemap

1. Go to "Sitemaps" in left menu
2. Enter: `sitemap-index.xml`
3. Click "Submit"

### Step 5: Verify

- Check "Coverage" for any errors
- Should show green "Valid" status

---

## 2. Seznam.cz Webmaster Registration

### Step 1: Go to Seznam Webmaster

**URL**: https://search.seznam.cz/webmaster

### Step 2: Add Site

- Enter: `marketing.tvoje.info`
- Click "Přidat" (Add)

### Step 3: Verify Ownership

**Method: Meta Tag**

1. Copy the verification code
2. I'll add it to the site

### Step 4: Submit URL

- Use "Přidat URL" (Add URL) if available
- Or wait for automatic crawling

---

## 3. Bing Webmaster Registration

### Step 1: Go to Bing Webmaster

**URL**: https://www.bing.com/webmaster

### Step 2: Sign In

- Use Microsoft account

### Step 3: Add Site

- Click "Add Site"
- Enter: `https://marketing.tvoje.info`

### Step 4: Verify

- Download XML file OR use meta tag
- I'll add the meta tag

### Step 5: Submit Sitemap

- Go to "Configure My Site" → "Sitemaps"
- Submit: `https://marketing.tvoje.info/sitemap-index.xml`

---

## 4. Environment Variables to Update

Create or update `.env` file in project root:

```bash
# Required
PUBLIC_SITE_URL=https://marketing.tvoje.info

# Optional - Replace placeholders
PUBLIC_FORMSPREE_ID=your_formspree_id
PUBLIC_GOOGLE_TAG_MANAGER=GTM-XXXXXXX
PUBLIC_FACEBOOK_PIXEL=YOUR_PIXEL_ID
```

### How to Get Each ID:

| Variable                    | How to Get                                            |
| --------------------------- | ----------------------------------------------------- |
| `PUBLIC_FORMSPREE_ID`       | Sign up at formspree.io, create form, get ID from URL |
| `PUBLIC_GOOGLE_TAG_MANAGER` | Go to tagmanager.google.com, create account, get ID   |
| `PUBLIC_FACEBOOK_PIXEL`     | Go to business.facebook.com, create Pixel, get ID     |

---

## 5. What I've Prepared

### Added to Layout.astro

- FB Pixel placeholder
- Meta tag slots for verification (ready to add)

### What's Needed From You

1. ✅ **Google Account** - Go to search.google.com
2. ✅ **Microsoft Account** - Go to bing.com/webmaster
3. ✅ **Seznam Account** - Go to search.seznam.cz/webmaster

### IDs to Update

After getting IDs, update `.env`:

```
PUBLIC_FACEBOOK_PIXEL=1234567890
```

---

## Quick Checklist

| Task                  | URL                        | Done |
| --------------------- | -------------------------- | ---- |
| Google Search Console | search.google.com          | ☐    |
| Submit sitemap        | (in GSC)                   | ☐    |
| Seznam.cz             | search.seznam.cz/webmaster | ☐    |
| Bing Webmaster        | bing.com/webmaster         | ☐    |
| Update .env           | (edit file)                | ☐    |

---

## Need Help?

- **Google Search Console Help**: https://support.google.com/search-console
- **Seznam Help**: https://podpora.seznam.cz/webmaster
- **Bing Help**: https://www.bing.com/webmaster/help
