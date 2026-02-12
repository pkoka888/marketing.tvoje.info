# Agent Python Script Policy

**Enforced By**: All agents (Kilo Code, Cline, Antigravity, OpenCode)

## Rule
Every agent MUST prefer Python over shell scripts for:
- Server automation
- Evidence collection
- System monitoring
- Configuration management

## File Structure
```
.kilocode/scripts/server-monitor/
├── collect_evidence.py    # Main evidence collection
├── safe_ssh.py            # SSH wrapper with validation
└── debug_network.py       # Network debugging
```

## Validation
Before creating any `.sh` file, agent must:
1. Check if Python equivalent exists in `.kilocode/scripts/server-monitor/`
2. Document reason if shell script is required
3. Add to migration backlog in PYTHON_PREFERRED.md

## Implementation Standards

### Type Hints Required
All Python scripts must use type hints:
```python
def collect_server_evidence(server: str, output_dir: str) -> bool:
    ...
```

### Error Handling
- Use try/except for SSH connections
- Return exit codes (0=success, 1=error)
- Log errors to appropriate log files

### Documentation
- Docstrings for all functions
- Example usage in module docstring
- Argument parsing with argparse

## Allowed Shell Scripts
- `.sh` files in `/bin/` or `/usr/bin/` (system scripts)
- CI/CD workflows (YAML files)
- Package.json scripts (npm lifecycle scripts)
