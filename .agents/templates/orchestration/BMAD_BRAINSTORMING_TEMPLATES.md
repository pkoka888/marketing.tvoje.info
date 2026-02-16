# BMAD-Based Brainstorming Templates

**BMAD Framework:** Business, Model, Architecture, Data - A structured approach to systematic thinking and decision-making.

---

## Table of Contents

1. [Project Analysis Template](#1-project-analysis-template)
2. [Decision Making Template](#2-decision-making-template)
3. [Architecture Planning Template](#3-architecture-planning-template)
4. [Feature Prioritization Template](#4-feature-prioritization-template)
5. [Risk Assessment Template](#5-risk-assessment-template)
6. [Technology Selection Template](#6-technology-selection-template)
7. [Roadmap Planning Template](#7-roadmap-planning-template)
8. [Research Integration Template](#8-research-integration-template)

---

## 1. Project Analysis Template

### Overview

Systematically analyze project requirements, stakeholders, constraints, and resources using the BMAD framework to establish a solid foundation for development.

### Step-by-Step Instructions

#### Step 1: Business Analysis

1. Define the business problem or opportunity
2. Identify business goals and objectives
3. Determine success metrics (KPIs)
4. Analyze market context and competition
5. Document business value proposition

#### Step 2: Model Analysis

1. Define the operational model (how the system will be used)
2. Identify user personas and their workflows
3. Map out business processes to be supported
4. Define revenue model (if applicable)
5. Document integration requirements with existing systems

#### Step 3: Architecture Analysis

1. Identify high-level system requirements
2. Determine architectural style (monolith, microservices, etc.)
3. Define non-functional requirements (performance, security, scalability)
4. Identify integration points and dependencies
5. Document technical constraints

#### Step 4: Data Analysis

1. Identify data entities and relationships
2. Define data sources and destinations
3. Determine data volume and velocity requirements
4. Document data privacy and compliance requirements
5. Define data retention and archival policies

### Example Prompts

**Business Analysis:**

```
Analyze the business context for [PROJECT_NAME]:
- What is the primary business problem we're solving?
- Who are the target users and what value do they expect?
- What are the measurable success criteria?
- What is the competitive landscape?
- What is the expected ROI and timeline?
```

**Model Analysis:**

```
Define the operational model for [PROJECT_NAME]:
- Who are the primary user personas?
- What are the key user journeys and workflows?
- How will this system integrate with existing business processes?
- What are the revenue/cost implications?
- What external systems need to be integrated?
```

**Architecture Analysis:**

```
Outline architectural requirements for [PROJECT_NAME]:
- What are the core functional requirements?
- What non-functional requirements are critical (performance, security, availability)?
- What are the technical constraints and limitations?
- What integration points are required?
- What scalability considerations apply?
```

**Data Analysis:**

```
Analyze data requirements for [PROJECT_NAME]:
- What data entities will be managed?
- What are the data sources and destinations?
- What are the expected data volumes and growth rates?
- What compliance requirements apply (GDPR, HIPAA, etc.)?
- What are the data retention and archival needs?
```

### Output Format

```markdown
# Project Analysis: [PROJECT_NAME]

## Business Analysis

### Business Problem

[Description of the problem or opportunity]

### Business Goals

- [Goal 1]
- [Goal 2]
- [Goal 3]

### Success Metrics

| Metric  | Target  | Measurement Method |
| ------- | ------- | ------------------ |
| [KPI 1] | [Value] | [Method]           |
| [KPI 2] | [Value] | [Method]           |

### Market Context

[Analysis of market, competition, positioning]

## Model Analysis

### User Personas

| Persona     | Role   | Goals   | Pain Points   |
| ----------- | ------ | ------- | ------------- |
| [Persona 1] | [Role] | [Goals] | [Pain Points] |

### Key Workflows

1. [Workflow 1 description]
2. [Workflow 2 description]

### Integration Requirements

- [System 1]: [Integration details]
- [System 2]: [Integration details]

## Architecture Analysis

### Functional Requirements

- [FR-001]: [Description]
- [FR-002]: [Description]

### Non-Functional Requirements

| Category    | Requirement   | Priority          |
| ----------- | ------------- | ----------------- |
| Performance | [Requirement] | [High/Medium/Low] |
| Security    | [Requirement] | [High/Medium/Low] |
| Scalability | [Requirement] | [High/Medium/Low] |

### Technical Constraints

- [Constraint 1]
- [Constraint 2]

## Data Analysis

### Data Entities

| Entity     | Attributes   | Relationships   |
| ---------- | ------------ | --------------- |
| [Entity 1] | [Attributes] | [Relationships] |

### Data Sources

- [Source 1]: [Description, format, frequency]
- [Source 2]: [Description, format, frequency]

### Compliance Requirements

- [Regulation]: [Requirements]
```

### Best Practices

1. **Involve stakeholders early** - Get input from all relevant stakeholders during analysis
2. **Document assumptions** - Clearly state any assumptions made during analysis
3. **Prioritize requirements** - Use MoSCoW (Must, Should, Could, Won't) to prioritize
4. **Validate with users** - Confirm understanding with actual users when possible
5. **Keep it iterative** - Revisit and refine analysis as more information becomes available
6. **Use visual aids** - Create diagrams, flowcharts, and user journey maps
7. **Focus on outcomes** - Emphasize business outcomes over technical features
8. **Consider constraints realistically** - Don't underestimate technical, budget, or time constraints

### Common Pitfalls

1. **Skipping stakeholder input** - Making assumptions without consulting actual users
2. **Over-analyzing** - Getting stuck in analysis paralysis
3. **Ignoring constraints** - Underestimating technical, budget, or time limitations
4. **Vague requirements** - Writing requirements that are ambiguous or untestable
5. **Focusing on solutions** - Jumping to technical solutions before understanding the problem
6. **Neglecting non-functional requirements** - Only focusing on functional requirements
7. **Incomplete data analysis** - Overlooking data privacy, compliance, or retention needs
8. **Not documenting decisions** - Failing to record why certain decisions were made

---

## 2. Decision Making Template

### Overview

A structured framework for making informed decisions by defining problems, generating options, establishing evaluation criteria, and using a decision matrix to select the best course of action.

### Step-by-Step Instructions

#### Step 1: Problem Definition

1. Clearly state the decision to be made
2. Identify the context and background
3. Determine the decision scope and boundaries
4. Identify who needs to be involved in the decision
5. Establish the decision timeline

#### Step 2: Option Generation

1. Brainstorm all possible options (no filtering yet)
2. Research and gather information for each option
3. Eliminate clearly infeasible options
4. Refine and detail remaining options
5. Document pros and cons for each option

#### Step 3: Evaluation Criteria

1. Identify key criteria for evaluation
2. Assign weights to each criterion based on importance
3. Define measurement methods for each criterion
4. Establish minimum thresholds for critical criteria
5. Document the scoring system

#### Step 4: Decision Matrix

1. Create a matrix with options as rows and criteria as columns
2. Score each option against each criterion
3. Calculate weighted scores
4. Identify the highest-scoring option
5. Perform sensitivity analysis on weights

### Example Prompts

**Problem Definition:**

```
Define the decision problem for [DECISION_TOPIC]:
- What specific decision needs to be made?
- What is the context and background?
- What are the boundaries of this decision?
- Who are the key stakeholders?
- What is the deadline for this decision?
```

**Option Generation:**

```
Generate options for [DECISION_TOPIC]:
- Brainstorm all possible approaches (aim for 5-10 options)
- Research each option thoroughly
- What are the pros and cons of each option?
- Which options are clearly infeasible and can be eliminated?
- Refine the remaining options with specific details
```

**Evaluation Criteria:**

```
Define evaluation criteria for [DECISION_TOPIC]:
- What criteria are most important for this decision?
- How should each criterion be weighted (1-10 scale)?
- How will each criterion be measured?
- Are there any minimum thresholds that must be met?
- What is the scoring system (e.g., 1-5 scale)?
```

**Decision Matrix:**

```
Create a decision matrix for [DECISION_TOPIC]:
- Score each option against each criterion
- Calculate weighted scores
- Which option has the highest score?
- How sensitive is the result to weight changes?
- What is the recommended decision?
```

### Output Format

```markdown
# Decision Analysis: [DECISION_TOPIC]

## Problem Definition

### Decision Statement

[Clear statement of what decision needs to be made]

### Context

[Background information and context]

### Scope

[Boundaries and limitations of the decision]

### Stakeholders

- [Stakeholder 1]: [Role and interest]
- [Stakeholder 2]: [Role and interest]

### Timeline

- Decision deadline: [Date]
- Implementation timeline: [Timeline]

## Options

### Option 1: [Option Name]

**Description:** [Detailed description]

**Pros:**

- [Pro 1]
- [Pro 2]

**Cons:**

- [Con 1]
- [Con 2]

**Feasibility:** [High/Medium/Low]

### Option 2: [Option Name]

[Same structure as Option 1]

## Evaluation Criteria

| Criterion     | Weight (1-10) | Measurement Method | Minimum Threshold |
| ------------- | ------------- | ------------------ | ----------------- |
| [Criterion 1] | [Weight]      | [Method]           | [Threshold]       |
| [Criterion 2] | [Weight]      | [Method]           | [Threshold]       |

## Decision Matrix

| Option   | [Criterion 1] | [Criterion 2] | [Criterion 3] | Weighted Score |
| -------- | ------------- | ------------- | ------------- | -------------- |
| Option 1 | [Score]       | [Score]       | [Score]       | [Total]        |
| Option 2 | [Score]       | [Score]       | [Score]       | [Total]        |
| Option 3 | [Score]       | [Score]       | [Score]       | [Total]        |

**Scoring System:** [Description of scoring system]

## Analysis

### Recommended Decision

**Option [X]: [Option Name]**

**Rationale:**

- [Reason 1]
- [Reason 2]

### Sensitivity Analysis

[Analysis of how changes in weights affect the outcome]

### Risks and Mitigations

| Risk     | Probability       | Impact            | Mitigation   |
| -------- | ----------------- | ----------------- | ------------ |
| [Risk 1] | [High/Medium/Low] | [High/Medium/Low] | [Mitigation] |

## Next Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]
```

### Best Practices

1. **Separate generation from evaluation** - Don't judge options while brainstorming
2. **Involve diverse perspectives** - Get input from people with different backgrounds
3. **Use objective criteria** - Make criteria as measurable as possible
4. **Document the process** - Keep records of how decisions were made
5. **Consider alternatives** - Always have a backup plan
6. **Test assumptions** - Validate key assumptions before finalizing
7. **Be transparent** - Share the decision process with stakeholders
8. **Review periodically** - Revisit decisions as circumstances change

### Common Pitfalls

1. **Confirmation bias** - Only seeking information that supports a preferred option
2. **Sunk cost fallacy** - Continuing with a decision because of past investments
3. **Analysis paralysis** - Over-analyzing and delaying decisions
4. **Groupthink** - Suppressing dissenting opinions in group settings
5. **Anchoring** - Being overly influenced by the first piece of information
6. **Ignoring opportunity costs** - Not considering what else could be done with resources
7. **Overconfidence** - Underestimating risks and overestimating capabilities
8. **Not defining criteria upfront** - Changing criteria to favor a preferred option

---

## 3. Architecture Planning Template

### Overview

Design system architecture by identifying components, mapping data flow, defining integration points, and planning for scalability using the BMAD framework.

### Step-by-Step Instructions

#### Step 1: System Components

1. Identify all system components (services, modules, databases, etc.)
2. Define responsibilities for each component
3. Determine component boundaries and interfaces
4. Identify shared components and utilities
5. Document component dependencies

#### Step 2: Data Flow

1. Map data entry points and sources
2. Trace data transformation steps
3. Identify data storage locations
4. Document data output and consumption points
5. Define data validation and error handling

#### Step 3: Integration Points

1. Identify external systems and APIs
2. Define integration protocols and formats
3. Determine synchronization requirements
4. Plan for error handling and retries
5. Document authentication and security requirements

#### Step 4: Scalability Considerations

1. Analyze expected load and growth patterns
2. Identify potential bottlenecks
3. Design for horizontal and vertical scaling
4. Plan for caching and performance optimization
5. Define monitoring and alerting requirements

### Example Prompts

**System Components:**

```
Define system components for [SYSTEM_NAME]:
- What are the main functional components needed?
- What are the responsibilities of each component?
- How do components interact with each other?
- What shared components or utilities are needed?
- What are the dependencies between components?
```

**Data Flow:**

```
Map data flow for [SYSTEM_NAME]:
- Where does data enter the system?
- What transformations does data undergo?
- Where is data stored?
- How is data consumed or output?
- How are data validation and errors handled?
```

**Integration Points:**

```
Identify integration points for [SYSTEM_NAME]:
- What external systems need to be integrated?
- What protocols and formats will be used?
- What are the synchronization requirements?
- How will errors and retries be handled?
- What authentication and security measures are needed?
```

**Scalability:**

```
Plan scalability for [SYSTEM_NAME]:
- What are the expected load patterns and growth rates?
- Where are potential bottlenecks?
- How can the system scale horizontally and vertically?
- What caching strategies should be used?
- What monitoring and alerting are needed?
```

### Output Format

```markdown
# Architecture Plan: [SYSTEM_NAME]

## System Components

### Component Diagram

[Insert diagram or ASCII art showing component relationships]

### Component Details

| Component     | Responsibilities   | Interfaces        | Dependencies   |
| ------------- | ------------------ | ----------------- | -------------- |
| [Component 1] | [Responsibilities] | [APIs/Interfaces] | [Dependencies] |
| [Component 2] | [Responsibilities] | [APIs/Interfaces] | [Dependencies] |

### Shared Components

- [Component]: [Description and usage]

## Data Flow

### Data Flow Diagram

[Insert diagram or ASCII art showing data flow]

### Data Sources

| Source     | Type   | Format   | Frequency   | Volume   |
| ---------- | ------ | -------- | ----------- | -------- |
| [Source 1] | [Type] | [Format] | [Frequency] | [Volume] |

### Data Transformations

1. [Transformation 1]: [Description]
2. [Transformation 2]: [Description]

### Data Storage

| Storage     | Type   | Schema   | Retention   | Backup   |
| ----------- | ------ | -------- | ----------- | -------- |
| [Storage 1] | [Type] | [Schema] | [Retention] | [Backup] |

### Data Outputs

| Output     | Destination   | Format   | Frequency   |
| ---------- | ------------- | -------- | ----------- |
| [Output 1] | [Destination] | [Format] | [Frequency] |

## Integration Points

### External Systems

| System     | Purpose   | Protocol   | Authentication | SLA   |
| ---------- | --------- | ---------- | -------------- | ----- |
| [System 1] | [Purpose] | [Protocol] | [Auth Method]  | [SLA] |

### API Specifications

- [API 1]: [Endpoint, method, request/response format]
- [API 2]: [Endpoint, method, request/response format]

### Error Handling

- [Error scenario]: [Handling strategy]
- [Retry policy]: [Description]

## Scalability

### Load Analysis

| Metric         | Current | Peak    | Projected (1yr) | Projected (3yr) |
| -------------- | ------- | ------- | --------------- | --------------- |
| [Users]        | [Value] | [Value] | [Value]         | [Value]         |
| [Requests/sec] | [Value] | [Value] | [Value]         | [Value]         |
| [Data Volume]  | [Value] | [Value] | [Value]         | [Value]         |

### Bottleneck Analysis

| Component   | Current Capacity | Expected Load | Risk Level | Mitigation   |
| ----------- | ---------------- | ------------- | ---------- | ------------ |
| [Component] | [Capacity]       | [Load]        | [Risk]     | [Mitigation] |

### Scaling Strategy

**Horizontal Scaling:**

- [Component]: [Scaling approach]
- [Component]: [Scaling approach]

**Vertical Scaling:**

- [Component]: [Scaling approach]
- [Component]: [Scaling approach]

### Performance Optimization

| Technique   | Component   | Expected Impact | Implementation   |
| ----------- | ----------- | --------------- | ---------------- |
| [Technique] | [Component] | [Impact]        | [Implementation] |

### Monitoring

| Metric   | Component   | Threshold   | Alert   |
| -------- | ----------- | ----------- | ------- |
| [Metric] | [Component] | [Threshold] | [Alert] |
```

### Best Practices

1. **Start simple** - Begin with a simple architecture and evolve as needed
2. **Design for failure** - Assume components will fail and design accordingly
3. **Use standard patterns** - Leverage proven architectural patterns
4. **Document thoroughly** - Keep architecture documentation up to date
5. **Plan for monitoring** - Design observability from the start
6. **Consider security** - Build security into every layer
7. **Think about operations** - Design for deployability and maintainability
8. **Validate early** - Prototype and validate architectural decisions

### Common Pitfalls

1. **Over-engineering** - Building more complexity than needed
2. **Premature optimization** - Optimizing before identifying actual bottlenecks
3. **Ignoring operational concerns** - Focusing only on development, not deployment
4. **Tight coupling** - Creating components that are too interdependent
5. **No monitoring** - Failing to design observability into the system
6. **Ignoring security** - Adding security as an afterthought
7. **Not planning for failure** - Assuming everything will work perfectly
8. **Documentation debt** - Letting architecture documentation become outdated

---

## 4. Feature Prioritization Template

### Overview

Prioritize features using multiple methods including MoSCoW, impact vs effort analysis, user story mapping, and MVP definition to ensure development focuses on the most valuable functionality.

### Step-by-Step Instructions

#### Step 1: MoSCoW Method

1. List all proposed features
2. Categorize each feature as Must, Should, Could, or Won't
3. Define clear criteria for each category
4. Review and validate categorization with stakeholders
5. Document rationale for each categorization

#### Step 2: Impact vs Effort Matrix

1. Assess impact of each feature (business value, user value)
2. Estimate effort required for each feature
3. Plot features on impact vs effort matrix
4. Identify quick wins (high impact, low effort)
5. Identify big bets (high impact, high effort)

#### Step 3: User Story Mapping

1. Create user personas
2. Map user journeys and activities
3. Break down activities into user stories
4. Organize stories by release priority
5. Identify minimum viable product (MVP) slice

#### Step 4: MVP Definition

1. Define core problem being solved
2. Identify essential features for problem solution
3. Determine success criteria for MVP
4. Plan for post-MVP iterations
5. Set timeline and resource constraints

### Example Prompts

**MoSCoW Method:**

```
Apply MoSCoW prioritization to [PROJECT_FEATURES]:
- List all proposed features
- Categorize each as Must, Should, Could, or Won't
- What are the criteria for each category?
- What is the rationale for each categorization?
- Do stakeholders agree with the prioritization?
```

**Impact vs Effort Matrix:**

```
Create impact vs effort analysis for [PROJECT_FEATURES]:
- What is the business impact of each feature?
- What is the user impact of each feature?
- What effort is required for each feature?
- Which features are quick wins?
- Which features are big bets?
```

**User Story Mapping:**

```
Map user stories for [PROJECT]:
- Who are the user personas?
- What are the key user journeys?
- What activities make up each journey?
- What user stories are needed for each activity?
- How should stories be organized by release?
```

**MVP Definition:**

```
Define the MVP for [PROJECT]:
- What is the core problem being solved?
- What features are absolutely essential?
- What are the success criteria for the MVP?
- What features will be added in post-MVP iterations?
- What are the timeline and resource constraints?
```

### Output Format

```markdown
# Feature Prioritization: [PROJECT_NAME]

## MoSCoW Analysis

### MoSCoW Criteria

- **Must Have:** [Criteria definition]
- **Should Have:** [Criteria definition]
- **Could Have:** [Criteria definition]
- **Won't Have:** [Criteria definition]

### Feature Categorization

| Feature     | Category                  | Rationale   | Stakeholder Agreement |
| ----------- | ------------------------- | ----------- | --------------------- |
| [Feature 1] | [Must/Should/Could/Won't] | [Rationale] | [Yes/No/Comments]     |
| [Feature 2] | [Must/Should/Could/Won't] | [Rationale] | [Yes/No/Comments]     |

### Summary

- **Must Have:** [Count] features
- **Should Have:** [Count] features
- **Could Have:** [Count] features
- **Won't Have:** [Count] features

## Impact vs Effort Matrix

### Matrix
```

High Impact
│
│ [Quick Wins] │ [Big Bets]
│ High Impact │ High Impact
│ Low Effort │ High Effort
│ │
────┼──────────────────┼────
│ │
│ [Fill-ins] │ [Money Pit]
│ Low Impact │ Low Impact
│ Low Effort │ High Effort
│
└──────────────────┴─────────────
Low Effort High Effort

```

### Feature Details
| Feature | Business Impact | User Impact | Effort | Quadrant | Priority |
|---------|----------------|-------------|--------|----------|----------|
| [Feature 1] | [High/Medium/Low] | [High/Medium/Low] | [Story Points] | [Quadrant] | [1-N] |

### Recommendations
**Quick Wins (Implement First):**
- [Feature 1]
- [Feature 2]

**Big Bets (Plan Carefully):**
- [Feature 1]
- [Feature 2]

## User Story Mapping
### User Personas
| Persona | Goals | Pain Points | Key Scenarios |
|---------|-------|-------------|---------------|
| [Persona 1] | [Goals] | [Pain Points] | [Scenarios] |

### User Journey Map
**Journey: [Journey Name]**
1. [Step 1]: [Description]
2. [Step 2]: [Description]
3. [Step 3]: [Description]

### Story Backbone
| Release | Activity | User Stories |
|---------|----------|--------------|
| Release 1 | [Activity 1] | [Story 1, Story 2] |
| Release 1 | [Activity 2] | [Story 3, Story 4] |
| Release 2 | [Activity 3] | [Story 5, Story 6] |

### User Stories
**[Story ID]: [Story Title]**
- **As a** [user type]
- **I want** [action]
- **So that** [benefit]
- **Acceptance Criteria:** [Criteria]
- **Priority:** [Must/Should/Could]
- **Estimate:** [Story Points]

## MVP Definition
### Core Problem
[Description of the core problem being solved]

### MVP Features
| Feature | Description | Acceptance Criteria | Priority |
|---------|-------------|---------------------|----------|
| [Feature 1] | [Description] | [Criteria] | Must |
| [Feature 2] | [Description] | [Criteria] | Must |

### Success Criteria
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [Metric 1] | [Target] | [Method] |
| [Metric 2] | [Target] | [Method] |

### Post-MVP Roadmap
**Iteration 1:** [Features and timeline]
**Iteration 2:** [Features and timeline]
**Iteration 3:** [Features and timeline]

### Constraints
- **Timeline:** [MVP delivery date]
- **Budget:** [Budget constraints]
- **Resources:** [Team size and skills]
- **Technical:** [Technical constraints]
```

### Best Practices

1. **Involve stakeholders** - Get input from all relevant stakeholders
2. **Use multiple methods** - Combine different prioritization techniques
3. **Focus on value** - Prioritize based on business and user value
4. **Be realistic** - Consider actual capacity and constraints
5. **Revisit regularly** - Re-prioritize as circumstances change
6. **Document decisions** - Record why features were prioritized
7. **Think in slices** - Plan for incremental delivery
8. **Validate assumptions** - Test assumptions about feature value

### Common Pitfalls

1. **Everything is priority 1** - Failing to make hard trade-offs
2. **Ignoring user needs** - Prioritizing based on internal preferences
3. **Overcommitting** - Planning more than can be delivered
4. **Not revisiting** - Keeping the same priorities despite changing circumstances
5. **Feature creep** - Continuously adding features to the MVP
6. **Ignoring technical debt** - Not allocating time for refactoring and maintenance
7. **Siloed decisions** - Making prioritization decisions without stakeholder input
8. **No clear criteria** - Prioritizing based on gut feel rather than defined criteria

---

## 5. Risk Assessment Template

### Overview

Identify, analyze, and plan for risks by assessing impact, developing mitigation strategies, and creating contingency plans to minimize project disruption.

### Step-by-Step Instructions

#### Step 1: Risk Identification

1. Brainstorm potential risks across all project dimensions
2. Categorize risks (technical, business, operational, etc.)
3. Identify risk triggers and early warning signs
4. Document risk sources and causes
5. Review historical data from similar projects

#### Step 2: Impact Analysis

1. Assess likelihood of each risk occurring
2. Evaluate impact if risk occurs (severity)
3. Calculate risk score (likelihood × impact)
4. Prioritize risks by score
5. Identify risk interdependencies

#### Step 3: Mitigation Strategies

1. Develop strategies for high-priority risks
2. Choose appropriate response type (avoid, mitigate, transfer, accept)
3. Define specific mitigation actions
4. Assign owners and timelines
5. Estimate costs of mitigation

#### Step 4: Contingency Plans

1. Develop fallback plans for critical risks
2. Define trigger conditions for contingency activation
3. Identify resources needed for contingency execution
4. Document communication protocols
5. Plan for post-incident review

### Example Prompts

**Risk Identification:**

```
Identify risks for [PROJECT]:
- What technical risks exist?
- What business risks exist?
- What operational risks exist?
- What are the triggers and warning signs for each risk?
- What historical risks from similar projects should be considered?
```

**Impact Analysis:**

```
Analyze risk impact for [PROJECT]:
- What is the likelihood of each risk occurring?
- What is the impact if each risk occurs?
- What is the risk score for each risk?
- Which risks are highest priority?
- Are there interdependencies between risks?
```

**Mitigation Strategies:**

```
Develop mitigation strategies for [PROJECT_RISKS]:
- What is the appropriate response for each risk (avoid, mitigate, transfer, accept)?
- What specific actions will mitigate each risk?
- Who is responsible for each mitigation?
- What is the timeline for mitigation?
- What are the costs of mitigation?
```

**Contingency Plans:**

```
Create contingency plans for [PROJECT_RISKS]:
- What fallback plans exist for critical risks?
- What triggers activate each contingency plan?
- What resources are needed for contingency execution?
- How will stakeholders be communicated with?
- How will incidents be reviewed post-occurrence?
```

### Output Format

```markdown
# Risk Assessment: [PROJECT_NAME]

## Risk Identification

### Risk Categories

**Technical Risks:**

- [Risk 1]: [Description]
- [Risk 2]: [Description]

**Business Risks:**

- [Risk 1]: [Description]
- [Risk 2]: [Description]

**Operational Risks:**

- [Risk 1]: [Description]
- [Risk 2]: [Description]

**External Risks:**

- [Risk 1]: [Description]
- [Risk 2]: [Description]

### Risk Register

| ID   | Risk               | Category   | Source   | Trigger   | Warning Signs |
| ---- | ------------------ | ---------- | -------- | --------- | ------------- |
| R001 | [Risk description] | [Category] | [Source] | [Trigger] | [Signs]       |
| R002 | [Risk description] | [Category] | [Source] | [Trigger] | [Signs]       |

## Impact Analysis

### Risk Matrix
```

Impact
High │ Medium │ High │ Critical
│ │ │
────┼─────────────┼─────────────┼────────────
Med │ Low │ Medium │ High
│ │ │
────┼─────────────┼─────────────┼────────────
Low │ Low │ Low │ Medium
│ │ │
└─────────────┴─────────────┴────────────
Low Medium High
Likelihood

```

### Risk Scoring
| ID | Risk | Likelihood (1-5) | Impact (1-5) | Score | Priority |
|----|------|------------------|--------------|-------|----------|
| R001 | [Risk] | [1-5] | [1-5] | [Score] | [Priority] |
| R002 | [Risk] | [1-5] | [1-5] | [Score] | [Priority] |

### Risk Interdependencies
| Risk | Depends On | Impacts | Relationship |
|------|------------|---------|--------------|
| [Risk A] | [Risk B] | [Risk C] | [Description] |

## Mitigation Strategies
### High Priority Risks
**Risk: [Risk Name]**
- **Response Strategy:** [Avoid/Mitigate/Transfer/Accept]
- **Mitigation Actions:**
  1. [Action 1]
  2. [Action 2]
- **Owner:** [Name/Role]
- **Timeline:** [Dates]
- **Cost:** [Estimated cost]
- **Status:** [Not Started/In Progress/Complete]

### Mitigation Summary
| Risk | Strategy | Actions | Owner | Timeline | Cost | Status |
|------|----------|---------|-------|----------|------|--------|
| R001 | [Strategy] | [Actions] | [Owner] | [Timeline] | [Cost] | [Status] |

## Contingency Plans
### Critical Risk Contingencies
**Risk: [Risk Name]**
- **Trigger Condition:** [Condition that activates plan]
- **Contingency Actions:**
  1. [Action 1]
  2. [Action 2]
- **Resources Required:** [Resources]
- **Communication Protocol:**
  - [Stakeholder]: [Message and timing]
- **Post-Incident Review:** [Review process]

### Contingency Activation Flow
```

[Risk Occurs] → [Trigger Detected] → [Plan Activated] → [Actions Executed] → [Review]

```

## Risk Monitoring
### Monitoring Schedule
| Risk | Monitoring Method | Frequency | Owner |
|------|-------------------|-----------|-------|
| R001 | [Method] | [Frequency] | [Owner] |
| R002 | [Method] | [Frequency] | [Owner] |

### Key Risk Indicators
| Indicator | Risk | Threshold | Current Status |
|-----------|------|-----------|----------------|
| [KRI 1] | [Risk] | [Threshold] | [Status] |

## Risk Review
### Review Schedule
- **Weekly Review:** [Team members]
- **Monthly Review:** [Stakeholders]
- **Quarterly Review:** [Executive team]

### Last Review
- **Date:** [Date]
- **Attendees:** [Names]
- **Decisions:** [Decisions made]
- **Action Items:** [Items to address]
```

### Best Practices

1. **Be comprehensive** - Consider risks from all angles
2. **Involve the team** - Get input from diverse perspectives
3. **Be realistic** - Don't underestimate risks
4. **Prioritize** - Focus on high-impact, high-likelihood risks
5. **Plan for the unknown** - Include contingency for unforeseen events
6. **Monitor continuously** - Regularly review and update risk assessments
7. **Learn from experience** - Use lessons learned to improve future assessments
8. **Communicate openly** - Share risk information with stakeholders

### Common Pitfalls

1. **Optimism bias** - Underestimating likelihood and impact of risks
2. **Ignoring low-probability risks** - Dismissing risks that seem unlikely
3. **Not updating** - Failing to revisit and update risk assessments
4. **No ownership** - Not assigning clear responsibility for risks
5. **Vague mitigation** - Creating generic, non-actionable mitigation plans
6. **Ignoring interdependencies** - Not considering how risks affect each other
7. **No contingency** - Not having backup plans for critical risks
8. **Poor communication** - Not sharing risk information with stakeholders

---

## 6. Technology Selection Template

### Overview

Evaluate and select technologies by matching requirements to capabilities, analyzing costs, assessing learning curves, and evaluating community support.

### Step-by-Step Instructions

#### Step 1: Requirements vs Capabilities

1. Document technical requirements
2. Identify candidate technologies
3. Map requirements to technology capabilities
4. Identify gaps and workarounds
5. Score technologies against requirements

#### Step 2: Cost Analysis

1. Identify all cost categories (licensing, infrastructure, maintenance)
2. Estimate costs for each technology option
3. Calculate total cost of ownership (TCO)
4. Consider both upfront and ongoing costs
5. Factor in hidden costs (training, migration)

#### Step 3: Learning Curve

1. Assess team's current skills
2. Evaluate learning resources availability
3. Estimate time to proficiency
4. Identify training needs
5. Plan knowledge transfer

#### Step 4: Community Support

1. Evaluate community size and activity
2. Assess documentation quality
3. Check for commercial support options
4. Review issue resolution patterns
5. Evaluate long-term viability

### Example Prompts

**Requirements vs Capabilities:**

```
Match requirements to capabilities for [TECHNOLOGY_DECISION]:
- What are the technical requirements?
- What are the candidate technologies?
- How well does each technology meet each requirement?
- What gaps exist and what workarounds are available?
- How does each technology score against requirements?
```

**Cost Analysis:**

```
Analyze costs for [TECHNOLOGY_OPTIONS]:
- What are the licensing costs for each option?
- What are the infrastructure costs?
- What are the maintenance costs?
- What is the total cost of ownership?
- What hidden costs should be considered?
```

**Learning Curve:**

```
Assess learning curve for [TECHNOLOGY_OPTIONS]:
- What are the team's current skills?
- What learning resources are available?
- How long will it take to reach proficiency?
- What training is needed?
- How will knowledge be transferred?
```

**Community Support:**

```
Evaluate community support for [TECHNOLOGY_OPTIONS]:
- How large and active is the community?
- What is the quality of documentation?
- Are commercial support options available?
- How are issues typically resolved?
- What is the long-term viability?
```

### Output Format

```markdown
# Technology Selection: [DECISION_NAME]

## Requirements vs Capabilities

### Technical Requirements

| Requirement | Priority            | Description   | Success Criteria |
| ----------- | ------------------- | ------------- | ---------------- |
| [Req 1]     | [Must/Should/Could] | [Description] | [Criteria]       |
| [Req 2]     | [Must/Should/Could] | [Description] | [Criteria]       |

### Candidate Technologies

| Technology | Type   | Version   | License   |
| ---------- | ------ | --------- | --------- |
| [Tech 1]   | [Type] | [Version] | [License] |
| [Tech 2]   | [Type] | [Version] | [License] |

### Capability Matrix

| Requirement | [Tech 1]      | [Tech 2]      | [Tech 3]      |
| ----------- | ------------- | ------------- | ------------- |
| [Req 1]     | [Score/Notes] | [Score/Notes] | [Score/Notes] |
| [Req 2]     | [Score/Notes] | [Score/Notes] | [Score/Notes] |

### Gaps and Workarounds

| Technology | Gap   | Workaround   | Effort   |
| ---------- | ----- | ------------ | -------- |
| [Tech 1]   | [Gap] | [Workaround] | [Effort] |

### Scoring Summary

| Technology | Total Score | Rank   |
| ---------- | ----------- | ------ |
| [Tech 1]   | [Score]     | [Rank] |
| [Tech 2]   | [Score]     | [Rank] |

## Cost Analysis

### Cost Categories

| Category               | [Tech 1]   | [Tech 2]   | [Tech 3]   |
| ---------------------- | ---------- | ---------- | ---------- |
| Licensing              | [Cost]     | [Cost]     | [Cost]     |
| Infrastructure         | [Cost]     | [Cost]     | [Cost]     |
| Development            | [Cost]     | [Cost]     | [Cost]     |
| Maintenance            | [Cost]     | [Cost]     | [Cost]     |
| Training               | [Cost]     | [Cost]     | [Cost]     |
| Migration              | [Cost]     | [Cost]     | [Cost]     |
| **Total (Year 1)**     | **[Cost]** | **[Cost]** | **[Cost]** |
| **Total (3-Year TCO)** | **[Cost]** | **[Cost]** | **[Cost]** |

### Cost Breakdown Details

**[Technology Name]**

- **Licensing:** [Details]
- **Infrastructure:** [Details]
- **Development:** [Details]
- **Maintenance:** [Details]
- **Training:** [Details]
- **Migration:** [Details]

### Hidden Costs

| Cost Type | Description   | Impact   |
| --------- | ------------- | -------- |
| [Cost 1]  | [Description] | [Impact] |

## Learning Curve

### Current Team Skills

| Skill     | Team Proficiency | Required Level | Gap   |
| --------- | ---------------- | -------------- | ----- |
| [Skill 1] | [Current]        | [Required]     | [Gap] |

### Learning Resources

| Technology | Documentation | Tutorials      | Courses        | Community |
| ---------- | ------------- | -------------- | -------------- | --------- |
| [Tech 1]   | [Quality]     | [Availability] | [Availability] | [Quality] |
| [Tech 2]   | [Quality]     | [Availability] | [Availability] | [Quality] |

### Time to Proficiency

| Technology | Basic   | Intermediate | Advanced | Expert  |
| ---------- | ------- | ------------ | -------- | ------- |
| [Tech 1]   | [Weeks] | [Weeks]      | [Weeks]  | [Weeks] |
| [Tech 2]   | [Weeks] | [Weeks]      | [Weeks]  | [Weeks] |

### Training Plan

**[Technology Name]**

- **Training Needed:** [Description]
- **Training Method:** [Method]
- **Timeline:** [Timeline]
- **Budget:** [Budget]
- **Resources:** [Resources]

## Community Support

### Community Metrics

| Technology | Community Size | Activity Level | GitHub Stars | Contributors |
| ---------- | -------------- | -------------- | ------------ | ------------ |
| [Tech 1]   | [Size]         | [Level]        | [Stars]      | [Count]      |
| [Tech 2]   | [Size]         | [Level]        | [Stars]      | [Count]      |

### Documentation Quality

| Technology | Getting Started | API Reference | Tutorials | Examples |
| ---------- | --------------- | ------------- | --------- | -------- |
| [Tech 1]   | [Rating]        | [Rating]      | [Rating]  | [Rating] |
| [Tech 2]   | [Rating]        | [Rating]      | [Rating]  | [Rating] |

### Commercial Support

| Technology | Support Available | Support Types | Cost   | SLA   |
| ---------- | ----------------- | ------------- | ------ | ----- |
| [Tech 1]   | [Yes/No]          | [Types]       | [Cost] | [SLA] |
| [Tech 2]   | [Yes/No]          | [Types]       | [Cost] | [SLA] |

### Issue Resolution

| Technology | Avg Response Time | Resolution Rate | Common Issues |
| ---------- | ----------------- | --------------- | ------------- |
| [Tech 1]   | [Time]            | [Rate]          | [Issues]      |
| [Tech 2]   | [Time]            | [Rate]          | [Issues]      |

### Long-term Viability

| Technology | Age     | Release Frequency | Backing        | Roadmap  |
| ---------- | ------- | ----------------- | -------------- | -------- |
| [Tech 1]   | [Years] | [Frequency]       | [Organization] | [Status] |
| [Tech 2]   | [Years] | [Frequency]       | [Organization] | [Status] |

## Recommendation

### Selected Technology

**[Technology Name]**

### Rationale

1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

### Key Benefits

- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

### Key Risks

- [Risk 1]
- [Risk 2]
- [Risk 3]

### Mitigation Plan

- [Mitigation 1]
- [Mitigation 2]

### Next Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]
```

### Best Practices

1. **Define requirements first** - Don't evaluate technologies without clear requirements
2. **Consider total cost** - Look beyond initial licensing costs
3. **Evaluate realistically** - Be honest about team skills and learning needs
4. **Check community health** - Active communities indicate long-term viability
5. **Prototype before committing** - Build proof-of-concepts for top contenders
6. **Consider the ecosystem** - Look at related tools and integrations
7. **Plan for the future** - Consider scalability and evolution needs
8. **Document the decision** - Record why the technology was selected

### Common Pitfalls

1. **Technology for technology's sake** - Choosing technologies because they're trendy
2. **Ignoring team skills** - Selecting technologies the team can't effectively use
3. **Underestimating costs** - Not considering total cost of ownership
4. **Overlooking licensing** - Not understanding license implications
5. **Ignoring community** - Choosing technologies with inactive communities
6. **No prototyping** - Committing without hands-on evaluation
7. **Short-term thinking** - Not considering long-term maintenance and evolution
8. **Analysis paralysis** - Over-analyzing and delaying decisions

---

## 7. Roadmap Planning Template

### Overview

Create a comprehensive project roadmap by defining phases and milestones, mapping dependencies, allocating resources, and establishing success metrics.

### Step-by-Step Instructions

#### Step 1: Phases and Milestones

1. Define project phases based on logical groupings
2. Identify key milestones for each phase
3. Establish phase dependencies
4. Set target dates for each milestone
5. Define phase exit criteria

#### Step 2: Dependencies

1. Identify internal dependencies between tasks
2. Identify external dependencies (third parties, systems)
3. Map dependency relationships
4. Identify critical path
5. Plan for dependency risks

#### Step 3: Resource Allocation

1. Identify required resources (people, tools, infrastructure)
2. Assign resources to phases and tasks
3. Identify resource constraints and conflicts
4. Plan for resource ramp-up and ramp-down
5. Budget for resource costs

#### Step 4: Success Metrics

1. Define metrics for each phase
2. Establish measurement methods
3. Set targets and thresholds
4. Plan for metric collection and reporting
5. Define success criteria for the overall project

### Example Prompts

**Phases and Milestones:**

```
Define phases and milestones for [PROJECT]:
- What are the logical phases of the project?
- What are the key milestones for each phase?
- What are the dependencies between phases?
- What are the target dates for each milestone?
- What are the exit criteria for each phase?
```

**Dependencies:**

```
Map dependencies for [PROJECT]:
- What are the internal dependencies between tasks?
- What are the external dependencies?
- What is the critical path?
- What are the dependency risks?
- How will dependency risks be mitigated?
```

**Resource Allocation:**

```
Plan resource allocation for [PROJECT]:
- What resources are needed (people, tools, infrastructure)?
- How will resources be assigned to phases and tasks?
- What are the resource constraints and conflicts?
- How will resources be ramped up and down?
- What is the budget for resources?
```

**Success Metrics:**

```
Define success metrics for [PROJECT]:
- What metrics will measure each phase's success?
- How will metrics be measured?
- What are the targets and thresholds?
- How will metrics be collected and reported?
- What are the overall project success criteria?
```

### Output Format

```markdown
# Roadmap: [PROJECT_NAME]

## Phases and Milestones

### Phase Overview

| Phase     | Description   | Duration   | Start Date | End Date |
| --------- | ------------- | ---------- | ---------- | -------- |
| [Phase 1] | [Description] | [Duration] | [Date]     | [Date]   |
| [Phase 2] | [Description] | [Duration] | [Date]     | [Date]   |

### Phase Details

**Phase 1: [Phase Name]**

- **Description:** [Detailed description]
- **Objectives:**
  - [Objective 1]
  - [Objective 2]
- **Deliverables:**
  - [Deliverable 1]
  - [Deliverable 2]
- **Milestones:**
  | Milestone | Target Date | Dependencies | Status |
  |-----------|-------------|--------------|--------|
  | [Milestone 1] | [Date] | [Dependencies] | [Status] |
  | [Milestone 2] | [Date] | [Dependencies] | [Status] |
- **Exit Criteria:**
  - [Criterion 1]
  - [Criterion 2]
- **Risks:** [Risks]

### Timeline Visualization
```

[Timeline visualization - Gantt chart or similar]

```

## Dependencies
### Dependency Map
| Task | Depends On | Blocks | Type | Risk Level |
|------|------------|--------|------|------------|
| [Task A] | [Task X, Task Y] | [Task B, Task C] | [Internal/External] | [High/Medium/Low] |
| [Task B] | [Task A] | [Task D] | [Internal/External] | [High/Medium/Low] |

### Critical Path
**Critical Path Tasks:**
1. [Task 1] → [Task 2] → [Task 3] → [Task 4]
- **Total Duration:** [Duration]
- **Buffer:** [Buffer time]

### External Dependencies
| Dependency | Owner | Type | Commitment | Risk | Mitigation |
|------------|-------|------|------------|------|------------|
| [Dependency 1] | [Owner] | [Type] | [Commitment] | [Risk] | [Mitigation] |

### Dependency Risks
| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| [Risk 1] | [High/Medium/Low] | [High/Medium/Low] | [Mitigation] | [Contingency] |

## Resource Allocation
### Resource Requirements
| Resource Type | Quantity | Skills | Phase | Cost |
|---------------|----------|--------|-------|------|
| [Resource 1] | [Quantity] | [Skills] | [Phase(s)] | [Cost] |
| [Resource 2] | [Quantity] | [Skills] | [Phase(s)] | [Cost] |

### Team Allocation
| Role | Person | Phase | Allocation % | Responsibilities |
|------|--------|-------|--------------|------------------|
| [Role 1] | [Name] | [Phase] | [%] | [Responsibilities] |
| [Role 2] | [Name] | [Phase] | [%] | [Responsibilities] |

### Resource Timeline
```

[Resource allocation over time visualization]

```

### Resource Constraints
| Constraint | Impact | Mitigation |
|------------|--------|------------|
| [Constraint 1] | [Impact] | [Mitigation] |
| [Constraint 2] | [Impact] | [Mitigation] |

### Budget
| Category | Phase 1 | Phase 2 | Phase 3 | Total |
|----------|---------|---------|---------|-------|
| Personnel | [Cost] | [Cost] | [Cost] | [Cost] |
| Infrastructure | [Cost] | [Cost] | [Cost] | [Cost] |
| Tools & Licenses | [Cost] | [Cost] | [Cost] | [Cost] |
| Training | [Cost] | [Cost] | [Cost] | [Cost] |
| Contingency | [Cost] | [Cost] | [Cost] | [Cost] |
| **Total** | **[Cost]** | **[Cost]** | **[Cost]** | **[Cost]** |

## Success Metrics
### Phase Metrics
**Phase 1: [Phase Name]**
| Metric | Target | Measurement Method | Frequency | Owner |
|--------|--------|-------------------|-----------|-------|
| [Metric 1] | [Target] | [Method] | [Frequency] | [Owner] |
| [Metric 2] | [Target] | [Method] | [Frequency] | [Owner] |

### Overall Project Metrics
| Metric | Target | Measurement Method | Frequency | Owner |
|--------|--------|-------------------|-----------|-------|
| [Metric 1] | [Target] | [Method] | [Frequency] | [Owner] |
| [Metric 2] | [Target] | [Method] | [Frequency] | [Owner] |

### Success Criteria
**Project Success Criteria:**
- [Criterion 1]: [Description and measurement]
- [Criterion 2]: [Description and measurement]
- [Criterion 3]: [Description and measurement]

### Metric Dashboard
| Metric | Current | Target | Status | Trend |
|--------|---------|--------|--------|-------|
| [Metric 1] | [Value] | [Target] | [Status] | [Trend] |
| [Metric 2] | [Value] | [Target] | [Status] | [Trend] |

## Governance
### Review Schedule
| Review Type | Frequency | Participants | Purpose |
|-------------|-----------|--------------|---------|
| [Daily Standup] | [Daily] | [Team] | [Purpose] |
| [Weekly Review] | [Weekly] | [Team + Leads] | [Purpose] |
| [Phase Gate] | [Per Phase] | [Stakeholders] | [Purpose] |

### Decision Making
| Decision Type | Approver | Criteria | Timeline |
|---------------|----------|----------|----------|
| [Type 1] | [Approver] | [Criteria] | [Timeline] |
| [Type 2] | [Approver] | [Criteria] | [Timeline] |

### Communication Plan
| Audience | Frequency | Method | Content |
|----------|-----------|--------|---------|
| [Audience 1] | [Frequency] | [Method] | [Content] |
| [Audience 2] | [Frequency] | [Method] | [Content] |

## Risk Management
### Roadmap Risks
| Risk | Phase | Probability | Impact | Mitigation | Owner |
|------|-------|-------------|--------|------------|-------|
| [Risk 1] | [Phase] | [High/Medium/Low] | [High/Medium/Low] | [Mitigation] | [Owner] |

### Contingency Plans
| Scenario | Trigger | Response | Timeline |
|----------|---------|----------|----------|
| [Scenario 1] | [Trigger] | [Response] | [Timeline] |
```

### Best Practices

1. **Be realistic** - Set achievable dates and milestones
2. **Include buffers** - Build in contingency time for unexpected issues
3. **Plan for dependencies** - Identify and manage dependencies early
4. **Monitor progress** - Regularly track and report on roadmap progress
5. **Be flexible** - Be prepared to adjust the roadmap as needed
6. **Communicate clearly** - Keep stakeholders informed of progress and changes
7. **Celebrate milestones** - Recognize achievements to maintain momentum
8. **Learn and adapt** - Use lessons learned to improve future roadmaps

### Common Pitfalls

1. **Overly optimistic timelines** - Setting unrealistic dates
2. **Ignoring dependencies** - Not accounting for task dependencies
3. **No buffers** - Not including contingency time
4. **Resource conflicts** - Over-allocating resources
5. **Poor communication** - Not keeping stakeholders informed
6. **Rigidity** - Not being willing to adjust the roadmap
7. **No metrics** - Not measuring progress or success
8. **Scope creep** - Continuously adding to the roadmap without adjustment

---

## 8. Research Integration Template

### Overview

Integrate research findings into project planning by researching existing solutions, conducting build vs buy analysis, developing adaptation strategies, and creating customization plans.

### Step-by-Step Instructions

#### Step 1: Existing Solutions Research

1. Identify relevant existing solutions in the market
2. Research open-source alternatives
3. Evaluate commercial products
4. Analyze competitor approaches
5. Document findings and comparisons

#### Step 2: Build vs Buy Analysis

1. Define requirements for the solution
2. Estimate build costs (time, resources, maintenance)
3. Evaluate buy options (licensing, integration, customization)
4. Consider hybrid approaches
5. Make recommendation with rationale

#### Step 3: Adaptation Strategy

1. Identify gaps between existing solutions and requirements
2. Determine adaptation approach (configure, extend, replace)
3. Plan integration with existing systems
4. Assess technical feasibility
5. Define adaptation timeline

#### Step 4: Customization Plan

1. Identify customization requirements
2. Prioritize customizations
3. Design customization architecture
4. Plan customization implementation
5. Define maintenance and upgrade strategy

### Example Prompts

**Existing Solutions Research:**

```
Research existing solutions for [PROBLEM_DOMAIN]:
- What commercial solutions exist in the market?
- What open-source alternatives are available?
- How do competitors approach this problem?
- What are the strengths and weaknesses of each solution?
- How do solutions compare to our requirements?
```

**Build vs Buy Analysis:**

```
Conduct build vs buy analysis for [SOLUTION_NEED]:
- What are the requirements for the solution?
- What are the estimated costs to build (time, resources, maintenance)?
- What are the buy options (licensing, integration, customization)?
- Are there hybrid approaches to consider?
- What is the recommended approach and why?
```

**Adaptation Strategy:**

```
Develop adaptation strategy for [EXISTING_SOLUTION]:
- What are the gaps between the existing solution and our requirements?
- What is the best adaptation approach (configure, extend, replace)?
- How will the solution integrate with existing systems?
- What are the technical feasibility considerations?
- What is the timeline for adaptation?
```

**Customization Plan:**

```
Create customization plan for [SOLUTION]:
- What customizations are required?
- How should customizations be prioritized?
- What is the customization architecture?
- How will customizations be implemented?
- How will customizations be maintained and upgraded?
```

### Output Format

```markdown
# Research Integration: [PROJECT_NAME]

## Existing Solutions Research

### Market Overview

| Solution     | Type                     | Vendor   | License   | Pricing   |
| ------------ | ------------------------ | -------- | --------- | --------- |
| [Solution 1] | [Commercial/Open Source] | [Vendor] | [License] | [Pricing] |
| [Solution 2] | [Commercial/Open Source] | [Vendor] | [License] | [Pricing] |

### Solution Analysis

**[Solution Name]**

- **Type:** [Commercial/Open Source]
- **Vendor:** [Vendor name]
- **Description:** [Description]
- **Key Features:**
  - [Feature 1]
  - [Feature 2]
- **Strengths:**
  - [Strength 1]
  - [Strength 2]
- **Weaknesses:**
  - [Weakness 1]
  - [Weakness 2]
- **Technical Requirements:** [Requirements]
- **Integration Capabilities:** [Capabilities]
- **Community/Support:** [Details]
- **Maturity:** [Maturity level]
- **Last Updated:** [Date]

### Comparison Matrix

| Feature/Criteria | [Solution 1] | [Solution 2] | [Solution 3] | Our Requirements |
| ---------------- | ------------ | ------------ | ------------ | ---------------- |
| [Feature 1]      | [Support]    | [Support]    | [Support]    | [Required]       |
| [Feature 2]      | [Support]    | [Support]    | [Support]    | [Required]       |

### Competitor Analysis

| Competitor     | Solution Used | Approach   | Strengths   | Weaknesses   |
| -------------- | ------------- | ---------- | ----------- | ------------ |
| [Competitor 1] | [Solution]    | [Approach] | [Strengths] | [Weaknesses] |

### Research Findings

**Key Insights:**

1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

**Recommendations:**

- [Recommendation 1]
- [Recommendation 2]

## Build vs Buy Analysis

### Requirements

| Requirement | Priority            | Description   | Success Criteria |
| ----------- | ------------------- | ------------- | ---------------- |
| [Req 1]     | [Must/Should/Could] | [Description] | [Criteria]       |
| [Req 2]     | [Must/Should/Could] | [Description] | [Criteria]       |

### Build Analysis

**Estimated Costs:**
| Cost Category | Estimate | Notes |
|---------------|----------|-------|
| Development | [Cost] | [Notes] |
| Testing | [Cost] | [Notes] |
| Documentation | [Cost] | [Notes] |
| Maintenance (Year 1) | [Cost] | [Notes] |
| **Total (Year 1)** | **[Cost]** | |
| **Total (3-Year)** | **[Cost]** | |

**Timeline:**
| Phase | Duration | Start | End |
|-------|----------|-------|-----|
| [Phase 1] | [Duration] | [Date] | [Date] |
| [Phase 2] | [Duration] | [Date] | [Date] |

**Resource Requirements:**
| Role | Quantity | Duration | Cost |
|------|----------|----------|------|
| [Role 1] | [Quantity] | [Duration] | [Cost] |

**Pros:**

- [Pro 1]
- [Pro 2]

**Cons:**

- [Con 1]
- [Con 2]

### Buy Analysis

**Option 1: [Solution Name]**
| Cost Category | Estimate | Notes |
|---------------|----------|-------|
| License | [Cost] | [Notes] |
| Implementation | [Cost] | [Notes] |
| Training | [Cost] | [Notes] |
| Maintenance (Year 1) | [Cost] | [Notes] |
| **Total (Year 1)** | **[Cost]** | |
| **Total (3-Year)** | **[Cost]** | |

**Requirements Coverage:**
| Requirement | Supported | Gap | Workaround |
|-------------|-----------|-----|------------|
| [Req 1] | [Yes/No/Partial] | [Gap] | [Workaround] |
| [Req 2] | [Yes/No/Partial] | [Gap] | [Workaround] |

**Pros:**

- [Pro 1]
- [Pro 2]

**Cons:**

- [Con 1]
- [Con 2]

### Comparison

| Factor        | Build    | Buy [Option 1] | Buy [Option 2] |
| ------------- | -------- | -------------- | -------------- |
| Initial Cost  | [Cost]   | [Cost]         | [Cost]         |
| Time to Value | [Time]   | [Time]         | [Time]         |
| Customization | [Level]  | [Level]        | [Level]        |
| Maintenance   | [Effort] | [Effort]       | [Effort]       |
| Control       | [Level]  | [Level]        | [Level]        |
| Risk          | [Level]  | [Level]        | [Level]        |

### Recommendation

**Recommended Approach:** [Build/Buy/Hybrid]

**Rationale:**

1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

**Selected Solution:** [Solution name if buy]

## Adaptation Strategy

### Gap Analysis

| Requirement | Existing Solution | Gap               | Priority          |
| ----------- | ----------------- | ----------------- | ----------------- |
| [Req 1]     | [Support level]   | [Gap description] | [High/Medium/Low] |
| [Req 2]     | [Support level]   | [Gap description] | [High/Medium/Low] |

### Adaptation Approach

**Strategy:** [Configure/Extend/Replace/Hybrid]

**Approach Details:**

- [Detail 1]
- [Detail 2]
- [Detail 3]

### Integration Plan

| System     | Integration Type | Effort   | Timeline   |
| ---------- | ---------------- | -------- | ---------- |
| [System 1] | [Type]           | [Effort] | [Timeline] |
| [System 2] | [Type]           | [Effort] | [Timeline] |

### Technical Feasibility

| Aspect     | Feasibility       | Concerns   | Mitigation   |
| ---------- | ----------------- | ---------- | ------------ |
| [Aspect 1] | [High/Medium/Low] | [Concerns] | [Mitigation] |
| [Aspect 2] | [High/Medium/Low] | [Concerns] | [Mitigation] |

### Adaptation Timeline

| Phase     | Activities   | Duration   | Dependencies   |
| --------- | ------------ | ---------- | -------------- |
| [Phase 1] | [Activities] | [Duration] | [Dependencies] |
| [Phase 2] | [Activities] | [Duration] | [Dependencies] |

## Customization Plan

### Customization Requirements

| Customization     | Description   | Priority          | Complexity        |
| ----------------- | ------------- | ----------------- | ----------------- |
| [Customization 1] | [Description] | [High/Medium/Low] | [High/Medium/Low] |
| [Customization 2] | [Description] | [High/Medium/Low] | [High/Medium/Low] |

### Prioritization

**Phase 1 Customizations:**

- [Customization 1]
- [Customization 2]

**Phase 2 Customizations:**

- [Customization 3]
- [Customization 4]

### Customization Architecture
```

[Architecture diagram or description]

```

**Design Principles:**
- [Principle 1]
- [Principle 2]

### Implementation Plan
| Customization | Approach | Owner | Timeline | Dependencies |
|---------------|----------|-------|----------|--------------|
| [Customization 1] | [Approach] | [Owner] | [Timeline] | [Dependencies] |

### Maintenance Strategy
**Upgrade Path:**
- [Strategy for handling upgrades]

**Customization Preservation:**
- [Method for preserving customizations during upgrades]

**Documentation:**
- [Documentation requirements]

**Testing:**
- [Testing strategy for customizations]

### Risk Mitigation
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | [High/Medium/Low] | [High/Medium/Low] | [Mitigation] |
| [Risk 2] | [High/Medium/Low] | [High/Medium/Low] | [Mitigation] |

## Next Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Appendices
### Appendix A: Detailed Solution Evaluations
[Detailed evaluations of each solution]

### Appendix B: Vendor Contact Information
| Solution | Contact | Email | Phone |
|----------|---------|-------|-------|
| [Solution 1] | [Name] | [Email] | [Phone] |

### Appendix C: Proof of Concept Results
[Results from any proof of concept testing]

### Appendix D: References
- [Reference 1]
- [Reference 2]
```

### Best Practices

1. **Thorough research** - Don't skip or rush the research phase
2. **Consider multiple options** - Evaluate at least 3-4 alternatives
3. **Be objective** - Avoid bias toward build or buy
4. **Consider total cost** - Look beyond initial costs to TCO
5. **Validate with stakeholders** - Get input from all relevant stakeholders
6. **Plan for integration** - Don't underestimate integration complexity
7. **Think long-term** - Consider maintenance, upgrades, and evolution
8. **Document everything** - Keep detailed records of research and decisions

### Common Pitfalls

1. **Insufficient research** - Not thoroughly evaluating options
2. **Build bias** - Automatically preferring to build without proper analysis
3. **Buy bias** - Automatically preferring to buy without proper analysis
4. **Ignoring integration** - Underestimating integration complexity
5. **Short-term thinking** - Focusing only on initial costs
6. **Over-customization** - Customizing too much, creating maintenance burden
7. **No upgrade strategy** - Not planning for how to handle vendor upgrades
8. **Stakeholder misalignment** - Not getting buy-in from all stakeholders

---

## Using These Templates

### General Guidelines

1. **Start with the right template** - Choose the template that best matches your current need
2. **Customize as needed** - Adapt templates to fit your specific context
3. **Iterate and refine** - Templates are living documents - update them as you learn
4. **Share with the team** - Ensure everyone understands how to use the templates
5. **Store centrally** - Keep templates in a shared, accessible location
6. **Version control** - Track changes to templates over time
7. **Gather feedback** - Continuously improve templates based on usage
8. **Train the team** - Ensure team members know how to use templates effectively

### Template Selection Guide

| Situation                      | Recommended Template(s)                     |
| ------------------------------ | ------------------------------------------- |
| Starting a new project         | Project Analysis, Risk Assessment           |
| Making a technical decision    | Decision Making, Technology Selection       |
| Designing system architecture  | Architecture Planning, Technology Selection |
| Planning features              | Feature Prioritization, User Story Mapping  |
| Identifying and managing risks | Risk Assessment                             |
| Choosing technologies          | Technology Selection, Decision Making       |
| Planning project timeline      | Roadmap Planning, Feature Prioritization    |
| Evaluating existing solutions  | Research Integration, Build vs Buy Analysis |

### Combining Templates

Many projects benefit from using multiple templates together:

**For a new project:**

1. Project Analysis → Understand requirements and context
2. Risk Assessment → Identify and plan for risks
3. Feature Prioritization → Determine what to build
4. Technology Selection → Choose the right tools
5. Architecture Planning → Design the system
6. Roadmap Planning → Create implementation plan

**For a technical decision:**

1. Decision Making → Structure the decision process
2. Technology Selection → Evaluate options
3. Risk Assessment → Consider risks of each option

**For evaluating solutions:**

1. Research Integration → Research existing solutions
2. Build vs Buy Analysis → Compare approaches
3. Decision Making → Make the final decision

---

## BMAD Framework Reference

### Business (B)

- **Focus:** Business goals, value proposition, market context
- **Questions:**
  - What problem are we solving?
  - Who are our customers/users?
  - What is the business value?
  - How will we measure success?
  - What are the competitive dynamics?

### Model (M)

- **Focus:** Operational model, workflows, user journeys
- **Questions:**
  - How will the system be used?
  - What are the key workflows?
  - Who are the user personas?
  - How does this fit into existing processes?
  - What are the integration requirements?

### Architecture (A)

- **Focus:** System design, components, technical approach
- **Questions:**
  - What are the system components?
  - How do components interact?
  - What are the technical requirements?
  - What are the constraints and limitations?
  - How will the system scale?

### Data (D)

- **Focus:** Data entities, flows, storage, governance
- **Questions:**
  - What data do we need?
  - Where does data come from?
  - How is data transformed?
  - Where is data stored?
  - What are the compliance requirements?

---

## Template Maintenance

### Version History

| Version | Date   | Changes         | Author   |
| ------- | ------ | --------------- | -------- |
| 1.0     | [Date] | Initial version | [Author] |

### Improvement Log

| Date   | Improvement   | Impact   |
| ------ | ------------- | -------- |
| [Date] | [Description] | [Impact] |

### Feedback

To provide feedback or suggest improvements:

- [Contact method]
- [Feedback process]

---

_This document is part of the BMAD Brainstorming Templates collection. For more information, see the project documentation._
