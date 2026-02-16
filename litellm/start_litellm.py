#!/usr/bin/env python3
"""
LiteLLM Proxy Startup Script

Usage:
    python start_litellm.py

Requirements:
    - pip install litellm python-dotenv pyyaml
    - Copy .env.example to .env and add your API keys
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
ENV_FILE = SCRIPT_DIR / ".env"
CONFIG_FILE = SCRIPT_DIR / "proxy_config.yaml"


def run_validation():
    """Run configuration validation before starting."""
    try:
        # Import validation module
        import validate_config

        print("\n" + "="*60)
        print("Running pre-start validation...")
        print("="*60)

        result = validate_config.main()

        if result != 0:
            print("\n" + "="*60)
            print("Validation FAILED. Fix issues before starting proxy.")
            print("Run 'python validate_config.py' for details.")
            print("="*60 + "\n")
            return False

        print("\n" + "="*60)
        print("Validation PASSED. Starting proxy...")
        print("="*60 + "\n")
        return True

    except ImportError as e:
        print(f"WARNING: Could not import validate_config: {e}")
        print("Skipping validation (validate_config.py not found or missing dependencies)")
        return True
    except Exception as e:
        print(f"WARNING: Validation error: {e}")
        print("Proceeding with startup anyway...")
        return True


def main():
    # Load environment variables
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
        print(f"Loaded environment from {ENV_FILE}")
    else:
        print(f"WARNING: {ENV_FILE} not found!")
        print("Please copy .env.example to .env and add your API keys")
        sys.exit(1)

    # Run validation before starting
    if not run_validation():
        sys.exit(1)

    # Check for API keys (informational only - validation already checked)
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "YOUR_GROQ_KEY_HERE":
        print("WARNING: GROQ_API_KEY not set or is placeholder!")
        print("You can still run, but Groq models won't work.")

    # Find the litellm CLI executable
    # On Windows with venv, it's in the same directory as python executable
    python_dir = Path(sys.executable).parent
    litellm_exe = python_dir / "litellm"

    # On Windows, also try with .exe extension
    if sys.platform == "win32":
        litellm_exe_win = python_dir / "litellm.exe"
        if litellm_exe_win.exists():
            litellm_exe = litellm_exe_win

    # Build command - use CLI entry point instead of -m module execution
    # LiteLLM doesn't support `python -m litellm` because it lacks __main__.py
    if litellm_exe.exists():
        cmd = [
            str(litellm_exe),
            "--config",
            str(CONFIG_FILE),
            "--port",
            "4000",
            "--host",
            "0.0.0.0",
        ]
    else:
        # Fallback: try using the CLI via subprocess shell
        # This works if litellm is in PATH
        cmd = [
            "litellm",
            "--config",
            str(CONFIG_FILE),
            "--port",
            "4000",
            "--host",
            "0.0.0.0",
        ]

    print(f"\nStarting LiteLLM Proxy...")
    print(f"Config: {CONFIG_FILE}")
    print(f"URL: http://localhost:4000")
    print(f"Command: {' '.join(cmd)}")
    print(f"\nPress Ctrl+C to stop\n")

    # Run litellm
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
