# Marketing Portfolio MVP Implementation Plan

**Created**: 2026-02-16
**Status**: Active
**Orchestrator**: OpenCode (with subagent orchestration)

---

## Executive Summary

This plan consolidates the MVP implementation for the Marketing Portfolio website. Based on analysis of:

- Current codebase (12 pages, build passes)
- Plan-e-mvp-implementation.md (outdated DevOps references)
- MASTER_MARKETING_PRD.md (core requirements)
- bmad-marketing-platform-roadmap.md (ARCHIVED - different project)

**Goal**: Complete Marketing Portfolio MVP with proper research and best practices.

---

## Current State

| Component       | Status                                                    | Notes                       |
| --------------- | --------------------------------------------------------- | --------------------------- |
| Pages           | ✅ 12 pages                                               | Build passes                |
| Sections        | ✅ Hero, About, Projects, Services, Contact, Testimonials | All present                 |
| Services        | ✅ strategy, campaigns, consulting                        | Marketing-focused           |
| Bilingual       | ✅ EN/CZ                                                  | Working                     |
| Dark Mode       | ✅                                                        | ThemeSwitcher with 5 themes |
| Language Toggle | ✅                                                        | EN/CS switcher              |
| Mobile Nav      | ✅                                                        | Hamburger menu              |
| Formspree       | ✅                                                        | Contact form integrated     |
| Deployment      | ✅                                                        | VPS deployed                |

---

## Priority TODO (P0-P3)

### P0 - Critical (This Week)

| #    | Task                           | Status         | Notes                                                                                      |
| ---- | ------------------------------ | -------------- | ------------------------------------------------------------------------------------------ |
| P0.1 | Update Hero title to Marketing | ✅ Done        | "Marketing & Growth Specialist"                                                            |
| P0.2 | Add 3-5 marketing projects     | ✅ Done        | Fixed categories to seo/ppc/web/infrastructure                                             |
| P0.3 | Update project categories      | ✅ Done        | SEO, PPC/Ads, Content, Growth                                                              |
| P0.4 | Run Lighthouse test            | ✅ 98/93/69/92 | Performance 98 (up from 94), Accessibility 93, Best Practices 69, SEO 92 - Need deployment |

### P1 - High (Week 2)

| #    | Task                       | Status  | Notes                              |
| ---- | -------------------------- | ------- | ---------------------------------- |
| P1.1 | Enhance form functionality | ✅ Done | Added budget dropdown              |
| P1.2 | Add testimonials           | ✅ Done | Added 2 new testimonials (3 total) |
| P1.3 | Verify project filtering   | ✅ Done | Categories fixed, filtering works  |

### P2 - Medium (Week 3)

| #    | Task                      | Status  | Notes                                |
| ---- | ------------------------- | ------- | ------------------------------------ |
| P2.1 | Services clarity review   | ✅ Done | Verified marketing terminology       |
| P2.2 | About section enhancement | ✅ Done | Updated certifications to marketing  |
| P2.3 | SEO meta tags audit       | ✅ Done | Meta-focused tags verified marketing |

### P3 - Low (Week 4+)

| #    | Task                     | Status  | Notes                   |
| ---- | ------------------------ | ------- | ----------------------- |
| P3.1 | Social media integration | ✅ Done | Real social links added |
| P3.2 | Loading states           | ⏳      | Skeleton loaders        |
| P3.3 | Performance fine-tuning  | ⏳      | If Lighthouse <95       |

---

## Files to Archive

Move to `plans/.archive/`:

| File                                      | Reason                   |
| ----------------------------------------- | ------------------------ |
| `bmad-marketing-platform-roadmap.md`      | Different project (SaaS) |
| `mission-brief-marketing-platform.md`     | SaaS platform brief      |
| `plans/marketing-portfolio-prd-plan.md`   | Outdated, superseded     |
| `docs/prd-data/marketing-platform-prd.md` | SaaS PRD                 |
| `docs/prd-data/scrap/*`                   | Research for SaaS        |

---

## Files to Keep

| File                           | Purpose                       |
| ------------------------------ | ----------------------------- |
| `MASTER_MARKETING_PRD.md`      | Core PRD (update terminology) |
| `plan-e-mvp-implementation.md` | Base reference (update)       |

---

## Research Results (COMPLETE - 4 parallel subagents)

| #   | Topic                         | Findings                                                    |
| --- | ----------------------------- | ----------------------------------------------------------- |
| R1  | Portfolio Best Practices 2026 | Bento grids, typography-led, conversion 2-5%, WCAG 2.2 AA   |
| R2  | Astro Performance             | Islands architecture, AVIF images, Tailwind 4.0, LCP <2s    |
| R3  | Free LLM Providers            | **OpenRouter** best (31 free models), Groq limited          |
| R4  | UX Patterns                   | 3-4 form fields, curate 3-5 case studies, /cs/ subdirectory |

---

## Implementation Notes

### Providers Configuration

| Provider       | Status         | Best Use                      |
| -------------- | -------------- | ----------------------------- |
| **Kilo Code**  | ⏳ Test        | Agentic coding (MiniMax-M2.5) |
| **Cline**      | ⏳ Test        | VS Code tasks (kat-coder-pro) |
| **Groq**       | ✅ Working     | Complex tasks, research       |
| **OpenRouter** | ⏳ Recommended | Free fallback (50 req/day)    |

See `UNIFIED_PROVIDER_STRATEGY.md` for full decision matrix.

### Agent Rules

- Use `.clinerules/` for validation
- Use `.kilocode/rules/` for context
- Visual verification required for UI changes
- Build must pass before commit

---

## Timeline

| Week | Focus    | Deliverables                                 |
| ---- | -------- | -------------------------------------------- |
| 1    | P0 Tasks | Hero updated, projects added, Lighthouse 95+ |
| 2    | P1 Tasks | Form enhanced, testimonials added            |
| 3    | P2 Tasks | SEO audit, services clarity                  |
| 4    | P3 Tasks | Polish, performance tuning                   |

---

## Next Steps

1. Execute P0 tasks in parallel with research
2. Archive SaaS-related files
3. Update MASTER_MARKETING_PRD.md terminology
4. Run Lighthouse and verify 95+ scores

---

_Plan Status: READY FOR EXECUTION_
_Last Updated: 2026-02-16_
