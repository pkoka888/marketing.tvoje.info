#!/usr/bin/env python3
"""
Template Reference Manager.

Core class for managing template references and
metadata in the plan template system. Loads, validates,
and resolves template references across the project.

Metadata JSON schema (nested):
  template.{name, type, version, description, path,
            author, created, updated}
  activation.{triggers, keywords, context, priority,
              auto_activate}
  models.{preferred, fallback, cost_optimization}
  references.{cross_links, dependencies, related}
  validation.{required_sections, format_checks,
              content_rules}
  metadata.{frameworks, compatibility, usage_count,
            last_used, success_rate, tags}
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TemplateReference:
    """Template reference with raw metadata."""

    template_id: str
    template_path: Path
    metadata_path: Path
    raw_metadata: dict = field(default_factory=dict)
    last_modified: Optional[datetime] = None

    # --- Property accessors into nested JSON ---

    @property
    def version(self) -> str:
        tpl = self.raw_metadata.get("template", {})
        return tpl.get("version", "")

    @property
    def name(self) -> str:
        tpl = self.raw_metadata.get("template", {})
        return tpl.get("name", "")

    @property
    def template_type(self) -> str:
        tpl = self.raw_metadata.get("template", {})
        return tpl.get("type", "")

    @property
    def description(self) -> str:
        tpl = self.raw_metadata.get("template", {})
        return tpl.get("description", "")

    @property
    def author(self) -> str:
        tpl = self.raw_metadata.get("template", {})
        return tpl.get("author", "")

    @property
    def references(self) -> List[str]:
        refs = self.raw_metadata.get("references", {})
        return refs.get("cross_links", [])

    @property
    def dependencies(self) -> List[str]:
        refs = self.raw_metadata.get("references", {})
        return refs.get("dependencies", [])

    @property
    def related(self) -> List[str]:
        refs = self.raw_metadata.get("references", {})
        return refs.get("related", [])

    @property
    def tags(self) -> List[str]:
        meta = self.raw_metadata.get("metadata", {})
        return meta.get("tags", [])

    @property
    def triggers(self) -> List[str]:
        act = self.raw_metadata.get("activation", {})
        return act.get("triggers", [])

    @property
    def keywords(self) -> List[str]:
        act = self.raw_metadata.get("activation", {})
        return act.get("keywords", [])

    @property
    def preferred_models(self) -> List[str]:
        mdl = self.raw_metadata.get("models", {})
        return mdl.get("preferred", [])

    @property
    def required_sections(self) -> List[str]:
        val = self.raw_metadata.get("validation", {})
        return val.get("required_sections", [])


class TemplateReferenceManager:
    """
    Manages template references and metadata.

    Loads template metadata from nested JSON, resolves
    references, validates integrity, tracks dependencies,
    and updates reference metadata.
    """

    def __init__(
        self,
        templates_dir: Path,
        metadata_suffix: str = "-metadata.json",
    ):
        self.templates_dir = Path(templates_dir)
        self.metadata_suffix = metadata_suffix
        self.templates: Dict[str, TemplateReference] = {}

        if not self.templates_dir.exists():
            raise ValueError(
                "Templates directory does not exist:"
                f" {self.templates_dir}"
            )

        logger.info(
            "Initialized TemplateReferenceManager"
            f" for {self.templates_dir}"
        )

    def scan_templates(
        self,
    ) -> Dict[str, TemplateReference]:
        """Scan templates dir, build references."""
        logger.info("Scanning templates directory...")

        for tf in self.templates_dir.glob("*.md"):
            tid = tf.stem
            mf = tf.parent / f"{tid}{self.metadata_suffix}"

            if mf.exists():
                try:
                    tref = self._load_template_reference(
                        tid, tf, mf
                    )
                    self.templates[tid] = tref
                    logger.debug(f"Loaded template: {tid}")
                except Exception as e:
                    logger.error(
                        f"Failed to load template {tid}: {e}"
                    )
            else:
                logger.warning(
                    "No metadata file for template:"
                    f" {tid}"
                )

        logger.info(
            f"Scanned {len(self.templates)} templates"
        )
        return self.templates

    def _load_template_reference(
        self,
        template_id: str,
        template_path: Path,
        metadata_path: Path,
    ) -> TemplateReference:
        """Load a single template reference."""
        with open(metadata_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        stat = template_path.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime)

        return TemplateReference(
            template_id=template_id,
            template_path=template_path,
            metadata_path=metadata_path,
            raw_metadata=raw,
            last_modified=mtime,
        )

    def resolve_references(
        self,
        template_id: str,
        visited: Optional[Set[str]] = None,
    ) -> List[str]:
        """Resolve all refs including transitive deps."""
        if visited is None:
            visited = set()

        if template_id in visited:
            raise ValueError(
                "Circular reference detected"
                f" involving: {template_id}"
            )

        visited.add(template_id)

        if template_id not in self.templates:
            raise ValueError(
                f"Template not found: {template_id}"
            )

        template = self.templates[template_id]
        resolved = list(template.references)

        for dep in template.dependencies:
            # Deps are file paths — check if stem is
            # a known template ID
            dep_id = Path(dep).stem
            if dep_id in self.templates:
                resolved.extend(
                    self.resolve_references(
                        dep_id, visited.copy()
                    )
                )

        # Deduplicate preserving order
        seen: Set[str] = set()
        return [
            r for r in resolved
            if not (r in seen or seen.add(r))
        ]

    def validate_references(
        self,
    ) -> Dict[str, List[str]]:
        """Validate all template references."""
        logger.info("Validating template references...")
        errors: Dict[str, List[str]] = {}

        for tid, tref in self.templates.items():
            errs = []

            # Check cross_links point to known templates
            for ref in tref.references:
                ref_stem = Path(ref).stem
                if ref_stem not in self.templates:
                    errs.append(
                        f"Missing referenced template: {ref}"
                    )

            # Check for circular references
            try:
                self.resolve_references(tid)
            except ValueError as e:
                errs.append(str(e))

            if errs:
                errors[tid] = errs

        logger.info(
            "Validation complete."
            f" Errors in {len(errors)} templates"
        )
        return errors

    def get_template_chain(
        self, template_id: str
    ) -> List[str]:
        """Get complete dependency chain."""
        resolved = self.resolve_references(template_id)
        chain = [template_id] + resolved
        seen: Set[str] = set()
        return [
            item for item in chain
            if not (item in seen or seen.add(item))
        ]

    def update_metadata(
        self,
        template_id: str,
        updates: Dict[str, Any],
    ) -> bool:
        """Update metadata (merges into raw JSON)."""
        if template_id not in self.templates:
            logger.error(
                f"Template not found: {template_id}"
            )
            return False

        template = self.templates[template_id]

        try:
            with open(
                template.metadata_path, "r",
                encoding="utf-8",
            ) as f:
                raw = json.load(f)

            _deep_merge(raw, updates)
            tpl = raw.setdefault("template", {})
            tpl["updated"] = datetime.now().strftime(
                "%Y-%m-%d"
            )

            with open(
                template.metadata_path, "w",
                encoding="utf-8",
            ) as f:
                json.dump(
                    raw, f, indent=2,
                    ensure_ascii=False,
                )
                f.write("\n")

            template.raw_metadata = raw
            template.last_modified = datetime.now()

            logger.info(
                f"Updated metadata for: {template_id}"
            )
            return True

        except Exception as e:
            logger.error(
                "Failed to update metadata"
                f" for {template_id}: {e}"
            )
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get template system statistics."""
        total = len(self.templates)
        total_refs = sum(
            len(t.references)
            for t in self.templates.values()
        )
        total_deps = sum(
            len(t.dependencies)
            for t in self.templates.values()
        )

        ref_counts: Dict[str, int] = {}
        for t in self.templates.values():
            for ref in t.references:
                cnt = ref_counts.get(ref, 0)
                ref_counts[ref] = cnt + 1

        most_ref = sorted(
            ref_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:5]

        avg = total_refs / total if total > 0 else 0
        return {
            "total_templates": total,
            "total_references": total_refs,
            "total_dependencies": total_deps,
            "avg_references_per_template": avg,
            "most_referenced_templates": most_ref,
        }


