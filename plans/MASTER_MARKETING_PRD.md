# MASTER PRODUCT REQUIREMENTS DOCUMENT (PRD)

## Fresh & Premium Marketing Portfolio v1.0

---

## 1. Vision & Strategy

### 1.1 Vision Statement

For Czech and international businesses seeking data-driven marketing growth who struggle to find agencies that combine creative excellence with technical precision, the **Fresh Marketing Portfolio** is a premium agency showcase that delivers compelling case studies, transparent results, and a modern digital experience. Unlike traditional creative agencies that overemphasize aesthetics or "tech shops" that lack brand sensibility, our product uniquely bridges creative storytelling with marketing automation expertise.

### 1.2 Mission

Empower potential clients to make informed decisions by showcasing real campaign results, explaining our strategic approach, and demonstrating the measurable impact of our work.

### 1.3 Strategic Pillars

| Pillar                    | Description                                                                   |
| ------------------------- | ----------------------------------------------------------------------------- |
| **Creative Excellence**   | Award-worthy visual design that builds trust through "Design Taste".          |
| **Results Transparency**  | Metrics-driven case studies with real ROI (ROI%, ROAS, CAC).                  |
| **Technical Credibility** | Showcasing automation/AI capabilities as a _multiplier_, not a core identity. |
| **Local Market Focus**    | Deep Czech market expertise blended with Silicon Valley standards.            |

---

## 2. Problem Statement

### 2.1 Core Problems

1. **Identity Confusion**: Current site reads as "DevOps/Technical".
2. **Content Mismatch**: Terminology is too "code-heavy" (e.g., CI/CD, migration).
3. **Visual Vibe**: Current design is "Cold/Blue/Generic Tech".
4. **Value Clarity**: Value proposition is hidden behind technical jargon.

### 2.2 Target Audience

- **Czech SMEs**: €50K-500K revenue (Needs: Local trust, transparent pricing).
- **International SaaS**: B2B, scaling phase (Needs: English, technical CRM/Email automation proof).
- **Enterprise**: €1M+ revenue (Needs: Scale, multi-market strategies, ROI dashboards).

---

## 3. Goals & Success Criteria

### 3.1 Strategic Goals

- **G1: Identity Shift**: 100% "Agency" vibe by end of Phase 1.
- **G2: Content Refresh**: Bilingual copy for all 6 core sections.
- **G3: Design Upgrade**: Modern animations + "Fresh" palette (Orange/Purple).
- **G4: Lead Gen**: Build funnel for 50+ monthly qualified leads.

### 3.2 North Star Metric

**Monthly Qualified Lead Submissions (Contact Form + Calendly)**

### 3.3 Success Criteria Checklist

- [ ] Hero section communicates "Marketing Agency" in < 3 seconds.
- [ ] Bilingual (CS/EN) toggle functional and translated.
- [ ] 3+ Case Studies with verifyable ROI metrics.
- [ ] Lighthouse Performance ≥ 90.
- [ ] LCP < 2.0s for mobile users.

---

## 4. Requirement Specifications

### 4.1 Functional Requirements (MoSCoW)

#### [MUST] FR-01: Agency Hero Section

- **Headline**: High-impact marketing copy (e.g., "Digital Growth, Quantified").
- **Subheadline**: Bridging Strategy, Creative, and Automation.
- **CTA**: "View Results" -> Scrolls to Case Studies.
- **Visual**: High-end abstract or agency-life imagery (Generated via AI).

#### [MUST] FR-02: Results-First Case Studies

- **Structure**: Challenge → Strategy → Execution → **The Numbers**.
- **Metrics**: ROAS, CAC reduction, Growth %.
- **Format**: MDX for easy content management.

#### [MUST] FR-03: Services (Boutique Approach)

- **Creative**: Content strategy, High-tier Visual design.
- **Automation**: Email (Klaviyo), CRM (HubSpot), AI Workflows.
- **Performance**: Meta Ads, TikTok Ads, Google Search.

#### [SHOULD] FR-04: Specialized Marketing Blog

- **Focus**: 2026 Trends (AEO - Answer Engine Optimization).
- **Format**: SEO-optimized long-form content.

---

## 5. Technical Context (Optimized)

### 5.1 Architecture Stack

| Layer         | Technology                      | Status                                 |
| ------------- | ------------------------------- | -------------------------------------- |
| **Core**      | Astro 5.0                       | RETAIN (Best in class performance)     |
| **Styles**    | Tailwind CSS 4.0                | UPGRADE (Native CSS vars, performance) |
| **Animation** | Astro View Transitions + Motion | ADD (For "Fresh" feel)                 |
| **Content**   | MDX + Content Layer             | RETAIN                                 |

### 5.2 Key Modification Areas

- **`tailwind.config.mjs`**: Inject "Fresh" palette.
- **`src/i18n/`**: Full purge of "DevOps" dictionaries.
- **`src/components/sections/`**: Rebuild Hero, About, Services as "Premium" components.
- **`src/content/projects/`**: Delete old .mdx files; replace with Marketing data.

---

## 6. Roadmap (6-Week Sprint)

| Phase             | Duration | Deliverables                                             |
| ----------------- | -------- | -------------------------------------------------------- |
| **1: Foundation** | Week 1-2 | New Visual Identity, Hero/About rebuild, Content Purge.  |
| **2: Proof**      | Week 3-4 | Case Study implementation, ROI Dashboards, Testimonials. |
| **3: Convince**   | Week 5-6 | Blog (AEO focus), Lead Gen forms, SEO Audit.             |

---

## 7. Metrics & Analytics

- **Plausible**: Zero-cookie privacy tracking.
- **Formspree**: Lead capture integration.
- **Lighthouse CI**: Automated performance/A11Y gating.

---

_Created by Antigravity AI Orchestrator based on BMAD v2026 methodology_
