# Architecture Design Workflow

## Phase 1: Preparation

1. **Validate Prerequisites**
   - Confirm PRD exists and is approved
   - Verify epics are defined
   - Check UX constraints and requirements
   - Identify project level (BMAD 0-5) to scope depth

2. **Gather Inputs**
   - Read latest PRD and epic roadmap
   - Collect non-functional requirements
   - Document compliance rules and constraints
   - Identify existing assets (repos, diagrams, tech standards)
   - Note integration requirements

3. **Identify Architecture Drivers**
   - List quality attributes (performance, security, scalability, maintainability)
   - Document external constraints (regulatory, technical, business)
   - Map integration points and dependencies

## Phase 2: Analysis

4. **Analyze Requirements**
   - Map functional requirements to architectural components
   - Identify data flows and state management needs
   - Determine integration points with external systems
   - Assess scalability and performance requirements

5. **Design Component Topology**
   - Define major components and their responsibilities
   - Document component relationships and interfaces
   - Design data flow between components
   - Identify shared services and utilities

6. **Technology Selection**
   - Evaluate technology options against drivers
   - Consider team expertise and existing stack
   - Assess long-term maintainability
   - Document alternatives with pros/cons

## Phase 3: Decision Making

7. **Make Key Decisions**
   - For each major decision:
     - State the decision clearly
     - Provide rationale linked to drivers
     - List alternatives considered
     - Document trade-offs
     - Identify risks and mitigations

8. **Create Implementation Guardrails**
   - Define coding standards and patterns
   - Specify testing requirements
   - Document deployment considerations
   - Set monitoring and observability requirements

## Phase 4: Documentation

9. **Generate Architecture Document**
   - Use `assets/decision-architecture-template.md.template`
   - Or use `scripts/generate_architecture.py` if structured data available
   - Include all sections: overview, components, decisions, risks
   - Add diagrams where appropriate

10. **Review and Validate**
    - Walk through checklist in `CHECKLIST.md`
    - Verify traceability from requirements to decisions
    - Confirm feasibility with technical team
    - Check alignment with business goals

## Phase 5: Handoff

11. **Publish and Communicate**
    - Share architecture document with stakeholders
    - Present key decisions and rationale
    - Document follow-up actions
    - Update risk and decision logs

12. **Transition to Next Phase**
    - Hand off to delivery-planning skill
    - Provide context for development-execution skill
    - Document any open questions or dependencies
    - Schedule architecture review checkpoints

## Quality Gates

- **Completeness**: All requirements addressed, no gaps
- **Feasibility**: Technical team confirms implementability
- **Traceability**: Every decision links to requirements
- **Clarity**: Implementation team understands guardrails
- **Alignment**: Architecture supports business goals

## Error Handling

- **Missing Inputs**: Escalate to orchestrator or originating skill
- **Conflicting Requirements**: Document conflict, request clarification
- **Technical Infeasibility**: Propose alternatives, document trade-offs
- **Ambiguity**: Flag for resolution before proceeding
