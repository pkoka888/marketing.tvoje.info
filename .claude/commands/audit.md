Run a full cross-agent platform integrity check for the Unified Agentic Platform 2026.

Steps:
1. Run `python scripts/verify_agentic_platform.py` and report all failures
2. Verify all `file://` prompt paths in `.kilocode/agents/*.json` actually resolve on disk
3. Verify all `source:` paths in `.agent/agents.yaml` exist on disk
4. Compare `.agent/workflows/` vs `.clinerules/workflows/` — list any files that exist in one but not the other
5. Check that critical rules (server-preservation, python-preferred, cost-optimization, bmad-integration) exist in all rule dirs: `.kilocode/rules/`, `.agents/rules/`, `.clinerules/skills/`
6. Confirm `CLAUDE.md` exists at project root and `.claude/settings.json` is present
7. Summarize: how many checks passed, how many failed, list all broken items with file paths
