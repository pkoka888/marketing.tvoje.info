# Agent Configuration Structure

**Last Updated**: 2026-02-13
**Purpose**: Document correct file/folder placement for AI agent tools

---

## Overview

This project uses multiple AI agent tools, each with its own configuration structure. This document clarifies the correct placement of configuration files, rules, agents, skills, and workflows for each tool.

---

## Agent Tool Comparison

| Tool                           | Config File                        | Directory      | Purpose                |
| ------------------------------ | ---------------------------------- | -------------- | ---------------------- |
| **OpenCode CLI** (Antigravity) | `opencode.json`                    | `.opencode/`   | CLI-based AI assistant |
| **Kilo Code**                  | `.kilocode/custom-instructions.md` | `.kilocode/`   | VS Code extension      |
| **Cline**                      | `.clinerules/`                     | `.clinerules/` | CLI headless agent     |

---

## OpenCode CLI (Antigravity IDE)

### Configuration File: `opencode.json`

**Valid top-level keys** (from [official schema](https://opencode.ai/config.json)):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md", "path/to/rules.md"],
  "theme": "opencode",
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5",
  "provider": {},
  "agent": {},
  "default_agent": "build",
  "tools": {},
  "tui": {},
  "server": {},
  "mcp": {},
  "share": {}
}
```

**INVALID keys** (will cause validation errors):

- ❌ `"rules"` - Not part of the schema
- ❌ `"skills"` - Not a top-level key
- ❌ `"workflows"` - Not a top-level key

### Directory Structure: `.opencode/`

OpenCode CLI supports the following subdirectories (plural names preferred):

```
.opencode/
├── agents/       # Custom agent definitions (markdown files)
├── commands/     # Custom commands
├── modes/        # Custom modes
├── plugins/      # Plugins
├── skills/       # Skills
├── tools/        # Tools
└── themes/       # Themes
```

### Configuration Precedence

Config sources are loaded in this order (later sources override earlier ones):

1. Remote config (from `.well-known/opencode`)
2. Global config (`~/.config/opencode/opencode.json`)
3. Custom config (`OPENCODE_CONFIG` env var)
4. Project config (`opencode.json` in project)
5. `.opencode` directories
6. Inline config (`OPENCODE_CONFIG_CONTENT` env var)

### Instructions Array

The `instructions` key accepts an array of file paths to external instruction files:

```json
{
  "instructions": [
    "AGENTS.md",
    ".clinerules/validator.md",
    "C:/Users/pavel/vscodeportable/agentic/ai-prompts/prompts/astro-4/rule-astro-coding-standards.md"
  ]
}
```

---

## Kilo Code (VS Code Extension)

### Configuration Directory: `.kilocode/`

```
.kilocode/
├── custom-instructions.md    # Main instructions file
├── mcp.json                  # MCP server configuration
├── modes/                    # Custom mode definitions
├── rules/                    # Shared rules
│   └── memory-bank/          # Memory bank files
├── rules-architect/          # Architect mode rules
├── rules-code/               # Code mode rules
├── rules-debug/              # Debug mode rules
├── rules-ask/                # Ask mode rules
├── rules-keeper/             # Keeper agent rules
├── skills/                   # Skill definitions
├── workflows/                # Workflow definitions
└── knowledge/                # Knowledge base
```

### Mode-Specific Rules

Each mode can have its own rules directory:

- `rules-architect/` - Rules for Architect mode
- `rules-code/` - Rules for Code mode
- `rules-debug/` - Rules for Debug mode
- `rules-ask/` - Rules for Ask mode

### Skills Structure

```
.kilocode/skills/
├── skill-name/
│   ├── SKILL.md              # Main skill definition
│   ├── REFERENCE.md          # Reference documentation
│   ├── WORKFLOW.md           # Workflow steps
│   └── RULES.md              # Skill-specific rules
```

---

## Cline (CLI Headless)

### Configuration Directory: `.clinerules/`

```
.clinerules/
├── bmad-integration.md       # BMAD workflow integration
├── cost-optimization.md      # Cost optimization rules
├── plan-watcher.md           # Plan watcher rules
├── python-preferred.md       # Python-first policy
├── validator.md              # Validation rules
├── mcp-port-preservation.md  # MCP port rules
└── 98-visual-verification.md # Visual verification
```

---

## Current Project Structure

This project uses a hybrid approach:

```
marketing.tvoje.info/
├── opencode.json             # OpenCode CLI config (VALID)
├── .gemini/
│   └── GEMINI.md             # Antigravity-specific instructions
├── .agent/                   # Antigravity agent files
│   ├── agents.yaml           # Agent registry
│   ├── health-checks.yaml    # Health check definitions
│   ├── flows/                # LangGraph flows
│   └── reports/              # Generated reports
├── .kilocode/                # Kilo Code configuration
│   ├── mcp.json              # MCP server config
│   ├── rules/                # Shared rules
│   ├── rules-*/              # Mode-specific rules
│   ├── skills/               # Skills
│   ├── workflows/            # Workflows
│   └── knowledge/            # Knowledge base
├── .clinerules/              # Cline rules
└── AGENTS.md                 # Shared agent instructions
```

---

## Migration Required

### Issue Fixed

The `opencode.json` file contained an invalid `"rules"` key that caused validation errors:

```json
// REMOVED - Invalid key
"rules": {
  "visualVerification": {
    "enabled": true,
    "playwright": {
      "enabled": true,
      "headless": true
    }
  },
  "mcpPorts": {
    "redis": 36379,
    "playwright": 9222
  }
}
```

### Correct Placement

| Setting                   | Correct Location                             |
| ------------------------- | -------------------------------------------- |
| MCP port configuration    | `.kilocode/mcp.json`                         |
| Visual verification rules | `.clinerules/98-visual-verification.md`      |
| Playwright configuration  | `.kilocode/mcp.json` (Playwright MCP server) |

---

## Best Practices

### 1. Use `instructions` Array for Cross-Tool Rules

Reference shared rule files from `opencode.json`:

```json
{
  "instructions": ["AGENTS.md", ".clinerules/validator.md"]
}
```

### 2. Keep Tool-Specific Rules in Their Directories

- OpenCode CLI → `.opencode/` or referenced via `instructions`
- Kilo Code → `.kilocode/rules/`
- Cline → `.clinerules/`

### 3. Use AGENTS.md for Shared Instructions

The `AGENTS.md` file serves as the main instruction file for all agents:

- Agent registry
- Setup commands
- Architecture overview
- Key file locations
- Validation checklist

### 4. Memory Bank for Persistent Context

Store persistent project context in `.kilocode/rules/memory-bank/`:

- `brief.md` - Project brief
- `product.md` - Product description
- `context.md` - Current context
- `architecture.md` - System architecture
- `tech.md` - Technologies and setup

---

## Validation

### Validate OpenCode Configuration

```bash
# Check if opencode.json is valid
npx opencode --validate
```

### Validate MCP Configuration

```bash
# Validate MCP server configuration
npm run validate:mcp
```

---

## References

- [OpenCode CLI Documentation](https://opencode.ai/docs/config)
- [OpenCode Config Schema](https://opencode.ai/config.json)
- [AGENTS.md Standard](https://agents.md)
- [Kilo Code Documentation](https://kilocode.ai/docs)

---

## Changelog

| Date       | Change                                       |
| ---------- | -------------------------------------------- |
| 2026-02-13 | Fixed invalid `rules` key in `opencode.json` |
| 2026-02-13 | Created this documentation                   |
