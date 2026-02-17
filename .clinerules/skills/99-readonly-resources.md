---
description: VSCodePortable read-only access policy — copy-first before modifying
---

# Rule: VSCodePortable Read-Only Access

**ID:** `RULE-VSCP-01`
**Severity:** Critical

## Overview

The `c:\Users\pavel\vscodeportable\` directory contains shared resources, global knowledge, and agentic frameworks that are utilized across multiple projects. To maintain the integrity of these global assets, this directory MUST be treated as **READ-ONLY** by all project-specific agents.

## Requirements

1.  **No Direct Modifications**: Agents shall NOT modify, delete, or create files within `c:\Users\pavel\vscodeportable\` under any circumstances.
2.  **Copy-First Policy**: If a resource (template, script, rule, or knowledge item) from `vscodeportable` is needed for a specific project:
    - **Read** the file from `vscodeportable`.
    - **Copy** the content to the appropriate project-local directory (e.g., `.agents/templates`, `.kilocode/knowledge`, `docs/reference`).
    - **Modify** only the local copy.
3.  **Reference-Only**: When using knowledge items or research findings, reference the source path in `vscodeportable` but do not alter the original document.

## Exceptions

- **Global Index Updates**: Specialized "Librarian" or "Researcher" agents containing specific instructions to update the global index (e.g., `/index-research` workflow) are exempt _only_ for the specific purpose of appending new knowledge.
- **System Maintenance**: Agents explicitly tasked with maintaining the `vscodeportable` infrastructure itself (e.g., "Updating global schema") may modify files, subject to user approval.

## Enforcement

- All file system write tools (`write_to_file`, `replace_file_content`, etc.) should verify the target path does not start with `c:\Users\pavel\vscodeportable\` unless an explicit exception is granted.
