# Custom Modes

This directory contains **documentation-only** files for custom Kilo Code modes.

## Configuration Location

The **actual mode configuration** is in `.kilocodemodes` at the project root, NOT in this directory.

```
marketing.tvoje.info/
├── .kilocodemodes          # ← Actual Kilo Code configuration (YAML)
└── .kilocode/modes/        # ← Documentation only (this directory)
    ├── README.md
    ├── server-monitor/
    │   └── MODE.md
    └── sysadmin/
        └── MODE.md
```

## Available Modes (10 total)

| Slug | Name | Purpose |
|------|------|---------|
| `analyst` | BMAD Analyst | Market research, competitive analysis, SWOT |
| `architect` | BMAD Architect | System design, API architecture |
| `dev` | BMAD Developer | Code implementation, dev stories |
| `pm` | BMAD Product Manager | Sprint planning, backlog management |
| `qa` | BMAD QA Engineer | Testing, validation, quality |
| `sm` | BMAD Scrum Master | Agile facilitation, story planning |
| `ux` | BMAD UX Designer | UX design, wireframes, user flows |
| `solo` | BMAD Solo Developer | Rapid prototyping, quick iterations |
| `server-monitor` | Server Monitor | Server diagnostics, evidence collection |
| `sysadmin` | System Administrator | Server management, infrastructure |

## Mode Documentation Structure

Each subdirectory contains a `MODE.md` file with:

- **YAML frontmatter**: Mode metadata (slug, name, role, etc.)
- **Detailed description**: Purpose and capabilities
- **Usage guidelines**: When and how to use the mode
- **Custom instructions**: Mode-specific rules

## Creating New Modes

1. **Add to `.kilocodemodes`** (project root):

```yaml
- slug: new-mode
  name: New Mode Name
  roleDefinition: |
    You are a [role description].
  groups: [read, edit, command, mcp]
  customInstructions: |
    Additional instructions here.
```

2. **Create documentation** (this directory):

```bash
mkdir .kilocode/modes/new-mode
touch .kilocode/modes/new-mode/MODE.md
```

3. **Document the mode** in `MODE.md` with YAML frontmatter and markdown content.

## Official Documentation

- Kilo Code Modes: https://kilo.ai/docs/modes
- Custom Modes Guide: https://kilo.ai/docs/custom-modes

## Related Files

- `.kilocodemodes` - Actual mode configuration (YAML)
- `.kilocode/rules-code/` - Code mode rules
- `.kilocode/rules-architect/` - Architect mode rules
- `.kilocode/rules-keeper/` - Keeper mode rules
