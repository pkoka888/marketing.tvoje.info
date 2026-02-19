#!/usr/bin/env python3
"""
Convert Windows paths to Git Bash format in MCP configs
"""
import json
import re
from pathlib import Path

def convert_path(path):
    """Convert C:/path to /c/path format for Git Bash compatibility"""
    if not isinstance(path, str):
        return path

    # Handle C:/path or c:/path format
    match = re.match(r'^([A-Za-z]):(/.*)$', path)
    if match:
        return f"/{match.group(1).lower()}{match.group(2)}"

    # Handle backslash format (C:\path)
    match = re.match(r'^([A-Za-z]):\\(.*)$', path)
    if match:
        unix_path = match.group(2).replace('\\', '/')
        return f"/{match.group(1).lower()}/{unix_path}"

    return path

def fix_mcp_config(config_path):
    """Fix paths in an MCP config file"""
    config_path = Path(config_path)
    if not config_path.exists():
        print(f"❌ Not found: {config_path}")
        return False

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON error in {config_path}: {e}")
        return False

    modified = False

    def fix_recursive(obj):
        nonlocal modified
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    new_value = convert_path(value)
                    if new_value != value:
                        obj[key] = new_value
                        modified = True
                elif isinstance(value, (dict, list)):
                    fix_recursive(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, str):
                    new_item = convert_path(item)
                    if new_item != item:
                        obj[i] = new_item
                        modified = True
                elif isinstance(item, (dict, list)):
                    fix_recursive(item)

    fix_recursive(config)

    if modified:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Fixed: {config_path}")
        return True
    else:
        print(f"⏭️  No changes needed: {config_path}")
        return True

def main():
    configs = [
        ".kilocode/mcp.json",
        ".clinerules/mcp.json",
        ".antigravity/mcp.json"
    ]

    print("Fixing MCP config paths for Git Bash compatibility...")
    print("-" * 60)

    success_count = 0
    for config in configs:
        if fix_mcp_config(config):
            success_count += 1

    print("-" * 60)
    print(f"Processed {success_count}/{len(configs)} config files")

if __name__ == "__main__":
    main()
