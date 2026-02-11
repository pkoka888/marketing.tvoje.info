# UX Design Workflow

## Phase 1: Discovery & Requirements

### 1.1 Gather Context
- Read PRD sections: user journeys, functional requirements, constraints
- Review architecture notes for technical limitations
- Check for existing brand guidelines or design system
- Identify target personas and their goals

### 1.2 Define Scope
- Clarify which features/surfaces need UX design
- Prioritize based on user impact and complexity
- Identify dependencies between features
- Document any assumptions or constraints

### 1.3 Stakeholder Alignment
- Confirm design goals with stakeholders
- Align on success metrics
- Identify any non-negotiable constraints
- Establish timeline and deliverables

## Phase 2: Information Architecture

### 2.1 Content Organization
- Create site map or navigation structure
- Define content hierarchy and relationships
- Group related content logically
- Plan for growth and scalability

### 2.2 User Flow Design
- Map primary user journeys step-by-step
- Identify decision points and branches
- Document happy paths and edge cases
- Consider error states and recovery paths

### 2.3 State Diagrams
- Define all interaction states (loading, success, error, empty)
- Document transitions between states
- Identify triggers for state changes
- Plan for progressive disclosure

## Phase 3: Wireframing

### 3.1 Low-Fidelity Wireframes
- Create rough sketches for all key screens
- Focus on layout and component placement
- Don't worry about visual details yet
- Iterate quickly based on feedback

### 3.2 Component Structure
- Define reusable components and their variations
- Document component hierarchy and relationships
- Specify content rules for each component
- Plan for responsive behavior

### 3.3 Responsive Planning
- Design mobile-first layouts
- Define breakpoints and layout changes
- Ensure touch targets meet minimum size (44x44px)
- Plan content reflow and adaptation

## Phase 4: Design System

### 4.1 Visual Language
- Define color palette with accessibility contrast ratios
- Establish typography scale and hierarchy
- Specify spacing and layout rules
- Document iconography style

### 4.2 Component Library
- Create specifications for all UI components
- Define variants (primary, secondary, disabled, etc.)
- Document interaction patterns
- Include accessibility requirements

### 4.3 Pattern Documentation
- Document common design patterns (navigation, forms, modals)
- Specify when to use each pattern
- Include implementation guidance
- Link to requirements and user stories

## Phase 5: Interaction Design

### 5.1 Micro-interactions
- Define animations and transitions
- Specify feedback mechanisms (hover, focus, active states)
- Plan for loading states and progress indicators
- Ensure interactions feel responsive and natural

### 5.2 Form Design
- Design form layouts and field groupings
- Specify validation rules and error messages
- Plan for success and error states
- Ensure accessibility (labels, ARIA, keyboard)

### 5.3 Feedback Systems
- Define how users receive confirmation
- Plan for error recovery and guidance
- Specify notification patterns
- Ensure feedback is timely and clear

## Phase 6: Accessibility Review

### 6.1 WCAG Compliance
- Verify color contrast ratios (4.5:1 minimum)
- Ensure keyboard navigation works for all interactions
- Test with screen reader (semantic HTML, ARIA labels)
- Check focus indicators and skip links

### 6.2 Responsive Testing
- Test on mobile devices (320px - 640px)
- Test on tablets (640px - 1024px)
- Test on desktop (1024px+)
- Verify touch targets and content reflow

### 6.3 Usability Validation
- Conduct think-aloud sessions with target users
- Measure task completion rates and times
- Identify confusion points and workarounds
- Gather qualitative feedback

## Phase 7: Documentation & Handoff

### 7.1 Design Rationale
- Document why key decisions were made
- Link design choices to requirements
- Explain trade-offs and alternatives considered
- Provide context for future iterations

### 7.2 Implementation Specs
- Create detailed component specifications
- Include code snippets or pseudo-code where helpful
- Specify responsive behavior and breakpoints
- Document any technical constraints

### 7.3 Asset Organization
- Organize all design assets (images, icons, fonts)
- Use clear, consistent naming conventions
- Include version control for assets
- Provide handoff checklist for developers

## Phase 8: Validation & Iteration

### 8.1 Analytics Planning
- Define success metrics (conversion, engagement, satisfaction)
- Plan analytics instrumentation
- Identify key user flows to track
- Set up A/B testing opportunities

### 8.2 Usability Testing
- Conduct moderated or unmoderated testing
- Test with representative users
- Measure against success criteria
- Document findings and recommendations

### 8.3 Iteration Planning
- Prioritize findings based on impact and effort
- Create backlog of improvements
- Plan for continuous validation
- Establish feedback loop with users

## Quality Gates

### Before Handoff
- [ ] All user flows documented and validated
- [ ] Wireframes cover all required screens
- [ ] Design system is complete and consistent
- [ ] Accessibility requirements are met
- [ ] Responsive behavior is defined
- [ ] Implementation specs are clear
- [ ] Assets are organized and labeled

### After Implementation
- [ ] Conduct usability testing
- [ ] Review analytics data
- [ ] Gather user feedback
- [ ] Identify improvement opportunities
- [ ] Plan next iteration

## Deliverables

### Core Deliverables
1. **User Flows** - Step-by-step journey documentation
2. **Wireframes** - Low-fidelity screen layouts
3. **Design System** - Component library and visual language
4. **Interaction Specs** - State diagrams and behavior definitions
5. **Accessibility Report** - WCAG compliance verification
6. **Implementation Guide** - Developer handoff documentation

### Supporting Documentation
- Design rationale and decision log
- Asset inventory and organization
- Validation plan and success metrics
- Iteration backlog and recommendations

## Common Scenarios

### New Feature Design
1. Review PRD requirements and user stories
2. Create user flows for new feature
3. Design wireframes for affected screens
4. Update design system with new components
5. Document accessibility requirements
6. Create implementation specifications
7. Plan validation and iteration

### Redesign Project
1. Analyze current UX and identify pain points
2. Gather user feedback and analytics data
3. Create new user flows and wireframes
4. Update design system consistently
5. Plan migration strategy
6. Validate with users before implementation
7. Document changes and rationale

### Incremental Improvement
1. Identify specific UX issue to address
2. Design solution for that issue only
3. Test solution in isolation
4. Roll out incrementally
5. Monitor impact and iterate
