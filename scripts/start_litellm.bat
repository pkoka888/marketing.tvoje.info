@echo off
echo --- Starting LiteLLM Proxy ---

REM Ensure venv exists
if not exist ".venv" (
    echo Error: Virtual environment not found. Please run scripts\setup_litellm.bat first.
    pause
    exit /b 1
)

REM Configuration Path
set CONFIG_PATH=C:\Users\pavel\vscodeportable\agentic\litellm\proxy_server_config.yaml

REM Run Proxy
echo Proxying config: %CONFIG_PATH%
echo Listening on: http://localhost:4000
echo.

.venv\Scripts\python.exe scripts\run_litellm.py
pause

pause
