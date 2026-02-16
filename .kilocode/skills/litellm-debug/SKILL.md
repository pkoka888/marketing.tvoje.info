# LiteLLM Debug Skill

## Description

Comprehensive debugging and troubleshooting skill for LiteLLM proxy configuration, particularly focused on Windows port binding issues, Groq API integration, and provider fallback configurations.

## Purpose

Diagnose and resolve LiteLLM proxy issues including:

- Windows port binding failures (port 4000)
- Groq API configuration errors
- Environment variable issues
- Redis dependency problems
- Provider fallback setup

## Skill Triggers

Use this skill when:

- LiteLLM proxy reports "Listening" but doesn't bind to port
- Connection refused errors on localhost:4000
- Groq API authentication failures
- Model not found errors
- Rate limiting issues

## Quick Reference

### Common Error Codes

| Error Code            | Meaning                   | Solution                                 |
| --------------------- | ------------------------- | ---------------------------------------- |
| `401 Unauthorized`    | Missing/invalid API key   | Set `GROQ_API_KEY` environment variable  |
| `404 Model Not Found` | Model name not in config  | Use correct model alias or add to config |
| `429 Rate Limited`    | Too many requests         | Check `rpm` setting, implement backoff   |
| `500 Internal Error`  | Proxy configuration issue | Check logs, verify config file syntax    |
| `Connection Refused`  | Port not bound            | Check Windows Firewall, port conflicts   |
| `Timeout`             | Request timeout           | Increase `timeout` in litellm_params     |

### Groq-Specific Errors

| Error                     | Meaning              | Solution                       |
| ------------------------- | -------------------- | ------------------------------ |
| `invalid_api_key`         | GROQ_API_KEY invalid | Verify key at console.groq.com |
| `model_overloaded`        | Groq capacity issue  | Retry with exponential backoff |
| `context_length_exceeded` | Input too long       | Reduce prompt size             |

## Diagnostic Commands

### Windows Port Diagnostics

```cmd
:: Check if port 4000 is in use
netstat -ano | findstr :4000

:: Check what process is using port 4000 (if any)
for /f "tokens=5" %a in ('netstat -ano ^| findstr :4000') do tasklist /fi "pid eq %a"

:: Check Windows Firewall status
netsh advfirewall show allprofiles

:: Test if port 4000 is blocked
netsh advfirewall firewall show rule name=all | findstr 4000

:: Check Hyper-V port exclusion
netsh interface ipv4 show excludedportrange protocol=tcp
```

### LiteLLM Health Check

```cmd
:: Test health endpoint
curl http://localhost:4000/health

:: PowerShell alternative
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:4000/health' -UseBasicParsing"
```

### Environment Verification

```cmd
:: Check if GROQ_API_KEY is set
echo %GROQ_API_KEY%

:: Set temporarily for testing
set GROQ_API_KEY=your_key_here
```

### Debug Mode Startup

```cmd
cd C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm
python -m litellm --config proxy_server_config.yaml --port 4000 --host 127.0.0.1 --debug
```

## Configuration Paths

### Primary Configuration

| File         | Path                                                                                         |
| ------------ | -------------------------------------------------------------------------------------------- |
| Config       | `C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm\proxy_server_config.yaml` |
| Env Template | `C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm\.env.example`             |

### Project Scripts

| Script                           | Purpose                                      |
| -------------------------------- | -------------------------------------------- |
| `scripts/run_litellm.py`         | Main launcher (correct config path)          |
| `scripts/start_litellm_proxy.py` | Alternative launcher (different config path) |
| `scripts/verify_groq_litellm.py` | Verification script                          |

## Known Issues

### Issue #1: Inconsistent Config Paths

**Problem**: Scripts reference different configuration file paths.
**Solution**: Always use `run_litellm.py` which has the correct path.

### Issue #2: Missing Environment Variables

**Problem**: `GROQ_API_KEY` and `OPENAI_API_KEY` must be set.
**Solution**: Create `.env` file in litellm directory or set environment variables.

### Issue #3: Redis Dependency

**Problem**: Router settings require Redis but may not be running.
**Solution**: Comment out Redis settings if not using Redis, or start Redis server.

### Issue #4: Windows Port Binding

**Problem**: Proxy says "Listening" but Windows doesn't bind port.
**Solutions**:

1. Run terminal as Administrator
2. Use `--host 127.0.0.1` instead of `0.0.0.0`
3. Add firewall rule: `netsh advfirewall firewall add rule name="LiteLLM" dir=in action=allow protocol=tcp localport=4000`
4. Check Hyper-V port exclusion

## Resolution Workflow

1. **Verify Environment Variables**
   - Check `GROQ_API_KEY` is set
   - Verify API key at console.groq.com

2. **Check Port Availability**
   - Run `netstat -ano | findstr :4000`
   - Kill any stuck processes

3. **Test with Localhost**
   - Use `--host 127.0.0.1` for testing
   - Run with `--debug` flag

4. **Verify Configuration**
   - Check config file path is correct
   - Validate YAML syntax
   - Comment out Redis if not using

5. **Check Windows Firewall**
   - Add rule for port 4000
   - Run as Administrator

## Related Files

- [REFERENCE.md](./REFERENCE.md) - Detailed error code reference
- [WORKFLOW.md](./WORKFLOW.md) - Step-by-step debugging workflow
- [CHECKLIST.md](./CHECKLIST.md) - Pre-flight checklist

## Version

- Created: 2026-02-13
- Author: Kilo Code
- Version: 1.0
