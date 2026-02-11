# Development Execution Workflow

## Phase 1: Prerequisites Verification

1. **Read Story File**
   - Locate the story file (typically in `stories/` or `.stories/`)
   - Verify story status is `ready`
   - Confirm all prerequisites are met

2. **Review References**
   - Read relevant sections of `ARCHITECTURE.md`
   - Review UX specifications (if separate)
   - Check quality plan from `bmad-quality-assurance`

3. **Confirm Environment**
   - Verify development environment is set up
   - Check that required tools are available
   - Ensure test suite can run

## Phase 2: Implementation Planning

1. **Analyze Scope**
   - Identify affected files and components
   - Map out dependencies
   - Plan integration points

2. **Create Implementation Plan**
   - Break down into small, reviewable steps
   - Identify test requirements
   - Document rationale for each change

3. **Present Plan**
   - Share plan with user/stakeholders
   - Get approval before proceeding
   - Adjust based on feedback

## Phase 3: Implementation

1. **Apply Changes Incrementally**
   - Make one logical change at a time
   - Explain each change with rationale
   - Reference architecture decisions

2. **Write Tests Alongside Code**
   - Create test files for new functionality
   - Update existing tests as needed
   - Ensure test coverage is adequate

3. **Run Tests**
   - Execute test suite after each change
   - Capture test output verbatim
   - Fix failures immediately

## Phase 4: Documentation

1. **Update Story File**
   - Add Dev Agent Record entry
   - Update status to `in-progress` → `testing` → `done`
   - Document learnings and blockers

2. **Create Implementation Notes**
   - Use template from `assets/implementation-notes-template.md.template`
   - Summarize changes made
   - Record test results
   - Note any outstanding issues

3. **Update Related Documentation**
   - Update inline code comments
   - Modify architecture docs if patterns changed
   - Update API documentation if needed

## Phase 5: Quality Gates

1. **Run Full Test Suite**
   - Execute all tests (unit + integration)
   - Verify coverage meets requirements
   - Document any failures

2. **Code Review Checklist**
   - No TODOs or debug code left behind
   - All tests passing
   - Code follows project standards
   - Documentation is complete

3. **Performance Check** (if applicable)
   - Run performance benchmarks
   - Verify against targets
   - Document results

## Phase 6: Completion

1. **Final Status Update**
   - Set story status to `done`
   - Add final Dev Agent Record entry
   - Note any follow-up work needed

2. **Summary for Stakeholders**
   - List all changes made
   - Summarize test results
   - Highlight any risks or concerns
   - Recommend next steps

3. **Notify Orchestrator**
   - Signal completion of story
   - Provide summary for handoff
   - Request next story or task

## Error Handling

### If Prerequisites Missing
- Halt implementation
- Document specific blocker
- Notify orchestrator
- Suggest remediation steps

### If Tests Fail
- Analyze failure cause
- Fix immediately
- Re-run tests
- Document fix

### If Architecture Conflict
- Review ARCHITECTURE.md
- Consult with architect
- Document decision
- Proceed with consensus

## Success Criteria

A story is complete when:
- [ ] All tests pass (unit + integration)
- [ ] Story documentation updated
- [ ] Implementation notes created
- [ ] No TODOs or debug code remain
- [ ] Code review checklist passed
- [ ] Summary provided to stakeholders
- [ ] Orchestrator notified

## Handoff to Next Skill

After completion, typical next steps:
- **bmad-quality-assurance**: Review implementation
- **bmad-story-planning**: Next story preparation
- **bmad-architecture-design**: If architectural changes needed
- **bmad-ux-design**: If UX validation needed
