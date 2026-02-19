---
description: Antigravity IDE specific rules and best practices for 2026
---

# Antigravity IDE Best Practices

**Based on**: Official documentation, community guides, and Snyk security
recommendations **Applies to**: All agents working with Antigravity IDE

---

## Antigravity IDE Overview

Antigravity is Google's "Agent-First" IDE (released Nov 2025) that uses:

- **Agent Manager**: Parallel agent orchestration
- **MCP Integration**: Model Context Protocol for tool access
- **Rules**: Passive constraints (context injection)
- **Workflows**: Active procedures (repeatable tasks)

**Key Philosophy**: "Managing a small team of engineers" rather than typing code

---

## MCP Configuration in Antigravity

### Format Differences

Antigravity uses a **different MCP format** than Kilo/Cline:

```json
// Antigravity Format
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "description": "Description here"
    }
  }
}
```

```json
// Kilo/Cline Format
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "alwaysAllow": ["tool1", "tool2"]
    }
  }
}
```

**Key Differences:**

- Antigravity: No `alwaysAllow` array (uses UI approval)
- Kilo/Cline: Has `alwaysAllow` for auto-approval
- Antigravity: Supports `description` field
- Both: Use same `command`/`args` structure

### Best Practices for Antigravity MCP

1. **Use Descriptions**

   ```json
   {
     "filesystem": {
       "command": "npx",
       "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
       "description": "Project filesystem access for reading and writing files"
     }
   }
   ```

2. **Prefer npx over global installs**
   - Use `npx -y @modelcontextprotocol/server-name`
   - Avoids version conflicts
   - Always gets latest

3. **Use relative paths when possible**

   ```json
   "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
   // vs
   "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/absolute/path"]
   ```

4. **Security: No alwaysAllow equivalent**
   - Antigravity shows approval UI for each operation
   - Users must approve write operations
   - This is a security feature, not a limitation

---

## Rules vs Workflows

### Rules (Passive Context)

**Purpose**: Constraints and context injected into the model

**Location**: `.antigravity/skills/SKILL.md`

**Format**:

```markdown
---
description: What this rule does
globs: *.py  # Optional file pattern
---

# Rule Title

Context here. This text is injected into the model when matching files are
accessed.
```

**Best Practices**:

- Keep rules concise (200-500 words)
- Use frontmatter with description
- Use `globs` to target specific file types
- Rules are passive - they don't execute actions

### Workflows (Active Procedures)

**Purpose**: Repeatable, multi-step procedures

**Location**: `.antigravity/workflows/`

**Format**:

```markdown
# Workflow Title

## Step 1: Analysis

Analyze the current state...

## Step 2: Implementation

Make the necessary changes...

## Step 3: Verification

Run tests to verify...
```

**Best Practices**:

- Break into clear steps
- Use parallel agents for independent tasks
- Include verification at the end
- Reference rules, don't duplicate them

---

## Parallel Agent Orchestration

### The Power of Antigravity

Antigravity's key feature is **parallel agent execution**:

```
❌ Sequential (Slow):
Agent A: Refactor auth (10 min) → Agent B: Write tests (10 min) = 20 min total

✅ Parallel (Fast):
Agent A: Refactor auth (10 min)
Agent B: Write tests (10 min) ← simultaneously
= 10 min total
```

### Best Practices for Parallel Agents

1. **Spawn Specialized Agents**

   ```
   Instead of: "Fix the auth and add tests"

   Do this:
   - Agent A: "Refactor auth.ts to use new provider pattern (no behavior change)"
   - Agent B: "Write comprehensive unit tests for auth.ts edge cases"
   ```

2. **Clear Boundaries**
   - Each agent should have a specific, non-overlapping task
   - Agents can work on same file if tasks are independent
   - Use memory to share context between agents

3. **Use Memory for Coordination**

   ```markdown
   ## Shared Context

   - auth.ts: Currently uses legacy pattern
   - Goal: Migrate to provider pattern
   - Constraint: Maintain backward compatibility

   ## Agent A Task

   Refactor implementation...

   ## Agent B Task

   Write tests for new pattern...
   ```

4. **Verification Agent** Always have a final agent verify the work:
   ```
   Agent C: "Review changes from Agent A and Agent B for consistency"
   ```

---

## Antigravity Configuration Files

### Primary Config

**File**: `.antigravity/mcp.json`

**Purpose**: MCP server definitions

