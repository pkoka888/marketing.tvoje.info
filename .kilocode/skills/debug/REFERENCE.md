# Debug Reference

Quick reference for common debugging commands, tools, and error patterns.

## Quick Commands

### Build Debugging

```bash
# Full build with verbose output
npm run build 2>&1 | tee build.log

# Type check only
npm run typecheck

# Lint check
npm run lint

# Check for outdated dependencies
npm outdated

# Check for vulnerable dependencies
npm audit

# Clear build cache
rm -rf node_modules/.astro
rm -rf .astro
```

### Test Debugging

```bash
# Run all tests
npm run test

# Run specific test file
npm run test -- path/to/test.ts

# Run tests with coverage
npm run test -- --coverage

# Run tests in watch mode
npm run test:watch
```

### Server Debugging

```bash
# SSH to server (Tailscale)
ssh -p 20 admin@server60
ssh -p 20 admin@server61
ssh -p 20 admin@server62

# Check Docker containers
docker ps -a
docker logs <container_name>
docker inspect <container_name>

# Check PM2 processes
pm2 status
pm2 logs
pm2 monit

# Check Nginx status
sudo systemctl status nginx
sudo nginx -t

# Check disk usage
df -h
du -sh /var/log/*
```

### MCP Debugging

```bash
# Validate MCP configuration
npm run validate:mcp

# Check Redis connection
redis-cli -h host.docker.internal -p 36379 ping

# Check Playwright
npx playwright --version
```

## Log Locations

### Local Logs

| Log Type   | Location        | Command              |
| ---------- | --------------- | -------------------- |
| Build      | Terminal output | `npm run build 2>&1` |
| Test       | Terminal output | `npm run test 2>&1`  |
| Lint       | Terminal output | `npm run lint 2>&1`  |
| Dev Server | Terminal output | `npm run dev 2>&1`   |

### Server Logs (server60, server61, server62)

| Log Type     | Location                        | SSH Command                         |
| ------------ | ------------------------------- | ----------------------------------- |
| Nginx Access | `/var/log/nginx/access.log`     | `tail -f /var/log/nginx/access.log` |
| Nginx Error  | `/var/log/nginx/error.log`      | `tail -f /var/log/nginx/error.log`  |
| PM2 Logs     | `/var/www/portfolio/.pm2/logs/` | `pm2 logs`                          |
| Auth Logs    | `/var/log/auth.log`             | `tail -f /var/log/auth.log`         |
| System Logs  | `/var/log/syslog`               | `tail -f /var/log/syslog`           |
| Docker Logs  | Container output                | `docker logs <container>`           |

### CI/CD Logs

| Source         | Location                           |
| -------------- | ---------------------------------- |
| GitHub Actions | `.github/workflows/` → Actions tab |
| Deploy Logs    | GitHub Actions → Deploy workflow   |

## Error Patterns

### Build Errors

| Error Pattern                             | Likely Cause       | Resolution                                 |
| ----------------------------------------- | ------------------ | ------------------------------------------ |
| `Cannot find module 'X'`                  | Missing dependency | `npm install X`                            |
| `Cannot find module './X'`                | Wrong import path  | Check relative path                        |
| `Type 'X' is not assignable to type 'Y'`  | Type mismatch      | Fix type definitions                       |
| `Object is possibly 'undefined'`          | Missing null check | Add null check or `!`                      |
| `Property 'X' does not exist on type 'Y'` | Missing property   | Add property or fix type                   |
| `Syntax error`                            | Invalid syntax     | Check code syntax                          |
| `Unexpected token`                        | Parser error       | Check for typos                            |
| `Out of memory`                           | Node memory limit  | `NODE_OPTIONS="--max-old-space-size=4096"` |
| `ENOENT: no such file or directory`       | File not found     | Check file path                            |
| `EACCES: permission denied`               | Permission issue   | Fix file permissions                       |

### Runtime Errors

| Error Pattern                                      | Likely Cause       | Resolution                   |
| -------------------------------------------------- | ------------------ | ---------------------------- |
| `TypeError: Cannot read property 'X' of undefined` | Null reference     | Add null check               |
| `TypeError: X is not a function`                   | Wrong type         | Check function exists        |
| `RangeError: Maximum call stack size exceeded`     | Infinite recursion | Fix recursion                |
| `RangeError: Invalid array length`                 | Invalid array      | Check array size             |
| `ReferenceError: X is not defined`                 | Undefined variable | Define variable              |
| `SyntaxError: Unexpected token`                    | Syntax error       | Fix syntax                   |
| `Network error`                                    | Connection issue   | Check network                |
| `Timeout exceeded`                                 | Slow operation     | Optimize or increase timeout |
| `CORS error`                                       | CORS policy        | Configure CORS headers       |

### Server Errors

| Error Pattern             | Likely Cause        | Resolution             |
| ------------------------- | ------------------- | ---------------------- |
| `ECONNREFUSED`            | Service not running | Start service          |
| `ETIMEDOUT`               | Connection timeout  | Check network/firewall |
| `ENOENT`                  | File not found      | Check file path        |
| `EACCES`                  | Permission denied   | Fix permissions        |
| `ENOSPC`                  | Disk full           | Clean up disk          |
| `EMFILE`                  | Too many open files | Increase ulimit        |
| `502 Bad Gateway`         | Upstream error      | Check upstream service |
| `503 Service Unavailable` | Service down        | Restart service        |
| `504 Gateway Timeout`     | Upstream timeout    | Check upstream         |

