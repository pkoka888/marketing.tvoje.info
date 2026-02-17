# Orchestrator Debug Template

**Purpose**: Template for orchestrating parallel debug agents
**Mode**: Debug (Orchestrator)

---

## Orchestration Patterns

### Pattern A: Sectioning (Independent Subtasks)
Tasks broken into independent subtasks that run in parallel, results aggregated programmatically.

**When to use**: Complex issues with multiple potential causes, time-critical debugging

### Pattern B: Voting (Multiple Perspectives)
Same task run multiple times with different approaches to get diverse outputs.

**When to use**: Critical issues requiring high confidence, security-related debugging

## Issue Routing Matrix

| Issue Type | Primary Agents | Confidence Threshold |
|-----------|---------------|---------------------|
| Build Failure | Log Analyzer, Dependency Checker | 0.75 |
| Runtime Error | Stack Trace Analyzer, Log Analyzer | 0.80 |
| Test Failure | Test Runner, Configuration Validator | 0.70 |
| Server Issue | Server Analyzer, Log Analyzer | 0.85 |
| Security Issue | Log Analyzer, Dependency Checker | 0.85 |

## Orchestration Execution

### Step 1: Issue Classification
1. Parse issue description
2. Identify keywords and patterns
3. Classify issue type
4. Select appropriate template

### Step 2: Agent Dispatch
1. Load template configuration
2. Initialize primary agents (parallel)
3. Set up evidence collection

### Step 3: Evidence Collection
1. Collect agent reports
2. Normalize findings format
3. Store in `evidence/{timestamp}/agent-reports/`

### Step 4: Aggregation
1. Apply weighted confidence
2. Cross-validate findings (consensus increases confidence)
3. Calculate final score

### Step 5: Resolution or Escalation
1. If confidence >= threshold: Recommend fix
2. If confidence < threshold: Escalate to human
3. Document all findings

## Evidence Storage

```
evidence/{timestamp}/
├── issue-summary.json
├── agent-reports/
│   ├── log-analyzer.json
│   ├── dependency-checker.json
│   └── server-analyzer.json
├── aggregated-findings.json
└── root-cause-report.md
```

## Related Files

- **General Debug**: `.agent/workflows/debug-issue.md`
- **Build Debug**: `.agent/workflows/debug-build.md`
- **Server Debug**: `.agent/workflows/debug-server.md`
