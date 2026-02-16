# Agent State Tracker

**Last Updated**: 2026-02-13 08:45
**Format**: JSON for machine parsing + markdown for humans

---

## Active Agents

| Agent       | Status    | Current Task              | Last Active |
| ----------- | --------- | ------------------------- | ----------- |
| Antigravity | 🟢 Active | Orchestration             | 2026-02-13  |
| Kilo Code   | 🟢 Active | Website Redesign Research | 2026-02-13  |
| Groq        | 🟢 Active | Direct API                | 2026-02-13  |
| Firecrawl   | 🟢 Active | Job & Company Scraping    | 2026-02-13  |

---

## Current Orchestration Mode

**Mode**: BMAD Orchestration
**Project**: Marketing Website Redesign (CZ Market)
**Phase**: Analysis Complete → Planning

---

## Recent Agent Handovers

| Time             | From     | To        | Task                      | Result      |
| ---------------- | -------- | --------- | ------------------------- | ----------- |
| 2026-02-13 08:45 | OpenCode | -         | Website Research Complete | ✅ Complete |
| 2026-02-13 08:30 | OpenCode | Firecrawl | Job postings scraping     | ✅ Complete |
| 2026-02-13 08:00 | OpenCode | -         | Copywriter Agent Created  | ✅ Complete |
| 2026-02-13 07:45 | OpenCode | -         | Designer Agent Created    | ✅ Complete |
| 2026-02-13 07:30 | OpenCode | -         | Backend CI/CD Created     | ✅ Complete |

---

## Website Redesign Project (2026-02-13)

### Research Completed

- ✅ 23 job postings scraped from Jobs.cz
- ✅ 5 company websites analyzed (Seznam, Grizly, Niceboy, 2N, ČZ)
- ✅ Keyword analysis with pricing data
- ✅ Customer language mapping

### Files Created

| File                                                | Purpose               |
| --------------------------------------------------- | --------------------- |
| `docs/prd-data/scrap/job-summary-table.md`          | Market overview       |
| `docs/prd-data/scrap/job-keywords-analysis.md`      | Keywords + salaries   |
| `docs/prd-data/scrap/copy-draft-from-jobs.md`       | Customer-centric copy |
| `docs/prd-data/scrap/companies/website-analysis.md` | Design trends         |
| `.agents/agents/copywriter.md`                      | Copywriter agent spec |
| `.agents/agents/designer.md`                        | Designer agent spec   |
| `.kilocode/skills/copywriter/`                      | Copywriter skill      |
| `.kilocode/skills/designer/`                        | Designer skill        |
| `backend/Dockerfile`                                | Backend container     |
| `backend/docker-compose.yml`                        | Docker compose        |
| `.github/workflows/backend-ci.yml`                  | Backend CI/CD         |
| `docs/plans/gemini-image-generation.md`             | Image gen plan        |

### Design System (Designer Agent)

- **Colors**: Google-inspired (#4285F4, #EA4335, #FBBC05, #34A853)
- **Effects**: Gradient mesh, glassmorphism, micro-interactions
- **Typography**: Outfit (headings), Plus Jakarta Sans (body)

### Copy Guidelines (Copywriter Agent)

- **Language**: Czech primary, English secondary
- **Style**: Customer language from job postings
- **Avoid**: Technical jargon (MLOps, AEO, ROAS)
- **Use**: "e-commerce", "online reklama", "víc zákazníků"

---

## Provider Fallback System

**Status**: ✅ Implemented
**Last Updated**: 2026-02-13

### LiteLLM Investigation Results

| Issue           | Status           | Resolution      |
| --------------- | ---------------- | --------------- |
| Port 4000       | ❌ Access Denied | Use direct API  |
| Direct Groq API | ✅ Working       | No proxy needed |
| Firecrawl       | ✅ Working       | MCP configured  |

### Verified Groq Models

- `llama-3.3-70b-versatile` ✅
- `llama-3.1-8b-instant` ✅
