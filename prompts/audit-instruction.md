# Kilo Code Audit Instruction (Phase 4)

## Context

You are the **Lead Auditor** for the "Agentic Platform 2026". Your goal is to map the current implementation against the "Phase 3 Optimization" goals and identify gaps using the new standard templates.

## Mission

1.  **Read Governance & Documentation**:
    - `AGENTS.md` (Source of Truth)
    - `opencode.json` (Model Config)
    - `.github/workflows/bmad.yml` (CI/CD)
    - `docs/DEPLOYMENT.md` (Deployment Strategy)
    - `docs/VERIFICATION.md` (Testing Strategy)
    - `.clinerules/workflows/orchestrate-parallel.md` (Handoff Protocol)

2.  **Execute Audit**:
    - Verify **Model Hierarchy**: Does `opencode.json` match `AGENTS.md`'s 7-layer priority?
    - Verify **Redis Safety**: Is `scripts/verify_redis.py` robust? Does it check namespaces?
    - Verify **Documentation**: Do `docs/` match the actual `deploy.yml` workflow?
    - Verify **Protocol**: Does the orchestration workflow include the Handoff Protocol?

3.  **Output Report**:
    - Use the template at `plans/templates/AUDIT_REPORT.md`.
    - Fill it comprehensively.
    - Save it to `plans/reports/audit-kilo-phase4.md`.

4.  **Gap Analysis**:
    - Compare `AGENTS.md` promises vs. codebase reality.
    - List any missing automations or documentation.

## Constraints

- **Tone**: Critical, objective, evidence-first.
- **Format**: Markdown.
- **Tools**: Use `read_file`, `grep_search`.

## Execution Command

```bash
# Run this entire prompt content
cat prompts/audit-instruction.md | kilo run --model "gemini/gemini-2.5-flash"
```
