#!/usr/bin/env python3
"""
.env Validation Script
Compares .env keys against .env.example to detect missing or extra keys.

Usage:
    python scripts/validate_env.py
"""

import os
import sys
from pathlib import Path

# Expected keys from .env.example
EXPECTED_KEYS = {
    # LLM Providers
    "OPENROUTER_API_KEY",
    "GROQ_API_KEY", 
    "GEMINI_API_KEY",
    "OPENAI_API_KEY",
    "NVIDIA_API_KEY",
    "KILOCODE_API_KEY",
    # Gateways
    "ROUTEWAY_API_KEY",
    # Web Scraping
    "FIRECRAWL_API_KEY",
    # Auth
    "GITHUB_TOKEN",
    # Infrastructure
    "TS_OAUTH_CLIENT_ID",
    "TS_OAUTH_SECRET",
    # VPS
    "VPS_IP",
    "VPS_USER",
    "VPS_SSH_PORT",
    "VPS_SSH_KEY",
    # Public Config
    "PUBLIC_SITE_URL",
    "PUBLIC_FORMSPREE_ENDPOINT",
    "PUBLIC_PLAUSIBLE_DOMAIN",
    # Database
    "REDIS_PASSWORD",
    # Development (optional)
    "NODE_ENV",
    "PROJECT_NAME",
    "DEBUG",
    "LOG_LEVEL",
    "FEATURE_DARK_MODE",
    "FEATURE_I18N",
    "REDIS_URL",
    "PUBLIC_PLAUSIBLE_API_HOST",
}


def parse_env_file(filepath):
    """Parse .env file and extract key names."""
    keys = set()
    if not filepath.exists():
        return keys
    
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key = line.split("=")[0].strip()
                if key:
                    keys.add(key)
    
    return keys


def main():
    print("=" * 60)
    print(".ENV VALIDATION")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    # Parse both files
    env_keys = parse_env_file(env_file)
    example_keys = parse_env_file(env_example)
    
    print(f"\n.env keys: {len(env_keys)}")
    print(f".env.example keys: {len(example_keys)}")
    print()
    
    # Check for missing required keys (in example as ACTIVE but not in .env)
    # Keys that have values (not commented out) in .env.example
    required_keys = {
        "OPENROUTER_API_KEY", "GROQ_API_KEY", "GEMINI_API_KEY",
        "OPENAI_API_KEY", "NVIDIA_API_KEY", "KILOCODE_API_KEY",
        "ROUTEWAY_API_KEY", "FIRECRAWL_API_KEY", "GITHUB_TOKEN",
        "PUBLIC_SITE_URL", "PUBLIC_FORMSPREE_ENDPOINT", 
        "PUBLIC_PLAUSIBLE_DOMAIN", "REDIS_PASSWORD"
    }
    
    missing_required = required_keys - env_keys
    
    # Optional/uncommented keys that differ
    optional_in_example = example_keys - required_keys
    extra_keys = env_keys - example_keys
    
    issues_found = False
    
    # Only report critical missing keys (required API keys)
    if missing_required:
        issues_found = True
        print("⚠️  MISSING REQUIRED KEYS:")
        for key in sorted(missing_required):
            print(f"  - {key}")
        print()
    
    # Report extra keys (might be valid additions)
    if extra_keys:
        print("ℹ️  EXTRA KEYS (in .env but not in .env.example):")
        for key in sorted(extra_keys):
            print(f"  - {key}")
        print()
    
    if not issues_found:
        print("✅ ALL REQUIRED KEYS PRESENT")
        return 0
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
