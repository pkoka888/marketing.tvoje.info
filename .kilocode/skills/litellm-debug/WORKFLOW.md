# LiteLLM Debug Workflow

## Overview

Step-by-step workflow for diagnosing and resolving LiteLLM proxy issues on Windows 11.

## Phase 1: Initial Assessment (5 minutes)

### Step 1.1: Verify Environment Variables

```cmd
:: Check GROQ_API_KEY
echo %GROQ_API_KEY%

:: Should output: gsk_xxxxxxxx
:: If empty or shows "%GROQ_API_KEY%", variable is not set
```

**If not set:**

```cmd
:: Set for current session (CMD)
set GROQ_API_KEY=gsk_your_key_here

:: Or PowerShell
$env:GROQ_API_KEY="gsk_your_key_here"
```

### Step 1.2: Check Port Availability

```cmd
:: Check if port 4000 is in use
netstat -ano | findstr :4000

:: If output shows LISTENING, note the PID
:: If empty, port is available
```

**If port is in use:**

```cmd
:: Kill process using port (replace PID)
taskkill /PID 12345 /F
```

### Step 1.3: Verify Configuration File

```cmd
:: Check if config file exists
dir "C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm\proxy_server_config.yaml"
```

**Expected output:** File should exist with recent modification date.

## Phase 2: Start LiteLLM (5 minutes)

### Step 2.1: Navigate to Directory

```cmd
cd "C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm"
```

### Step 2.2: Activate Virtual Environment (if exists)

```cmd
:: Check for venv
dir .venv

:: Activate (PowerShell)
.\.venv\Scripts\Activate.ps1

:: Activate (CMD)
.\.venv\Scripts\activate.bat
```

### Step 2.3: Start with Debug Mode

```cmd
:: Start with localhost binding and debug
python -m litellm --config proxy_server_config.yaml --port 4000 --host 127.0.0.1 --debug
```

**Expected output:**

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:4000
```

### Step 2.4: Verify Server is Running

**Open new terminal:**

```cmd
:: Test health endpoint
curl http://localhost:4000/health

:: PowerShell alternative
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:4000/health' -UseBasicParsing"
```

**Expected response:**

```json
{ "status": "healthy" }
```

## Phase 3: Diagnose Issues (10 minutes)

### Issue A: "Listening" but Connection Refused

**Symptoms:**

- LiteLLM shows "Listening on port 4000"
- `curl http://localhost:4000/health` fails with connection refused

**Diagnostic Steps:**

```cmd
:: 1. Check if port is actually bound
netstat -ano | findstr :4000

:: 2. Check Windows Firewall
netsh advfirewall show allprofiles

:: 3. Check Hyper-V port exclusion
netsh interface ipv4 show excludedportrange protocol=tcp

:: 4. Try different host
python -m litellm --config proxy_server_config.yaml --port 4000 --host 0.0.0.0 --debug
```

**Solutions:**

1. Run terminal as Administrator
2. Add firewall rule:
   ```cmd
   netsh advfirewall firewall add rule name="LiteLLM" dir=in action=allow protocol=tcp localport=4000
   ```
3. Use `127.0.0.1` instead of `0.0.0.0`
4. Check if Hyper-V is excluding port 4000

### Issue B: API Key Errors

**Symptoms:**

- 401 Unauthorized
- "Invalid API key" errors

**Diagnostic Steps:**

```cmd
:: 1. Verify key format
echo %GROQ_API_KEY%

:: 2. Test key directly with Groq
curl https://api.groq.com/openai/v1/models -H "Authorization: Bearer %GROQ_API_KEY%"
```

**Solutions:**

1. Verify key at console.groq.com
2. Check for extra spaces/newlines
3. Regenerate key if compromised

### Issue C: Model Not Found

**Symptoms:**

- 404 Not Found
- "Model not found" errors

**Diagnostic Steps:**

```cmd
:: List available models
curl http://localhost:4000/v1/models
```

**Solutions:**

1. Check model name in config matches request
2. Verify model alias is correct:
   - `groq-70b` → `groq/llama-3.3-70b-versatile`
   - `groq-8b` → `groq/llama-3.1-8b-instant`

### Issue D: Rate Limiting

**Symptoms:**

- 429 Too Many Requests
- "Rate limit exceeded" errors

**Solutions:**

1. Check Groq console for rate limits
2. Add rate limiting to config:
   ```yaml
   litellm_params:
     rpm: 30
     tpm: 180000
   ```
3. Implement exponential backoff in client

## Phase 4: Test Complete Flow (5 minutes)

### Step 4.1: Test Chat Completion

```cmd
curl -X POST http://localhost:4000/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\": \"groq-70b\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"
```

**Expected response:**

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "choices": [...]
}
```

### Step 4.2: Test with Different Models

```cmd
:: Test groq-8b
curl -X POST http://localhost:4000/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\": \"groq-8b\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"
```

## Phase 5: Configure for Production (10 minutes)

### Step 5.1: Create Windows Service (Optional)

```cmd
:: Using NSSM (Non-Sucking Service Manager)
nssm install LiteLLM "C:\Python311\python.exe" "-m litellm --config C:\path\to\config.yaml --port 4000"
nssm start LiteLLM
```

### Step 5.2: Configure Environment Persistence

```cmd
:: Set permanent environment variable (Admin)
setx GROQ_API_KEY "gsk_xxx" /M
```

### Step 5.3: Update Firewall Rules

```cmd
:: Add permanent firewall rule (Admin)
netsh advfirewall firewall add rule name="LiteLLM Proxy" dir=in action=allow protocol=tcp localport=4000
netsh advfirewall firewall add rule name="LiteLLM Proxy" dir=out action=allow protocol=tcp localport=4000
```

## Troubleshooting Checklist

- [ ] GROQ_API_KEY environment variable is set
- [ ] Port 4000 is not in use by another process
- [ ] Configuration file exists and is valid YAML
- [ ] Virtual environment is activated (if using)
- [ ] Running terminal as Administrator
- [ ] Windows Firewall allows port 4000
- [ ] Hyper-V is not excluding port 4000
- [ ] Using correct model aliases in requests

## Common Commands Reference

| Task              | Command                                                                                              |
| ----------------- | ---------------------------------------------------------------------------------------------------- |
| Check port        | `netstat -ano \| findstr :4000`                                                                      |
| Kill process      | `taskkill /PID <pid> /F`                                                                             |
| Test health       | `curl http://localhost:4000/health`                                                                  |
| Start debug       | `python -m litellm --config config.yaml --debug`                                                     |
| Check firewall    | `netsh advfirewall show allprofiles`                                                                 |
| Add firewall rule | `netsh advfirewall firewall add rule name="LiteLLM" dir=in action=allow protocol=tcp localport=4000` |

## Escalation Path

1. **Self-Service**: Check this workflow and REFERENCE.md
2. **Logs**: Enable `--debug` and `--detailed_debug` flags
3. **Community**: GitHub Issues - github.com/BerriAI/litellm
4. **Groq Support**: console.groq.com/support

## Related Documentation

- [SKILL.md](./SKILL.md) - Main skill documentation
- [REFERENCE.md](./REFERENCE.md) - Error code reference
- [CHECKLIST.md](./CHECKLIST.md) - Pre-flight checklist
