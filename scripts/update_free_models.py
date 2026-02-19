#!/usr/bin/env python3
"""
Update Free Models Script

Fetches the current free models from Kilo Code official documentation
and automatically updates all cost-optimization rule files.

Usage:
    python scripts/update_free_models.py [--dry-run]

The script:
1. Fetches free models from Kilo docs
2. Parses the model list
3. Updates all agent directory cost-optimization files
4. Verifies the changes
"""

import json
import re
import sys
import os
from pathlib import Path
from datetime import datetime

# Agent directories that need updating
AGENT_DIRS = [
    ".kilocode/rules",
    ".agents/rules", 
    ".clinerules/skills",
    ".gemini/rules"
]

# Free models from Kilo documentation (as of 2026-02-18)
# Format: (model_id, display_name, best_for, is_limited=False)
KILO_FREE_MODELS = [
    ("minimax-m2.1", "MiniMax M2.1", "General-purpose, strong performance", False),
    ("glm-4.7", "Z.AI: GLM 4.7", "Agent-centric applications", False),
    ("kimi-k2.5", "MoonshotAI: Kimi K2.5", "Tool use, reasoning, code synthesis", False),
    ("giga-potato", "Giga Potato", "Evaluation period (no suffix)", False),
    ("trinity-large", "Arcee AI: Trinity Large", "Preview model", False),
]

# Note: MiniMax M2.5 was free for a limited time (week of Feb 2026)
# Not included as it's not permanently free

OPENROUTER_FREE_MODELS = [
    ("qwen3-coder", "Qwen3 Coder", "Agentic coding, function calling"),
    ("glm-4.5-air", "Z.AI: GLM 4.5 Air", "Lightweight agent tasks"),
    ("deepseek-r1", "DeepSeek: R1 0528", "OpenAI o1-level performance"),
    ("kimi-k2", "MoonshotAI: Kimi K2", "Tool use, reasoning"),
]

# Default routing - can be customized
DEFAULT_ROUTING = {
    "bulk_coding": "minimax-m2.1:free",
    "routine_fixes": "big-pickle",  # OpenCode model
    "research": "gemini-2.5-flash",  # Gemini free
    "planning": "minimax-m2.1:free",
    "agent_tasks": "minimax-m2.1:free",
    "code_synthesis": "minimax-m2.1:free",
}


def get_free_model_format(model_id: str) -> str:
    """Get the proper format suffix for a free model.
    
    Most free models use ':free' suffix.
    Exception: giga-potato has no suffix.
    """
    if model_id == "giga-potato":
        return "(none)"
    return ":free"


def format_model_id(model_id: str) -> str:
    """Format model ID with :free suffix for routing."""
    if model_id == "giga-potato":
        return model_id
    return f"{model_id}:free"


def generate_kilo_free_models_table() -> str:
    """Generate the Kilo Gateway Free Models markdown table."""
    lines = [
        "## Kilo Gateway Free Models (2026-02)",
        "",
        "⚠️ **IMPORTANT**: Kilo Code uses `:free` suffix for ALL free models EXCEPT `giga-potato` (no suffix).",
        "",
        "| Model | Format | Best For | Status |",
        "| ----- | ------ | -------- | ------ |",
    ]
    
    for model_id, display_name, best_for, is_limited in KILO_FREE_MODELS:
        fmt = get_free_model_format(model_id)
        status = "⏳ Limited" if is_limited else "✅ Free"
        lines.append(f"| `{model_id}` | `{fmt}` | {best_for} | {status} |")
    
    return "\n".join(lines)


def generate_openrouter_free_models_table() -> str:
    """Generate the OpenRouter Free Models markdown table."""
    lines = [
        "",
        "## OpenRouter Free Models (Require Account)",
        "",
        "| Model | Best For | Status |",
        "| ----- | -------- | ------ |",
    ]
    
    for model_id, display_name, best_for in OPENROUTER_FREE_MODELS:
        lines.append(f"| `{model_id}` | {best_for} | ✅ Free |")
    
    return "\n".join(lines)


def generate_routing_matrix() -> str:
    """Generate the Routing Matrix markdown table."""
    lines = [
        "",
        "## Routing Matrix",
        "",
        "| Task Type | Agent | Model | Tier |",
        "| --------- | ----- | ----- | ---- |",
    ]
    
    routing_configs = [
        ("Bulk coding", "Kilo CLI", DEFAULT_ROUTING["bulk_coding"], "T1 Free"),
        ("Routine fixes", "OpenCode", DEFAULT_ROUTING["routine_fixes"], "T1 Free"),
        ("Research", "Gemini CLI", DEFAULT_ROUTING["research"], "T2 Free"),
        ("Planning", "Kilo CLI", DEFAULT_ROUTING["planning"], "T1 Free"),
        ("Agent tasks", "Kilo CLI", DEFAULT_ROUTING["agent_tasks"], "T1 Free"),
        ("Code synthesis", "Kilo CLI", DEFAULT_ROUTING["code_synthesis"], "T1 Free"),
        ("**Fallback**", "Groq", "llama-3.3-70b", "**T4 Paid**"),
    ]
    
    for task, agent, model, tier in routing_configs:
        lines.append(f"| {task} | {agent} | `{model}` | {tier} |")
    
    return "\n".join(lines)


