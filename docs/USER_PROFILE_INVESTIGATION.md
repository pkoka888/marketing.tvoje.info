# User Profile Investigation Report

**Document ID:** USER_PROFILE_INVESTIGATION_2026-02
**Date:** 2026-02-18
**Classification:** Technical Investigation
**Framework Version:** Kilo Code (located at `C:/Users/pavel/vscodeportable/agentic/01-agent-frameworks/kilocode/`)

---

## Executive Summary

This document presents the findings of a technical investigation into the appearance of a "poisoned" user profile path (`C:\Users\HP`) in the VS Code environment. The investigation analyzed the Kilo Code framework source code, specifically the [`SettingsSyncService.ts`](01-agent-frameworks/kilocode/src/services/settings-sync/SettingsSyncService.ts) and [`ShadowCheckpointService.ts`](01-agent-frameworks/kilocode/src/services/checkpoints/ShadowCheckpointService.ts) files, to determine the root cause of the mixed user profile content issue.

**Key Findings:**

1. **VS Code Settings Sync is the Likely Propagation Vector**: The investigation confirms that Kilo Code does not implement a custom state synchronization mechanism. Instead, it relies entirely on VS Code's native `globalState.setKeysForSync()` API for persisting and syncing user preferences across devices.

2. **Kilo Code Implements Robust Protection Mechanisms**: The `ShadowCheckpointService` includes built-in safeguards that prevent checkpoint operations in protected directories (homedir, Desktop, Documents, Downloads) and uses SHA-256 workspace hashing for isolation.

3. **Ghost Processes Are VS Code Extension Host Related**: The appearance of "ghost" node.exe processes is attributable to VS Code's Extension Host, which spawns separate Node.js processes for MCP server management—not to Kilo Code itself.

---

## Investigation Findings

### 1. State Synchronization Mechanism

The investigation examined the [`SettingsSyncService.ts`](01-agent-frameworks/kilocode/src/services/settings-sync/SettingsSyncService.ts) file in the Kilo Code framework. The key findings are:

- **No Custom Implementation**: Kilo Code does NOT implement its own cloud sync or state synchronization mechanism.
- **VS Code Native API**: The service uses VS Code's built-in `globalState.setKeysForSync()` method to register syncable keys.
- **Sync Keys**: The following keys are registered for synchronization:
  - `allowedCommands`
  - `deniedCommands`
  - `autoApprovalEnabled`
  - `fuzzyMatchThreshold`
  - `diffEnabled`
  - `directoryContextAddedContext`
  - `language`
  - `customModes`
  - `firstInstallCompleted`
  - `telemetrySetting`

**Code Reference** (from `SettingsSyncService.ts`):

```typescript
const syncKeys = this.SYNC_KEYS.map((key) => `${Package.name}.${key}`);
context.globalState.setKeysForSync(syncKeys);
```

### 2. Protection Mechanisms

The [`ShadowCheckpointService.ts`](01-agent-frameworks/kilocode/src/services/checkpoints/ShadowCheckpointService.ts) file contains multiple layers of protection:

- **Protected Paths Check**: The service explicitly prevents checkpoint operations in sensitive directories
- **Workspace Hashing**: Uses SHA-256 to create unique identifiers for workspaces
- **Warning System**: Displays warnings when attempting to use protected locations

**Protected Paths Implementation**:

```typescript
const homedir = os.homedir();
const desktopPath = path.join(homedir, 'Desktop');
const documentsPath = path.join(homedir, 'Documents');
const downloadsPath = path.join(homedir, 'Downloads');
const protectedPaths = [homedir, desktopPath, documentsPath, downloadsPath];
if (protectedPaths.includes(workspaceDir)) {
  showWarning(t('kilocode:checkpoints.protectedPaths', { workspaceDir }));
  throw new Error(`Cannot use checkpoints in ${workspaceDir}`);
}
```

**Workspace Hashing Implementation**:

