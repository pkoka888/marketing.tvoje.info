# Unified Agentic Platform Integration Plan

**Date**: 2026-02-17
**Purpose**: Align all CLI tools (Antigravity, Kilo, OpenCode, Cline) with consistent configuration

---

## Executive Summary

This project uses a **multi-agent platform** approach with 5 AI coding tools. Each tool has its own configuration system but shares common concepts (skills, rules, workflows). This plan documents how to align them for consistency and best practices.

---

## Current State Analysis

### 1. Antigravity (Google)

| Aspect        | Location                                                               | Status               |
| ------------- | ---------------------------------------------------------------------- | -------------------- |
| **Config**    | `GEMINI.md` (root + `.gemini/`)                                        | ✅ Exists            |
| **Skills**    | `.agent/skills/` (project) or `~/.gemini/antigravity/skills/` (global) | ⚠️ Need to create    |
| **MCP**       | `.antigravity/mcp.json`                                                | ✅ Just created      |
| **Workflows** | `.agent/workflows/`                                                    | ✅ Already exists    |
| **Knowledge** | Uses context from files                                                | ⚠️ Needs enhancement |

**Key Finding**: Antigravity uses `GEMINI.md` (NOT `AGENTS.md`). Priority: `AGENTS.md` → `GEMINI.md` → defaults

### 2. OpenCode

| Aspect        | Location                        | Status            |
| ------------- | ------------------------------- | ----------------- |
| **Config**    | `.opencode/` or `opencode.json` | ✅ Exists         |
| **Skills**    | `.opencode/skill/`              | ✅ Exists         |
| **Agents**    | `.opencode/agent/`              | ⚠️ Need to create |
| **Rules**     | Reads `AGENTS.md`               | ✅ Supported      |
| **Workflows** | `.opencode/workflows/`          | ✅ Exists         |

### 3. Kilo Code

| Aspect        | Location               | Status      |
| ------------- | ---------------------- | ----------- |
| **Config**    | `.kilocode/`           | ✅ Complete |
| **Rules**     | `.kilocode/rules-*/`   | ✅ Complete |
| **Skills**    | `.kilocode/skills/`    | ✅ Complete |
| **Workflows** | `.kilocode/workflows/` | ✅ Complete |
| **Modes**     | `.kilocodemodes`       | ✅ Complete |

### 4. Cline

| Aspect        | Location                 | Status    |
| ------------- | ------------------------ | --------- |
| **Config**    | `.clinerules/`           | ✅ Exists |
| **Skills**    | `.clinerules/skills/`    | ✅ Exists |
| **Workflows** | `.clinerules/workflows/` | ✅ Exists |
| **Hooks**     | `.clinerules/hooks/`     | ✅ Exists |

### 5. Claude Code

| Aspect       | Location                | Status       |
| ------------ | ----------------------- | ------------ |
| **Config**   | `.claude/`              | ✅ Exists    |
| **Settings** | `.claude/settings.json` | ✅ Exists    |
| **Rules**    | Uses `CLAUDE.md`        | ✅ Supported |

---

## Configuration Comparison Matrix

| Feature          | Antigravity             | OpenCode               | Kilo                   | Cline                    | Claude      |
| ---------------- | ----------------------- | ---------------------- | ---------------------- | ------------------------ | ----------- |
| **Skills**       | `.agent/skills/`        | `.opencode/skill/`     | `.kilocode/skills/`    | `.clinerules/skills/`    | N/A         |
| **Rules**        | `GEMINI.md`             | `AGENTS.md`            | `.kilocode/rules-*/`   | `.clinerules/`           | `CLAUDE.md` |
| **Workflows**    | `.agent/workflows/`     | `.opencode/workflows/` | `.kilocode/workflows/` | `.clinerules/workflows/` | N/A         |
| **MCP**          | `.antigravity/mcp.json` | `opencode.json`        | `.kilocode/mcp.json`   | Via config               | Via config  |
| **Project File** | `GEMINI.md`             | `AGENTS.md`            | N/A                    | N/A                      | `CLAUDE.md` |

