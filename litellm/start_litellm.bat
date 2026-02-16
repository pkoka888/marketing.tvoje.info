@echo off
REM LiteLLM Proxy Startup Script for marketing.tvoje.info
REM
REM Usage:
REM   1. Copy litellm\.env.example to litellm\.env and add your API keys
REM   2. Run this script: start_litellm.bat
REM   3. Proxy will be available at http://localhost:4000

echo Starting LiteLLM Proxy...
echo.

REM Check if .env exists
if not exist "%~dp0.env" (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your API keys
    pause
    exit /b 1
)

REM Load environment variables
echo Loading environment from .env...
for /f "usebackq tokens=*" %%a in ("%~dp0.env") do set %%a

REM Check for GROQ_API_KEY
if "%GROQ_API_KEY%"=="" (
    echo WARNING: GRO_API_KEY not set in .env
)

REM Start LiteLLM proxy
echo.
echo Starting proxy on http://localhost:4000
echo Press Ctrl+C to stop
echo.

python -m litellm --config "%~dp0proxy_config.yaml" --port 4000 --host 0.0.0.0

pause
