import sys
import subprocess
import os

# Identify python executable
python_exe = sys.executable

print(f"Using python: {python_exe}")

# Command to run litellm module
cmd = [python_exe, "-m", "litellm", "--config", r"C:\Users\pavel\vscodeportable\agentic\litellm\proxy_server_config.yaml", "--port", "4000", "--debug"]

print(f"Running command: {cmd}")

try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running litellm: {e}")
    sys.exit(e.returncode)
