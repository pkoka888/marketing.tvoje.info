---
description: Run full cross-agent platform integrity check
subtask: true
model: groq/llama-3.1-8b-instant
---

Run full cross-agent platform integrity check.

## Steps

1. Run the verify script:

!`python scripts/verify_agentic_platform.py`

2. Check that all `.kilocode/agents/*.json` prompt paths resolve to existing files
3. Verify `.agent/agents.yaml` source file references exist
4. Compare `.agent/workflows/` vs `.clinerules/workflows/` for missing workflows
5. Verify `.opencode/agent/coder.md` and `orchestrator.md` exist
6. Report all findings with pass/fail status

## Expected Output

- Exit 0: All checks pass
- Exit 1: List specific failures with file paths and remediation steps
