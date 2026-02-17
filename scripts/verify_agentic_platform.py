import json
import os
import sys

import yaml


def check_dir(path):
    exists = os.path.isdir(path)
    print(f"{'✅' if exists else '❌'} {path}")
    return exists


def check_file(path):
    exists = os.path.isfile(path)
    print(f"{'✅' if exists else '❌'} {path}")
    return exists


def validate_yaml(path):
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            yaml.safe_load(f)
        print(f"✅ {path} (Valid YAML)")
        return True
    except Exception as e:
        print(f"❌ {path} (Invalid YAML: {e})")
        return False


def validate_json(path):
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"✅ {path} (Valid JSON)")
        return True
    except Exception as e:
        print(f"❌ {path} (Invalid JSON: {e})")
        return False


def check_agent_json_prompt_paths():
    """Verify file:// prompt paths in .kilocode/agents/*.json actually resolve."""
    agents_dir = ".kilocode/agents"
    if not os.path.isdir(agents_dir):
        return []
    issues = []
    for agent_file in os.listdir(agents_dir):
        if not agent_file.endswith(".json"):
            continue
        full_path = os.path.join(agents_dir, agent_file)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        prompt = data.get("prompt", "")
        if prompt.startswith("file://"):
            rel = prompt[7:]  # strip file://
            # Resolve relative to the agents dir
            resolved = os.path.normpath(os.path.join(agents_dir, rel))
            exists = os.path.isfile(resolved) or os.path.isdir(resolved)
            icon = "✅" if exists else "❌"
            print(f"  {icon} {agent_file} prompt → {resolved}")
            if not exists:
                issues.append(f"{agent_file}: prompt path not found: {resolved}")
    return issues


def check_agents_yaml_sources():
    """Verify all source: file:// paths in .agent/agents.yaml exist."""
    yaml_path = ".agent/agents.yaml"
    if not os.path.exists(yaml_path):
        return []
    issues = []
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for rule in (data or {}).get("rules", []):
        src = rule.get("source", "")
        if src.startswith("file://"):
            file_path = src[7:]
            exists = os.path.isfile(file_path)
            icon = "✅" if exists else "❌"
            print(f"  {icon} agents.yaml rule → {file_path}")
            if not exists:
                issues.append(f"agents.yaml: rule source not found: {file_path}")
    return issues


def check_rule_parity():
    """Verify critical rules exist in all agent rule directories."""
    critical_rules = [
        "server-preservation",
        "python-preferred",
        "cost-optimization",
        "bmad-integration",
    ]
    rule_dirs = [
        ".kilocode/rules",
        ".agents/rules",
        ".clinerules/skills",
    ]
    issues = []
    for rule in critical_rules:
        for d in rule_dirs:
            if not os.path.isdir(d):
                print(f"  ⚠️  {d} (directory missing — skipping rule parity for {rule})")
                continue
            entries = os.listdir(d)
            found = any(e.startswith(rule) or e == rule for e in entries)
            icon = "✅" if found else "❌"
            print(f"  {icon} {d}/{rule}")
            if not found:
                issues.append(f"Rule '{rule}' missing in {d}")
    return issues


def check_opencode_setup():
    """Verify OpenCode integration files are present and use free model as default."""
    issues = []
    required = [
        ("opencode.json", "opencode.json"),
        (".opencode/agent/coder.md", ".opencode/agent/coder.md"),
        (".opencode/agent/orchestrator.md", ".opencode/agent/orchestrator.md"),
        (".opencode/command/audit.md", ".opencode/command/audit.md"),
        (".opencode/skill/astro-portfolio/SKILL.md", ".opencode/skill/astro-portfolio/SKILL.md"),
    ]
    for path, label in required:
        exists = os.path.isfile(path)
        icon = "✅" if exists else "❌"
        print(f"  {icon} {label}")
        if not exists:
            issues.append(f"Missing: {path}")
    # Check default model is free (not anthropic/ or openai/ at top level)
    if os.path.isfile("opencode.json"):
        try:
            with open("opencode.json", "r", encoding="utf-8") as f:
                cfg = json.load(f)
            model = cfg.get("model", "")
            paid_prefixes = ("anthropic/", "openai/")
            if any(model.startswith(p) for p in paid_prefixes):
                print(f"  ❌ opencode.json default model is PAID: {model}")
                issues.append(f"opencode.json: default model should be free, got: {model}")
            else:
                print(f"  ✅ opencode.json default model is free: {model}")
        except Exception as e:
            print(f"  ❌ opencode.json: failed to parse — {e}")
            issues.append(f"opencode.json: parse error: {e}")
    return issues


def check_claude_setup():
    """Verify Claude Code integration files are present."""
    issues = []
    for path, label in [
        ("CLAUDE.md", "CLAUDE.md (project root)"),
        (".claude/settings.json", ".claude/settings.json"),
        (".claude/hooks/pre_tool_use.py", ".claude/hooks/pre_tool_use.py"),
        (".claude/commands/audit.md", ".claude/commands/audit.md"),
    ]:
        exists = os.path.isfile(path)
        icon = "✅" if exists else "❌"
        print(f"  {icon} {label}")
        if not exists:
            issues.append(f"Missing: {path}")
    return issues


def main():
    print("--- 🛡️ Unified Agentic Platform Verification ---")
    all_issues = []

    # 1. Structural Checks (original)
    print("\n[Namespace: .clinerules]")
    check_dir(".clinerules/skills")
    check_dir(".clinerules/workflows")
    check_dir(".clinerules/hooks")
    check_file(".clinerules/hooks/TaskStart")
    check_file(".clinerules/hooks/PreToolUse")

    print("\n[Namespace: .kilocode]")
    check_dir(".kilocode/skills")
    check_dir(".kilocode/workflows")
    check_dir(".kilocode/agents")
    check_file(".kilocodemodes")
    check_file("kilocode.json")

    print("\n[Namespace: .agent]")
    check_dir(".agent")
    check_file(".agent/agents.yaml")

    # 2. Schema Validation (original)
    print("\n[Configuration Validation]")
    validate_yaml(".kilocodemodes")
    validate_json("kilocode.json")
    validate_yaml(".agent/agents.yaml")

    for agent_file in os.listdir(".kilocode/agents"):
        if agent_file.endswith(".json"):
            validate_json(os.path.join(".kilocode/agents", agent_file))

    # 3. Broken Reference Checks (NEW)
    print("\n[Broken Reference Checks — .kilocode/agents prompt paths]")
    all_issues.extend(check_agent_json_prompt_paths())

    print("\n[Broken Reference Checks — agents.yaml rule sources]")
    all_issues.extend(check_agents_yaml_sources())

    # 4. OpenCode Setup Checks (NEW)
    print("\n[OpenCode Setup]")
    all_issues.extend(check_opencode_setup())

    # 4. Claude Code Setup Checks (NEW)
    print("\n[Claude Code Setup]")
    all_issues.extend(check_claude_setup())

    # 5. Cross-Agent Rule Parity (NEW)
    print("\n[Cross-Agent Rule Parity — critical rules in all agent dirs]")
    all_issues.extend(check_rule_parity())

    # 6. Summary
    print("\n--- 🏁 Verification Completed ---")
    if all_issues:
        print(f"\n⚠️  {len(all_issues)} issue(s) found:")
        for issue in all_issues:
            print(f"  • {issue}")
        sys.exit(1)
    else:
        print("\n✅ All checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
