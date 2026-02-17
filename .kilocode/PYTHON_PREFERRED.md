# Python Preferred Policy

## Rationale

- Cross-platform compatibility (Windows/Linux)
- Rich library ecosystem (paramiko, psutil, subprocess)
- Type safety with type hints
- Easier maintainability

## Scripts Location

All server management scripts must be in `.kilocode/scripts/server-monitor/` with `.py` extension.

## Allowed

- `.py` files (preferred)
- `.sh` files only if Python equivalent not feasible

## Migration Status

- [x] collect-evidence.sh → collect_evidence.py
- [x] safe-ssh.sh → safe_ssh.py
- [x] safe-scp.sh → safe_scp.py (combined into safe_ssh.py)
- [x] debug-network.sh → debug_network.py

## Dependencies

Required Python packages:

```
paramiko>=2.12.0
psutil>=5.9.0
```

## Installation

```bash
pip install paramiko psutil
```

## Usage

```bash
# Network debug
python .kilocode/scripts/server-monitor/debug_network.py

# Safe SSH execution
python .kilocode/scripts/server-monitor/safe_ssh.py server60 "uptime"

# Collect evidence from all servers
python .kilocode/scripts/server-monitor/collect_evidence.py all

# Collect from specific server
python .kilocode/scripts/server-monitor/collect_evidence.py server62
```
