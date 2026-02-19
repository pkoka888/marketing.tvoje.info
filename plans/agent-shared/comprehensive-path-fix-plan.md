# Comprehensive Path Fix Plan - Phase 3

## Executive Summary

After analyzing the project architecture, MCP configurations, and agent systems, I've identified **additional issues** beyond the initial hardcoded paths that need to be addressed for a complete solution.

## Issues Discovered

### 1. **Memory Bank Missing** ❌
- **Problem**: `.kilocode/knowledge/memory-bank/` directory is empty
- **Impact**: No persistent project context, agents lose knowledge between sessions
- **Files Missing**: 
  - `agents-state.md`
  - `tasks-queue.md` 
  - `verification-history.md`
  - `brief.md`, `product.md`, `context.md`, `architecture.md`, `tech.md`, `servers.md`

### 2. **Antigravity MCP Configuration Incomplete** ⚠️
- **Problem**: `.antigravity/mcp.json` uses npx for most servers but has hardcoded paths
- **Impact**: Inconsistent with other agent frameworks, potential path resolution issues

### 3. **Health Monitor Script Path Dependencies** ⚠️
- **Problem**: `.agent/flows/health_monitor.py` has hardcoded paths in STATE_FILE
- **Impact**: Won't work on different user accounts or systems

### 4. **Verification Scripts Need Updates** ⚠️
- **Problem**: `scripts/verify-mcp-servers.js` and `scripts/fix-mcp-paths.js` have hardcoded paths
- **Impact**: Scripts won't work on different systems

### 5. **Environment Variables Not Standardized** ⚠️
- **Problem**: No consistent approach to environment variables across configs
- **Impact**: Cross-platform compatibility issues persist

## Updated Implementation Plan

### Phase 1: Complete MCP Path Resolution (P0) ✅ COMPLETED
- [x] Convert all `/c/...` paths to `C:/...` format
- [x] Fix project-specific paths to use relative paths
- [x] Move hardcoded IPs to GitHub secrets

### Phase 2: Memory Bank Infrastructure (P1) 🔄 IN PROGRESS
- [ ] Create complete memory bank structure
- [ ] Populate with project context
- [ ] Integrate with agent workflows

### Phase 3: Cross-Platform Environment Variables (P2) 📋 PENDING
- [ ] Standardize environment variable usage
- [ ] Create platform detection logic
- [ ] Update all configs to use env vars

### Phase 4: Agent System Integration (P3) 📋 PENDING
- [ ] Update Antigravity MCP config for consistency
- [ ] Fix health monitor script paths
- [ ] Update verification scripts

## Parallel Agent Implementation Strategy

### Agent 1: Memory Bank Architect
**Skills Required**: `bmad-discovery-research`, `bmad-story-planning`
**Task**: Create complete memory bank infrastructure
**Output**: 
- Memory bank structure in `.kilocode/knowledge/memory-bank/`
- Project context files
- Integration with existing agent workflows

### Agent 2: Environment Variable Specialist  
**Skills Required**: `bmad-discovery-research`, `bmad-code-review`
**Task**: Standardize environment variable usage across all configs
**Output**:
- Environment variable strategy document
- Updated MCP configs using env vars
- Platform detection logic

### Agent 3: Cross-Platform Compatibility Engineer
**Skills Required**: `bmad-discovery-research`, `bmad-performance-optimization`
**Task**: Fix remaining cross-platform issues
**Output**:
- Updated Antigravity MCP config
- Fixed health monitor script
- Updated verification scripts

### Agent 4: Integration Coordinator
**Skills Required**: `bmad-discovery-research`, `bmad-code-review`
**Task**: Ensure all changes work together
**Output**:
- Integration test plan
- Cross-agent compatibility verification
- Final documentation

## Implementation Commands

### For Memory Bank Architect:
```bash
# Create memory bank structure
mkdir -p .kilocode/knowledge/memory-bank
touch .kilocode/knowledge/memory-bank/{agents-state,tasks-queue,verification-history,brief,product,context,architecture,tech,servers}.md

# Populate with project context
# (Use bmad-discovery-research to gather context from existing files)
```

### For Environment Variable Specialist:
```bash
# Analyze current path usage
grep -r "C:/Users/pavel" .kilocode/ .clinerules/ opencode.json .antigravity/ --include="*.json"

# Create environment variable strategy
# Replace hardcoded paths with env vars
```

### For Cross-Platform Compatibility Engineer:
```bash
# Fix Antigravity MCP config
# Update health monitor script paths
# Update verification scripts
```

### For Integration Coordinator:
```bash
# Test all changes together
# Verify cross-agent compatibility
# Create final documentation
```

## Success Criteria

### Phase 2 Success (Memory Bank)
- [ ] Complete memory bank structure created
- [ ] All context files populated with relevant information
- [ ] Memory bank integrated with agent workflows
- [ ] Agents can access persistent project knowledge

### Phase 3 Success (Environment Variables)
- [ ] All hardcoded paths replaced with environment variables
- [ ] Platform detection logic working
- [ ] Cross-platform compatibility verified
- [ ] No hardcoded user-specific paths remain

### Phase 4 Success (Integration)
- [ ] All agent systems working together
- [ ] Cross-platform deployment working
- [ ] Health monitoring functional
- [ ] Verification scripts working on different systems

## Risk Assessment

### High Risk
- **Memory Bank Corruption**: Could lose project context
- **Agent Coordination Failure**: Multiple agents making conflicting changes

### Medium Risk  
- **Environment Variable Conflicts**: Different agents using different env var names
- **Platform Detection Failures**: Logic not working on some systems

### Low Risk
- **Documentation Inconsistency**: Different agents creating conflicting docs

## Rollback Plan
1. **Git Revert**: All changes are in version control
2. **Memory Bank Reset**: Can recreate from existing project files
3. **Environment Variables**: Can fall back to hardcoded paths temporarily
4. **Agent Coordination**: Can run agents sequentially instead of parallel

## Next Steps
1. **Start with Memory Bank Architect** - Foundation for all other work
2. **Coordinate agent execution** - Use proper synchronization
3. **Test each phase** - Verify before moving to next phase
4. **Document as you go** - Maintain clear audit trail

This comprehensive plan addresses all discovered issues and provides a clear path to complete resolution.