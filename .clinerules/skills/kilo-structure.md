---
description: Mandatory Kilo Code directory hierarchy and canonical rule store enforcement
---

# Kilo Code Structural Integrity Rules

This project follows the official Kilo Code and Cline structural standards for agentic engineering.

## 1. Directory Hierarchy
Strict adherence to the following directory structure is MANDATORY:

- **`.kilocode/skills/`**: Atomic markdown files (`SKILL.md`) for capabilities.
- **`.kilocode/workflows/`**: Markdown files for repeatable processes.
- **`.kilocode/agents/`**: JSON definitions for Kilo CLI agents.
- **`.kilocode/knowledge/`**: Curated project knowledge.
- **`.kilocodemodes`**: Root-level YAML for extension custom modes.

## 2. Capability Definition (Skills)
- When adding new capabilities, create a new subdirectory in `.kilocode/skills/[skill-name]/`.
- Every skill MUST contain a `SKILL.md` file.
- Use atomic, descriptive names for skills.

## 3. Process Definition (Workflows)
- Repeatable task sequences should be defined in `.kilocode/workflows/[workflow-name].md`.
- Use the slash-command format for workflow identifiers.

## 4. Mode Configuration
- All new modes MUST be registered in `.kilocodemodes`.
- Modes MUST follow the official YAML format including `slug`, `name`, `model`, `groups`, and `customInstructions`.

## 5. Coding Standards
- **Tailwind CSS**: Use Tailwind classes for all UI work.
- **VSCode Theme**: Use `--vscode-*` variables for semantic coloring.
- **Error Handling**: Never use empty catch blocks. Always log or propagate errors.
- **Test-Driven**: Ensure test coverage for all code changes. Run tests from the appropriate package directory.

## 6. Verification
- Before completing a task, verify structural compliance.
- Run `python scripts/validate_kilo_configs.py` after editing configurations.
