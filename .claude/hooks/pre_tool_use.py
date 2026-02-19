#!/usr/bin/env python3
"""
Claude Code PreToolUse hook — Cross-agent sync enforcement + cost-gate.
Detects writes to agent config dirs + expensive model usage.
"""
import json
import sys

AGENT_DIRS = [
    ".kilocode/",
    ".clinerules/",
    ".agent/",
    ".agents/",
    ".claude/",
    ".gemini/",
]

# Expensive model keywords that trigger cost-gate reminder
EXPENSIVE_MODEL_KEYWORDS = [
    "claude-opus",
    "claude-sonnet",
    "claude-4",
    "gemini-2.5-pro",
    "gemini-pro",
    "openai-o3",
    "openai-o1",
    "o3",
    "o1",
    "anthropic",
    "sonnet-4-5",
    "sonnet-4.5",
    "opus-4.6"
]

SYNC_NOTE = (
    "\n### Cross-Agent Sync Protocol (MANDATORY)\n"
    "You are writing to an agent config directory. Before proceeding:\n"
    "1. Read the canonical version in `.kilocode/rules/` FIRST\n"
    "2. After this change, update equivalent files in ALL other agent dirs\n"
    "3. Run: `python scripts/verify_agentic_platform.py`\n"
    "Canonical store: `.kilocode/rules/` | Governance: `AGENTS.md`\n"
)

COST_GATE_NOTE = (
    "\n### Cost-Gate Reminder (plan-approval-required)\n"
    "You appear to be using an expensive model. Per "
    "`.kilocode/rules/plan-approval-required`:\n"
    "- Free models (Kilo, OpenCode, Cline) should be tried FIRST\n"
    "- Expensive models (Claude Opus/Sonnet, Gemini 2.5 Pro, "
    "OpenAI o3) require plan approval\n"
    "- Document why free alternatives cannot handle the task\n"
    "- Log usage in `.kilocode/rules/cost-optimization`\n"
    "Rule: `.kilocode/rules/plan-approval-required` | "
    "Free alternatives: `.kilocode/rules/cost-optimization`\n"
)


def check_expensive_model_reminder(tool_name: str, arguments: dict) -> str:
    """
    Check if expensive model usage is detected in the tool arguments.
    Returns a reminder string if detected, empty string otherwise.
    """
    # Check common argument fields that might contain model names
    search_text = ""

    # Check model or model_name field
    if isinstance(arguments, dict):
        model = arguments.get("model", "") or arguments.get("model_name", "")
        prompt = (
            arguments.get("prompt", "") or
            arguments.get("system_prompt", "")
        )

        # Combine relevant fields for searching
        search_text = f"{model} {prompt}".lower()

    # Also check string arguments directly
    if isinstance(arguments, str):
        search_text = arguments.lower()

    # Check for expensive model keywords
    for keyword in EXPENSIVE_MODEL_KEYWORDS:
        if keyword.lower() in search_text:
            return COST_GATE_NOTE

    return ""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    path = tool_input.get("path", "") or tool_input.get("file_path", "")

    result = {"decision": "allow"}
    reasons = []

    # Check for agent config directory sync reminder
    if tool in ("Write", "Edit", "MultiEdit") and path and any(
        d in path for d in AGENT_DIRS
    ):
        reasons.append(SYNC_NOTE)

    # Check for expensive model usage reminder
    model_reminder = check_expensive_model_reminder(tool, tool_input)
    if model_reminder:
        reasons.append(model_reminder)

    # Combine all reasons
    if reasons:
        result["reason"] = "".join(reasons)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
