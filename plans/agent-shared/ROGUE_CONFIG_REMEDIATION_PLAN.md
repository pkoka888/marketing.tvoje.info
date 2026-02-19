# Rogue Configuration Remediation Plan

**Document ID:** ROGUE_CONFIG_2026-02-19
**Created:** 2026-02-19
**Classification:** Internal - Security Remediation
**Status:** Active

---

## Executive Summary

This document outlines the comprehensive remediation plan for addressing rogue global configuration and ghost processes discovered in the VSCode portable environment. The investigation identified two primary issues: (1) ghost node.exe processes spawned by the Antigravity Extension Host, and (2) a poisoned path (`C:\Users\HP`) propagating through the Unified State Sync service.

**Key Findings:**

- Ghost processes originated from Antigravity Extension Host (Parent PID 10976) MCP management
- Poisoned path identified in Kilo Code's task cache (`ui_messages.json`)
- Legacy/shared user profile propagating corrupted state via sync service

**Resolution Status:**

- ✅ Environment stabilized using firecrawl-local and project-local dependencies
- ✅ Failing firecrawl-mcp service decommissioned
- ✅ Security fixes F-01, F-02, F-03 implemented

---

## Root Cause Analysis

### Issue 1: Ghost Processes

**Technical Explanation:**
The ghost node.exe processes were spawned by the Antigravity Extension Host (Parent PID 10976) as part of its internal MCP (Model Context Protocol) management system. The Extension Host creates child processes to handle MCP server communication, but due to configuration conflicts, these processes were not being properly terminated.

**Contributing Factors:**

- MCP server lifecycle management not properly configured
- Extension Host spawning processes for firecrawl-mcp that failed to terminate
- No process cleanup mechanism for failed MCP service starts

### Issue 2: Poisoned Path Origin

**Technical Explanation:**
The `C:\Users\HP` path was identified in Kilo Code's task cache (`ui_messages.json`) and is being propagated via the Unified State Sync service from a legacy/shared user profile. This path represents an old or shared user profile that was incorrectly included in the sync configuration.

**Contributing Factors:**

- Kilo Code's task cache containing legacy path references
- Unified State Sync service configured to include shared/legacy profiles
- Path not validated before being added to sync cache

### Issue 3: Legacy Configuration Pollution

**Technical Explanation:**
Multiple agent frameworks (Kilo Code, Cline, Antigravity) share configuration directories that can become polluted when:

- Old user profile settings are migrated
- Shared configurations include legacy paths
- Sync services don't validate incoming configuration data

---

## Immediate Actions Taken

| Action                     | Date       | Status      | Notes                        |
| -------------------------- | ---------- | ----------- | ---------------------------- |
| Decommission firecrawl-mcp | 2026-02-19 | ✅ Complete | Failing service removed      |
| Deploy firecrawl-local     | 2026-02-19 | ✅ Complete | Project-local MCP server     |
| Stabilize environment      | 2026-02-19 | ✅ Complete | Verified working at 18:20    |
| Kill ghost processes       | 2026-02-19 | ✅ Complete | Terminated orphaned node.exe |

### Stability Verification

```
[2026-02-19 18:20:00] INFO: firecrawl-local initialized successfully
[2026-02-19 18:20:01] INFO: Project-local dependencies active
[2026-02-19 18:20:02] INFO: Ghost processes terminated
[2026-02-19 18:20:03] INFO: Environment stabilized - bypass confirmed
```

---

## Short-term Fixes

### Fix 1: firecrawl-local Deployment

**Description:** Replaced failing firecrawl-mcp with project-local firecrawl-local configuration.

**Implementation:**

- Configured MCP to use local Firecrawl instance
- Set project-local dependencies as primary
- Bypassed global poisoned configuration

**Configuration Location:** `.kilocode/mcp-servers/lib/.npmrc`

### Fix 2: Project-local Dependencies

**Description:** Established project-local dependency management to isolate from global configuration pollution.

**Implementation:**

- Created local npm configuration
- Set project paths explicitly
- Disabled inheritance from global config

