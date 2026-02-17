# Theme Selector Popup Plan - Exit Intent & Delayed Show

**Created**: 2026-02-16
**Status**: Planning
**Type**: Feature Enhancement

---

## Problem Statement

1. **Theme Switcher Missing**: The ThemeSwitcher component exists but is NOT imported anywhere in the Header - only dark/light toggle exists
2. **User Request**: Create modern popup theme selector that:
   - Shows as dropdown (compact, consistent)
   - Shows theme names
   - Appears after 1 minute of page time
   - Appears on exit intent (when mouse leaves viewport toward top)
   - Motivational message to encourage selection
   - Modern modal/popup design

---

## Current State

### Files Involved:

- `src/components/common/ThemeSwitcher.astro` - Exists but unused
- `src/components/common/Header.astro` - Has dark/light toggle only (lines 68-81)
- `src/layouts/Layout.astro` - Has theme switching logic
- `src/styles/themes.css` - Theme CSS variables
- `src/styles/global.css` - Global styles

### Theme Options (5 themes):

1. **Titan** - Direct/Professional (blue)
2. **Nova** - Friendly/Expert (gradient)
3. **Target** - Goal-focused (dark blue)
4. **Spark** - Bold/Provocative (neon)
5. **Lux** - Minimal/Premium (gold)

---

## Implementation Plan

### Phase 1: Component Architecture

#### 1.1 Create ThemeSelector Component

**File**: `src/components/common/ThemeSelector.astro`

**Features**:

- Dropdown with theme names
- Preview thumbnails
- Current theme indicator
- Compact design (icon + text)

**Structure**:

```astro
<!-- Compact dropdown trigger -->
<button class="theme-selector-trigger">
  <span class="theme-icon"></span>
  <span class="theme-name">Titan</span>
  <svg class="chevron"></svg>
</button>

<!-- Dropdown panel -->
<div class="theme-dropdown hidden">
  <div class="theme-option" data-theme="titan">
    <div class="theme-preview"></div>
    <span class="theme-label">Titan</span>
    <span class="theme-desc">Direct, Professional</span>
  </div>
  <!-- ... other themes -->
</div>
```

#### 1.2 Create ThemePopup Component

**File**: `src/components/common/ThemePopup.astro`

**Features**:

- Modal overlay with backdrop blur
- Motivational headline
- Theme preview cards
- "Continue browsing" CTA
- Smooth entrance/exit animations
- Close on backdrop click or ESC

**Content**:

```
Headline: "Find Your Perfect Look!"
Subhead: "Choose a theme that matches your style and keep exploring"
[Theme Cards Grid]
[Continue] button
```

---

### Phase 2: Timing Logic

#### 2.1 Delayed Show (1 minute)

```javascript
// In Layout.astro or ThemePopup.astro
setTimeout(() => {
  if (!localStorage.getItem('themeSelected')) {
    showThemePopup();
  }
}, 60000); // 1 minute
```

#### 2.2 Exit Intent Detection

```javascript
document.addEventListener('mouseleave', (e) => {
  if (e.clientY <= 0 && !localStorage.getItem('themeSelected')) {
    showThemePopup();
  }
});
```

#### 2.3 Show Limits

- Show max 1 time per session
- Don't show if user already selected theme
- Don't show on certain pages (e.g., /contact, /projects)
- Respect `localStorage.themePopupDismissed`

---

### Phase 3: Integration

#### 3.1 Header Integration

- Replace current dark/light toggle with ThemeSelector dropdown
- Add trigger button in Header.astro

#### 3.2 Layout Integration

- Add ThemePopup component to Layout.astro
- Add timing logic in Layout.astro script

---

### Phase 4: Styling

#### 4.1 ThemeSelector Styles (global.css)

```css
.theme-selector-trigger {
  @apply flex items-center gap-2 px-3 py-2 rounded-lg
         bg-gray-100 dark:bg-dark-800 hover:bg-gray-200
         dark:hover:bg-dark-700 transition-all duration-200;
}

.theme-dropdown {
  @apply absolute right-0 mt-2 w-64 rounded-xl
         bg-white dark:bg-dark-800 shadow-xl
         border border-gray-200 dark:border-dark-700 overflow-hidden;
  animation: dropdown-open 0.2s ease-out;
}
```

#### 4.2 ThemePopup Styles (global.css)

```css
.theme-popup-overlay {
  @apply fixed inset-0 z-50 flex items-center justify-center
         bg-black/50 backdrop-blur-sm;
  animation: fade-in 0.3s ease-out;
}

.theme-popup-content {
  @apply relative max-w-2xl w-full mx-4 rounded-2xl
         bg-white dark:bg-dark-900 shadow-2xl
         border border-gray-200 dark:border-dark-700 overflow-hidden;
  animation: popup-scale 0.3s ease-out;
}
```

---

## Subagent Orchestration Plan

### Agent 1: UI Component Developer

**Task**: Create ThemeSelector dropdown component

**Files**:

- `src/components/common/ThemeSelector.astro`
- Update `src/components/common/Header.astro` to include

**Deliverables**:

- Compact dropdown with 5 theme options
- Theme preview colors
- Click-outside to close
- Keyboard accessible

### Agent 2: Popup Developer

**Task**: Create ThemePopup modal

**Files**:

- `src/components/common/ThemePopup.astro`
- Update `src/layouts/Layout.astro`

**Deliverables**:

- Modal with motivational content
- 5 theme preview cards
- Timing logic (1 min + exit intent)
- Session storage logic

### Agent 3: Styling Engineer

**Task**: Add all required CSS

**Files**:

- `src/styles/global.css`

**Deliverables**:

- ThemeSelector dropdown styles
- ThemePopup modal styles
- Animations (fade, scale, slide)
- Responsive design

### Agent 4: Integration Tester

**Task**: Verify implementation

**Files**: All above + tests

**Deliverables**:

- Build passes
- Playwright tests for popup
- Manual verification

---

## Files to Modify/Create

| File                                        | Action | Description           |
| ------------------------------------------- | ------ | --------------------- |
| `src/components/common/ThemeSelector.astro` | Create | Dropdown component    |
| `src/components/common/ThemePopup.astro`    | Create | Modal popup component |
| `src/components/common/Header.astro`        | Modify | Add ThemeSelector     |
| `src/layouts/Layout.astro`                  | Modify | Add ThemePopup        |
| `src/styles/global.css`                     | Modify | Add component styles  |

---

## Acceptance Criteria

### Visual

- [ ] Dropdown shows theme names with preview colors
- [ ] Popup appears centered with blur backdrop
- [ ] Smooth animations on open/close
- [ ] Responsive on mobile

### Functional

- [ ] Popup shows after 60 seconds
- [ ] Popup shows on mouse exit (top of viewport)
- [ ] Popup respects session limits (show once)
- [ ] Theme selection persists to localStorage
- [ ] "Continue" button closes popup

### Technical

- [ ] Build passes
- [ ] No console errors
- [ ] Keyboard accessible
- [ ] WCAG compliant (focus trap, ESC to close)

---

## Alternative Approaches Considered

### Option A: Bottom-right toast (Current Plan)

- Pros: Non-intrusive, modern
- Cons: May be missed

### Option B: Full-screen takeover

- Pros: High engagement
- Cons: Too intrusive, bad UX

### Option C: Floating button

- Pros: Always visible
- Cons: Takes screen space

**Selected**: Option A (Popup modal) as requested by user

---

## Questions for User

1. Should popup show on ALL pages or exclude some (e.g., contact)?
2. Should we show different motivational text per theme?
3. Should we track "theme selected" in analytics?

---

_Plan Status: READY FOR EXECUTION_
