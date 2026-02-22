#!/usr/bin/env python3
"""
MCP Configuration Discovery Script
Scans entire project for MCP configs and finds duplicates/inconsistencies
"""

import json
import os
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict

PROJECT_ROOT = Path(r"C:\Users\pavel\projects\marketing.tvoje.info")


def find_all_config_files():
    """Find all JSON, YAML, YML config files in project"""
    patterns = [
        "**/*.json",
        "**/*.yaml",
        "**/*.yml",
    ]

    exclude_dirs = {
        "node_modules",
        ".git",
        "dist",
        "build",
        "coverage",
        ".cache",
        ".parcel-cache",
        ".vite",
        "__pycache__",
        "tmp-agentic",
        "temp-everything-claude-code",
        "archive",
        ".astro",
        "src",
        "public",
        "tests",
    }

    configs = []
    for pattern in patterns:
        for f in PROJECT_ROOT.glob(pattern):
            # Skip excluded directories
            if any(exc in f.parts for exc in exclude_dirs):
                continue
            # Skip package.json, tsconfig etc
            if f.name in ["package.json", "tsconfig.json", "jsconfig.json"]:
                continue
            configs.append(f)
    return configs


def is_mcp_config(content: str) -> bool:
    """Check if JSON contains MCP configuration"""
    try:
        data = json.loads(content)
        return "mcp" in str(data).lower() or "mcpServers" in str(data).lower()
    except:
        return False


def parse_mcp_config(filepath: Path) -> dict:
    """Parse MCP config from file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Try JSON first
        try:
            data = json.loads(content)
            if "mcp" in data or "mcpServers" in data:
                return {"format": "json", "data": data}
        except:
            pass

        # Try YAML
        try:
            data = yaml.safe_load(content)
            if data and (
                "mcp" in str(data).lower() or "mcpServers" in str(data).lower()
            ):
                return {"format": "yaml", "data": data}
        except:
            pass

    except Exception as e:
        return {"error": str(e)}

    return None


def extract_mcp_servers(data: dict) -> list:
    """Extract MCP server names from config"""
    servers = []

    # Handle different formats
    mcp_data = data.get("mcp", {}) or data.get("mcpServers", {})

    if isinstance(mcp_data, dict):
        servers = list(mcp_data.keys())
    elif isinstance(mcp_data, list):
        servers = [s.get("name", s) for s in mcp_data if isinstance(s, dict)]

    return servers


def analyze_mcp_config(filepath: Path) -> dict:
    """Analyze single MCP config file"""
    result = {
        "path": str(filepath.relative_to(PROJECT_ROOT)),
        "exists": filepath.exists(),
        "servers": [],
        "hasMemoryMcp": False,
        "hasRedisMcp": False,
        "hasGithubMcp": False,
        "hasFilesystemMcp": False,
    }

    if not filepath.exists():
        return result

    parsed = parse_mcp_config(filepath)
    if parsed and "data" in parsed:
        result["format"] = parsed.get("format", "unknown")
        result["servers"] = extract_mcp_servers(parsed["data"])
        result["hasMemoryMcp"] = "memory" in str(result["servers"]).lower()
        result["hasRedisMcp"] = "redis" in str(result["servers"]).lower()
        result["hasGithubMcp"] = "github" in str(result["servers"]).lower()
        result["hasFilesystemMcp"] = any(
            "filesystem" in s.lower() for s in result["servers"]
        )

    return result


def find_duplicate_configs():
    """Find all MCP config files and analyze them"""
    print("🔍 Scanning for MCP configuration files...")

    # Find all potential config files
    all_configs = find_all_config_files()

    # Filter to actual MCP configs
    mcp_configs = []
    for f in all_configs:
        try:
            content = f.read_text(encoding="utf-8")
            if is_mcp_config(content):
                mcp_configs.append(f)
        except:
            pass

    print(f"📁 Found {len(mcp_configs)} MCP config files")

    # Analyze each
    results = []
    for f in mcp_configs:
        analysis = analyze_mcp_config(f)
        analysis["path"] = str(f.relative_to(PROJECT_ROOT))
        results.append(analysis)

    return results


def compare_configs(results: list) -> dict:
    """Compare MCP configs and find inconsistencies"""

    # Group by agent
    by_agent = defaultdict(list)
    for r in results:
        path = r["path"]
        if ".antigravity" in path:
            by_agent["antigravity"].append(r)
        elif ".kilocode" in path:
            by_agent["kilocode"].append(r)
        elif ".clinerules" in path:
            by_agent["cline"].append(r)
        elif ".agent" in path and "temp" not in path:
            by_agent[".agent"].append(r)
        elif "opencode.json" in path:
            by_agent["opencode"].append(r)
        else:
            by_agent["other"].append(r)

    # Compare servers
    all_servers = defaultdict(list)
    for r in results:
        for server in r["servers"]:
            all_servers[server].append(r["path"])

    return {"by_agent": dict(by_agent), "servers": dict(all_servers)}


def generate_report():
    """Generate comprehensive report"""
    results = find_duplicate_configs()
    comparison = compare_configs(results)

    report = []
    report.append("# MCP Configuration Discovery Report")
    report.append(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Summary
    report.append("## Summary")
    report.append(f"- Total MCP config files found: {len(results)}")
    report.append(
        f"- Unique MCP servers across all configs: {len(comparison['servers'])}\n"
    )

    # By Agent
    report.append("## Configs by Agent")
    for agent, configs in comparison["by_agent"].items():
        report.append(f"\n### {agent.upper()}")
        for c in configs:
            report.append(f"- `{c['path']}`")
            report.append(
                f"  - Servers: {len(c['servers'])} - {', '.join(c['servers'])}"
            )

    # Server Matrix
    report.append("\n## Server Availability Matrix")
    report.append(
        "\n| Server | "
        + " | ".join([a.upper()[:8] for a in comparison["by_agent"].keys()])
        + " |"
    )
    report.append("|" + "---|" * (len(comparison["by_agent"]) + 1))

    for server in sorted(comparison["servers"].keys()):
        row = [server]
        for agent in comparison["by_agent"].keys():
            has_it = any(server in c["servers"] for c in comparison["by_agent"][agent])
            row.append("✅" if has_it else "❌")
        report.append("| " + " | ".join(row) + " |")

    # Issues
    report.append("\n## Issues & Duplications")

    # Find servers with multiple configs
    for server, paths in comparison["servers"].items():
        if len(paths) > 1:
            report.append(f"\n### ⚠️ {server} - Found in {len(paths)} locations:")
            for p in paths:
                report.append(f"  - {p}")

    # Missing in antigravity
    report.append("\n## Recommendations")
    report.append("\n### For .antigravity (SINGLE SOURCE OF TRUTH):")

    # Get all unique servers
    all_unique_servers = set()
    for r in results:
        all_unique_servers.update(r["servers"])

    # Check what's missing in .antigravity
    if ".antigravity" in comparison["by_agent"]:
        anti_servers = set()
        for c in comparison["by_agent"][".antigravity"]:
            anti_servers.update(c["servers"])

        missing = all_unique_servers - anti_servers
        if missing:
            report.append("\nMissing servers to add:")
            for s in sorted(missing):
                report.append(f"- {s}")

    return "\n".join(report)


if __name__ == "__main__":
    print(generate_report())
