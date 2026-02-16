# Comprehensive PRD Template (Based on Claude Code Skill Factory)

## User Input Section

**Preset:** [product-manager / developer / designer]
**Use Case:** [What feature/project to build]
**Mode:** [Core / Detailed / Quick]

---

## Generated Prompt Structure

```xml
<role>
You are a [Senior Product Manager / Engineer / Designer] specializing in [domain]. Your expertise includes [relevant skills].
</role>

<domain>
[Industry] - [Product Type]
</domain>

<objective>
[What to build and why it matters]
</objective>

<context>
**Product Context:**
- Product: [Name] - [Description]
- Platform: [Tech stack]
- Users: [Target users]

**User Feedback:**
- [Quote 1]
- [Quote 2]

**Business Context:**
- [Goal 1]
- [Goal 2]
</context>

<requirements>
<functional_requirements>
1. **[Feature 1]**
   - Description
   - User interaction

2. **[Feature 2]**
   - Description
   - User interaction
</functional_requirements>

<non_functional_requirements>
- Performance: [metrics]
- Security: [requirements]
- Scalability: [requirements]
</non_functional_requirements>

<constraints>
- [Budget/Timeline]
- [Technical constraints]
- [Dependencies]
</constraints>
</requirements>

<output_specifications>
<structure>
1. **Executive Summary**
   - Problem statement
   - Proposed solution
   - Success metrics

2. **Background & Goals**
   - User research findings
   - Business objectives

3. **User Personas & Use Cases**
   - Primary personas
   - Jobs-to-be-done

4. **Requirements**
   - Functional requirements
   - Non-functional requirements
   - Edge cases

5. **User Experience**
   - User flows
   - Wireframes
   - Copy examples

6. **Technical Specifications**
   - System architecture
   - API endpoints
   - Database schema

7. **Success Metrics & Analytics**
   - KPIs
   - Event tracking

8. **Release Plan**
   - Phased rollout
   - Beta testing

9. **Open Questions & Assumptions**
   - Unresolved decisions

10. **Appendix**
    - Research data
    - Technical notes
</structure>

<format>
- Executive summary: [length]
- User stories: "As a [persona], I want [goal], so that [benefit]"
- Acceptance criteria: "Given [context], When [action], Then [outcome]"
</format>

<quality_standards>
- All user stories have clear acceptance criteria
- Edge cases documented
- Success metrics measurable and time-bound
</quality_standards>
</output_specifications>

<workflow>
<phase name="1. Discovery & Research">
**Tasks:**
- [Task 1]
- [Task 2]

**Deliverables:**
- [Deliverable 1]
</phase>

<phase name="2. Requirements Definition">
**Tasks:**
- Define user stories
- Document functional requirements

**Deliverables:**
- Complete user story backlog
- Prioritized feature list
</phase>
</workflow>

<best_practices>
<requirements>
- Write from user perspective
- Include acceptance criteria for every story
- Document "why" not just "what"
</requirements>

<user_experience>
- Design for 80% use case first
- Minimize friction
- Test across contexts
</user_experience>

<technical>
- Consider offline scenarios
- Plan for graceful degradation
- Design for scale
</technical>
</best_practices>

<examples>
<example name="User Story Template">
**User Story:**
As a [persona],
I want [goal],
So that [benefit]

**Acceptance Criteria:**
- Given [context]
- When [action]
- Then [outcome]

**Edge Cases:**
- [Case 1]
- [Case 2]
</example>
</examples>

<success_criteria>
✅ [Metric 1]: [Target]
✅ [Metric 2]: [Target]
</success_criteria>

<validation_checklist>
Before marking complete, verify:
- [ ] User research validates problem and solution
- [ ] Engineering has reviewed
- [ ] Design has reviewed UX
- [ ] All user stories have acceptance criteria
- [ ] Edge cases documented
- [ ] Success metrics measurable
</validation_checklist>
```

---

## Usage for Agents

When creating a new feature PRD, use this template structure and fill in:

1. Role definition based on who is writing the PRD
2. Domain context (industry, product type)
3. Clear objective
4. Product context (name, platform, users)
5. Real user quotes/feedback
6. Business goals
7. Detailed functional & non-functional requirements
8. Constraints (budget, timeline, tech)
9. Desired output structure
10. Workflow phases
11. Best practices relevant to domain
12. Examples as templates
13. Measurable success criteria
14. Validation checklist
