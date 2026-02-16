# LiteLLM Error Code Reference

## HTTP Status Codes

### 400 Bad Request

**Cause**: Malformed request or invalid parameters
**Common Scenarios**:

- Missing required fields in request body
- Invalid model name format
- Malformed JSON in request

**Solution**:

```bash
# Verify request format
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "groq-70b", "messages": [{"role": "user", "content": "Hello"}]}'
```

### 401 Unauthorized

**Cause**: Missing or invalid API key
**Common Scenarios**:

- `GROQ_API_KEY` not set
- API key expired or revoked
- API key copied incorrectly (extra spaces, missing characters)

**Solution**:

```cmd
:: Check if environment variable is set
echo %GROQ_API_KEY%

:: Set for current session
set GROQ_API_KEY=gsk_your_key_here

:: Or in PowerShell
$env:GROQ_API_KEY="gsk_your_key_here"
```

### 403 Forbidden

**Cause**: API key valid but lacks permission
**Common Scenarios**:

- Model not available for your tier
- Rate limit exceeded
- Geographic restriction

**Solution**:

- Check Groq console for tier limits
- Verify model availability at console.groq.com

### 404 Not Found

**Cause**: Model or endpoint not found
**Common Scenarios**:

- Model alias not in configuration
- Typo in model name
- Configuration file not loaded

**Solution**:

```yaml
# Verify model is in proxy_server_config.yaml
model_list:
  - model_name: groq-70b
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: os.environ/GROQ_API_KEY
```

### 429 Too Many Requests

**Cause**: Rate limit exceeded
**Common Scenarios**:

- Requests per minute (RPM) limit hit
- Tokens per minute (TPM) limit hit
- Concurrent request limit hit

**Solution**:

```yaml
# Add rate limiting in config
litellm_params:
  model: groq/llama-3.3-70b-versatile
  rpm: 30 # Requests per minute
  tpm: 180000 # Tokens per minute
```

### 500 Internal Server Error

**Cause**: LiteLLM proxy configuration error
**Common Scenarios**:

- Invalid YAML syntax
- Missing required configuration
- Redis connection failure

**Solution**:

```bash
# Run with debug mode
python -m litellm --config proxy_server_config.yaml --debug
```

### 502 Bad Gateway

**Cause**: Upstream provider error
**Common Scenarios**:

- Groq API down
- Network connectivity issues
- DNS resolution failure

**Solution**:

```bash
# Test direct Groq API
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

### 503 Service Unavailable

**Cause**: LiteLLM proxy not running or overloaded
**Common Scenarios**:

- Proxy crashed
- Port not bound
- Too many queued requests

**Solution**:

```cmd
:: Check if proxy is running
netstat -ano | findstr :4000

:: Check health endpoint
curl http://localhost:4000/health
```

## Groq-Specific Errors

### `invalid_api_key`

**Message**: "Invalid API key provided"
**Cause**: GROQ_API_KEY is incorrect format or revoked
**Solution**:

1. Verify key at console.groq.com
2. Check for extra spaces or newlines
3. Regenerate key if compromised

### `model_overloaded`

**Message**: "Model is currently overloaded"
**Cause**: Groq infrastructure at capacity
**Solution**:

```python
# Implement exponential backoff
import time
import random

