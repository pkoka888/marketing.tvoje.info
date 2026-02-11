# Testing Infrastructure

This directory contains the comprehensive testing infrastructure for the Kilo Code template project.

## Directory Structure

```
tests/
├── README.md                    # This file
├── run-tests.js                 # Main validation test runner
├── validation/                  # Validation scripts
│   ├── validate-memory-bank.js  # Memory Bank validation
│   ├── validate-mcp-config.js   # MCP configuration validation
│   ├── validate-workflows.js    # Workflow validation
│   ├── validate-skills.js       # Skill validation
│   └── validate-rules.js        # Rule validation
├── fixtures/                    # Test fixtures and sample data
│   ├── sample-brief.md          # Sample Memory Bank file
│   ├── sample-mcp-config.json   # Sample MCP configuration
│   ├── sample-workflow.md       # Sample workflow file
│   └── sample-skill.md          # Sample skill file
├── unit/                        # Unit tests (placeholder)
└── integration/                 # Integration tests
    ├── run-integration-tests.js # Main integration test runner
    ├── test-memory-bank.js      # Memory Bank integration tests
    ├── test-mcp-servers.js      # MCP server integration tests
    ├── test-workflows.js        # Workflow integration tests
    ├── test-modes.js            # Mode integration tests
    ├── test-skills.js           # Skill integration tests
    ├── test-e2e.js              # End-to-end integration tests
    └── test-security.js         # Security integration tests
```

## Usage

### Run All Tests

```bash
npm test
```

Or directly:

```bash
node tests/run-tests.js
```

### Run Tests with Verbose Output

```bash
npm run test:verbose
```

Or directly:

```bash
node tests/run-tests.js --verbose
```

### Run Specific Test

```bash
npm run test:memory-bank
npm run test:mcp-config
npm run test:workflows
npm run test:skills
npm run test:rules
```

Or directly:

```bash
node tests/run-tests.js --test memory-bank
node tests/run-tests.js --test mcp-config
node tests/run-tests.js --test workflows
node tests/run-tests.js --test skills
node tests/run-tests.js --test rules
```

### List Available Tests

```bash
npm run test:list
```

Or directly:

```bash
node tests/run-tests.js --list
```

### Run Individual Validation Scripts

```bash
npm run validate:memory-bank
npm run validate:mcp-config
npm run validate:workflows
npm run validate:skills
npm run validate:rules
```

Or directly:

```bash
node tests/validation/validate-memory-bank.js
node tests/validation/validate-mcp-config.js
node tests/validation/validate-workflows.js
node tests/validation/validate-skills.js
node tests/validation/validate-rules.js
```

### Run All Validations

```bash
npm run validate:all
```

## Integration Tests

### Run All Integration Tests

```bash
npm run test:integration
```

Or directly:

```bash
node tests/integration/run-integration-tests.js
```

### Run Integration Tests with Verbose Output

```bash
npm run test:integration:verbose
```

Or directly:

```bash
node tests/integration/run-integration-tests.js --verbose
```

### Run Specific Integration Test Suite

```bash
npm run test:integration:memory-bank
npm run test:integration:mcp-servers
npm run test:integration:workflows
npm run test:integration:modes
npm run test:integration:skills
npm run test:integration:e2e
npm run test:integration:security
```

Or directly:

```bash
node tests/integration/test-memory-bank.js
node tests/integration/test-mcp-servers.js
node tests/integration/test-workflows.js
node tests/integration/test-modes.js
node tests/integration/test-skills.js
node tests/integration/test-e2e.js
node tests/integration/test-security.js
```

### List Available Integration Test Suites

```bash
npm run test:integration:list
```

Or directly:

```bash
node tests/integration/run-integration-tests.js --list
```

### Run All Tests (Validation + Integration)

```bash
npm run test:all
```

## Integration Test Suites

### test-memory-bank.js

Tests Memory Bank functionality:
- Memory Bank loading at task start
- [Memory Bank: Active] indicator
- Memory Bank update workflow
- Memory Bank initialization
- context.md factual constraint
- brief.md developer-maintained constraint

### test-mcp-servers.js

Tests MCP Server functionality:
- Filesystem server connectivity
- Memory server operations
- Git server operations
- GitHub server authentication
- Time server operations
- Fetch server HTTP requests
- Redis server connection
- SQLite server operations
- Puppeteer server automation
- Rate limiting
- Permission controls

