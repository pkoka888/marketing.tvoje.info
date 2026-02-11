# Keeper Sources Reference

**Last Updated:** 2026-02-11

## Source Directory

All templates are sourced from:
```
C:\Users\pavel\vscodeportable\agentic\
```

This is a read-only portable VS Code environment that contains:
- Template configurations
- Agent rules and workflows
- MCP server configurations
- Community prompts and skills

## Source Components

### 1. kilocode-rules
**Path:** `C:\Users\pavel\vscodeportable\agentic\kilocode-rules\`

| Source | Purpose | Sync Status |
|--------|---------|--------------|
| `rules/` | Core rules templates | Merge |
| `rules-architect/` | Architect mode rules | Merge |
| `rules-code/` | Code mode rules | Merge |
| `rules-debug/` | Debug mode rules | Merge |

### 2. prompts
**Path:** `C:\Users\pavel\vscodeportable\agentic\prompts\`

| Source | Purpose | Sync Status |
|--------|---------|--------------|
| `.clinerules/` | 27 Cline community rules | Copy |
| `workflows/` | Workflow templates | Copy |

### 3. bmad-skills
**Path:** `C:\Users\pavel\vscodeportable\agentic\bmad-skills\`

| Source | Purpose | Sync Status |
|--------|---------|--------------|
| `yaml/` | BMAD skills | Copy |
| `README.md` | Skills documentation | Copy |

### 4. bmad-workflow-automation
**Path:** `C:\Users\pavel\vscodeportable\agentic\bmad-workflow-automation\`

| Source | Purpose | Sync Status |
|--------|---------|--------------|
| `src/` | BMAD workflows | Merge |

### 5. servers (Read-Only)
**Path:** `C:\Users\pavel\vscodeportable\agentic\servers\`

| Source | Purpose | Sync Status |
|--------|---------|--------------|
| All MCP servers | Reference only | Do not copy |

### 6. antigravity
**Path:** `C:\Users\pavel\vscodeportable\antigravity\`

VS Code extensions installed in portable environment (reference only).

## Template Mapping

| Source Path | Local Destination | Action |
|-------------|------------------|--------|
| `kilocode-rules/rules/*` | `.kilocode/rules/` | Merge |
| `kilocode-rules/rules-*/*` | `.kilocode/rules-*/` | Merge |
| `prompts/.clinerules/*` | `.clinerules/` | Copy |
| `prompts/workflows/*` | `.kilocode/workflows/` | Copy |
| `bmad-skills/yaml/*` | `.kilocode/skills/` | Copy |
| `bmad-workflow-automation/src/*` | `.kilocode/workflows/` | Merge |
| `servers/*` | Reference only | Don't copy |

## Protected Files

These project-specific files are NEVER overwritten during sync:
- `.clinerules/astro-portfolio.md`
- `.clinerules/tailwind-css.md`
- `.clinerules/accessibility-rules.md`
- `.clinerules/i18n-content.md`
- `.kilocode/rules/memory-bank/*`

## Sync History

| Date | Action | Details |
|------|--------|---------|
| 2026-02-11 | Initial Setup | Created Keeper configuration |

## Usage Commands

### Analyze Sources
```
Request: "Keeper analyze all"
```
Scans all source directories and compares with local.

### Import Templates
```
Request: "Keeper import workflows"
```
Imports selected templates from source.

### Sync Configurations
```
Request: "Keeper sync all"
```
Synchronizes local with source, preserving customizations.

### Rollback
```
Request: "Keeper rollback"
```
Restores from last backup.

## Safety Rules

1. Always read-only analysis first
2. Show diff before making changes
3. Require user confirmation
4. Create backup before modifications
5. Preserve local customizations

## References

- Keeper Plan: `/plans/keeper-agent-plan.md`
- Analyze Rules: `.kilocode/rules-keeper/analyze.md`
- Sync Rules: `.kilocode/rules-keeper/sync.md`
- Workflows: `.kilocode/workflows/keeper-*.md`
