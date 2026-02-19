#!/usr/bin/env python3
"""
Template Reference Population Script.

Populates template references based on metadata
relationships. Updates template files with
cross-references and dependencies.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Set

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from template_reference_manager import (  # noqa: E402
    TemplateReferenceManager,
    TemplateReference,
)


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - %(name)s"
        " - %(levelname)s - %(message)s"
    ),
)
logger = logging.getLogger(__name__)


class TemplateReferencePopulator:
    """Handles dynamic population of template refs."""

    def __init__(
        self,
        templates_dir: Path,
        manager: TemplateReferenceManager,
    ):
        self.templates_dir = templates_dir
        self.manager = manager
        self.updated_templates: Set[str] = set()

    def populate_references(self) -> bool:
        """Populate template references dynamically."""
        logger.info(
            "Starting dynamic reference population..."
        )

        try:
            templates = self.manager.scan_templates()
            logger.info(
                f"Loaded {len(templates)} templates"
                " for population"
            )

            graph = self._build_dependency_graph(
                templates
            )

            for tid, tref in templates.items():
                if self._populate_template_references(
                    tid, tref, graph
                ):
                    self.updated_templates.add(tid)

            logger.info(
                "Populated references for"
                f" {len(self.updated_templates)} templates"
            )
            return True

        except Exception as e:
            logger.error(
                f"Failed to populate references: {e}"
            )
            return False

    def _build_dependency_graph(
        self,
        templates: Dict[str, TemplateReference],
    ) -> Dict[str, Set[str]]:
        """Build dependency graph from refs."""
        graph: Dict[str, Set[str]] = {}

        for tid, tref in templates.items():
            graph[tid] = set()

            # Add dependencies from raw metadata
            deps = tref.raw_metadata.get(
                "references", {}
            ).get("dependencies", [])
            for dep in deps:
                dep_stem = Path(dep).stem
                if dep_stem in templates:
                    graph[tid].add(dep_stem)

            # Add reverse deps
            for oid, oref in templates.items():
                if oid != tid:
                    for ref in oref.references:
                        ref_stem = Path(ref).stem
                        if ref_stem == tid:
                            graph[tid].add(oid)

        return graph

    def _populate_template_references(
        self,
        template_id: str,
        template_ref: TemplateReference,
        graph: Dict[str, Set[str]],
    ) -> bool:
        """Populate references for a template."""
        try:
            content = template_ref.template_path.read_text(
                encoding="utf-8"
            )

            section = self._find_reference_section(
                content
            )

            if section:
                updated = self._update_reference_section(
                    content, section,
                    template_id, template_ref, graph,
                )
            else:
                updated = self._add_reference_section(
                    content,
                    template_id, template_ref, graph,
                )

            if updated != content:
                template_ref.template_path.write_text(
                    updated, encoding="utf-8"
                )
                logger.debug(
                    "Updated references in:"
                    f" {template_id}"
                )
                return True

            return False

        except Exception as e:
            logger.error(
                "Failed to populate references"
                f" for {template_id}: {e}"
            )
            return False

    def _find_reference_section(
        self, content: str
    ) -> str:
        """Find reference section in content."""
        lines = content.split("\n")
        in_refs = False
        ref_lines = []

        for line in lines:
            if (
                "## References" in line
                or "## Related Templates" in line
                or "## Related Skills" in line
            ):
                in_refs = True
                ref_lines.append(line)
            elif in_refs and (
                line.startswith("##")
                or line.strip() == ""
            ):
                break
            elif in_refs:
                ref_lines.append(line)

        return "\n".join(ref_lines) if ref_lines else ""

    def _update_reference_section(
        self,
        content: str,
        current_section: str,
        template_id: str,
        template_ref: TemplateReference,
        graph: Dict[str, Set[str]],
    ) -> str:
        """Update reference section."""
        new_refs = self._generate_reference_content(
            template_id, template_ref, graph
        )
        return content.replace(current_section, new_refs)

    def _add_reference_section(
        self,
        content: str,
        template_id: str,
        template_ref: TemplateReference,
        graph: Dict[str, Set[str]],
    ) -> str:
        """Add new reference section to template."""
        ref_content = self._generate_reference_content(
            template_id, template_ref, graph
        )

        lines = content.split("\n")
        insert_idx = len(lines)

        footer_kw = ["notes", "changelog", "version"]
        for i, line in enumerate(lines):
            if line.startswith("## ") and any(
                kw in line.lower() for kw in footer_kw
            ):
                insert_idx = i
                break

        lines.insert(insert_idx, "")
        lines.insert(insert_idx, ref_content)

        return "\n".join(lines)

    def _generate_reference_content(
        self,
        template_id: str,
        template_ref: TemplateReference,
        graph: Dict[str, Set[str]],
    ) -> str:
        """Generate reference content for template."""
        lines = ["## References", ""]

        # Dependencies
        deps = graph.get(template_id, set())
        if deps:
            lines.append("### Dependencies")
            for dep in sorted(deps):
                lines.append(
                    f"- [{dep}]({dep}.md)"
                    " - Referenced template"
                )
            lines.append("")

        # Referenced By
        referrers = set()
        for oid, odeps in graph.items():
            if template_id in odeps:
                referrers.add(oid)

        if referrers:
            lines.append("### Referenced By")
            for ref in sorted(referrers):
                lines.append(
                    f"- [{ref}]({ref}.md)"
                    " - References this template"
                )
            lines.append("")

        # Related by type
        ttype = template_ref.template_type
        if ttype:
            related = []
            mgr = self.manager
            for oid, oref in mgr.templates.items():
                if (
                    oid != template_id
                    and oref.template_type == ttype
                ):
                    related.append(oid)

            if related:
                lines.append(
                    f"### Related {ttype} Templates"
                )
                for rel in sorted(related):
                    lines.append(
                        f"- [{rel}]({rel}.md)"
                        " - Same category"
                    )
                lines.append("")

        return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    try:
        templates_dir = Path("plans/templates")
        manager = TemplateReferenceManager(templates_dir)
        populator = TemplateReferencePopulator(
            templates_dir, manager
        )

        if populator.populate_references():
            logger.info(
                "Template reference population"
                " completed successfully"
            )
            return 0
        else:
            logger.error(
                "Template reference population failed"
            )
            return 1

    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
