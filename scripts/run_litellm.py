import sys
import os
from dotenv import load_dotenv

# Load .env file from project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

print(f"--- LiteLLM Proxy Launcher ---")

# Check for API Key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("WARNING: GROQ_API_KEY not found in environment or .env file.")
    print("Please add GROQ_API_KEY=gsk_... to your .env file.")
elif "gsk_" not in api_key and "placeholder" in api_key.lower():
    print("WARNING: GROQ_API_KEY appears to be a placeholder.")
else:
    print("GROQ_API_KEY detected.")

# Import and Run LiteLLM
try:
    # Try importing the CLI entry point directly
    from litellm.proxy.proxy_cli import run_server

    # Set arguments programmatically to avoid CLI parsing issues
    # We point to the absolute path of the config file
    config_path = r"C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm\proxy_server_config.yaml"

    # Mock sys.argv as if called from command line
    sys.argv = ["litellm", "--config", config_path, "--port", "4000", "--host", "0.0.0.0", "--debug"]

    print(f"Starting proxy with config: {config_path}")
    print(f"Listening on: http://0.0.0.0:4000")

    run_server()
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import litellm. {e}")
    print("Ensue you are running this prompt within the virtual environment.")
    sys.exit(1)
except Exception as e:
    print(f"Runtime error: {e}")
    sys.exit(1)
