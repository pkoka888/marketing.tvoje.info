#!/usr/bin/env python3
"""
DevOps Version Checker
Run at IDE startup or manually: python scripts/check-versions.py

Checks all CLI tools, detects version mismatches between local, .nvmrc, CI, and package.json.
Exit code 0 = all OK, 1 = warnings found.
"""

import json
import subprocess
import sys
import re
from pathlib import Path

# Expected versions / minimums
EXPECTED = {
    "node": {"min": "22.0.0", "nvmrc": True},
    "npm": {"min": "10.0.0"},
    "git": {"min": "2.40.0"},
    "python": {"min": "3.10.0"},
    "docker": {"min": "24.0.0"},
    "cline": {"present": True},
    "opencode": {"present": True},
    "pre-commit": {"cmd": ["python", "-m", "pre_commit", "--version"], "present": True},
}

warnings = []
info = []


def get_version(cmd: list[str], pattern: str = r"[\d]+\.[\d]+\.[\d]+") -> str | None:
    """Run a command and extract version string."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        output = result.stdout.strip() + result.stderr.strip()
        match = re.search(pattern, output)
        if match:
            ver = match.group(0).lstrip("v")
            return ver
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def parse_version(v: str) -> tuple[int, ...]:
    """Parse version string to tuple for comparison."""
    return tuple(int(x) for x in v.split(".")[:3])


def check_nvmrc():
    """Check if .nvmrc exists and node version matches."""
    nvmrc = Path(".nvmrc")
    if not nvmrc.exists():
        warnings.append("⚠️  .nvmrc not found — create one for consistent Node versions")
        return None
    expected = nvmrc.read_text().strip().lstrip("v")
    return expected


def check_ci_node_version():
    """Check CI workflow Node version matches local."""
    ci_files = list(Path(".github/workflows").glob("*.yml"))
    versions_found = set()
    for f in ci_files:
        content = f.read_text()
        matches = re.findall(r"NODE_VERSION:\s*['\"]?(\d+)['\"]?", content)
        versions_found.update(matches)
    return versions_found


def check_package_json():
    """Check package.json engines field."""
    pkg = Path("package.json")
    if not pkg.exists():
        return None
    data = json.loads(pkg.read_text())
    return data.get("engines", {})


def main():
    print("🔍 DevOps Version Checker")
    print("=" * 50)

    # Check each CLI tool
    checks = {
        "node": (["node", "-v"], r"v?([\d]+\.[\d]+\.[\d]+)"),
        "npm": (["npm.cmd", "-v"] if sys.platform == "win32" else ["npm", "-v"], r"[\d]+\.[\d]+\.[\d]+"),
        "git": (["git", "--version"], r"[\d]+\.[\d]+\.[\d]+"),
        "python": (["python", "--version"], r"[\d]+\.[\d]+\.[\d]+"),
        "docker": (["docker", "--version"], r"[\d]+\.[\d]+\.[\d]+"),
        "cline": (["cline.cmd", "--version"] if sys.platform == "win32" else ["cline", "--version"], r"[\d]+\.[\d]+\.[\d]+"),
        "opencode": (["opencode", "--version"], r"[\d]+\.[\d]+\.[\d]+"),
    }

    versions = {}
    for name, (cmd, pattern) in checks.items():
        ver = get_version(cmd, pattern)
        versions[name] = ver
        spec = EXPECTED.get(name, {})

        if ver is None:
            if spec.get("present"):
                warnings.append(f"❌ {name} — NOT FOUND")
            else:
                info.append(f"⏭️  {name} — not installed (optional)")
        else:
            info.append(f"✅ {name} {ver}")
            if "min" in spec and parse_version(ver) < parse_version(spec["min"]):
                warnings.append(f"⚠️  {name} {ver} < minimum {spec['min']}")

    # Pre-commit (special command)
    pre_ver = get_version(["python", "-m", "pre_commit", "--version"])
    if pre_ver:
        info.append(f"✅ pre-commit {pre_ver}")
    else:
        warnings.append("❌ pre-commit — NOT FOUND (pip install pre-commit)")

    # .nvmrc check
    nvmrc_ver = check_nvmrc()
    if nvmrc_ver and versions.get("node"):
        node_major = versions["node"].split(".")[0]
        nvmrc_major = nvmrc_ver.split(".")[0]
        if node_major != nvmrc_major:
            warnings.append(
                f"⚠️  Node version mismatch: local={versions['node']}, .nvmrc={nvmrc_ver}"
            )
        else:
            info.append(f"✅ .nvmrc matches (both v{nvmrc_major})")

    # CI version check
    ci_versions = check_ci_node_version()
    if ci_versions and versions.get("node"):
        node_major = versions["node"].split(".")[0]
        for ci_v in ci_versions:
            if ci_v != node_major:
                warnings.append(
                    f"⚠️  CI Node version mismatch: local=v{node_major}, CI=v{ci_v}"
                )

    # Package.json engines
    engines = check_package_json()
    if engines:
        info.append(f"📦 package.json engines: {engines}")

    # Report
    print()
    for line in info:
        print(f"  {line}")

    if warnings:
        print(f"\n{'=' * 50}")
        print(f"⚠️  {len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  {w}")
        print()
        return 1
    else:
        print(f"\n✅ All checks passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