def _deep_merge(base: dict, updates: dict) -> None:
    """Recursively merge updates into base dict."""
    for key, value in updates.items():
        if (
            key in base
            and isinstance(base[key], dict)
            and isinstance(value, dict)
        ):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def main():
    """CLI: scan and print template summary."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Template Reference Manager"
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Scan and list all templates",
    )
    parser.add_argument(
        "--validate", action="store_true",
        help="Validate all references",
    )
    parser.add_argument(
        "--stats", action="store_true",
        help="Print statistics",
    )
    parser.add_argument(
        "--dir",
        default="plans/templates",
        help="Templates directory",
    )
    args = parser.parse_args()

    mgr = TemplateReferenceManager(Path(args.dir))
    mgr.scan_templates()

    if args.validate:
        errors = mgr.validate_references()
        if errors:
            for tid, errs in errors.items():
                for e in errs:
                    print(f"  ERROR [{tid}]: {e}")
            return 1
        print("All references valid.")
        return 0

    if args.stats:
        stats = mgr.get_statistics()
        for k, v in stats.items():
            print(f"  {k}: {v}")
        return 0

    # Default: scan and print summary
    for tid, tref in mgr.templates.items():
        tags = ",".join(tref.tags[:3])
        print(
            f"  {tid:25s} v{tref.version:8s}"
            f" refs={len(tref.references)}"
            f" deps={len(tref.dependencies)}"
            f" tags={tags}"
        )
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
