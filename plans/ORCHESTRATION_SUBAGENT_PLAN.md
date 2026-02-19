# Subagent Orchestration Plan

## Current Status
Pending tasks identified from previous session:
1. **Fix FIRECRAWL_API_KEY detection** - Key exists in .env but script reports "Not Found"
2. **Add TS_OAUTH and VPS keys to .env** - These exist in GitHub Secrets but not in .env
3. **Verify all API keys end-to-end**

## Task Analysis

### Task 1: FIRECRAWL_API_KEY Detection Fix
- **Root Cause**: Python script using `load_dotenv()` not correctly parsing the key
- **Location**: `scripts/verify_api_keys.py`
- **Agent**: Kilo Code (bulk coding)
- **Skill**: `bmad-development-execution` + `debug`
- **Model**: `x-ai/grok-code-fast-1:optimized:free`

### Task 2: Add TS_OAUTH and VPS Keys
- **Source**: GitHub Secrets (already exist)
- **Target**: .env file
- **Agent**: Kilo Code or Cline (simple edit)
- **Skill**: `bmad-development-execution`
- **Model**: `minimax-m2.1:free`

### Task 3: End-to-End API Verification
- **Scope**: Test all 19 keys with actual API calls
- **Agent**: OpenCode `@researcher` (research) + `@codex` (testing)
- **Skill**: `bmad-discovery-research` + `debug`
- **Model**: `big-pickle` (free, 200K context)

## Subagent Assignments

| Task | Agent | Skill | Model | Justification |
|------|-------|-------|-------|---------------|
| Fix FIRECRAWL detection | Kilo `bmad-dev` | bmad-development-execution, debug | x-ai/grok-code-fast-1:optimized:free | Free, unlimited, good for code fixes |
| Add keys to .env | Cline | bmad-development-execution | minimax-m2.1:free | Simple edit task |
| Research security | OpenCode `@researcher` | bmad-discovery-research | big-pickle | 200K context for research |
| Test verification | OpenCode `@codex` | debug | x-ai/grok-code-fast-1:optimized:free | Free, good for testing |

## Orchestration Strategy

### Parallel Safe Tasks
- Fix FIRECRAWL (Kilo) + Research security (OpenCode) can run in parallel
- Add keys to .env can run in parallel with verification

### Sequential Gates
- Add keys to .env must complete before final verification
- Fix FIRECRAWL must complete before final verification

## Commands to Execute

```bash
# Task 1: Fix FIRECRAWL detection (Kilo)
kilo run --prompt "Fix the FIRECRAWL_API_KEY detection in scripts/verify_api_keys.py. The key exists in .env (FIRECRAWL_API_KEY=fc-351f9e63c88b412ebcf75b2283d98179) but the script reports 'Not Found'. Debug and fix the dotenv loading or key detection logic."

# Task 2: Add keys to .env (Cline)
cline "Add the following keys to .env from GitHub Secrets: TS_OAUTH_CLIENT_ID, TS_OAUTH_SECRET, VPS_IP, VPS_USER, VPS_SSH_PORT, VPS_SSH_KEY"

# Task 3: Research 2026 security (OpenCode)
@researcher "Research current 2026 API security best practices for web applications. Focus on: key rotation, environment variable security, secrets management, and OAuth token handling. Create a brief report."

# Task 4: Test verification (OpenCode)
@codex "Run the updated verify_api_keys.py script and confirm all 19 API keys are detected correctly"
```

## Expected Outcomes
1. FIRECRAWL_API_KEY detection fixed - script reports "Present" or "OK"
2. .env updated with 6 new keys (TS_OAUTH_*, VPS_*)
3. Security best practices documented in docs/SECURITY_BEST_PRACTICES.md
4. All 19 keys verified working

## Cost Tracking
- Kilo (free): ~0
- Cline (free): ~0
- OpenCode (free): ~0
- **Total**: $0 (within budget)
