# Redis MCP Unification Plan

**Date**: 2026-02-17 **Status**: Draft - Pending Approval

---

## Current State Analysis

### MCP Configuration Files (4 files with Redis)

| File                    | Redis Approach              | Namespace              | Issues                                           |
| ----------------------- | --------------------------- | ---------------------- | ------------------------------------------------ |
| `.clinerules/mcp.json`  | ✅ Custom `redis-server.js` | `marketing-tvoje-info` | None                                             |
| `.kilocode/mcp.json`    | ✅ Custom `redis-server.js` | `marketing-tvoje-info` | None                                             |
| `opencode.json`         | ✅ Custom `redis-server.js` | `marketing-tvoje-info` | Has stray `astro` env var                        |
| `.antigravity/mcp.json` | ✅ Custom `redis-server.js` | `marketing_tvoje_info` | Uses `REDIS_NAMESPACE` instead of `PROJECT_NAME` |

### Redis Server (Docker)

```yaml
# docker-compose.yml
redis:
  image: redis:alpine
  ports: '36379:6379'
  command: redis-server --appendonly yes --requirepass "marketing"
```

### Current Issues

1. **Inconsistent environment variables**:
   - `.clinerules/mcp.json`: `PROJECT_NAME`
   - `.kilocode/mcp.json`: `PROJECT_NAME`
   - `opencode.json`: `PROJECT_NAME` (plus stray `astro` var)
   - `.antigravity/mcp.json`: `REDIS_NAMESPACE` (different convention)

2. **Hardcoded credentials**: Redis password stored in plaintext in
   `docker-compose.yml` and connection URLs

3. **Namespace naming inconsistency**: `marketing-tvoje-info` vs
   `marketing_tvoje_info`

4. **Missing env variable support**: Redis password should use environment
   variable

---

## Proposed Changes

### Phase 1: Environment Variable Setup

#### 1.1 Add to `.env` (gitignored)

```env
# Redis Configuration
REDIS_PASSWORD=marketing
REDIS_HOST=localhost
REDIS_PORT=36379
REDIS_URL=redis://:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}
REDIS_NAMESPACE=marketing-tvoje-info
```

#### 1.2 Add to GitHub Secrets

- `REDIS_PASSWORD` = `marketing`
- `REDIS_URL` = `redis://:marketing@localhost:36379` (for CI/CD)

#### 1.3 Add to `.env.example` (for documentation)

```env
# Redis Configuration (required for MCP)
REDIS_PASSWORD=your-redis-password
REDIS_HOST=localhost
REDIS_PORT=36379
REDIS_NAMESPACE=your-project-name
```

### Phase 2: Docker Compose Update

**Before:**

```yaml
redis:
  image: redis:alpine
  command: redis-server --appendonly yes --requirepass "marketing"
```

**After:**

```yaml
redis:
  image: redis:alpine
  container_name: marketing-redis
  ports:
    - '${REDIS_PORT:-36379}:6379'
  volumes:
    - redis_data:/data
  command:
    redis-server --appendonly yes --save 60 1000 --requirepass
    "${REDIS_PASSWORD:-marketing}"
  restart: unless-stopped
  healthcheck:
    test: ['CMD', 'redis-cli', '-a', '${REDIS_PASSWORD:-marketing}', 'ping']
    interval: 30s
    timeout: 10s
    retries: 3

volumes:
  redis_data:
```

### Phase 3: MCP Config Unification

All 4 config files should use identical Redis configuration:

```json
{
  "redis": {
    "command": "node",
    "args": [
      "C:/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/redis-server.js"
    ],
    "env": {
      "PROJECT_NAME": "marketing-tvoje-info",
      "REDIS_URL": "redis://:${REDIS_PASSWORD}@localhost:${REDIS_PORT:-36379}"
    },
    "description": "Redis MCP with project namespace isolation",
    "alwaysAllow": [
      "redis_get",
      "redis_set",
      "redis_del",
      "redis_keys",
      "redis_exists",
      "redis_ttl",
      "redis_expire",
      "redis_ping",
      "redis_info",
      "redis_list_projects"
    ]
  }
}
```

### Phase 4: redis-server.js Update

Update to read password from environment if not in URL:

```javascript
// Add support for REDIS_PASSWORD env var
function getRedisClient() {
  const redisUrl = process.env.REDIS_URL;
  const redisPassword = process.env.REDIS_PASSWORD;
  const redisHost = process.env.REDIS_HOST || 'localhost';
  const redisPort = parseInt(process.env.REDIS_PORT || '3639', 10);

  // Option 1: Use REDIS_URL if provided
  if (redisUrl) {
    return new Redis(redisUrl, {
      /* opts */
    });
  }

  // Option 2: Use individual params with password
  return new Redis({
    host: redisHost,
    port: redisPort,
    password: redisPassword,
    // ... other opts
  });
}
```

### Phase 5: Script Updates

#### 5.1 Update `scripts/verify_redis.py`

- Use `REDIS_NAMESPACE` from environment
- Default to `marketing-tvoje-info` (hyphen format)

#### 5.2 Remove or update `test_redis_auth.js`

- This was a debugging script, can be removed or updated to use env vars

---

## Files to Modify

| File                                    | Action        | Changes                                     |
| --------------------------------------- | ------------- | ------------------------------------------- |
| `.env`                                  | Create/Update | Add Redis env vars                          |
| `.env.example`                          | Update        | Add Redis template                          |
| `docker-compose.yml`                    | Update        | Use env vars, add healthcheck               |
| `.clinerules/mcp.json`                  | Update        | Ensure unified config                       |
| `.kilocode/mcp.json`                    | Update        | Ensure unified config                       |
| `opencode.json`                         | Update        | Remove stray `astro`, ensure unified config |
| `.antigravity/mcp.json`                 | Update        | Change `REDIS_NAMESPACE` to `PROJECT_NAME`  |
| `.kilocode/mcp-servers/redis-server.js` | Update        | Add REDIS_PASSWORD support                  |
| `scripts/verify_redis.py`               | Update        | Fix namespace consistency                   |

---

## GitHub Secrets to Add

Run these commands or add via GitHub UI:

```bash
gh secret set REDIS_PASSWORD --body "marketing"
gh secret set REDIS_URL --body "redis://:marketing@localhost:36379"
```

---

## Verification Steps

1. ✅ `.env` is in `.gitignore` (confirmed)
2. [ ] Stop Docker container: `docker-compose down`
3. [ ] Create/update `.env` file
4. [ ] Update `docker-compose.yml`
5. [ ] Update all MCP config files
6. [ ] Update `redis-server.js`
7. [ ] Start Docker: `docker-compose up -d`
8. [ ] Test connection: `python scripts/verify_redis.py`
9. [ ] Add GitHub secrets
10. [ ] Commit changes (excluding `.env`)

---

## Risk Assessment

| Risk                              | Mitigation                       |
| --------------------------------- | -------------------------------- |
| Breaking existing MCP connections | Test each agent after changes    |
| Environment variable not loaded   | Docker Compose auto-loads `.env` |
| Password exposure                 | `.env` is gitignored             |

---

## Rollback Plan

If issues occur:

1. Revert to hardcoded values temporarily
2. Check Docker logs: `docker logs marketing-redis`
3. Verify `.env` file exists and is readable

---

## Approval Required

- [ ] Proceed with Phase 1 (Environment setup)
- [ ] Proceed with Phase 2 (Docker update)
- [ ] Proceed with Phase 3 (MCP unification)
- [ ] Proceed with Phase 4 (redis-server.js update)
- [ ] Proceed with Phase 5 (Script updates)
- [ ] Add GitHub secrets
