# Story Planning Reference

## Core Concepts

### User Story Format
A user story follows the standard format:
```
As a [type of user],
I want [goal],
So that [benefit].
```

### Acceptance Criteria
Acceptance criteria must be:
- **Testable**: Can be verified through automated or manual testing
- **Unambiguous**: Clear and specific, no room for interpretation
- **Complete**: Covers all aspects of the story
- **Valuable**: Delivers measurable value to the user

### Story Size
Stories should be sized appropriately:
- **Small**: 1-2 days of work
- **Medium**: 3-5 days of work
- **Large**: 6-10 days of work (consider splitting)

### Dependencies
Types of dependencies:
- **Hard dependency**: Must be completed before this story can start
- **Soft dependency**: Can start but may need rework
- **Blocking**: This story blocks other stories

### Delivery Signals
Clear indicators that a story is complete:
- All acceptance criteria pass
- Code is reviewed and approved
- Tests pass (unit, integration, e2e)
- Documentation is updated
- Feature is deployed to staging

## Story Template

The story template (`assets/story-script-template.md.template`) includes:
- Title and ID
- User story statement
- Acceptance criteria
- Dependencies
- Prerequisites
- Test hooks
- Delivery signals
- References to epic and architecture decisions

## Backlog Management

### Prioritization Framework
Stories are prioritized based on:
1. **Business value**: Impact on user experience and business goals
2. **Dependencies**: Stories that unblock other work
3. **Risk**: High-risk stories should be done early
4. **Effort**: Quick wins to build momentum

### Sprint Planning
Sprint planning considers:
- Team capacity (velocity)
- Story dependencies
- Risk mitigation
- Stakeholder priorities

## Quality Standards

### Story Quality
Every story must:
- Align with architecture decisions
- Reference upstream epic
- Include test hooks
- Define clear acceptance criteria
- List dependencies explicitly

### Backlog Quality
The backlog must:
- Be prioritized and sequenced
- Show dependencies between stories
- Identify blockers
- Be realistic about capacity

## Common Patterns

### Epic to Story Breakdown
When breaking down an epic:
1. Identify user journeys within the epic
2. Group related functionality into stories
3. Ensure stories are independent where possible
4. Sequence stories to minimize dependencies

### Handling Dependencies
When stories have dependencies:
- Document the dependency clearly
- Consider if the dependency can be removed
- Sequence stories to minimize waiting time
- Communicate blockers early

### Story Refinement
During story refinement:
- Clarify acceptance criteria
- Identify missing dependencies
- Estimate effort accurately
- Ensure testability

## Tools and Scripts

### create_story.py
The `scripts/create_story.py` script automates story creation from JSON input:
- Validates required fields
- Generates story markdown from template
- Creates file in appropriate location
- Updates backlog summary

### Usage Example
```bash
python scripts/create_story.py story.json
```

Where `story.json` contains:
```json
{
  "title": "User Authentication",
  "story": "As a user, I want to log in so that I can access my account",
  "acceptance_criteria": [
    "User can enter email and password",
    "System validates credentials",
    "User is redirected to dashboard on success"
  ],
  "dependencies": ["user-registration"],
  "prerequisites": ["auth-service"],
  "test_hooks": ["unit", "integration"],
  "epic": "user-management",
  "architecture_refs": ["auth-architecture"]
}
```

## Integration with Other Skills

### bmad-product-planning
- Consumes epics from product-planning
- References epic IDs in stories
- Aligns stories with product vision

### bmad-architecture-design
- References architecture decisions in stories
- Ensures stories align with guardrails
- Identifies architectural dependencies

### bmad-ux-design
- Incorporates UX assets into stories
- References wireframes and prototypes
- Ensures stories meet UX requirements

### bmad-development-execution
- Hands off stories for implementation
- Provides context for developers
- Tracks story completion status

## Best Practices

### Story Writing
- Write from the user's perspective
- Focus on value, not implementation details
- Keep stories small and manageable
- Ensure stories are testable

### Backlog Management
- Keep backlog visible and up to date
- Prioritize based on value and dependencies
- Communicate changes to stakeholders
- Review and refine backlog regularly

### Sprint Planning
- Be realistic about capacity
- Account for uncertainty
- Leave buffer for unexpected work
- Focus on completing stories, not starting them

## Common Pitfalls

### Too Large Stories
- **Problem**: Stories that are too large are hard to estimate and complete
- **Solution**: Break down into smaller, independent stories

### Unclear Acceptance Criteria
- **Problem**: Vague criteria lead to disputes and rework
- **Solution**: Make criteria specific, measurable, and testable

### Missing Dependencies
- **Problem**: Hidden dependencies cause delays and rework
- **Solution**: Explicitly list all dependencies and prerequisites

### Ignoring Architecture
- **Problem**: Stories that violate architecture cause technical debt
- **Solution**: Reference architecture decisions and align with guardrails
