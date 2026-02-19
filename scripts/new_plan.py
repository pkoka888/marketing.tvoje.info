#!/usr/bin/env python3
"""
New Plan Creator.

CLI tool to create new plans from templates with proper
variable substitution and metadata generation.

Usage:
    python scripts/new_plan.py --list
    python scripts/new_plan.py --template TASK_PLAN --name "My Feature Plan"
    python scripts/new_plan.py --template AUDIT_REPORT --name "Security Audit" --output plans/
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import the template manager
from template_reference_manager import TemplateReferenceManager


TEMPLATE_VARIABLES = {
    "{{DATE}}": lambda: datetime.now().strftime("%Y-%m-%d"),
    "{{DATETIME}}": lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "{{AGENT_NAME}}": lambda: "Cline",
    "{{VERSION}}": lambda: "1.0.0",
}

# Threshold for keyword matching - below this falls back to TASK_PLAN
KEYWORD_SCORE_THRESHOLD = 2


def load_template_keywords(templates_dir: Path) -> Dict[str, List[str]]:
    """Load activation.keywords from all template metadata JSONs."""
    keywords: Dict[str, List[str]] = {}
    
    if not templates_dir.exists():
        return keywords
    
    for metadata_file in templates_dir.glob("*-metadata.json"):
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Extract template ID from filename (e.g., AUDIT_REPORT-metadata.json -> AUDIT_REPORT)
            template_id = metadata_file.stem.replace("-metadata", "")
            
            # Extract keywords from activation.keywords
            if "activation" in data and "keywords" in data["activation"]:
                kw_list = data["activation"]["keywords"]
                if isinstance(kw_list, list):
                    keywords[template_id] = [k.lower() for k in kw_list if isinstance(k, str)]
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Warning: Could not parse {metadata_file}: {e}")
    
    return keywords


def score_keywords(description: str, keywords: List[str]) -> int:
    """Score a description against keywords using simple word matching."""
    desc_lower = description.lower()
    words = re.findall(r"\b\w+\b", desc_lower)
    
    score = 0
    for keyword in keywords:
        # Exact word match
        if keyword in words:
            score += 1
        # Partial match (keyword contained in word)
        elif any(keyword in word for word in words):
            score += 0.5
    
    return int(score)


def auto_select_template(description: str, templates_dir: Path) -> Tuple[str, Dict[str, int]]:
    """
    Automatically select a template based on keyword matching.
    
    Returns:
        Tuple of (selected_template_id, score_dict)
    """
    keywords = load_template_keywords(templates_dir)
    
    if not keywords:
        print("⚠️  No template keywords found, using TASK_PLAN as fallback")
        return "TASK_PLAN", {}
    
    scores: Dict[str, int] = {}
    for template_id, kw_list in keywords.items():
        scores[template_id] = score_keywords(description, kw_list)
    
    # Sort by score descending
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Show all scores for debugging
    print(f"\n🔍 Keyword matching scores:")
    for template_id, score in sorted_scores:
        print(f"   {template_id}: {score}")
    
    # Get highest scoring template
    if sorted_scores:
        best_template, best_score = sorted_scores[0]
        
        if best_score >= KEYWORD_SCORE_THRESHOLD:
            return best_template, scores
        else:
            print(f"\n⚠️  Best score ({best_score}) below threshold ({KEYWORD_SCORE_THRESHOLD}), using TASK_PLAN fallback")
            return "TASK_PLAN", scores
    
    return "TASK_PLAN", scores


def list_templates(templates_dir: Path) -> None:
    """List all available templates with details."""
    mgr = TemplateReferenceManager(templates_dir)
    mgr.scan_templates()

    print("\n📋 Available Templates:")
    print("-" * 70)

    for tid, tref in sorted(mgr.templates.items()):
        print(f"\n  📄 {tid}")
        print(f"     Type: {tref.template_type}")
        print(f"     Version: {tref.version}")
        print(f"     Description: {tref.description[:60]}...")
        print(f"     Tags: {', '.join(tref.tags[:5])}")
        if tref.preferred_models:
            print(f"     Models: {', '.join(tref.preferred_models[:3])}")


def substitute_variables(content: str, extra_vars: Optional[Dict[str, str]] = None) -> str:
    """Replace template variables with actual values."""
    result = content

    # Built-in variables
    for var, getter in TEMPLATE_VARIABLES.items():
        result = result.replace(var, getter())

    # Extra variables from user
    if extra_vars:
        for key, value in extra_vars.items():
            var_pattern = "{{" + key.upper() + "}}"
            result = result.replace(var_pattern, value)
            # Also handle lowercase
            var_pattern_lower = "{{" + key.lower() + "}}"
            result = result.replace(var_pattern_lower, value)

    return result


def generate_metadata(
    template_id: str,
    template_metadata: dict,
    output_name: str,
    output_path: Path,
) -> dict:
    """Generate metadata for the new plan file."""
    now = datetime.now().strftime("%Y-%m-%d")

    # Deep copy the template metadata
    new_meta = json.loads(json.dumps(template_metadata))

    # Update template section
    if "template" in new_meta:
        new_meta["template"]["name"] = output_name
        new_meta["template"]["path"] = str(output_path)
        new_meta["template"]["updated"] = now

    # Update metadata section
    if "metadata" in new_meta:
        new_meta["metadata"]["last_updated"] = now

    return new_meta


def create_plan(
    templates_dir: Path,
    template_id: str,
    plan_name: str,
    output_dir: Path,
    extra_vars: Optional[Dict[str, str]] = None,
) -> Path:
    """Create a new plan from a template."""
    mgr = TemplateReferenceManager(templates_dir)
    mgr.scan_templates()

    if template_id not in mgr.templates:
        raise ValueError(f"Template not found: {template_id}")

    tref = mgr.templates[template_id]

    # Read template content
    template_content = tref.template_path.read_text(encoding="utf-8")

    # Create safe filename from plan name
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", plan_name)
    safe_name = re.sub(r"_+", "_", safe_name).strip("_")
    output_filename = f"{safe_name}.md"
    output_path = output_dir / output_filename
    metadata_path = output_dir / f"{safe_name}-metadata.json"

    # Substitute variables
    final_content = substitute_variables(template_content, extra_vars)
    final_content = final_content.replace("[Task Name]", plan_name)

    # Generate metadata
    new_metadata = generate_metadata(
        template_id,
        tref.raw_metadata,
        plan_name,
        output_path,
    )

    # Write files
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_content, encoding="utf-8")
    metadata_path.write_text(
        json.dumps(new_metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"\n✅ Created plan: {output_path}")
    print(f"✅ Created metadata: {metadata_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Create new plans from templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  List templates:
    python scripts/new_plan.py --list

  Auto-select template from description:
    python scripts/new_plan.py --auto "audit redis security"
    python scripts/new_plan.py --auto "test QA results"

  Create a task plan:
    python scripts/new_plan.py -t TASK_PLAN -n "Add user authentication"

  Create an audit report:
    python scripts/new_plan.py -t AUDIT_REPORT -n "Security audit" -o plans/reports/

  With custom variables:
    python scripts/new_plan.py -t TASK_PLAN -n "Feature X" -v agent=Kilo
        """,
    )

    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available templates",
    )

    parser.add_argument(
        "--template", "-t",
        type=str,
        help="Template ID to use (e.g., TASK_PLAN, AUDIT_REPORT)",
    )

    parser.add_argument(
        "--name", "-n",
        type=str,
        help="Name for the new plan",
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default="plans",
        help="Output directory (default: plans/)",
    )

    parser.add_argument(
        "--var", "-v",
        action="append",
        metavar="KEY=VALUE",
        help="Custom variables for substitution (can be used multiple times)",
    )

    parser.add_argument(
        "--templates-dir",
        type=str,
        default="plans/templates",
        help="Templates directory (default: plans/templates/)",
    )

    parser.add_argument(
        "--auto", "-a",
        type=str,
        metavar="DESCRIPTION",
        help="Auto-select template based on task description keywords",
    )

    args = parser.parse_args()

    templates_dir = Path(args.templates_dir)
    output_dir = Path(args.output)

    # Handle auto-select mode
    if args.auto:
        print(f"\n🤖 Auto-select mode: {args.auto}")
        selected_template, scores = auto_select_template(args.auto, templates_dir)
        print(f"\n✅ Selected template: {selected_template}")
        
        # If --name not provided, use a default
        if not args.name:
            # Use first few words of description as name
            words = args.auto.split()[:4]
            args.name = " ".join(words).title()
        
        # Use selected template
        args.template = selected_template
    
    if args.list:
        list_templates(templates_dir)
        return 0

    if not args.template:
        print("❌ Error: --template is required when not listing")
        parser.print_help()
        return 1

    if not args.name:
        print("❌ Error: --name is required when creating a plan")
        parser.print_help()
        return 1

    # Parse custom variables
    extra_vars: Dict[str, str] = {}
    if args.var:
        for var_spec in args.var:
            if "=" in var_spec:
                key, value = var_spec.split("=", 1)
                extra_vars[key] = value
            else:
                print(f"⚠️  Invalid variable format: {var_spec} (expected KEY=VALUE)")

    try:
        create_plan(
            templates_dir,
            args.template.upper(),
            args.name,
            output_dir,
            extra_vars,
        )
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())