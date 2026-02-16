# BMAD Marketing Automation Platform - Orchestrated Roadmap

**Project**: Marketing Automation Platform (CZ)
**Orchestrator**: Antigravity (Gemini 3 Pro)
**Implementation**: Groq (llama-3.3-70b-versatile)
**Date**: 2026-02-13
**Status**: PLAN (Ready for Gemini Execution)

---

## Executive Summary

This roadmap uses BMAD-METHOD v6.0.0-Beta.8 to orchestrate the Marketing Automation Platform project. Antigravity (Gemini 3 Pro) serves as the orchestrator, delegating research and implementation tasks to Groq via LiteLLM.

**Workflow**: Research → PRD → Architecture → Implementation → QA

---

## Phase 0: Foundation (Week 1)

**Objective**: Validate problem-solution fit with market research

### Tasks

| Task | Agent  | Action                             | Output         |
| ---- | ------ | ---------------------------------- | -------------- |
| T0.1 | Gemini | Research: Survey 50 solo marketers | Survey results |
| T0.2 | Groq   | Build landing page                 | live URL       |
| T0.3 | Gemini | Analyze pricing sensitivity        | Report         |
| T0.4 | Groq   | Set up Shoptet partner application | Submitted      |

### Approval Gate

- [ ] Minimum 20 survey responses
- [ ] Landing page live
- [ ] Go/no-go decision

---

## Phase 1: Discovery & PRD (Weeks 2-3)

**Objective**: Complete product requirements with market validation

### Tasks

| Task | Agent  | Action                          | Output                                  |
| ---- | ------ | ------------------------------- | --------------------------------------- |
| T1.1 | Gemini | Finalize user personas          | docs/prd-data/personas.md               |
| T1.2 | Gemini | Competitive analysis deep-dive  | docs/prd-data/competitive-matrix.md     |
| T1.3 | Groq   | Update PRD with validation data | docs/prd-data/marketing-platform-prd.md |
| T1.4 | Gemini | Define MVP scope                | docs/prd-data/mvp-scope.md              |

### Deliverables

| Artifact      | Path                                      | Status  |
| ------------- | ----------------------------------------- | ------- |
| Updated PRD   | `docs/prd-data/marketing-platform-prd.md` | Ready   |
| User Personas | `docs/prd-data/personas.md`               | Pending |
| MVP Scope     | `docs/prd-data/mvp-scope.md`              | Pending |

### Approval Gate

- [ ] PRD approved by stakeholder
- [ ] MVP scope defined
- [ ] Technical feasibility confirmed

---

## Phase 2: Architecture & Design (Weeks 4-6)

**Objective**: Define technical architecture and UX design

### Tasks

| Task | Agent  | Action                     | Output                        |
| ---- | ------ | -------------------------- | ----------------------------- |
| T2.1 | Gemini | System architecture design | docs/architecture/system.md   |
| T2.2 | Groq   | Database schema design     | docs/architecture/database.md |
| T2.3 | Gemini | UX wireframes (Figma)      | Figma link                    |
| T2.4 | Groq   | API specification          | docs/architecture/api-spec.md |
| T2.5 | Gemini | Security & GDPR design     | docs/architecture/security.md |

### Deliverables

| Artifact            | Path                            | Status  |
| ------------------- | ------------------------------- | ------- |
| System Architecture | `docs/architecture/system.md`   | Pending |
| Database Schema     | `docs/architecture/database.md` | Pending |
| API Spec            | `docs/architecture/api-spec.md` | Pending |

### Approval Gate

- [ ] Architecture approved
- [ ] Security review passed
- [ ] MVP scope fits within budget

---

## Phase 3: Implementation - MVP (Weeks 7-14)

**Objective**: Build MVP ready for first users

### Sprint 1: Foundation (Weeks 7-8)

| Task | Agent | Action                   | Output           |
| ---- | ----- | ------------------------ | ---------------- |
| S1.1 | Groq  | Set up Next.js project   | Repo initialized |
| S1.2 | Groq  | Implement Supabase Auth  | Auth working     |
| S1.3 | Groq  | Create PostgreSQL schema | DB ready         |
| S1.4 | Groq  | Set up CI/CD pipeline    | GitHub Actions   |

