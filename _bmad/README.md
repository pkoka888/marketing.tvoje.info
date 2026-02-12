# BMAD Integration

This directory contains the BMAD (Business-Minded Agile Development) structure for the project.

## Integration Points

### 1. Kilo Agent Integration
The Kilo agent (`.kilocode/`) uses BMAD workflows for structured tasks.
- **Rules**: `.kilocode/rules-architect/` maps to `_bmad/bmm/workflows/2-plan/`
- **Memory**: `.kilocode/rules/memory-bank/` is synchronized with `_bmad/_memory/` via `scripts/sync-memory-bank.js`.

### 2. Antigravity Integration (MCP)
Antigravity connects to BMAD via the `bmad-mcp` server defined in `.kilocode/mcp.json`.
- **Tools**: Access to `bmad-method` CLI and internal workflows.
- **Knowledge**: Reads from `_bmad/_config/` for project context.

### 3. Execution
To run BMAD workflows manually:
```bash
# Run a specific workflow
npx bmad-method run --workflow "1-analysis"

# List available agents
npx bmad-method list agents
```

## Structure
- `_config/`: BMAD configuration.
- `_memory/`: Project memory and context.
- `bmm/`: Business Model Methodology artifacts.
- `core/`: Core definitions.

## Maintenance
- Ensure `scripts/sync-memory-bank.js` is run before major planning sessions.
- Use `npx bmad-method update` to pull latest templates.