---

## Key Research Findings (2026)

### Antigravity Best Practices

1. **Skills System**
   - Use `SKILL.md` with YAML frontmatter
   - Location: `.agent/skills/` (project) or `~/.gemini/antigravity/skills/` (global)
   - Auto-discovered at conversation start

2. **GEMINI.md vs AGENTS.md**
   - Antigravity reads `GEMINI.md` specifically
   - Does NOT automatically read `AGENTS.md`
   - Recommendation: Keep both synced

3. **Agent Orchestration**
   - Use Agent Manager view for multi-agent
   - Swarm mode for parallel agents
   - Artifact-first protocol for outputs

4. **MCP Configuration**
   - Project-level: `.antigravity/mcp.json`
   - Global: `~/.gemini/antigravity/mcp.json`

### OpenCode Best Practices

1. **Config Precedence** (later overrides earlier):
   - Inline config → `.opencode/` → Project config → Global → Remote

2. **AGENTS.md Support**
   - Full support for project instructions
   - Use `/init` to auto-generate

### Kilo Code Best Practices

1. **Modes System**
   - Use `.kilocodemodes` for mode definitions
   - Modes: default, code, architect, debug, sysadmin

2. **Custom Rules**
   - Plain text or Markdown
   - Mode-specific: `rules-code`, `rules-architect`, etc.

---

## Integration Actions

### Phase 1: Core Alignment (Priority: Critical)

| #   | Action                                                | Target      | Status       |
| --- | ----------------------------------------------------- | ----------- | ------------ |
| 1.1 | Sync GEMINI.md with AGENTS.md content                 | Antigravity | ✅ Completed |
| 1.2 | Add Antigravity skills from existing .kilocode/skills | Antigravity | ✅ Completed |
| 1.3 | Ensure MCP parity across all tools                    | All         | ✅ Completed |
| 1.4 | Add .agent/skills/ directory                          | Project     | ✅ Completed |

### Phase 2: Enhanced Configuration (Priority: High)

| #   | Action                                         | Target      | Status       |
| --- | ---------------------------------------------- | ----------- | ------------ |
| 2.1 | Create unified AGENTS.md with all tool configs | Project     | ⏳ Pending   |
| 2.2 | Add OpenCode agents from .agent/agents         | OpenCode    | ⏳ Pending   |
| 2.3 | Create CLI tool comparison skill               | All         | ⏳ Pending   |
| 2.4 | Document fallback strategies                   | All         | ⏳ Pending   |
| 2.5 | Align Antigravity with Memory Bank             | Antigravity | ✅ Completed |

### Phase 3: Advanced Integration (Priority: Medium)

| #   | Action                                      | Target | Status     |
| --- | ------------------------------------------- | ------ | ---------- |
| 3.1 | Implement cross-tool orchestration workflow | All    | ⏳ Pending |
| 3.2 | Create skill sharing pipeline               | All    | ⏳ Pending |
| 3.3 | Add verification automation                 | All    | ⏳ Pending |

---

## Fallback Strategy

When one tool fails or is unavailable:

| Primary                    | Fallback 1      | Fallback 2 |
| -------------------------- | --------------- | ---------- |
| Antigravity (Gemini 3 Pro) | OpenCode (Groq) | Kilo Code  |
| OpenCode                   | Kilo Code       | Cline      |
| Kilo Code                  | Cline           | OpenCode   |
| Cline                      | Kilo Code       | OpenCode   |

---

## Quality Assurance

All configurations must pass:

1. `python scripts/verify_agentic_platform.py` - Exit 0
2. JSON/YAML validation
3. File existence checks
4. Cross-reference consistency

---

## References

- Antigravity Docs: https://antigravity.google/docs
- Kilo Code Docs: https://kilo.ai/docs
- OpenCode Docs: https://opencode.ai/docs
- Cline Docs: https://docs.cortecs.ai
- Agent Skills Spec: https://antigravity.codes/blog/mastering-agent-skills
