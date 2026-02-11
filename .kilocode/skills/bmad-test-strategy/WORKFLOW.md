# Quality Assurance Workflow

## Phase 1: Prerequisites Check

1. **Confirm inputs available**
   - PRD and epics exist (from product-requirements skill)
   - Architecture decisions documented (from architecture-design skill)
   - Story backlog defined (from story-planning skill)
   - Existing quality assets identified

2. **Run checklist**
   - Complete all items in `CHECKLIST.md`
   - Document any gaps or blockers

3. **Escalate if missing**
   - Request specific missing artifacts
   - Do not proceed without prerequisites

## Phase 2: Risk Assessment

1. **Analyze requirements**
   - Identify critical user journeys
   - Map failure modes and impact
   - Assess regulatory/compliance needs

2. **Prioritize risks**
   - High: Security, data privacy, compliance
   - Medium: Performance, reliability, usability
   - Low: Cosmetic, edge cases

3. **Define mitigation**
   - Test strategies for high-risk areas
   - Monitoring and alerting
   - Rollback procedures

## Phase 3: Test Strategy Authoring

1. **Use test strategy template**
   - Fill in `assets/test-strategy-template.md.template`
   - Cover all test types (functional, non-functional, security, performance)
   - Define automation approach and tooling

2. **Define quality gates**
   - CI/CD checks and thresholds
   - Coverage targets (line, branch, function)
   - Sign-off criteria and owners

3. **Review and approve**
   - Share with stakeholders
   - Incorporate feedback
   - Get sign-off before proceeding

## Phase 4: ATDD Scenario Creation

1. **Map requirements to tests**
   - Each requirement has at least one acceptance test
   - Each user story has Given-When-Then scenarios
   - Traceability matrix maintained

2. **Use ATDD template**
   - Fill in `assets/atdd-scenarios-template.md.template`
   - Include edge cases and error paths
   - Define test data and expected outcomes

3. **Prioritize scenarios**
   - Critical path tests first
   - High-risk areas early
   - Regression tests for existing features

## Phase 5: Quality Checklist Creation

1. **Use quality checklist template**
   - Fill in `assets/quality-checklist-template.md.template`
   - Cover functional, performance, security, accessibility
   - Include compatibility and regression checks

2. **Define pass/fail criteria**
   - Clear acceptance criteria
   - Quantitative thresholds where possible
   - Owner and timeline for each item

## Phase 6: Integration and Execution

1. **Partner with development-execution**
   - Integrate tests into CI/CD pipeline
   - Configure automated test runs
   - Set up coverage reporting

2. **Execute test plan**
   - Run ATDD scenarios during development
   - Execute quality checklist before release
   - Track results and defects

3. **Monitor and report**
   - Track test execution metrics
   - Report coverage and defect trends
   - Escalate blockers immediately

## Phase 7: Continuous Improvement

1. **Review outcomes**
   - Analyze defect patterns
   - Identify process gaps
   - Gather stakeholder feedback

2. **Update artifacts**
   - Refine test strategy based on learnings
   - Add new ATDD scenarios for edge cases
   - Improve quality checklist items

3. **Share knowledge**
   - Document lessons learned
   - Update reference materials
   - Train team on new practices

## Error Handling

- **Missing prerequisites**: Halt and request specific artifacts
- **Tooling unavailable**: Document gaps and propose alternatives
- **Environment issues**: Log details, create remediation plan
- **High-risk findings**: Escalate immediately with evidence

## Success Criteria

- All checklist items satisfied
- Test strategy approved by stakeholders
- ATDD scenarios trace to requirements
- Quality gates integrated into CI/CD
- Coverage targets met
- Zero critical defects at release
