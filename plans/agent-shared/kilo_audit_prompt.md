# Kilo Code Mission: Infrastructure Audit & Alignment

**Role**: Senior Infrastructure Auditor
**Objective**: Audit all 9 BMAD agents and the operational environment to ensure consistency, security, and proper resource usage.

## 1. Audit Targets

- **Agents**: Review all agents defined in:
  - `.agent/agents.yaml` (Antigravity registry)
  - `.kilocodemodes` (Kilo Code modes)
- **Infrastructure**:
  - MCP Servers (`.kilocode/mcp.json`)
  - Redis Usage (`ONE-AND-ONLY-REDIS` interaction)
  - Directory Permissions (`vscodeportable` vs project root)

## 2. Verification Criteria (The "Golden Rules")

For each agent, verify:

1.  **Read-Only Compliance**: Does the agent respect the `.clinerules/99-readonly-resources.md` rule? Check if they have write access into `vscodeportable` (should be FALSE).
2.  **Memory Loading**: Does the agent configuration (instructions/system prompt) explicitly load `_bmad/bmm/config.yaml` or project context at startup?
3.  **Redis Connection**: Does the agent use the shared `ONE-AND-ONLY-REDIS` MCP server, or is it trying to spawn its own Redis instance/connection? (It MUST use the shared MCP).
4.  **Playwright/Browser usage**: Is it correctly configured to use the `playwright` MCP server (once enabled)?

## 3. Deliverables

Produce a report in `plans/agent-shared/audit_report.md` with:

- **Agent Status Table**: [Agent Name] | [Read-Only Safe?] | [Memory Load?] | [Redis Safe?] | [Issues]
- **Discrepancies**: List any agent defining its own "brains" or ignoring the global `mcp.json`.
- **Action Plan**: Specific JSON/YAML updates needed to align all agents.

## 4. Execution

Run this audit immediately using your `read_file` and `grep_search` capabilities. Do NOT modify files yet; just report.
