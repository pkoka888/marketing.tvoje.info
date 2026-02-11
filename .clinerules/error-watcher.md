---
description: Error watcher rules — monitor and analyze error logs across the stack
---

# Error Watcher Role

When asked to "watch errors" or "error scan", check all error sources:

## Error Sources

### 1. Application Build Errors
```bash
npm run build 2>&1
```
Parse stderr for: TypeScript errors, Astro compilation, PostCSS/Tailwind issues

### 2. Test Failures
```bash
npm run test 2>&1
```
Parse output for: FAIL lines, assertion errors, timeout issues

### 3. Lint Errors
```bash
npx eslint src/ --config eslint.config.mjs 2>&1
```

### 4. Docker Errors (if applicable)
```bash
docker compose logs --tail=100 2>&1
```
Look for: container crashes, OOM kills, network errors, volume mount failures

### 5. MCP Server Errors
Check for common npx spawn failures:
- `ENOENT` — package not found
- `ETIMEOUT` — download timeout
- `EACCES` — permission denied
- Port conflicts

### 6. Git / GitHub Actions
```bash
git log --oneline -5
```
Check recent commits for CI status. Review `.github/workflows/` for:
- Failing steps
- Outdated action versions
- Missing secrets

## Debugging Plan Format

For each unresolved error, generate:
```markdown
## Error: [short description]
- **Source**: [build|test|docker|mcp|git]
- **File**: [path if applicable]
- **Error message**: [exact text]
- **Root cause analysis**: [why it happened]
- **Fix proposal**: [specific steps]
- **Priority**: [P0 blocker | P1 important | P2 improvement]
```

## Report Location
Save to `plans/agent-shared/error-logs/` as:
```
YYYY-MM-DD-error-scan.md
```
