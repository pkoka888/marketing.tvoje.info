# F03: Chrome DevTools MCP Suppression Fix

**Issue ID**: F03-chrome-devtools-mcp-fix
**Priority**: LOW (Operational Issue)
**Status**: Documentation Complete
**Created**: 2026-02-19
**Parent**: Rogue Global Configuration Investigation

---

## Executive Summary

This document provides the investigation findings and suppression recommendations for the Chrome DevTools MCP polling error causing repeated "command not found" errors at approximately 1/second rate. The actual source is the **Playwright MCP** (`@playwright/mcp`), which provides Chrome DevTools functionality.

---

## 1. Current Behavior Analysis

### 1.1 Issue Description

- **Error Type**: "command not found" polling error
- **Frequency**: ~1 request per second
- **Impact**: Continuous CPU consumption, log noise
- **MCP Server**: Playwright MCP (provides Chrome DevTools capabilities)

### 1.2 Configuration Locations

The Playwright MCP is configured in TWO locations:

#### Location 1: `opencode.json` (lines 138-142)

```json
"playwright-mcp": {
  "type": "local",
  "command": ["node", "C:/nvm4w/nodejs/node_modules/@playwright/mcp/cli.js"],
  "environment": {}
}
```

#### Location 2: `.clinerules/mcp.json` (lines 41-44)

```json
"playwright-mcp": {
  "command": "node",
  "args": ["C:/nvm4w/nodejs/node_modules/@playwright/mcp/cli.js"]
}
```

### 1.3 Root Cause

The Playwright MCP (`@playwright/mcp/cli.js`) polls for browser availability (Chrome/Chromium) at regular intervals. When browsers are not installed or not accessible in the environment:

1. The MCP attempts to detect available browsers on system startup
2. Detection fails with "command not found" or similar error
3. Polling continues at ~1 second intervals
4. Results in continuous CPU consumption and error log noise

---

## 2. Why Polling Causes Issues

### 2.1 Performance Impact

| Metric      | Impact                                    |
| ----------- | ----------------------------------------- |
| CPU Usage   | Continuous low-level polling (~1 req/sec) |
| Memory      | Minor overhead from active process        |
| Log Volume  | Generates repetitive error entries        |
| System Load | Increased from constant process spawning  |

### 2.2 Operational Impact

- **Log Noise**: Pollutes error logs with repeated "command not found" messages
- **Resource Waste**: Unnecessary CPU cycles on every polling interval
- **Debugging Difficulty**: Makes it harder to identify real errors in log output

---

## 3. Recommended Suppression Approach

### 3.1 Option A: Complete Removal (Recommended)

**Description**: Remove Playwright MCP from both configuration files entirely.

**Files to Modify**:

1. `opencode.json` - Remove `playwright-mcp` entry
2. `.clinerules/mcp.json` - Remove `playwright-mcp` entry

**Pros**:

- Eliminates all polling overhead
- Removes error messages completely
- Simplifies MCP configuration

**Cons**:

- Loses browser automation capabilities
- Loses Chrome DevTools functionality

**When to Use**:

- Browser automation not required for current workflows
- Seeking minimal resource footprint
- Alternative tools available for browser tasks

---

### 3.2 Option B: Conditional Disable via Environment Variable

**Description**: Set environment variable to disable browser detection without removing MCP.

**Implementation**:

```json
"playwright-mcp": {
  "command": "node",
  "args": ["C:/nvm4w/nodejs/node_modules/@playwright/mcp/cli.js"],
  "env": {
    "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD": "true",
    "PLAYWRIGHT_NO_BROWSER": "true"
  }
}
```

**Pros**:

- Retains MCP functionality for future use
- Single configuration change
- Easy to reverse

**Cons**:

- May not fully suppress polling behavior
- Requires testing to verify effectiveness

---

### 3.3 Option C: Lazy Loading / On-Demand Activation

**Description**: Configure MCP to only initialize when explicitly requested.

**Implementation**: This requires modifying the MCP startup configuration at the IDE/agent level.

**Pros**:

- Full functionality preserved
- Zero overhead when not in use

**Cons**:

- Requires IDE/agent configuration changes
- May not be supported by all MCP clients

---

## 4. Steps to Disable or Reduce Polling Frequency

### 4.1 Immediate Action (Remove Playwright MCP)

**Step 1**: Edit `opencode.json`

```bash
# Remove lines 138-142 containing "playwright-mcp"
```

**Step 2**: Edit `.clinerules/mcp.json`

```bash
# Remove lines 41-44 containing "playwright-mcp"
```

**Step 3**: Restart IDE/Agent sessions

```bash
# Close and reopen Kilo Code / OpenCode / Cline
```

**Step 4**: Verify elimination

```bash
# Monitor system for cessation of polling errors
```

---

### 4.2 Alternative: Reduce Polling Frequency

If complete removal is not desired, the polling frequency can potentially be reduced by:

1. **Environment Configuration**: Add `PLAYWRIGHT_BROWSER_CHECK_INTERVAL` environment variable (if supported)
2. **Custom MCP Wrapper**: Create a wrapper script that adds delay between polls
3. **Resource Limits**: Use OS-level process scheduling to limit CPU allocation

---

## 5. Implementation Checklist

- [ ] **Assessment Complete**: Identified Playwright MCP as source
- [ ] **Configuration Mapped**: Found in opencode.json and .clinerules/mcp.json
- [ ] **Recommendation Documented**: Removal recommended (Option A)
- [ ] **Implementation Pending**: User approval required for changes

---

## 6. Next Steps

| Step | Action                          | Owner     | Status  |
| ---- | ------------------------------- | --------- | ------- |
| 1    | Review this document            | User      | Pending |
| 2    | Approve suppression approach    | User      | Pending |
| 3    | Implement configuration changes | Developer | Pending |
| 4    | Verify error cessation          | QA        | Pending |

---

## 7. References

### Configuration Files

- `opencode.json` - OpenCode MCP configuration
- `.clinerules/mcp.json` - Cline MCP configuration

### Related Documentation

- Playwright MCP: `@playwright/mcp` npm package
- MCP Protocol: Model Context Protocol specification

---

## 8. Notes

- **Note 1**: The term "Chrome DevTools MCP" in the original issue refers to the Playwright MCP, which provides Chrome DevTools functionality
- **Note 2**: Firecrawl MCP was decommissioned per previous findings; this is a separate issue
- **Note 3**: This is a LOW priority operational issue - impacts resource efficiency but not functionality

---

**Document Status**: Ready for Review
**Last Updated**: 2026-02-19
**Author**: Kilo Code (Investigation Agent)
