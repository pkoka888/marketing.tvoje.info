---
description: Keeper Sync mode rules for synchronizing with portable VS Code environment
author: Project
version: 1.0
category: "Keeper Agent"
tags: ["keeper", "sync", "portable", "synchronization"]
globs: ["**/*"]
alwaysApply: false
---

# Keeper Sync Mode

## Purpose
Synchronize local project configurations with portable VS Code templates.

## Sync Strategy

### Three-Way Sync
```
Source: C:\Users\pavel\vscodeportable\agentic\
Target: .kilocode/ (local project)
Local:  Custom rules (never overwrite)
```

## Sync Commands

### Full Sync
```
Request: "Keeper sync all"
```
Syncs all categories from source.

### Category Sync
```
Request: "Keeper sync workflows"
```
Syncs only workflows category.

### Specific File
```
Request: "Keeper sync plan.md"
```
Syncs specific file from source.

## Safety Protocol

1. Create backup before sync
2. Show diff of changes
3. Require user confirmation
4. Preserve local customizations

## Protected Files

Never overwrite:
- `.clinerules/astro-portfolio.md`
- `.clinerules/tailwind-css.md`
- `.clinerules/accessibility-rules.md`
- `.clinerules/i18n-content.md`
- `.kilocode/rules/memory-bank/`

## Rollback
```
Request: "Keeper rollback"
```
Restores from backup.
