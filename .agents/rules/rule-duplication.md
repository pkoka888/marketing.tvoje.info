# Rule Duplication Across Agents

## Purpose

Define the process for ensuring critical rules are consistently applied across all agent frameworks (Kilo Code, Cline, Gemini, Antigravity).

## When to Duplicate Rules

A rule MUST be distributed to ALL agent frameworks when it:

1. **Safety Critical** - Affects safety/critical operations (cleanup, deletion, server modifications)
2. **State Modifying** - Changes infrastructure state
3. **Cost Impacting** - Impacts budget or costs
4. **Security Related** - Changes security posture
5. **Shared Knowledge** - Contains information all agents need

## Agent Framework Directories

| Framework   | Rules Directory         | Primary Use                    |
| ----------- | ----------------------- | ------------------------------ |
| Kilo Code   | `.kilocode/rules-code/` | Development, implementation    |
| Cline       | `.clinerules/`          | Code validation, quality gates |
| Antigravity | `.agents/`              | Orchestration, planning        |
| Gemini      | `.gemini/`              | Research, analysis             |

## Process

### Step 1: Create Rule in Primary Location

```bash
# Usually in .kilocode/rules-code/ for implementation rules
# Or .agents/rules/ for orchestration rules
```

### Step 2: Evaluate Scope

Ask: "Does this apply to other agents?"

| If Answer                | Then                           |
| ------------------------ | ------------------------------ |
| YES - All agents need it | Proceed to Step 3              |
| NO - Single agent only   | Keep in original location only |

### Step 3: Distribute

Copy to all relevant directories:

```bash
# Example for server preservation rule
cp .kilocode/rules-code/server-preservation.md .agents/rules/
cp .kilocode/rules-code/server-preservation.md .gemini/rules/
```

### Step 4: Validate

Run consistency check:

```bash
python .agent/workflows/weekly-consistency.py
```

### Step 5: Document

Update relevant documentation to reference cross-agent rules.

## Weekly Consistency Analysis

### Schedule

Every Sunday at 18:00 (or on-demand)

### Checks

1. **Rule Synchronization** - Compare rules across directories
2. **API Key Patterns** - Detect secrets in .env files
3. **Health Check Alignment** - MCP and service availability
4. **MCP Server Status** - Redis, filesystem, memory servers

### Output

Report saved to: `plans/agent-consistency-check.md`

### Flagged Issues

- Missing rule copies in other directories
- Inconsistent rule versions
- Configuration drift

## Cross-Reference Table

| Rule                | Kilo | Cline | Agents | Gemini |
| ------------------- | ---- | ----- | ------ | ------ |
| server-preservation | ✅   | ✅    | ✅     | ✅     |
| python-preferred    | ✅   | ✅    | ❌     | ❌     |
| bmad-integration    | ✅   | ✅    | ✅     | ❌     |
| cost-optimization   | ✅   | ✅    | ✅     | ✅     |

## Related Files

- `.agent/workflows/weekly-consistency.py` - Automated checker
- `.kilocode/rules-code/server-preservation.md` - Original rule
- `.agents/rules/server-preservation.md` - Agent copy
- `.gemini/rules/server-preservation.md` - Gemini copy

## Enforcement

1. **On Rule Creation**: Always evaluate if duplication needed
2. **On Agent Failure**: Check rule consistency first
3. **Weekly**: Run automated consistency check
4. **On Incident**: Verify rule application before cleanup

## Emergency Override

If rule duplication is not feasible (e.g., time constraints):

1. Document the exception
2. Set reminder to fix within 48 hours
3. Note in `plans/agent-consistency-check.md`
