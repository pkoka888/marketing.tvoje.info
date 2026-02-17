# Design Enhancement Plan - Parallel Agent Orchestration

**Created**: 2026-02-16
**Status**: Active
**Orchestrator**: OpenCode (with parallel subagents)

---

## Goal

Implement 5 design enhancements from React boilerplates research in parallel using subagents:

1. Bento Grid Layout
2. Minimal Dark/Light Toggle
3. Animated Gradient Mesh
4. Glassmorphism Cards
5. Micro-interactions

---

## Implementation Strategy

| Agent       | Task               | Target Component          |
| ----------- | ------------------ | ------------------------- |
| **Agent 1** | Bento Grid         | Hero/Services section     |
| **Agent 2** | Dark Toggle        | ThemeSwitcher.astro       |
| **Agent 3** | Gradient Mesh      | themes.css + Hero         |
| **Agent 4** | Glassmorphism      | Card.astro                |
| **Agent 5** | Micro-interactions | Button.astro + global.css |

---

## Phase 1: Analysis & Planning (Parallel Research)

### Agent Tasks:

- [ ] Research existing component implementations
- [ ] Identify injection points for new features
- [ ] Document dependencies between components

### Files to Analyze:

- `src/components/sections/Hero.astro`
- `src/components/sections/Services.astro`
- `src/components/common/ThemeSwitcher.astro`
- `src/components/ui/Card.astro`
- `src/components/ui/Button.astro`
- `src/styles/themes.css`
- `src/styles/global.css`

---

## Phase 2: Implementation (Parallel Execution)

### Task 2.1: Bento Grid Layout

**Agent**: Designer
**Target**: Hero + Services sections
**Files**: `src/components/sections/Hero.astro`, `src/components/sections/Services.astro`
**Changes**:

- Replace linear service cards with bento grid
- Add varying card sizes (1x1, 2x1, 1x2)
- Add hover effects with scale/glow

### Task 2.2: Minimal Dark/Light Toggle

**Agent**: Frontend Dev
**Target**: Theme switcher
**Files**: `src/components/common/ThemeSwitcher.astro`, `src/layouts/Layout.astro`
**Changes**:

- Simplify toggle to minimal icon switch
- Add smooth transition animation
- Add system preference detection
- Persist to localStorage

### Task 2.3: Animated Gradient Mesh

**Agent**: Designer
**Target**: Background effects
**Files**: `src/styles/themes.css`, `src/components/sections/Hero.astro`
**Changes**:

- Create CSS gradient animation keyframes
- Add mesh blur effect
- Apply to hero background
- Support light/dark variants

### Task 2.4: Glassmorphism Cards

**Agent**: Frontend Dev
**Target**: Project cards
**Files**: `src/components/ui/Card.astro`, `src/components/sections/Projects.astro`
**Changes**:

- Add backdrop-filter: blur
- Add semi-transparent background
- Add subtle border
- Add hover lift effect

### Task 2.5: Micro-interactions

**Agent**: Frontend Dev
**Target**: Buttons + Global
**Files**: `src/components/ui/Button.astro`, `src/styles/global.css`
**Changes**:

- Button hover scale (1.02)
- Button active scale (0.98)
- Focus ring animation
- Link underline animation
- Card hover lift

---

## Phase 3: Integration & Testing

### Task 3.1: Component Integration

- [ ] Ensure all components work together
- [ ] Verify theme switching applies to all new elements
- [ ] Check responsive behavior

### Task 3.2: Visual Testing

- [ ] Desktop view verification
- [ ] Mobile view verification
- [ ] Dark mode verification
- [ ] Light mode verification

### Task 3.3: Performance Testing

- [ ] Lighthouse score check (target: 95+)
- [ ] Build time check
- [ ] Bundle size check

### Task 3.4: Accessibility Testing

- [ ] Keyboard navigation
- [ ] Focus states
- [ ] Color contrast
- [ ] Screen reader compatibility

---

## Phase 4: Deployment

### Task 4.1: Build & Test

```bash
npm run build
npm run test
```

### Task 4.2: Deploy to VPS

```bash
scp dist/* pavel@100.91.164.109:/var/www/projects/marketing.tvoje.info/
```

### Task 4.3: Verify Production

- [ ] Homepage loads
- [ ] Theme toggle works
- [ ] All sections render

---

## Agent Commands

### Start Parallel Research:

```
[Agent: Explore] Analyze Hero.astro, Services.astro, ThemeSwitcher.astro, Card.astro, Button.astro
[Agent: Explore] Analyze themes.css and global.css for styling patterns
```

### Start Parallel Implementation:

```
[Agent: Designer] Implement Bento Grid in Hero/Services
[Agent: Designer] Implement Gradient Mesh animation
[Agent: Frontend] Implement Dark/Light Toggle
[Agent: Frontend] Implement Glassmorphism Cards
[Agent: Frontend] Implement Micro-interactions
```

### Verify:

```
[Agent: Test] Run Playwright visual verification
```

---

## Dependencies

| Task               | Depends On  | Blocked By |
| ------------------ | ----------- | ---------- |
| Bento Grid         | Phase 1     | None       |
| Dark Toggle        | Phase 1     | None       |
| Gradient Mesh      | Phase 1     | None       |
| Glassmorphism      | Phase 1     | None       |
| Micro-interactions | Phase 1     | None       |
| Integration        | All Phase 2 | Phase 2    |
| Testing            | Integration | Phase 3.1  |
| Deployment         | Testing     | Phase 3.3  |

---

## Success Criteria

| Metric                   | Target         | Current |
| ------------------------ | -------------- | ------- |
| Lighthouse Performance   | ≥95            | 100     |
| Lighthouse Accessibility | ≥95            | 93      |
| Bento Grid               | ✅ Implemented | ❌      |
| Glassmorphism            | ✅ Implemented | ❌      |
| Gradient Animation       | ✅ Implemented | ❌      |
| Micro-interactions       | ✅ Implemented | ❌      |
| Theme Toggle             | ✅ Improved    | ⏳      |

---

## Timeline

| Phase   | Duration | Focus          |
| ------- | -------- | -------------- |
| Phase 1 | 10 min   | Research       |
| Phase 2 | 30 min   | Implementation |
| Phase 3 | 15 min   | Testing        |
| Phase 4 | 5 min    | Deployment     |

**Total**: ~60 minutes

---

## Notes

- Use existing theme system (titan, nova, spark, lux, target)
- Maintain bilingual support (EN/CS)
- Keep accessibility focus (WCAG 2.2 AA)
- Minimize JavaScript additions (Astro philosophy)

---

_Plan Status: READY FOR EXECUTION_
_Last Updated: 2026-02-16_
