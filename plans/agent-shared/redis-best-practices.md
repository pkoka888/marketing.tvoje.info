# Redis Best Practices for marketing.tvoje.info

**Date:** 2026-02-19  
**Context:** MCP Server Coordination & Caching

---

## 🎯 Executive Summary

**Recommendation:** Use **DB 0 with key prefixes** (current setup is good!) +
implement proper backup/flush procedures.

---

## 1. Database Selection Strategy

### Option A: Multiple DBs (DB 0, DB 1, DB 2...)

```bash
# Not recommended for this use case
redis-cli SELECT 1  # Switch to DB 1
redis-cli SELECT 2  # Switch to DB 2
```

**Pros:**

- Logical separation
- Easy to flush one DB

**Cons:**

- Not supported by Redis Cluster
- Harder to manage permissions
- Confusing with key prefixes already in place

### Option B: Single DB with Prefixes (✅ RECOMMENDED)

```bash
# Current approach - KEEP THIS
project:marketing-tvoje-info:rate-limit:user123
project:marketing-tvoje-info:cache:page-home
project:marketing-tvoje-info:session:abc123
```

**Pros:**

- ✅ Works with Redis Cluster
- ✅ Clear ownership per project
- ✅ Already implemented in your code
- ✅ Easier backup/restore per project

**Cons:**

- Slightly more memory for prefixes

### ✅ Verdict: Stick with Option B (Current Setup)

Your `redis-server.js` already uses:

```javascript
const KEY_PREFIX = `project:${PROJECT_NAME}:`;
```

**This is the industry best practice!**

---

## 2. When to Clean/Flush Redis Data

### 🔴 NEVER Flush All (FLUSHALL)

```bash
# DANGEROUS - Don't do this!
redis-cli FLUSHALL
```

**Why:** Affects all projects using this Redis instance

### 🟢 Safe Options:

#### Option 1: Flush by Pattern (Recommended)

```bash
# Only delete keys for your project
redis-cli --scan --pattern "project:marketing-tvoje-info:*" | xargs redis-cli DEL
```

#### Option 2: Use Different Redis Instances

```yaml
# docker-compose.yml - Separate instances per environment
services:
  redis-dev:
    container_name: marketing-redis-dev
    ports:
      - '36379:6379'

  redis-prod:
    container_name: marketing-redis-prod
    ports:
      - '36380:6379'
```

#### Option 3: Time-Based Expiration (Best for Caching)

```javascript
// In your code - add TTL to all cache keys
redis.set(key, value, 'EX', 3600); // 1 hour expiration
```

---

## 3. Cache Warming Strategy

### What is Cache Warming?

Pre-populating cache with frequently accessed data after restart.

### Implementation:

#### Script: `scripts/warm-redis-cache.js`

```javascript
#!/usr/bin/env node
/**
 * Redis Cache Warming Script
 * Pre-populates cache after Redis restart
 */

import Redis from 'ioredis';

const redis = new Redis('redis://:marketing@localhost:36379');
const PROJECT_NAME = 'marketing-tvoje-info';
const KEY_PREFIX = `project:${PROJECT_NAME}:`;

async function warmCache() {
  console.log('🔥 Warming up Redis cache...\n');

  // 1. Warm project metadata
  await redis.setex(`${KEY_PREFIX}meta:version`, 3600, '1.0.0');
  console.log('✅ Project metadata cached');

  // 2. Warm rate limit counters (initialize to 0)
  await redis.setex(`${KEY_PREFIX}rate-limit:daily:count`, 86400, '0');
  console.log('✅ Rate limit counters initialized');

  // 3. Warm common MCP tool responses
  const commonTools = ['redis_ping', 'redis_info'];
  for (const tool of commonTools) {
    await redis.setex(`${KEY_PREFIX}tool:${tool}`, 300, 'ready');
  }
  console.log('✅ Common tool states cached');

  // 4. Set last-warmed timestamp
  await redis.set(`${KEY_PREFIX}meta:last-warmed`, new Date().toISOString());

  console.log('\n✨ Cache warming complete!');
  redis.disconnect();
}

warmCache().catch(console.error);
```

