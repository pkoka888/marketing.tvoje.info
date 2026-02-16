# Mission Brief: Marketing Automation Platform Development

**Date**: 2026-02-13
**Orchestrator**: Antigravity (Gemini 3 Pro)
**Executor**: Groq (via LiteLLM)
**Project**: Marketing Automation Platform for Czech Market

---

## Mission Statement

Build a low-code marketing automation platform for solo marketers and small agencies in Czech Republic, using BMAD-METHOD orchestration with Gemini as orchestrator and Groq as implementation engine.

---

## Background

### Problem Space

- 500+ solo marketers in Czech Republic overwhelmed by tool fragmentation
- Enterprise tools (HubSpot) too expensive (€500+/mo)
- Simple tools (Mailchimp) lack AI capabilities
- No Czech-localized solution exists

### Solution

A "Low-Code Orchestration Platform" with:

- Shoptet integration (local USP)
- AI Content Studio with GDPR shield
- Simple dashboard for non-technical users
- €9-29/month pricing

### Market Research Complete

- ✅ PRD updated: `docs/prd-data/marketing-platform-prd.md`
- ✅ Competitive analysis
- ✅ User personas defined
- ✅ Pricing model defined

---

## Mission Parameters

### Constraints

- **Budget**: ~$50 total (Groq is cheap)
- **Timeline**: 16 weeks to launch
- **Team**: Gemini (orchestration) + Groq (implementation)
- **Tech Stack**: Next.js, FastAPI, PostgreSQL, Supabase

### Quality Gates

1. Phase approval required before progression
2. All code tested before commit
3. Security review before launch

---

## Execution Protocol

### Step 1: Start LiteLLM

```bash
python litellm/start_litellm.py
```

### Step 2: Verify Groq

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "groq/llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "test"}]}'
```

### Step 3: Begin Phase 0

- Survey 50 potential users
- Build landing page
- Validate pricing

---

## Phase Breakdown

| Phase | Duration    | Focus          | Cost |
| ----- | ----------- | -------------- | ---- |
| 0     | Week 1      | Validation     | $2   |
| 1     | Weeks 2-3   | PRD & Research | $3   |
| 2     | Weeks 4-6   | Architecture   | $5   |
| 3     | Weeks 7-14  | Implementation | $30  |
| 4     | Weeks 15-16 | Launch         | $5   |
| 5     | Ongoing     | Iterate        | $5   |

---

## Deliverables Required

### Phase 0

- [ ] Survey results (20+ responses)
- [ ] Landing page live

### Phase 1

- [ ] Final PRD approved
- [ ] MVP scope defined

### Phase 2

- [ ] System architecture document
- [ ] Database schema
- [ ] API specification

### Phase 3

- [ ] Working MVP
- [ ] 20 beta users

### Phase 4

- [ ] Public launch
- [ ] First 5 paying customers

---

## Key Contacts

| Role                  | Responsibility                                 |
| --------------------- | ---------------------------------------------- |
| Gemini (Orchestrator) | High-level decisions, research, approval gates |
| Groq (Executor)       | Code implementation, file creation, testing    |

---

## Success Metrics

| Metric               | Target |
| -------------------- | ------ |
| Beta Users           | 20     |
| Paid Users (Month 4) | 20     |
| MRR (Month 6)        | €6,000 |
| NPS                  | >40    |

---

## Immediate Next Steps

1. **Start LiteLLM**: `python litellm/start_litellm.py`
2. **Verify Groq**: Test API connection
3. **Begin Phase 0**: Market validation survey
4. **Create Landing Page**: Simple waitlist page

---

_Mission Brief v1.0_
_Ready for Gemini Orchestration_