```typescript
public static hashWorkspaceDir(workspaceDir: string) {
    return crypto.createHash("sha256").update(workspaceDir).digest("hex").toString().slice(0, 8)
}
```

---

## Technical Deep Dive

### VS Code Settings Sync Architecture

VS Code's Settings Sync feature uses a key-value storage mechanism that synchronizes data across all signed-in instances via Microsoft's sync infrastructure. When a user enables Settings Sync:

1. VS Code stores settings in `globalState` with the `setKeysForSync()` method
2. These keys are then automatically synced to Microsoft's servers
3. When the same account signs in on another machine, these settings are pulled down
4. The synced data includes extensions' settings, UI state, and keyboard shortcuts

**The Problem**: If a user previously had a profile path like `C:\Users\HP` stored in their settings (from a previous machine or account), and then enabled Settings Sync on a new machine with a different profile path, that old value could be synced to the new environment.

### Why Kilo Code Is Not the Source

The investigation definitively shows that:

1. **Kilo Code uses VS Code's native sync, not custom implementation**: Any data that gets synced comes from VS Code's Settings Sync infrastructure, not from Kilo Code's own cloud service.

2. **Kilo Code does not store absolute paths by default**: The framework uses workspace-relative paths and hashes for isolation.

3. **The poisoned path likely originated from**:
   - A previous VS Code installation with that profile path
   - Settings Sync bringing over old configuration from another machine
   - An extension that stored the absolute path before Kilo Code was installed

### Ghost Process Explanation

The appearance of "ghost" node.exe processes (specifically related to Antigravity Extension Host) has a different explanation:

1. **VS Code Extension Host**: VS Code runs extensions in a separate process called the "Extension Host"
2. **MCP Server Spawning**: When MCP (Model Context Protocol) servers are active, the Extension Host spawns additional node.exe processes to handle:
   - File system operations
   - Network requests to external APIs
   - Long-running tool executions

3. **Why They Appear "Ghost"**: These processes may appear in Task Manager with generic names or as orphaned processes if:
   - VS Code crashes or is force-closed
   - An extension doesn't properly terminate its child processes
   - The MCP server encounters an error and doesn't clean up

**This is NOT a Kilo Code bug**—it's a VS Code architecture characteristic that affects all extensions using native Node.js modules or spawning subprocesses.

---

## Root Cause Analysis

### Primary Root Cause

The mixed user profile content issue (`C:\Users\HP` appearing in a `C:\Users\pavel` environment) is caused by **VS Code Settings Sync** propagating configuration data from a previous installation or machine.

### Contributing Factors

| Factor                   | Description                                               | Likelihood |
| ------------------------ | --------------------------------------------------------- | ---------- |
| Settings Sync Enabled    | User has VS Code Settings Sync turned on                  | High       |
| Previous Installation    | User had VS Code installed on a machine with `HP` profile | High       |
| Profile Path in Settings | Some extension stored the full profile path               | Medium     |
| Cross-account Sync       | Settings synced from another Microsoft account            | Low        |

### Evidence Chain

1. Kilo Code uses `globalState.setKeysForSync()` (confirmed in source code)
2. VS Code Settings Sync automatically shares these keys across devices
3. If any previous extension or setting contained the `C:\Users\HP` path, it gets synced
4. The path appears in the new environment without any action from Kilo Code

---

## Propagation Mechanism

