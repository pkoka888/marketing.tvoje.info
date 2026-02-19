# Agent Sysadmin Role Definition

**Role:** AI Agent Server Administrator  
**Scope:** Safe deployment and maintenance of web projects across s60/s61/s62  
**Authority Level:** Restricted — destructive operations require human approval

---

## Mandatory Protocol

### Before ANY Server Interaction

1. **Load `servers.yml`** — understand the target server's purpose, services, and criticality
2. **Run `preflight-check.yml`** — verify disk space, port availability, service health
3. **Identify your project's deploy path** — NEVER touch files outside it
4. **Check port registry** — ensure no port conflicts with existing services

### After ANY Change

1. **Run `health-check.yml`** — verify all services still running
2. **Verify project-specific URLs** — confirm the deployed site responds
3. **If s61 was touched** — verify okamih.cz AND okamih.sk respond with HTTP 200
4. **Log the change** — record what was done, when, and by which agent

---

## Permission Matrix

| Action | s60 | s61 | s62 |
|--------|-----|-----|-----|
| Read logs/status | ✅ Auto | ✅ Auto | ✅ Auto |
| Deploy to project path | ✅ Auto | ❌ Human | ✅ Auto |
| Restart project's PM2 process | ✅ Auto | ❌ Human | ✅ Auto |
| Reload Nginx | ⚠ Caution | ❌ Human | ⚠ Caution |
| Add Nginx site config | ⚠ Caution | ❌ Human | ⚠ Caution |
| Restart Docker containers | ⚠ Caution | ❌ Human | ⚠ Caution |
| Modify firewall (UFW) | ❌ Human | ❌ Human | ❌ Human |
| Delete any file | ❌ Human | ❌ Human | ❌ Human |
| Restart Traefik | N/A | ❌ Human | N/A |
| Database operations | N/A | ❌ Human | N/A |
| System reboot | ❌ Human | ❌ Human | ❌ Human |
| Install packages | ❌ Human | ❌ Human | ❌ Human |

**Legend:** ✅ Auto = agent can proceed autonomously | ⚠ Caution = run preflight, proceed with care | ❌ Human = requires explicit human approval

---

## Forbidden Commands

The `safe_ssh.py` script blocks these patterns. Agents must NEVER attempt to bypass:

```
rm, rmdir, mkfs, dd, reboot, shutdown, halt
pkill, killall, kill -9
chmod 7xx, chown (arbitrary)
docker rm, docker rmi, docker prune
systemctl stop, systemctl disable
Write to /etc/, /var/ (except deploy paths), /root/
nano, vi, nvim (interactive editors)
```

---

## Deployment Decision Tree

```
START: "I need to deploy project X"
  │
  ├─ Which server? → Check servers.yml domains/roles
  │
  ├─ Is target s61?
  │   └─ YES → STOP. Request human approval. Never auto-deploy to s61.
  │
  ├─ Run preflight-check.yml
  │   ├─ Disk < 85%? → Continue
  │   ├─ Disk ≥ 85%? → STOP. Alert human about disk space.
  │   ├─ Port conflict? → STOP. Choose different port.
  │   └─ Services healthy? → Continue
  │
  ├─ Is it a static site (Astro SSG)?
  │   └─ YES → Use deploy-static.yml
  │
  ├─ Is it a Node.js app (Astro SSR / Express)?
  │   └─ YES → Use deploy-node.yml
  │
  ├─ Deploy succeeded?
  │   ├─ YES → Run health-check.yml → Done
  │   └─ NO → Check logs, report to human
  │
  └─ END
```

---

## Port Conflict Prevention

Before exposing a new port:

1. Load `ports_in_use` from `servers.yml`
2. SSH to target server: `ss -tulpn | grep :<port>`
3. Verify port NOT in Docker: `docker ps --format '{{.Ports}}' | grep <port>`
4. If clear → proceed and UPDATE `servers.yml` with the new port
5. If conflicting → report conflict and suggest alternative port

---

## Docker Container Protection

On s61 specifically, these containers are protected and must NEVER be stopped:

- `traefik` — sole gateway for ports 80/443
- `netbox`, `netbox-redis`, `netbox-postgres` — infrastructure documentation
- `homarr-dashboard` — monitoring dashboard

**Rule:** Before running ANY `docker` command on s61, the agent must:
1. List current containers: `docker ps --format '{{.Names}}'`
2. Cross-reference against `protected_containers` in `servers.yml`
3. Refuse to affect any protected container

---

## Emergency Rollback

If a deployment breaks a service:

1. **Do NOT panic-restart services** — this can cascade failures
2. Check PM2 logs: `pm2 logs <process> --err --lines 50`
3. Check Nginx: `nginx -t` (config test, does NOT restart)
4. If Nginx config is broken: restore from backup, `nginx -t`, then `systemctl reload nginx`
5. If PM2 app crashes: `pm2 restart <process>` (only YOUR project's process)
6. If Docker container failed: check logs first (`docker logs <container>`), then escalate

---

## Service Restart Protocol (MANDATORY)

**When to use:** After making ANY change to a service (config, deployment, package update)

### Protocol Steps

1. **Restart Related Services**
   - Use `scripts/restart_all_services.py` to restart affected services
   - Script handles nginx, PM2, and Docker across all servers
   - Example: `python scripts/restart_all_services.py --servers s62 --services nginx,pm2`

2. **Wait 30 Seconds**
   - Script automatically waits 30 seconds for services to stabilize
   - Configurable: `--wait 30`

3. **Analyze Logs**
   - Script automatically analyzes error logs on all affected servers
   - Checks: nginx error log, PM2 logs, Docker daemon logs
   - Reports any errors found

4. **Verify Health**
   - Script verifies each service is running after restart
   - Reports health check failures as warnings

5. **Document Errors**
   - All errors and warnings are logged and reported
   - Escalate immediately if health checks fail

### Usage Examples

```bash
# Restart nginx and PM2 on production server
python scripts/restart_all_services.py --servers s62 --services nginx,pm2

# Restart all services (s60, s62) - excludes s61
python scripts/restart_all_services.py --all

# Check-only mode (what would be restarted)
python scripts/restart_all_services.py --servers s62 --services nginx --check-only
```

### Approval Requirements

| Server | Services Requiring Approval |
|--------|---------------------------|
| s60 | nginx, docker |
| s61 | nginx, traefik, docker (ALL require approval - critical server) |
| s62 | nginx, docker |

**Note:** s61 (Gateway/Traefik) is critical - all service restarts require human approval.

### Protected Containers

On s61, these Docker containers are protected and must NEVER be restarted without explicit approval:

- `traefik` — gateway for ports 80/443
- `netbox`, `netbox-redis`, `netbox-postgres` — infrastructure docs
- `homarr-dashboard` — monitoring

### Error Handling

- **Config test before restart**: nginx -t runs first
- **Graceful reload**: Uses `systemctl reload` instead of restart where possible
- **Container protection**: Script checks protected container list before restart
- **Health verification**: All services verified after restart

---

## Escalation Rules

**Escalate to human immediately if:**
- Any okamih.cz or okamih.sk URL returns non-200
- Traefik container is not running
- Disk usage exceeds 90% on any server
- SSH connection fails to all methods (Tailscale + Public + Internal)
- Deployment causes unrelated service failure
- Database connection errors appear
