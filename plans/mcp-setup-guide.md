# Task Plan: MCP Setup

**Date**: 2026-02-17
**Agent**: Cline (Batch Template Migration)

## 1. Goal

Set up 10 MCP (Model Context Protocol) servers for the marketing portfolio project with proper security configuration and verification.

## 2. Context & Constraints

- **Files**: `.kilocode/mcp.json`, `.kilocode/mcp-servers/`, `.env`
- **Rules**: Follow AGENTS.md security standards, use project-isolated Redis namespace
- **Budget**: Free (using existing npm packages)

## 3. Implementation Steps

1.  **Set up Redis MCP server**
    - [ ] Configure custom Redis server at `.kilocode/mcp-servers/redis-server.js`
    - [ ] Fix WSL2 port conflict (use `0.0.0.0` instead of `127.0.0.1`)
    - [ ] Test Redis connection via Docker CLI
    - [ ] Verify all 10 Redis tools operational

2.  **Complete bmad-mcp testing**
    - [ ] Test `bmad-task action="status"`
    - [ ] Test workflow stage transitions (start → submit → approve)
    - [ ] Align config across `.kilocode/`, `.clinerules/`, `.gemini/`

3.  **Add Firecrawl API key**
    - [ ] Check GitHub Secrets for `FIRECRAWL_API_KEY`
    - [ ] Add to local `.env` if needed
    - [ ] Test `firecrawl_search` functionality

4.  **Run full verification**
    - [ ] Execute verification checklist
    - [ ] Document results in `mcp-verification-results.md`

## 4. Verification

- [ ] Automated Test: Run MCP verification checklist
- [ ] Manual Check: Test each server's critical functions

---

### Original Document: Architecture

### Server Inventory (10 servers)

| Server              | Command       | Status      | Purpose                                |
| ------------------- | ------------- | ----------- | -------------------------------------- |
| ONE-AND-ONLY-REDIS  | node (custom) | ⚠️ Partial  | Project-isolated Redis operations      |
| filesystem-projects | npx           | ✅ Pass     | R/W to projects directory              |
| filesystem-agentic  | npx           | ✅ Pass     | Read-only to agentic templates         |
| memory              | npx           | ✅ Pass     | Knowledge graph for context            |
| git                 | npx           | ✅ Pass     | Git repository operations              |
| github              | npx           | ✅ Pass     | GitHub API integration                 |
| time                | uvx           | ✅ Pass     | Time/timezone operations               |
| fetch               | uvx           | ✅ Pass     | HTTP requests                          |
| bmad-mcp            | npx           | ⚠️ Partial  | BMAD workflow (56% agent coverage)     |
| firecrawl-mcp       | npx           | ❓ Untested | Web scraping (needs FIRECRAWL_API_KEY) |

**Pass rate:** 8/10 (80%)

### Security Configuration (already applied)

- `bmad-mcp` wildcard `"*"` → `["bmad-task"]` (security fix)
- Path validation enabled in `.kilocode/mcp.json` — allows only `projects/` and `vscodeportable/agentic/`

### Environment Variables

| Variable            | Source                            | Required For       |
| ------------------- | --------------------------------- | ------------------ |
| `REDIS_URL`         | `.env`                            | ONE-AND-ONLY-REDIS |
| `PROJECT_NAME`      | `.env`                            | ONE-AND-ONLY-REDIS |
| `GITHUB_TOKEN`      | `gh auth token` or CI auto-inject | github             |
| `FIRECRAWL_API_KEY` | GitHub Secrets                    | firecrawl-mcp      |

---

## 2. BMAD Framework Coverage

`bmad-mcp` covers ~56% of `_bmad/bmm/` agents (5/9). Missing: Analyst, UX Designer, Quick Flow Solo Dev, Tech Writer.

**Recommendation:** For full BMAD coverage use `_bmad/bmm/` files directly. Use `bmad-mcp` only for quick simplified orchestration.

---

## 3. Installation Procedures

### Redis (Custom Implementation)

The official `@modelcontextprotocol/server-redis` package does not exist. Custom server at [`.kilocode/mcp-servers/redis-server.js`](.kilocode/mcp-servers/redis-server.js) supports:

- **Local**: `REDIS_URL=redis://localhost:6379`
- **Cloud**: `UPSTASH_REDIS_REST_URL` + `UPSTASH_REDIS_REST_TOKEN`