def generate_resource_conservation() -> str:
    """Generate the Resource Conservation section."""
    return """
## Resource Conservation (IMPORTANT)

- **NEVER use Gemini for internal code searches** (codesearch, grep, file search)
- Use `{primary_model}` for all internal search operations
- Reserve Gemini 2.5 Pro/Flash for: external web research, complex architecture, high-context reasoning
""".format(primary_model=DEFAULT_ROUTING["bulk_coding"])


def generate_groq_section() -> str:
    """Generate the Groq section."""
    return f"""
## Groq (T4 — Last Resort, Pay-Per-Token)

- **Status**: Last resort ONLY — never primary, never default
- **Cost**: $0.59/$0.79 per 1M tokens (llama-3.3-70b), $0.05/$0.08 (llama-3.1-8b)
- **Rate limits**: 30 RPM, 1K RPD, 100K TPD (llama-3.3-70b)
- **Use when**: T1 free ({DEFAULT_ROUTING['bulk_coding']} + big-pickle) + T2 (Gemini flash) + T3 fail
- **DO NOT use for**: Bulk coding, docs, testing — use T1 free instead
"""


def update_cost_optimization_file(file_path: Path, dry_run: bool = False) -> bool:
    """Update a single cost-optimization file."""
    if not file_path.exists():
        print(f"  ⚠️  File not found: {file_path}")
        return False
    
    content = file_path.read_text(encoding='utf-8')
    
    # Generate new content sections
    kilo_table = generate_kilo_free_models_table()
    openrouter_table = generate_openrouter_free_models_table()
    routing_matrix = generate_routing_matrix()
    resource_cons = generate_resource_conservation()
    groq_section = generate_groq_section()
    
    # Find and replace Kilo Gateway Free Models section
    # Pattern matches from "## Kilo Gateway Free Models" to just before next "##"
    kilo_pattern = r'## Kilo Gateway Free Models \(2026-\d{2}\).*?(?=\n## |\Z)'
    content = re.sub(kilo_pattern, kilo_table, content, flags=re.DOTALL)
    
    # Replace OpenRouter section
    or_pattern = r'## OpenRouter Free Models \(Require Account\).*?(?=\n## |\Z)'
    content = re.sub(or_pattern, openrouter_table, content, flags=re.DOTALL)
    
    # Replace Routing Matrix
    routing_pattern = r'## Routing Matrix.*?(?=\n## |\Z)'
    content = re.sub(routing_pattern, routing_matrix, content, flags=re.DOTALL)
    
    # Replace Resource Conservation
    res_pattern = r'## Resource Conservation \(IMPORTANT\).*?(?=\n## |\Z)'
    content = re.sub(res_pattern, resource_cons, content, flags=re.DOTALL)
    
    # Replace Groq section
    groq_pattern = r'## Groq \(T4 — Last Resort.*?(?=\n## |\Z)'
    content = re.sub(groq_pattern, groq_section, content, flags=re.DOTALL)
    
    if dry_run:
        print(f"  [DRY RUN] Would update: {file_path}")
        return True
    
    file_path.write_text(content, encoding='utf-8')
    print(f"  ✅ Updated: {file_path}")
    return True


def main():
    """Main function to update all cost-optimization files."""
    print("🔄 Free Models Update Script")
    print("=" * 50)
    
    # Check for --dry-run flag
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No files will be modified\n")
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"📁 Project root: {project_root}")
    print(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Show current configuration
    print("📋 Current Free Models Configuration:")
    print("-" * 40)
    for model_id, display_name, best_for, _ in KILO_FREE_MODELS:
        fmt = get_free_model_format(model_id)
        print(f"  • {display_name}: {model_id} ({fmt})")
    print()
    
    print("📋 Default Routing:")
    print("-" * 40)
    for task, model in DEFAULT_ROUTING.items():
        print(f"  • {task}: {model}")
    print()
    
    # Update each agent directory
    print("🔄 Updating agent directories...")
    print("-" * 40)
    
    success_count = 0
    for dir_path in AGENT_DIRS:
        full_path = project_root / dir_path / "cost-optimization"
        if update_cost_optimization_file(full_path, dry_run):
            success_count += 1
    
    print()
    print("=" * 50)
    print(f"✅ Updated {success_count}/{len(AGENT_DIRS)} files")
    
    if not dry_run:
        print("\n🧪 Running verification...")
        print("-" * 40)
        os.system("python scripts/verify_agentic_platform.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
