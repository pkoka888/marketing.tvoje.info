import subprocess
import sys
import os
from pathlib import Path

def run_command(command: list[str]) -> bool:
    print(f"Running: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def init_env():
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("--- Initializing Python Environment ---")

    # 1. Check Python version
    print(f"Using Python: {sys.executable}")

    # 2. Create Virtual Environment
    if not os.path.exists(".venv"):
        print("Creating virtual environment...")
        if not run_command([sys.executable, "-m", "venv", ".venv"]):
            print("Failed to create venv.")
            return

    # 3. Install requirements
    venv_python = ".venv/Scripts/python.exe" if os.name == "nt" else ".venv/bin/python"
    if os.path.exists("requirements.txt"):
        print("Installing requirements...")
        run_command([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
        run_command([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])

    print("\n--- Setup Complete ---")
    print("Good Practices for this environment:")
    print("1. Use 'python' for all commands (mapped to 3.x)")
    print("2. 'python3.cmd' and 'py.cmd' shims have been added to the root for compatibility.")
    print("3. Always work within the Virtual Environment.")
    print("\nTo activate the environment in PowerShell:")
    print("   & .\\.venv\\Scripts\\Activate.ps1")

if __name__ == "__main__":
    init_env()