### When to Run:

- After Redis restart
- After code deployment
- Scheduled: Every 6 hours

---

## 4. Persistence Configuration

### Current Setup (Good!)

```yaml
# docker-compose.yml
command: redis-server --appendonly yes --requirepass "marketing"
```

This enables **AOF (Append Only File)** persistence.

### Persistence Options:

| Method                | Pros                    | Cons                          | Use Case               |
| --------------------- | ----------------------- | ----------------------------- | ---------------------- |
| **RDB** (Snapshots)   | Compact, fast restore   | Data loss since last snapshot | Cache-only data        |
| **AOF** (Append-only) | Durable, less data loss | Larger files, slower          | Critical data          |
| **Both**              | Best of both            | More disk usage               | Production recommended |

### ✅ Recommended for Production:

```yaml
# docker-compose.yml - Production
services:
  redis:
    image: redis:alpine
    command: >
      redis-server --appendonly yes --appendfsync everysec --save 60 1000
      --requirepass "marketing" --maxmemory 256mb --maxmemory-policy allkeys-lru
```

---

## 5. Memory Management

### Current Risk:

- No memory limit set
- Could exhaust system RAM

### ✅ Fix: Add Memory Limits

```yaml
# docker-compose.yml
services:
  redis:
    image: redis:alpine
    command: >
      redis-server --appendonly yes --requirepass "marketing" --maxmemory 256mb
      --maxmemory-policy allkeys-lru
    deploy:
      resources:
        limits:
          memory: 512M
```

### Eviction Policies Explained:

| Policy           | What It Does                     | Best For                      |
| ---------------- | -------------------------------- | ----------------------------- |
| `allkeys-lru`    | Removes least recently used keys | **General caching** ✅        |
| `volatile-lru`   | Removes LRU keys with TTL set    | Mixed data (some persistent)  |
| `allkeys-random` | Random removal                   | Unpredictable access patterns |
| `noeviction`     | Returns errors when full         | **Never use for cache!**      |

**Recommendation:** `allkeys-lru` (already good default)

---

## 6. Backup & Restore Procedures

### Backup Script: `scripts/backup-redis.sh`

```bash
#!/bin/bash
# Redis Backup Script

BACKUP_DIR="./backups/redis"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

echo "💾 Backing up Redis data..."

# Method 1: Redis SAVE (creates RDB dump)
docker exec marketing-redis redis-cli -a marketing SAVE

# Copy dump file
docker cp marketing-redis:/data/dump.rdb "$BACKUP_DIR/dump_$DATE.rdb"

# Method 2: Backup AOF file
docker cp marketing-redis:/data/appendonly.aof "$BACKUP_DIR/appendonly_$DATE.aof" 2>/dev/null || true

echo "✅ Backup complete: $BACKUP_DIR/dump_$DATE.rdb"
```

### Restore Script: `scripts/restore-redis.sh`

```bash
#!/bin/bash
# Redis Restore Script

if [ -z "$1" ]; then
    echo "Usage: $0 <backup-file.rdb>"
    exit 1
fi

BACKUP_FILE="$1"

echo "🔄 Restoring Redis from $BACKUP_FILE..."

# Stop Redis
docker-compose stop redis

# Restore data file
docker cp "$BACKUP_FILE" marketing-redis:/data/dump.rdb

# Start Redis
docker-compose start redis

echo "✅ Restore complete!"
echo "Verify: docker exec marketing-redis redis-cli -a marketing ping"
```

### When to Backup:

- **Daily:** Automated at 3 AM
- **Before deployments:** Manual
- **Weekly:** Full backup to cloud storage

---

## 7. Monitoring & Maintenance

### Health Check Script: `scripts/redis-health-check.sh`

