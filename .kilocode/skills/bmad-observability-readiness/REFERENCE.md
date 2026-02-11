# Observability Readiness Reference Guide

## Metrics Taxonomy Standards

### Naming Conventions
```
<namespace>.<component>.<metric_name>
Examples:
- website.hero.render_duration_ms
- api.projects.response_time_ms
- form.contact.submission_count
- build.pipeline.duration_seconds
```

### Metric Types and When to Use

| Type | Use Case | Example |
|------|----------|---------|
| Counter | Cumulative total (always increases) | `submission_count`, `build_total` |
| Gauge | Current value at a point in time | `active_users`, `queue_depth` |
| Histogram | Distribution of values | `response_time_ms`, `bundle_size_bytes` |
| Summary | Aggregated quantiles | `latency_p50`, `latency_p99` |

### Golden Signals Metrics

| Signal | Metrics to Collect | Threshold Examples |
|--------|-------------------|-------------------|
| **Latency** | Response time (p50, p95, p99) | p95 < 200ms |
| **Errors** | Error rate (4xx, 5xx) | Error rate < 1% |
| **Traffic** | Requests per second, throughput | Auto-scale trigger |
| **Saturation** | CPU, memory, queue depth | CPU > 80% |
| **Availability** | Uptime percentage | 99.9% SLA |

## Logging Standards

### Structured Log Fields

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "contact-form",
  "environment": "production",
  "trace_id": "abc123",
  "span_id": "xyz789",
  "message": "Form submission received",
  "user_id": "user_123",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "request_path": "/api/contact",
  "request_method": "POST",
  "status_code": 200,
  "duration_ms": 45
}
```

### Log Levels and When to Use

| Level | Use Case | Example |
|-------|----------|---------|
| DEBUG | Detailed info for debugging | Variable values, flow steps |
| INFO | Normal operation events | User actions, API calls, jobs |
| WARN | Unexpected but recoverable | Retries, fallbacks, degraded |
| ERROR | Failures requiring attention | Exceptions, failed calls, timeouts |
| CRITICAL | System-level failures | Out of memory, database down |

### PII Handling Guidelines

| Field | Action | Alternative |
|-------|--------|-------------|
| Email | Mask or hash | `u***@example.com` |
| IP Address | Truncate or mask | `192.168.1.xxx` |
| Names | Remove or alias | `[REDACTED]` |
| Phone | Mask | `***-***-1234` |

## Tracing Standards

### OpenTelemetry Span Structure

```
Service: contact-form
├── Span: handle_submission
│   ├── Attributes: method=POST, path=/api/contact
│   ├── Events: validation_started, validation_complete
│   └── Span: validate_email
│       ├── Attributes: format=email, length=25
│       └── Status: OK
```

### Standard Span Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `service.name` | Service identifier | `marketing-portfolio` |
| `deployment.environment` | Environment | `production`, `staging` |
| `http.method` | HTTP method | `GET`, `POST` |
| `http.url` | Full URL | `https://tvoje.info/contact` |
| `http.status_code` | Response code | `200`, `404`, `500` |
| `error.type` | Error category | `validation`, `timeout`, `auth` |

## Alerting Best Practices

### SLO Calculation Formula

```
Error Rate = (Failed Requests / Total Requests) × 100
Error Budget = 100% - SLO Target
SLO Status = Error Rate ≤ SLO Target ? ✅ HEALTHY : ❌ DEGRADED
```

### Alert Threshold Guidelines

| Scenario | Threshold | Evaluation Window |
|----------|-----------|-------------------|
| Error spike | >5% errors | 5 minutes |
| High latency | p99 > 1s | 10 minutes |
| Traffic anomaly | >2x baseline | 15 minutes |
| Availability | <99.9% | 1 hour |

### Alert Runbook Template

```markdown
# Alert: High Error Rate on Contact Form

## Severity: P1 (Critical)

## Symptoms
- Error rate > 5% for 5+ minutes
- Users unable to submit contact form

## Diagnosis Steps
1. Check Grafana dashboard: /dashboards/contact-form
2. Review recent deploys in the last hour
3. Check upstream API status (Formspree)
4. Examine error logs for patterns

## Remediation Actions
1. If recent deploy: rollback to previous version
2. If upstream issue: document and notify users
3. If capacity issue: scale up resources

## Escalation
- P1: Alert on-call immediately
- P2: Create ticket, review next business day
```

## Dashboard Examples

### SLO Dashboard Widgets

```
1. Error Budget Remaining (Gauge 0-100%)
   - Service: Contact Form
   - Target: 99.9%
   - Current: 99.7%

2. Request Rate (Time Series)
   - Total requests per minute
   - Error rate overlay

3. Latency Distribution (Histogram)
   - p50, p95, p99 percentiles
   - Target threshold line

4. Availability (Stat)
   - Uptime percentage
   - SLA target comparison
```

## Tooling Options

### Observability Stack Comparison

| Tool | Strengths | Best For | Cost |
|------|-----------|----------|------|
| **Datadog** | Full platform, APM | Large teams, complex systems | $$$ |
| **Grafana + Prometheus** | Open source, customizable | Cost-conscious teams | $ |
| **New Relic** | Ease of use, alerting | Teams needing quick setup | $$ |
| **AWS CloudWatch** | Native AWS integration | AWS-heavy environments | $$ |
| **Plausible** | Privacy-focused analytics | GDPR compliance | $$ |

### Selection Criteria

1. **Budget**: Open source (Grafana) vs commercial (Datadog)
2. **Scale**: Number of services, data volume
3. **Team expertise**: Familiarity with tooling
4. **Integration**: Existing infrastructure compatibility
5. **Compliance**: GDPR, SOC2, HIPAA requirements
