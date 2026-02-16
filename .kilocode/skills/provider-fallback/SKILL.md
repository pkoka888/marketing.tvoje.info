# Provider Fallback Skill

## Description

Comprehensive provider fallback management system for AI agents. Handles seamless switching between LiteLLM/Groq and Kilo Code providers with intelligent health monitoring, priority-based selection, and automated recovery.

## Version

- **Version**: 2.0.0
- **Last Updated**: 2026-02-13
- **Author**: Kilo Code System

---

## Table of Contents

1. [Overview](#overview)
2. [Provider Architecture](#provider-architecture)
3. [Health Monitoring](#health-monitoring)
4. [Fallback Logic](#fallback-logic)
5. [Error Handling](#error-handling)
6. [Metrics Collection](#metrics-collection)
7. [Integration Examples](#integration-examples)
8. [Configuration](#configuration)
9. [Windows-Specific Issues](#windows-specific-issues)
10. [Related Documentation](#related-documentation)

---

## Overview

### Purpose

Ensures continuous operation of AI agents even when external API providers experience issues. Provides intelligent fallback with minimal disruption to user workflow.

### Key Features

- **Real-time Health Monitoring**: Continuous provider health checks
- **Intelligent Fallback Logic**: Priority-based provider selection
- **Seamless Switching**: Zero-disruption provider transitions
- **Comprehensive Error Handling**: Covers all failure scenarios
- **Metrics Collection**: Performance and reliability tracking
- **Auto-Recovery**: Automatic restoration of primary provider

### Supported Providers

| Provider                       | Type     | Priority | Use Case                     |
| ------------------------------ | -------- | -------- | ---------------------------- |
| LiteLLM + Groq                 | Primary  | 1        | Production AI operations     |
| Kilo Code (z-ai/glm-5:free)    | Fallback | 2        | Development, testing, backup |
| OpenRouter (minimax-m2.1:free) | Tertiary | 3        | Extended fallback            |

---

## Provider Architecture

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Request Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │ Agent       │  │ Health      │  │ Metrics             │     │
│  │ Request     │──│ Monitor     │──│ Collector           │     │
│  └──────┬──────┘  └─────────────┘  └─────────────────────┘     │
└─────────┼───────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Fallback Decision Engine                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │ Priority    │  │ Error       │  │ Recovery            │     │
│  │ Selector    │  │ Classifier  │  │ Manager             │     │
│  └──────┬──────┘  └─────────────┘  └─────────────────────┘     │
└─────────┼───────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Provider Layer                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │ Primary     │  │ Fallback    │  │ Tertiary            │     │
│  │ LiteLLM     │  │ Kilo Code   │  │ OpenRouter          │     │
│  │ (Groq)      │  │ (z-ai)      │  │ (minimax)           │     │
│  │ Priority: 1 │  │ Priority: 2 │  │ Priority: 3         │     │
│  └─────────────┘  └─────────────┘  └─────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### Provider Endpoints

| Provider   | Endpoint                  | Models                                                  | Auth Method        |
| ---------- | ------------------------- | ------------------------------------------------------- | ------------------ |
| LiteLLM    | http://localhost:4000     | groq/llama-3.3-70b-versatile, groq/llama-3.1-8b-instant | GROQ_API_KEY       |
| Kilo Code  | VS Code Extension         | z-ai/glm-5:free                                         | Extension Auth     |
| OpenRouter | https://openrouter.ai/api | minimax-m2.1:free                                       | OPENROUTER_API_KEY |

### Groq Model Specifications (Verified 2026-02-13)

| Model ID                  | Speed    | Input Price | Output Price | Context | Use Case              |
| ------------------------- | -------- | ----------- | ------------ | ------- | --------------------- |
| `llama-3.1-8b-instant`    | 560 T/s  | $0.05/1M    | $0.08/1M     | 131K    | Fast, cheap responses |
| `llama-3.3-70b-versatile` | 280 T/s  | $0.59/1M    | $0.79/1M     | 131K    | Complex reasoning     |
| `openai/gpt-oss-120b`     | 500 T/s  | $0.15/1M    | $0.60/1M     | 131K    | OpenAI compatibility  |
| `openai/gpt-oss-20b`      | 1000 T/s | $0.075/1M   | $0.30/1M     | 131K    | Fast OpenAI alt       |
| `groq/compound`           | 450 T/s  | -           | -            | 131K    | Agentic workflows     |
| `groq/compound-mini`      | 450 T/s  | -           | -            | 131K    | Lightweight agents    |

### Groq Rate Limits (Developer Plan)

| Model                     | RPM | RPD    | TPM    | TPD  |
| ------------------------- | --- | ------ | ------ | ---- |
| `llama-3.1-8b-instant`    | 30  | 14,400 | 6,000  | 500K |
| `llama-3.3-70b-versatile` | 30  | 1,000  | 12,000 | 100K |
| `openai/gpt-oss-120b`     | 30  | 1,000  | 8,000  | 200K |
| `openai/gpt-oss-20b`      | 30  | 1,000  | 8,000  | 200K |
| `groq/compound`           | 30  | 250    | 70,000 | -    |
| `groq/compound-mini`      | 30  | 250    | 70,000 | -    |

> **Note**: Rate limits apply at organization level. Cached tokens don't count towards limits.

---

## Health Monitoring

### Health Check Configuration

```python
# health_monitor.py
import requests
import time
import json
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

class ProviderStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class HealthCheckResult:
    provider: str
    status: ProviderStatus
    latency_ms: float
    error: Optional[str] = None
    timestamp: float = time.time()

class ProviderHealthMonitor:
    """Monitors health of AI providers with configurable intervals."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.health_history: Dict[str, list] = {}
        self.max_history = 100

    def check_litellm_health(self) -> HealthCheckResult:
        """Check LiteLLM proxy health."""
        start_time = time.time()
        try:
            response = requests.get(
                f"{self.config['litellm']['endpoint']}/health",
                timeout=self.config['health_check_timeout']
            )
            latency = (time.time() - start_time) * 1000

            if response.status_code == 200:
                return HealthCheckResult(
                    provider="litellm",
                    status=ProviderStatus.HEALTHY,
                    latency_ms=latency
                )
            else:
                return HealthCheckResult(
                    provider="litellm",
                    status=ProviderStatus.DEGRADED,
                    latency_ms=latency,
                    error=f"HTTP {response.status_code}"
                )
        except requests.exceptions.ConnectionError:
            return HealthCheckResult(
                provider="litellm",
                status=ProviderStatus.UNHEALTHY,
                latency_ms=0,
                error="Connection refused"
            )
        except requests.exceptions.Timeout:
            return HealthCheckResult(
                provider="litellm",
                status=ProviderStatus.UNHEALTHY,
                latency_ms=self.config['health_check_timeout'] * 1000,
                error="Timeout"
            )
        except Exception as e:
            return HealthCheckResult(
                provider="litellm",
                status=ProviderStatus.UNKNOWN,
                latency_ms=0,
                error=str(e)
            )

    def check_groq_api(self) -> HealthCheckResult:
        """Check Groq API directly."""
        start_time = time.time()
        try:
            response = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {self.config['groq_api_key']}"},
                timeout=10
            )
            latency = (time.time() - start_time) * 1000

            if response.status_code == 200:
                return HealthCheckResult(
                    provider="groq",
                    status=ProviderStatus.HEALTHY,
                    latency_ms=latency
                )
            elif response.status_code == 429:
                return HealthCheckResult(
                    provider="groq",
                    status=ProviderStatus.DEGRADED,
                    latency_ms=latency,
                    error="Rate limited"
                )
            else:
                return HealthCheckResult(
                    provider="groq",
                    status=ProviderStatus.UNHEALTHY,
                    latency_ms=latency,
                    error=f"HTTP {response.status_code}"
                )
        except Exception as e:
            return HealthCheckResult(
                provider="groq",
                status=ProviderStatus.UNHEALTHY,
                latency_ms=0,
                error=str(e)
            )

    def record_health(self, result: HealthCheckResult):
        """Record health check result in history."""
        if result.provider not in self.health_history:
            self.health_history[result.provider] = []

        self.health_history[result.provider].append(result)

        # Trim history
        if len(self.health_history[result.provider]) > self.max_history:
            self.health_history[result.provider] = self.health_history[result.provider][-self.max_history:]

    def get_provider_reliability(self, provider: str, window: int = 10) -> float:
        """Calculate provider reliability score (0.0 - 1.0)."""
        if provider not in self.health_history:
            return 0.0

        recent = self.health_history[provider][-window:]
        if not recent:
            return 0.0

        healthy_count = sum(
            1 for r in recent if r.status == ProviderStatus.HEALTHY
        )
        degraded_count = sum(
            1 for r in recent if r.status == ProviderStatus.DEGRADED
        )

        # Weight: healthy=1.0, degraded=0.5, unhealthy=0.0
        score = (healthy_count + degraded_count * 0.5) / len(recent)
        return score
```

### Health Check Intervals

| Check Type     | Interval | Timeout | Description                   |
| -------------- | -------- | ------- | ----------------------------- |
| Quick Ping     | 30s      | 5s      | Basic connectivity check      |
| Full Health    | 60s      | 10s     | Complete health verification  |
| API Validation | 300s     | 15s     | Test actual API functionality |

---

## Fallback Logic

### Priority-Based Selection

```python
# fallback_selector.py
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import time

class FallbackReason(Enum):
    CONNECTION_ERROR = "connection_error"
    RATE_LIMIT = "rate_limit"
    AUTH_FAILURE = "auth_failure"
    TIMEOUT = "timeout"
    MODEL_NOT_FOUND = "model_not_found"
    SERVER_ERROR = "server_error"
    HEALTH_CHECK_FAIL = "health_check_fail"
    MANUAL_SWITCH = "manual_switch"

@dataclass
class Provider:
    name: str
    priority: int
    endpoint: str
    models: List[str]
    is_healthy: bool = True
    last_failure: Optional[float] = None
    failure_count: int = 0
    cooldown_until: Optional[float] = None

class FallbackSelector:
    """Intelligent provider selection with fallback logic."""

    def __init__(self, providers: List[Provider], config: dict):
        self.providers = sorted(providers, key=lambda p: p.priority)
        self.config = config
        self.current_provider = self.providers[0]
        self.fallback_history: List[dict] = []

    def select_provider(self, model: Optional[str] = None) -> Provider:
        """Select best available provider based on health and priority."""
        for provider in self.providers:
            # Skip if in cooldown
            if provider.cooldown_until and time.time() < provider.cooldown_until:
                continue

            # Skip if unhealthy
            if not provider.is_healthy:
                continue

            # Check model availability
            if model and model not in provider.models:
                continue

            return provider

        # All providers failed - return highest priority anyway
        return self.providers[0]

    def report_failure(self, provider: Provider, reason: FallbackReason, error: str):
        """Report provider failure and trigger fallback if needed."""
        provider.failure_count += 1
        provider.last_failure = time.time()

        # Set cooldown based on failure type
        cooldown_minutes = self.config['cooldown_minutes'].get(
            reason.value,
            self.config['default_cooldown_minutes']
        )
        provider.cooldown_until = time.time() + (cooldown_minutes * 60)

        # Mark unhealthy after threshold
        if provider.failure_count >= self.config['failure_threshold']:
            provider.is_healthy = False

        # Log fallback event
        self.fallback_history.append({
            'timestamp': time.time(),
            'provider': provider.name,
            'reason': reason.value,
            'error': error,
            'failure_count': provider.failure_count
        })

        # Select new provider
        self.current_provider = self.select_provider()

    def report_success(self, provider: Provider):
        """Report successful operation to reset failure counters."""
        provider.failure_count = 0
        provider.is_healthy = True
        provider.cooldown_until = None

    def restore_provider(self, provider: Provider):
        """Manually restore a provider after fixing issues."""
        provider.is_healthy = True
        provider.failure_count = 0
        provider.cooldown_until = None
```

### Fallback Decision Matrix

| Error Type          | HTTP Code | Action                     | Cooldown |
| ------------------- | --------- | -------------------------- | -------- |
| Connection Refused  | N/A       | Immediate fallback         | 5 min    |
| Unauthorized        | 401       | Verify API key, fallback   | 30 min   |
| Rate Limited        | 429       | Wait 60s or fallback       | 1 min    |
| Model Not Found     | 404       | Check config, fallback     | 10 min   |
| Server Error        | 500       | Retry once, fallback       | 5 min    |
| Timeout             | N/A       | Increase timeout, fallback | 2 min    |
| Service Unavailable | 503       | Fallback immediately       | 10 min   |

---

## Error Handling

### Error Classification

```python
# error_classifier.py
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class ErrorSeverity(Enum):
    LOW = "low"           # Transient, auto-recoverable
    MEDIUM = "medium"     # Requires fallback
    HIGH = "high"         # Requires intervention
    CRITICAL = "critical" # System-wide issue

class ErrorCategory(Enum):
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    RATE_LIMIT = "rate_limit"
    CONFIGURATION = "configuration"
    SERVER = "server"
    CLIENT = "client"
    UNKNOWN = "unknown"

@dataclass
class ClassifiedError:
    category: ErrorCategory
    severity: ErrorSeverity
    is_recoverable: bool
    retry_after: Optional[int] = None  # seconds
    suggested_action: str = ""
    fallback_recommended: bool = False

class ErrorClassifier:
    """Classifies errors and determines appropriate response."""

    def classify(self, error: Exception, context: dict = None) -> ClassifiedError:
        """Classify an error and return handling instructions."""
        error_str = str(error).lower()

        # Connection errors
        if 'connection refused' in error_str or 'connection error' in error_str:
            return ClassifiedError(
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.MEDIUM,
                is_recoverable=True,
                suggested_action="Check if LiteLLM is running. Start with: python -m litellm --config proxy_server_config.yaml",
                fallback_recommended=True
            )

        # Timeout errors
        if 'timeout' in error_str:
            return ClassifiedError(
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.LOW,
                is_recoverable=True,
                retry_after=5,
                suggested_action="Increase timeout or check network latency",
                fallback_recommended=True
            )

        # Authentication errors
        if '401' in error_str or 'unauthorized' in error_str:
            return ClassifiedError(
                category=ErrorCategory.AUTHENTICATION,
                severity=ErrorSeverity.HIGH,
                is_recoverable=False,
                suggested_action="Verify API key is set correctly. Check GROQ_API_KEY environment variable.",
                fallback_recommended=True
            )

        # Rate limit errors
        if '429' in error_str or 'rate limit' in error_str:
            return ClassifiedError(
                category=ErrorCategory.RATE_LIMIT,
                severity=ErrorSeverity.LOW,
                is_recoverable=True,
                retry_after=60,
                suggested_action="Wait for rate limit reset or switch to fallback provider",
                fallback_recommended=True
            )

        # Model not found
        if '404' in error_str or 'not found' in error_str:
            return ClassifiedError(
                category=ErrorCategory.CONFIGURATION,
                severity=ErrorSeverity.MEDIUM,
                is_recoverable=False,
                suggested_action="Check model name in configuration. Verify model is available.",
                fallback_recommended=True
            )

        # Server errors
        if '500' in error_str or 'internal error' in error_str:
            return ClassifiedError(
                category=ErrorCategory.SERVER,
                severity=ErrorSeverity.MEDIUM,
                is_recoverable=True,
                retry_after=30,
                suggested_action="Check server logs. May be temporary issue.",
                fallback_recommended=True
            )

        # Service unavailable
        if '503' in error_str or 'unavailable' in error_str:
            return ClassifiedError(
                category=ErrorCategory.SERVER,
                severity=ErrorSeverity.HIGH,
                is_recoverable=True,
                retry_after=300,
                suggested_action="Service is temporarily unavailable. Use fallback.",
                fallback_recommended=True
            )

        # Unknown error
        return ClassifiedError(
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.MEDIUM,
            is_recoverable=True,
            suggested_action="Investigate error. Check logs for details.",
            fallback_recommended=True
        )
```

---

## Metrics Collection

### Metrics Schema

```python
# metrics_collector.py
import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from pathlib import Path

@dataclass
class ProviderMetrics:
    provider: str
    requests_total: int = 0
    requests_success: int = 0
    requests_failed: int = 0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    uptime_percent: float = 100.0
    last_success: Optional[float] = None
    last_failure: Optional[float] = None
    current_status: str = "unknown"

@dataclass
class FallbackEvent:
    timestamp: float
    from_provider: str
    to_provider: str
    reason: str
    error_message: str
    recovery_time_seconds: Optional[float] = None

class MetricsCollector:
    """Collects and persists provider metrics."""

    def __init__(self, metrics_dir: Path):
        self.metrics_dir = metrics_dir
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_file = metrics_dir / "provider_metrics.json"
        self.events_file = metrics_dir / "fallback_events.jsonl"
        self.latency_history: Dict[str, List[float]] = {}

    def record_request(self, provider: str, latency_ms: float, success: bool):
        """Record a request result."""
        metrics = self._load_metrics(provider)

        metrics.requests_total += 1
        if success:
            metrics.requests_success += 1
            metrics.last_success = time.time()
        else:
            metrics.requests_failed += 1
            metrics.last_failure = time.time()

        # Update latency tracking
        if provider not in self.latency_history:
            self.latency_history[provider] = []
        self.latency_history[provider].append(latency_ms)

        # Keep last 1000 latency samples
        if len(self.latency_history[provider]) > 1000:
            self.latency_history[provider] = self.latency_history[provider][-1000:]

        # Calculate percentiles
        latencies = sorted(self.latency_history[provider])
        if latencies:
            metrics.avg_latency_ms = sum(latencies) / len(latencies)
            p95_index = int(len(latencies) * 0.95)
            metrics.p95_latency_ms = latencies[min(p95_index, len(latencies) - 1)]

        # Calculate uptime
        if metrics.requests_total > 0:
            metrics.uptime_percent = (metrics.requests_success / metrics.requests_total) * 100

        metrics.current_status = "healthy" if success else "unhealthy"
        self._save_metrics(metrics)

    def record_fallback(self, event: FallbackEvent):
        """Record a fallback event."""
        with open(self.events_file, 'a') as f:
            f.write(json.dumps(asdict(event)) + '\n')

    def get_summary(self) -> Dict:
        """Get metrics summary for all providers."""
        summary = {}
        for metrics_file in self.metrics_dir.glob("*.json"):
            if metrics_file.stem != "provider_metrics":
                continue
            with open(metrics_file) as f:
                data = json.load(f)
                summary[data['provider']] = data
        return summary

    def _load_metrics(self, provider: str) -> ProviderMetrics:
        """Load metrics for a provider."""
        if self.metrics_file.exists():
            with open(self.metrics_file) as f:
                data = json.load(f)
                if provider in data:
                    return ProviderMetrics(**data[provider])
        return ProviderMetrics(provider=provider)

    def _save_metrics(self, metrics: ProviderMetrics):
        """Save metrics for a provider."""
        data = {}
        if self.metrics_file.exists():
            with open(self.metrics_file) as f:
                data = json.load(f)
        data[metrics.provider] = asdict(metrics)
        with open(self.metrics_file, 'w') as f:
            json.dump(data, f, indent=2)
```

### Metrics Dashboard Data

```json
{
  "providers": {
    "litellm": {
      "requests_total": 1523,
      "requests_success": 1489,
      "requests_failed": 34,
      "avg_latency_ms": 245.5,
      "p95_latency_ms": 512.0,
      "uptime_percent": 97.77,
      "current_status": "healthy"
    },
    "kilo_code": {
      "requests_total": 156,
      "requests_success": 156,
      "requests_failed": 0,
      "avg_latency_ms": 189.2,
      "p95_latency_ms": 320.0,
      "uptime_percent": 100.0,
      "current_status": "healthy"
    }
  },
  "fallback_events_last_24h": 3,
  "avg_recovery_time_seconds": 127.5
}
```

---

## Integration Examples

### LiteLLM Integration

```python
# litellm_integration.py
import os
from litellm import completion
from typing import Optional, Dict, Any

class LiteLLMClient:
    """LiteLLM client with automatic fallback."""

    def __init__(self, config: Dict[str, Any], fallback_client=None):
        self.config = config
        self.fallback_client = fallback_client
        self.endpoint = config.get('litellm_endpoint', 'http://localhost:4000')
        self.default_model = config.get('default_model', 'groq-70b')

    def chat_completion(
        self,
        messages: list,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send chat completion request with fallback handling."""
        model = model or self.default_model

        try:
            # Set endpoint
            os.environ['OPENAI_API_BASE'] = self.endpoint

            response = completion(
                model=model,
                messages=messages,
                **kwargs
            )
            return response

        except Exception as e:
            # Classify error
            from error_classifier import ErrorClassifier
            classifier = ErrorClassifier()
            classified = classifier.classify(e)

            if classified.fallback_recommended and self.fallback_client:
                print(f"LiteLLM failed ({classified.category.value}), falling back...")
                return self.fallback_client.chat_completion(messages, model, **kwargs)

            raise
```

### Kilo Code Integration

```python
# kilo_code_integration.py
from typing import Dict, Any, Optional

class KiloCodeClient:
    """Kilo Code client for fallback operations."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get('model', 'z-ai/glm-5:free')
        self.provider = 'z-ai'

    def chat_completion(
        self,
        messages: list,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send chat completion via Kilo Code."""
        # Kilo Code uses VS Code extension
        # This is a placeholder for programmatic access
        # In practice, Kilo Code is accessed via the VS Code extension

        return {
            'provider': self.provider,
            'model': model or self.model,
            'messages': messages,
            'status': 'delegated_to_vscode',
            'note': 'Use Kilo Code VS Code extension for actual completion'
        }

    def is_available(self) -> bool:
        """Check if Kilo Code is available."""
        # Check if VS Code extension is installed and active
        # This would require VS Code extension API
        return True
```

### Production Configuration

```yaml
# provider_config.yaml
providers:
  primary:
    name: litellm
    endpoint: http://localhost:4000
    models:
      - groq-70b
      - groq-8b
    priority: 1
    health_check:
      endpoint: /health
      interval_seconds: 30
      timeout_seconds: 5

  fallback:
    name: kilo_code
    provider: z-ai
    model: glm-5:free
    priority: 2

  tertiary:
    name: openrouter
    endpoint: https://openrouter.ai/api/v1
    model: minimax/minimax-m2.1:free
    priority: 3
    api_key_env: OPENROUTER_API_KEY

fallback_rules:
  failure_threshold: 3
  cooldown_minutes:
    connection_error: 5
    auth_failure: 30
    rate_limit: 1
    server_error: 5
    timeout: 2
  default_cooldown_minutes: 5

metrics:
  enabled: true
  output_dir: ./metrics
  retention_days: 30

logging:
  fallback_events: ./logs/fallback_events.jsonl
  level: INFO
```

---

## Configuration

### Environment Variables

| Variable             | Description                 | Required | Default               |
| -------------------- | --------------------------- | -------- | --------------------- |
| `GROQ_API_KEY`       | Groq API key for LiteLLM    | Yes      | -                     |
| `LITELLM_ENDPOINT`   | LiteLLM proxy endpoint      | No       | http://localhost:4000 |
| `OPENROUTER_API_KEY` | OpenRouter API key          | No       | -                     |
| `FALLBACK_LOG_DIR`   | Directory for fallback logs | No       | ./logs                |

### Configuration Files

| File                       | Purpose                | Location                                                             |
| -------------------------- | ---------------------- | -------------------------------------------------------------------- |
| `proxy_server_config.yaml` | LiteLLM configuration  | `C:\Users\pavel\vscodeportable\agentic\01-agent-frameworks\litellm\` |
| `provider_config.yaml`     | Fallback configuration | `.kilocode/skills/provider-fallback/`                                |
| `kilocode.json`            | Kilo Code settings     | `.kilocode/`                                                         |

---

## Windows-Specific Issues

### Issue 1: Port Binding Failures

**Symptom**: LiteLLM says "Listening on http://0.0.0.0:4000" but connection refused

**Causes**:

1. Windows Firewall blocking port
2. Hyper-V reserving port range
3. Another process using port

**Solutions**:

```cmd
:: Check if port is in use
netstat -ano | findstr :4000

:: Check Hyper-V excluded ports
netsh interface ipv4 show excludedportrange protocol=tcp

:: Add firewall rule
netsh advfirewall firewall add rule name="LiteLLM" dir=in action=allow protocol=tcp localport=4000

:: Run as Administrator
:: Right-click Command Prompt -> Run as Administrator
python -m litellm --config proxy_server_config.yaml --port 4000 --host 127.0.0.1
```

### Issue 2: Environment Variables Not Persisting

**Symptom**: GROQ_API_KEY works in current session but not after restart

**Solutions**:

```cmd
:: Set permanently (User level)
setx GROQ_API_KEY "gsk_your_key_here"

:: Set permanently (System level - requires Admin)
setx GROQ_API_KEY "gsk_your_key_here" /M

:: Verify
echo %GROQ_API_KEY%

:: Or use PowerShell
[Environment]::SetEnvironmentVariable("GROQ_API_KEY", "gsk_your_key_here", "User")
```

### Issue 3: Python Path Issues

**Symptom**: `python -m litellm` fails with "No module named litellm"

**Solutions**:

```cmd
:: Check Python installation
where python
python --version

:: Check pip
pip --version

:: Install LiteLLM
pip install litellm

:: If using virtual environment
.venv\Scripts\activate
pip install litellm
```

### Issue 4: Long Path Names

**Symptom**: Configuration file not found or path too long errors

**Solutions**:

```cmd
:: Enable long paths in Windows (requires Admin)
:: Registry edit or Group Policy

:: Or use shorter paths
:: Move LiteLLM config to C:\litellm\

:: Use 8.3 short names
dir /x C:\Users\pavel\vscodeportable\
```

### Issue 5: Antivirus Interference

**Symptom**: LiteLLM starts but requests timeout or fail

**Solutions**:

```cmd
:: Add Python and LiteLLM to antivirus exclusions
:: Windows Defender:
:: Settings -> Update & Security -> Windows Security -> Virus & threat protection
:: -> Manage settings -> Exclusions -> Add exclusion

:: Exclude:
:: - Python executable path
:: - LiteLLM installation directory
:: - Project directory
```

---

## Related Documentation

- [REFERENCE.md](./REFERENCE.md) - Error codes and troubleshooting reference
- [WORKFLOW.md](./WORKFLOW.md) - Detailed fallback workflows
- [RULES.md](./RULES.md) - Fallback rules and logic
- [CHECKLIST.md](./CHECKLIST.md) - Fallback checklist
- [../litellm-debug/SKILL.md](../litellm-debug/SKILL.md) - LiteLLM debugging procedures

---

## Changelog

### v2.0.0 (2026-02-13)

- Added comprehensive health monitoring system
- Implemented priority-based provider selection
- Added metrics collection and reporting
- Added Windows-specific troubleshooting section
- Enhanced error classification and handling
- Added integration examples for LiteLLM and Kilo Code

### v1.0.0 (2026-02-11)

- Initial implementation
- Basic fallback between LiteLLM and Kilo Code
- Simple error handling