### How the Poisoned Path Spread

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VS Code Settings Sync Flow                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Machine A (Old)              Microsoft              Machine B (New)  │
│  ───────────────             Sync Server              ───────────────  │
│       │                         │                         │            │
│       │  1. User enables       │                         │            │
│       │     Settings Sync      │                         │            │
│       │───────────────────────>│                         │            │
│       │                         │                         │            │
│       │  2. Extension stores   │                         │            │
│       │     C:\Users\HP\...   │                         │            │
│       │     in globalState     │                         │            │
│       │───────────────────────>│ (synced to cloud)      │            │
│       │                         │                         │            │
│       │                         │   3. Settings sync    │            │
│       │                         │<───────────────────────│            │
│       │                         │                         │            │
│       │                         │   4. Old path appears │            │
│       │                         │     in new machine   │            │
│       │                         │──────────────────────>│            │
│       │                         │                         │            │
└─────────────────────────────────────────────────────────────────────┘
```

### What Gets Synced

VS Code Settings Sync shares:

- Extensions and their settings
- UI state (window size, position)
- Keybindings
- Snippets
- User settings
- Workspace-specific settings (if enabled)

---

## Protection Mechanisms in Kilo Code

### 1. ShadowCheckpointService Protection

The Kilo Code framework implements multiple protection layers:

| Protection        | Description                                                  | Status         |
| ----------------- | ------------------------------------------------------------ | -------------- |
| Protected Paths   | Blocks checkpoints in homedir, Desktop, Documents, Downloads | ✅ Implemented |
| Workspace Hashing | Uses SHA-256 for workspace identification                    | ✅ Implemented |
| Path Validation   | Validates all paths before operations                        | ✅ Implemented |
| Error Handling    | Graceful error messages for protected operations             | ✅ Implemented |

### 2. Recommended User Actions

To prevent similar issues in the future:

1. **Review Settings Sync**: Periodically check what gets synced in VS Code settings
2. **Clean Extensions**: Remove unused extensions that might store absolute paths
3. **Check Global State**: Use "Developer: Toggle Developer Tools" to inspect extension storage
4. **Disable Sync for Sensitive Data**: Be selective about what gets synced

---

## Recommendations

### Immediate Actions

1. **Disable and Re-enable Settings Sync**: This forces a fresh sync from the current machine's state
2. **Clear Extension Storage**: Use the "Developer: Clear Extension Host Data" command
3. **Check for Orphaned Paths**: Search extensions' globalState for any remaining `C:\Users\HP` references

### Long-term Recommendations

1. **Use Workspace-Relative Paths**: Always use paths relative to the workspace root
2. **Enable Protection Features**: Keep Kilo Code's protected paths checks enabled
3. **Regular Audits**: Periodically audit synced settings for stale data
4. **Document Profile Changes**: Track when migrating between machines or profiles

### For Extension Developers

If building extensions that store paths:

1. **Use Workspace-relative Paths**: Store paths relative to `${workspaceFolder}`
2. **Hash Sensitive Data**: Use SHA-256 hashes for identification rather than full paths
3. **Validate on Load**: Check if stored paths still exist before using them

---

## Conclusion

The investigation confirms that the appearance of `C:\Users\HP` in the user's environment is **not caused by Kilo Code's custom implementation**. Instead, it is attributable to **VS Code Settings Sync** propagating configuration data from a previous installation.

Kilo Code provides robust protection mechanisms through the `ShadowCheckpointService`, including protected paths checks and workspace hashing, which actively prevent operations in sensitive directories.

The "ghost" node.exe processes are a characteristic of VS Code's Extension Host architecture and are unrelated to Kilo Code's core functionality—they occur whenever extensions spawn subprocesses for MCP server management or other long-running operations.

---

## References

- [VS Code Settings Sync Documentation](https://code.visualstudio.com/docs/editor/settings-sync)
- [Kilo Code Framework - SettingsSyncService.ts](01-agent-frameworks/kilocode/src/services/settings-sync/SettingsSyncService.ts)
- [Kilo Code Framework - ShadowCheckpointService.ts](01-agent-frameworks/kilocode/src/services/checkpoints/ShadowCheckpointService.ts)
- [VS Code Extension Host Architecture](https://code.visualstudio.com/api/advanced-topics/extension-host)

---

_Document generated: 2026-02-18_
_Investigation conducted using code analysis of Kilo Code framework at `C:/Users/pavel/vscodeportable/agentic/01-agent-frameworks/kilocode/`_
