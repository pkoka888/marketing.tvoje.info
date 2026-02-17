# Antigravity Agent Review Prompt

Use this prompt in **Google Antigravity** to review and enhance the unified agentic platform configuration.

---

## Context

You are working with a marketing portfolio project that uses **5 AI coding tools** simultaneously:

1. **Antigravity** (Gemini 3 Pro) - Primary high-capacity AI IDE
2. **Kilo Code** (z-ai/glm4.7) - Bulk coding
3. **OpenCode** (groq/llama-3.3-70b) - Standard coding
4. **Cline** (minimax:free) - VS Code integration
5. **Claude Code** (claude-sonnet-4-5) - Deep reasoning

## Research Findings

### Antigravity Configuration (Key Discovery!)

- Antigravity reads **GEMINI.md** specifically (NOT AGENTS.md!)
- Skills location: `.agent/skills/` (project) or `~/.gemini/antigravity/skills/` (global)
- MCP config: `.antigravity/mcp.json`

### Configuration Comparison

| Feature      | Antigravity       | OpenCode             | Kilo                 | Cline                  |
| ------------ | ----------------- | -------------------- | -------------------- | ---------------------- |
| Project File | GEMINI.md         | AGENTS.md            | N/A                  | N/A                    |
| Skills       | .agent/skills/    | .opencode/skill/     | .kilocode/skills/    | .clinerules/skills/    |
| Workflows    | .agent/workflows/ | .opencode/workflows/ | .kilocode/workflows/ | .clinerules/workflows/ |

## Your Task

Review the following files and **make improvements**:

### Files to Review

1. **`GEMINI.md`** - Main Antigravity config
2. **`.antigravity/README.md`** - Documentation (just created)
3. **`.antigravity/mcp.json`** - MCP servers
4. **`plans/INTEGRATION_PLAN.md`** - Full integration plan

### Specific Tasks

1. **Enhance GEMINI.md**
   - Add better instructions for cross-agent coordination
   - Include fallback strategy when Gemini is unavailable
   - Add skill references

2. **Create Skills**
   - Create `.agent/skills/astro-portfolio/SKILL.md` based on existing `.opencode/skill/astro-portfolio/SKILL.md`
   - Create `.agent/skills/devops/SKILL.md` for server operations

3. **Verify Configuration**
   - Ensure MCP servers are correctly configured
   - Check that all paths exist
   - Verify JSON/YAML syntax

4. **Documentation**
   - Update `.antigravity/README.md` with any findings
   - Add any missing best practices

## Key Directories

| Path            | Purpose                  |
| --------------- | ------------------------ |
| `src/`          | Astro source code        |
| `.kilocode/`    | Kilo Code config         |
| `.clinerules/`  | Cline rules              |
| `.opencode/`    | OpenCode config          |
| `.agent/`       | Antigravity workflows    |
| `.antigravity/` | Antigravity config (new) |
| `plans/`        | Planning documents       |

## Commands to Run

After modifications:

```bash
npm run build    # Verify build passes
npm run lint    # Check for errors
```

## Output Requirements

1. List all files you modified
2. Explain each change
3. Note any issues found
4. Provide recommendations for future improvements

---

## Important Notes

- This project follows **free-model-first** principle
- Use Gemini 3 Pro as primary (1M tokens/day free)
- Fallback to Groq/Kilo when Gemini unavailable
- Always run verification after changes
