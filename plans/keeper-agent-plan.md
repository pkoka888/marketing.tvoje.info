# Keeper Agent Plan

**Created:** 2026-02-11
**Purpose:** Bridge portable VS Code environment with project configurations

## Overview

The "Keeper" agent/mode will synchronize configurations between:
- **Global Source:** `C:\Users\pavel\vscodeportable\` - Portable VS Code with extensions, configs, and agents
- **Local Projects:** Individual project directories with local `.kilocode/` configurations

## Directory Analysis

### Source: `C:\Users\pavel\vscodeportable\`

| Component | Location | Purpose |
|-----------|----------|---------|
| **kilocode-rules** | `agentic/kilocode-rules/` | Core Kilo Code rules templates |
| **prompts** | `agentic/prompts/.clinerules/` | 27 Cline community rules |
| **BMAD bundles** | `agentic/bmad-bundles/` | BMAD Method bundles |
| **BMAD skills** | `agentic/bmad-skills/` | Agent skills package |
| **BMAD workflows** | `agentic/bmad-workflow-automation/` | Workflow automation |
| **MCP servers** | `agentic/servers/` | MCP reference servers |
| **Templates** | `agentic/templates/` | Project templates |
| **Cline** | `agentic/cline/` | Cline extension configuration |
| **Kilocode** | `agentic/kilocode/` | Kilo Code extension |
| ** antigravity** | `antigravity/` | VS Code extensions |

### Target: Project `.kilocode/`

| Component | Purpose |
|-----------|---------|
| `rules/` | General rules + memory-bank |
| `rules-architect/` | Architect mode rules |
| `rules-code/` | Code mode rules |
| `rules-debug/` | Debug mode rules |
| `rules-ask/` | Ask mode rules |
| `modes/` | Mode definitions |
| `skills/` | Project skills |
| `workflows/` | Workflow definitions |
| `mcp.json` | MCP server configuration |

## Keeper Agent Responsibilities

### 1. Analyzer
- Scan `C:\Users\pavel\vscodeportable\agentic\` for new/updated templates
- Compare with project `.kilocode/` configurations
- Identify missing or outdated configurations
- Track version differences

### 2. Importer
- Copy new rules from templates to project
- Adapt rules to project-specific context
- Merge configurations without overwriting
- Handle conflicts intelligently

### 3. Sync Manager
- Keep local rules synchronized with global templates
- Preserve project-specific customizations
- Track template sources for each rule
- Provide update recommendations

### 4. Documentation
- Document all imported configurations
- Track template sources
- Maintain changelog of updates
- Provide audit trail

## Implementation Plan

### Phase 1: Analysis Mode
Create `.kilocode/rules-keeper/analyze.md`:
- Scan portable directory structure
- Identify available templates
- Compare versions
- Report differences

### Phase 2: Import Workflow
Create `.kilocode/workflows/import-from-keeper.md`:
- Select templates to import
- Adapt to project context
- Handle conflicts
- Update documentation

### Phase 3: Sync Mode
Create `.kilocode/rules-keeper/sync.md`:
- Regular synchronization checks
- Version tracking
- Automatic updates (optional)
- Rollback capability

### Phase 4: Documentation
Create `docs/KEEPER_GUIDE.md`:
- Usage instructions
- Best practices
- Troubleshooting
- Examples

## File Structure

```
.kilocode/
├── rules-keeper/           ✅ NEW
│   ├── analyze.md          ✅ NEW - Analysis mode rules
│   ├── sync.md            ✅ NEW - Sync mode rules
│   └── config.yaml        ✅ NEW - Keeper configuration
├── workflows/
│   ├── keeper-analyze.md  ✅ NEW - Analyze workflow
│   ├── keeper-import.md   ✅ NEW - Import workflow
│   └── keeper-sync.md     ✅ NEW - Sync workflow
└── mcp.json (reference)

docs/
└── KEEPER_GUIDE.md       ✅ NEW - Keeper documentation

.kilocode/
└── knowledge/
    └── keeper-sources.md  ✅ NEW - Reference to portable dir
```

## Configuration Example

```yaml
# .kilocode/rules-keeper/config.yaml
source:
  base_path: "C:/Users/pavel/vscodeportable/agentic"
  templates:
    - "kilocode-rules/"
    - "prompts/.clinerules/"
    - "bmad-skills/"
    - "bmad-workflow-automation/"
    - "servers/"

sync:
  auto_import: false
  backup_before_update: true
  keep_local_customizations: true

ignored:
  - "*.git/"
  - "node_modules/"
  - "dist/"
  - "build/"

custom_rules:
  - "astro-portfolio.md"    # Project-specific, don't overwrite
  - "tailwind-css.md"       # Project-specific, don't overwrite
  - "accessibility-rules.md" # Project-specific, don't overwrite
```

## Workflow Examples

### Analyze Workflow
```
User: "Analyze keeper sources"
Keeper: 
1. Scan portable directory
2. Compare versions with local
3. Report missing/new items
4. Recommend actions
```

### Import Workflow
```
User: "Import new workflows from templates"
Keeper:
1. List available workflows
2. User selects items
3. Adapt to project context
4. Create backup
5. Import files
6. Update documentation
```

### Sync Workflow
```
User: "Sync with keeper"
Keeper:
1. Check for updates
2. Show changes
3. User confirms
4. Apply updates (preserving customizations)
5. Report results
```

## Template Mapping

| Source | Destination | Notes |
|--------|-------------|-------|
| `kilocode-rules/rules/` | `.kilocode/rules/` | Core rules |
| `kilocode-rules/rules-*/` | `.kilocode/rules-*/` | Mode rules |
| `prompts/.clinerules/` | `.clinerules/` | Cline rules |
| `prompts/workflows/` | `.kilocode/workflows/` | Workflows |
| `bmad-skills/yaml/` | `.kilocode/skills/` | Skills |
| `bmad-workflow-automation/src/` | `.kilocode/workflows/` | BMAD workflows |
| `servers/` | Reference only | Don't copy MCP servers |

## Safety Considerations

### Read-Only Analysis
- Always scan in read-only mode first
- Show differences before making changes
- Require user confirmation for imports

### Backup Strategy
- Backup before any modifications
- Keep multiple backup versions
- Easy rollback capability

### Conflict Resolution
- Preserve local customizations
- Merge when possible
- Flag conflicts for user decision

## Next Steps

1. Create `.kilocode/rules-keeper/` directory
2. Implement analyze mode rules
3. Create import workflow
4. Create sync workflow
5. Write documentation
6. Test with sample templates

## References

- Template source: `C:\Users\pavel\vscodeportable\agentic\`
- BMAD Method: `agentic/BMAD-METHOD/`
- Cline prompts: `agentic/prompts/`
- MCP servers: `agentic/servers/`
