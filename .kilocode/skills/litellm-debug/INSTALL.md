# LiteLLM Installation and Configuration Guide

## Overview

This guide provides comprehensive instructions for installing and configuring LiteLLM proxy server for the Antigravity + Groq integration on Windows 11.

## System Requirements

| Requirement | Minimum | Recommended |
| ----------- | ------- | ----------- |
| Python      | 3.9+    | 3.11+       |
| RAM         | 4GB     | 8GB+        |
| CPU Cores   | 2       | 4+          |
| Disk Space  | 1GB     | 2GB+        |

## Installation Methods

### Method 1: pip Installation (Recommended for Windows)

```powershell
# Create virtual environment
cd C:\Users\pavel\vscodeportable\agentic\litellm
python -m venv .venv

# Activate virtual environment (PowerShell)
.\.venv\Scripts\Activate.ps1

# Install LiteLLM with proxy support
pip install 'litellm[proxy]'

# Verify installation
litellm --version
```

### Method 2: Docker Installation (Alternative)

```powershell
# Pull the latest image
docker pull docker.litellm.ai/berriai/litellm:main-latest

# Run with config
docker run -v ${PWD}/proxy_server_config.yaml:/app/config.yaml -p 4000:4000 docker.litellm.ai/berriai/litellm:main-stable --config /app/config.yaml
```

## Configuration

### Step 1: Create Configuration File

Create `proxy_server_config.yaml` in your LiteLLM directory:

```yaml
model_list:
  # Groq Models
  - model_name: groq-70b
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: os.environ/GROQ_API_KEY
    model_info:
      max_tokens: 8192
      input_cost_per_token: 0.00000059
      output_cost_per_token: 0.00000079

  - model_name: groq-8b
    litellm_params:
      model: groq/llama-3.1-8b-instant
      api_key: os.environ/GROQ_API_KEY
    model_info:
      max_tokens: 8192
      input_cost_per_token: 0.0
      output_cost_per_token: 0.0

router_settings:
  routing_strategy: 'simple-shuffle'
  num_retries: 3
  timeout: 60

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL

litellm_settings:
  drop_params: true
  set_verbose: true
```

### Step 2: Set Environment Variables

Create `.env` file in the same directory:

```env
# Required API Keys
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# LiteLLM Configuration
LITELLM_MASTER_KEY=sk-your-master-key
LITELLM_SALT_KEY=sk-your-salt-key

# Optional Database (for persistence)
DATABASE_URL=postgresql://user:pass@localhost:5432/litellm

# Redis (for caching/routing)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Step 3: Load Environment Variables

```powershell
# In PowerShell, load environment variables
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=')
    Set-Item -Path "env:$name" -Value $value
}
```

## Starting the Proxy

### Windows-Specific Configuration

**CRITICAL**: Windows has specific port binding requirements. Use these commands:

```powershell
# Run as Administrator!
# Kill any stuck processes on port 4000
netstat -ano | findstr :4000
# If any process found, kill it:
# taskkill /PID <PID> /F

# Start LiteLLM with explicit host binding
litellm --config proxy_server_config.yaml --port 4000 --host 127.0.0.1
```

### Alternative: Use 0.0.0.0 for External Access

```powershell
# Add firewall rule first (run as Administrator)
netsh advfirewall firewall add rule name="LiteLLM" dir=in action=allow protocol=tcp localport=4000

# Start with external binding
litellm --config proxy_server_config.yaml --port 4000 --host 0.0.0.0
```

### Debug Mode

```powershell
# Start with detailed debugging
litellm --config proxy_server_config.yaml --port 4000 --host 127.0.0.1 --detailed_debug
```

## Verification

### Step 1: Check Health Endpoint

```powershell
# In a new PowerShell window
curl http://localhost:4000/health
# Expected: {"status": "healthy"}
```

### Step 2: Test Model List

```powershell
curl http://localhost:4000/v1/models
```

### Step 3: Test Chat Completion

```powershell
curl --location 'http://localhost:4000/chat/completions' --header 'Content-Type: application/json' --data '{
    "model": "groq-70b",
    "messages": [{"role": "user", "content": "Hello, are you working?"}]
}'
```

## Windows-Specific Troubleshooting

### Issue 1: Port Binding Fails Silently

**Symptoms**: LiteLLM says "Listening on port 4000" but connection refused.

**Solutions**:

1. **Run as Administrator**: Right-click PowerShell → "Run as Administrator"

2. **Check Hyper-V Port Exclusion**:

   ```powershell
   netsh interface ipv4 show excludedportrange protocol=tcp
   ```

   If 4000 is in excluded range, either:
   - Use a different port (e.g., 4001)
   - Disable Hyper-V dynamic ports: `netsh int ipv4 set dynamicport tcp start=49152 num=16384`

3. **Check Windows Firewall**:

   ```powershell
   # Allow port 4000
   netsh advfirewall firewall add rule name="LiteLLM" dir=in action=allow protocol=tcp localport=4000
   netsh advfirewall firewall add rule name="LiteLLM" dir=out action=allow protocol=tcp localport=4000
   ```

4. **Use 127.0.0.1 Instead of 0.0.0.0**:
   ```powershell
   litellm --config proxy_server_config.yaml --port 4000 --host 127.0.0.1
   ```

### Issue 2: Connection Refused (WinError 10061)

**Solutions**:

1. Verify proxy is running: `netstat -ano | findstr :4000`
2. Check if Python is listening: `Get-Process -Name python*`
3. Test with localhost: `curl http://127.0.0.1:4000/health`

