# Redis MCP Server Issue - Investigation Report

**Date:** 2026-02-19  
**Status:** ⚠️ Redis Container Not Running  
**Impact:** Redis MCP server cannot connect

---

## Problem Summary

The Redis MCP server is failing to start because **Redis is not running**. The
server keeps restarting because it cannot establish a connection.

---

## Root Cause

**Connection Refused Error:**

```
[ioredis] Unhandled error event: AggregateError [ECONNREFUSED]
Redis Error: Reached the max retries per request limit
```

**Expected:** Redis should be running on `localhost:36379` (or
`host.docker.internal:36379`) **Actual:** No Redis server is accepting
connections

---

## Investigation Steps Taken

### 1. Docker Container Status

```bash
docker ps --filter "name=redis"
# Result: No containers running

docker ps -a --filter "name=redis"
# Result:
#   redis-local       Created
#   marketing-redis   Created
```

**Finding:** Containers exist but are stopped

### 2. Docker Compose Configuration

**File:** `docker-compose.yml`

```yaml
services:
  redis:
    image: redis:alpine
    container_name: marketing-redis
    ports:
      - '36379:6379'
    command: redis-server --appendonly yes --requirepass "marketing"
```

**Finding:** Configuration is correct

### 3. Attempted Fixes

```bash
docker-compose up -d redis
# Error: Container name "/marketing-redis" already in use
docker rm -f marketing-redis redis-local
# Containers removed successfully
docker-compose up -d redis
# Command timed out after 120 seconds
```

**Finding:** Docker is having issues starting the container

### 4. Environment Configuration

**File:** `.env`

```bash
REDIS_URL=redis://:marketing@host.docker.internal:36379
REDIS_PASSWORD=marketing
```

**Finding:** Configuration is correct for Docker setup

---

## Solutions

### Option 1: Fix Docker (Recommended)

**Issue:** Docker daemon or networking problems

**Steps:**

1. Restart Docker Desktop:

   ```powershell
   # PowerShell (Admin)
   Restart-Service docker
   # Or use Docker Desktop GUI to restart
   ```

2. Prune Docker and start fresh:

   ```bash
   docker system prune -a --volumes
   docker-compose up -d redis
   ```

3. Verify:
   ```bash
   docker ps --filter "name=redis"
   # Should show: marketing-redis   Up X minutes   0.0.0.0:36379->6379/tcp
   ```

### Option 2: Use WSL2 Redis

If Docker is problematic, install Redis directly in WSL2:

```bash
# In WSL2 terminal
sudo apt update
sudo apt install redis-server
sudo service redis-server start

# Update .env to use WSL localhost
REDIS_URL=redis://:marketing@localhost:6379
```

### Option 3: Use Windows Redis

Install Redis for Windows:

1. Download from: https://github.com/microsoftarchive/redis/releases
2. Or use Chocolatey: `choco install redis-64`
3. Start Redis: `redis-server --port 36379 --requirepass marketing`
4. Update .env: `REDIS_URL=redis://:marketing@localhost:36379`

### Option 4: Disable Redis MCP (Temporary)

If Redis is not immediately needed, disable the MCP server:

**In `.kilocode/mcp.json`:**

```json
// Remove or comment out the redis section temporarily
// "redis": { ... }
```

---

## Verification Commands

Once Redis is running:

```bash
# Test with Node.js
node -e "const Redis = require('ioredis'); const r = new Redis('redis://:marketing@localhost:36379'); r.ping().then(console.log).catch(console.error).finally(() => r.disconnect())"

# Test with MCP wrapper
node .kilocode/mcp-servers/mcp-wrapper.js redis

# Full verification
node scripts/verify-mcp-servers.js
```

---

## Impact Assessment

| Feature              | Status Without Redis | Workaround                 |
| -------------------- | -------------------- | -------------------------- |
| Redis MCP Server     | ❌ Not functional    | Disable or use alternative |
| Rate Limiting        | ⚠️ Uses fallback     | In-memory rate limiting    |
| Project Coordination | ⚠️ Limited           | File-based coordination    |
| Caching              | ❌ Not available     | No caching layer           |

**Recommendation:** Redis is **nice-to-have** but not critical for basic
functionality. The other 10 MCP servers work fine without it.

---

## Quick Decision Tree

```
Do you need Redis features (caching, rate limiting, coordination)?
├── YES → Fix Docker (Option 1)
│   └── Still having issues? → Use WSL2 Redis (Option 2)
│
└── NO → Disable Redis MCP (Option 4)
    └── Temporarily remove from mcp.json configs
```

---

## Files Affected

- `.kilocode/mcp.json` - Redis server config
- `.clinerules/mcp.json` - Redis server config
- `opencode.json` - Redis server config
- `.env` - Redis connection URL
- `docker-compose.yml` - Redis service definition

---

## Next Steps

1. **Immediate:** Choose solution above based on your needs
2. **Short-term:** Fix Docker or install Redis locally
3. **Long-term:** Consider Redis cloud service (Redis Cloud, AWS ElastiCache)

---

## Related Issues

- Docker Desktop may need restart after Windows updates
- WSL2 integration issues can affect Docker networking
- Port 36379 might be blocked by firewall

---

**Status:** Waiting for Docker fix or alternative Redis setup  
**Priority:** Medium (Redis is optional for core functionality)
