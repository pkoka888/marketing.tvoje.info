# MCP Servers & Services Recovery Plan

**Date**: 2026-02-19 **Status**: Critical - Services Down **Context**: Switched
to Git Bash, MCP servers not functional

---

## Current State Analysis

### What's Broken

1. **Path Format Mismatch**: MCP configs use Windows paths (`C:/...`) but Git
   Bash needs Unix paths (`/c/...`)
2. **Missing CLI Tools**: `kilo` and `cline` commands not in Git Bash PATH
3. **MCP Config Drift**: 4 different configs (.kilocode, .clinerules,
   .antigravity, opencode.json) with inconsistencies
4. **Swarm Orchestration**: Analyst (Flash) and Developer (Kilo) agents failing
   in audit

### Working Components

- Node.js: ✅ v22.22.0 (via nvm4w)
- npm: ✅ 10.9.4
- Python: ✅ 3.13.7
- uvx: ✅ Available
- Redis: ✅ Responding to PING

---

## Recovery Phases

### Phase 1: PATH & Environment Fixes (P0)

**Goal**: Make core tools accessible in Git Bash

#### 1.1 Add Kilo CLI to PATH

```bash
# Add to ~/.bashrc or ~/.bash_profile
export PATH="$PATH:$APPDATA/npm"
export PATH="$PATH:/c/Users/pavel/AppData/Roaming/npm"

# Or create symlinks
ln -sf "/c/Users/pavel/AppData/Roaming/npm/kilo" /usr/local/bin/kilo
ln -sf "/c/Users/pavel/AppData/Roaming/npm/cline" /usr/local/bin/cline
```

#### 1.2 Verify Tool Access

```bash
which kilo && kilo --version
which cline && cline --version
which opencode && opencode --version
```

---

### Phase 2: MCP Configuration Fix (P0)

**Goal**: Standardize MCP configs for Git Bash compatibility

#### 2.1 Path Conversion Strategy

Convert all Windows paths to Git Bash format:

- `C:/nvm4w/nodejs/node_modules` → `/c/nvm4w/nodejs/node_modules`
- `C:/Users/pavel/projects` → `/c/Users/pavel/projects`

#### 2.2 Create Unified MCP Config

Create `mcp-servers.json` in project root (single source of truth):

```json
{
  "mcpServers": {
    "filesystem-projects": {
      "command": "node",
      "args": [
        "/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js",
        "/c/Users/pavel/projects"
      ]
    },
    "filesystem-agentic": {
      "command": "node",
      "args": [
        "/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js",
        "/c/Users/pavel/vscodeportable/agentic"
      ]
    },
    "memory": {
      "command": "node",
      "args": [
        "/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-memory/dist/index.js"
      ]
    },
    "git": {
      "command": "node",
      "args": ["/c/nvm4w/nodejs/node_modules/git-mcp/dist/index.js"]
    },
    "github": {
      "command": "node",
      "args": [
        "/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-github/dist/index.js"
      ],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "redis": {
      "command": "node",
      "args": [
        "/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/redis-server.js"
      ],
      "env": {
        "PROJECT_NAME": "marketing-tvoje-info",
        "REDIS_PASSWORD": "${REDIS_PASSWORD}"
      }
    },
    "bmad-mcp": {
      "command": "node",
      "args": ["/c/nvm4w/nodejs/node_modules/bmad-mcp/dist/index.js"],
      "env": {
        "PROJECT_ROOT": "."
      }
    },
    "firecrawl-local": {
      "command": "node",
      "args": [
        "/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-libs/firecrawl-fresh/node_modules/firecrawl-mcp/dist/index.js"
      ],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    },
    "playwright-mcp": {
      "command": "node",
      "args": ["/c/nvm4w/nodejs/node_modules/@playwright/mcp/cli.js"]
    }
  }
}
```

#### 2.3 Sync Configs to All Agents

Update these files with unified config:

- `.kilocode/mcp.json`
- `.clinerules/mcp.json`
- `.antigravity/mcp.json`
- `opencode.json` (convert from opencode format)

---

### Phase 3: Swarm Orchestration Fix (P1)

**Goal**: Restore parallel agent execution

#### 3.1 Fix Swarm Audit Script

Update `scripts/swarm_audit.py`:

```python
#!/usr/bin/env python3
import concurrent.futures
import os
import subprocess
import sys
import time
from datetime import datetime

# Import agent_tools for Flash
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent_tools import ask_groq

def task_flash(prompt):
    print("🚀 [Swarm] Analyst (Gemini Flash) starting...")
    try:
        # Use groq or other available model instead of flash
        res = ask_groq(prompt, model="llama-3.1-8b")
        return {
            "agent": "Analyst (Groq)",
            "output": res.content if res.success else res.error,
            "success": res.success
        }
    except Exception as e:
        return {
            "agent": "Analyst (Groq)",
            "success": False,
            "error": str(e)
        }

def task_kilo(prompt):
    print("🚀 [Swarm] Developer (Kilo) starting...")
    try:
        # Check if kilo is available
        result = subprocess.run(
            ["kilo", "--version"],
            capture_output=True,
            text=True,
            shell=False  # Important for Git Bash
        )
        return {
            "agent": "Developer (Kilo)",
            "output": result.stdout if result.returncode == 0 else result.stderr,
            "success": result.returncode == 0
        }
    except Exception as e:
        return {
            "agent": "Developer (Kilo)",
            "success": False,
            "error": str(e)
        }

def task_cline(prompt):
    print("🚀 [Swarm] QA (Cline) starting...")
    try:
        result = subprocess.run(
            ["cline", "--version"],
            capture_output=True,
            text=True,
            shell=False
        )
        return {
            "agent": "QA (Cline)",
            "output": "Cline CLI Verified: OK" if result.returncode == 0 else result.stderr,
            "success": result.returncode == 0
        }
    except Exception as e:
        return {
            "agent": "QA (Cline)",
            "success": False,
            "error": str(e)
        }

def main():
    print(f"--- 🐝 Swarm Audit Initiated ({datetime.now().strftime('%H:%M:%S')}) ---")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        f_flash = executor.submit(
            task_flash,
            "Audit MCP configuration for Git Bash compatibility. Focus on path formats."
        )
        f_kilo = executor.submit(task_kilo, "Check Kilo availability")
        f_cline = executor.submit(task_cline, "Verify Cline CLI")

        results = [f.result() for f in [f_flash, f_kilo, f_cline]]

    print("\n--- 🏁 Swarm Audit Results ---")
    report_path = "plans/agent-shared/swarm_audit_report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, "w") as f:
        f.write(f"# Swarm Audit Report - {datetime.now().isoformat()}\n\n")
        for r in results:
            icon = "✅" if r["success"] else "❌"
            print(f"{icon} {r['agent']}")
            f.write(f"## {r['agent']}\n")
            f.write(f"Status: {icon}\n\n")
            f.write(f"### Findings\n{r.get('output', 'No output')}\n\n")

    print(f"\nAudit complete. Detailed report at {report_path}")

if __name__ == "__main__":
    main()
```

#### 3.2 Create Path Helper Script

Create `scripts/fix_gitbash_paths.py`:

```python
#!/usr/bin/env python3
"""
Convert Windows paths to Git Bash format in MCP configs
"""
import json
import re
from pathlib import Path

def convert_path(path):
    """Convert C:/path to /c/path format"""
    match = re.match(r'^([A-Za-z]):(/.*)$', path)
    if match:
        return f"/{match.group(1).lower()}{match.group(2)}"
    return path

def fix_mcp_config(config_path):
    """Fix paths in an MCP config file"""
    with open(config_path, 'r') as f:
        config = json.load(f)

    modified = False

    def fix_recursive(obj):
        nonlocal modified
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str) and ('C:/' in value or 'c:/' in value):
                    obj[key] = convert_path(value)
                    modified = True
                elif isinstance(value, (dict, list)):
                    fix_recursive(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, str) and ('C:/' in item or 'c:/' in item):
                    obj[i] = convert_path(item)
                    modified = True
                elif isinstance(item, (dict, list)):
                    fix_recursive(item)

    fix_recursive(config)

    if modified:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Fixed: {config_path}")
    else:
        print(f"⏭️  No changes: {config_path}")

def main():
    configs = [
        ".kilocode/mcp.json",
        ".clinerules/mcp.json",
        ".antigravity/mcp.json"
    ]

    for config in configs:
        if Path(config).exists():
            fix_mcp_config(config)
        else:
            print(f"❌ Not found: {config}")

if __name__ == "__main__":
    main()
```

---

### Phase 4: Testing & Verification (P1)

#### 4.1 MCP Server Test Script

Create `scripts/test_mcp_servers.py`:

```python
#!/usr/bin/env python3
"""
Test all MCP servers are reachable
"""
import subprocess
import json

def test_mcp_server(name, command, args):
    """Test if an MCP server responds"""
    try:
        result = subprocess.run(
            [command] + args,
            capture_output=True,
            text=True,
            timeout=5
        )
        return {
            "name": name,
            "status": "✅" if result.returncode == 0 else "❌",
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "name": name,
            "status": "❌",
            "error": str(e)
        }

def main():
    with open(".kilocode/mcp.json") as f:
        config = json.load(f)

    print("Testing MCP Servers...")
    print("-" * 50)

    for name, server in config.get("mcpServers", {}).items():
        result = test_mcp_server(
            name,
            server["command"],
            server.get("args", [])
        )
        print(f"{result['status']} {name}")

if __name__ == "__main__":
    main()
```

---

## Quick Recovery Commands

### Immediate Fixes (Run in Git Bash)

```bash
# 1. Fix PATH
echo 'export PATH="$PATH:/c/Users/pavel/AppData/Roaming/npm"' >> ~/.bashrc
echo 'export PATH="$PATH:/c/nvm4w/nodejs"' >> ~/.bashrc
source ~/.bashrc

# 2. Fix MCP paths
python scripts/fix_gitbash_paths.py

# 3. Test tools
which kilo && kilo --version
which cline && cline --version

# 4. Run swarm audit
python scripts/swarm_audit.py

# 5. Test MCP servers
python scripts/test_mcp_servers.py
```

---

## Success Criteria

- [ ] All MCP servers respond without errors
- [ ] `kilo`, `cline`, `opencode` commands available in Git Bash
- [ ] Swarm audit passes for all 3 agents
- [ ] Redis connectivity confirmed
- [ ] Parallel orchestration functional

---

## Next Steps

1. **Run Phase 1**: Fix PATH for Git Bash
2. **Run Phase 2**: Execute path fix script
3. **Run Phase 3**: Test swarm orchestration
4. **Verify**: Run full test suite

Would you like me to implement any of these phases now?