### test-workflows.js

Tests Workflow functionality:
- analyze-prompt workflow
- create-prompt workflow
- optimize-prompt workflow
- test-prompt workflow
- workflow file name matching
- step-by-step execution
- user input collection

### test-modes.js

Tests Mode functionality:
- Architect mode multi-attempt reasoning
- Code mode simulation testing
- Debug mode 8-step protocol
- Ask mode Memory Bank loading
- mode-specific rule application

### test-skills.js

Tests Skill functionality:
- Prompt Consultant skill loading
- skill name matching
- skill workflow integration
- skill YAML frontmatter

### test-e2e.js

Tests End-to-End scenarios:
- Complete workflow from start to finish
- Memory Bank persistence across sessions
- MCP server communication
- Mode switching
- Error handling and recovery

### test-security.js

Tests Security controls:
- Path validation
- Rate limiting enforcement
- Permission controls
- Environment variable handling
- Token authentication

## Validation Scripts

### validate-memory-bank.js

Validates Memory Bank files in `.kilocode/rules/memory-bank/`:

- Checks all 5 core files exist
- Validates file structure and content
- Checks for required sections
- Verifies YAML frontmatter format (if applicable)
- Tests file readability

**Core Files:**
- `brief.md` - Project overview and goals
- `product.md` - Product description and user experience
- `context.md` - Current work focus and recent changes
- `architecture.md` - System architecture and technical decisions
- `tech.md` - Technologies and development setup

### validate-mcp-config.js

Validates MCP configuration in `.kilocode/mcp.json`:

- Checks JSON syntax
- Validates server configurations
- Checks for required servers
- Verifies security measures (rate limiting, permissions)
- Tests path validation rules

**Required Servers:**
- `filesystem-projects`
- `filesystem-agentic`

### validate-workflows.js

Validates workflow files in `.kilocode/workflows/`:

- Checks workflow files exist
- Validates XML-like tag structure
- Verifies task name matches file name
- Checks for required sections

**Required Sections:**
- `<task_objective>`
- `<detailed_sequence_steps>`

### validate-skills.js

Validates skill files in `.kilocode/skills/`:

- Checks skill directories exist
- Validates YAML frontmatter
- Verifies skill name matches directory name
- Checks for required sections

**Required YAML Fields:**
- `name`
- `description`

### validate-rules.js

Validates rule files in `.kilocode/rules-*/` directories:

- Checks rule files exist
- Validates YAML frontmatter blocks
- Verifies alwaysApply settings
- Checks for required fields

**Required YAML Fields:**
- `description`

## Exit Codes

- `0` - All validations passed
- `1` - Validation errors found
- `2` - Invalid arguments

## Test Fixtures

The `fixtures/` directory contains sample files for testing and reference:

- `sample-brief.md` - Example Memory Bank brief file
- `sample-mcp-config.json` - Example MCP configuration
- `sample-workflow.md` - Example workflow file
- `sample-skill.md` - Example skill file

## Adding New Tests

To add a new validation script:

1. Create a new file in `tests/validation/`
2. Follow the naming convention: `validate-{name}.js`
3. Implement the validation logic
4. Add the test to the `TESTS` array in `tests/run-tests.js`
5. Add npm scripts to `package.json`

## Requirements

- Node.js >= 14.0.0
- No external dependencies required

## Best Practices

1. **Separation of Concerns**: Each validation script should focus on a specific area
2. **Clear Error Messages**: Provide descriptive error messages with file paths and line numbers
3. **Exit Codes**: Use appropriate exit codes for automation
4. **Verbose Mode**: Support verbose output for debugging
5. **Human-Readable Reports**: Generate clear, readable test reports

## Troubleshooting

### Tests Fail with "File Not Found"

Ensure you're running the tests from the project root directory:

```bash
cd c:/Users/pavel/projects/jobs
npm test
```

### Permission Errors on Windows

If you encounter permission errors, try running the command prompt as Administrator.

### Node.js Version Issues

Ensure you have Node.js >= 14.0.0 installed:

```bash
node --version
```

## Contributing

When adding new validation rules:

1. Update the relevant validation script
2. Add test cases to the fixtures
3. Update this README with new information
4. Test thoroughly before committing
