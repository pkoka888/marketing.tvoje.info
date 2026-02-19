# Parallel Configuration Audit - Phase 2

**Date:** 2026-02-19 **Status:** POST-IDE-RESTART VERIFICATION

---

## Overview

After IDE restart with new MCP configurations, we need to verify no hardcoded
paths or environment syntax issues remain. Three parallel audit tasks will run
across different agent frameworks.

---

## Task Distribution

| Task       | Agent     | Focus Area                   | Output File                                    |
| ---------- | --------- | ---------------------------- | ---------------------------------------------- |
| **Task 1** | Cline     | Hardcoded Windows paths      | `plans/parallel-audit/paths-report.md`         |
| **Task 2** | Kilo Code | Environment variable syntax  | `plans/parallel-audit/env-syntax-report.md`    |
| **Task 3** | OpenCode  | Cross-platform compatibility | `plans/parallel-audit/compatibility-report.md` |

---

## Task 1: Hardcoded Windows Paths Audit (Cline)

**Agent:** @cline **Model:** minimax-m2.1:free **Scope:** Search for hardcoded
paths that break on different systems

### Search Patterns

```regex
# Windows absolute paths
[Cc]:[/\\][^\s"'\n]+[/\\][^\s"'\n]+
[Cc]:\\[^\s"'\n]+

# User-specific paths
[/\\][Uu]sers[/\\][^/\\\s"'\n]+
[/\\]home[/\\][^/\\\s"'\n]+

# Hardcoded project paths
marketing\.tvoje\.info[^\s"'\n]*
vscodeportable[^\s"'\n]*
nvm4w[^\s"'\n]*

# IP addresses (should be in secrets)
\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b
```

### File Types to Check

- `.json` - Config files
- `.yml`, `.yaml` - Workflow files
- `.md` - Documentation
- `.js`, `.ts`, `.mjs` - Scripts
- `.py` - Python scripts
- `.sh`, `.ps1`, `.bat` - Shell scripts

### Output Format

Create: `plans/parallel-audit/paths-report.md`

```markdown
# Hardcoded Paths Audit Report

## Critical (Must Fix)

| File | Line | Pattern      | Recommendation               |
| ---- | ---- | ------------ | ---------------------------- |
| file | 12   | C:\Users\... | Use env var or relative path |

## High Priority

...

## Medium Priority

...
```

---

## Task 2: Environment Variable Syntax Audit (Kilo Code)

**Agent:** @kilo (bmad-dev mode) **Model:** x-ai/grok-code-fast-1:optimized:free
**Scope:** Find broken environment variable syntax

### Search Patterns

```regex
# Invalid syntax (doesn't work in most shells)
\$\{[A-Z_]+\}

# Valid alternatives to check
process\.env\.
[Ba]nner\.[a-z]+
\{env:[A-Z_]+\}
os\.environ\.get
```

### Check These Configs

- `.kilocode/mcp.json`
- `.clinerules/mcp.json`
- `.antigravity/mcp.json`
- `opencode.json`
- `.github/workflows/*.yml`
- `.env.example`
- `.env.template`

### Output Format

Create: `plans/parallel-audit/env-syntax-report.md`

```markdown
# Environment Variable Syntax Audit

## Invalid Syntax Found (${VAR})

| File     | Line | Variable       | Current | Should Be               |
| -------- | ---- | -------------- | ------- | ----------------------- |
| mcp.json | 42   | REDIS_PASSWORD | ${...}  | Use wrapper or env file |

## Valid Alternatives in Use

...

## Recommendations

...
```

---

## Task 3: Cross-Platform Compatibility Audit (OpenCode)

**Agent:** @researcher **Model:** big-pickle **Scope:** Verify configs work on
Windows, Linux, macOS

### Check These Issues

#### 1. Path Separators

```regex
# Windows backslash (may break on Unix)
\\\\[^\s"']+

# Unix forward slash (generally safe)
/[^\s"']+
```

#### 2. Command Differences

- `npx` vs direct `node` paths
- `uvx` availability
- Shell-specific syntax (`&&` vs `;`)

#### 3. MCP Server Commands

Check these work cross-platform:

- `node /c/nvm4w/...` (Git Bash path)
- `npx -y @modelcontextprotocol/...`
- `uvx mcp-server-*`

### Output Format

Create: `plans/parallel-audit/compatibility-report.md`

```markdown
# Cross-Platform Compatibility Report

## Windows-Specific Issues

| File | Issue | Impact | Fix |
| ---- | ----- | ------ | --- |
| ...  | ...   | ...    | ... |

## Linux/macOS Issues

...

## Universal Solutions

...
```

---

## Coordination Rules

### 1. No Overlapping Edits

Each agent works on their own report file. No code changes without explicit
approval.

### 2. Shared Findings

If an agent finds issues in another agent's scope:

- Document in their report
- Add reference: "See Task X report for details"

### 3. Completion Signal

Each agent ends with:

```
## Completion Status
- [ ] Task complete
- Files created/modified: [list]
- Critical issues found: [count]
- Ready for review: [yes/no]
```

### 4. Aggregation

After all three tasks complete, @orchestrator will:

1. Read all three reports
2. Create consolidated action plan
3. Prioritize fixes
4. Assign implementation tasks

---

## Files to Create

```
plans/parallel-audit/
├── paths-report.md (Cline)
├── env-syntax-report.md (Kilo Code)
├── compatibility-report.md (OpenCode)
└── consolidated-action-plan.md (Orchestrator - after all complete)
```

---

## Success Criteria

- [ ] All three reports created
- [ ] No `${VAR}` syntax remains in active configs
- [ ] Hardcoded paths documented with migration plan
- [ ] Cross-platform compatibility verified
- [ ] Consolidated action plan created

---

## Quick Start Commands

### For Cline (Task 1):

```bash
# Search for hardcoded paths
grep -r "C:\\\\\\\\|c:\\\\\\\\|/c/" --include="*.json" --include="*.yml" --include="*.yaml" . 2>/dev/null | grep -v node_modules | grep -v ".git"
```

### For Kilo Code (Task 2):

```bash
# Search for env var syntax
grep -r '\${' --include="*.json" --include="*.yml" --include="*.yaml" . 2>/dev/null | grep -v node_modules | grep -v ".git"
```

### For OpenCode (Task 3):

```bash
# Check path formats
grep -r "command.*node" --include="*.json" . 2>/dev/null | grep -v node_modules
```

---

_Phase 2 orchestration plan created: 2026-02-19_
