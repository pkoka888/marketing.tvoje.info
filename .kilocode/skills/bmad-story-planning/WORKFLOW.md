# Story Planning Workflow

## Phase 1: Readiness Check

### Step 1.1: Verify Prerequisites
**Action**: Run `CHECKLIST.md` to confirm all prerequisites are met.

**Checklist Items**:
- [ ] Epics exist and are approved (from bmad-product-planning)
- [ ] Architecture decisions are documented and stable
- [ ] UX assets (wireframes, prototypes) are available when relevant
- [ ] Sprint capacity and delivery cadence are defined

**If Prerequisites Missing**:
- Identify which prerequisite is missing
- Route to responsible skill:
  - Missing epics → bmad-product-planning
  - Missing architecture → bmad-architecture-design
  - Missing UX assets → bmad-ux-design
- Document the blocker in backlog
- Notify orchestrator and stakeholders

**If All Prerequisites Met**:
- Proceed to Phase 2

## Phase 2: Story Creation

### Step 2.1: Prioritize Epics and Stories
**Action**: Analyze epics and prioritize based on value, dependencies, and risk.

**Prioritization Framework**:
1. **Business Value**: Impact on user experience and business goals
2. **Dependencies**: Stories that unblock other work
3. **Risk**: High-risk stories should be done early
4. **Effort**: Quick wins to build momentum

**Output**: Prioritized list of epics and stories with sequencing.

### Step 2.2: Draft Story Files
**Action**: Create or update story markdown files.

**For Each Story**:
1. **Title**: Clear, user-centric title
2. **User Story**: "As a [type of user], I want [goal], so that [benefit]"
3. **Acceptance Criteria**: Testable, unambiguous, complete, valuable
4. **Dependencies**: Explicitly list all dependencies
5. **Prerequisites**: Document required components or services
6. **Test Hooks**: Define unit, integration, and e2e tests
7. **Delivery Signals**: Specify what "done" looks like
8. **References**: Cite upstream epic and architecture decisions

**Story Creation Methods**:
- **Manual**: Use `assets/story-script-template.md.template` as a guide
- **Automated**: Use `scripts/create_story.py` with JSON input

### Step 2.3: Validate Story Quality
**Action**: Ensure each story meets quality standards.

**Quality Checks**:
- [ ] Story aligns with architecture decisions
- [ ] Story references upstream epic
- [ ] Acceptance criteria are testable
- [ ] Dependencies are explicitly listed
- [ ] Test hooks are defined
- [ ] Story is appropriately sized (1-10 days)

**If Quality Issues Found**:
- Refine the story to address issues
- Re-validate after changes

## Phase 3: Backlog Management

### Step 3.1: Create Backlog Summary
**Action**: Generate a backlog summary document.

**Backlog Summary Contents**:
- Prioritized list of stories
- Dependencies between stories
- Blockers and risks
- Sprint sequencing recommendations
- Capacity estimates

### Step 3.2: Map Dependencies
**Action**: Create a dependency graph for stories.

**Dependency Mapping**:
- Identify hard dependencies (must complete before starting)
- Identify soft dependencies (can start but may need rework)
- Identify blocking stories (this story blocks others)
- Sequence stories to minimize waiting time

### Step 3.3: Identify Blockers
**Action**: Document all blockers and risks.

**Blocker Documentation**:
- What is blocked
- Why it's blocked
- Who can unblock it
- Estimated time to unblock

## Phase 4: Sprint Planning

### Step 4.1: Assess Sprint Capacity
**Action**: Determine team capacity for the upcoming sprint.

**Capacity Assessment**:
- Team velocity (stories completed per sprint)
- Available developer days
- Time off or holidays
- Buffer for unexpected work

### Step 4.2: Select Stories for Sprint
**Action**: Choose stories that fit within capacity and address priorities.

**Selection Criteria**:
- Highest priority stories first
- Respect dependencies
- Balance risk and effort
- Include at least one quick win

### Step 4.3: Create Sprint Plan
**Action**: Document the sprint plan with timeline.

**Sprint Plan Contents**:
- Stories in the sprint
- Sequence of work
- Owner for each story
- Expected completion dates
- Dependencies and blockers

## Phase 5: Handoff to Development

### Step 5.1: Review Stories with Development Team
**Action**: Conduct a story review session with developers.

**Review Agenda**:
- Present each story
- Clarify acceptance criteria
- Discuss implementation approach
- Identify technical concerns
- Estimate effort (if not already done)

### Step 5.2: Review Stories with Test Team
**Action**: Conduct a story review session with testers.

