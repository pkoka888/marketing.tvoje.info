# Provider Fallback Rules

## Overview

This document defines the comprehensive rules and logic governing provider selection, fallback behavior, and recovery procedures for the AI provider fallback system.

---

## Table of Contents

1. [Provider Priority Rules](#provider-priority-rules)
2. [Fallback Trigger Rules](#fallback-trigger-rules)
3. [Cooldown Rules](#cooldown-rules)
4. [Failure Threshold Rules](#failure-threshold-rules)
5. [Recovery Rules](#recovery-rules)
6. [Circuit Breaker Rules](#circuit-breaker-rules)
7. [Cost Optimization Rules](#cost-optimization-rules)
8. [Context Preservation Rules](#context-preservation-rules)
9. [Configuration Rules](#configuration-rules)
10. [Rule Evaluation Engine](#rule-evaluation-engine)

---

## Provider Priority Rules

### Rule P1: Default Priority Order

```
Priority 1 (Primary):    LiteLLM Proxy (localhost:4000) → Groq API
Priority 2 (Fallback):   Kilo Code Extension → z-ai/glm-5:free
Priority 3 (Tertiary):   OpenRouter → minimax-m2.1:free
Priority 4 (Emergency):  Direct API → Gemini Flash (free tier)
```

**Rationale**:

- LiteLLM provides unified interface with built-in fallback
- Kilo Code is always available as local extension
- OpenRouter offers free tier with reasonable limits
- Gemini Flash as last resort with 1M tokens/day free

### Rule P2: Priority Override Conditions

Override default priority when:

| Condition                             | Override Action             |
| ------------------------------------- | --------------------------- |
| Budget approaching limit ($18+/month) | Skip paid providers         |
| Rate limit on primary (429)           | Immediate fallback to next  |
| Auth failure (401/403)                | Skip provider for session   |
| Connection refused                    | Skip provider for 5 minutes |
| Model not found (404)                 | Skip model, try alternate   |
| Timeout (>30s)                        | Immediate fallback          |

### Rule P3: Model Selection Within Provider

When a provider has multiple models:

```
LiteLLM/Groq:
  1. groq-70b (llama-3.3-70b-versatile) - Complex tasks
  2. groq-8b (llama-3.1-8b-instant) - Simple tasks

Kilo Code:
  1. z-ai/glm-5:free - Default
  2. z-ai/glm-4:free - Fallback within provider

OpenRouter:
  1. minimax/minimax-m2.1:free - Default
  2. meta-llama/llama-3-8b-instruct:free - Fallback
```

---

## Fallback Trigger Rules

### Rule F1: Immediate Fallback Triggers

Immediate fallback (no retry) occurs on:

| Error Type            | HTTP Code | Action                    |
| --------------------- | --------- | ------------------------- |
| Authentication Failed | 401, 403  | Skip provider for session |
| Rate Limited          | 429       | Fallback with cooldown    |
| Model Not Found       | 404       | Try alternate model       |
| Service Unavailable   | 503       | Fallback with cooldown    |
| Bad Gateway           | 502       | Fallback with retry       |
| Gateway Timeout       | 504       | Fallback with retry       |

### Rule F2: Retry-Before-Fallback Triggers

Retry before fallback on:

| Error Type            | Retries | Backoff     | Fallback After |
| --------------------- | ------- | ----------- | -------------- |
| Connection Timeout    | 2       | Exponential | 3rd failure    |
| Network Error         | 2       | Linear (5s) | 3rd failure    |
| Internal Server Error | 1       | None        | 2nd failure    |
| Service Overloaded    | 2       | Exponential | 3rd failure    |

### Rule F3: Connection Failure Rules

```
IF connection_refused:
  1. Log failure with timestamp
  2. Mark provider as "unhealthy"
  3. Start health check loop (30s interval)
  4. Fallback to next provider
  5. Auto-recover after 3 consecutive successful health checks

IF timeout:
  1. Log timeout duration
  2. Increment timeout counter
  3. IF timeout_counter >= 3:
       Mark provider as "degraded"
       Increase timeout threshold by 50%
  4. Fallback to next provider
```

### Rule F4: Graceful Degradation

```
Degradation Levels:
  Level 0 (Normal):      All providers available
  Level 1 (Degraded):    Primary unavailable, using fallback
  Level 2 (Critical):    Only tertiary provider available
  Level 3 (Emergency):   Using emergency provider only
  Level 4 (Failed):      No providers available

Actions per Level:
  Level 0: Normal operation
  Level 1: Log warning, continue with fallback
  Level 2: Log error, alert user, continue
  Level 3: Log critical, alert user, limited functionality
  Level 4: Log emergency, notify user, queue requests
```

---

## Cooldown Rules

### Rule C1: Provider Cooldown Periods

| Trigger Event      | Cooldown Duration | Decay Factor     |
| ------------------ | ----------------- | ---------------- |
| Rate Limit (429)   | 60 seconds        | 0.9 per success  |
| Auth Failure       | Session duration  | No decay         |
| Connection Refused | 5 minutes         | 0.8 per success  |
| Timeout            | 2 minutes         | 0.9 per success  |
| Server Error (5xx) | 30 seconds        | 0.95 per success |
| Model Overload     | 90 seconds        | 0.85 per success |

### Rule C2: Cooldown Decay

```python
def calculate_effective_cooldown(base_cooldown, success_count, decay_factor):
    """
    Calculate effective cooldown after successful requests.

    Args:
        base_cooldown: Initial cooldown in seconds
        success_count: Number of consecutive successful requests
        decay_factor: Multiplier per success (0.0-1.0)

    Returns:
        Effective cooldown in seconds (minimum 5s)
    """
    effective = base_cooldown * (decay_factor ** success_count)
    return max(effective, 5)  # Minimum 5 second cooldown
```

### Rule C3: Cooldown Bypass

Bypass cooldown when:

1. **Emergency Mode**: All other providers failed
2. **User Override**: Explicit user request with confirmation
3. **Health Check**: Provider reports healthy after cooldown start
4. **Time Critical**: Request marked as time-sensitive

---

## Failure Threshold Rules

### Rule T1: Consecutive Failure Thresholds

```
Provider Status Thresholds:
  Healthy:    0-2 consecutive failures
  Degraded:   3-5 consecutive failures
  Unhealthy:  6+ consecutive failures

Status Transitions:
  Healthy → Degraded:   3 consecutive failures
  Degraded → Unhealthy: 6 consecutive failures
  Unhealthy → Degraded: 2 consecutive successes
  Degraded → Healthy:   5 consecutive successes
```

### Rule T2: Time-Window Failure Thresholds

```
Sliding Window: 5 minutes

Failure Count Thresholds:
  0-2 failures:   Normal operation
  3-5 failures:   Warning state, increased monitoring
  6-10 failures:  Degraded state, prefer fallback
  11+ failures:   Unhealthy state, avoid provider

Recovery:
  - Reset count after 5 minutes of no failures
  - Partial reset: -1 failure per successful request
```

### Rule T3: Error Type Weighting

Different error types have different weights:

| Error Type         | Weight | Reason                          |
| ------------------ | ------ | ------------------------------- |
| Auth Failure       | 3.0    | Critical, requires intervention |
| Rate Limit         | 1.0    | Expected, temporary             |
| Connection Refused | 2.0    | Service down                    |
| Timeout            | 1.5    | Performance issue               |
| Server Error       | 1.5    | Temporary issue                 |
| Model Not Found    | 2.5    | Configuration issue             |

```python
def calculate_weighted_failure_score(failures):
    """
    Calculate weighted failure score for provider health.

    Args:
        failures: List of failure events with types

    Returns:
        Weighted score (threshold: 10.0 = unhealthy)
    """
    weights = {
        'auth_failure': 3.0,
        'rate_limit': 1.0,
        'connection_refused': 2.0,
        'timeout': 1.5,
        'server_error': 1.5,
        'model_not_found': 2.5
    }

    score = sum(weights.get(f.type, 1.0) for f in failures)
    return score
```

---

## Recovery Rules

### Rule R1: Automatic Recovery

```
Recovery Sequence:
  1. Health check passes (quick ping)
  2. Wait cooldown period
  3. Health check passes (full health)
  4. Mark as "recovering"
  5. Route 10% of traffic
  6. Monitor for 5 minutes
  7. If stable, mark as "healthy"
  8. Gradually increase traffic (25%, 50%, 100%)
```

### Rule R2: Recovery Backoff

```
Recovery Attempt Backoff:
  1st attempt: Immediate after cooldown
  2nd attempt: 30 seconds after 1st failure
  3rd attempt: 2 minutes after 2nd failure
  4th attempt: 5 minutes after 3rd failure
  5th+ attempt: 15 minutes after previous failure

Max Recovery Attempts: 10 per hour
Reset attempt counter: After 30 minutes of stability
```

### Rule R3: Provider Rehabilitation

```python
def rehabilitate_provider(provider, current_traffic_percentage):
    """
    Gradually restore traffic to recovering provider.

    Args:
        provider: Provider to rehabilitate
        current_traffic_percentage: Current traffic share

    Returns:
        New traffic percentage
    """
    if provider.success_streak >= 5:
        # Increase traffic by 25% of remaining capacity
        increase = (100 - current_traffic_percentage) * 0.25
        new_percentage = current_traffic_percentage + increase
        return min(new_percentage, 100)

    return current_traffic_percentage
```

---

## Circuit Breaker Rules

### Rule B1: Circuit Breaker States

```
States:
  CLOSED:    Normal operation, requests flow through
  OPEN:      Failing, reject all requests immediately
  HALF_OPEN: Testing, allow limited requests

State Transitions:
  CLOSED → OPEN:      Failure threshold exceeded
  OPEN → HALF_OPEN:   After timeout period
  HALF_OPEN → CLOSED: Success threshold met
  HALF_OPEN → OPEN:   Any failure during test
```

### Rule B2: Circuit Breaker Thresholds

| Provider Type | Failure Threshold | Success Threshold | Timeout |
| ------------- | ----------------- | ----------------- | ------- |
| Primary       | 5 failures        | 3 successes       | 60s     |
| Fallback      | 3 failures        | 2 successes       | 30s     |
| Tertiary      | 2 failures        | 2 successes       | 15s     |
| Emergency     | 1 failure         | 1 success         | 10s     |

### Rule B3: Circuit Breaker Implementation

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, success_threshold=3, timeout=60):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.success_count = 0
        self.state = 'CLOSED'
        self.last_failure_time = None

    def can_execute(self):
        if self.state == 'CLOSED':
            return True
        elif self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
                return True
            return False
        else:  # HALF_OPEN
            return True

    def record_success(self):
        self.failure_count = 0
        if self.state == 'HALF_OPEN':
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = 'CLOSED'
                self.success_count = 0

    def record_failure(self):
        self.success_count = 0
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
```

---

## Cost Optimization Rules

### Rule O1: Free-First Routing

```
Default Routing (Cost Optimized):
  1. LiteLLM → Groq (Free tier)
  2. Kilo Code → z-ai/glm-5:free (Free)
  3. OpenRouter → minimax-m2.1:free (Free)
  4. Gemini Flash → Free tier (1M tokens/day)

Paid Provider Rules:
  - Only use paid providers when explicitly requested
  - Log all paid API calls with cost estimate
  - Alert when monthly budget exceeds 80%
  - Hard stop at 100% budget utilization
```

### Rule O2: Budget Tracking

```python
class BudgetTracker:
    def __init__(self, monthly_limit=20.0):
        self.monthly_limit = monthly_limit
        self.current_spend = 0.0
        self.alert_thresholds = [0.5, 0.8, 0.9, 1.0]

    def can_proceed(self, estimated_cost):
        if self.current_spend + estimated_cost > self.monthly_limit:
            return False
        return True

    def record_spend(self, cost):
        self.current_spend += cost
        for threshold in self.alert_thresholds:
            if self.current_spend / self.monthly_limit >= threshold:
                self.alert(threshold)

    def alert(self, threshold):
        if threshold >= 1.0:
            # Kill-switch: Stop all paid operations
            logging.critical(f"Budget exhausted: ${self.current_spend:.2f}")
        elif threshold >= 0.9:
            logging.warning(f"Budget at 90%: ${self.current_spend:.2f}")
```

### Rule O3: Cost-Aware Model Selection

```
Task Type → Model Selection:
  Research/Analysis:     Free models (Groq, Kilo)
  Code Generation:       Free models (Groq 70b preferred)
  Architecture Design:   Paid models (with approval)
  Complex Reasoning:     Paid models (with approval)
  Simple Tasks:          Smaller free models (Groq 8b)

Cost Escalation:
  1. Start with free model
  2. If task fails after 2 attempts, escalate
  3. Log escalation reason
  4. Use cheapest capable paid model
```

---

## Context Preservation Rules

### Rule X1: Conversation Context

```
When switching providers:
  1. Preserve conversation history
  2. Include system prompt
  3. Note provider switch in context
  4. Maintain message format compatibility

Context Format:
  {
    "messages": [...],
    "system_prompt": "...",
    "metadata": {
      "original_provider": "litellm",
      "fallback_provider": "kilo_code",
      "switch_reason": "rate_limit",
      "timestamp": "2026-02-13T03:00:00Z"
    }
  }
```

### Rule X2: Request Retry Context

```python
def prepare_retry_context(original_request, failure_info, attempt_number):
    """
    Prepare context for retry with fallback provider.

    Args:
        original_request: The failed request
        failure_info: Details about the failure
        attempt_number: Current attempt number

    Returns:
        Modified request for fallback provider
    """
    context = {
        "original_request": original_request,
        "failure": {
            "provider": failure_info.provider,
            "error": failure_info.error,
            "timestamp": failure_info.timestamp
        },
        "attempt": attempt_number,
        "max_attempts": 3
    }

    # Add context hint for fallback provider
    modified_request = original_request.copy()
    modified_request["context"] = context
    modified_request["retry_hint"] = f"This is attempt {attempt_number}. Previous provider failed."

    return modified_request
```

### Rule X3: State Persistence

```
Persist to disk when:
  - Provider state changes (healthy/unhealthy)
  - Circuit breaker state changes
  - Budget threshold crossed
  - Configuration changes

Persistence Format (JSON):
  {
    "timestamp": "2026-02-13T03:00:00Z",
    "providers": {
      "litellm": {"status": "healthy", "success_rate": 0.95},
      "kilo_code": {"status": "healthy", "success_rate": 0.99},
      "openrouter": {"status": "degraded", "success_rate": 0.85}
    },
    "circuit_breakers": {
      "litellm": "CLOSED",
      "openrouter": "HALF_OPEN"
    },
    "budget": {
      "current": 5.23,
      "limit": 20.00,
      "percent_used": 26.15
    }
  }
```

---

## Configuration Rules

### Rule G1: Configuration Hierarchy

```
Priority (highest to lowest):
  1. Environment variables
  2. User configuration file
  3. Default configuration

Environment Variables:
  PROVIDER_PRIORITY=litellm,kilo_code,openrouter
  PROVIDER_TIMEOUT=30
  PROVIDER_MAX_RETRIES=3
  PROVIDER_COOLDOWN=60
  BUDGET_LIMIT=20

Configuration File (.provider-fallback.yaml):
  providers:
    litellm:
      endpoint: http://localhost:4000
      timeout: 30
    kilo_code:
      model: z-ai/glm-5:free
  fallback:
    max_retries: 3
    cooldown: 60
  budget:
    monthly_limit: 20
```

### Rule G2: Configuration Validation

```python
def validate_config(config):
    """
    Validate provider fallback configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    # Check required fields
    if 'providers' not in config:
        errors.append("Missing 'providers' configuration")

    # Validate each provider
    for name, provider in config.get('providers', {}).items():
        if 'endpoint' not in provider and name != 'kilo_code':
            errors.append(f"Provider '{name}' missing endpoint")

    # Validate numeric ranges
    if config.get('fallback', {}).get('max_retries', 3) > 10:
        errors.append("max_retries cannot exceed 10")

    if config.get('fallback', {}).get('cooldown', 60) < 5:
        errors.append("cooldown cannot be less than 5 seconds")

    return len(errors) == 0, errors
```

### Rule G3: Hot Reloading

```
Configuration Hot Reload:
  1. Watch configuration file for changes
  2. Validate new configuration
  3. If valid:
     - Apply new settings
     - Log configuration change
     - Notify monitoring system
  4. If invalid:
     - Keep current configuration
     - Log validation errors
     - Alert administrators

Reload Triggers:
  - File modification timestamp change
  - SIGHUP signal (Unix)
  - Explicit reload API call
```

---

## Rule Evaluation Engine

### Rule E1: Evaluation Order

```
For each request, evaluate rules in order:

  1. Budget Check (O1, O2)
     └─ If budget exhausted → Reject or use free tier only

  2. Circuit Breaker Check (B1, B2, B3)
     └─ If circuit open → Skip to next provider

  3. Cooldown Check (C1, C2, C3)
     └─ If in cooldown → Skip or bypass based on rules

  4. Health Check (T1, T2, T3)
     └─ If unhealthy → Skip with option to test

  5. Provider Selection (P1, P2, P3)
     └─ Select best available provider

  6. Execute Request
     └─ Monitor for failures

  7. Handle Response
     ├─ Success → Update health, decay cooldown
     └─ Failure → Apply fallback rules (F1-F4)
```

### Rule E2: Rule Conflict Resolution

```
When rules conflict:

  1. Safety rules override optimization rules
     Example: Budget limit overrides free-first routing

  2. Explicit configuration overrides defaults
     Example: User-set priority overrides default order

  3. More specific rule overrides general rule
     Example: Provider-specific timeout overrides global timeout

  4. Time-based rules take precedence
     Example: Cooldown bypass for time-critical requests
```

### Rule E3: Rule Evaluation Logging

```python
def log_rule_evaluation(request_id, rules_evaluated, decision):
    """
    Log rule evaluation for debugging and auditing.

    Args:
        request_id: Unique request identifier
        rules_evaluated: List of rules that were evaluated
        decision: Final decision made
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "rules": rules_evaluated,
        "decision": decision,
        "provider": decision.provider,
        "reason": decision.reason
    }

    # Log to file
    with open("provider_fallback.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # Log to metrics
    metrics.counter("rule_evaluations", tags={
        "decision": decision.reason
    })
```

---

## Quick Reference

### Decision Matrix

| Scenario                | Rule   | Action                      |
| ----------------------- | ------ | --------------------------- |
| Rate limit (429)        | F1, C1 | Fallback, 60s cooldown      |
| Auth failure (401)      | F1, C1 | Fallback, session cooldown  |
| Connection refused      | F3, C1 | Fallback, 5min cooldown     |
| Timeout                 | F2, C1 | Retry 2x, then fallback     |
| Budget at 90%           | O2     | Alert, restrict paid APIs   |
| Budget at 100%          | O2     | Kill-switch, free tier only |
| 3 consecutive failures  | T1     | Mark degraded               |
| 6 consecutive failures  | T1     | Mark unhealthy              |
| 5 consecutive successes | T1     | Mark healthy                |
| Circuit open            | B1     | Skip provider               |
| Recovery test pass      | R1     | Route 10% traffic           |

### Rule Priority

```
1. Safety (Budget, Auth)     - Always evaluate first
2. Availability (Circuit)    - Prevent cascading failures
3. Health (Thresholds)       - Route to working providers
4. Optimization (Cost)       - Prefer free/cheap options
5. Recovery (Rehabilitation) - Restore failed providers
```

---

## Related Documents

- [SKILL.md](./SKILL.md) - Main documentation
- [REFERENCE.md](./REFERENCE.md) - Error codes and troubleshooting
- [WORKFLOW.md](./WORKFLOW.md) - Usage workflows

---

## Version History

| Version | Date       | Changes                       |
| ------- | ---------- | ----------------------------- |
| 1.0.0   | 2026-02-13 | Initial comprehensive ruleset |
