# Known Infrastructure Issues

**Last Updated:** 2026-02-19

## Active Issues

### 🔴 CRITICAL: s62 Public SSH Port 2262 Unreachable

| Property | Value |
|----------|-------|
| **Server** | s62 (192.168.1.62) |
| **Issue** | Port 2262 not reachable via public IP 89.203.173.196 |
| **Confirmed** | 2026-02-12 via `debug_network.py` |
| **Impact** | GitHub Actions cannot SSH directly to s62 from public internet |
| **Workaround** | Use Tailscale (port 20) or hop through s60 (port 2260) |
| **Action Required** | Investigate ISP/router NAT forwarding rules for port 2262 |

**Evidence:**
```json
"s62": {
  "public": { "host": "89.203.173.196", "port": 2262, "reachable": false }
}
```

**Current CI/CD workarounds:**
- `automatizace.expc.cz`: Uses Tailscale (100.91.164.109:20) with public 2262 as fallback (which fails)
- `marketing.tvoje.info`: Hops through s60 (89.203.173.196:2260 → 192.168.1.62:2262 internally)

---

### ⚠️ WARNING: s61 Disk Usage at 88%

| Property | Value |
|----------|-------|
| **Server** | s61 (192.168.1.61) |
| **Issue** | Root filesystem at 88% (237 GB total) |
| **Impact** | Cannot restart failed monitoring containers, risk of service failure |
| **Action Required** | Manual cleanup by infrastructure owner |

**DO NOT** attempt automated cleanup. Risk of data loss.

---

### ⚠️ WARNING: s61 Failed Monitoring Containers

| Container | Exit Code | Port | Down Since |
|-----------|-----------|------|------------|
| dash-prometheus-1 | 255 | 9090 | ~2026-02-05 |
| dash-grafana-1 | 255 | 3000 | ~2026-02-05 |
| dash-redis-1 | 255 | 6379 | ~2026-02-05 |
| dash-app-1 | — (Created, never started) | — | — |

**Root cause:** Docker daemon restart or server reboot; containers lack `restart: unless-stopped` policy.  
**Prerequisite for fix:** Resolve disk space issue first.

---

### ℹ️ INFO: s61 Failed systemd Services

| Service | Status | Notes |
|---------|--------|-------|
| apache2.service | failed | Conflicts with Nginx — can be disabled |
| certbot.service | failed | Let's Encrypt renewal issues |
| netbox.service | failed | Running via Docker instead |
| php8.4-fpm.service | failed | Version conflict with active php8.3-fpm |

---

### ℹ️ INFO: s60 Evidence Not Yet Collected

Server60 evidence was NOT collected during the 2026-02-12 evidence session (only s61 was captured). Full evidence collection from s60 is needed to complete the infrastructure inventory.

---

## Resolved Issues

_None documented yet._
