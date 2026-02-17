# Antigravity IDE Configuration

This directory contains Antigravity-specific configuration for the marketing portfolio project.

## Overview

**Google Antigravity** is Google's agent-first development platform (AI IDE) launched November 2025. It provides:

- Agent-centric development (autonomous agents that plan, execute, verify)
- Gemini 3 Pro integration (free, 1M tokens/day)
- MCP (Model Context Protocol) support
- Cross-interface synergy (AI controls Editor, Terminal, Browser)

## Integration Status (2026)

This project is fully integrated with the **Unified Agentic Platform**.

- **Configuration**: `GEMINI.md` synced with `AGENTS.md`
- **Skills**: `.agent/skills/` (Astro Portfolio, DevOps)
- **Workflows**: `.agent/workflows/`
- **Fallback**: Gemini -> OpenCode -> Kilo Code

## Installation

```
Download: https://antigravity.google/download
Platform: Windows, macOS, Linux
Requirement: Personal Gmail account for public preview
```

## Configuration Files

| File         | Purpose                               |
| ------------ | ------------------------------------- |
| `mcp.json`   | MCP servers configuration             |
| `skills/`    | Custom agent skills (SKILL.md format) |
| `workflows/` | Reusable workflow definitions         |

## MCP Servers

Configure MCP servers in `mcp.json`. These provide the AI with access to external tools and services.

### Example Configuration

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/Users/pavel/projects/marketing.tvoje.info"
      ]
    }
  }
}
```

### Available MCP Servers

- **memory** - Persistent knowledge graph
- **filesystem** - Local file access
- **git** - Git operations
- **github** - GitHub API integration
- **fetch** - Web fetching
- **redis** - Rate limiting & coordination

## Agent Skills

Create skills in the `skills/` folder. Each skill is a directory with `SKILL.md`.

### Skill Structure

```
skills/
├── astro-portfolio/
│   └── SKILL.md
├── devops/
│   └── SKILL.md
└── general/
    └── SKILL.md
```

### SKILL.md Template

```markdown
# Skill Name

Brief description of what this skill does.

## When to Use

- Scenario 1
- Scenario 2

## Instructions

Detailed instructions for the agent...

## Examples

Example 1:
```

## Best Practices

Based on 2026 research:

### Agent Workflow

1. **Break tasks** into 15-30 minute chunks
2. **Produce artifacts**: Plans, Walkthroughs, Diffs
3. **Provide context** with examples
4. **Review early and often**
5. **Trust but verify** - maintain human oversight

### Code Standards

- Use strong typing - avoid `any` types
- Implement comprehensive error handling
- Write tests for agent-generated code
- Document complex logic

### Design Aesthetics (for UI work)

- Use vibrant, curated color palettes
- Implement glassmorphism and subtle gradients
- Add micro-animations for smooth interactions
- Use modern typography (Inter, Roboto, Outfit)
- Create premium, state-of-the-art interfaces

## Integration with Project

This project uses a **multi-agent platform** approach:

| Tool            | Purpose              | Model               |
| --------------- | -------------------- | ------------------- |
| **Antigravity** | High-capacity AI IDE | Gemini 3 Pro (free) |
| **Kilo Code**   | Bulk coding          | z-ai/glm4.7 (free)  |
| **OpenCode**    | Primary coding       | groq/llama-3.3-70b  |
| **Cline**       | VS Code integration  | minimax:free        |
| **Claude Code** | Deep reasoning       | claude-sonnet-4-5   |

## Commands

| Action         | Command             |
| -------------- | ------------------- |
| Run agent      | `Cmd+K` or `Ctrl+K` |
| Accept diff    | `Cmd+S` / `Ctrl+S`  |
| Cancel         | `Escape`            |
| New agent task | `Cmd+Shift+I`       |

## Notes

- Antigravity MCP config follows: https://antigravity.google/docs/mcp
- Agent Skills follow: https://antigravity.codes/blog/mastering-agent-skills
- Project rules synced from `.kilocode/rules/` and `.agent/`

## Resources

- [Official Docs](https://antigravity.google/docs)
- [Community](https://antigravity.codes)
- [Skill Vault](https://github.com/rmyndharis/antigravity-skills)
- [MCP Servers](https://antigravity.codes/mcp)
