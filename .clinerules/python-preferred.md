# Python Preferred Rule

**Rule ID**: LANG-PYTHON-001
**Effective Date**: 2026-02-12
**Scope**: All code files created or modified

## Mandate
1. All new automation scripts MUST use Python (.py)
2. Existing shell scripts should be migrated to Python
3. Python 3.10+ required for type hints support

## Exceptions
- System shell commands (npm scripts in package.json)
- CI/CD workflows (GitHub Actions YAML)
- One-liners in documentation
- Git hooks (pre-commit hooks)

## Libraries Required
- `paramiko` - SSH client functionality
- `psutil` - System monitoring
- `subprocess` - Shell command execution ( Checklist
- [stdlib)

## Migrationx] collect-evidence.sh → collect_evidence.py
- [x] safe-ssh.sh → safe_ssh.py  
- [x] debug-network.sh → debug_network.py

## Enforcement
This rule is enforced by:
1. Cline will flag `.sh` files in code reviews
2. Kilo Code will prefer `.py` for new automation tasks
3. Git hooks can validate script language

## Benefits
1. **Cross-platform**: Works on Windows, Linux, macOS
2. **Maintainable**: Type hints, better IDE support
3. **Secure**: Easier to validate commands (no shell injection)
4. **Testable**: Unit testing with pytest
