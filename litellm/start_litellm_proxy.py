#!/usr/bin/env python3
"""
LiteLLM Proxy Server Startup Script

Usage:
    python start_litellm_proxy.py

Or with custom port:
    python start_litellm_proxy.py --port 8080
"""

import os
import sys
import argparse
from pathlib import Path

# Load environment
SCRIPT_DIR = Path(__file__).resolve().parent
ENV_FILE = SCRIPT_DIR / ".env"

if ENV_FILE.exists():
    from dotenv import load_dotenv

    load_dotenv(ENV_FILE)
    print(f"Loaded environment from {ENV_FILE}")

# Check for API key
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    print("ERROR: GROQ_API_KEY not found in .env")
    print("Please add GROQ_API_KEY to litellm/.env")
    sys.exit(1)

# Set environment for litellm
os.environ["GROQ_API_KEY"] = GROQ_KEY


def main():
    parser = argparse.ArgumentParser(description="Start LiteLLM Proxy")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to")
    args = parser.parse_args()

    import uvicorn
    from litellm.proxy.proxy_server import app

    print(f"""
╔════════════════════════════════════════════════════════════╗
║           LiteLLM Proxy Server                            ║
╠════════════════════════════════════════════════════════════╣
║  URL: http://{args.host}:{args.port}                        ║
║  Health: http://{args.host}:{args.port}/health              ║
║  Model: groq/llama-3.3-70b-versatile                     ║
╚════════════════════════════════════════════════════════════╝
    """)

    config = uvicorn.Config(
        app,
        host=args.host,
        port=args.port,
        log_level="info",
    )
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()