```bash
#!/bin/bash
# Redis Health Check

echo "🔍 Redis Health Check"
echo "====================="

# Check if running
if ! docker ps | grep -q marketing-redis; then
    echo "❌ Redis container is not running"
    exit 1
fi

# Check connectivity
if docker exec marketing-redis redis-cli -a marketing ping | grep -q PONG; then
    echo "✅ Redis is responding"
else
    echo "❌ Redis is not responding"
    exit 1
fi

# Memory usage
echo ""
echo "📊 Memory Usage:"
docker exec marketing-redis redis-cli -a marketing INFO memory | grep used_memory_human

# Connected clients
echo ""
echo "👥 Connected Clients:"
docker exec marketing-redis redis-cli -a marketing INFO clients | grep connected_clients

# Key count (for this project only)
echo ""
echo "🔑 Project Keys:"
docker exec marketing-redis redis-cli -a marketing EVAL "
    local keys = redis.call('keys', 'project:marketing-tvoje-info:*')
    return #keys
" 0

echo ""
echo "✅ Health check complete!"
```

---

## 8. Decision Flowchart

```
Should I flush Redis?
│
├─ Is it an emergency?
│  ├─ YES → Use pattern-specific flush (Option 1)
│  └─ NO → Continue
│
├─ Is this production?
│  ├─ YES → Backup first, then selective flush
│  └─ NO → Can flush, but prefer pattern-specific
│
├─ Do you want to clear all projects?
│  ├─ YES → Use FLUSHALL (rarely needed)
│  └─ NO → Use pattern-specific flush
│
└─ Recommended: Keep data, add TTL to new keys
```

---

## 9. Quick Fixes Summary

### Safe Flush (Your Project Only):

```bash
# Flush only marketing-tvoje-info keys
docker exec marketing-redis redis-cli -a marketing --scan --pattern "project:marketing-tvoje-info:*" | \
  xargs -r docker exec marketing-redis redis-cli -a marketing DEL
```

### Check Memory:

```bash
docker exec marketing-redis redis-cli -a marketing INFO memory
```

### Update docker-compose.yml:

```yaml
services:
  redis:
    image: redis:alpine
    container_name: marketing-redis
    ports:
      - '36379:6379'
    volumes:
      - redis_data:/data
    command: >
      redis-server --appendonly yes --appendfsync everysec --requirepass
      "marketing" --maxmemory 256mb --maxmemory-policy allkeys-lru
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
```

---

## 10. Migration Path

### Current State → Best Practice:

1. ✅ **Keep:** Single DB (0) with key prefixes
2. ✅ **Add:** Memory limits (256MB with LRU)
3. ✅ **Add:** Backup scripts
4. ✅ **Add:** Cache warming
5. ✅ **Add:** Health monitoring

### Implementation Priority:

1. **P0:** Fix Docker/Start Redis
2. **P1:** Add memory limits to docker-compose.yml
3. **P2:** Set up backup cron job
4. **P3:** Add cache warming to deployment

---

## 📋 Action Items

### Immediate (Fix Docker):

- [ ] Run `scripts/fix-docker-redis.sh`
- [ ] Or use WSL2 Redis alternative

### Short-term (This Week):

- [ ] Update `docker-compose.yml` with memory limits
- [ ] Create backup script cron job
- [ ] Test restore procedure

### Long-term (Ongoing):

- [ ] Monitor memory usage monthly
- [ ] Review eviction policy effectiveness
- [ ] Archive old backups

---

## 🎯 Bottom Line

**Current Setup:** Good foundation ✅  
**Improvements Needed:** Memory limits, backups, monitoring  
**Database Strategy:** Keep using prefixes (don't switch to multiple DBs)  
**Flushing:** Use pattern-specific deletes, never FLUSHALL

**Redis is ready for production once Docker is fixed!** 🚀

---

_Guide created: 2026-02-19_  
_For: marketing.tvoje.info Redis configuration_