def retry_with_backoff(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "overloaded" in str(e):
                wait = (2 ** attempt) + random.random()
                time.sleep(wait)
            else:
                raise
```

### `context_length_exceeded`

**Message**: "Context length exceeded"
**Cause**: Input tokens exceed model limit
**Solution**:

- Llama-3.3-70b: 128k context
- Llama-3.1-8b: 128k context
- Reduce prompt size or use chunking

### `rate_limit_exceeded`

**Message**: "Rate limit exceeded"
**Cause**: Too many requests in time window
**Solution**:

- Check limits at console.groq.com
- Implement request queuing
- Use multiple API keys (rotation)

## LiteLLM Proxy Errors

### `ConfigFileNotFound`

**Message**: "Configuration file not found"
**Cause**: Incorrect path to config file
**Solution**:

```bash
# Use absolute path
python -m litellm --config "C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm\proxy_server_config.yaml"
```

### `PortAlreadyInUse`

**Message**: "Port 4000 is already in use"
**Cause**: Another process using port 4000
**Solution**:

```cmd
:: Find process using port
netstat -ano | findstr :4000

:: Kill process (replace PID)
taskkill /PID 12345 /F
```

### `RedisConnectionError`

**Message**: "Could not connect to Redis"
**Cause**: Redis not running or wrong connection string
**Solution**:

```yaml
# Option 1: Comment out Redis settings
# router_settings:
#   routing_strategy: "latency-based-routing"

# Option 2: Start Redis
docker run -d -p 6379:6379 redis
```

### `EnvironmentVariableNotSet`

**Message**: "Environment variable GROQ_API_KEY not set"
**Cause**: os.environ/GROQ_API_KEY referenced but not set
**Solution**:

```cmd
:: Windows CMD
set GROQ_API_KEY=gsk_xxx

:: PowerShell
$env:GROQ_API_KEY="gsk_xxx"

:: Or create .env file
echo GROQ_API_KEY=gsk_xxx > .env
```

## Windows-Specific Errors

### `WinError 10013`

**Message**: "An attempt was made to access a socket in a way forbidden by its access permissions"
**Cause**: Windows Firewall or port exclusion
**Solution**:

```cmd
:: Run as Administrator
netsh advfirewall firewall add rule name="LiteLLM" dir=in action=allow protocol=tcp localport=4000

:: Check Hyper-V port exclusion
netsh interface ipv4 show excludedportrange protocol=tcp
```

### `WinError 10048`

**Message**: "Address already in use"
**Cause**: Port already bound by another process
**Solution**:

```cmd
:: Find and kill process
netstat -ano | findstr :4000
taskkill /PID <PID> /F
```

### `WinError 10061`

**Message**: "No connection could be made because the target machine actively refused it"
**Cause**: Service not listening on port
**Solution**:

- Verify LiteLLM is running
- Check if using correct host (127.0.0.1 vs 0.0.0.0)
- Verify firewall allows connection

## Kilo Code / Groq Provider Errors

### Model Name Errors

**Incorrect**: `z-ai/glm-5:free`
**Correct**: Check Kilo Code model list for available models

### Connection Timeout

**Cause**: Network latency or proxy issues
**Solution**:

```yaml
# Increase timeout in config
litellm_params:
  timeout: 120 # seconds
```

## Error Diagnosis Flowchart

```
Error Occurred
      │
      ├─► HTTP 401/403 ──► Check API Key
      │
      ├─► HTTP 404 ──► Check Model Name in Config
      │
      ├─► HTTP 429 ──► Implement Rate Limiting
      │
      ├─► HTTP 500 ──► Check Config Syntax
      │
      ├─► HTTP 502/503 ──► Check Provider Status
      │
      ├─► Connection Refused ──► Check Port Binding
      │
      └─► Timeout ──► Increase Timeout / Check Network
```

## Logging and Debugging

### Enable Debug Logging

```bash
# Command line
python -m litellm --config config.yaml --debug

# Environment variable
set LITELLM_LOG=DEBUG
```

### Log Locations

- Windows: `%TEMP%\litellm\`
- Linux/Mac: `/tmp/litellm/`

### Verbose Output

```bash
python -m litellm --config config.yaml --port 4000 --host 127.0.0.1 --debug --detailed_debug
```

## Related Documentation

- [SKILL.md](./SKILL.md) - Main skill documentation
- [WORKFLOW.md](./WORKFLOW.md) - Step-by-step debugging workflow
- [CHECKLIST.md](./CHECKLIST.md) - Pre-flight checklist