**Review Agenda**:
- Review acceptance criteria
- Discuss test approach
- Identify edge cases
- Clarify delivery signals

### Step 5.3: Finalize Sprint Plan
**Action**: Get approval from all stakeholders.

**Approval Checklist**:
- [ ] Development team accepts stories
- [ ] Test team accepts acceptance criteria
- [ ] Stakeholders approve sprint plan
- [ ] All blockers are addressed

### Step 5.4: Handoff to bmad-development-execution
**Action**: Transfer stories to development-execution skill.

**Handoff Package**:
- Story files for the sprint
- Backlog summary
- Dependency graph
- Sprint timeline
- Any additional context or notes

## Phase 6: Monitoring and Updates

### Step 6.1: Track Story Progress
**Action**: Monitor progress of stories in development.

**Tracking Metrics**:
- Stories started
- Stories in progress
- Stories completed
- Stories blocked
- Time spent vs. estimated

### Step 6.2: Update Backlog
**Action**: Keep backlog current as stories progress.

**Update Triggers**:
- Story completed
- Story blocked
- New dependencies discovered
- Priorities change
- Capacity changes

### Step 6.3: Communicate Status
**Action**: Provide regular status updates to stakeholders.

**Communication Cadence**:
- Daily standups (development team)
- Weekly status reports (stakeholders)
- Sprint reviews (end of sprint)
- Backlog grooming (between sprints)

## Error Handling

### Missing Prerequisites
**Symptom**: Epics, architecture, or UX assets are missing.

**Actions**:
1. Identify which prerequisite is missing
2. Route to responsible skill for resolution
3. Document the blocker
4. Notify orchestrator and stakeholders
5. Wait for resolution before proceeding

### Conflicting Architecture
**Symptom**: Story violates architecture decisions or guardrails.

**Actions**:
1. Identify which architecture decision is violated
2. Consult with bmad-architecture-design
3. Refine story to align with architecture
4. Update story references
5. Re-validate story quality

### Unclear Acceptance Criteria
**Symptom**: Acceptance criteria are vague or untestable.

**Actions**:
1. Clarify with product owner
2. Rewrite criteria to be specific and measurable
3. Ensure criteria can be verified through testing
4. Re-validate story quality

### Story Too Large
**Symptom**: Story estimate exceeds 10 days or is too complex.

**Actions**:
1. Break story into smaller, independent stories
2. Ensure each sub-story has clear acceptance criteria
3. Map dependencies between sub-stories
4. Update backlog with new stories

## Quality Gates

### Before Handoff
All of the following must be true:
- [ ] `CHECKLIST.md` passes
- [ ] All stories align with architecture decisions
- [ ] All stories have testable acceptance criteria
- [ ] All stories reference upstream epics
- [ ] Backlog summary is complete and up to date
- [ ] Dependencies are mapped and documented
- [ ] Sprint plan is approved by all stakeholders

### During Sprint
- [ ] Story progress is tracked daily
- [ ] Blockers are identified and communicated immediately
- [ ] Backlog is updated as changes occur
- [ ] Stakeholders receive regular status updates

### After Sprint
- [ ] Completed stories are documented
- [ ] Lessons learned are captured
- [ ] Backlog is groomed for next sprint
- [ ] Sprint review is conducted with all stakeholders

## Integration with Other Skills

### bmad-product-planning
- **Input**: Epics and product requirements
- **Output**: Stories that reference epics
- **Trigger**: When epics are approved and ready for breakdown

### bmad-architecture-design
- **Input**: Architecture decisions and guardrails
- **Output**: Stories that align with architecture
- **Trigger**: When architecture is stable and documented

### bmad-ux-design
- **Input**: UX assets, wireframes, prototypes
- **Output**: Stories that incorporate UX requirements
- **Trigger**: When UX assets are available

### bmad-development-execution
- **Input**: Story files and sprint plan
- **Output**: Completed features and code
- **Trigger**: When stories are approved and ready for development

### bmad-test-strategy
- **Input**: Test hooks from stories
- **Output**: Test plans and test cases
- **Trigger**: When stories are handed off for development

## Success Metrics

### Story Quality
- Percentage of stories that pass quality gates
- Number of stories requiring refinement
- Time from story creation to approval

### Sprint Success
- Percentage of stories completed per sprint
- Accuracy of effort estimates
- Number of blockers discovered during sprint

### Stakeholder Satisfaction
- Development team satisfaction with story clarity
- Test team satisfaction with acceptance criteria
- Stakeholder satisfaction with sprint outcomes
