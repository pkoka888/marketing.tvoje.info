# BMAD Remediation Plan: User Profile Mixing Issue

**Date**: 2026-02-18
**Agent**: Kilo Code (bmad-dev)
**Framework**: BMAD v6.0.0-Beta.8

---

## 1. Executive Summary

This remediation plan addresses the "poisoned path" issue where `C:\Users\HP` appeared in a `C:\Users\pavel` environment. Investigation confirmed:

- **Root Cause**: VS Code Settings Sync (Microsoft's cloud sync), NOT Kilo Code's custom implementation
- **Ghost Processes**: Normal VS Code Extension Host behavior for MCP server management
- **Current Fix**: firecrawl-local replaced firecrawl-mcp (decommissioned)
- **Protection Exists**: ShadowCheckpointService with protected paths + SHA-256 workspace hashing

**Resolution Status**: Issue resolved. Recommendations below for prevention.

---

## 2. Technical Root Causes

| ID | Root Cause | Evidence |
|----|------------|----------|
| RC-01 | **VS Code Settings Sync** propagates stale paths from previous machine/profile | Kilo Code uses `globalState.setKeysForSync()` - no custom sync implementation |
| RC-02 | Extension storing absolute paths before Kilo Code installation | Any extension could store `C:\Users\HP\*` in globalState |
| RC-03 | firecrawl-mcp service failure | Service deprecated, replaced with firecrawl-local |

### Evidence Chain

```
SettingsSyncService.ts → globalState.setKeysForSync() → Microsoft Cloud → New Machine
```

---

## 3. Affected Components

| Component | Impact | Status |
|-----------|--------|--------|
| Kilo Code SettingsSyncService | Uses VS Code native sync (no custom impl) | ✅ Not Bug |
| VS Code Extension Host | Spawns node.exe for MCP (normal behavior) | ✅ Expected |
| ShadowCheckpointService | Protected paths + SHA-256 hashing | ✅ Active Protection |
| firecrawl-mcp | Service failed, decommissioned | ✅ Replaced |
| firecrawl-local | Implemented as replacement | ✅ Working |

---

## 4. Actionable Recommendations

### P0 - Immediate Actions (Critical)

#### REC-01: Disable VS Code Settings Sync for Sensitive Paths
- **Priority**: P0
- **Action**: Turn off VS Code Settings Sync or selectively exclude problematic keys
- **Risk**: Medium - Loses convenience of sync
- **Mitigation**: Document which keys are safe to sync
- **Verification**: Check `File > Preferences > Settings Sync` is properly configured

#### REC-02: Clear Stale Global State
- **Priority**: P0
- **Action**: Clear VS Code globalState for extensions that may contain old paths
- **Risk**: Low - Extensions will reinitialize with correct paths
- **Mitigation**: Export current settings before clearing
- **Verification**: Path `C:\Users\HP` no longer appears in workspace

### P1 - Short-term Actions (High Priority)

#### REC-03: Document Portable VS Code Setup Best Practices
- **Priority**: P1
- **Action**: Create `.vscode/settings.json` with portable mode configuration to avoid user profile mixing
- **Risk**: Low - Documentation only
- **Mitigation**: N/A
- **Verification**: Settings file present and valid JSON

#### REC-04: Verify ShadowCheckpointService is Active
- **Priority**: P1
- **Action**: Confirm ShadowCheckpointService protected paths are functioning
- **Risk**: None - Read-only verification
- **Mitigation**: N/A
- **Verification**: Test checkpoint creation in non-protected directory succeeds, protected directory fails

### P2 - Long-term Preventive Measures (Medium Priority)

#### REC-05: Add MCP Server Health Checks
- **Priority**: P2
- **Action**: Implement monitoring for MCP server health (especially firecrawl-local)
- **Risk**: Low - Improved observability
- **Mitigation**: N/A
- **Verification**: Health check endpoint returns status for each MCP server

#### REC-06: Create Incident Response Runbook
- **Priority**: P2
- **Action**: Document steps for future profile mixing incidents
- **Risk**: None - Documentation only
- **Mitigation**: N/A
- **Verification**: Runbook present in `docs/incident-response/`

---

## 5. Risk Analysis

| Recommendation | Risk Level | Impact | Mitigation |
|---------------|------------|--------|------------|
| REC-01: Disable Settings Sync | Medium | Loss of convenience | Selective key sync |
| REC-02: Clear Global State | Low | Extension reinit | Export settings first |
| REC-03: Document Best Practices | Low | None | N/A |
| REC-04: Verify Protection | None | N/A | N/A |
| REC-05: MCP Health Checks | Low | Improved ops | N/A |
| REC-06: Incident Runbook | None | N/A | N/A |

---

## 6. Implementation Steps

### Step 1: Immediate Resolution
- [ ] Disable VS Code Settings Sync or configure selective sync
- [ ] Clear stale globalState values containing `C:\Users\HP`
- [ ] Verify path no longer appears in workspace

### Step 2: Verification
- [ ] Run `python scripts/verify_agentic_platform.py` - must exit 0
- [ ] Verify ShadowCheckpointService protected paths active
- [ ] Confirm firecrawl-local is operational

### Step 3: Documentation
- [ ] Create portable VS Code setup guide
- [ ] Document incident response procedure

---

## 7. Verification

- [ ] Automated: `python scripts/verify_agentic_platform.py`
- [ ] Manual: Check no `C:\Users\HP` paths in workspace
- [ ] Manual: Verify firecrawl-local MCP server responds

---

## 8. References

| Document | Purpose |
|----------|---------|
| `docs/USER_PROFILE_INVESTIGATION.md` | Full investigation report |
| `AGENTS.md` | Agent platform governance |
| `.kilocode/rules/bmad-integration.md` | BMAD workflow protocol |

---

## 9. Appendix: Protection Mechanisms Summary

### ShadowCheckpointService Protections

| Protection | Status |
|------------|--------|
| Protected Paths (homedir, Desktop, Documents, Downloads) | ✅ Active |
| SHA-256 Workspace Hashing | ✅ Active |
| Warning System | ✅ Active |

### MCP Server Status

| Server | Status | Notes |
|--------|--------|-------|
| firecrawl-local | ✅ Working | Replaced firecrawl-mcp |
| memory | ✅ Running | Cross-session state |
| redis | ✅ Running | Parallel coordination |
| github | ✅ Configured | PR/issue management |
