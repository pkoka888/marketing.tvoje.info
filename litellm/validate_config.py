#!/usr/bin/env python3
"""
LiteLLM Configuration Validation Script

Validates:
1. Required environment variables are set
2. YAML configuration syntax and structure
3. Fallback chain integrity (all referenced models exist)
4. Provider connectivity

Exit codes: 0 = pass, 1 = env fail, 2 = yaml fail, 3 = multiple
"""
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def status(st: str, msg: str):
    icons = {"PASS": f"{Colors.GREEN}+{Colors.RESET}",
             "FAIL": f"{Colors.RED}X{Colors.RESET}",
             "WARN": f"{Colors.YELLOW}!{Colors.RESET}",
             "INFO": f"{Colors.BLUE}i{Colors.RESET}"}
    print(f"  [{icons.get(st, '?')}] {msg}")


def check_env() -> bool:
    print("\n[Environment Variables]")
    required = {
        "LITELLM_MASTER_KEY": "Proxy auth",
        "GROQ_API_KEY": "T4 last resort",
    }
    recommended = {
        "OPENROUTER_API_KEY": "T1 free models",
        "GEMINI_API_KEY": "T2 free complex + T3 architect",
        "OPENAI_API_KEY": "T4 paid fallback",
    }

    ok = True
    for var, desc in required.items():
        val = os.environ.get(var)
        if val and not val.startswith("YOUR_"):
            status("PASS", f"{var} ({desc}): {val[:6]}...")
        else:
            status("FAIL", f"{var} ({desc}): NOT SET")
            ok = False

    for var, desc in recommended.items():
        val = os.environ.get(var)
        if val and not val.startswith("YOUR_"):
            status("PASS", f"{var} ({desc}): {val[:6]}...")
        else:
            status("WARN", f"{var} ({desc}): not set — tier will use fallbacks")
    return ok


def check_yaml(config_path: Path) -> dict:
    print("\n[YAML Configuration]")
    if not config_path.exists():
        status("FAIL", f"Config not found: {config_path}")
        return None

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        status("PASS", "YAML syntax valid")
    except yaml.YAMLError as e:
        status("FAIL", f"YAML parse error: {e}")
        return None

    # Required sections
    if "model_list" not in config:
        status("FAIL", "Missing model_list section")
        return None
    status("PASS", f"model_list: {len(config['model_list'])} models")

    if "router_settings" not in config:
        status("WARN", "Missing router_settings (fallbacks won't work)")
    else:
        rs = config["router_settings"]
        if "fallbacks" in rs:
            status("PASS", f"router_settings.fallbacks: {len(rs['fallbacks'])} chains")
        else:
            status("WARN", "No fallbacks in router_settings")
        if "default_fallbacks" in rs:
            status("PASS", f"default_fallbacks: {rs['default_fallbacks']}")

    if "general_settings" in config:
        mk = config["general_settings"].get("master_key", "")
        if "os.environ" in str(mk):
            status("PASS", "master_key uses env reference")
        elif mk:
            status("FAIL", "master_key appears hardcoded")
            return None

    # Check for hardcoded secrets in model params
    for model in config.get("model_list", []):
        api_key = model.get("litellm_params", {}).get("api_key", "")
        if isinstance(api_key, str) and api_key and not api_key.startswith("os.environ"):
            status("FAIL", f"Hardcoded API key in model {model.get('model_name', '?')}")
            return None

    return config


def check_fallback_integrity(config: dict) -> bool:
    """Verify all fallback target models exist in model_list."""
    print("\n[Fallback Chain Integrity]")
    model_names = {m["model_name"] for m in config.get("model_list", [])}
    rs = config.get("router_settings", {})
    fallbacks = rs.get("fallbacks", [])
    default_fb = rs.get("default_fallbacks", [])

    ok = True
    for entry in fallbacks:
        for source, targets in entry.items():
            if source not in model_names:
                status("FAIL", f"Fallback source '{source}' not in model_list")
                ok = False
            for t in targets:
                if t not in model_names:
                    status("FAIL", f"Fallback target '{t}' (from {source}) not in model_list")
                    ok = False

    for t in default_fb:
        if t not in model_names:
            status("FAIL", f"default_fallback '{t}' not in model_list")
            ok = False

    if ok:
        status("PASS", f"All {len(fallbacks)} chains reference valid models")
    return ok


def check_connectivity() -> bool:
    """Quick connectivity check to Groq (always-available T4)."""
    print("\n[Provider Connectivity]")
    groq_key = os.environ.get("GROQ_API_KEY")
    if not groq_key:
        status("WARN", "GROQ_API_KEY not set, skipping")
        return True

    try:
        import urllib.request
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {groq_key}"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                status("PASS", "Groq API reachable")
                return True
    except Exception as e:
        status("WARN", f"Groq connectivity: {e}")
    return True  # Non-critical


def main() -> int:
    print("=" * 50)
    print("LiteLLM Config Validation")
    print("=" * 50)

    script_dir = Path(__file__).parent
    env_file = script_dir / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        status("INFO", f"Loaded {env_file}")

    config_path = script_dir / "proxy_config.yaml"

    env_ok = check_env()
    config = check_yaml(config_path)
    yaml_ok = config is not None
    fb_ok = check_fallback_integrity(config) if yaml_ok else False
    check_connectivity() if env_ok else None

    print(f"\n{'='*50}")
    if env_ok and yaml_ok and fb_ok:
        status("PASS", "All validations passed")
        return 0
    if not env_ok:
        status("FAIL", "Environment check failed")
        return 1
    if not yaml_ok:
        status("FAIL", "YAML validation failed")
        return 2
    return 3


if __name__ == "__main__":
    sys.exit(main())
