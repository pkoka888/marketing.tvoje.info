---
description: Run the Vitest test suite
---
// turbo-all

## Steps

1. Run all tests:
```bash
npm run test
```

2. For watch mode during development:
```bash
npm run test:watch
```

## Test Locations
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Validation tests: `tests/validation/`
- Test fixtures: `tests/fixtures/`

## Notes
- Tests use Vitest as the runner
- Config is in `vitest.config.ts`
