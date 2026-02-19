# Kilo Code Feedback: Rogue Global Configuration Fix Plan

**Date**: 2026-02-19
**Agent**: Antigravity (Gemini)
**Source Investigation**: `docs/USER_PROFILE_INVESTIGATION.md`, `docs/plans/USER_PROFILE_REMEDIATION_PLAN.md`

## Summary

Three upstream findings for Kilo Code + local remediation steps.

### Upstream Findings (for GitHub Issue)

| ID   | File                             | Issue                                                                                                                     | Severity |
| ---- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------- |
| F-01 | `SettingsSyncService.ts`         | No path validation on synced globalState values — stale paths from other machines propagate silently                      | Low      |
| F-02 | `ShadowCheckpointService.ts:134` | Protected path check uses `.includes()` (exact match) instead of prefix match — `~/Desktop/subfolder` bypasses protection | Medium   |
| F-03 | Extension activation             | No startup health check for stale/foreign paths in globalState                                                            | Low      |

### Local Remediation

| Step | Action                                                         | Status |
| ---- | -------------------------------------------------------------- | ------ |
| L-01 | Clear stale `C:\Users\HP` from VS Code globalState             | [ ]    |
| L-02 | Configure selective Settings Sync key ignoring                 | [ ]    |
| L-03 | Verify clean state (grep + checkpoint test + firecrawl health) | [ ]    |
| L-04 | Document portable VS Code setup best practices                 | [ ]    |

### GitHub Issue Format

**Title**: `[Enhancement] Add stale path detection to SettingsSyncService + prefix-match for protected paths`
**Labels**: `enhancement`, `security`, `settings-sync`

See full plan in Antigravity brain artifact for detailed diff proposals and verification steps.
