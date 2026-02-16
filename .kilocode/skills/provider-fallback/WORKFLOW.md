# Provider Fallback Workflow

## Overview

Detailed workflow for managing fallback between LiteLLM/Groq and Kilo Code providers.

## Phase 1: Detection (1 minute)

### Step 1.1: Health Check

```cmd
:: Test LiteLLM health endpoint
curl http://localhost:4000/health

:: Expected response
{"status": "healthy"}

:: If no response or error, proceed to Step 1.2
```

### Step 1.2: Error Classification

Identify the error type:

| Error               | Classification | Action   |
| ------------------- | -------------- | -------- |
| Connection refused  | Network        | Phase 2A |
| 401 Unauthorized    | Auth           | Phase 2B |
| 429 Rate Limited    | Rate           | Phase 2C |
| 404 Model Not Found | Config         | Phase 2D |
| 500 Internal Error  | Server         | Phase 2E |
| Timeout             | Performance    | Phase 2F |

## Phase 2: Diagnosis (2-5 minutes)

### Phase 2A: Network Issues

```cmd
:: Check if LiteLLM is running
netstat -ano | findstr :4000

:: If no output, LiteLLM is not running
:: Start LiteLLM
cd "C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm"
python -m litellm --config proxy_server_config.yaml --port 4000 --host 127.0.0.1

:: Check firewall
netsh advfirewall firewall show rule name="LiteLLM"

:: If no rule exists, add it
netsh advfirewall firewall add rule name="LiteLLM" dir=in action=allow protocol=tcp localport=4000
```

### Phase 2B: Authentication Issues

```cmd
:: Check if API key is set
echo %GROQ_API_KEY%

:: If empty or shows variable name, set it
set GROQ_API_KEY=gsk_your_key_here

:: Verify key is valid
curl https://api.groq.com/openai/v1/models -H "Authorization: Bearer %GROQ_API_KEY%"
```

### Phase 2C: Rate Limiting

```cmd
:: Wait 60 seconds for rate limit reset
timeout /t 60

:: Or switch to fallback immediately
:: Proceed to Phase 3
```

### Phase 2D: Model Configuration

```cmd
:: Check available models
curl http://localhost:4000/v1/models

:: Verify model name in config
type "C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm\proxy_server_config.yaml"
```

### Phase 2E: Server Errors

```cmd
:: Check LiteLLM logs
:: Run with debug flag
python -m litellm --config proxy_server_config.yaml --debug

:: Check for Python errors
python -c "import litellm; print(litellm.__version__)"
```

### Phase 2F: Timeout Issues

```cmd
:: Increase timeout in request
:: Or check network latency
ping api.groq.com
```

## Phase 3: Fallback Activation (Immediate)

### Step 3.1: Switch to Kilo Code

If diagnosis fails or takes too long:

1. **Update Agent Configuration**

   ```json
   // .kilocode/kilocode.json
   {
     "provider": "z-ai",
     "model": "glm-5:free"
   }
   ```

2. **Log Fallback Event**

   ```
   [2026-02-13T03:00:00Z] FALLBACK: LiteLLM connection refused, switched to Kilo Code
   ```

3. **Continue Operation**
   - All subsequent requests use Kilo Code
   - No interruption to user workflow

### Step 3.2: Verify Fallback Works

```cmd
:: Test Kilo Code is working
:: In VS Code, use Kilo Code extension
:: Or test via CLI if available
```

## Phase 4: Primary Restoration (5-10 minutes)

### Step 4.1: Fix Underlying Issue

Based on diagnosis from Phase 2:

**Network Issues:**

- Restart LiteLLM with correct config
- Add firewall rules
- Check port availability

**Authentication Issues:**

- Set correct API key
- Verify at console.groq.com
- Regenerate if compromised

**Rate Limiting:**

- Wait for reset
- Implement request queuing
- Add rate limiting to config

**Configuration Issues:**

- Fix model names
- Update config file
- Restart LiteLLM

**Server Errors:**

- Update LiteLLM package
- Check Python dependencies
- Review error logs

**Timeout Issues:**

- Increase timeout values
- Check network stability
- Consider caching

### Step 4.2: Test Primary