### Docker Errors

| Error Pattern                    | Likely Cause      | Resolution                 |
| -------------------------------- | ----------------- | -------------------------- |
| `Container exited with code 1`   | App crash         | Check logs                 |
| `Container exited with code 137` | OOM killed        | Increase memory            |
| `Container exited with code 255` | Network/SSH issue | Check network              |
| `Image not found`                | Missing image     | Pull/build image           |
| `Port already in use`            | Port conflict     | Stop conflicting container |
| `Volume not found`               | Missing volume    | Create volume              |

### Test Errors

| Error Pattern                           | Likely Cause | Resolution                   |
| --------------------------------------- | ------------ | ---------------------------- |
| `AssertionError: expected X to equal Y` | Logic error  | Fix code or test             |
| `Timeout of 5000ms exceeded`            | Slow test    | Optimize or increase timeout |
| `Snapshot mismatch`                     | UI change    | Update snapshot              |
| `Cannot find module`                    | Import error | Fix import path              |
| `Test not run`                          | Skipped test | Remove `.skip`               |

## Server Infrastructure

### Server Access

| Server   | IP           | Tailscale Port | Internal Port | Purpose            |
| -------- | ------------ | -------------- | ------------- | ------------------ |
| server60 | 192.168.1.60 | 20             | 2260          | Infrastructure/VPS |
| server61 | 192.168.1.61 | 20             | 2261          | Gateway/Traefik    |
| server62 | 192.168.1.62 | 20             | 2262          | Production/Web     |

### Services by Server

**server60**:

- PM2, Nginx, Docker, Node.js 20+

**server61**:

- Traefik, Nginx, Docker
- MariaDB 11.8.3, PostgreSQL 17, Redis
- PHP 8.3 FPM, GitLab Runner, Netdata, Tinyproxy

**server62**:

- PM2, Nginx, Docker, Node.js 20+
- Portfolio application

### Known Issues

| Server   | Issue                       | Priority | Status         |
| -------- | --------------------------- | -------- | -------------- |
| server61 | Disk usage 88%              | P0       | Monitoring     |
| server61 | Prometheus container failed | P1       | Needs recovery |
| server61 | Grafana container failed    | P1       | Needs recovery |
| server61 | Redis container failed      | P1       | Needs recovery |

## Debugging Tools

### Node.js Debugging

```bash
# Debug mode
NODE_OPTIONS="--inspect" npm run dev

# Memory snapshot
node --heapsnapshot-signal=SIGUSR2 index.js

# CPU profiling
node --prof index.js
node --prof-process isolate-*.log
```

### Docker Debugging

```bash
# Container shell
docker exec -it <container> /bin/sh

# Container logs (follow)
docker logs -f <container>

# Container resource usage
docker stats <container>

# Container processes
docker top <container>

# Container details
docker inspect <container>
```

### Network Debugging

```bash
# Check port usage
netstat -tlnp | grep <port>

# Check process
ps aux | grep <process>

# Check connections
ss -tunap

# DNS lookup
nslookup <domain>
dig <domain>

# HTTP request
curl -v <url>
```

### Git Debugging

```bash
# Recent changes
git log --oneline -10

# File history
git log --follow <file>

# Diff with previous commit
git diff HEAD~1

# Blame (who changed this line)
git blame <file>

# Find commit that introduced bug
git bisect start
git bisect bad
git bisect good <commit>
```

## Configuration Files

### Project Configuration

| File                  | Purpose                  |
| --------------------- | ------------------------ |
| `astro.config.mjs`    | Astro configuration      |
| `tailwind.config.mjs` | Tailwind configuration   |
| `tsconfig.json`       | TypeScript configuration |
| `package.json`        | npm dependencies         |
| `.env`                | Environment variables    |
| `.kilocode/mcp.json`  | MCP server configuration |

### Server Configuration

| File                 | Location                                 | Purpose             |
| -------------------- | ---------------------------------------- | ------------------- |
| `nginx.conf`         | `/etc/nginx/nginx.conf`                  | Nginx configuration |
| `pm2.config.js`      | `/var/www/portfolio/ecosystem.config.js` | PM2 configuration   |
| `docker-compose.yml` | Various                                  | Docker services     |

## Health Check Commands

```bash
# Full health check
npm run build && npm run test && npm run lint

# Quick health check
npm run typecheck && npm run lint

# Server health check
ssh -p 20 admin@server61 "docker ps && df -h && free -m"

# MCP health check
npm run validate:mcp
```

## Related Files

- **SKILL.md**: Main debugging skill documentation
- **WORKFLOW.md**: Step-by-step debugging workflows
- **`.kilocode/rules/memory-bank/servers.md`**: Server infrastructure reference
- **`.kilocode/rules-code/server-preservation.md`**: Server safety rules