**Format**:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "...",
      "args": [...],
      "description": "..."
    }
  },
  "disabled": false,
  "disabledTools": []
}
```

### Skills Directory

**Location**: `.antigravity/skills/`

**Files**: `SKILL.md` files with frontmatter

**Purpose**: Passive rules and context

### Workflows Directory

**Location**: `.antigravity/workflows/`

**Files**: Markdown with step-by-step procedures

**Purpose**: Active, repeatable processes

---

## Security Best Practices (Snyk Recommendations)

### 1. MCP Server Permissions

**Risk**: MCP servers can execute commands, access files, call APIs

**Mitigation**:

- Review each MCP server's capabilities before installing
- Use least-privilege paths in filesystem servers
- Prefer read-only servers when possible
- Regularly audit installed MCP servers

### 2. Environment Variables

**Risk**: Secrets in environment variables can be exposed

**Mitigation**:

- Use `.env` files (gitignored)
- Use wrapper scripts to load secrets
- Never hardcode API keys in configs
- Rotate keys regularly

### 3. Path Validation

**Risk**: Path traversal attacks through MCP filesystem servers

**Mitigation**:

```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      "." // ← Restrict to project root
    ],
    "description": "Project filesystem only"
  }
}
```

### 4. Code Review for Agent Output

**Risk**: Agents may generate insecure code

**Mitigation**:

- Always review agent-generated code
- Run security scans (Snyk, npm audit)
- Use linters with security rules
- Don't auto-commit agent changes

---

## Integration with Other Agents

### Cross-Compatibility

Antigravity configs can coexist with other agents:

```
.kilocode/mcp.json      # Kilo Code config
.clinerules/mcp.json    # Cline config
.antigravity/mcp.json   # Antigravity config
opencode.json           # OpenCode config
```

**Best Practice**: Keep configs synchronized:

- If adding MCP server to one, add to all
- Use same paths across all configs
- Maintain feature parity

### Converting Between Formats

**Kilo → Antigravity**:

```json
// Kilo
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-name"],
  "alwaysAllow": ["tool1", "tool2"]
}

// Antigravity
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-name"],
  "description": "Description here"
  // Note: No alwaysAllow in Antigravity
}
```

**Antigravity → Kilo**:

```json
// Antigravity
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-name"],
  "description": "Description"
}

// Kilo
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-name"],
  "alwaysAllow": ["tool1", "tool2"],  // ← Add based on usage
  "description": "Description"  // ← Optional in Kilo
}
```

---

## Troubleshooting

### MCP Server Not Found

**Symptom**: "Command not found" errors

**Solution**:

```bash
# Use npx -y to auto-install
"command": "npx",
"args": ["-y", "@modelcontextprotocol/server-name"]

# Or install globally first
npm install -g @modelcontextprotocol/server-name
```

### Permission Denied

**Symptom**: "EACCES: permission denied"

**Solution**:

- Check file permissions
- Use relative paths
- Ensure paths exist

### Connection Refused

**Symptom**: MCP server starts but can't connect

**Solution**:

- Check port availability
- Verify firewall settings
- Check MCP server logs

---

## Official Resources

- **Antigravity Codes**: https://antigravity.codes/ (Community resources)
- **Documentation**: https://antigravity.google/docs/mcp
- **MCP Store**: Built into Antigravity IDE ("..." menu)
- **Snyk Guide**:
  https://docs.snyk.io/integrations/developer-guardrails-for-agentic-workflows/quickstart-guides-for-mcp/antigravity-guide

---

## Quick Reference

| Feature          | Antigravity      | Kilo/Cline       | OpenCode        |
| ---------------- | ---------------- | ---------------- | --------------- |
| MCP Format       | `command`/`args` | `command`/`args` | `type: "local"` |
| `alwaysAllow`    | ❌ No            | ✅ Yes           | ❌ No           |
| `description`    | ✅ Yes           | ❌ No            | ❌ No           |
| Permission Model | UI approval      | Auto with allow  | Built-in        |
| Rules            | `skills/*.md`    | `rules/*.md`     | `skill/*.md`    |
| Workflows        | `workflows/*.md` | `workflows/*.md` | `command/*.md`  |
| Parallel Agents  | ✅ Native        | ⚠️ Manual        | ⚠️ Manual       |

---

**Remember**: Antigravity is designed for agent-first workflows. Embrace
parallel execution, use Rules for context, and Workflows for procedures.
