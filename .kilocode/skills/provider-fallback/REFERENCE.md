# Provider Fallback Reference Guide

## Version

- **Version**: 2.0.0
- **Last Updated**: 2026-02-13
- **Author**: Kilo Code System

---

## Table of Contents

1. [Error Code Reference](#error-code-reference)
2. [Troubleshooting Scenarios](#troubleshooting-scenarios)
3. [Diagnostic Commands](#diagnostic-commands)
4. [Recovery Procedures](#recovery-procedures)
5. [Known Issues and Workarounds](#known-issues-and-workarounds)

---

## Error Code Reference

### HTTP Status Codes

| Code    | Description           | Cause                                  | Resolution                                             | Fallback Action                 |
| ------- | --------------------- | -------------------------------------- | ------------------------------------------------------ | ------------------------------- |
| **400** | Bad Request           | Invalid request format, malformed JSON | Check request payload, validate parameters             | Retry with corrected request    |
| **401** | Unauthorized          | Missing or invalid API key             | Verify GROQ_API_KEY in environment, check key validity | Switch to Kilo Code provider    |
| **403** | Forbidden             | API key lacks permissions, IP blocked  | Check API key permissions, verify IP whitelist         | Switch to Kilo Code provider    |
| **404** | Not Found             | Invalid endpoint, model not available  | Verify endpoint URL, check model name spelling         | Try alternative model           |
| **429** | Rate Limited          | Too many requests, quota exceeded      | Wait for rate limit reset (check `retry-after` header) | Immediate fallback to Kilo Code |
| **500** | Internal Server Error | Provider-side error                    | Retry with exponential backoff (max 3 attempts)        | Fallback after 3 failures       |
| **502** | Bad Gateway           | LiteLLM proxy cannot reach upstream    | Check Groq API status, verify network                  | Restart LiteLLM proxy           |
| **503** | Service Unavailable   | Provider temporarily down              | Check provider status page, wait 30s                   | Fallback to Kilo Code           |
| **504** | Gateway Timeout       | Request took too long                  | Reduce request complexity, check network latency       | Fallback to Kilo Code           |

### Connection Errors

| Error Code       | Description           | Cause                                 | Resolution                             | Fallback Action                  |
| ---------------- | --------------------- | ------------------------------------- | -------------------------------------- | -------------------------------- |
| **ECONNREFUSED** | Connection Refused    | LiteLLM proxy not running, wrong port | Start LiteLLM proxy, verify port 4000  | Use direct Groq API or Kilo Code |
| **ETIMEDOUT**    | Connection Timeout    | Network issues, firewall blocking     | Check firewall rules, increase timeout | Fallback to Kilo Code            |
| **ENOTFOUND**    | DNS Resolution Failed | Invalid hostname, DNS issues          | Verify hostname, check DNS settings    | Use IP address or fallback       |
| **ECONNRESET**   | Connection Reset      | Remote server closed connection       | Retry request, check server logs       | Fallback after 2 resets          |
| **EPIPE**        | Broken Pipe           | Connection closed during write        | Retry request                          | Fallback after failure           |

### Provider-Specific Errors

#### Groq API Errors

| Error Code               | Description         | Cause                     | Resolution                              | Fallback Action       |
| ------------------------ | ------------------- | ------------------------- | --------------------------------------- | --------------------- |
| **groq-invalid-api-key** | Invalid API Key     | Wrong or expired API key  | Regenerate key at console.groq.com      | Switch to Kilo Code   |
| **groq-rate-limit**      | Rate Limit Exceeded | Free tier limits hit      | Wait 1 minute, reduce request frequency | Immediate fallback    |
| **groq-model-overload**  | Model Overloaded    | Server capacity exceeded  | Wait 30 seconds, retry                  | Fallback to Kilo Code |
| **groq-context-length**  | Context Too Long    | Input exceeds model limit | Reduce prompt size, use larger model    | Truncate and retry    |
| **groq-invalid-model**   | Model Not Found     | Model name incorrect      | Check available models via API          | Use default model     |

#### Groq Rate Limit Errors (Model-Specific)

| Model                     | Limit Type      | Error Message          | Wait Time  | Fallback Model            |
| ------------------------- | --------------- | ---------------------- | ---------- | ------------------------- |
| `llama-3.1-8b-instant`    | RPM (30/min)    | "Rate limit exceeded"  | 2 seconds  | `z-ai/glm-5:free`         |
| `llama-3.1-8b-instant`    | RPD (14.4K/day) | "Daily quota exceeded" | Next day   | `z-ai/glm-5:free`         |
| `llama-3.1-8b-instant`    | TPM (6K/min)    | "Token limit exceeded" | 10 seconds | `z-ai/glm-5:free`         |
| `llama-3.1-8b-instant`    | TPD (500K/day)  | "Daily token quota"    | Next day   | `z-ai/glm-5:free`         |
| `llama-3.3-70b-versatile` | RPM (30/min)    | "Rate limit exceeded"  | 2 seconds  | `llama-3.1-8b-instant`    |
| `llama-3.3-70b-versatile` | RPD (1K/day)    | "Daily quota exceeded" | Next day   | `llama-3.1-8b-instant`    |
| `llama-3.3-70b-versatile` | TPM (12K/min)   | "Token limit exceeded" | 5 seconds  | `llama-3.1-8b-instant`    |
| `llama-3.3-70b-versatile` | TPD (100K/day)  | "Daily token quota"    | Next day   | `llama-3.1-8b-instant`    |
| `groq/compound`           | RPM (30/min)    | "Rate limit exceeded"  | 2 seconds  | `llama-3.3-70b-versatile` |
| `groq/compound`           | RPD (250/day)   | "Daily quota exceeded" | Next day   | `llama-3.3-70b-versatile` |

#### Groq Rate Limit Handling Strategy

```python
# rate_limit_handler.py
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class GroqRateLimit:
    """Groq rate limit configuration per model."""
    rpm: int          # Requests per minute
    rpd: int          # Requests per day
    tpm: int          # Tokens per minute
    tpd: int          # Tokens per day

GROQ_RATE_LIMITS = {
    "llama-3.1-8b-instant": GroqRateLimit(
        rpm=30, rpd=14400, tpm=6000, tpd=500000
    ),
    "llama-3.3-70b-versatile": GroqRateLimit(
        rpm=30, rpd=1000, tpm=12000, tpd=100000
    ),
    "openai/gpt-oss-120b": GroqRateLimit(
        rpm=30, rpd=1000, tpm=8000, tpd=200000
    ),
    "groq/compound": GroqRateLimit(
        rpm=30, rpd=250, tpm=70000, tpd=None
    ),
}

def get_retry_after(model: str, limit_type: str) -> int:
    """Calculate retry-after time in seconds."""
    limits = GROQ_RATE_LIMITS.get(model)
    if not limits:
        return 60  # Default 1 minute

    if limit_type == "rpm":
        return 2  # Wait 2 seconds for RPM
    elif limit_type == "tpm":
        return 10  # Wait 10 seconds for TPM
    elif limit_type in ("rpd", "tpd"):
        return 3600  # Wait 1 hour for daily limits

    return 60  # Default

def get_fallback_model(model: str) -> str:
    """Get fallback model when rate limited."""
    fallback_chain = {
        "llama-3.3-70b-versatile": "llama-3.1-8b-instant",
        "llama-3.1-8b-instant": "z-ai/glm-5:free",
        "openai/gpt-oss-120b": "llama-3.3-70b-versatile",
        "groq/compound": "llama-3.3-70b-versatile",
    }
    return fallback_chain.get(model, "z-ai/glm-5:free")
```

#### LiteLLM Proxy Errors

| Error Code               | Description           | Cause                        | Resolution                         | Fallback Action            |
| ------------------------ | --------------------- | ---------------------------- | ---------------------------------- | -------------------------- |
| **litellm-config-error** | Configuration Error   | Invalid config.yaml          | Validate YAML syntax, check paths  | Use default config         |
| **litellm-no-models**    | No Models Available   | No models configured         | Add models to config.yaml          | Use direct API calls       |
| **litellm-auth-failed**  | Authentication Failed | Invalid master key           | Check LITELLM_MASTER_KEY env var   | Disable auth for local dev |
| **litellm-port-in-use**  | Port Already in Use   | Another process on port 4000 | Kill existing process, change port | Use different port         |

#### Kilo Code Errors

| Error Code                 | Description       | Cause                          | Resolution                | Fallback Action |
| -------------------------- | ----------------- | ------------------------------ | ------------------------- | --------------- |
| **kilo-extension-error**   | Extension Error   | VS Code extension crashed      | Reload VS Code window     | Use OpenRouter  |
| **kilo-model-unavailable** | Model Unavailable | z-ai/glm-5:free not responding | Check internet connection | Use OpenRouter  |
| **kilo-rate-limit**        | Rate Limited      | Too many requests              | Wait 60 seconds           | Use OpenRouter  |

---

## Troubleshooting Scenarios

### Scenario 1: LiteLLM Proxy Not Starting

**Symptoms:**

- `ECONNREFUSED` when connecting to localhost:4000
- LiteLLM process exits immediately
- Port 4000 not listening

**Diagnostic Steps:**

```powershell
# Check if port 4000 is in use
netstat -ano | findstr :4000

# Check if LiteLLM process exists
tasklist | findstr python

# Try starting LiteLLM manually
python scripts/start_litellm.py

# Check for configuration errors
python -c "import yaml; yaml.safe_load(open('litellm_config.yaml'))"
```

**Resolution:**

1. Kill any process using port 4000:
   ```powershell
   # Find PID using port
   netstat -ano | findstr :4000
   # Kill process (replace PID)
   taskkill /PID <PID> /F
   ```
2. Verify configuration file exists and is valid
3. Check Python environment has required packages:
   ```powershell
   pip install litellm groq
   ```
4. Start LiteLLM with verbose logging:
   ```powershell
   litellm --config litellm_config.yaml --port 4000 --debug
   ```

### Scenario 2: Groq API Rate Limiting

**Symptoms:**

- HTTP 429 responses from Groq API
- "Rate limit exceeded" error messages
- Intermittent failures

**Diagnostic Steps:**

```powershell
# Test Groq API directly
curl -X GET "https://api.groq.com/openai/v1/models" -H "Authorization: Bearer %GROQ_API_KEY%"

# Check rate limit headers (PowerShell)
$headers = Invoke-WebRequest -Uri "https://api.groq.com/openai/v1/models" -Headers @{"Authorization"="Bearer $env:GROQ_API_KEY"} | Select-Object -ExpandProperty Headers
$headers["x-ratelimit-remaining"]
$headers["x-ratelimit-reset"]
```

**Resolution:**

1. Implement exponential backoff in requests
2. Reduce request frequency
3. Use fallback provider during rate limit periods
4. Consider upgrading Groq plan for higher limits

### Scenario 3: Authentication Failures

**Symptoms:**

- HTTP 401 responses
- "Invalid API key" errors
- Sudden authentication failures

**Diagnostic Steps:**

```powershell
# Verify API key is set
echo %GROQ_API_KEY%

# Test API key validity
curl -X GET "https://api.groq.com/openai/v1/models" -H "Authorization: Bearer %GROQ_API_KEY%"

# Check for whitespace issues
python -c "import os; key = os.environ.get('GROQ_API_KEY', ''); print(f'Key length: {len(key)}, First 5 chars: {key[:5]}')"
```

**Resolution:**

1. Verify API key in `.env` file:
   ```powershell
   type .env | findstr GROQ_API_KEY
   ```
2. Regenerate key at https://console.groq.com/keys
3. Update `.env` file with new key
4. Restart LiteLLM proxy to pick up new key

### Scenario 4: Model Not Found Errors

**Symptoms:**

- HTTP 404 responses
- "Model not found" errors
- "Invalid model" messages

**Diagnostic Steps:**

```powershell
# List available Groq models
curl -X GET "https://api.groq.com/openai/v1/models" -H "Authorization: Bearer %GROQ_API_KEY%"

# Check LiteLLM configuration
type litellm_config.yaml | findstr model_name
```

**Resolution:**

1. Verify model name in configuration matches available models
2. Update model name in `litellm_config.yaml`
3. Common Groq model names:
   - `llama-3.3-70b-versatile`
   - `llama-3.1-8b-instant`
   - `mixtral-8x7b-32768`

### Scenario 5: Network Connectivity Issues

**Symptoms:**

- `ETIMEDOUT` errors
- `ENOTFOUND` DNS errors
- Intermittent connection failures

**Diagnostic Steps:**

```powershell
# Test basic connectivity
ping api.groq.com

# Test HTTPS connectivity
curl -I https://api.groq.com

# Check DNS resolution
nslookup api.groq.com

# Test with PowerShell
Test-NetConnection -ComputerName api.groq.com -Port 443
```

**Resolution:**

1. Check firewall rules:
   ```powershell
   # Check Windows Firewall
   netsh advfirewall firewall show rule name=all | findstr 443
   ```
2. Verify proxy settings if applicable
3. Check VPN/Tailscale connectivity
4. Try alternative DNS (8.8.8.8 or 1.1.1.1)

### Scenario 6: Windows-Specific Issues

#### Port Binding Issues

**Symptoms:**

- "Port already in use" errors
- LiteLLM fails to start on port 4000

**Diagnostic Steps:**

```powershell
# Check what's using port 4000
netstat -ano | findstr :4000

# Check for Windows services
Get-Service | Where-Object {$_.DisplayName -like "*python*"}
```

**Resolution:**

1. Exclude port from Hyper-V:
   ```powershell
   # Run as Administrator
   netsh int ipv4 add excludedportrange protocol=tcp startport=4000 numberofports=1
   ```
2. Or use a different port (e.g., 4001)

#### Firewall Blocking

**Symptoms:**

- Connection refused from other machines
- Local connections work, remote don't

**Resolution:**

```powershell
# Add firewall rule for LiteLLM (run as Administrator)
netsh advfirewall firewall add rule name="LiteLLM" dir=in action=allow protocol=tcp localport=4000

# Or disable Windows Firewall temporarily for testing (not recommended for production)
netsh advfirewall set allprofiles state off
```

#### Hyper-V Port Conflicts

**Symptoms:**

- Random ports blocked
- "An attempt was made to access a socket in a way forbidden by its access permissions"

**Resolution:**

```powershell
# Check Hyper-V excluded port ranges
netsh int ipv4 show excludedportrange protocol=tcp

# Reserve port range for applications
netsh int ipv4 set dynamicport tcp start=49152 num=16384

# Exclude specific port for LiteLLM
netsh int ipv4 add excludedportrange protocol=tcp startport=4000 numberofports=1
```

---

## Diagnostic Commands

### Windows CMD/PowerShell Commands

#### Health Checks

```powershell
# Check LiteLLM health endpoint
curl http://localhost:4000/health

# Check Groq API status
curl -X GET "https://api.groq.com/openai/v1/models" -H "Authorization: Bearer $env:GROQ_API_KEY"

# Check Kilo Code extension status (in VS Code)
# Run in VS Code Developer Tools Console:
# vscode.extensions.getExtension('kilo-code.kilo-code')
```

#### Process Management

```powershell
# List Python processes
tasklist | findstr python

# Kill specific process by PID
taskkill /PID <PID> /F

# Kill all Python processes (use with caution)
taskkill /IM python.exe /F

# Start LiteLLM in background
start /B python scripts/start_litellm.py
```

#### Network Diagnostics

```powershell
# Test port connectivity
Test-NetConnection -ComputerName localhost -Port 4000

# Monitor network connections
netstat -ano | findstr ESTABLISHED

# Check listening ports
netstat -ano | findstr LISTENING

# DNS lookup
nslookup api.groq.com
Resolve-DnsName api.groq.com
```

#### Environment Variables

```powershell
# List all environment variables
set

# Check specific variable
echo %GROQ_API_KEY%

# Set environment variable (current session)
set GROQ_API_KEY=your_key_here

# Set environment variable (permanent)
[Environment]::SetEnvironmentVariable("GROQ_API_KEY", "your_key_here", "User")
```

### Log File Locations

| Log Type           | Location                    | Description          |
| ------------------ | --------------------------- | -------------------- |
| LiteLLM Logs       | `./logs/litellm.log`        | LiteLLM proxy output |
| LiteLLM Error Logs | `./logs/litellm_error.log`  | LiteLLM errors       |
| Groq API Logs      | Console output              | Direct API call logs |
| Kilo Code Logs     | VS Code Output Panel        | Extension logs       |
| Windows Event Logs | Event Viewer > Windows Logs | System-level errors  |

### Health Check Endpoints

| Endpoint        | URL                                     | Expected Response         |
| --------------- | --------------------------------------- | ------------------------- |
| LiteLLM Health  | `http://localhost:4000/health`          | `{"status": "healthy"}`   |
| LiteLLM Models  | `http://localhost:4000/v1/models`       | List of available models  |
| Groq API Models | `https://api.groq.com/openai/v1/models` | List of Groq models       |
| Groq API Health | `https://api.groq.com/openai/v1/models` | HTTP 200 with models list |

### Configuration Validation

```powershell
# Validate LiteLLM config YAML
python -c "import yaml; config = yaml.safe_load(open('litellm_config.yaml')); print('Config valid:', bool(config))"

# Validate environment variables
python -c "import os; print('GROQ_API_KEY set:', bool(os.environ.get('GROQ_API_KEY')))"

# Test complete setup
python scripts/verify_groq_litellm.py
```

---

## Recovery Procedures

### Procedure 1: Full Provider Reset

**When to use:** All providers failing, complete system reset needed

**Steps:**

1. Stop all services:

   ```powershell
   taskkill /IM python.exe /F
   ```

2. Clear any cached data:

   ```powershell
   del /Q logs\*.log
   ```

3. Verify environment:

   ```powershell
   type .env | findstr API_KEY
   ```

4. Restart LiteLLM:

   ```powershell
   python scripts/start_litellm.py
   ```

5. Verify health:
   ```powershell
   curl http://localhost:4000/health
   ```

### Procedure 2: Fallback to Kilo Code

**When to use:** LiteLLM/Groq unavailable, need immediate operation

**Steps:**

1. Verify Kilo Code extension is active in VS Code
2. Update configuration to use Kilo Code:
   ```json
   {
     "provider": "kilo-code",
     "model": "z-ai/glm-5:free"
   }
   ```
3. Test with simple request
4. Monitor for rate limits

### Procedure 3: Fallback to OpenRouter

**When to use:** Both LiteLLM and Kilo Code unavailable

**Steps:**

1. Verify OpenRouter API key:

   ```powershell
   echo %OPENROUTER_API_KEY%
   ```

2. Configure OpenRouter:

   ```json
   {
     "provider": "openrouter",
     "model": "minimax/minimax-m2.1:free",
     "endpoint": "https://openrouter.ai/api/v1"
   }
   ```

3. Test connection:
   ```powershell
   curl -X POST "https://openrouter.ai/api/v1/chat/completions" -H "Authorization: Bearer %OPENROUTER_API_KEY%" -H "Content-Type: application/json" -d "{\"model\":\"minimax/minimax-m2.1:free\",\"messages\":[{\"role\":\"user\",\"content\":\"test\"}]}"
   ```

### Procedure 4: Manual Provider Switching

**When to use:** Need to manually control which provider is used

**Steps:**

1. Check current provider status:

   ```python
   from scripts.health_monitor import ProviderHealthMonitor
   monitor = ProviderHealthMonitor(config)
   print(monitor.check_all_providers())
   ```

2. Select provider manually:

   ```python
   # Force use of specific provider
   provider = "kilo-code"  # or "litellm", "openrouter"
   ```

3. Update configuration file with selected provider

### Procedure 5: Configuration Reset

**When to use:** Configuration corrupted, need fresh start

**Steps:**

1. Backup current config:

   ```powershell
   copy litellm_config.yaml litellm_config.yaml.backup
   ```

2. Create minimal config:

   ```yaml
   model_list:
     - model_name: groq-70b
       litellm_params:
         model: groq/llama-3.3-70b-versatile
         api_key: os.environ/GROQ_API_KEY

   general_settings:
     master_key: os.environ/LITELLM_MASTER_KEY
   ```

3. Restart LiteLLM with new config

4. Verify with health check

---

## Known Issues and Workarounds

### Issue 1: LiteLLM Memory Leak

**Description:** LiteLLM proxy slowly consumes more memory over time

**Affected Versions:** LiteLLM < 1.40.0

**Workaround:**

- Restart LiteLLM proxy every 24 hours
- Use PM2 or similar process manager with memory limits:
  ```powershell
  npm install -g pm2
  pm2 start scripts/start_litellm.py --name litellm --max-memory-restart 1G
  ```

**Fix:** Update to LiteLLM >= 1.40.0

### Issue 2: Groq API Intermittent 503

**Description:** Groq API occasionally returns 503 errors during peak hours

**Affected Versions:** All

**Workaround:**

- Implement retry with exponential backoff
- Use fallback provider during peak hours (US business hours)
- Pre-cache common responses

### Issue 3: Windows Port Exclusion Conflicts

**Description:** Hyper-V reserves ports that conflict with LiteLLM default port

**Affected Versions:** Windows 10/11 with Hyper-V enabled

**Workaround:**

- Use port 8080 or 8000 instead of 4000
- Or exclude port before Hyper-V starts (requires registry edit)

**Fix:**

```powershell
# Run at boot before Hyper-V starts
netsh int ipv4 add excludedportrange protocol=tcp startport=4000 numberofports=1
```

### Issue 4: Kilo Code Extension Timeout

**Description:** Kilo Code extension times out on large requests

**Affected Versions:** Kilo Code < 2.0.0

**Workaround:**

- Split large requests into smaller chunks
- Increase timeout in VS Code settings:
  ```json
  {
    "kilo-code.timeout": 120000
  }
  ```

### Issue 5: OpenRouter Rate Limiting

**Description:** OpenRouter free tier has strict rate limits

**Affected Versions:** All

**Workaround:**

- Limit requests to 50 per day
- Use primarily as tertiary fallback
- Monitor usage at https://openrouter.ai/activity

### Issue 6: DNS Cache Issues

**Description:** Stale DNS cache causes connection failures

**Affected Versions:** Windows all versions

**Workaround:**

```powershell
# Flush DNS cache
ipconfig /flushdns

# Or use IP address directly
# api.groq.com -> Use IP from nslookup
```

### Issue 7: Proxy Configuration Interference

**Description:** System proxy settings interfere with API calls

**Affected Versions:** All

**Workaround:**

- Disable proxy for localhost:
  ```powershell
  set NO_PROXY=localhost,127.0.0.1
  ```
- Or configure proxy bypass in Windows Settings

### Issue 8: Antivirus Blocking Python

**Description:** Antivirus software blocks Python network access

**Affected Versions:** Various antivirus products

**Workaround:**

- Add Python executable to antivirus exclusions
- Add project directory to exclusions
- Temporarily disable for testing (not recommended for production)

---

## Quick Reference Card

### Emergency Fallback Sequence

1. **Primary fails** → Try LiteLLM health check
2. **LiteLLM down** → Restart proxy
3. **Restart fails** → Use Kilo Code
4. **Kilo Code fails** → Use OpenRouter
5. **All fail** → Check network, then retry from step 1

### Key Commands

```powershell
# Quick health check
curl http://localhost:4000/health

# Restart LiteLLM
taskkill /IM python.exe /F && python scripts/start_litellm.py

# Check environment
echo %GROQ_API_KEY%

# Test Groq directly
curl -X GET "https://api.groq.com/openai/v1/models" -H "Authorization: Bearer %GROQ_API_KEY%"
```

### Support Resources

| Resource          | URL                                |
| ----------------- | ---------------------------------- |
| Groq Status       | https://status.groq.com            |
| Groq Docs         | https://console.groq.com/docs      |
| LiteLLM Docs      | https://docs.litellm.ai            |
| LiteLLM GitHub    | https://github.com/BerriAI/litellm |
| OpenRouter Status | https://status.openrouter.ai       |

---

## Cross-Reference

For detailed implementation guidance, see:

- [SKILL.md](./SKILL.md) - Main skill documentation
- [`.kilocode/rules-code/cost-optimization.md`](../../rules-code/cost-optimization.md) - Cost optimization rules
- [`.agent/flows/health_monitor.py`](../../../.agent/flows/health_monitor.py) - Health monitoring implementation
