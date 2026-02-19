#!/usr/bin/env python3
"""
Template Reference Validation Script.

Validates template references for integrity and
consistency. Checks for missing references, circular
dependencies, and metadata consistency.
"""

import sys
import json
import re
import logging
import argparse
from pathlib import Path
from typing import Dict, List

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from template_reference_manager import (  # noqa: E402
    TemplateReferenceManager,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class TemplateValidator:
    """Validates template references and metadata."""

    def __init__(self, templates_dir: Path):
        self.templates_dir = Path(templates_dir)
        self.manager = TemplateReferenceManager(
            templates_dir
        )
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> bool:
        """Run all validation checks."""
        logger.info(
            "Starting comprehensive"
            " template validation..."
        )

        try:
            templates = self.manager.scan_templates()
            logger.info(
                f"Loaded {len(templates)} templates"
            )
        except Exception as e:
            self.errors.append(
                f"Failed to load templates: {e}"
            )
            return False

        self._validate_template_files()
        self._validate_metadata_files()
        self._validate_references(templates)
        self._validate_dependencies(templates)
        self._validate_circular_deps(templates)
        self._validate_metadata_consistency(templates)

        self._report_results()
        return len(self.errors) == 0

    def _validate_template_files(self) -> None:
        """Validate template files exist and read."""
        logger.info("Validating template files...")

        for tf in self.templates_dir.glob("*.md"):
            if not tf.is_file():
                self.errors.append(
                    f"Template not found: {tf}"
                )
                continue
            try:
                content = tf.read_text(encoding="utf-8")
                if not content.strip():
                    self.warnings.append(
                        f"Empty template: {tf}"
                    )
            except Exception as e:
                self.errors.append(
                    f"Cannot read {tf}: {e}"
                )

    def _validate_metadata_files(self) -> None:
        """Validate metadata files are valid JSON."""
        logger.info("Validating metadata files...")

        for tf in self.templates_dir.glob("*.md"):
            mf = tf.parent / (
                tf.stem + "-metadata.json"
            )

            if not mf.exists():
                self.warnings.append(
                    f"No metadata for: {tf.stem}"
                )
                continue

            try:
                raw = json.loads(
                    mf.read_text(encoding="utf-8")
                )

                # Validate nested structure
                if "template" not in raw:
                    self.errors.append(
                        f"Missing 'template' section"
                        f" in {mf.name}"
                    )
                else:
                    tpl = raw["template"]
                    for fld in [
                        "name", "version", "type",
                    ]:
                        if fld not in tpl:
                            self.errors.append(
                                f"Missing template."
                                f"{fld} in {mf.name}"
                            )

                if "references" not in raw:
                    self.warnings.append(
                        f"No references section"
                        f" in {mf.name}"
                    )

                if "validation" not in raw:
                    self.warnings.append(
                        f"No validation section"
                        f" in {mf.name}"
                    )

            except json.JSONDecodeError as e:
                self.errors.append(
                    f"Invalid JSON in {mf.name}: {e}"
                )
            except Exception as e:
                self.errors.append(
                    f"Cannot read {mf.name}: {e}"
                )

    def _validate_references(
        self, templates: Dict
    ) -> None:
        """Validate all cross_links exist."""
        logger.info("Validating template references...")

        for tid, tref in templates.items():
            for ref in tref.references:
                ref_stem = Path(ref).stem
                if ref_stem not in templates:
                    self.errors.append(
                        f"'{tid}' references"
                        f" non-existent '{ref}'"
                    )

    def _validate_dependencies(
        self, templates: Dict
    ) -> None:
        """Validate dependency paths exist."""
        logger.info("Validating dependencies...")

        for tid, tref in templates.items():
            for dep in tref.dependencies:
                dep_path = Path(dep)
                if not dep_path.exists():
                    self.warnings.append(
                        f"'{tid}' depends on"
                        f" missing path: {dep}"
                    )

    def _validate_circular_deps(
        self, templates: Dict
    ) -> None:
        """Validate no circular dependencies."""
        logger.info("Checking circular deps...")

        for tid in templates:
            try:
                self.manager.resolve_references(tid)
            except ValueError as e:
                self.errors.append(
                    f"Circular dep: {e}"
                )

    def _validate_metadata_consistency(
        self, templates: Dict
    ) -> None:
        """Validate metadata consistency."""
        logger.info("Validating metadata consistency...")

        seen_ids = set()
        ver_pat = re.compile(r"^\d+\.\d+\.\d+$")

        for tid, tref in templates.items():
            if tid in seen_ids:
                self.errors.append(
                    f"Duplicate template ID: {tid}"
                )
            seen_ids.add(tid)

            v = tref.version
            if v and not ver_pat.match(v):
                self.warnings.append(
                    f"Non-standard version for"
                    f" '{tid}': {v}"
                )

    def _report_results(self) -> None:
        """Report validation results."""
        logger.info("Validation complete")

        if self.errors:
            logger.error(
                f"Found {len(self.errors)} errors:"
            )
            for error in self.errors:
                logger.error(f"  - {error}")
        else:
            logger.info("No errors found")

        if self.warnings:
            logger.warning(
                f"Found {len(self.warnings)} warnings:"
            )
            for warning in self.warnings:
                logger.warning(f"  - {warning}")
        else:
            logger.info("No warnings found")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate template references"
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=Path("plans/templates"),
        help="Templates directory",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.templates_dir.exists():
        logger.error(
            "Templates dir does not exist:"
            f" {args.templates_dir}"
        )
        return 1

    if not args.templates_dir.is_dir():
        logger.error(
            "Not a directory:"
            f" {args.templates_dir}"
        )
        return 1

    validator = TemplateValidator(args.templates_dir)
    success = validator.validate_all()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