### Sprint 2: Connectors (Weeks 9-10)

| Task | Agent | Action                   | Output               |
| ---- | ----- | ------------------------ | -------------------- |
| S2.1 | Groq  | Google Ads API connector | Integration complete |
| S2.2 | Groq  | Shoptet API connector    | Integration complete |
| S2.3 | Groq  | Simple dashboard view    | UI working           |

### Sprint 3: AI Content Studio (Weeks 11-12)

| Task | Agent | Action                 | Output          |
| ---- | ----- | ---------------------- | --------------- |
| S3.1 | Groq  | AI Content Studio UI   | Interface ready |
| S3.2 | Groq  | OpenAI integration     | API connected   |
| S3.3 | Groq  | PII filter (GDPR)      | Shield working  |
| S3.4 | Groq  | Czech prompt templates | Templates ready |

### Sprint 4: Reporting (Weeks 13-14)

| Task | Agent | Action               | Output        |
| ---- | ----- | -------------------- | ------------- |
| S4.1 | Groq  | PDF report generator | Feature ready |
| S4.2 | Groq  | AI Insights          | Feature ready |
| S4.3 | Groq  | User onboarding flow | UX complete   |

### Approval Gate

- [ ] MVP builds without errors
- [ ] All features functional
- [ ] 20 beta users recruited

---

## Phase 4: Launch (Weeks 15-16)

**Objective**: Release to first customers

| Task | Agent  | Action                | Output         |
| ---- | ------ | --------------------- | -------------- |
| T4.1 | Gemini | Marketing copy        | Campaign ready |
| T4.2 | Groq   | Landing page (public) | Live           |
| T4.3 | Groq   | Analytics setup       | Tracking ready |
| T4.4 | Gemini | Launch announcement   | Published      |

### Success Metrics

| Metric          | Target   | Measurement |
| --------------- | -------- | ----------- |
| Beta Signups    | 20 users | Database    |
| Activation Rate | 40%      | Analytics   |
| First Paid      | 5 users  | Stripe      |

---

## Phase 5: Iterate (Ongoing)

**Objective**: Product-market fit and scale

| Milestone          | Target     | Timeline |
| ------------------ | ---------- | -------- |
| 20 Paid Users      | €2,000 MRR | Month 4  |
| 50 Paid Users      | €6,000 MRR | Month 6  |
| Product-Market Fit | NPS > 40   | Month 6  |

---

## Agent Delegation Protocol

### For Gemini (Orchestrator)

```
When delegating to Groq:
1. Use LiteLLM proxy: http://localhost:4000
2. Model: groq/llama-3.3-70b-versatile
3. Provide clear context from PRD
4. Set specific acceptance criteria
5. Validate output before proceeding
```

### For Groq (Implementation)

```
When receiving task:
1. Read relevant PRD/artifacts
2. Implement according to specs
3. Run tests if applicable
4. Report completion with evidence
5. If blocked, report with context
```

---

## Cost Budget

| Phase     | Estimated Cost | Model        |
| --------- | -------------- | ------------ |
| Phase 0-2 | ~$10           | Groq (cheap) |
| Phase 3   | ~$30           | Groq         |
| Phase 4   | ~$5            | Groq         |
| **Total** | **~$45**       |              |

**Note**: Gemini used sparingly for high-value decisions only.

---

## Files & Templates

| Template         | Location                                        |
| ---------------- | ----------------------------------------------- |
| Standard Roadmap | `.agents/templates/roadmap/standard-roadmap.md` |
| PRD Template     | `.agents/templates/prd/detailed-prd.md`         |
| BMAD Agents      | `_bmad/bmm/agents/`                             |
| BMAD Workflows   | `_bmad/bmm/workflows/`                          |

---

## Execution Notes

1. **Start with Phase 0**: Validate before building
2. **Use Groq for implementation**: It's fast and cheap
3. **Use Gemini for decisions**: High-value architectural choices
4. **Gate each phase**: Don't proceed without approval
5. **Track metrics**: From day 1

---

_Plan Status: READY FOR EXECUTION_
_Next Step: Begin Phase 0 - Market Validation_
