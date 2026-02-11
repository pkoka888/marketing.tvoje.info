# Quality Assurance Reference

## Test Strategy Template

Use `assets/test-strategy-template.md.template` to author a test strategy covering:

- **Scope and objectives**: What will be tested and why
- **Risk assessment**: High-impact failure modes and mitigation
- **Test types**: Functional, non-functional, security, performance, compliance
- **Automation approach**: Tools, frameworks, and coverage targets
- **Environments**: Dev, staging, production with data and access
- **Data strategy**: Test data management, privacy, and synthetic data
- **Quality gates**: CI/CD checks, metrics, and sign-off criteria

## ATDD Scenarios Template

Use `assets/atdd-scenarios-template.md.template` to define acceptance tests:

- **Scenario ID and title**: Unique identifier and description
- **Requirement traceability**: Links to PRD or story
- **Given-When-Then structure**: Pre-conditions, actions, expected outcomes
- **Test data**: Input values and edge cases
- **Acceptance criteria**: Pass/fail conditions
- **Owner and timeline**: Who owns the test and when it runs

## Quality Checklist Template

Use `assets/quality-checklist-template.md.template` to create a checklist:

- **Functional completeness**: All features work as specified
- **Performance**: Load time, response time, throughput
- **Security**: Authentication, authorization, data protection
- **Accessibility**: WCAG compliance, keyboard navigation, screen readers
- **Compatibility**: Browsers, devices, OS versions
- **Regression**: Existing features still work after changes

## Coverage Matrix

Track test coverage across:

- **Requirements**: Each requirement has at least one test
- **User stories**: Each story has acceptance tests
- **Risk areas**: High-risk components have extra coverage
- **Edge cases**: Boundary values, null inputs, error paths

## CI/CD Integration

Define quality gates in CI/CD:

- **Automated tests**: Unit, integration, E2E run on every commit
- **Code quality**: Linting, formatting, type checking
- **Security scans**: Dependency vulnerabilities, SAST, DAST
- **Performance budgets**: Bundle size, load time, CLS thresholds
- **Deployment gates**: Tests must pass before promotion

## Metrics and Reporting

Track and report:

- **Test execution**: Pass/fail rates, flaky tests, execution time
- **Coverage**: Line, branch, function coverage percentages
- **Defect metrics**: Open, closed, severity, age
- **Quality trends**: Velocity, defect density, MTTR

## Risk Mitigation

Address common risks:

- **Insufficient time**: Prioritize high-risk areas, use risk-based testing
- **Environment drift**: Use infrastructure as code, versioned environments
- **Test data issues**: Synthetic data generation, data masking
- **Flaky tests**: Isolate, fix, or quarantine unstable tests
- **Skill gaps**: Training, pair programming, external QA support

## Tooling Recommendations

Consider tools for:

- **Test automation**: Jest, Cypress, Playwright, Selenium
- **Performance**: Lighthouse, WebPageTest, k6
- **Security**: OWASP ZAP, Snyk, Dependabot
- **Coverage**: Istanbul, Codecov, SonarQube
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins
