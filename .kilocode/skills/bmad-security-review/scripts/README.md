# Scripts

This directory contains automation scripts for the Security Review skill.

## Contents

- **Security Scanners**: Automated vulnerability scanning scripts
- **Compliance Checkers**: Scripts to verify compliance with standards (OWASP, ASVS, etc.)
- **Report Generators**: Scripts to generate security reports from findings
- **Utility Scripts**: Helper scripts for common security tasks

## Usage

Scripts in this directory are referenced from the main skill files:
- SKILL.md - Skill definition and activation criteria
- CHECKLIST.md - Quality assurance checklist
- REFERENCE.md - Quick-access resources
- WORKFLOW.md - Step-by-step workflow

## Script Types

- **Shell Scripts** (`.sh`) - Bash scripts for Unix/Linux/macOS environments
- **PowerShell Scripts** (`.ps1`) - PowerShell scripts for Windows environments
- **Python Scripts** (`.py`) - Python scripts for cross-platform automation
- **Node.js Scripts** (`.js`) - JavaScript scripts for Node.js environments

## Requirements

Each script should include:
- Shebang line for the appropriate interpreter
- Usage instructions and help text
- Required dependencies and installation steps
- Error handling and logging
- Exit codes for success/failure

## Notes

- Scripts are optional and can be customized per project needs
- Always review scripts before running in production environments
- Keep scripts version-controlled alongside the skill
- Document any environment variables or configuration files required
