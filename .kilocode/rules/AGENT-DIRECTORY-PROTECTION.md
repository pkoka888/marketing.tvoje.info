---
description:
  Protection rules for agent configuration directories - prevents unauthorized
  modifications
---

# Agent Directory Protection Rule

**Rule ID**: AGENT-PROTECT-001 **Applies to**: All AI agents (Kilo, Cline,
OpenCode, Antigravity) **Priority**: CRITICAL

## Core Principle

Agent configuration directories (`.kilocode/`, `.clinerules/`, `.antigravity/`,
`.opencode/`, `.claude/`, `.gemini/`, `.agents/`) contain sensitive settings
that affect how ALL agents operate. Changes to these directories require
explicit human approval.

## Protected Directories

The following directories are PROTECTED and require explicit approval for
modifications:

```
.kilocode/          # Kilo Code configuration
.clinerules/        # Cline configuration
.antigravity/       # Antigravity configuration
.opencode/          # OpenCode configuration
.claude/            # Claude Code configuration
.gemini/            # Gemini CLI configuration
.agents/            # BMAD Squad configuration
.vscode/            # VS Code settings (if contains agent configs)
```

## Specific Protections

### 1. MCP Configuration Files

**Protected Files:**

- `.kilocode/mcp.json`
- `.clinerules/mcp.json`
- `.antigravity/mcp.json`
- `opencode.json` (mcp section)
- `.claude/mcp.json`
- `.gemini/mcp.json`

**Restrictions:**

- ❌ DO NOT add new MCP servers without approval
- ❌ DO NOT modify existing MCP server configurations
- ❌ DO NOT change `alwaysAllow` arrays
- ❌ DO NOT modify paths in filesystem servers
- ✅ MAY read and analyze current configurations
- ✅ MAY document current state

**Why:** MCP configurations control which external tools agents can access.
Incorrect changes can:

- Break existing functionality
- Grant unintended permissions
- Expose sensitive directories
- Break cross-agent compatibility

### 2. Agent Rule Files

**Protected Files:**

- `.kilocode/rules/*`
- `.clinerules/skills/*`
- `.antigravity/skills/*`
- `.opencode/skill/*`
- `.claude/settings.json`
- `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`

**Restrictions:**

- ❌ DO NOT modify existing rules
- ❌ DO NOT add new rules without approval
- ❌ DO NOT delete rules
- ✅ MAY read and reference rules
- ✅ MAY suggest new rules (but don't implement)

### 3. Mode Configuration Files

**Protected Files:**

- `.kilocodemodes`
- `.clinerules/modes/*`
- `.opencode/agent/*`

**Restrictions:**

- ❌ DO NOT modify mode definitions
- ❌ DO NOT add new modes
- ✅ MAY read current modes

### 4. Workflow Files

**Protected Files:**

- `.kilocode/workflows/*`
- `.clinerules/workflows/*`
- `.antigravity/workflows/*`
- `.opencode/command/*`

**Restrictions:**

- ❌ DO NOT modify workflows
- ❌ DO NOT add new workflows
- ✅ MAY read and execute workflows

## Exception Process

If a change to protected directories is genuinely needed:

1. **STOP** - Do not make the change
2. **ANALYZE** - Document what needs to change and why
3. **PROPOSE** - Present to user with:
   - Current state
   - Proposed change
   - Justification
   - Risk assessment
4. **WAIT** - Only proceed after explicit user approval

## Cross-Agent Synchronization

**CRITICAL:** Many configuration files are MIRRORS of each other:

```
.kilocode/rules/cost-optimization
.clinerules/skills/cost-optimization.md
.agents/rules/cost-optimization.md
.gemini/rules/cost-optimization.md
```

**Rules:**

- ❌ DO NOT modify one without checking others
- ❌ DO NOT create inconsistencies between agents
- ✅ If change approved, update ALL mirrored files
- ✅ Use `scripts/verify_agentic_platform.py` after changes

## Safe Operations (No Approval Needed)

The following operations are SAFE and don't require approval:

### Reading/Analyzing

- Read any config file to understand current state
- Analyze configurations for issues
- Document current settings
- Compare configurations between agents

### Project-Specific Files

- `.kilocode/knowledge/*` - Project knowledge (safe to modify)
- `.clinerules/memory-bank/*` - Memory bank (safe to modify)
- `.kilocode/rules/memory-bank/*` - Memory bank (safe to modify)
- `.kilocode/skills/*` - Custom skills (safe to modify)

### Testing/Validation

- Run validation scripts
- Test MCP server connectivity
- Verify configurations

## Red Flags - Immediate Stop

STOP and ask for approval if you see:

1. **Multiple agents modifying same file** - Coordinate first
2. **Path changes in filesystem MCP servers** - High risk
3. **Permission changes (alwaysAllow)** - Security risk
4. **New MCP servers being added** - Requires cross-agent check
5. **Rule deletions** - May break workflows

## Best Practices

1. **When in doubt, ask** - Better to wait for approval than break configs
2. **Document everything** - Note what you read and why
3. **Read before proposing** - Understand current state first
4. **Check mirrors** - Look for equivalent files in other agent dirs
5. **Use verification** - Run verify_agentic_platform.py after any approved
   change

## Examples

### ❌ WRONG - Direct Modification

```
User: "Add a new MCP server for database"
Agent: [Directly edits .kilocode/mcp.json]
```

### ✅ RIGHT - Proposal First

```
User: "Add a new MCP server for database"
Agent: "I can help with that. Let me first check the current MCP configurations across all agents...

Current state:
- .kilocode/mcp.json has 8 MCP servers
- .clinerules/mcp.json has 6 MCP servers
- .antigravity/mcp.json has 5 MCP servers

To add a database MCP server, I would need to:
1. Update .kilocode/mcp.json
2. Update .clinerules/mcp.json
3. Update .antigravity/mcp.json
4. Update opencode.json

Proposed addition:
{
  "database": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": { "DATABASE_URL": "${DATABASE_URL}" }
  }
}

This would require adding the MCP server to 4 config files to maintain consistency.

Should I proceed with this change?"
```

### ❌ WRONG - Silent Modification

```
Agent: [Notices config issue and fixes it without telling user]
```

### ✅ RIGHT - Report and Propose

```
Agent: "I notice a potential issue in the MCP configurations:
- .kilocode/mcp.json has filesystem-projects pointing to /projects
- .clinerules/mcp.json has filesystem-projects pointing to C:/Users/pavel/projects

These should be consistent. Would you like me to:
1. Standardize both to use C:/Users/pavel/projects
2. Leave as-is
3. Something else?"
```

## Enforcement

This rule is enforced by:

1. Pre-commit hooks checking for agent dir modifications
2. Required approval workflow for protected files
3. Cross-agent verification scripts
4. Agent self-monitoring (check before modifying)

---

**Remember**: Agent configurations are infrastructure. Changes affect ALL
agents. Be conservative.
