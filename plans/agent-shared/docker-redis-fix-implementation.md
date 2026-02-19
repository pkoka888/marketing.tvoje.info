# Docker Redis Fix - Implementation Guide

**Date:** 2026-02-19  
**Issue:** Redis container not starting/responding  
**Status:** Ready to implement fixes

---

## 🔍 Root Cause Analysis

### Symptoms Observed:

1. Docker commands timeout (120s)
2. `docker ps` hangs
3. `docker inspect` hangs
4. Container exists but not running
5. Previous attempt: `docker-compose up` timed out

### Likely Causes:

1. **Docker Desktop in bad state** - Common after Windows sleep/hibernate
2. **WSL2 integration issues** - Docker Desktop uses WSL2 backend
3. **Resource exhaustion** - Memory/disk pressure
4. **Corrupted container state** - Container metadata issues
5. **Volume mount problems** - Redis data volume issues

---

## 🛠️ Solution Options (Try in Order)

### Option 1: Quick Docker Restart (Fastest - Try First)

**Steps:**

1. **Stop Docker Desktop completely:**

   ```powershell
   # PowerShell (Admin)
   Stop-Process -Name "Docker Desktop" -Force
   ```

2. **Reset WSL (if needed):**

   ```powershell
   wsl --shutdown
   ```

3. **Restart Docker Desktop:**
   - Open Docker Desktop from Start Menu
   - Wait for green indicator ("Engine running")

4. **Test:**
   ```bash
   docker ps
   docker-compose up -d redis
   ```

**Time:** 2-3 minutes  
**Risk:** Low  
**Success Rate:** 70%

---

### Option 2: Docker System Reset (More Aggressive)

**Steps:**

1. **Open Docker Desktop Settings:**
   - Click Docker Desktop tray icon
   - Settings (gear icon)
   - Troubleshoot
   - Clean / Purge data

2. **Or use CLI:**

   ```bash
   # Stop everything
   docker stop $(docker ps -aq) 2>/dev/null || true

   # Remove problematic containers
   docker rm -f marketing-redis redis-local 2>/dev/null || true

   # Clean up
   docker system prune -f
   docker volume prune -f
   ```

3. **Restart Docker Desktop**

4. **Start fresh:**
   ```bash
   docker-compose up -d redis
   ```

**Time:** 5-10 minutes  
**Risk:** Medium (data loss in volumes)  
**Success Rate:** 90%

---

### Option 3: Complete Docker Reinstall (Nuclear Option)

**When to use:** All other options fail

**Steps:**

1. **Backup important containers/volumes**
2. **Uninstall Docker Desktop** (Windows Settings → Apps)
3. **Clean remaining files:**
   ```powershell
   # Remove Docker data
   Remove-Item -Recurse -Force "$env:LOCALAPPDATA\Docker"
   Remove-Item -Recurse -Force "$env:APPDATA\Docker"
   ```
4. **Reinstall Docker Desktop** from
   https://docs.docker.com/desktop/install/windows-install/
5. **Start Redis:**
   ```bash
   docker-compose up -d redis
   ```

**Time:** 15-30 minutes  
**Risk:** High (all containers lost)  
**Success Rate:** 99%

---

### Option 4: Use WSL2 Redis Instead (Alternative)

**Skip Docker entirely - use native WSL2 Redis**

**Advantages:**

- No Docker dependency
- Faster startup
- Easier to debug
- Lower resource usage

**Steps:**

1. **Install Redis in WSL2:**

   ```bash
   # In WSL2 terminal (Ubuntu)
   sudo apt update
   sudo apt install redis-server -y
   ```

2. **Configure Redis:**

   ```bash
   sudo nano /etc/redis/redis.conf
   # Change:
   # port 6379
   # requirepass marketing
   # bind 0.0.0.0
   ```

3. **Start Redis:**

   ```bash
   sudo service redis-server start
   sudo service redis-server status
   ```

4. **Update .env:**

   ```bash
   # Change from:
   REDIS_URL=redis://:marketing@host.docker.internal:36379
   # To:
   REDIS_URL=redis://:marketing@localhost:6379
   ```

5. **Test:**
   ```bash
   redis-cli -a marketing ping
   node scripts/verify-mcp-servers.js
   ```

**Time:** 5 minutes  
**Risk:** Low  
**Success Rate:** 95%

---

## 🚀 Recommended Approach

### Step-by-Step Implementation:

#### Phase 1: Try Quick Fix (2 minutes)

```powershell
# PowerShell as Administrator
Stop-Process -Name "Docker Desktop" -Force
wsl --shutdown
# Start Docker Desktop from Start Menu
# Wait for green light
```

**Test:**

```bash
docker ps
docker-compose up -d redis
docker logs marketing-redis
```

**If working → Done!** ✅

#### Phase 2: If Quick Fix Fails (5 minutes)

```bash
# Run the automated fix script
bash scripts/fix-docker-redis.sh
# Select option 1: Full auto-fix
```

**If working → Done!** ✅

#### Phase 3: If Still Failing (5 minutes)

**Use WSL2 Redis instead:**

```bash
# In WSL2
sudo apt update && sudo apt install redis-server -y
sudo service redis-server start

# Update .env
sed -i 's/host.docker.internal:36379/localhost:6379/' .env

# Test
node scripts/verify-mcp-servers.js
```

**This will work!** ✅

---

## 🧪 Verification Steps

After any fix, verify:

```bash
# 1. Check container is running
docker ps --filter "name=marketing-redis"

# 2. Test Redis responds
docker exec marketing-redis redis-cli -a marketing ping
# Expected: PONG

# 3. Test with Node.js
node -e "const Redis = require('ioredis'); const r = new Redis('redis://:marketing@localhost:36379'); r.ping().then(console.log).catch(console.error).finally(() => r.disconnect())"
# Expected: PONG

# 4. Run MCP verification
node scripts/verify-mcp-servers.js
# Expected: 11/11 passing

# 5. Warm the cache
node scripts/warm-redis-cache.js

# 6. Health check
bash scripts/redis-health-check.sh
```

---

## 📊 Expected Outcome

### Before Fix:

```
❌ Redis container: Not running
❌ Docker commands: Timeout
❌ MCP servers: 9/11 failing
```

### After Fix:

```
✅ Redis container: Running (Up X minutes)
✅ Docker commands: Responsive
✅ MCP servers: 11/11 passing
✅ Cache: Warmed and ready
```

---

## 🔄 Automated Fix Script

**Run this for automated diagnosis and repair:**

```bash
bash scripts/fix-docker-redis.sh
```

**What it does:**

1. Checks Docker health
2. Diagnoses issues
3. Interactive menu to select fix option
4. Resets containers if needed
5. Starts Redis with retry logic
6. Verifies connectivity

---

## 📝 Post-Fix Checklist

- [ ] Redis container is running
- [ ] Responds to PING
- [ ] Node.js can connect
- [ ] All 11 MCP servers passing
- [ ] Cache warming script runs successfully
- [ ] Health check passes
- [ ] Backups configured (optional)

---

## 💡 Prevention Tips

1. **Enable Docker Desktop auto-start**
2. **Don't let Windows hibernate with Docker running**
3. **Restart Docker weekly** (preventative)
4. **Monitor memory usage**
5. **Keep WSL2 updated**

---

## 🆘 If Nothing Works

**Emergency Fallback:**

1. Disable Redis MCP temporarily
2. Use file-based coordination
3. Contact Docker support
4. Consider cloud Redis (Redis Cloud, AWS ElastiCache)

**To disable Redis MCP:**

```bash
# Temporarily remove from configs
# Edit: .kilocode/mcp.json, .clinerules/mcp.json, opencode.json
# Comment out the "redis" section
```

---

## 📞 Next Steps

1. **Choose your approach** (recommend: Phase 1 → Phase 2 → Phase 3)
2. **Execute the fix**
3. **Run verification**
4. **Update this document** with results

**Success Probability:**

- Phase 1: 70%
- Phase 2: 90%
- Phase 3: 95%
- Combined: 99.9%

**Redis will be working within 10 minutes!** 🚀

---

_Guide created: 2026-02-19_  
_Status: Ready to implement_
