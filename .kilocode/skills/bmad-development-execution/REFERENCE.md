# Development Execution Reference

## Key Concepts

- **Story-Driven Development**: All implementation work is tied to approved stories from delivery-planning.
- **Traceability**: Every code change references the story, architecture decisions, and UX requirements.
- **Test-First**: Tests are written or updated alongside implementation, never as an afterthought.
- **Incremental Delivery**: Small, reviewable changes with clear rationale.

## Common Patterns

### Reading a Story File
```bash
# Story files are typically in stories/ or .stories/
cat stories/user-authentication.md
```

### Running Tests
```bash
# Run all tests
npm test

# Run specific test suite
npm test -- --grep "authentication"

# Run tests with coverage
npm test -- --coverage
```

### Updating Story Status
```markdown
## Status
ready → in-progress → testing → done → blocked
```

### Documenting Implementation Notes
```markdown
# Implementation Notes

## Story
[Story Name]

## Changes Made
- File: src/components/Button.tsx
  - Added `loading` prop
  - Updated TypeScript types

## Tests
- Unit tests: 5 passed
- Integration tests: 3 passed

## Learnings
- Consider extracting loading state to a separate component
```

## Architecture References

When implementing, reference relevant sections of `ARCHITECTURE.md`:
- Component patterns
- Data flow diagrams
- API contracts
- State management approach

## UX Guidance

Follow UX specifications from story or separate UX docs:
- Interaction patterns
- Accessibility requirements
- Responsive behavior
- Error states

## Quality Gates

Before marking a story as done:
1. All tests pass (unit + integration)
2. Code review completed
3. Story documentation updated
4. No TODOs or debug code left behind
5. Performance benchmarks met (if applicable)

## Troubleshooting

### Common Issues

**Tests failing after implementation:**
- Check if test expectations match new behavior
- Verify test data is up to date
- Review integration points

**Story status not updating:**
- Ensure story file is writable
- Check YAML frontmatter format
- Verify status transition is valid

**Architecture conflicts:**
- Review ARCHITECTURE.md for patterns
- Consult with architect if needed
- Document decision in story

## Best Practices

1. **Small Changes**: Keep diffs focused and reviewable
2. **Clear Rationale**: Explain why each change is needed
3. **Test Coverage**: Aim for high coverage on new code
4. **Documentation**: Update inline comments and story docs
5. **Communication**: Summarize work for stakeholders

## Related Skills

- **bmad-story-planning**: Creates the stories you implement
- **bmad-architecture-design**: Provides architectural guidance
- **bmad-ux-design**: Provides UX specifications
- **bmad-test-strategy**: Defines test approach
- **bmad-quality-assurance**: Reviews your work
