#!/usr/bin/env python3
"""
Universal API Keys Verification Script v3
Tests ALL API keys from .env + GitHub Secrets

Usage: python scripts/verify_api_keys.py
"""

import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    os.system("pip install requests python-dotenv -q")
    import requests

from dotenv import load_dotenv

# Complete API Key Configuration
API_KEYS_CONFIG = {
    # === LLM / AI PROVIDERS ===
    "OPENROUTER_API_KEY": {
        "endpoint": "https://openrouter.ai/api/v1/models",
        "method": "GET",
        "auth_type": "bearer",
        "purpose": "Free LLM models (minimax, glm4, qwen3, deepseek)",
    },
    "GROQ_API_KEY": {
        "endpoint": "https://api.groq.com/openai/v1/models",
        "method": "GET",
        "auth_type": "bearer",
        "purpose": "Fast LLM fallback (llama-3.1, llama-3.3)",
    },
    "GEMINI_API_KEY": {
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
        "method": "GET",
        "auth_type": "param",
        "param_name": "key",
        "purpose": "Google AI LLM (gemini-2.5-flash, gemini-2.5-pro)",
    },
    "OPENAI_API_KEY": {
        "endpoint": "https://api.openai.com/v1/models",
        "method": "GET",
        "auth_type": "bearer",
        "purpose": "OpenAI LLM (GPT-4o, gpt-4o-mini)",
    },
    "NVIDIA_API_KEY": {
        "endpoint": "https://integrate.api.nvidia.com/v1/models",
        "method": "GET",
        "auth_type": "bearer",
        "purpose": "NVIDIA NIM microservices",
    },
    "KILOCODE_API_KEY": {
        "purpose": "Kilo Code CLI authentication (JWT, verified by IDE only)",
        "presence_only": True,
    },
    # === ALTERNATIVE LLM GATEWAYS ===
    "ROUTEWAY_API_KEY": {
        "endpoint": "https://api.routeway.ai/v1/models",
        "method": "GET",
        "auth_type": "bearer",
        "purpose": "Alternative LLM gateway (free models available)",
    },
    # === WEB SCRAPING ===
    "FIRECRAWL_API_KEY": {
        "purpose": "Web scraping and data extraction",
        "presence_only": True,  # Key exists in .env, verified manually
    },
    # === AUTH / CI/CD ===
    "GITHUB_TOKEN": {
        "endpoint": "https://api.github.com/user",
        "method": "GET",
        "auth_type": "bearer",
        "purpose": "GitHub API for CI/CD and automation",
    },
    # === OAUTH / REMOTE ACCESS (GitHub Secrets only — not in .env) ===
    "TS_OAUTH_CLIENT_ID": {
        "purpose": "Tailscale OAuth client ID",
        "source": "github_secrets",
    },
    "TS_OAUTH_SECRET": {
        "purpose": "Tailscale OAuth client secret",
        "source": "github_secrets",
    },
    # === VPS (GitHub Secrets only — not in .env) ===
    "VPS_IP": {"purpose": "VPS server IP address", "source": "github_secrets"},
    "VPS_USER": {"purpose": "VPS SSH username", "source": "github_secrets"},
    "VPS_SSH_PORT": {"purpose": "VPS SSH port", "source": "github_secrets"},
    "VPS_SSH_KEY": {"purpose": "VPS SSH private key", "source": "github_secrets"},
    # === CONFIG ===
    "PUBLIC_SITE_URL": {"purpose": "Public site URL for SEO", "presence_only": True},
    "PUBLIC_FORMSPREE_ENDPOINT": {
        "purpose": "Formspree form endpoint",
        "presence_only": True,
    },
    "PUBLIC_PLAUSIBLE_DOMAIN": {
        "purpose": "Plausible analytics domain",
        "presence_only": True,
    },
    # === DATABASE ===
    "REDIS_PASSWORD": {"purpose": "Redis cache password", "presence_only": True},
}


def test_api_key(name: str, config: dict) -> tuple[bool, str]:
    # Keys that only exist in GitHub Secrets — skip gracefully
    if config.get("source") == "github_secrets":
        api_key = os.environ.get(name)
        if api_key:
            masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            return True, f"Present ({masked})"
        return True, "⏭️ GH Secrets only (not in .env)"

    api_key = os.environ.get(name)

    if not api_key:
        return False, "Not found"

    masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"

    if config.get("presence_only"):
        return True, f"Present ({masked})"

    try:
        headers, params = {}, {}

        if config.get("auth_type") == "bearer":
            headers["Authorization"] = f"Bearer {api_key}"
        elif config.get("auth_type") == "header":
            headers[config.get("header_name", "X-goog-api-key")] = api_key
        elif config.get("auth_type") == "param":
            params[config["param_name"]] = api_key

        response = requests.request(
            method=config["method"],
            url=config["endpoint"],
            headers=headers,
            params=params,
            timeout=15,
        )

        if response.status_code == 200:
            return True, f"OK ({response.status_code})"
        elif response.status_code == 401:
            return False, "Unauthorized"
        elif response.status_code == 402:
            return False, "Payment Required"
        elif response.status_code == 403:
            return False, "Forbidden"
        elif response.status_code == 404:
            return False, "Not Found"
        else:
            return False, f"Error {response.status_code}"

    except Exception as e:
        return False, f"Exception: {str(e)[:30]}"


def main():
    print("=" * 70)
    print("Universal API Keys Verification v3")
    print("=" * 70)

    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)
        print(f"✅ Loaded: {env_path} (override=True)")

    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    categories = {
        "🤖 LLM Providers": [
            "OPENROUTER_API_KEY",
            "GROQ_API_KEY",
            "GEMINI_API_KEY",
            "OPENAI_API_KEY",
            "NVIDIA_API_KEY",
            "KILOCODE_API_KEY",
        ],
        "🌐 Gateways": ["ROUTEWAY_API_KEY"],
        "🕸️ Web Scraping": ["FIRECRAWL_API_KEY"],
        "🔐 Auth / CI/CD": ["GITHUB_TOKEN"],
        "🔧 Infrastructure": ["TS_OAUTH_CLIENT_ID", "TS_OAUTH_SECRET"],
        "🖥️ VPS": ["VPS_IP", "VPS_USER", "VPS_SSH_PORT", "VPS_SSH_KEY"],
        "🌍 Config": [
            "PUBLIC_SITE_URL",
            "PUBLIC_FORMSPREE_ENDPOINT",
            "PUBLIC_PLAUSIBLE_DOMAIN",
        ],
        "💾 Database": ["REDIS_PASSWORD"],
    }

    results = {}
    for category, keys in categories.items():
        print(f"{category}:")
        print("-" * 50)
        for key in keys:
            config = API_KEYS_CONFIG.get(key, {})
            success, message = test_api_key(key, config)
            results[key] = success
            if "⏭️" in message:
                status = "⏭️"
            elif success:
                status = "✅"
            else:
                status = "❌"
            print(f"  {status} {key}: {message}")
        print()

    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print("=" * 70)
    print(f"Summary: {passed}/{total} keys verified")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
