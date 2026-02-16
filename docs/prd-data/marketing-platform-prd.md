# Product Requirements Document: Marketing Automation Platform (CZ)

**Version:** 1.1
**Date:** 2026-02-13
**Status:** Draft (Updated)
**Target Audience:** Solo Marketers & Small Agencies (1-5 pax) in Czech Republic

---

## 1. Executive Summary

**Problem**: Czech freelance marketers (500+) and small agencies (~100) are overwhelmed by tool fragmentation and administrative tasks. Enterprise tools (HubSpot, Salesforce) are too expensive (€500+/mo) and complex, while simple tools (Mailchimp) lack the "AI orchestration" needed for 2026.

**Solution**: A "Low-Code Orchestration Platform" tailored for the Czech market. It bridges the gap between simple UI and powerful backend automation (Make.com/Python), offering native Shoptet integration and GDPR-safe AI content generation.

**Unique Value Prop**: "The power of a Dev team, in a simple dashboard." (Czech: "Síla vývojářského týmu v jednoduchém dashboardu.")

**Target**: 50 paying customers in first 12 months

---

## 2. User Personas

### Primary: "Honza the Freelancer"

- **Profile**: Manages 5-10 clients (PPC, Social). Needs to report ROI to keep clients.
- **Pain Point**: Spends 10h/week on manual reporting and copy-pasting data between E-shop and Ads.
- **Goal**: Automate reporting and basic content creation to handle more clients.
- **Budget**: €9-29/month

### Secondary: "Small Agency Sarah"

