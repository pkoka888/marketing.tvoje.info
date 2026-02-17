# AGENTS.md

This file provides instructions for all AI agents working with this repository.
Format follows the [AGENTS.md standard](https://agents.md).

---

## Agent Registry

| Agent                          | Role                           | Config          | Model             |
| ------------------------------ | ------------------------------ | --------------- | ----------------- |
| **Antigravity** (OpenCode CLI) | Architect, planner, auditor    | `GEMINI.md`     | MiniMax-M2.1:free |
| **Kilo Code** (VS Code ext)    | Developer, implementer, keeper | `.kilocode/`    | MiniMax-M2.1:free |
| **Cline** (CLI headless)       | Validator, tester, debugger    | `.clinerules/`  | MiniMax-M2.1:free |
| **OpenCode** (fallback)        | Backup executor                | `cli/opencode/` | Default           |

---

## Setup Commands

```bash
npm install          # Install dependencies
npm run dev          # Start dev server (localhost:4321)
npm run build        # Production build to dist/
npm run test         # Run Vitest suite
npm run lint         # ESLint check
npm run format:check # Prettier check
```

## Test Commands

```bash
npm run test         # Run all tests
npm run test:watch   # Watch mode
```

## Build Commands

```bash
npm run build        # Astro static build → dist/
npm run preview      # Preview production build
```

---

## Shared Knowledge Locations

| Location                       | Purpose                           | Writable By                |
| ------------------------------ | --------------------------------- | -------------------------- |
| `AGENTS.md`                    | Agent registry & instructions     | All agents (with approval) |
| `GEMINI.md`                    | Antigravity-specific instructions | Antigravity                |
| `.kilocode/knowledge/`         | Project architecture & patterns   | Kilo Code, Keeper          |
| `.kilocode/rules/memory-bank/` | Persistent project context        | Kilo Code                  |
| `.clinerules/`                 | Cline coding & validation rules   | Cline                      |
| `plans/agent-shared/`          | Cross-agent plans & reports       | All agents                 |

---

## Validation Checklist

Before committing changes, verify:

- [ ] `npm run build` passes (exit 0)
- [ ] `npm run test` passes
- [ ] `npm run format:check` passes
- [ ] No new lint errors
- [ ] Bilingual content: both EN and CS versions updated
- [ ] Accessibility: semantic HTML, ARIA labels, contrast ratios
- [ ] No hardcoded secrets (use `.env`)

---

## Error Log Locations

| Source         | How to Check                                      |
| -------------- | ------------------------------------------------- |
| Astro build    | `npm run build 2>&1`                              |
| Vitest         | `npm run test 2>&1`                               |
| ESLint         | `npx eslint src/ --config eslint.config.mjs 2>&1` |
| GitHub Actions | `.github/workflows/` → GitHub Actions tab         |

---

## Architecture

- **Framework**: Astro 5.0 (static site, zero JS by default)
- **Styling**: Tailwind CSS 3.4
- **Language**: TypeScript 5.7
- **Content**: MDX collections (`src/content/projects/`)
- **i18n**: EN (default, no prefix) + CS (`/cs/` prefix)
- **Translations**: `src/i18n/translations.ts`
- **Deployment**: VPS s62 via GitHub Actions (static files to Nginx)
- **URL**: https://marketing.tvoje.info
- **CI/CD**: GitHub Actions (`.github/workflows/`)
- **Testing**: Vitest (`vitest.config.ts`)
- **Analytics**: Plausible (cookie-free)
- **Forms**: Formspree

---

## File Structure Conventions

- Component sections: `src/components/sections/` (Hero, About, Projects, etc.)
- UI primitives: `src/components/ui/` (Badge, Button, Card)
- Common layout: `src/components/common/` (Header, Footer)
- Pages: `src/pages/` (EN), `src/pages/cs/` (CS)
- One `<h1>` per page, semantic HTML5 elements
- `lang` prop on bilingual components

---

## Memory Bank (Kilo Code)

Loading `.kilocode/rules/memory-bank/` is **mandatory** for every Kilo Code task.
Response must include `[Memory Bank: Active]` or `[Memory Bank: Missing]`.

## Keeper Agent (Kilo Code)

Source directory: `C:\Users\pavel\vscodeportable\agentic\`
Commands: `Keeper analyze all`, `Keeper sync all`, `Keeper rollback`
Protected files: `.clinerules/*`, `.kilocode/rules/memory-bank/`
