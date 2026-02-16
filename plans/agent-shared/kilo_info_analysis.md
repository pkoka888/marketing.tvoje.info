# Mission: App Analysis & Infrastructure Stabilization

**Role**: Orhcestrator & Technical Lead
**Objective**: Fix the persistent Redis restart loops, restore browser verification capabilities, and audit the application state using "Good Practices".

## 1. Finding: The Root Cause of Instability

- **Redis Restarts**: The `redis-server.js` MCP server keeps restarting because it cannot connect to Redis.
- **Cause**: The `REDIS_URL` environment variable (`${REDIS_URL}`) defined in `mcp.json` is not resolving correctly when Kilo Code runs agents. It likely defaults to `undefined`, falls back to `localhost:6379`, and fails because your Redis is on **port 36379**.
- **Browser Failure**: Playwright fails because `$HOME` is missing in the agent environment.

## 2. Required Actions (The "Fix")

### A. Fix Redis Config (Priority: Critical)

**Action**: Update `.kilocode/mcp.json` to hardcode the local Redis URL or ensure `.env` loading.

- **Current**: `"env": { "REDIS_URL": "${REDIS_URL}", ... }`
- **Fix**: Replace `${REDIS_URL}` with `redis://127.0.0.1:36379` (if port check confirms).

### B. Restore Browser Environment

**Action**: Provide `$HOME` to the agent process or use a portable Playwright path.

- **Workaround**: For now, rely on `console.log` and manual verification until we fix the environment variable injection in `tasks.json`.

### C. App Analysis Plan (The "Good Practice" Audit)

**Objective**: Analyze current app state (`npm run dev`).
**Action**:

1.  **Git/Config Management**:
    - **Practice**: "Hybrid Git" — Use Git for versioning config templates (`config.yaml.template`), but keep active configs (`config.yaml`) in `.gitignore` if they contain secrets or local paths.
    - **Current State**: `mcp.json` is tracked. **Recommendation**: Keep it tracked but use `config.json` for local overrides if supported, or ensure secrets use environment variables (which we do).
2.  **Code Safety**:
    - **Practice**: "Read-Only Core" — The `vscodeportable/agentic` reference is read-only. This is excellent and should be maintained.
    - **Audit**: Verify no agent is trying to write there.

## 3. Execution Instructions for Kilo Code

1.  **Edit `mcp.json`**: Update the `REDIS_URL` to the concrete local value `redis://127.0.0.1:36379`.
2.  **Audit Agents**: Run the `kilo_audit_prompt.md` mission to check all agent definitions.
3.  **Report**: Overwrite `plans/agent-shared/squad-status.json` with "active" once Redis stays up for >1 minute.

**Proceed with these fixes immediately.**
