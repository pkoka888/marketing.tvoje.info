@echo off
echo --- Setting up LiteLLM Environment ---

REM 1. Create access to Python
set PYTHON_EXE=C:\Users\HP\AppData\Local\Programs\Python\Python313\python.exe

REM 2. Create Virtual Environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    "%PYTHON_EXE%" -m venv .venv
) else (
    echo Virtual environment already exists.
)

REM 3. Install/Upgrade Dependencies
echo Installing LiteLLM and Proxy dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install "litellm[proxy]" uvicorn click

echo.
echo --- Setup Complete ---
echo You can now run logs via: scripts\start_litellm.bat
pause