**Start Docker Redis:**

```bash
# With persistence
docker run -d --name redis-local -p 6379:6379 \
  -v redis-data:/data redis:7-alpine \
  redis-server --appendonly yes
```

Or use `docker-compose.redis.yml`:

```yaml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    container_name: redis-local
    ports: ['6379:6379']
    volumes: [redis-data:/data]
    command: redis-server --appendonly yes
    restart: unless-stopped
volumes:
  redis-data:
```

**Install npm dependencies:**

```bash
npm install @modelcontextprotocol/server ioredis
```

**Add to `.env`:**

```env
REDIS_URL=redis://localhost:6379
PROJECT_NAME=marketing.tvoje.info
```

### Post-install Verification

```bash
# Verify Redis container
docker ps --filter name=redis-local
docker exec redis-local redis-cli ping   # → PONG

# Verify npm packages
npm list ioredis @modelcontextprotocol/server

# Validate mcp.json
node -e "JSON.parse(require('fs').readFileSync('.kilocode/mcp.json'))" && echo "OK"

# Test Redis MCP server directly
node .kilocode/mcp-servers/redis-server.js
# Expected: [Redis MCP] Connected to Redis successfully
```

---

## 4. Remaining Blockers

### P1 — Redis Node.js Connection Fix

**Root cause:** `redis-server.js` connects to `127.0.0.1:6379` where WSL2 requires auth, but Docker Redis is on `0.0.0.0:6379`.

**Fix in [`.kilocode/mcp-servers/redis-server.js`](.kilocode/mcp-servers/redis-server.js):**

```javascript
const redis = new Redis({
  host: '0.0.0.0', // Use Docker interface explicitly
  port: 6379,
});
```

**Acceptance criteria:**

- [ ] `redis_ping` returns `PONG`
- [ ] All 10 Redis tools operational

### P1 — bmad-mcp Testing and Alignment

**Test sequence:**

```bash
bmad-task action="status"
bmad-task action="start" objective="Test" cwd="."
bmad-task action="submit" session_id="<id>" stage="po" claude_result="test"
```

**Acceptance criteria:**

- [ ] Server responds to `bmad-task action="status"`
- [ ] Workflow stage transitions work (start → submit → approve)
- [ ] Config aligned across `.kilocode/`, `.clinerules/`, `.gemini/`

### P2 — Firecrawl API Key

1. Check GitHub Secrets for `FIRECRAWL_API_KEY`
2. Add to local `.env` if needed: `FIRECRAWL_API_KEY=fc-xxxx`
3. Test: `firecrawl_search query="test" limit=1`

---

## 5. Full Verification Checklist

| Server              | Test Command                                | Expected        |
| ------------------- | ------------------------------------------- | --------------- |
| ONE-AND-ONLY-REDIS  | `redis_ping`                                | `PONG`          |
| filesystem-projects | `list_directory path="."`                   | Dir listing     |
| filesystem-agentic  | `read_text_file path="README.md"`           | File contents   |
| memory              | `read_graph`                                | JSON graph      |
| git                 | `git_status`                                | Repo status     |
| github              | `search_repositories query="user:pkoka888"` | Repo list       |
| time                | `get_current_time timezone="Europe/Prague"` | Current time    |
| fetch               | `fetch url="https://httpbin.org/get"`       | Page content    |
| bmad-mcp            | `bmad-task action="status"`                 | Status response |
| firecrawl-mcp       | `firecrawl_search query="test" limit=1`     | Search results  |

**After completing blockers:** Update [`.kilocode/rules/memory-bank/tech.md`](.kilocode/rules/memory-bank/tech.md) and [`plans/mcp-verification-results.md`](plans/mcp-verification-results.md).

---

## Related Documents

| Document                                                                     | Purpose              |
| ---------------------------------------------------------------------------- | -------------------- |
| [`.kilocode/mcp.json`](.kilocode/mcp.json)                                   | Authoritative config |
| [`plans/mcp-verification-checklist.md`](plans/mcp-verification-checklist.md) | Detailed test cases  |
| [`plans/mcp-verification-results.md`](plans/mcp-verification-results.md)     | Test results         |
| [`plans/.archive/mcp-server-consolidation-plan.md`](plans/.archive/)         | Archived source      |
| [`plans/.archive/mcp-servers-installation-plan.md`](plans/.archive/)         | Archived source      |
