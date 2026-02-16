# Frontend Gap Analysis & Implementation Plan

Analysis of the current codebase against the **Visual & Content Upgrade Plan 2026**.

## Executive Summary

The `src/` directory is missing critical components defined in `visual-upgrade-2026.md`. While the core Astro/React structure is present, the "10x Performance" features (Design Switcher, Real Tools) are effectively 0% implemented.

## 🔴 Critical Gaps (Unimplemented Tasks)

### 1. Design System & Theming

- **Missing**: `ThemeSwitcher.tsx` component.
- **Missing**: `ThemeContext` provider for managing the 8 planned themes (Google Modern, Glass Morphism, etc.).
- **Missing**: CSS Variables in `tailwind.config.mjs` to support dynamic switching.
- **Status**: ❌ Not Started.

### 2. Branding & Identity

- **Missing**: New "EX" SVG Logo implementation.
- **Missing**: "Visionary Expert" personal photo asset.
- **Status**: ❌ Using placeholders or old assets.

### 3. "Real Tools" (Buyer Enablement)

The plan calls for interactive mock tools to demonstrate value. None exist in `src/components/dashboard/` or `src/components/ui/`.

- **Missing**: `AdsManager.tsx` (Ad spend simulator).
- **Missing**: `SmartMerchantCenter.tsx` (Feed health score).
- **Missing**: `AnalyticsDashboard.tsx` (3D Pie/Line charts).
- **Status**: ❌ Not Started.

### 4. Copywriting

- **Partial**: Headlines in `Hero.astro` need updating to the new 2026 variants (e.g., "Přestaňte pálit peníze").
- **Status**: ⚠️ Outdated.

### 5. Technical Debt & Code Health

- **Linting Errors**: `npm run lint` reveals unused variables and type issues in `src/components/dashboard/Orchestrator.tsx` and `src/components/sections/Hero.astro`.
- **Git Status**: Clean, but `package-lock.json` is out of sync in some branches.
- **Status**: ⚠️ Needs cleanup before feature work.

---

## 📅 Implementation Roadmap

### Phase 1: Foundation (Design System)

1.  **[CODE]** Create `src/context/ThemeContext.tsx` with light/dark modes.
2.  **[CODE]** Update `tailwind.config.mjs` with CSS variable mappings.
3.  **[CODE]** Build `src/components/common/ThemeSwitcher.tsx` (Floating UI).

### Phase 2: "Real Tools" Components

4.  **[CODE]** Scaffold `src/components/dashboard/mock-tools/` directory.
5.  **[CODE]** Implement `AdsManagerSimulator.tsx` using Recharts/Framer Motion.
6.  **[CODE]** Implement `MerchantHealth.tsx` with interactive "Fix" buttons.

### Phase 3: Visual Polish

7.  **[ASSETS]** Generate/Implement new "EX" logo SVGs.
8.  **[CONTENT]** Update `Hero.astro` headlines to 2026 variants.

## Recommended Next Step

Start **Phase 1: Foundation**. Without the `ThemeContext` and Tailwind variables, the visual upgrade cannot proceed.
