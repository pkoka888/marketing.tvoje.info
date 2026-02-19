#!/usr/bin/env python3
"""
Template Index — cross-reference table.

Reads all template metadata JSON files and scans
.kilocode/skills/, .kilocode/rules/, and
.kilocode/workflows/ to build a cross-reference table.

Usage:
    python scripts/template_index.py
    python scripts/template_index.py --json

Exit codes: 0 = clean, 1 = broken references found
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from template_reference_manager import (  # noqa: E402
    TemplateReferenceManager,
)

ROOT = Path(__file__).resolve().parent.parent


def collect_assets():
    """Collect all skills, rules, workflows."""
    skills = set()
    sk_dir = ROOT / ".kilocode" / "skills"
    if sk_dir.exists():
        for d in sk_dir.iterdir():
            if d.is_dir():
                skills.add(d.name)

    rules = set()
    ru_dir = ROOT / ".kilocode" / "rules"
    if ru_dir.exists():
        for f in ru_dir.iterdir():
            if f.is_file() and not f.suffix:
                rules.add(f.name)
            elif f.is_file() and f.suffix == ".md":
                rules.add(f.stem)

    workflows = set()
    wf_dir = ROOT / ".kilocode" / "workflows"
    if wf_dir.exists():
        for f in wf_dir.glob("*.md"):
            if f.name != "README.md":
                workflows.add(f.stem)

    return skills, rules, workflows


def build_index(mgr):
    """Build cross-reference index."""
    skills, rules, workflows = collect_assets()
    index = []
    broken = []

    for tid, tref in mgr.templates.items():
        refs = tref.raw_metadata.get(
            "references", {}
        )

        # Skills linked from metadata
        linked_skills = refs.get("skills", [])
        # Rules linked from metadata
        linked_rules = refs.get("rules", [])
        # Workflows linked from metadata
        linked_workflows = refs.get(
            "workflows", []
        )

        # Validate links
        for s in linked_skills:
            if s not in skills:
                broken.append(
                    f"{tid}: skill '{s}' not found"
                )
        for r in linked_rules:
            if r not in rules:
                broken.append(
                    f"{tid}: rule '{r}' not found"
                )
        for w in linked_workflows:
            if w not in workflows:
                broken.append(
                    f"{tid}: workflow '{w}'"
                    " not found"
                )

        index.append({
            "template": tid,
            "type": tref.template_type,
            "version": tref.version,
            "skills": linked_skills,
            "rules": linked_rules,
            "workflows": linked_workflows,
            "cross_links": len(tref.references),
            "dependencies": len(tref.dependencies),
            "tags": tref.tags,
        })

    return index, broken, skills, rules, workflows


def print_table(index, broken):
    """Print formatted cross-reference table."""
    hdr = (
        f"{'Template':25s} {'Skills':30s}"
        f" {'Rules':25s} {'Workflows':20s}"
    )
    print(hdr)
    print("-" * len(hdr))

    for row in index:
        sk = ", ".join(row["skills"][:3]) or "-"
        ru = ", ".join(row["rules"][:3]) or "-"
        wf = ", ".join(row["workflows"][:2]) or "-"
        print(
            f"{row['template']:25s} {sk:30s}"
            f" {ru:25s} {wf:20s}"
        )

    print()
    if broken:
        print(f"BROKEN REFERENCES ({len(broken)}):")
        for b in broken:
            print(f"  [X] {b}")
    else:
        print("No broken references.")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Template cross-reference index"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output as JSON",
    )
    parser.add_argument(
        "--dir", default="plans/templates",
        help="Templates directory",
    )
    args = parser.parse_args()

    tdir = Path(args.dir)
    mgr = TemplateReferenceManager(tdir)
    mgr.scan_templates()

    idx, broken, sk, ru, wf = build_index(mgr)

    if args.json:
        out = {
            "index": idx,
            "broken": broken,
            "available_skills": sorted(sk),
            "available_rules": sorted(ru),
            "available_workflows": sorted(wf),
        }
        print(json.dumps(out, indent=2))
    else:
        print(
            f"Assets: {len(sk)} skills,"
            f" {len(ru)} rules,"
            f" {len(wf)} workflows\n"
        )
        print_table(idx, broken)

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