```cmd
:: Start LiteLLM
cd "C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm"
python -m litellm --config proxy_server_config.yaml --port 4000 --host 127.0.0.1

:: Test health
curl http://localhost:4000/health

:: Test completion
curl -X POST http://localhost:4000/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\": \"groq-70b\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"
```

### Step 4.3: Switch Back to Primary

1. **Update Agent Configuration**

   ```json
   // .gemini/GEMINI.md or equivalent
   {
     "provider": "litellm",
     "endpoint": "http://localhost:4000",
     "model": "groq-70b"
   }
   ```

2. **Log Restoration Event**

   ```
   [2026-02-13T03:15:00Z] RESTORED: LiteLLM recovered, switched back to primary
   ```

3. **Verify Operation**
   - Test with simple prompt
   - Confirm response quality
   - Monitor for issues

## Phase 5: Prevention (Ongoing)

### Step 5.1: Implement Monitoring

```python
# health_monitor.py
import requests
import time
import logging

logging.basicConfig(filename='fallback-events.log', level=logging.INFO)

def check_litellm_health():
    try:
        response = requests.get("http://localhost:4000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def monitor_loop(interval=60):
    while True:
        if not check_litellm_health():
            logging.warning(f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ')}] LiteLLM health check failed")
        time.sleep(interval)

if __name__ == "__main__":
    monitor_loop()
```

### Step 5.2: Add Auto-Recovery

```python
# auto_recovery.py
import subprocess
import time

def start_litellm():
    subprocess.Popen([
        "python", "-m", "litellm",
        "--config", "proxy_server_config.yaml",
        "--port", "4000",
        "--host", "127.0.0.1"
    ], cwd=r"C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm")

def auto_recover():
    if not check_litellm_health():
        logging.info("Attempting auto-recovery...")
        start_litellm()
        time.sleep(10)  # Wait for startup
        if check_litellm_health():
            logging.info("Auto-recovery successful")
        else:
            logging.error("Auto-recovery failed, manual intervention required")
```

### Step 5.3: Document Issues

Keep track of recurring issues:

| Date       | Issue        | Resolution   | Frequency |
| ---------- | ------------ | ------------ | --------- |
| 2026-02-13 | Port binding | Run as Admin | 2x        |
| ...        | ...          | ...          | ...       |

## Decision Tree

```
LiteLLM Request
       │
       ▼
   Health Check
       │
   ┌───┴───┐
   │       │
  OK      Fail
   │       │
   ▼       ▼
Continue  Diagnose
           │
     ┌─────┼─────┐
     │     │     │
  Quick  Complex Unknown
  Fix    Issue   Issue
     │     │     │
     ▼     ▼     ▼
  Retry  Fallback Fallback
     │
  ┌──┴──┐
  │     │
 OK    Fail
  │     │
  ▼     ▼
Continue Fallback
```

## Phase 6: Production Deployment Workflows

### Step 6.1: Pre-Deployment Health Check

```cmd
:: Run comprehensive health check before deployment
curl -s http://localhost:4000/health || echo "LiteLLM not available"

:: Check all provider endpoints
curl -s https://api.groq.com/openai/v1/models -H "Authorization: Bearer %GROQ_API_KEY%" | findstr "data"
curl -s https://openrouter.ai/api/v1/models -H "Authorization: Bearer %OPENROUTER_API_KEY%" | findstr "id"
```

### Step 6.2: Deployment with Fallback Ready

```yaml
# .github/workflows/deploy-with-fallback.yml
name: Deploy with Fallback
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Check Primary Provider
        id: health
        run: |
          if curl -s --max-time 5 http://localhost:4000/health | grep -q "healthy"; then
            echo "provider=litellm" >> $GITHUB_OUTPUT
          else
            echo "provider=kilo-code" >> $GITHUB_OUTPUT
          fi

      - name: Deploy with Provider
        run: |
          echo "Deploying using ${{ steps.health.outputs.provider }}"
          # Continue deployment with selected provider
```

### Step 6.3: Post-Deployment Verification

