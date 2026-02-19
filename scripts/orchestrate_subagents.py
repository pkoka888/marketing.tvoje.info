#!/usr/bin/env python3
"""
Subagent Orchestrator for Audit Fixes
Executes audit fixes in parallel using subagents via MCP.

Usage:
    python scripts/orchestrate_subagents.py           # Run all fixes
    python scripts/orchestrate_subagents.py --list     # List tasks only
    python scripts/orchestrate_subagents.py --dry-run # Show what would run
"""

import os
import sys
import json
from pathlib import Path

# This script defines the tasks - execution happens via use_subagents tool
# The prompts are structured for parallel execution with distinct file targets

AUDIT_FIX_TASKS = [
    {
        "agent": "bmad-fix-chinese",
        "description": "Fix Chinese character in plan-approval-required",
        "severity": "CRITICAL",
        "prompt": """Fix the Chinese character corruption in all 4 copies of plan-approval-required.

Find 'cannot胜任' (around line 52) and replace with 'cannot handle the task'.

Target files:
- .kilocode/rules/plan-approval-required
- .agents/rules/plan-approval-required
- .clinerules/skills/plan-approval-required
- .gemini/rules/plan-approval-required

This is a simple find/replace - use free model x-ai/grok-code-fast-1:optimized:free.""",
        "files": [".kilocode/rules/plan-approval-required", ".agents/rules/plan-approval-required", ".clinerules/skills/plan-approval-required", ".gemini/rules/plan-approval-required"]
    },
    {
        "agent": "bmad-fix-tiers",
        "description": "Fix LiteLLM tier labels in cost-optimization",
        "severity": "MEDIUM",
        "prompt": """Fix the LiteLLM tier labels in all 4 copies of cost-optimization.

Replace the entire LiteLLM section with:
```
### LiteLLM (Self-Hosted Proxy, port 4000)
See `litellm/proxy_config.yaml` for full config:
- T1 FREE: `minimax-free`, `glm4-free`, `qwen3-coder-free`, `deepseek-r1-free` (OpenRouter)
- T2 FREE: `gemini-flash` (15 RPM), `gemini-pro` (2 RPM) (Google free tier)
- T3 PAID: `groq-llama-8b` ($0.05/$0.08), `groq-llama-70b` ($0.59/$0.79) (Groq)
- T4 PAID: `gpt-4o-mini` (OpenAI — last resort)
Fallback chain: T1 → T2 → T3 → T4
```

Target files:
- .kilocode/rules/cost-optimization
- .agents/rules/cost-optimization
- .clinerules/skills/cost-optimization
- .gemini/rules/cost-optimization""",
        "files": [".kilocode/rules/cost-optimization", ".agents/rules/cost-optimization", ".clinerules/skills/cost-optimization", ".gemini/rules/cost-optimization"]
    },
    {
        "agent": "bmad-fix-agent-name",
        "description": "Fix new_plan.py agent name",
        "severity": "MEDIUM",
        "prompt": """In scripts/new_plan.py line 28, change:
`"{{AGENT_NAME}}": lambda: "Cline",`
to:
`"{{AGENT_NAME}}": lambda: "Agent",`

This is a simple edit - use free model.""",
        "files": ["scripts/new_plan.py"]
    },
    {
        "agent": "bmad-fix-typo",
        "description": "Fix GAP_ANALYSIS typo",
        "severity": "LOW",
        "prompt": """In plans/templates/GAP_ANALYSIS.md, fix the typo:
Change 'RESEARCH_FFINDINGS' to 'RESEARCH_FINDINGS'

This is a simple find/replace - use free model.""",
        "files": ["plans/templates/GAP_ANALYSIS.md"]
    },
    {
        "agent": "bmad-update-context",
        "description": "Update memory-bank context.md",
        "severity": "LOW",
        "prompt": """Update .kilocode/rules/memory-bank/context.md with:

# Context — Current Task

- Phase: POST_IMPLEMENTATION_CLEANUP
- Active tasks: Fix audit findings, prepare commit
- Last verified: 2026-02-19 (verify_agentic_platform.py: PASS)
- Uncommitted: 79 files (plan-approval-required, cost-opt, templates, API hardening)

Replace the entire file content with this.""",
        "files": [".kilocode/rules/memory-bank/context.md"]
    },
    {
        "agent": "bmad-create-readme",
        "description": "Create scripts/README.md",
        "severity": "ENHANCEMENT",
        "prompt": """Create scripts/README.md with this content:

# Scripts Documentation

This directory contains automation scripts for the marketing.tvoje.info project.

## Script Inventory

| Script | Purpose | Creator |
|--------|---------|---------|
| verify_agentic_platform.py | Cross-agent integrity check | Claude Code |
| verify_api_keys.py | API key verification (19 keys) | Kilo Code |
| validate_kilo_configs.py | YAML/JSON schema validation | Kilo Code |
| template_reference_manager.py | Template metadata manager | Claude Code |
| populate_template_references.py | Populate template cross-refs | Claude Code |
| validate_template_references.py | Validate template refs | Claude Code |
| template_index.py | Cross-reference table | Claude Code |
| new_plan.py | Plan creator from templates | Cline + Kilo |
| generate_images.py | AI image generation | Claude Code |
| orchestrate_flash.py | Flash orchestration | Kilo Code |
| orchestrate_subagents.py | Subagent orchestration | Kilo Code |
| swarm_audit.py | Swarm-based audit | Kilo Code |
| update_free_models.py | Free model list updater | Kilo Code |
| search_npm.py | NPM package search | Kilo Code |
| setup_mcp_servers.py | MCP server setup | Kilo Code |
| check_redis.py | Redis connectivity check | Claude Code |
| validate_env.py | .env validation | Kilo Code |
| protected/snapshot_config.py | Config drift detection | Kilo Code |

## Usage

```bash
# Verify platform
python scripts/verify_agentic_platform.py

# Create plan
python scripts/new_plan.py --list
```""",
        "files": ["scripts/README.md"]
    },
    {
        "agent": "bmad-refactor-dry",
        "description": "DRY refactor snapshot_config.py",
        "severity": "ENHANCEMENT",
        "prompt": """Refactor scripts/protected/snapshot_config.py to eliminate hardcoded config.

In the get_current_config() function:
1. Add try/except to import API_KEYS_CONFIG from scripts/verify_api_keys.py
2. Extract endpoint/method/auth_type from each key config
3. Keep fallback hardcoded dict for when import fails

Example structure:
```python
def get_current_config():
    try:
        from verify_api_keys import API_KEYS_CONFIG
        config = {}
        for key_name, key_data in API_KEYS_CONFIG.items():
            config[key_name] = {
                "endpoint": key_data.get("endpoint"),
                "method": key_data.get("method", "GET"),
                "auth_type": key_data.get("auth_type"),
                ...
            }
        return config
    except ImportError:
        # Fallback - keep existing hardcoded dict
        return {...}
```

Use free model for this refactor.""",
        "files": ["scripts/protected/snapshot_config.py"]
    }
]

