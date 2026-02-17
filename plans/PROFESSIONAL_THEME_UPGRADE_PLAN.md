# Plan: Professional Theme Upgrade

This plan outlines the strategy for upgrading the site's visual themes to a more professional and modern standard, inspired by the research on React/Next.js templates like ShadCN/UI.

Instead of overhauling all 8 existing themes, we will create **two new flagship themes** and refine the base styling for components to align with a modern, clean aesthetic.

## New Themes

1.  **`shad-light` (Light Theme):** A clean, minimal theme inspired by the default ShadCN/UI and Vercel design system. It prioritizes typography, whitespace, and subtle interactions.
2.  **`shad-dark` (Dark Theme):** A professional dark mode version of `shad-light`, focusing on reduced contrast for comfortable viewing and a muted, sophisticated color palette.

## Phase 1: Base Style & Configuration Update

This phase establishes the foundational aesthetic for the new themes.

### 1.1. Update Tailwind Configuration (`tailwind.config.mjs`)

- **Fonts:** Update the sans-serif font stack to a modern, system-ui based stack.
  - **Action:** Change `fontFamily` to `['Inter var', 'system-ui', 'sans-serif']`.
- **Border Radius:** Standardize border-radius values to be more subtle and consistent with ShadCN/UI's look.
  - **Action:** Add/modify the `borderRadius` theme object to include specific values like `sm: '0.25rem'`, `md: '0.5rem'`, `lg: '0.75rem'`. Cards and buttons will primarily use `md`.
- **Keyframes:** Add subtle animations for components.
  - **Action:** Add keyframes for `fadeIn` and `slideUp` to be used in popups and on page load.

### 1.2. Define New Theme Palettes (`src/styles/themes.css`)

- **Action:** Add the color definitions for `[data-site-theme='shad-light']` and `[data-site-theme='shad-dark']` to the top of the file with the other themes.

#### `shad-light` Palette (Inspired by ShadCN/UI default)

```css
[data-site-theme='shad-light'] {
  --color-primary: 220 88% 52%; /* A muted, professional blue */
  --color-secondary: 210 40% 96.1%; /* Light gray for secondary elements */
  --color-accent: 217 91% 60%;
  --color-background: 0 0% 100%;
  --color-surface: 0 0% 100%; /* Cards and surfaces are pure white */
  --color-text-main: 222 84% 4.9%; /* Very dark, almost black */
  --color-text-muted: 215 28% 44%;
}
```

#### `shad-dark` Palette

```css
[data-site-theme='shad-dark'] {
  --color-primary: 217 91% 60%;
  --color-secondary: 215 28% 17%;
  --color-accent: 217 91% 60%;
  --color-background: 222 84% 4.9%;
  --color-surface: 222 84% 6.9%; /* Slightly lighter surface for cards */
  --color-text-main: 210 40% 98%;
  --color-text-muted: 215 28% 64%;
}
```

## Phase 2: Component Style Overrides

This phase applies the new aesthetic to specific components when the new themes are active.

### 2.1. Update Card Component Styles

- **Action:** Add new rules to `src/styles/themes.css` for `.card` components under the `shad-light` and `shad-dark` themes.
- **Style:** Remove box-shadow, add a 1px solid border, and use the new standardized border-radius.

```css
/* ShadCN Inspired Cards */
[data-site-theme='shad-light'] .card,
[data-site-theme='shad-dark'] .card {
  border: 1px solid hsl(var(--color-secondary));
  box-shadow: none;
  border-radius: 0.5rem; /* md */
  background: hsl(var(--color-surface));
}

[data-site-theme='shad-light'] .card:hover,
[data-site-theme='shad-dark'] .card:hover {
  background: hsl(var(--color-secondary));
}
```

### 2.2. Update Button Component Styles

- **Action:** Modify the base `Button.astro` component to use the new theme variables and styles for a more modern look (solid background, no pill shape). The component should be adapted to use Tailwind classes that reflect this.

### 2.3. Update Theme Switcher

- **Action:** Add `shad-light` and `shad-dark` to the list of available themes in the `ThemeSwitcher.astro` and/or `ThemeSelector.astro` component.

## Phase 3: Implementation & Verification

- **Task 1:** Implement all Phase 1 changes (Tailwind config, CSS variables).
- **Task 2:** Implement Phase 2 changes (Component style overrides).
- **Task 3:** Update the theme selection UI to include the new themes.
- **Task 4:** Manually test the new themes across all pages to ensure consistency and fix any visual regressions.
