#!/usr/bin/env python3
"""
Claude Code PreToolUse hook — Cross-agent sync enforcement.
Detects writes to any agent config directory and injects mandatory sync reminder.
"""
import json
import sys

AGENT_DIRS = [".kilocode/", ".clinerules/", ".agent/", ".agents/", ".claude/", ".gemini/"]
SYNC_NOTE = (
    "\n### Cross-Agent Sync Protocol (MANDATORY)\n"
    "You are writing to an agent config directory. Before proceeding:\n"
    "1. Read the canonical version in `.kilocode/rules/` FIRST\n"
    "2. After this change, update equivalent files in ALL other agent dirs\n"
    "3. Run: `python scripts/verify_agentic_platform.py`\n"
    "Canonical store: `.kilocode/rules/` | Governance: `AGENTS.md`\n"
)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    path = tool_input.get("path", "") or tool_input.get("file_path", "")

    result = {"decision": "allow"}

    if tool in ("Write", "Edit", "MultiEdit") and path and any(d in path for d in AGENT_DIRS):
        result["reason"] = SYNC_NOTE

    print(json.dumps(result))


if __name__ == "__main__":
    main()