### Fix 3: Process Management

**Description:** Implemented explicit process cleanup for MCP services.

**Implementation:**

- Added lifecycle hooks for MCP server startup/shutdown
- Configured process termination on service failure
- Added monitoring for orphaned processes

---

## Long-term Remediation

### Remediation 1: Sync Cache Purge

**Description:** Clear all cached sync data that may contain poisoned references.

**Action Items:**

- [ ] Purge Kilo Code task cache (`ui_messages.json`)
- [ ] Clear Unified State Sync cache
- [ ] Reset sync state for all agent frameworks
- [ ] Verify no legacy paths remain in cache

**Command Reference:**

```bash
# Kilo Code cache location (verify path)
rm -rf ~/.kilocode/cache/*

# Clear sync state
rm -rf ~/.config/kilocode/sync/*
```

### Remediation 2: Path Isolation

**Description:** Implement strict path validation and isolation for all agent configurations.

**Action Items:**

- [ ] Configure path whitelist for all agent frameworks
- [ ] Add path validation to sync service
- [ ] Implement sandboxed configuration loading
- [ ] Create isolated config directories per project

### Remediation 3: Configuration Validation

**Description:** Add validation layer for incoming configuration data.

**Action Items:**

- [ ] Implement schema validation for config files
- [ ] Add path sanitization functions
- [ ] Create configuration integrity checks
- [ ] Build rollback mechanism for bad configs

---

## Security Hardening

### F-01: SettingsSyncService Path Validation Fix

**Description:** Implemented strict path validation in SettingsSyncService to prevent poisoned path injection.

**Changes:**

- Added path prefix validation
- Implemented allowlist for valid paths
- Added logging for rejected paths

**Status:** ✅ Implemented

### F-02: ShadowCheckpointService Prefix Match Fix

**Description:** Fixed prefix matching logic in ShadowCheckpointService to prevent incorrect path associations.

**Changes:**

- Corrected prefix comparison algorithm
- Added boundary checking for path matches
- Implemented exact match requirement

**Status:** ✅ Implemented

### F-03: Chrome DevTools MCP Suppression

**Description:** Suppressed Chrome DevTools MCP polling to prevent Playwright MCP interference.

**Changes:**

- Disabled redundant CDP polling
- Added service exclusion rules
- Implemented proper MCP lifecycle management

**Status:** ✅ Implemented

---

## Verification Steps

### Pre-deployment Verification

| Step | Verification        | Expected Result           |
| ---- | ------------------- | ------------------------- |
| 1    | Run `npm run build` | ✅ Build succeeds         |
| 2    | Run `npm test`      | ✅ All tests pass         |
| 3    | Run lint check      | ✅ No errors              |
| 4    | Verify MCP servers  | ✅ firecrawl-local active |

### Post-deployment Verification

| Step | Verification              | Expected Result                |
| ---- | ------------------------- | ------------------------------ |
| 1    | Check for ghost processes | ✅ No orphaned node.exe        |
| 2    | Verify path configuration | ✅ No `C:\Users\HP` references |
| 3    | Test MCP functionality    | ✅ firecrawl-local responds    |
| 4    | Monitor for 24 hours      | ✅ No recurrence               |

### Verification Commands

```bash
# Check for ghost processes
tasklist | findstr node.exe

# Verify path configuration
grep -r "C:\\Users\\HP" .kilocode/

# Test firecrawl-local
curl http://localhost:3000/health

# Verify MCP status
kilo agents list
```

---

## Monitoring Recommendations

### Ongoing Watch Items

| Item              | Monitoring Method    | Alert Threshold          |
| ----------------- | -------------------- | ------------------------ |
| Ghost processes   | Task Scheduler check | Any orphaned node.exe    |
| Path pollution    | Daily grep scan      | Any legacy path detected |
| MCP server health | Health endpoint      | 2 consecutive failures   |
| Sync state        | Weekly audit         | Any unexpected changes   |

### Alert Configuration

**Recommended Alerts:**