```python
# post_deploy_check.py
import requests
import sys

def verify_providers():
    """Verify all providers are accessible after deployment."""
    results = {
        'litellm': check_litellm(),
        'groq': check_groq(),
        'openrouter': check_openrouter()
    }

    healthy = [k for k, v in results.items() if v]
    if len(healthy) < 2:
        print(f"WARNING: Only {len(healthy)} providers healthy: {healthy}")
        sys.exit(1)
    print(f"✅ {len(healthy)} providers healthy: {healthy}")

def check_litellm():
    try:
        r = requests.get("http://localhost:4000/health", timeout=5)
        return r.status_code == 200
    except:
        return False

def check_groq():
    try:
        r = requests.get("https://api.groq.com/openai/v1/models", timeout=10)
        return r.status_code == 200
    except:
        return False

def check_openrouter():
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        return r.status_code == 200
    except:
        return False

if __name__ == "__main__":
    verify_providers()
```

## Phase 7: Emergency Fallback Procedures

### Step 7.1: Immediate Fallback (All Providers Failing)

```cmd
:: Emergency: All providers failing - use cached responses
:: 1. Check if offline mode is available
echo "Checking offline capabilities..."

:: 2. Enable degraded mode
set PROVIDER_FALLBACK_MODE=degraded
set PROVIDER_CACHE_TTL=3600

:: 3. Log emergency event
echo [%DATE% %TIME%] EMERGENCY: All providers failed, entering degraded mode >> fallback-events.log
```

### Step 7.2: Provider Recovery Priority

| Priority | Provider              | Recovery Time | Action                     |
| -------- | --------------------- | ------------- | -------------------------- |
| P1       | LiteLLM (local)       | 1-2 min       | Restart service            |
| P2       | Kilo Code (extension) | Immediate     | Already available          |
| P3       | OpenRouter            | 2-5 min       | Check API status           |
| P4       | Direct Groq           | 5-10 min      | Check API key, rate limits |

### Step 7.3: Emergency Communication Template

```markdown
## Provider Outage Report

**Date**: [TIMESTAMP]
**Severity**: [Critical/High/Medium]
**Affected Providers**: [List]

### Current Status

- Primary (LiteLLM): [Status]
- Fallback (Kilo Code): [Status]
- Tertiary (OpenRouter): [Status]

### Impact

- [ ] Development workflow affected
- [ ] CI/CD pipeline affected
- [ ] Production deployment affected

### Mitigation

- Current active provider: [Provider]
- Estimated recovery: [Time]

### Next Steps

1. [Action 1]
2. [Action 2]
3. [Action 3]
```

## Phase 8: Monitoring Integration Workflows

### Step 8.1: Prometheus Metrics Export

```python
# metrics_exporter.py
from prometheus_client import Counter, Gauge, Histogram, start_http_server
import time

# Define metrics
FALLBACK_EVENTS = Counter(
    'provider_fallback_events_total',
    'Total number of fallback events',
    ['from_provider', 'to_provider', 'reason']
)

PROVIDER_HEALTH = Gauge(
    'provider_health_status',
    'Health status of each provider (1=healthy, 0=unhealthy)',
    ['provider']
)

REQUEST_LATENCY = Histogram(
    'provider_request_latency_seconds',
    'Request latency by provider',
    ['provider']
)

def record_fallback(from_provider, to_provider, reason):
    """Record a fallback event."""
    FALLBACK_EVENTS.labels(
        from_provider=from_provider,
        to_provider=to_provider,
        reason=reason
    ).inc()

def update_health(provider, is_healthy):
    """Update provider health gauge."""
    PROVIDER_HEALTH.labels(provider=provider).set(1 if is_healthy else 0)

def observe_latency(provider, latency):
    """Observe request latency."""
    REQUEST_LATENCY.labels(provider=provider).observe(latency)

# Start metrics server on port 9090
if __name__ == "__main__":
    start_http_server(9090)
    print("Metrics available at http://localhost:9090/metrics")
    while True:
        time.sleep(60)
```

