# Phase 1: Research & PRD

## Metadata

- **Status**: Ready for Review
- **Owner**: Roadmap-Keeper
- **Start Date**: 2026-02-13
- **Duration**: 2 days
- **Budget**: $5 (Gemini/Opus)

## Objectives

- [ ] Define full requirements for Marketing Automation Platform.
- [ ] Research top 20 Czech marketing agencies for 2026.
- [ ] Establish technical architecture (Next.js + Antigravity).

## Agents & Skills

- **Lead**: Orchestrator (Claude Opus)
- **Research**: Researcher (Gemini 3 Pro - SERP)
- **Doc Writer**: PRD-Specialist (Groq 70B via Template-Factory)

## Deliverables

| Artifact     | Path                                          | Description                 |
| ------------ | --------------------------------------------- | --------------------------- |
| Agency List  | `docs/prd-data/marketing-agencies-summary.md` | Top 20 agencies analysis    |
| PRD          | `docs/prd-data/bmad-prd.md`                   | Detailed spec from template |
| Architecture | `docs/architecture/system-design.md`          | Tech stack decision record  |

## Execution Plan

1.  **Researcher**: Scrape "top marketing agencies Czech 2026".
2.  **Orchestrator**: Review research data.
3.  **PRD-Specialist**: Fill `bmad-prd.md` template with findings.
4.  **Roadmap-Keeper**: Trigger Phase 2 (MVP) upon PRD approval.

## Next Phase Trigger

- PRD approved by User.
