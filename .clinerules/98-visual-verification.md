# Rule: Mandatory Visual Verification

**ID:** `RULE-VISUAL-01`
**Severity:** High

## Overview

All changes to Frontend components (`src/components`, `src/layouts`, `src/pages`) MUST be visually verified using the Playwright workflow or manual screenshots.

## Requirements

1.  **Workflow Execution**: Upon completing a UI task, the agent MUST run `.agent/workflows/verify-visuals.md`.
2.  **Evidence**: Screenshots must be saved to `evidence/` with a descriptive name (e.g., `evidence/feature-X-light.png`).
3.  **Review**: If the agent cannot view the image, it must ask the user to verify the screenshot before marking the task as complete.

## Enforcement

- Agents with the `bmad-ux` or `bmad-tester` role are primarily responsible.
- The `AUDITOR` agent will check for `evidence/` artifacts in PRs.
