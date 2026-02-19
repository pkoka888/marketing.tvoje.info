# Consolidated Action Plan - Phase 2

## Overview
This plan addresses all hardcoded path issues identified in the parallel audit that break cross-platform compatibility and prevent MCP servers from starting properly.

## Issues Summary
- **54 total issues** (42 critical, 12 high priority)
- **Root cause**: Git Bash paths (`/c/...`) not compatible with Node.js execution
- **Impact**: 9 out of 11 MCP servers failing to start
- **Affected files**: 4 MCP config files, 2 GitHub workflow files

## Priority Matrix

### P0 - CRITICAL (Fix Today)
**Impact**: MCP servers completely broken, deployment fails

| Issue | File | Fix Required | Status |
|-------|------|--------------|--------|
| Git Bash paths in MCP configs | All 4 MCP files | Convert `/c/...` → `C:/...` | ❌ |
| Hardcoded IPs in workflows | deploy.yml, deploy-litellm.yml | Move to secrets | ❌ |
| Hardcoded ports in workflows | deploy.yml | Move to secrets | ❌ |

### P1 - HIGH (This Week)
**Impact**: Cross-platform compatibility issues

| Issue | File | Fix Required | Status |
|-------|------|--------------|--------|
| User-specific paths | All MCP files | Use `$HOME` or relative paths | ❌ |
| Project-specific paths | All MCP files | Use relative paths | ❌ |

### P2 - MEDIUM (Next Sprint)
**Impact**: Long-term maintainability

| Issue | File | Fix Required | Status |
|-------|------|--------------|--------|
| Cross-platform strategy | All configs | Platform detection | ❌ |
| Standardize path format | All configs | Choose consistent approach | ❌ |

## Implementation Plan

### Phase 1: Emergency MCP Fix (P0)
1. **Fix MCP server paths** - Convert all `/c/...` to `C:/...`
2. **Move hardcoded IPs to secrets** - Update GitHub workflows
3. **Test MCP servers** - Verify all 11 servers start successfully

### Phase 2: Cross-Platform Compatibility (P1)
1. **Replace user-specific paths** - Use environment variables
2. **Fix project-specific paths** - Use relative paths
3. **Update all configurations** - Ensure consistency

### Phase 3: Long-term Strategy (P2)
1. **Implement platform detection** - Handle Windows vs Unix paths
2. **Create wrapper scripts** - Abstract path differences
3. **Document standards** - Prevent future issues

## Files to Modify

### MCP Configuration Files (4 files)
- `.kilocode/mcp.json`
- `.clinerules/mcp.json`
- `.antigravity/mcp.json` (if exists)
- `opencode.json`

### GitHub Workflow Files (2 files)
- `.github/workflows/deploy.yml`
- `.github/workflows/deploy-litellm.yml`

## Success Criteria

### P0 Success
- [ ] All 11 MCP servers start without errors
- [ ] No hardcoded IPs in workflows
- [ ] Deployment works with secrets

### P1 Success
- [ ] All configs use cross-platform paths
- [ ] No user-specific paths
- [ ] Project works on different user accounts

### P2 Success
- [ ] Platform detection working
- [ ] Wrapper scripts functional
- [ ] Documentation updated

## Risk Assessment

### High Risk
- **MCP server failures** - Currently blocking development
- **Deployment failures** - Hardcoded IPs prevent CI/CD

### Medium Risk
- **Cross-platform issues** - Will break on other systems
- **User account dependency** - Won't work for other developers

### Low Risk
- **Maintenance overhead** - Inconsistent path formats

## Rollback Plan
If fixes cause issues:
1. **Git revert** - All changes are in version control
2. **Backup configs** - Original files can be restored
3. **Gradual rollout** - Fix one file at a time

## Next Steps
1. Start with P0 fixes (MCP servers)
2. Test each fix immediately
3. Move to P1 fixes (cross-platform)
4. Document final solution