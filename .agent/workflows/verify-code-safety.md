---
description: Verification protocol for new code changes using TDD and golden practices.
---

# Code Safety Verification

**Agent**: `bmad-tester`
**Tools**: `grep_search` (Research), `vitest` (Testing)

## 1. Research & Analysis

Before verifying, understand the "Golden Practice" for the pattern.

- Search for existing tests: `grep_search "describe|it|test" tests/`
- Search `vscodeportable/agentic` for best practices on this pattern.

## 2. Test Plan Creation

Create a test plan _before_ execution.

- If it's a UI component: Plan a Vitest/React Testing Library test.
- If it's logic: Plan a unit test.
- **Rule**: Never run untested code in production.

## 3. Execution & Verification

1.  Run existing tests: `npm run test`
2.  If failing, fix immediately.
3.  Execute the new code/script in a dry-run or safe environment if possible.

## 4. Visual Confirmation (If UI)

- Run `.agent/workflows/verify-visuals.md` to get screenshots.