- **Profile**: Owner of a boutique agency (3 employees).
- **Pain Point**: Chaos in deliverables. Junior staff make mistakes in AI prompting.
- **Goal**: Standardized "Recipes" for tasks (e.g., "SEO Article Generation" flow that juniors can't break).
- **Budget**: €49-99/month

---

## 3. Market Validation

### Market Size Estimates

- **Solo Marketers in CZ**: 500-1000 (estimated from Freelancing.eu, LinkedIn)
- **Small Agencies (1-5 people)**: ~100 agencies (from WebTop100)
- **Total Addressable Market (TAM)**: ~500-1000 customers
- **Serviceable Available Market (SAM)**: ~200-400 (solo + small teams actively seeking tools)

### Assumptions to Validate

1. [ ] Survey 50 solo marketers to confirm pain points
2. [ ] Interview 10 small agencies about current tool stack
3. [ ] Test pricing sensitivity with landing page

### Competitive Landscape

| Competitor        | Strengths                | Weaknesses                    | Our Differentiation        |
| ----------------- | ------------------------ | ----------------------------- | -------------------------- |
| **Ecomail**       | Czech-based, email focus | No AI, limited integrations   | AI Content + Multi-channel |
| **SmartEmailing** | Czech support            | Legacy UX, no automation      | Modern UI + AI             |
| **Active24**      | Hosting + email bundle   | Not specialized for marketing | Marketing-first            |
| **Make.com**      | Powerful automation      | Too complex for solo          | Simplified UX              |
| **HubSpot**       | Enterprise features      | Expensive, overkill           | Affordable + Local         |

---

## 4. Product Features (MVP)

### Core Module A: The "Orchestrator" Dashboard

_The central command center that hides complexity._

- **Feature**: Unified view of connected apps (Google Ads, Sklik, Shoptet, Meta).
- **Function**: Displays "Active Flows" (e.g., "Abandoned Cart Recovery running").
- **Requirement**: Must not look like a developer console. Traffic light system (Green/Red status).
- **Status**: MVP - NOT in v1 (Phase 3)

### Core Module B: Czech Market Integrations

_The "Local Hero" advantage._

- **Shoptet Connector**: One-click connect to pull product feeds and order data. (Crucial USP).
- **Sklik Integration**: View spend and performance data alongside Google Ads.
- **Fakturoid/iDoklad**: Auto-generate invoices for agency clients.
- **Status**: MVP - Priority 1

### Core Module C: AI Content Studio ("Safe Mode")

_Generative AI with guardrails._

- **Feature**: "Bring Your Own Key" (OpenAI/Anthropic) or use Platform Credits.
- **GDPR Shield**:
  - Option 1: EU-based AI provider (DeepSeek, Mistral EU)
  - Option 2: PII filtering before US API calls
- **Templates**: Pre-tuned prompts for Czech nuances (tykania/vykania).
- **Status**: MVP - Priority 2

### Core Module D: Executive Reporting

_The "Data Translator"._

- **Feature**: One-click PDF generation.
- **AI Insight**: "Translate this graph into text for a CEO." (e.g., "CPA dropping means we are more efficient.").
- **Status**: MVP - Priority 2

---

## 5. Technical Requirements

### Tech Stack

- **Frontend**: React/Next.js (hosted on Vercel)
- **Backend**: Python FastAPI (wrapper around Make.com webhooks)
- **Database**: PostgreSQL (client data), Redis (cache)
- **Auth**: Supabase Auth or Auth0 (must support MFA)
- **Hosting**: Vercel (Frontend), Railway/DigitalOcean (Backend)

### Architecture

```
Users → React Dashboard → FastAPI → Make.com Webhooks / AI APIs
                                              ↓
                                        PostgreSQL
                                              ↓
                                        Dashboard
```

### MVP Scope (What's NOT in v1)

- [ ] Make.com visual embedding (Phase 3)
- [ ] Custom Python script upload (Phase 3)
- [ ] Full orchestrator dashboard (Phase 3)
- [ ] Multi-tenant complex reporting

### MVP Scope (What's IN v1)

- [ ] User auth & profile
- [ ] Google Ads connector (read-only)
- [ ] Shoptet connector (read-only)
- [ ] Simple dashboard (data aggregation)
- [ ] AI Content Studio with templates
- [ ] PII filter (GDPR shield)
- [ ] Basic PDF report generation

---

## 6. Revenue Model

### Pricing Tiers

| Tier           | Price  | Features                                            | Target         |
| -------------- | ------ | --------------------------------------------------- | -------------- |
| **Free**       | €0     | 1 data source, 5 AI generations/month               | Testing        |
| **Solo**       | €9/mo  | 3 data sources, 50 AI generations, basic reports    | Freelancers    |
| **Team**       | €29/mo | Unlimited data sources, unlimited AI, team features | Small agencies |
| **Enterprise** | Custom | Custom integrations, dedicated support              | Agencies 10+   |

### Revenue Assumptions

- 20% of trial users convert to paid
- Average revenue per user: €15/month
- Target: €6,000 MRR at 400 users

---

## 7. Roadmap

### Phase 1: The "Connector" (Months 1-3)

**Goal**: Validate problem-solution fit

- [ ] User Auth & Profile
- [ ] Connectors: Google Ads, Shoptet (Read-only)
- [ ] Simple Dashboard showing aggregated data
- [ ] Launch landing page with email capture

### Phase 2: The "Creator" (Months 3-6)

**Goal**: Product-market fit

- [ ] AI Content Studio (Text generation)
- [ ] "Safe Mode" PII filter
- [ ] Manual Approval Workflow (Review before post)
- [ ] Basic Reporting (PDF export)
- [ ] Get first 20 paying customers

### Phase 3: The "Orchestrator" (Months 6-12)

**Goal**: Scale

- [ ] Make.com visual embedding (or simplified view)
- [ ] Custom Python script uploading for advanced users
- [ ] Full dashboard with flow monitoring
- [ ] Scale to 50 customers

---

## 8. Success Metrics

| Metric         | Target                                         | Measurement     |
| -------------- | ---------------------------------------------- | --------------- |
| **Activation** | 40% of users connect 2+ data sources in week 1 | Analytics event |
| **Retention**  | 30% of users generate 1+ report/month          | Database query  |
| **Conversion** | 20% free → paid                                | Payment events  |
| **Time Saved** | 5h/month average                               | User survey     |
| **MRR**        | €6,000 at 400 users                            | Stripe/Database |

---

## 9. Risks & Mitigations

| Risk                               | Likelihood | Impact | Mitigation                            |
| ---------------------------------- | ---------- | ------ | ------------------------------------- |
| **Shoptet builds this themselves** | Medium     | High   | Move fast, build community            |
| **Make.com lowers prices**         | Low        | Medium | Focus on UX, not price                |
| **GDPR regulations tighten**       | Medium     | Medium | Use EU-based AI providers             |
| **Low adoption**                   | Medium     | High   | Validate with landing page first      |
| **Technical complexity**           | High       | Medium | MVP scope strict, no over-engineering |

---

## 10. Team & Resources

### Required Roles

- **Frontend Dev**: React/Next.js (can be part-time)
- **Backend Dev**: Python/FastAPI (can be part-time)
- **Product**: Owner (founder)

### External Dependencies

- Shoptet API access (apply for partner program)
- Make.com Enterprise (for webhooks)
- AI providers (OpenAI, DeepSeek)

---

## 11. Next Steps

1. [ ] Create landing page to validate demand
2. [ ] Survey 50 potential users
3. [ ] Apply for Shoptet partner program
4. [ ] Build MVP (Phase 1-2)
5. [ ] Launch to first 20 users

---

_Document Status: Draft v1.1_
_Last Updated: 2026-02-13_
_Author: OpenCode (based on market research)_
