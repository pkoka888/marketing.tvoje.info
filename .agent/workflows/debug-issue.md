# Debug Issue Workflow

**Purpose**: General issue debugging workflow with issue classification and agent routing
**Mode**: Debug

---

## Issue Classification

| Issue Type | Indicators | Primary Agents | Confidence Threshold |
|-----------|-----------|----------------|---------------------|
| Build Failure | `npm run build` fails, TypeScript errors | Log Analyzer + Dependency Checker | 0.75 |
| Runtime Error | Uncaught exceptions, process crashes | Stack Trace Analyzer + Log Analyzer | 0.80 |
| Server Issue | Health check fails, container exits | Server Analyzer + Log Analyzer | 0.85 |
| Test Failure | Test suite fails, assertion errors | Test Runner + Config Validator | 0.70 |

## Step-by-Step Workflow

### Step 1: Issue Intake
1. Gather error message, timestamp, environment
2. Create evidence directory: `mkdir -p evidence/{timestamp}/issue`
3. Document initial state

### Step 2: Classify Issue
- Route to `debug-build.md` for build failures
- Route to `debug-server.md` for server issues
- Otherwise proceed with general parallel analysis

### Step 3: Execute Debug Agents (Parallel)
Run appropriate agents in parallel based on classification.

### Step 4: Aggregate Evidence
1. Collect agent reports in standardized format
2. Cross-validate findings
3. Calculate confidence score

### Step 5: Report and Fix
Generate root cause report and implement fix if confidence >= threshold.

### Step 6: Escalation (if needed)
If confidence < threshold: document debugging attempts, request human input.

## Related Files

- **Build Debug**: `.agent/workflows/debug-build.md`
- **Server Debug**: `.agent/workflows/debug-server.md`
- **Orchestrator Template**: `.agent/workflows/orchestrator-debug.md`
