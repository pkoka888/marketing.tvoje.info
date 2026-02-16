#!/usr/bin/env python3
"""
Weekly Agent Consistency Checker

Runs weekly to verify:
1. Rule synchronization across directories
2. API key pattern detection in .env
3. Health check configuration alignment
4. MCP server availability

Schedule: Every Sunday at 18:00 or on-demand
Output: plans/agent-consistency-check.md
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration - resolve from script location
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # workflows -> agent -> project root
RULES_DIRS = [
    PROJECT_ROOT / ".kilocode" / "rules-code",
    PROJECT_ROOT / ".agents" / "rules",
    PROJECT_ROOT / ".gemini" / "rules",
]
CRITICAL_RULES = [
    "server-preservation",
    "python-preferred",
    "bmad-integration",
    "cost-optimization",
]
REPORT_PATH = PROJECT_ROOT / ".agent" / "plans" / "agent-consistency-check.md"


def log(msg: str) -> None:
    """Print with timestamp."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def check_rules_consistency() -> dict:
    """Check if critical rules exist in all directories."""
    results = {"status": "pass", "issues": [], "details": {}}

    for rule in CRITICAL_RULES:
        locations = {}
        for rules_dir in RULES_DIRS:
            if not rules_dir.exists():
                locations[str(rules_dir)] = "DIR_MISSING"
                continue

            # Check for rule file
            found = False
            for ext in [".md", ".yaml", ".yml"]:
                rule_file = rules_dir / f"{rule}{ext}"
                if rule_file.exists():
                    locations[str(rules_dir)] = "EXISTS"
                    found = True
                    break

            if not found:
                locations[str(rules_dir)] = "MISSING"

        results["details"][rule] = locations

        # Check if all locations exist
        missing = [loc for loc in locations.values() if loc == "MISSING"]
        if missing:
            results["status"] = "fail"
            results["issues"].append(f"Rule '{rule}' missing in: {', '.join(missing)}")

    return results


def check_api_keys() -> dict:
    """Check for exposed API keys in .env files."""
    results = {"status": "pass", "issues": [], "keys_found": []}

    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        results["status"] = "warn"
        results["issues"].append(".env file not found")
        return results

    # Read .env content
    content = env_file.read_text(encoding="utf-8")

    # Patterns for API keys (updated regex)
    patterns = [
        (r"sk-[a-zA-Z0-9]+", "OpenAI"),
        (r"gsk_[a-zA-Z0-9]+", "GROQ"),
        (r"fc-[a-zA-Z0-9]+", "Firecrawl"),
        (r"xoxb-[a-zA-Z0-9-]+", "Slack Bot"),
        (r"ghp_[a-zA-Z0-9]+", "GitHub"),
        (r"nvapi-[a-zA-Z0-9_-]+", "NVIDIA"),
    ]

    for pattern, provider in patterns:
        matches = re.findall(pattern, content)
        if matches:
            for match in matches:
                masked = match[:8] + "***" if len(match) > 8 else "***"
                results["keys_found"].append(
                    {"provider": provider, "masked": masked, "location": ".env"}
                )

    if results["keys_found"]:
        results["status"] = "warn"
        results["issues"].append(
            f"Found {len(results['keys_found'])} API keys in .env (should be in GH Secrets)"
        )

    return results


def check_health_checks() -> dict:
    """Check health-checks.yaml alignment."""
    results = {"status": "pass", "issues": [], "checks_found": 0}

    health_file = PROJECT_ROOT / ".agent" / "health-checks.yaml"
    if not health_file.exists():
        results["status"] = "warn"
        results["issues"].append("health-checks.yaml not found")
        return results

    content = health_file.read_text(encoding="utf-8")

    # Count checks
    check_count = len(re.findall(r"^\s+-\s+name:", content, re.MULTILINE))
    results["checks_found"] = check_count

    # Check for critical checks
    critical_checks = ["Redis Running", "Build Success", "No Secrets in .env"]
    for check in critical_checks:
        if check not in content:
            results["issues"].append(f"Missing critical check: {check}")
            results["status"] = "fail"

    # Check regex patterns
    if "gsk_" not in content and "fc-" not in content:
        results["issues"].append(
            "API key detection regex may be outdated (missing gsk_, fc- patterns)"
        )
        results["status"] = "fail"

    return results


def check_mcp_servers() -> dict:
    """Check MCP server configuration."""
    results = {"status": "pass", "issues": [], "servers": []}

    mcp_file = PROJECT_ROOT / ".kilocode" / "mcp.json"
    if not mcp_file.exists():
        results["status"] = "warn"
        results["issues"].append("mcp.json not found")
        return results

    try:
        mcp_config = json.loads(mcp_file.read_text(encoding="utf-8"))
        servers = mcp_config.get("mcpServers", {})
        results["servers"] = list(servers.keys())

        # Check Redis configuration
        if "redis" in servers:
            redis_config = servers["redis"]
            if "env" not in redis_config:
                results["issues"].append("Redis MCP missing env configuration")
                results["status"] = "fail"

    except json.JSONDecodeError as e:
        results["status"] = "fail"
        results["issues"].append(f"Invalid mcp.json: {e}")

    return results


