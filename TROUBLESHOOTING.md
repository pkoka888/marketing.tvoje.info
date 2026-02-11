# TROUBLESHOOTING.md

This guide provides comprehensive troubleshooting information for the Kilo Code template project. It covers common issues, their causes, and step-by-step solutions.

## Table of Contents

1. [Quick Start Troubleshooting](#quick-start-troubleshooting)
2. [Memory Bank Issues](#memory-bank-issues)
3. [MCP Server Issues](#mcp-server-issues)
4. [Mode-Specific Issues](#mode-specific-issues)
5. [Workflow Issues](#workflow-issues)
6. [File and Directory Issues](#file-and-directory-issues)
7. [Environment and Setup Issues](#environment-and-setup-issues)
8. [Performance Issues](#performance-issues)
9. [Common Error Messages](#common-error-messages)
10. [Debugging Tips](#debugging-tips)
11. [When to Contact Support](#when-to-contact-support)

---

## Quick Start Troubleshooting

### "I just started, what do I do?"

If you're new to the Kilo Code template, follow these initial steps:

#### Step 1: Verify Project Structure
```bash
# Check if .kilocode directory exists
dir .kilocode

# Expected output should show:
# mcp.json
# modes/
# skills/
# workflows/
# rules/
# rules-architect/
# rules-code/
# rules-debug/
# rules/memory-bank/
```

#### Step 2: Initialize Memory Bank
If you see `[Memory Bank: Missing]` at the start of any task:
```
Request: "initialize memory bank"
```

The AI will analyze your project and create the necessary documentation files in [`.kilocode/rules/memory-bank/`](.kilocode/rules/memory-bank/).

#### Step 3: Verify MCP Configuration
Check [`.kilocode/mcp.json`](.kilocode/mcp.json:1) exists and is valid:
```json
{
  "mcpServers": {
    "filesystem-projects": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/pavel/projects"],
      "alwaysAllow": ["read_text_file", "list_directory", "directory_tree", "read_multiple_files", "create_directory", "write_file"]
    }
  }
}
```

#### Step 4: Test Basic Functionality
Try a simple task:
```
Request: "list all files in the current directory"
```

If this works, your basic setup is functional.

### Quick Fixes for Common Issues

| Issue | Quick Fix |
|-------|-----------|
| `[Memory Bank: Missing]` | Run "initialize memory bank" command |
| MCP server not starting | Check Node.js is installed: `node --version` |
| Workflow not found | Verify workflow file name matches command (kebab-case) |
| Skill not loading | Check skill directory name matches frontmatter name |
| Rules not applying | Verify rule file has valid YAML frontmatter |

---

## Memory Bank Issues

### Memory Bank Not Loading ([Memory Bank: Missing])

**Symptoms:**
- AI responses start with `[Memory Bank: Missing]`
- AI doesn't understand project context
- Repetitive explanations needed

**Causes:**
1. Memory Bank directory doesn't exist
2. Memory Bank files are incomplete
3. Memory Bank files are corrupted

**Solutions:**

#### Solution 1: Initialize Memory Bank
```
Request: "initialize memory bank"
```

The AI will:
1. Analyze all project files
2. Create [`.kilocode/rules/memory-bank/brief.md`](.kilocode/rules/memory-bank/brief.md:1)
3. Create [`.kilocode/rules/memory-bank/product.md`](.kilocode/rules/memory-bank/product.md:1)
4. Create [`.kilocode/rules/memory-bank/context.md`](.kilocode/rules/memory-bank/context.md:1)
5. Create [`.kilocode/rules/memory-bank/architecture.md`](.kilocode/rules/memory-bank/architecture.md:1)
6. Create [`.kilocode/rules/memory-bank/tech.md`](.kilocode/rules/memory-bank/tech.md:1)

#### Solution 2: Verify Memory Bank Files
```bash
# Check if memory bank directory exists
dir .kilocode\rules\memory-bank

# Expected files:
# brief.md
# product.md
# context.md
# architecture.md
# tech.md
```

#### Solution 3: Restore from Backup
If you have a backup of the Memory Bank files:
```bash
# Restore from backup
copy backup\memory-bank\* .kilocode\rules\memory-bank\
```

### Memory Bank Files Incomplete or Corrupted

**Symptoms:**
- AI responses are inconsistent
- Project context is partially missing
- Errors when loading Memory Bank

**Solutions:**

#### Solution 1: Reinitialize Memory Bank
```
Request: "update memory bank"
```

This will review ALL files and update the Memory Bank comprehensively.

#### Solution 2: Manual File Repair
Check each Memory Bank file for:
- Valid Markdown syntax
- Proper heading structure
- No corrupted characters

Example structure for [`brief.md`](.kilocode/rules/memory-bank/brief.md:1):
```markdown
# Project Brief

## Project Overview
[Your project overview]

## Core Goals
1. [Goal 1]
2. [Goal 2]

## Project Scope
[Project scope details]
```

### brief.md Editing Issues (AI Should Not Edit Directly)

**Symptoms:**
- AI attempts to edit [`brief.md`](.kilocode/rules/memory-bank/brief.md:1)
- Changes to project overview are lost

**Important Rule:**
[`brief.md`](.kilocode/rules/memory-bank/brief.md:1) is **developer-maintained**. The AI should only suggest updates, NOT edit directly.

**Solutions:**

#### Solution 1: AI Suggests Updates
When the AI identifies needed changes to [`brief.md`](.kilocode/rules/memory-bank/brief.md:1), it should say:
```
"I suggest updating brief.md to include [specific change]. Would you like me to provide the suggested content?"
```

#### Solution 2: Manual Updates
As the developer, you should:
1. Review AI suggestions
2. Edit [`brief.md`](.kilocode/rules/memory-bank/brief.md:1) directly
3. Commit changes to version control

### context.md Becoming Too Long or Speculative

**Symptoms:**
- [`context.md`](.kilocode/rules/memory-bank/context.md:1) is excessively long
- Contains speculative or creative content
- Difficult to find current state information

**Important Rule:**
[`context.md`](.kilocode/rules/memory-bank/context.md:1) must be **factual, NOT creative or speculative**.

**Solutions:**

#### Solution 1: Keep context.md Short and Factual
Maintain this structure:
```markdown
# Context

## Current State
[Brief, factual description of current state]

## Recent Changes
- [Date]: [Factual change 1]
- [Date]: [Factual change 2]

## Next Steps
- [Next step 1]
- [Next step 2]
```

#### Solution 2: Archive Old Context
When [`context.md`](.kilocode/rules/memory-bank/context.md:1) becomes too long:
1. Create [`.kilocode/rules/memory-bank/context-archive.md`](.kilocode/rules/memory-bank/context-archive.md:1)
2. Move old entries to archive
3. Keep only recent entries in [`context.md`](.kilocode/rules/memory-bank/context.md:1)

### Memory Bank Update Not Reflecting Changes

**Symptoms:**
- Requested "update memory bank" but changes not reflected
- AI still uses old information

**Solutions:**

#### Solution 1: Verify Update Command
Use the exact phrase:
```
Request: "update memory bank"
```

The AI MUST review ALL files when this phrase is used.

#### Solution 2: Check File Permissions
```bash
# Verify write permissions
icacls .kilocode\rules\memory-bank

# Ensure you have write access
```

#### Solution 3: Clear AI Context
If the AI is still using cached information:
1. Start a new conversation
2. The AI will reload Memory Bank from files

---

## MCP Server Issues

### MCP Servers Not Starting

**Symptoms:**
- MCP server errors in logs
- File operations fail
- "Server not found" errors

**Causes:**
1. Node.js not installed
2. npx not available
3. Network issues
4. Invalid server configuration

**Solutions:**

#### Solution 1: Verify Node.js Installation
```bash
# Check Node.js version
node --version

# Expected: v18.0.0 or higher
# If not installed, download from: https://nodejs.org/
```

#### Solution 2: Verify npx Availability
```bash
# Check npx
npx --version

# If not available, reinstall Node.js with npm
```

#### Solution 3: Test MCP Server Manually
```bash
# Test filesystem server
npx -y @modelcontextprotocol/server-filesystem C:/Users/pavel/projects

# Should start without errors
```

#### Solution 4: Check MCP Configuration
Verify [`.kilocode/mcp.json`](.kilocode/mcp.json:1) is valid JSON:
```bash
# Validate JSON
node -e "console.log(JSON.parse(require('fs').readFileSync('.kilocode/mcp.json', 'utf8')))"
```

### Permission Denied Errors

**Symptoms:**
- "Permission denied" when accessing files
- MCP server operations fail
- File read/write errors

**Causes:**
1. Insufficient file system permissions
2. Path outside allowed directories
3. Antivirus blocking operations

**Solutions:**

#### Solution 1: Check File Permissions
```bash
# Check directory permissions
icacls .kilocode

# Grant full control if needed
icacls .kilocode /grant %USERNAME%:F
```

#### Solution 2: Verify Allowed Directories
Check [`.kilocode/mcp.json`](.kilocode/mcp.json:1) for allowed paths:
```json
{
  "mcpServers": {
    "filesystem-projects": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/pavel/projects"]
    }
  }
}
```

Ensure the path you're accessing is within the allowed directory.

#### Solution 3: Check Antivirus Settings
Add the following to antivirus exclusions:
- `C:/Users/pavel/projects/jobs`
- `C:/Users/pavel/vscodeportable/agentic`
- Node.js installation directory

### Path Validation Failures

**Symptoms:**
- "Invalid path" errors
- Path not recognized
- Operations fail on valid paths

**Causes:**
1. Using `~` or `$HOME` characters
2. Relative vs absolute path confusion
3. Path format issues (forward vs backslashes)

**Solutions:**

#### Solution 1: Use Correct Path Format
**Incorrect:**
```bash
~/.kilocode/mcp.json
$HOME/.kilocode/mcp.json
```

**Correct:**
```bash
.kilocode/mcp.json
C:/Users/pavel/projects/jobs/.kilocode/mcp.json
```

#### Solution 2: Use Forward Slashes
**Incorrect:**
```json
"C:\\Users\\pavel\\projects"
```

**Correct:**
```json
"C:/Users/pavel/projects"
```

#### Solution 3: Verify Path Exists
```bash
# Check if path exists
dir C:/Users/pavel/projects

# List directory contents
dir C:/Users/pavel/projects /s
```

### Rate Limiting Errors

**Symptoms:**
- "Rate limit exceeded" errors
- Operations slow down
- Requests timeout

**Causes:**
1. Too many rapid requests
2. API rate limits (for GitHub, etc.)
3. Server overload

**Solutions:**

#### Solution 1: Implement Exponential Backoff
When implementing code that uses MCP servers:
```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
    }
  }
}
```

#### Solution 2: Batch Operations
Instead of many small operations:
```javascript
// Instead of multiple reads
const file1 = await readFile('file1.txt');
const file2 = await readFile('file2.txt');

// Use batch read
const files = await readMultipleFiles(['file1.txt', 'file2.txt']);
```

#### Solution 3: Cache Results
Cache frequently accessed data to reduce MCP server calls.

### GitHub Token Authentication Failures

**Symptoms:**
- "Authentication failed" errors
- GitHub operations denied
- 401 Unauthorized errors

**Solutions:**

#### Solution 1: Set GitHub Token
Create or update [`.env`](.env:1) file:
```bash
GITHUB_TOKEN=your_github_personal_access_token
```

#### Solution 2: Generate New Token
1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate new token with required scopes
3. Update [`.env`](.env:1) file

#### Solution 3: Verify Token Permissions
Ensure token has required scopes:
- `repo` (for private repositories)
- `public_repo` (for public repositories)
- `read:org` (for organization access)

### Redis Connection Issues

**Symptoms:**
- "Connection refused" errors
- Redis operations fail
- Timeout errors

**Solutions:**

#### Solution 1: Verify Redis is Running
```bash
# Check Redis status
redis-cli ping

# Expected response: PONG
```

#### Solution 2: Start Redis Server
```bash
# Start Redis server
redis-server

# Or start as service
redis-server --service-start
```

#### Solution 3: Check Redis Configuration
Verify Redis connection settings in MCP configuration:
```json
{
  "mcpServers": {
    "redis": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-redis", "--host", "localhost", "--port", "6379"]
    }
  }
}
```

### Server-Specific Troubleshooting

#### Memory Server
**Issue:** Memory operations fail
**Solution:**
```bash
# Verify memory server is running
npx -y @modelcontextprotocol/server-memory

# Check memory graph
# Use search_nodes tool to verify connectivity
```

#### Git Server
**Issue:** Git operations fail
**Solution:**
```bash
# Verify git is installed
git --version

# Check git configuration
git config --list

# Initialize git if needed
git init
```

#### GitHub Server
**Issue:** GitHub API operations fail
**Solution:**
```bash
# Verify GitHub token is set
echo %GITHUB_TOKEN%

# Test GitHub connection
curl -H "Authorization: token %GITHUB_TOKEN%" https://api.github.com/user
```

#### Time Server
**Issue:** Time conversion fails
**Solution:**
```bash
# Test time server
npx -y mcp-server-time

# Verify timezone format
# Use IANA timezone names (e.g., "America/New_York", "Europe/London")
```

#### Fetch Server
**Issue:** URL fetching fails
**Solution:**
```bash
# Test fetch server
npx -y mcp-server-fetch

# Check network connectivity
ping google.com

# Verify URL is accessible
curl https://example.com
```

#### SQLite Server
**Issue:** Database operations fail
**Solution:**
```bash
# Verify database file exists
dir mydatabase.db

# Check database integrity
sqlite3 mydatabase.db "PRAGMA integrity_check;"

# Expected output: ok
```

#### Puppeteer Server
**Issue:** Browser automation fails
**Solution:**
```bash
# Test Puppeteer
npx -y @modelcontextprotocol/server-puppeteer

# Check if Chrome/Chromium is installed
where chrome

# Or install Chromium
npm install puppeteer
```

---

## Mode-Specific Issues

### Architect Mode: Multi-Attempt Reasoning Not Working

**Symptoms:**
- Single attempt only
- No iterative refinement
- Limited analysis depth

**Causes:**
1. Mode not properly activated
2. Reasoning configuration disabled
3. Token limit reached

**Solutions:**

#### Solution 1: Verify Mode Activation
Ensure you're in Architect mode:
```
Request: "Switch to Architect mode"
```

#### Solution 2: Check Mode Configuration
Verify [`.kilocode/modes/architect.md`](.kilocode/modes/architect.md:1) exists and contains:
```yaml
name: architect
description: Planning and architecture mode
multiAttemptReasoning: true
maxAttempts: 3
```

#### Solution 3: Increase Token Limit
If token limit is reached, request:
```
Request: "Continue with multi-attempt reasoning, use more tokens"
```

### Code Mode: Simulation Testing Failures

**Symptoms:**
- Simulation not performed
- Tests fail unexpectedly
- Code breaks after changes

**Causes:**
1. Simulation testing skipped
2. Incomplete dependency analysis
3. Missing flow analysis

**Solutions:**

#### Solution 1: Request Simulation Testing
Before implementation, explicitly request:
```
Request: "Perform simulation testing before implementing changes"
```

#### Solution 2: Verify Code Mode Rules
Check [`.kilocode/rules-code/implement.md`](.kilocode/rules-code/implement.md:1) contains simulation testing requirements.

#### Solution 3: Complete Dependency Analysis
Ensure the AI performs:
1. **Dependency Analysis**: Which components will be affected?
2. **Flow Analysis**: Complete end-to-end flow analysis

Example request:
```
Request: "Analyze dependencies and flow for this change before implementing"
```

### Debug Mode: 8-Step Protocol Not Executing

**Symptoms:**
- Debugging steps skipped
- Incomplete analysis
- No systematic approach

**Causes:**
1. Debug mode not activated
2. Protocol not loaded
3. Steps interrupted

**Solutions:**

#### Solution 1: Activate Debug Mode
```
Request: "Switch to Debug mode"
```

#### Solution 2: Load Debug Protocol
Verify [`.kilocode/rules-debug/debug.md`](.kilocode/rules-debug/debug.md:1) contains the 8-step protocol.

#### Solution 3: Request Full Protocol
```
Request: "Execute the full 8-step debugging protocol"
```

The 8 steps should be:
1. Identify the problem
2. Gather information
3. Formulate hypothesis
4. Test hypothesis
5. Analyze results
6. Implement fix
7. Verify solution
8. Document findings

### Ask Mode: Memory Bank Not Loading

**Symptoms:**
- `[Memory Bank: Missing]` in Ask mode
- AI lacks project context
- Generic responses

**Solutions:**

#### Solution 1: Initialize Memory Bank
```
Request: "initialize memory bank"
```

#### Solution 2: Verify Ask Mode Configuration
Check [`.kilocode/modes/ask.md`](.kilocode/modes/ask.md:1) includes Memory Bank loading.

#### Solution 3: Explicitly Request Context
```
Request: "Load Memory Bank and answer with full project context"
```

### Prompt Consultant Mode: Not Available (Global Configuration)

**Symptoms:**
- Prompt Consultant mode not listed
- Cannot switch to Prompt Consultant
- Mode not recognized

**Causes:**
1. Mode configured globally, not in project
2. Configuration file not found
3. Mode name mismatch

**Solutions:**

#### Solution 1: Check Global Configuration
Prompt Consultant mode is configured at:
```
C:/Users/pavel/vscodeportable/.kilocode/custom_modes.yaml
```

Verify it contains:
```yaml
prompt-consultant:
  name: Prompt Consultant
  description: Mode for prompt engineering tasks
  skill: prompt-consultant
```

#### Solution 2: Verify Skill Exists
Check [`.kilocode/skills/prompt-consultant/SKILL.md`](.kilocode/skills/prompt-consultant/SKILL.md:1) exists.

#### Solution 3: Restart VS Code
After configuration changes, restart VS Code to reload modes.

---

## Workflow Issues

### Workflow Not Found (File Name Mismatch)

**Symptoms:**
- "Workflow not found" error
- Cannot execute workflow
- Workflow command not recognized

**Causes:**
1. Workflow file name doesn't match command
2. Workflow file in wrong location
3. Case sensitivity issues

**Solutions:**

#### Solution 1: Verify File Naming Convention
Workflow file names MUST match command names (kebab-case):

| Command | Expected File Name |
|---------|-------------------|
| `analyze-prompt` | `analyze-prompt.md` |
| `create-prompt` | `create-prompt.md` |
| `optimize-prompt` | `optimize-prompt.md` |
| `test-prompt` | `test-prompt.md` |

#### Solution 2: Check Workflow Location
Workflows must be in [`.kilocode/workflows/`](.kilocode/workflows/):
```bash
dir .kilocode\workflows

# Expected output:
# analyze-prompt.md
# create-prompt.md
# optimize-prompt.md
# test-prompt.md
```

#### Solution 3: Verify Case Sensitivity
On case-sensitive systems, ensure exact match:
- `create-prompt.md` ✅
- `Create-Prompt.md` ❌
- `CREATE_PROMPT.md` ❌

### Workflow Execution Errors

**Symptoms:**
- Workflow stops mid-execution
- Steps fail
- Invalid output

**Causes:**
1. Invalid workflow structure
2. Missing required fields
3. Circular dependencies

**Solutions:**

#### Solution 1: Verify Workflow Structure
Check workflow file has valid structure:
```markdown
---
description: Create a new prompt
globs: ["*.md"]
alwaysApply: false
---

# Create Prompt Workflow

## Step 1: Define Purpose
[Step content]

## Step 2: Identify Target Audience
[Step content]

...
```

#### Solution 2: Check Required Fields
Ensure YAML frontmatter has required fields:
- `description`: Workflow description
- `globs`: File patterns (optional)
- `alwaysApply`: Whether to always apply (optional)

#### Solution 3: Validate YAML Frontmatter
```bash
# Use a YAML validator
# Or check with Node.js
node -e "const yaml = require('js-yaml'); console.log(yaml.load(require('fs').readFileSync('.kilocode/workflows/create-prompt.md', 'utf8')))"
```

### Step-by-Step Process Not Working

**Symptoms:**
- Workflow executes all steps at once
- No user input collection
- Steps skipped

**Causes:**
1. Workflow not using step-by-step format
2. Missing user input prompts
3. Incorrect workflow syntax

**Solutions:**

#### Solution 1: Use Proper Step Format
Each step should be clearly marked:
```markdown
## Step 1: [Step Title]

[Step description]

**Action Required:** [What user needs to do]

**Example:** [Example input]
```

#### Solution 2: Add User Input Prompts
Include explicit prompts for user input:
```markdown
## Step 2: Define Requirements

Please provide the following information:

1. What is the primary goal of this prompt?
2. Who is the target audience?
3. What constraints should be considered?

**Your response:** [Waiting for user input]
```

#### Solution 3: Use Sequential Execution
Ensure steps are numbered and sequential:
```markdown
## Step 1: [First step]
[Content]

## Step 2: [Second step]
[Content]

## Step 3: [Third step]
[Content]
```

### User Input Collection Issues

**Symptoms:**
- User input not captured
- Input not used in subsequent steps
- Workflow continues without input

**Solutions:**

#### Solution 1: Explicit Input Markers
Use clear markers for user input:
```markdown
**Please provide:** [What to provide]

**Your input:** [User will type here]

**Next:** [What happens after input]
```

#### Solution 2: Reference Previous Input
Reference user input in later steps:
```markdown
## Step 3: Draft Prompt

Based on your goal: "[User's goal from Step 1]"
And your audience: "[User's audience from Step 2]"

Draft a prompt that addresses these requirements.
```

#### Solution 3: Validate Input
Include validation steps:
```markdown
## Step 2: Validate Input

Please confirm the following:
- Goal: [User's goal]
- Audience: [User's audience]

Is this correct? (yes/no)
```

---

## File and Directory Issues

### .kilocode Directory Structure Problems

**Symptoms:**
- Configuration not loaded
- Rules not applied
- Modes not available

**Causes:**
1. Missing directories
2. Incorrect structure
3. Permission issues

**Solutions:**

#### Solution 1: Verify Directory Structure
```bash
# Check .kilocode directory
dir .kilocode /s

# Expected structure:
# .kilocode/
# ├── mcp.json
# ├── modes/
# ├── skills/
# ├── workflows/
# ├── rules/
# ├── rules-architect/
# ├── rules-code/
# ├── rules-debug/
# └── rules/memory-bank/
```

#### Solution 2: Create Missing Directories
```bash
# Create missing directories
mkdir .kilocode\modes
mkdir .kilocode\skills
mkdir .kilocode\workflows
mkdir .kilocode\rules
mkdir .kilocode\rules-architect
mkdir .kilocode\rules-code
mkdir .kilocode\rules-debug
mkdir .kilocode\rules\memory-bank
```

#### Solution 3: Fix Permissions
```bash
# Grant full control to .kilocode directory
icacls .kilocode /grant %USERNAME%:F /T
```

### Rule Files Not Loading

**Symptoms:**
- Rules not applied
- Default behavior only
- No mode-specific guidance

**Causes:**
1. Invalid YAML frontmatter
2. Missing required fields
3. File in wrong location

**Solutions:**

#### Solution 1: Verify YAML Frontmatter
Check rule file has valid frontmatter:
```yaml
---
description: Rule description
globs: ["*.md"]
alwaysApply: false
---
```

#### Solution 2: Validate Frontmatter
```bash
# Test YAML parsing
node -e "const yaml = require('js-yaml'); const fs = require('fs'); const content = fs.readFileSync('.kilocode/rules-code/implement.md', 'utf8'); const match = content.match(/^---\n([\s\S]*?)\n---/); if (match) console.log(yaml.load(match[1]));"
```

#### Solution 3: Check File Location
Ensure rule files are in correct directories:
- General rules: [`.kilocode/rules/`](.kilocode/rules/)
- Architect rules: [`.kilocode/rules-architect/`](.kilocode/rules-architect/)
- Code rules: [`.kilocode/rules-code/`](.kilocode/rules-code/)
- Debug rules: [`.kilocode/rules-debug/`](.kilocode/rules-debug/)

### Skills Not Loading (Name Mismatch)

**Symptoms:**
- Skill not available
- Mode doesn't use skill
- Skill guidelines not applied

**Causes:**
1. Skill directory name doesn't match frontmatter
2. SKILL.md missing
3. Invalid skill structure

**Solutions:**

#### Solution 1: Verify Skill Name Matching
Skill directory name MUST match frontmatter name:

**Directory:** [`.kilocode/skills/prompt-consultant/`](.kilocode/skills/prompt-consultant/)

**SKILL.md frontmatter:**
```yaml
---
name: prompt-consultant
description: Prompt engineering guidelines
---
```

#### Solution 2: Check SKILL.md Exists
```bash
# Verify SKILL.md exists
dir .kilocode\skills\prompt-consultant

# Expected: SKILL.md
```

#### Solution 3: Validate Skill Structure
Ensure SKILL.md has proper structure:
```markdown
---
name: prompt-consultant
description: Prompt engineering guidelines
---

# Prompt Consultant Skill

## Overview
[Skill overview]

## Guidelines
[Guidelines]

## Best Practices
[Best practices]
```

### Workflows Not Accessible

**Symptoms:**
- Cannot execute workflow
- Workflow not listed
- Command not recognized

**Solutions:**

#### Solution 1: Verify Workflow Location
```bash
# Check workflows directory
dir .kilocode\workflows

# Expected: workflow files
```

#### Solution 2: Check Workflow File Extension
Ensure workflow files have `.md` extension:
- `create-prompt.md` ✅
- `create-prompt` ❌
- `create-prompt.txt` ❌

#### Solution 3: Verify Workflow Syntax
Check workflow has valid YAML frontmatter:
```markdown
---
description: Workflow description
globs: ["*.md"]
alwaysApply: false
---

# Workflow Title

[Workflow content]
```

### AGENTS.md Files Not Being Read

**Symptoms:**
- Agent rules not applied
- Mode-specific behavior missing
- Default behavior only

**Causes:**
1. AGENTS.md missing
2. Invalid file format
3. File in wrong location

**Solutions:**

#### Solution 1: Verify AGENTS.md Exists
```bash
# Check for AGENTS.md files
dir .kilocode\rules-code\AGENTS.md
dir .kilocode\rules-debug\AGENTS.md
dir AGENTS.md
```

#### Solution 2: Check File Format
Ensure AGENTS.md is valid Markdown with proper structure:
```markdown
# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Mode-Specific Instructions

[Instructions]
```

#### Solution 3: Verify File Location
AGENTS.md files should be in:
- Root: [`AGENTS.md`](AGENTS.md:1)
- Code mode: [`.kilocode/rules-code/AGENTS.md`](.kilocode/rules-code/AGENTS.md:1)
- Debug mode: [`.kilocode/rules-debug/AGENTS.md`](.kilocode/rules-debug/AGENTS.md:1)

---

## Environment and Setup Issues

### VS Code Extension Not Loading

**Symptoms:**
- Kilo Code extension not visible
- Extension shows error
- Commands not available

**Solutions:**

#### Solution 1: Verify Extension Installation
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Kilo Code"
4. Verify it's installed and enabled

#### Solution 2: Check Extension Logs
1. Open VS Code
2. Go to Help → Toggle Developer Tools
3. Check Console for errors
4. Look for Kilo Code related errors

#### Solution 3: Reload VS Code
```
1. Press Ctrl+Shift+P
2. Type "Reload Window"
3. Press Enter
```

#### Solution 4: Reinstall Extension
```
1. Uninstall Kilo Code extension
2. Restart VS Code
3. Reinstall Kilo Code extension
```

### Node.js/npx Not Available

**Symptoms:**
- "node is not recognized" error
- "npx is not recognized" error
- MCP servers fail to start

**Solutions:**

#### Solution 1: Install Node.js
1. Download Node.js from https://nodejs.org/
2. Install LTS version (recommended)
3. Restart terminal/VS Code

#### Solution 2: Verify Installation
```bash
# Check Node.js version
node --version

# Check npm version
npm --version

# Check npx version
npx --version
```

#### Solution 3: Add to PATH
If Node.js is installed but not in PATH:
```bash
# Add Node.js to PATH (Windows)
setx PATH "%PATH%;C:\Program Files\nodejs"

# Restart terminal
```

#### Solution 4: Use Alternative Installation
If you cannot install Node.js globally:
```bash
# Use nvm (Node Version Manager)
# Download from: https://github.com/coreybutler/nvm-windows
nvm install 18
nvm use 18
```

### Environment Variables Not Set

**Symptoms:**
- Configuration not loaded
- Secrets not accessible
- API calls fail

**Solutions:**

#### Solution 1: Create .env File
Copy from template:
```bash
copy .env.template .env
```

#### Solution 2: Edit .env File
Edit [`.env`](.env:1) with your values:
```bash
# GitHub Token
GITHUB_TOKEN=your_github_token_here

# API Keys
API_KEY=your_api_key_here

# Other variables
VAR_NAME=value
```

#### Solution 3: Set Environment Variables (Windows)
```bash
# Set temporary variable (current session)
set GITHUB_TOKEN=your_token

# Set permanent variable
setx GITHUB_TOKEN "your_token"

# Verify
echo %GITHUB_TOKEN%
```

#### Solution 4: Set Environment Variables (PowerShell)
```powershell
# Set temporary variable
$env:GITHUB_TOKEN = "your_token"

# Set permanent variable
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your_token", "User")

# Verify
echo $env:GITHUB_TOKEN
```

### .env File Not Found

**Symptoms:**
- "Environment file not found" error
- Configuration not loaded
- Default values used

**Solutions:**

#### Solution 1: Create .env from Template
```bash
copy .env.template .env
```

#### Solution 2: Verify .env Location
```bash
# Check if .env exists in project root
dir .env

# Expected: .env file in project root
```

#### Solution 3: Check .gitignore
Ensure [`.gitignore`](.gitignore:1) doesn't exclude `.env` incorrectly:
```gitignore
# Should include:
.env

# Should NOT include:
!.env
```

### Git Configuration Issues

**Symptoms:**
- Git operations fail
- Commit errors
- Push/pull issues

**Solutions:**

#### Solution 1: Initialize Git Repository
```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"
```

#### Solution 2: Configure Git User
```bash
# Set user name
git config --global user.name "Your Name"

# Set user email
git config --global user.email "your.email@example.com"

# Verify
git config --list
```

#### Solution 3: Configure Git for Windows
```bash
# Configure line endings
git config --global core.autocrlf true

# Configure default branch
git config --global init.defaultBranch main
```

#### Solution 4: Fix Git Permissions
```bash
# Fix file permissions (Git Bash)
git config --global core.fileMode false
```

---

## Performance Issues

### Slow Response Times

**Symptoms:**
- AI responses take long
- Operations timeout
- Poor user experience

**Causes:**
1. Large context window
2. Complex operations
3. MCP server latency
4. Network issues

**Solutions:**

#### Solution 1: Reduce Context Window
```
Request: "Use minimal context for this task"
```

#### Solution 2: Optimize MCP Server Calls
Batch operations instead of multiple calls:
```javascript
// Instead of multiple reads
const file1 = await readFile('file1.txt');
const file2 = await readFile('file2.txt');

// Use batch read
const files = await readMultipleFiles(['file1.txt', 'file2.txt']);
```

#### Solution 3: Cache Results
Cache frequently accessed data to reduce repeated operations.

#### Solution 4: Check Network Connection
```bash
# Test network speed
ping google.com

# Test MCP server connectivity
# Check if servers are responding
```

### Memory Usage High

**Symptoms:**
- System slows down
- VS Code becomes unresponsive
- High memory consumption

**Solutions:**

#### Solution 1: Clear Memory Bank Archive
Archive old context entries:
```bash
# Create archive file
type .kilocode\rules\memory-bank\context.md >> .kilocode\rules\memory-bank\context-archive.md

# Clear current context
echo # Context > .kilocode\rules\memory-bank\context.md
```

#### Solution 2: Reduce File Loading
Request specific files instead of all:
```
Request: "Only load files in src/ directory"
```

#### Solution 3: Restart VS Code
```
1. Save all work
2. Close VS Code
3. Reopen VS Code
```

#### Solution 4: Disable Unused MCP Servers
Edit [`.kilocode/mcp.json`](.kilocode/mcp.json:1) to comment out unused servers:
```json
{
  "mcpServers": {
    "filesystem-projects": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/pavel/projects"]
    }
    // "redis": { ... }  // Commented out
  }
}
```

### Context Window Filling Up

**Symptoms:**
- "Context window full" error
- Responses truncated
- Cannot continue conversation

**Solutions:**

#### Solution 1: Update Memory Bank
```
Request: "Update memory bank to preserve current state"
```

#### Solution 2: Start Fresh Conversation
```
1. Save current work
2. Start new conversation
3. Memory Bank will be loaded automatically
```

#### Solution 3: Summarize Context
```
Request: "Summarize the current state and continue with minimal context"
```

#### Solution 4: Use Focused Requests
Instead of broad requests, use focused ones:
```
Instead of: "Review the entire project"
Use: "Review the authentication module in src/auth/"
```

### MCP Server Latency

**Symptoms:**
- MCP operations slow
- File operations timeout
- Poor performance

**Solutions:**

#### Solution 1: Optimize Server Configuration
Edit [`.kilocode/mcp.json`](.kilocode/mcp.json:1) to optimize:
```json
{
  "mcpServers": {
    "filesystem-projects": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/pavel/projects"],
      "env": {
        "NODE_OPTIONS": "--max-old-space-size=4096"
      }
    }
  }
}
```

#### Solution 2: Use Local Servers
Ensure MCP servers are running locally, not remotely.

#### Solution 3: Reduce Server Load
Batch operations and cache results to reduce server calls.

#### Solution 4: Check Server Resources
```bash
# Check CPU usage
tasklist

# Check memory usage
wmic OS get FreePhysicalMemory /Value

# Restart MCP servers if needed
```

---

## Common Error Messages

### "Memory Bank: Missing"

**What it means:**
The AI cannot find or load the Memory Bank files in [`.kilocode/rules/memory-bank/`](.kilocode/rules/memory-bank/).

**How to fix:**

#### Quick Fix:
```
Request: "initialize memory bank"
```

#### Detailed Fix:
1. Check if directory exists:
```bash
dir .kilocode\rules\memory-bank
```

2. If missing, create it:
```bash
mkdir .kilocode\rules\memory-bank
```

3. Initialize Memory Bank:
```
Request: "initialize memory bank"
```

4. Verify files were created:
```bash
dir .kilocode\rules\memory-bank

# Expected: brief.md, product.md, context.md, architecture.md, tech.md
```

### "Permission denied"

**What it means:**
The AI or MCP server doesn't have permission to access a file or directory.

**Troubleshooting steps:**

#### Step 1: Check File Permissions
```bash
# Check file permissions
icacls .kilocode

# Check directory permissions
icacls .kilocode\rules\memory-bank
```

#### Step 2: Grant Permissions
```bash
# Grant full control
icacls .kilocode /grant %USERNAME%:F /T
```

#### Step 3: Check Antivirus
Add project directory to antivirus exclusions:
- `C:/Users/pavel/projects/jobs`
- `C:/Users/pavel/vscodeportable/agentic`

#### Step 4: Verify Path
Ensure path is within allowed directories in [`.kilocode/mcp.json`](.kilocode/mcp.json:1).

### "Server not found"

**What it means:**
An MCP server cannot be found or started.

**Troubleshooting steps:**

#### Step 1: Verify Node.js
```bash
node --version
npx --version
```

#### Step 2: Test Server Manually
```bash
# Test filesystem server
npx -y @modelcontextprotocol/server-filesystem C:/Users/pavel/projects
```

#### Step 3: Check Configuration
Verify [`.kilocode/mcp.json`](.kilocode/mcp.json:1) is valid:
```bash
node -e "console.log(JSON.parse(require('fs').readFileSync('.kilocode/mcp.json', 'utf8')))"
```

#### Step 4: Restart VS Code
After configuration changes, restart VS Code.

### "Workflow not found"

**What it means:**
The workflow file cannot be found or the name doesn't match.

**Troubleshooting steps:**

#### Step 1: Check Workflow Location
```bash
dir .kilocode\workflows
```

#### Step 2: Verify File Name
Workflow file name MUST match command (kebab-case):
- Command: `create-prompt`
- File: `create-prompt.md`

#### Step 3: Check Case Sensitivity
Ensure exact case match:
- `create-prompt.md` ✅
- `Create-Prompt.md` ❌

#### Step 4: Verify File Extension
Ensure `.md` extension:
- `create-prompt.md` ✅
- `create-prompt` ❌

### "Skill not loaded"

**What it means:**
The skill cannot be loaded, usually due to name mismatch.

**Troubleshooting steps:**

#### Step 1: Check Skill Directory
```bash
dir .kilocode\skills
```

#### Step 2: Verify Name Matching
Directory name MUST match frontmatter name:

**Directory:** `prompt-consultant`

**SKILL.md frontmatter:**
```yaml
---
name: prompt-consultant
---
```

#### Step 3: Check SKILL.md Exists
```bash
dir .kilocode\skills\prompt-consultant\SKILL.md
```

#### Step 4: Validate Frontmatter
Ensure SKILL.md has valid YAML frontmatter.

### "Rule not applied"

**What it means:**
A rule file is not being applied to the current task.

**Troubleshooting steps:**

#### Step 1: Check Rule Location
Ensure rule is in correct directory:
- General: [`.kilocode/rules/`](.kilocode/rules/)
- Architect: [`.kilocode/rules-architect/`](.kilocode/rules-architect/)
- Code: [`.kilocode/rules-code/`](.kilocode/rules-code/)
- Debug: [`.kilocode/rules-debug/`](.kilocode/rules-debug/)

#### Step 2: Verify YAML Frontmatter
Check rule has valid frontmatter:
```yaml
---
description: Rule description
globs: ["*.md"]
alwaysApply: false
---
```

#### Step 3: Check File Pattern
Ensure `globs` pattern matches current file:
```yaml
globs: ["*.ts"]  # Only applies to TypeScript files
```

#### Step 4: Verify Mode
Some rules only apply in specific modes. Switch to correct mode.

### "Mode not available"

**What it means:**
The requested mode is not available or not configured.

**Troubleshooting steps:**

#### Step 1: Check Mode Configuration
For project modes, check [`.kilocode/modes/`](.kilocode/modes/):
```bash
dir .kilocode\modes
```

#### Step 2: Check Global Configuration
For Prompt Consultant mode, check:
```
C:/Users/pavel/vscodeportable/.kilocode/custom_modes.yaml
```

#### Step 3: Restart VS Code
After configuration changes, restart VS Code.

#### Step 4: Verify Mode Name
Use exact mode name:
- `architect` ✅
- `Architect` ❌
- `ARCHITECT` ❌

---

## Debugging Tips

### How to Enable Verbose Logging

#### VS Code Extension Logs
1. Open VS Code
2. Go to Help → Toggle Developer Tools
3. Check Console for Kilo Code logs
4. Look for errors and warnings

#### MCP Server Logs
MCP servers log to console. Check terminal output for server startup messages.

#### Enable Debug Mode
```
Request: "Enable verbose logging for debugging"
```

### Checking MCP Server Status

#### List Active Servers
```bash
# Check running processes
tasklist | findstr node

# Look for MCP server processes
```

#### Test Server Connectivity
```bash
# Test filesystem server
npx -y @modelcontextprotocol/server-filesystem C:/Users/pavel/projects

# Test memory server
npx -y @modelcontextprotocol/server-memory
```

#### Check Server Configuration
```bash
# View MCP configuration
type .kilocode\mcp.json

# Validate JSON
node -e "console.log(JSON.parse(require('fs').readFileSync('.kilocode/mcp.json', 'utf8')))"
```

### Verifying Memory Bank Files

#### Check File Existence
```bash
dir .kilocode\rules\memory-bank

# Expected: brief.md, product.md, context.md, architecture.md, tech.md
```

#### Validate File Content
```bash
# Check brief.md
type .kilocode\rules\memory-bank\brief.md

# Check product.md
type .kilocode\rules\memory-bank\product.md
```

#### Verify File Structure
Each Memory Bank file should have:
- Valid Markdown syntax
- Proper heading structure
- No corrupted characters

### Testing Individual Components

#### Test Memory Bank Loading
```
Request: "Load Memory Bank and confirm it's active"
```

Expected response: `[Memory Bank: Active]`

#### Test Mode Switching
```
Request: "Switch to Architect mode"
```

Expected: Mode switches successfully

#### Test Workflow Execution
```
Request: "Execute create-prompt workflow"
```

Expected: Workflow starts and guides through steps

#### Test MCP Operations
```
Request: "List all files in .kilocode directory"
```

Expected: File list returned successfully

### Getting Help and Support

#### Documentation Resources
- [`README.md`](README.md:1) - Main documentation
- [`SETUP.md`](SETUP.md:1) - Setup instructions
- [`USAGE.md`](USAGE.md:1) - Usage guide
- [`ARCHITECTURE.md`](ARCHITECTURE.md:1) - Architecture documentation
- [`AGENTS.md`](AGENTS.md:1) - Agent rules

#### Community Resources
- Kilo Code documentation
- GitHub issues
- Community forums

#### Diagnostic Information Collection
When seeking help, collect:
1. Error messages (exact text)
2. Steps to reproduce
3. System information:
   ```bash
   node --version
   npm --version
   npx --version
   ```
4. Configuration files:
   - [`.kilocode/mcp.json`](.kilocode/mcp.json:1)
   - [`.env`](.env:1) (redact sensitive data)
5. Memory Bank status:
   ```bash
   dir .kilocode\rules\memory-bank
   ```

#### Common Debugging Commands
```bash
# Check Node.js
node --version

# Check npm
npm --version

# Check npx
npx --version

# Check Git
git --version

# List .kilocode structure
dir .kilocode /s

# Check MCP configuration
type .kilocode\mcp.json

# Check environment variables
set

# Check running processes
tasklist | findstr node
```

---

## When to Contact Support

### Self-Service First
Before contacting support, try:
1. Search this troubleshooting guide
2. Check documentation files
3. Try the quick fixes
4. Review error messages

### When to Contact Support

Contact support when:

1. **Critical Issues**
   - Complete system failure
   - Data loss
   - Security concerns

2. **Persistent Issues**
   - Problem persists after trying all solutions
   - Issue affects multiple users
   - Regression (previously working feature broken)

3. **Complex Issues**
   - Multiple interconnected problems
   - Requires deep technical knowledge
   - Involves custom configurations

4. **Documentation Gaps**
   - Missing information in docs
   - Unclear instructions
   - Outdated content

### Information to Provide

When contacting support, provide:

1. **Issue Description**
   - Clear description of the problem
   - Expected vs actual behavior
   - When the issue started

2. **Steps to Reproduce**
   - Step-by-step instructions
   - Minimal reproduction case
   - Screenshots if applicable

3. **System Information**
   ```bash
   node --version
   npm --version
   npx --version
   git --version
   ```

4. **Configuration**
   - [`.kilocode/mcp.json`](.kilocode/mcp.json:1) (redact sensitive paths)
   - [`.env`](.env:1) (redact sensitive data)
   - Mode being used

5. **Error Messages**
   - Exact error text
   - Stack traces
   - Log files

6. **Memory Bank Status**
   ```bash
   dir .kilocode\rules\memory-bank
   ```

### Support Channels

1. **GitHub Issues**
   - For bug reports
   - Feature requests
   - Documentation issues

2. **Community Forums**
   - General questions
   - Best practices
   - User discussions

3. **Direct Support**
   - For enterprise customers
   - Critical issues
   - Security concerns

### Expected Response Times

- **Critical Issues**: Within 24 hours
- **High Priority**: Within 48 hours
- **Normal Priority**: Within 3-5 business days
- **Low Priority**: Within 1 week

### Escalation Process

If issue is not resolved:

1. **First Response**
   - Initial troubleshooting
   - Request for more information

2. **Follow-up**
   - Additional solutions
   - Workarounds if available

3. **Escalation**
   - Senior engineer review
   - Potential hotfix

4. **Resolution**
   - Final solution
   - Documentation update
   - Prevention measures

---

## Additional Resources

### Related Documentation
- [`README.md`](README.md:1) - Project overview
- [`SETUP.md`](SETUP.md:1) - Setup instructions
- [`USAGE.md`](USAGE.md:1) - Usage guide
- [`ARCHITECTURE.md`](ARCHITECTURE.md:1) - Architecture details
- [`AGENTS.md`](AGENTS.md:1) - Agent rules
- [`SECURITY.md`](SECURITY.md:1) - Security guidelines

### Memory Bank Files
- [`.kilocode/rules/memory-bank/brief.md`](.kilocode/rules/memory-bank/brief.md:1) - Project brief
- [`.kilocode/rules/memory-bank/product.md`](.kilocode/rules/memory-bank/product.md:1) - Product description
- [`.kilocode/rules/memory-bank/context.md`](.kilocode/rules/memory-bank/context.md:1) - Current context
- [`.kilocode/rules/memory-bank/architecture.md`](.kilocode/rules/memory-bank/architecture.md:1) - Architecture
- [`.kilocode/rules/memory-bank/tech.md`](.kilocode/rules/memory-bank/tech.md:1) - Technical details

### Configuration Files
- [`.kilocode/mcp.json`](.kilocode/mcp.json:1) - MCP server configuration
- [`.env.template`](.env.template:1) - Environment variables template
- [`.gitignore`](.gitignore:1) - Git ignore patterns

---

## Quick Reference

### Common Commands

| Command | Purpose |
|---------|---------|
| `initialize memory bank` | Create Memory Bank files |
| `update memory bank` | Update all Memory Bank files |
| `Switch to [mode]` | Switch to specific mode |
| `Execute [workflow]` | Run a workflow |
| `List files in [path]` | List directory contents |

### Common File Paths

| File | Purpose |
|------|---------|
| [`.kilocode/mcp.json`](.kilocode/mcp.json:1) | MCP server configuration |
| [`.kilocode/rules/memory-bank/`](.kilocode/rules/memory-bank/) | Memory Bank files |
| [`.kilocode/workflows/`](.kilocode/workflows/) | Workflow definitions |
| [`.kilocode/skills/`](.kilocode/skills/) | Skill definitions |
| [`.kilocode/rules-code/`](.kilocode/rules-code/) | Code mode rules |
| [`.env`](.env:1) | Environment variables |

### Common Error Codes

| Error | Meaning | Solution |
|-------|---------|----------|
| `Memory Bank: Missing` | Memory Bank not found | Run `initialize memory bank` |
| `Permission denied` | Access denied | Check file permissions |
| `Server not found` | MCP server unavailable | Check Node.js and configuration |
| `Workflow not found` | Workflow file missing | Check file name and location |
| `Skill not loaded` | Skill name mismatch | Verify directory and frontmatter match |

---

**Last Updated:** 2026-02-10

**Version:** 1.0.0

**For questions or issues, please refer to the [When to Contact Support](#when-to-contact-support) section.**