### Step 8.2: Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "Provider Fallback Monitoring",
    "panels": [
      {
        "title": "Provider Health Status",
        "type": "stat",
        "targets": [
          {
            "expr": "provider_health_status",
            "legendFormat": "{{provider}}"
          }
        ]
      },
      {
        "title": "Fallback Events (24h)",
        "type": "graph",
        "targets": [
          {
            "expr": "increase(provider_fallback_events_total[24h])",
            "legendFormat": "{{from_provider}} → {{to_provider}}"
          }
        ]
      },
      {
        "title": "Request Latency",
        "type": "heatmap",
        "targets": [
          {
            "expr": "rate(provider_request_latency_seconds_bucket[5m])",
            "legendFormat": "{{provider}}"
          }
        ]
      }
    ]
  }
}
```

### Step 8.3: Alertmanager Rules

```yaml
# alertmanager_rules.yml
groups:
  - name: provider_fallback
    rules:
      - alert: ProviderDown
        expr: provider_health_status == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: 'Provider {{ $labels.provider }} is down'
          description: 'Provider has been unhealthy for more than 1 minute'

      - alert: HighFallbackRate
        expr: increase(provider_fallback_events_total[1h]) > 5
        labels:
          severity: warning
        annotations:
          summary: 'High fallback rate detected'
          description: '{{ $value }} fallback events in the last hour'

      - alert: AllProvidersDown
        expr: sum(provider_health_status) == 0
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: 'All providers are down'
          description: 'No healthy providers available'
```

## Phase 9: Cost Optimization Workflows

### Step 9.1: Daily Cost Check

```python
# cost_monitor.py
import os
from datetime import datetime, timedelta
from typing import Dict, List

# Cost limits (USD)
MONTHLY_BUDGET = 20.0
DAILY_WARNING_THRESHOLD = 0.67  # $20/30 days

class CostMonitor:
    def __init__(self, log_file: str = "provider_costs.log"):
        self.log_file = log_file
        self.costs = self._load_costs()

    def _load_costs(self) -> Dict[str, float]:
        """Load costs from log file."""
        costs = {'total': 0.0, 'by_provider': {}}
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    if '$' in line:
                        # Parse cost from log line
                        parts = line.strip().split()
                        for part in parts:
                            if part.startswith('$'):
                                cost = float(part.replace('$', ''))
                                costs['total'] += cost
        except FileNotFoundError:
            pass
        return costs

    def check_budget(self) -> Dict:
        """Check if approaching budget limits."""
        remaining = MONTHLY_BUDGET - self.costs['total']
        percent_used = (self.costs['total'] / MONTHLY_BUDGET) * 100

        return {
            'total_spent': self.costs['total'],
            'remaining': remaining,
            'percent_used': percent_used,
            'status': self._get_status(percent_used)
        }

    def _get_status(self, percent: float) -> str:
        """Get budget status."""
        if percent >= 100:
            return 'EXCEEDED'
        elif percent >= 90:
            return 'CRITICAL'
        elif percent >= 75:
            return 'WARNING'
        else:
            return 'OK'

    def should_kill_switch(self) -> bool:
        """Check if kill-switch should be activated."""
        return self.costs['total'] >= MONTHLY_BUDGET

# Usage
if __name__ == "__main__":
    monitor = CostMonitor()
    status = monitor.check_budget()
    print(f"Budget Status: {status['status']}")
    print(f"Spent: ${status['total_spent']:.2f}")
    print(f"Remaining: ${status['remaining']:.2f}")

    if monitor.should_kill_switch():
        print("⚠️ KILL-SWITCH: Budget exceeded, switching to free providers only")