def generate_report(checks: dict) -> str:
    """Generate markdown report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""# Agent Consistency Check Report

**Generated**: {timestamp}
**Status**: {checks.get("overall_status", "unknown").upper()}

---

## Summary

| Check | Status | Issues |
|-------|--------|--------|
| Rules Consistency | {checks["rules"]["status"].upper()} | {len(checks["rules"]["issues"])} |
| API Keys | {checks["api_keys"]["status"].upper()} | {len(checks["api_keys"]["issues"])} |
| Health Checks | {checks["health_checks"]["status"].upper()} | {len(checks["health_checks"]["issues"])} |
| MCP Servers | {checks["mcp_servers"]["status"].upper()} | {len(checks["mcp_servers"]["issues"])} |

---

## Rules Consistency

### Status: {checks["rules"]["status"].upper()}

"""

    if checks["rules"]["issues"]:
        for issue in checks["rules"]["issues"]:
            report += f"- ❌ {issue}\n"
    else:
        report += "- ✅ All critical rules present in all directories\n"

    report += f"""
### Details

| Rule | {RULES_DIRS[0].name} | {RULES_DIRS[1].name} | {RULES_DIRS[2].name} |
|------|------|------|------|
"""

    for rule, locations in checks["rules"]["details"].items():
        row = f"| {rule} |"
        for d in RULES_DIRS:
            status = locations.get(str(d), "N/A")
            icon = "✅" if status == "EXISTS" else "❌" if status == "MISSING" else "⚠️"
            row += f" {icon} {status} |"
        report += row + "\n"

    report += f"""

## API Keys Check

### Status: {checks["api_keys"]["status"].upper()}

"""

    if checks["api_keys"]["issues"]:
        for issue in checks["api_keys"]["issues"]:
            report += f"- ⚠️ {issue}\n"

    if checks["api_keys"]["keys_found"]:
        report += "\n### Keys Found in .env\n\n"
        report += "| Provider | Masked Key | Location |\n|----------|------------|----------|\n"
        for key in checks["api_keys"]["keys_found"]:
            report += f"| {key['provider']} | `{key['masked']}` | {key['location']} |\n"

        report += "\n**Recommendation**: Move these keys to GitHub Secrets and reference via environment variables.\n"

    report += f"""

## Health Checks

### Status: {checks["health_checks"]["status"].upper()}

- Total checks: {checks["health_checks"]["checks_found"]}

"""

    if checks["health_checks"]["issues"]:
        for issue in checks["health_checks"]["issues"]:
            report += f"- ❌ {issue}\n"

    report += f"""

## MCP Servers

### Status: {checks["mcp_servers"]["status"].upper()}

- Configured servers: {len(checks["mcp_servers"]["servers"])}

"""

    if checks["mcp_servers"]["servers"]:
        for server in checks["mcp_servers"]["servers"]:
            report += f"- ✅ {server}\n"

    if checks["mcp_servers"]["issues"]:
        for issue in checks["mcp_servers"]["issues"]:
            report += f"- ❌ {issue}\n"

    report += f"""

---

## Action Items

"""

    all_issues = (
        checks["rules"]["issues"]
        + checks["api_keys"]["issues"]
        + checks["health_checks"]["issues"]
        + checks["mcp_servers"]["issues"]
    )

    if all_issues:
        for i, issue in enumerate(all_issues, 1):
            report += f"{i}. {issue}\n"
    else:
        report += "No issues found. System is consistent.\n"

    report += f"""

---

## Next Check

Scheduled: Next Sunday at 18:00

To run manually:
```bash
python .agent/workflows/weekly-consistency.py
```
"""

    return report


def main():
    """Main execution."""
    log("Starting weekly consistency check...")

    # Run all checks
    checks = {
        "rules": check_rules_consistency(),
        "api_keys": check_api_keys(),
        "health_checks": check_health_checks(),
        "mcp_servers": check_mcp_servers(),
    }

    # Determine overall status
    statuses = [
        checks["rules"]["status"],
        checks["api_keys"]["status"],
        checks["health_checks"]["status"],
        checks["mcp_servers"]["status"],
    ]

    if "fail" in statuses:
        checks["overall_status"] = "fail"
    elif "warn" in statuses:
        checks["overall_status"] = "warn"
    else:
        checks["overall_status"] = "pass"

    # Generate and save report
    report = generate_report(checks)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")

    log(f"Report saved to: {REPORT_PATH}")
    log(f"Overall status: {checks['overall_status'].upper()}")

    # Print summary
    for check_name, result in checks.items():
        if isinstance(result, dict) and result.get("issues"):
            log(f"{check_name}: {len(result['issues'])} issues")

    # Return exit code
    return 0 if checks["overall_status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
