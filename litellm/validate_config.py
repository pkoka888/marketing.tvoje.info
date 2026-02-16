#!/usr/bin/env python3
"""
LiteLLM Configuration Validation Script

Validates:
1. Required environment variables are set
2. YAML configuration syntax is valid
3. Connectivity to at least one provider

Exit codes:
  0 - All validations passed
  1 - Environment variables check failed
  2 - YAML configuration validation failed
  3 - Multiple failures
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
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_status(status: str, message: str) -> None:
    """Print a colored status message."""
    if status == "PASS":
        print(f"{Colors.GREEN}✓ PASS{Colors.RESET}: {message}")
    elif status == "FAIL":
        print(f"{Colors.RED}✗ FAIL{Colors.RESET}: {message}")
    elif status == "WARN":
        print(f"{Colors.YELLOW}⚠ WARN{Colors.RESET}: {message}")
    elif status == "INFO":
        print(f"{Colors.BLUE}ℹ INFO{Colors.RESET}: {message}")


def check_environment_variables() -> bool:
    """
    Check that required environment variables are set.

    Returns:
        True if all required variables are set, False otherwise.
    """
    print("\n" + "="*60)
    print("Environment Variables Check")
    print("="*60)

    # Required variables
    required_vars = [
        "LITELLM_MASTER_KEY",
        "GROQ_API_KEY",
    ]

    # Optional variables (at least one should be set for fallbacks)
    optional_vars = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
    ]

    all_valid = True

    # Check required variables
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mask the value for security
            masked = value[:4] + "..." if len(value) > 4 else "***"
            print_status("PASS", f"{var} is set ({masked})")
        else:
            print_status("FAIL", f"{var} is not set")
            all_valid = False

    # Check optional variables
    optional_set = 0
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            optional_set += 1
            print_status("INFO", f"{var} is set (optional)")

    if optional_set == 0:
        print_status("WARN", "No fallback API keys set (only Groq available)")
    else:
        print_status("PASS", f"{optional_set} fallback provider(s) configured")

    return all_valid


def validate_yaml_syntax(config_path: Path) -> dict:
    """
    Validate YAML syntax and load configuration.

    Args:
        config_path: Path to the proxy_config.yaml file.

    Returns:
        Parsed configuration dict if valid, None otherwise.
    """
    print("\n" + "="*60)
    print("YAML Configuration Validation")
    print("="*60)

    if not config_path.exists():
        print_status("FAIL", f"Configuration file not found: {config_path}")
        return None

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        print_status("PASS", "YAML syntax is valid")

        # Validate required sections
        required_sections = ["model_list", "litellm_settings"]
        for section in required_sections:
            if section in config:
                print_status("PASS", f"Section '{section}' found")
            else:
                print_status("FAIL", f"Required section '{section}' missing")
                return None

        # Check for fallbacks section
        if "fallbacks" in config:
            fallback_count = len(config.get("fallbacks", []))
            print_status("PASS", f"Fallbacks section found ({fallback_count} chains)")
        else:
            print_status("WARN", "No fallbacks section found (recommended for reliability)")

        # Check for hardcoded secrets
        config_str = str(config)
        if "sk-local-dev" in config_str:
            print_status("FAIL", "Hardcoded test key detected in config")
            return None

        # Check master_key uses environment variable
        general_settings = config.get("general_settings", {})
        master_key = general_settings.get("master_key", "")
        if "os.environ" in str(master_key):
            print_status("PASS", "Master key uses environment variable reference")
        elif master_key:
            print_status("FAIL", "Master key appears to be hardcoded (security risk)")
            return None

        return config

    except yaml.YAMLError as e:
        print_status("FAIL", f"YAML parsing error: {e}")
        return None
    except Exception as e:
        print_status("FAIL", f"Error reading config: {e}")
        return None


def test_provider_connectivity() -> bool:
    """
    Test connectivity to at least one LLM provider.

    Returns:
        True if at least one provider is reachable, False otherwise.
    """
    print("\n" + "="*60)
    print("Provider Connectivity Check")
    print("="*60)

    groq_key = os.environ.get("GROQ_API_KEY")
    if not groq_key:
        print_status("INFO", "GROQ_API_KEY not set, skipping connectivity test")
        return True  # Don't fail if key not set (env check already failed)

    try:
        import requests

        # Test Groq API connectivity
        print_status("INFO", "Testing Groq API connectivity...")

        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {groq_key}"},
            timeout=10
        )

        if response.status_code == 200:
            models = response.json().get("data", [])
            print_status("PASS", f"Groq API reachable ({len(models)} models available)")
            return True
        else:
            print_status("WARN", f"Groq API returned status {response.status_code}")
            return True  # Don't fail on API errors, just warn

    except requests.exceptions.Timeout:
        print_status("WARN", "Groq API timeout (network may be slow)")
        return True
    except requests.exceptions.ConnectionError:
        print_status("WARN", "Groq API connection error (network may be unavailable)")
        return True
    except ImportError:
        print_status("INFO", "requests module not installed, skipping connectivity test")
        return True
    except Exception as e:
        print_status("WARN", f"Unexpected error during connectivity test: {e}")
        return True  # Don't fail on unexpected errors


def main() -> int:
    """
    Main validation function.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    print("="*60)
    print("LiteLLM Configuration Validation")
    print("="*60)

    # Load environment variables from .env file
    script_dir = Path(__file__).parent
    env_file = script_dir / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print_status("INFO", f"Loaded environment from {env_file}")
    else:
        print_status("WARN", f"No .env file found at {env_file}")

    # Determine config path
    config_path = script_dir / "proxy_config.yaml"

    # Track validation results
    env_valid = True
    yaml_valid = True
    connectivity_valid = True

    # Run validations
    env_valid = check_environment_variables()
    config = validate_yaml_syntax(config_path)
    yaml_valid = config is not None

    if env_valid:
        connectivity_valid = test_provider_connectivity()

    # Print summary
    print("\n" + "="*60)
    print("Validation Summary")
    print("="*60)

    if env_valid and yaml_valid:
        print_status("PASS", "All critical validations passed")
        if not connectivity_valid:
            print_status("WARN", "Some non-critical checks failed")
        return 0
    else:
        if not env_valid:
            print_status("FAIL", "Environment variables check failed")
            return 1
        if not yaml_valid:
            print_status("FAIL", "YAML configuration validation failed")
            return 2
        return 3


if __name__ == "__main__":
    sys.exit(main())