```

### Step 9.2: Provider Cost Comparison

```python
# provider_costs.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProviderCost:
    """Provider cost structure."""
    name: str
    input_cost_per_1k: float  # USD per 1K tokens
    output_cost_per_1k: float
    is_free: bool = False

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a request."""
        if self.is_free:
            return 0.0
        return (
            (input_tokens / 1000) * self.input_cost_per_1k +
            (output_tokens / 1000) * self.output_cost_per_1k
        )

# Provider cost definitions
PROVIDERS = {
    'groq-70b': ProviderCost('groq-70b', 0.0, 0.0, is_free=True),  # Free tier
    'groq-8b': ProviderCost('groq-8b', 0.0, 0.0, is_free=True),
    'kilo-code': ProviderCost('kilo-code', 0.0, 0.0, is_free=True),
    'openrouter-free': ProviderCost('openrouter-free', 0.0, 0.0, is_free=True),
    'gemini-pro': ProviderCost('gemini-pro', 0.00125, 0.005, is_free=False),
    'gpt-4': ProviderCost('gpt-4', 0.03, 0.06, is_free=False),
}

def select_cost_effective_provider(task_type: str, budget_remaining: float) -> str:
    """Select the most cost-effective provider for a task."""
    # Free providers first
    free_providers = [p for p, c in PROVIDERS.items() if c.is_free]

    if free_providers:
        # Prefer based on task type
        if task_type in ['coding', 'implementation']:
            return 'kilo-code' if 'kilo-code' in free_providers else free_providers[0]
        elif task_type in ['research', 'analysis']:
            return 'groq-70b' if 'groq-70b' in free_providers else free_providers[0]
        return free_providers[0]

    # If no free providers, check budget
    if budget_remaining > 0:
        return 'gemini-pro'  # Cheapest paid option

    raise RuntimeError("No providers available within budget")
```

### Step 9.3: Budget Kill-Switch Implementation

```python
# kill_switch.py
import os
import json
from datetime import datetime
from pathlib import Path

class BudgetKillSwitch:
    """Emergency budget control."""

    def __init__(self, config_path: str = ".kilocode/provider-config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.triggered = False

    def _load_config(self) -> dict:
        """Load provider configuration."""
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())
        return {
            'budget_limit': 20.0,
            'current_spend': 0.0,
            'kill_switch_active': False,
            'allowed_providers': ['kilo-code', 'groq', 'openrouter-free']
        }

    def check_and_activate(self, current_spend: float) -> bool:
        """Check budget and activate kill-switch if needed."""
        if current_spend >= self.config['budget_limit']:
            self._activate_kill_switch()
            return True
        return False

    def _activate_kill_switch(self):
        """Activate kill-switch - restrict to free providers only."""
        self.triggered = True
        self.config['kill_switch_active'] = True
        self.config['allowed_providers'] = [
            'kilo-code',
            'groq-free',
            'openrouter-free'
        ]
        self._save_config()
        self._log_activation()

    def _save_config(self):
        """Save updated configuration."""
        self.config_path.write_text(json.dumps(self.config, indent=2))

    def _log_activation(self):
        """Log kill-switch activation."""
        log_entry = f"[{datetime.now().isoformat()}] KILL-SWITCH ACTIVATED - Budget exceeded\n"
        with open("cost-alerts.log", "a") as f:
            f.write(log_entry)

    def get_allowed_providers(self) -> list:
        """Get list of allowed providers."""
        return self.config.get('allowed_providers', [])

# Integration example
if __name__ == "__main__":
    kill_switch = BudgetKillSwitch()

    # Check before each request
    current_spend = 18.50  # Get from cost tracker
    if kill_switch.check_and_activate(current_spend):
        print("⚠️ Kill-switch activated! Only free providers available.")
        print(f"Allowed providers: {kill_switch.get_allowed_providers()}")
```

## Phase 10: Windows-Specific Workflows

### Step 10.1: Windows Service Management

```powershell
# manage_litellm_service.ps1
# Run as Administrator

$serviceName = "LiteLLM"
$pythonPath = "C:\Python311\python.exe"
$litellmPath = "C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm"
$configFile = "proxy_config.yaml"

function Start-LiteLLM {
    Write-Host "Starting LiteLLM service..."
    Start-Process -FilePath $pythonPath -ArgumentList @(
        "-m", "litellm",
        "--config", $configFile,
        "--port", "4000",
        "--host", "127.0.0.1"
    ) -WorkingDirectory $litellmPath -WindowStyle Hidden

    Start-Sleep -Seconds 5
    if (Test-Connection -ComputerName localhost -Port 4000 -Quiet) {
        Write-Host "✅ LiteLLM started successfully"
    } else {
        Write-Host "❌ LiteLLM failed to start"
    }
}

function Stop-LiteLLM {
    Write-Host "Stopping LiteLLM..."
    Get-Process -Name python -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowTitle -like "*litellm*" } |
        Stop-Process -Force
    Write-Host "LiteLLM stopped"
}

function Test-LiteLLM {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:4000/health" -TimeoutSec 5
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

# Main
switch ($args[0]) {
    "start" { Start-LiteLLM }
    "stop" { Stop-LiteLLM }
    "status" {
        if (Test-LiteLLM) {
            Write-Host "✅ LiteLLM is running"
        } else {
            Write-Host "❌ LiteLLM is not running"
        }
    }
    default { Write-Host "Usage: .\manage_litellm_service.ps1 [start|stop|status]" }
}
```

### Step 10.2: Windows Firewall Configuration

```powershell
# configure_firewall.ps1
# Run as Administrator

# Add firewall rule for LiteLLM
New-NetFirewallRule -DisplayName "LiteLLM Proxy" `
    -Direction Inbound `
    -LocalPort 4000 `
    -Protocol TCP `
    -Action Allow `
    -Profile Private

# Verify rule
Get-NetFirewallRule -DisplayName "LiteLLM Proxy" | Format-List

# Test connectivity
Test-NetConnection -ComputerName localhost -Port 4000
```

### Step 10.3: Windows Task Scheduler Setup

```powershell
# setup_scheduled_task.ps1
# Create a task to start LiteLLM on login

$action = New-ScheduledTaskAction -Execute "C:\Python311\python.exe" `
    -Argument "-m litellm --config proxy_config.yaml --port 4000" `
    -WorkingDirectory "C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm"

$trigger = New-ScheduledTaskTrigger -AtLogon

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopOnIdleEnd `
    -AllowStartIfOnBatteries

Register-ScheduledTask -TaskName "LiteLLM-AutoStart" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -RunLevel Highest

Write-Host "Scheduled task created. LiteLLM will start automatically on login."
```

### Step 10.4: Windows Event Log Integration

```python
# windows_event_logger.py
import win32evtlog
import win32evtlogutil
import win32con
from datetime import datetime

class WindowsEventLogger:
    """Log provider fallback events to Windows Event Log."""

    APP_NAME = "ProviderFallback"
    EVENT_LOG_TYPE = "Application"

    # Event IDs
    EVENT_FALLBACK = 1001
    EVENT_RESTORED = 1002
    EVENT_ERROR = 1003
    EVENT_KILL_SWITCH = 1004

    @staticmethod
    def log_fallback(from_provider: str, to_provider: str, reason: str):
        """Log a fallback event."""
        message = f"Provider fallback: {from_provider} → {to_provider}. Reason: {reason}"
        win32evtlogutil.ReportEvent(
            WindowsEventLogger.APP_NAME,
            WindowsEventLogger.EVENT_FALLBACK,
            eventCategory=win32con.EVENTLOG_INFORMATION_TYPE,
            strings=[message],
            data=b""
        )

    @staticmethod
    def log_restored(provider: str):
        """Log provider restoration."""
        message = f"Provider restored: {provider}"
        win32evtlogutil.ReportEvent(
            WindowsEventLogger.APP_NAME,
            WindowsEventLogger.EVENT_RESTORED,
            eventCategory=win32con.EVENTLOG_INFORMATION_TYPE,
            strings=[message],
            data=b""
        )

    @staticmethod
    def log_error(error: str):
        """Log an error."""
        win32evtlogutil.ReportEvent(
            WindowsEventLogger.APP_NAME,
            WindowsEventLogger.EVENT_ERROR,
            eventCategory=win32con.EVENTLOG_ERROR_TYPE,
            strings=[error],
            data=b""
        )

# Usage
if __name__ == "__main__":
    WindowsEventLogger.log_fallback("litellm", "kilo-code", "Connection refused")
    WindowsEventLogger.log_restored("litellm")
```

## Quick Reference Card

### Emergency Commands (Windows)

```cmd
:: Check LiteLLM status
curl http://localhost:4000/health

:: Restart LiteLLM
taskkill /F /IM python.exe
cd C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm
start /B python -m litellm --config proxy_config.yaml --port 4000

:: Check firewall
netsh advfirewall firewall show rule name="LiteLLM"

:: View fallback logs
type fallback-events.log | more
```

### Emergency Commands (Linux/WSL)

```bash
# Check LiteLLM status
curl http://localhost:4000/health

# Restart LiteLLM
pkill -f litellm
cd ~/vscodeportable/agentic/01-agent-frameworks/litellm
nohup python -m litellm --config proxy_config.yaml --port 4000 &

# Check logs
tail -f fallback-events.log
```

## Related Documentation

- [SKILL.md](./SKILL.md) - Main skill documentation
- [REFERENCE.md](./REFERENCE.md) - Error codes and troubleshooting
- [RULES.md](./RULES.md) - Fallback rules and logic
- [../litellm-debug/SKILL.md](../litellm-debug/SKILL.md) - LiteLLM debugging
