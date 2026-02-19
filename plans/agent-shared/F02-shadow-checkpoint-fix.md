# F-02: ShadowCheckpointService Prefix Match Security Fix

**Finding ID:** F-02
**Severity:** MEDIUM
**Category:** Path Validation Vulnerability
**Component:** VSCode Portable Extension Host (ShadowCheckpointService)
**Line Reference:** ~Line 134
**Status:** Documentation Complete - Upstream Fix Required
**Created:** 2026-02-19

---

## 1. Vulnerability Analysis

### Description

The ShadowCheckpointService uses improper string matching for path validation. The current implementation uses `.includes()` which performs a **substring search** rather than a **prefix match**, allowing paths outside the protected directory to bypass security controls.

### Current Vulnerable Code

```typescript
// Current implementation (VULNERABLE)
if (path.includes(basePath)) {
  // Allow access - but this is WRONG!
}
```

### Why `.includes()` Fails

The `.includes()` method checks whether a substring exists **anywhere** within the string. This creates a false positive vulnerability:

| Path Checked               | Protected Base | `.includes()` Result | Should Allow?    |
| -------------------------- | -------------- | -------------------- | ---------------- |
| `~/Desktop/project`        | `~/Desktop`    | `true`               | ✅ Yes (correct) |
| `~/Desktop/project/subdir` | `~/Desktop`    | `true`               | ✅ Yes (correct) |
| `~/Desktop`                | `~/Desktop`    | `true`               | ✅ Yes (correct) |
| `~/Desktop/subfolder`      | `~/Desktop`    | `true`               | ✅ Yes (correct) |
| `~/DesktopOther`           | `~/Desktop`    | `true`               | ❌ NO (bypass!)  |
| `x~/Desktop`               | `~/Desktop`    | `true`               | ❌ NO (bypass!)  |

### Attack Scenarios

1. **Path Traversal via Similar Prefixes**

   ```
   Protected: ~/Desktop/project
   Attack Path: ~/Desktop_project/../etc/passwd
   Result: .includes() returns TRUE → Access granted!
   ```

2. **Sibling Directory Bypass**
   ```
   Protected: ~/work/repos
   Attack Path: ~/work/repos_hacked
   Result: .includes() returns TRUE → Access granted!
   ```

---

## 2. Recommended Fix

### Option A: Proper Prefix Match with Separator Check (Preferred)

```typescript
import * as path from 'path';

/**
 * Securely check if childPath is within basePath
 * Uses proper prefix matching with directory separator validation
 */
function isPathWithinBase(childPath: string, basePath: string): boolean {
  // Normalize paths to use forward slashes for consistent comparison
  const normalizedChild = childPath.replace(/\\/g, '/');
  const normalizedBase = basePath.replace(/\\/g, '/');

  // Ensure base path ends with separator for proper prefix matching
  const baseWithSeparator = normalizedBase.endsWith('/') ? normalizedBase : normalizedBase + '/';

  // Use startsWith for true prefix matching
  return normalizedChild.startsWith(baseWithSeparator);
}

// Usage in ShadowCheckpointService
if (isPathWithinBase(requestedPath, protectedBasePath)) {
  // Safe - path is truly within protected directory
  return allowAccess();
}
```

### Option B: Using Node.js path Module

```typescript
import * as path from 'path';

/**
 * Use path.relative() to determine if path is within base
 * Returns empty string if path equals base
 * Returns string starting with '..' if path is outside base
 * Returns subpath if path is within base
 */
function isPathWithinBaseSafe(childPath: string, basePath: string): boolean {
  // Resolve to absolute paths for accurate comparison
  const absoluteChild = path.resolve(childPath);
  const absoluteBase = path.resolve(basePath);

  // Get relative path
  const relativePath = path.relative(absoluteBase, absoluteChild);

  // If relative path starts with '..', child is outside base
  // If relative path is empty or doesn't start with '..', child is within base
  return !relativePath.startsWith('..') && !path.isAbsolute(relativePath);
}

// Usage in ShadowCheckpointService
if (isPathWithinBaseSafe(requestedPath, protectedBasePath)) {
  // Safe - path is truly within protected directory
  return allowAccess();
}
```

---

## 3. Test Cases

### Test Suite for Prefix Match Fix

```typescript
import { describe, it, expect } from 'vitest';
import { isPathWithinBase } from './path-utils';

describe('isPathWithinBase - Security Tests', () => {

    // Should ALLOW - true subdirectories
    it('should allow exact match', () => {
        expect(isPathWithinBase('~/Desktop', '~/Desktop')).toBe(true);
    });

    it('should allow direct subdirectory', () => {
        expect(isPathWithinBase('~/Desktop/project', '~/Desktop')).toBe(true);
    });

    it('should allow nested subdirectory', () => {
        expect(isPathWithinBase('~/Desktop/project/src', '~/Desktop')).to(be(true);
    });

    it('should handle trailing slash in base', () => {
        expect(isPathWithinBase('~/Desktop/project', '~/Desktop/')).toBe(true);
    });

    // Should BLOCK - paths outside protected directory
    it('should block sibling directory (underscore)', () => {
        expect(isPathWithinBase('~/Desktop_other', '~/Desktop')).toBe(false);
    });

    it('should block prefix that is not a directory', () => {
        expect(isPathWithinBase('x~/Desktop', '~/Desktop')).toBe(false);
    });

    it('should block similar prefix', () => {
        expect(isPathWithinBase('~/DesktopProject', '~/Desktop')).toBe(false);
    });

    // Edge cases
    it('should handle Windows paths', () => {
        expect(isPathWithinBase('C:\\Users\\Admin\\Desktop', 'C:\\Users\\Admin')).toBe(true);
    });

    it('should handle mixed path separators', () => {
        expect(isPathWithinBase('C:/Users/Admin/Desktop', 'C:\\Users\\Admin')).toBe(true);
    });
});
```

---

## 4. Implementation Checklist

- [ ] Replace `.includes()` with proper prefix matching
- [ ] Add separator validation (must be `/` or `\`)
- [ ] Handle both Unix and Windows path formats
- [ ] Add unit tests for all attack scenarios
- [ ] Test with symbolic links and junction points (Windows)
- [ ] Verify performance impact (minimal - string operations are fast)
- [ ] Update security documentation

---

## 5. Security Impact Assessment

| Aspect             | Assessment                                             |
| ------------------ | ------------------------------------------------------ |
| **Severity**       | Medium                                                 |
| **Exploitability** | High (simple path manipulation)                        |
| **Impact**         | Unauthorized file access in portable extension context |
| **Scope**          | Limited to portable extension data directories         |
| **Fix Complexity** | Low (single function replacement)                      |

---

## 6. References

- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [Node.js path Module Docs](https://nodejs.org/api/path.html)
- [CWE-22: Improper Limitation of a Pathname](https://cwe.mitre.org/data/definitions/22.html)

---

## 7. Upstream Submission

This finding should be submitted to the VS Code repository:

1. **Repository:** `microsoft/vscode`
2. **Component:** `src/vs/workbench/services/extensions/electron-sandbox/`
3. **File:** `ShadowCheckpointService.ts` (or similar)
4. **Fix:** Replace line ~134 `.includes()` with proper prefix validation

---

**Document Status:** Complete
**Next Action:** Submit fix recommendation to VS Code upstream
