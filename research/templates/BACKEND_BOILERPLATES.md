# Backend & Full-Stack Boilerplate Research

**Date**: 2026-02-18
**Purpose**: Find ready-to-use backend/full-stack boilerplates for Astro portfolio

---

## Summary

### Local Agentic Folder (vscodeportable/agentic)

**No backend templates found** - Contains primarily:

- Agent framework configs (Cline, Kilo, LangChain, etc.)
- BMAD methodology templates
- Infrastructure configs (Redis, GPTCache)
- No Express/Node.js backend boilerplates

---

## GitHub Full-Stack Astro Templates

### 1. Freedom Stack (RECOMMENDED)

| Property   | Value                                        |
| ---------- | -------------------------------------------- |
| **URL**    | https://github.com/cameronapak/freedom-stack |
| **Stars**  | 186                                          |
| **Status** | Archived (v1), v2/v3 available               |
| **DB**     | Astro DB (LibSQL/SQLite)                     |
| **Auth**   | Better Auth                                  |
| **ORM**    | Drizzle                                      |

**Tech Stack:**

- Astro 5.0
- Tailwind CSS + DaisyUI + Preline
- HTMX + Alpine.js (interactivity)
- Astro DB (LibSQL)
- Drizzle ORM
- Better Auth
- Nodemailer (emails)

**Pros:**

- Most complete full-stack solution
- Built-in auth, database, email
- Cursor-optimized (.cursorrules)
- Netlify deployment
- Type-safe

**Cons:**

- Uses Turso/LibSQL (not plain SQLite)
- More complex than needed for simple contact form
- Archived (v1)

**Fit for our needs**: ⚠️ Overkill for simple contact form

---

### 2. Dossier Astro SQLite App

| Property  | Value                                                 |
| --------- | ----------------------------------------------------- |
| **URL**   | https://github.com/dossierhq/dossier-astro-sqlite-app |
| **Stars** | 4                                                     |
| **DB**    | SQLite                                                |
| **ORM**   | Dossier (custom)                                      |

**Tech Stack:**

- Astro
- SQLite
- Dossier ORM

**Pros:**

- Simple SQLite
- Active development

**Cons:**

- Dossier is niche/new ORM
- Limited features

**Fit for our needs**: ⚠️ Too niche

---

### 3. Astro Neon Full-Stack Starter

| Property  | Value                                                                 |
| --------- | --------------------------------------------------------------------- |
| **URL**   | https://github.com/marslansarwar171/astro-neon-full-stack-starter-kit |
| **Stars** | 3                                                                     |
| **DB**    | Neon Postgres                                                         |
| **ORM**   | Drizzle                                                               |

**Tech Stack:**

- Astro + Tailwind
- Neon Postgres
- Drizzle ORM

**Pros:**

- PostgreSQL (production-grade)

**Cons:**

- Requires cloud DB (Neon)
- Not self-hosted

**Fit for our needs**: ❌ Requires cloud

---

### 4. Astro Supabase Starter

| Property  | Value                                                  |
| --------- | ------------------------------------------------------ |
| **URL**   | https://github.com/rankingpress/astro-supabase-starter |
| **Stars** | 1                                                      |
| **DB**    | Supabase (PostgreSQL)                                  |

**Pros:**

- Full-stack with Supabase

**Cons:**

- Requires cloud (Supabase)
- Limited docs

**Fit for our needs**: ❌ Requires cloud

---

## Alternative: Simple Express + SQLite

### 5. Node Express SQLite Form App

| Property  | Value                                         |
| --------- | --------------------------------------------- |
| **URL**   | https://github.com/sahiljaved/DB-Form-Web-App |
| **Stars** | 1                                             |
| **Stack** | Express + SQLite + plain JS                   |

**Pros:**

- Simple, minimal
- Easy to understand

**Cons:**

- No TypeScript
- Basic styling
- No Astro integration

**Fit for our needs**: ⚠️ Standalone, not integrated

---

## Analysis for Our Use Case

### Requirements:

1. Contact form with database storage
2. VPS deployment (s62)
3. Keep existing Astro site
4. Simple/minimal

### Options Ranked:

| Rank | Option                    | Effort | Complexity | VPS Fit |
| ---- | ------------------------- | ------ | ---------- | ------- |
| 1    | Astro Node Adapter + API  | Low    | Simple     | ✅      |
| 2    | Express standalone server | Medium | Simple     | ✅      |
| 3    | Freedom Stack             | High   | Complex    | ⚠️      |
| 4    | Drizzle + SQLite          | Medium | Medium     | ✅      |

---

## Recommendation

### For Simple Contact Form: Option 1

**Astro Node Adapter** is best because:

- Minimal effort (1 command: `npx astro add node`)
- Works with existing site
- VPS-compatible with PM2
- SQLite via better-sqlite3
- No extra services needed

```bash
# Add Node adapter
npx astro add node

# Deploy with PM2
pm2 start dist/server/entry.mjs
```

### For Future Full-Stack: Freedom Stack v3

If you need full features later:

- https://github.com/cameronapak/freedom-stack-v3
- Built-in auth, DB, email
- More complete solution

---

## References

1. Freedom Stack: https://github.com/cameronapak/freedom-stack
2. Freedom Stack v2: https://github.com/cameronapak/freedom-stack-v2
3. Freedom Stack v3: https://github.com/cameronapak/freedom-stack-v3
4. Better T Stack: https://better-t-stack.amanv.dev/new
5. Dossier Astro: https://github.com/dossierhq/dossier-astro-sqlite-app
6. Astro Neon Starter: https://github.com/marslansarwar171/astro-neon-full-stack-starter-kit
7. Astro Supabase Starter: https://github.com/rankingpress/astro-supabase-starter
