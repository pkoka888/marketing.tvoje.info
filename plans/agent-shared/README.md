# Agent Shared Plans

This directory is the cross-agent knowledge hub. All agents (Antigravity, Kilo Code, Cline, OpenCode) read and write here.

## Structure

```
plans/agent-shared/
├── README.md              # This file
├── audit-reports/          # Agent self-audit outputs
├── validation-reports/     # Cline validator outputs
└── error-logs/             # Aggregated error analysis
```

## Conventions

- File naming: `YYYY-MM-DD-{agent}-{topic}.md`
- Example: `2026-02-11-antigravity-foundation-audit.md`
- Reports should include: timestamp, agent name, findings, recommendations
- Use markdown for human readability