### Issue 3: Permission Denied (WinError 10013)

**Solutions**:

1. Run PowerShell as Administrator
2. Check antivirus software blocking
3. Verify port is not reserved:
   ```powershell
   netsh interface ipv4 show excludedportrange protocol=tcp
   ```

### Issue 4: Address Already in Use (WinError 10048)

**Solutions**:

1. Find and kill process:

   ```powershell
   netstat -ano | findstr :4000
   taskkill /PID <PID> /F
   ```

2. Or use different port:
   ```powershell
   litellm --config proxy_server_config.yaml --port 4001
   ```

## Production Configuration

### Using PM2 (Process Manager)

```powershell
# Install PM2
npm install -g pm2

# Create ecosystem.config.js
# ecosystem.config.js content:
module.exports = {
  apps: [{
    name: 'litellm-proxy',
    script: 'litellm',
    args: '--config proxy_server_config.yaml --port 4000 --host 127.0.0.1',
    cwd: 'C:/Users/pavel/vscodeportable/agentic/litellm',
    interpreter: 'none',
    env: {
      GROQ_API_KEY: 'your_key',
      LITELLM_MASTER_KEY: 'your_master_key'
    }
  }]
}

# Start with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save
pm2-startup install
```

### Using Windows Service (NSSM)

```powershell
# Download NSSM from https://nssm.cc/download
# Install as service
nssm install LiteLLM "C:\Users\pavel\vscodeportable\agentic\litellm\.venv\Scripts\litellm.exe"
nssm set LiteLLM AppParameters "--config proxy_server_config.yaml --port 4000"
nssm set LiteLLM AppDirectory "C:\Users\pavel\vscodeportable\agentic\litellm"
nssm set LiteLLM AppEnvironmentExtra "GROQ_API_KEY=your_key"

# Start service
nssm start LiteLLM
```

## Integration with Antigravity (OpenCode CLI)

### Configure OpenCode to Use LiteLLM

Update your OpenCode configuration to point to LiteLLM:

```json
{
  "provider": "openai",
  "api_base": "http://localhost:4000/v1",
  "api_key": "your_litellm_master_key",
  "model": "groq-70b"
}
```

### Fallback Configuration

When LiteLLM is unavailable, configure fallback to Kilo Code:

```json
{
  "providers": {
    "primary": {
      "name": "litellm",
      "api_base": "http://localhost:4000/v1",
      "model": "groq-70b"
    },
    "fallback": {
      "name": "kilocode",
      "model": "z-ai/glm-5:free"
    }
  }
}
```

## Monitoring and Logging

### Enable Detailed Logging

```powershell
litellm --config proxy_server_config.yaml --port 4000 --detailed_debug
```

### Log File Location

Default log location: `~/.litellm/logs/`

Custom log location:

```powershell
export LITELLM_LOG_DIR="C:/Users/pavel/vscodeportable/agentic/litellm/logs"
```

### Health Check Script

Create `health_check.ps1`:

```powershell
#!/usr/bin/env pwsh
$HEALTH_URL = "http://localhost:4000/health"
$MAX_RETRIES = 3
$RETRY_DELAY = 5

for ($i = 1; $i -le $MAX_RETRIES; $i++) {
    try {
        $response = Invoke-WebRequest -Uri $HEALTH_URL -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "LiteLLM is healthy"
            exit 0
        }
    } catch {
        Write-Host "Attempt $i failed: $_"
        if ($i -lt $MAX_RETRIES) {
            Start-Sleep -Seconds $RETRY_DELAY
        }
    }
}

Write-Host "LiteLLM health check failed after $MAX_RETRIES attempts"
exit 1
```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Set master key** to protect your proxy
4. **Enable HTTPS** in production
5. **Restrict CORS** to known origins
6. **Use rate limiting** to prevent abuse

## Next Steps

1. Test the proxy with your Antigravity configuration
2. Set up monitoring and alerting
3. Configure fallback to Kilo Code when LiteLLM is unavailable
4. Document any project-specific configurations

## Related Documentation

- [LiteLLM Official Docs](https://docs.litellm.ai/)
- [Groq API Docs](https://console.groq.com/docs)
- [SKILL.md](./SKILL.md) - Debugging skill
- [REFERENCE.md](./REFERENCE.md) - Error code reference
- [WORKFLOW.md](./WORKFLOW.md) - Debugging workflow
