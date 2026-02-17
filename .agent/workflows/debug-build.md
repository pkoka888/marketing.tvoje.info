# Debug Build Workflow

**Purpose**: Build failure specific debugging workflow
**Mode**: Debug

---

## Overview

This workflow provides a specialized approach to debugging build and compilation failures. It coordinates Log Analyzer and Dependency Checker agents to identify root causes quickly.

## Trigger Conditions

| Condition | Priority | Description |
|-----------|----------|-------------|
| `npm run build` exits non-zero | High | Build command failure |
| TypeScript compilation errors | High | TS errors in output |
| Missing dependencies detected | Medium | Module not found errors |
| Build timeout | Medium | Build exceeds time limit |
| Memory limit exceeded | High | OOM during build |

## Step-by-Step Workflow

### Step 1: Capture Build Output

```bash
npm run build 2>&1 | tee evidence/{timestamp}/build-output.log
```

### Step 2: Run Parallel Analysis

Execute Log Analyzer and Dependency Checker in parallel:
- **Log Analyzer**: Parse build output for error patterns
- **Dependency Checker**: Validate dependency versions and compatibility

### Step 3: Aggregate and Score

1. Collect agent reports
2. Calculate confidence: `(log_confidence * 0.5) + (dep_confidence * 0.5)`
3. Cross-validate findings

### Step 4: Configuration Check (if confidence < 0.75)

Run Configuration Validator:
1. Check `tsconfig.json`
2. Check `astro.config.mjs`
3. Check environment variables

### Step 5: Generate and Apply Fix

Apply recommended fix, run build again, verify or iterate.

## Evidence Collection

```
evidence/{timestamp}/
├── build-output.log
├── package-versions.json
├── agent-reports/
│   ├── log-analyzer.json
│   └── dependency-checker.json
├── aggregated-findings.json
└── root-cause-report.md
```

## Related Files

- **General Debug**: `.agent/workflows/debug-issue.md`
- **Server Debug**: `.agent/workflows/debug-server.md`
- **Orchestrator Template**: `.agent/workflows/orchestrator-debug.md`