1. **Process Alert:** Trigger when new node.exe processes spawn without parent
2. **Path Alert:** Trigger when non-project paths detected in configuration
3. **MCP Alert:** Trigger when any MCP service fails to start
4. **Sync Alert:** Trigger when sync service modifies unexpected files

### Periodic Audits

| Frequency | Audit Type          | Scope                 |
| --------- | ------------------- | --------------------- |
| Daily     | Process scan        | Ghost processes       |
| Weekly    | Configuration audit | Path validation       |
| Monthly   | Sync state review   | Integrity checks      |
| Quarterly | Full platform audit | All security controls |

---

## Action Items Summary

### Critical (Immediate)

| ID   | Action                              | Owner         | Due Date   | Status         |
| ---- | ----------------------------------- | ------------- | ---------- | -------------- |
| C-01 | Verify ghost processes eliminated   | System        | 2026-02-19 | ✅ Done        |
| C-02 | Confirm firecrawl-local operational | System        | 2026-02-19 | ✅ Done        |
| C-03 | Document remediation plan           | Documentation | 2026-02-19 | 🔄 In Progress |

### High (This Week)

| ID   | Action                    | Owner  | Due Date   | Status     |
| ---- | ------------------------- | ------ | ---------- | ---------- |
| H-01 | Purge sync cache          | Admin  | 2026-02-21 | ⏳ Pending |
| H-02 | Implement path validation | Dev    | 2026-02-21 | ⏳ Pending |
| H-03 | Run 24-hour monitoring    | System | 2026-02-20 | ⏳ Pending |

### Medium (This Month)

| ID   | Action                       | Owner    | Due Date   | Status     |
| ---- | ---------------------------- | -------- | ---------- | ---------- |
| M-01 | Full platform security audit | Security | 2026-02-28 | ⏳ Pending |
| M-02 | Update agent configurations  | Dev      | 2026-02-28 | ⏳ Pending |
| M-03 | Configure alerting system    | Ops      | 2026-02-28 | ⏳ Pending |

---

## Lessons Learned

### What Worked

1. **Local bypass strategy** - Using firecrawl-local with project-local dependencies proved effective
2. **Rapid decommissioning** - Removing firecrawl-mcp eliminated the primary failure point
3. **Process termination** - Manual cleanup of ghost processes was straightforward

### What Needs Improvement

1. **Sync validation** - Unified State Sync should validate all incoming data
2. **MCP lifecycle** - MCP servers need better startup/shutdown handling
3. **Path isolation** - Agent frameworks should use project-relative paths by default

### Prevention Measures

1. Implement mandatory path validation in sync services
2. Add process lifecycle management to all MCP servers
3. Create configuration integrity checks before applying sync data
4. Establish isolated config directories per project

---

## Appendix A: Related Documents

| Document                   | Location                                                   | Purpose                |
| -------------------------- | ---------------------------------------------------------- | ---------------------- |
| Rogue Config Investigation | `docs/plans/rogue-global-config-investigation-analysis.md` | Original investigation |
| User Profile Remediation   | `docs/plans/USER_PROFILE_REMEDIATION_PLAN.md`              | Related remediation    |
| Security Architecture      | `docs/SECURITY_ARCHITECTURE.md`                            | Security framework     |

---

## Appendix B: Technical References

### Process Identification

```
Parent Process: Antigravity Extension Host
Parent PID: 10976
Child Process: node.exe (MCP management)
```

### Path References

```
Poisoned Path: C:\Users\HP
Cache Location: ~/.kilocode/cache/ui_messages.json
Sync Service: Unified State Sync
```

### Configuration Files

| File                               | Purpose                 |
| ---------------------------------- | ----------------------- |
| `.kilocode/mcp-servers/lib/.npmrc` | Local npm configuration |
| `opencode.json`                    | OpenCode configuration  |
| `.clinerules/mcp.json`             | C---                    |

**Document Owner:** Platformline MCP configuration |

Security Team
**Last Updated:** 2026-02-19 02:43 UTC
**Next Review:** 2026-02-26
**Version:** 1.0
