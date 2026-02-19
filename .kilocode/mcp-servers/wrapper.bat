@echo off
REM MCP Server Wrapper for Windows - Loads .env before starting servers
REM This keeps secrets centralized in .env file only

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%\..\.."

REM Load .env file
if exist "%PROJECT_ROOT%\.env" (
    for /f "tokens=*" %%a in ('type "%PROJECT_ROOT%\.env" ^| findstr /v "^#"') do (
        set "line=%%a"
        if not "!line!"=="" (
            for /f "tokens=1,* delims==" %%b in ("!line!") do (
                set "%%b=%%c"
            )
        )
    )
)

REM Execute the original command with all arguments
shift
%*