VERIFICATION_GATES = [
    ("verify_agentic_platform", "python scripts/verify_agentic_platform.py"),
    ("validate_template_references", "python scripts/validate_template_references.py"),
    ("new_plan_list", "python scripts/new_plan.py --list")
]


def list_tasks():
    """List all tasks without executing."""
    print("\n📋 Audit Fix Tasks (7 total)")
    print("=" * 60)
    for i, task in enumerate(AUDIT_FIX_TASKS, 1):
        severity = task["severity"]
        severity_emoji = {"CRITICAL": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "ENHANCEMENT": "🔵"}.get(severity, "⚪")
        print(f"\n{i}. {severity_emoji} {task['description']} ({severity})")
        print(f"   Agent: {task['agent']}")
        print(f"   Files: {', '.join(task['files'])}")

    print("\n" + "=" * 60)
    print("📋 Verification Gates (3 total)")
    print("=" * 60)
    for name, cmd in VERIFICATION_GATES:
        print(f"  • {name}: {cmd}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Subagent Orchestrator for Audit Fixes")
    parser.add_argument("--list", action="store_true", help="List tasks only")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run")
    args = parser.parse_args()

    if args.list:
        list_tasks()
        return 0

    print("""
🎯 SUBAGENT ORCHESTRATION FOR AUDIT FIXES

This script defines 7 parallel subagent tasks and 3 sequential verification gates.

To execute:
1. Use use_subagents tool with prompts from AUDIT_FIX_TASKS
2. Run verification gates after all fixes complete

Tasks:
""")
    list_tasks()

    print("""
USAGE:
- This script defines the prompts for use_subagents tool
- Execute in parallel using the prompts above
- Then run verification gates sequentially
""")

    return 0


if __name__ == "__main__":
    sys.exit(main())
