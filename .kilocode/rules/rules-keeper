---
description: Keeper Analyzer mode rules for scanning portable VS Code environment
author: Project
version: 1.0
category: "Keeper Agent"
tags: ["keeper", "analyzer", "sync", "portable"]
globs: ["**/*"]
alwaysApply: false
---

# Keeper Analyzer Mode

## Purpose
Scan `C:\Users\pavel\vscodeportable\agentic\` for templates and compare with local project configurations.

## Source Directories

### Read-Only Analysis
Always scan these directories for templates:
```
C:/Users/pavel/vscodeportable/agentic/
├── kilocode-rules/           # Core Kilo Code rules
│   ├── rules/               # General rules
│   ├── rules-architect/     # Architect mode rules
│   ├── rules-code/         # Code mode rules
│   └── rules-debug/        # Debug mode rules
├── prompts/
│   ├── .clinerules/        # 27 Cline community rules
│   └── workflows/          # Workflow templates
├── bmad-skills/            # BMAD skills package
├── bmad-workflow-automation/ # BMAD workflows
├── servers/                # MCP reference servers (read-only)
└── templates/              # Project templates
```

## Analysis Workflow

### Step 1: Scan Source
1. Use `list_files` to scan `C:/Users/pavel/vscodeportable/agentic/`
2. Identify available templates in each category
3. Note version/timestamps where available
4. Build source inventory

### Step 2: Compare with Local
1. Scan local `.kilocode/` directory
2. Compare file lists
3. Identify missing templates
4. Identify newer versions
5. Identify local customizations

### Step 3: Report Findings
Present analysis in format:
```
## Keeper Analysis Report

### Source: C:\Users\pavel\vscodeportable\agentic\

| Template | Source Version | Local Version | Status |
|----------|----------------|---------------|---------|
| plan.md | 2026-02-10 | 2026-02-11 | ✅ Up to date |
| implement.md | 2026-02-10 | Missing | ⚠️ Missing |

### Missing Templates
- rules-code/implement.md
- workflows/create-new-workflow.md

### Local Customizations
- rules-code/custom-rules.md (project-specific)
```

## Commands

### Analyze All
```
Request: "Keeper analyze all"
```
Scans all source directories and compares with local.

### Analyze Specific
```
Request: "Keeper analyze workflows"
```
Scans only workflows category.

### Check Version
```
Request: "Keeper check plan.md"
```
Checks specific template version.

## Safety Rules
- ✅ Always read-only analysis first
- ✅ Show differences before importing
- ✅ Require user confirmation for any changes
- ✅ Preserve local customizations
- ✅ Create backup before modifications
