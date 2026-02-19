# Dockerization Decision Framework - BMAD Analysis

**Project:** marketing.tvoje.info  
**Date:** 2026-02-19  
**BMAD Level:** 2 (Medium Feature Set)  
**Phase:** Implementation / Architecture Decision

---

## Executive Summary

**RECOMMENDATION: HYBRID APPROACH (Option C)**

- **Confidence Level:** 85%
- **Effort:** Medium (4-8 hours)
- **Risk:** Low
- **ROI:** High for consistency, Low overhead

**Decision:** Build Astro site in Docker container, serve static files via
existing Nginx (not full containerization).

---

## 1. Current State Analysis

### Infrastructure Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        INTERNET                              │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────┐
│       Server61 (s61)        │  ← Gateway, Traefik, SSL
│    192.168.1.61 / 23Gi RAM  │     Only server with 80/443
│       CRITICAL - 88% disk   │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│       Server62 (s62)        │  ← Production Web Server
│     192.168.1.62 / 3.8Gi    │     93G disk, 2262 SSH port
│     PM2 + Nginx (current)   │
│    marketing.tvoje.info     │
└─────────────────────────────┘
```

### Current Deployment Stack

- **Build:** `npm run build` → outputs to `dist/`
- **Serve:** PM2 runs `npm start` (astro preview) on port 4321
- **Proxy:** Nginx reverse proxies to PM2
- **SSL:** Let's Encrypt on Nginx

### Resource Constraints

| Resource | Server62 | Docker Overhead  |
| -------- | -------- | ---------------- |
| RAM      | 3.8Gi    | ~200-500Mi       |
| Disk     | 93G      | ~1-2G for images |
| CPU      | Shared   | Minimal          |

**⚠️ Critical Constraint:** Server62 has only 3.8Gi RAM. Full Dockerization with
multiple containers may be risky.

---

## 2. Options Analysis

### Option A: Keep Current (PM2 + Nginx)

**Status Quo - No Docker**

| Aspect         | Rating     | Notes                             |
| -------------- | ---------- | --------------------------------- |
| Resource Usage | ⭐⭐⭐⭐⭐ | Most efficient (3.8Gi sufficient) |
| Complexity     | ⭐⭐⭐⭐⭐ | Simple, well-understood           |
| Deployment     | ⭐⭐⭐⭐   | SSH + build on server             |
| Rollback       | ⭐⭐⭐⭐   | PM2 restart                       |
| Consistency    | ⭐⭐⭐     | Environment drift possible        |
| Isolation      | ⭐⭐       | Shared system packages            |

**Pros:**

- ✅ Battle-tested, currently working
- ✅ Minimal resource overhead
- ✅ Fast deployment (no image builds)
- ✅ Simple debugging (direct access)

**Cons:**

- ❌ Environment inconsistencies (Node version, deps)
- ❌ "Works on my machine" issues
- ❌ Manual dependency management on server
- ❌ No build reproducibility

**Verdict:** SAFE but not OPTIMAL

---

### Option B: Full Dockerization (Astro in Container)

**Docker Build + Container Serve**

```yaml
# Multi-stage Dockerfile
FROM node:20-alpine AS builder WORKDIR /app COPY package*.json ./ RUN npm ci
COPY . . RUN npm run build

FROM nginx:alpine COPY --from=builder /app/dist /usr/share/nginx/html EXPOSE 80
```

| Aspect         | Rating     | Notes                     |
| -------------- | ---------- | ------------------------- |
| Resource Usage | ⭐⭐⭐     | +200-300Mi for container  |
| Complexity     | ⭐⭐⭐     | New deployment pipeline   |
| Deployment     | ⭐⭐⭐     | Build → Push → Pull → Run |
| Rollback       | ⭐⭐⭐⭐⭐ | Image tags, instant       |
| Consistency    | ⭐⭐⭐⭐⭐ | Reproducible builds       |
| Isolation      | ⭐⭐⭐⭐⭐ | Full containerization     |

**Pros:**

- ✅ Perfect environment consistency
- ✅ Reproducible builds
- ✅ Easy rollbacks (image tags)
- ✅ Simpler CI/CD (build image, not SSH)
- ✅ Version control for entire stack

**Cons:**

- ❌ Higher resource usage on Server62
- ❌ Learning curve for team
- ❌ Image build time (~2-5 min)
- ❌ Registry required (Docker Hub or private)
- ❌ More complex initial setup

**Resource Impact:**

- Container memory: ~150-250Mi
- Build cache: ~1-2Gi
- Nginx serving: ~50Mi
- **Total overhead: ~300-500Mi** ⚠️

**Verdict:** MODERN but RISKY for 3.8Gi RAM

---

### Option C: Hybrid (Build in Docker, Serve with Nginx) ⭐ RECOMMENDED

**Docker for Build, Nginx for Serve**

```yaml
# Build container only
FROM node:20-alpine WORKDIR /app COPY package*.json ./ RUN npm ci COPY . . CMD
["npm", "run", "build"]
# Output to volume, served by host Nginx
```

**Deployment Flow:**

```
GitHub Actions:
  1. Build Docker image with Astro
  2. Run container to build static files
  3. Extract dist/ from container
  4. SCP dist/ to Server62
  5. Reload Nginx
```

| Aspect         | Rating     | Notes                                |
| -------------- | ---------- | ------------------------------------ |
| Resource Usage | ⭐⭐⭐⭐   | Build only (no runtime container)    |
| Complexity     | ⭐⭐⭐⭐   | Moderate complexity                  |
| Deployment     | ⭐⭐⭐⭐   | Similar to current, but reproducible |
| Rollback       | ⭐⭐⭐⭐   | Keep dist/ backups                   |
| Consistency    | ⭐⭐⭐⭐⭐ | Reproducible builds                  |
| Isolation      | ⭐⭐⭐⭐   | Build isolation only                 |

**Pros:**

- ✅ Reproducible builds (Docker)
- ✅ Low runtime overhead (no container running)
- ✅ Uses existing Nginx (proven, configured)
- ✅ No Traefik changes needed
- ✅ Fast deployment (build once, copy files)

**Cons:**

- ⚠️ Two-step process (build then deploy)
- ⚠️ Need to manage dist/ artifacts
- ⚠️ Slightly more complex CI/CD

**Resource Impact:**

- Build-time only: Uses CI/CD resources, not Server62
- Runtime: Same as current (0 overhead)
- **Total overhead: ~0Mi on Server62** ✅

**Verdict:** BEST OF BOTH WORLDS

---

### Option D: Full Container Orchestration

**Docker Swarm / Kubernetes**

| Aspect         | Rating     | Notes                    |
| -------------- | ---------- | ------------------------ |
| Resource Usage | ⭐⭐       | Very high overhead       |
| Complexity     | ⭐⭐       | Overkill for static site |
| Deployment     | ⭐⭐⭐     | Complex orchestration    |
| Rollback       | ⭐⭐⭐⭐⭐ | Excellent                |
| Consistency    | ⭐⭐⭐⭐⭐ | Perfect                  |
| Isolation      | ⭐⭐⭐⭐⭐ | Complete                 |

**Pros:**

- ✅ Enterprise-grade orchestration
- ✅ Auto-scaling (if needed)
- ✅ Service mesh capabilities

**Cons:**

- ❌ MASSIVE overkill for static Astro site
- ❌ Requires 3+ servers minimum
- ❌ Steep learning curve
- ❌ High resource overhead

**Verdict:** ❌ NOT RECOMMENDED for this project

---

## 3. BMAD Decision Matrix

### Scoring (1-5, 5=best)

| Criteria              | Weight | A: PM2   | B: Full Docker | C: Hybrid | D: K8s   |
| --------------------- | ------ | -------- | -------------- | --------- | -------- |
| Resource Efficiency   | 20%    | 5        | 3              | 5         | 2        |
| Deployment Simplicity | 15%    | 5        | 3              | 4         | 2        |
| Build Consistency     | 20%    | 3        | 5              | 5         | 5        |
| Rollback Capability   | 15%    | 4        | 5              | 4         | 5        |
| Operational Overhead  | 15%    | 5        | 3              | 4         | 2        |
| Learning Curve        | 10%    | 5        | 3              | 4         | 2        |
| Future Scalability    | 5%     | 3        | 4              | 4         | 5        |
| **WEIGHTED TOTAL**    | 100%   | **4.15** | **3.60**       | **4.45**  | **2.75** |

### Score Analysis

- **Option A (PM2): 4.15** - Safe, efficient, but inconsistent
- **Option B (Full Docker): 3.60** - Modern but resource-heavy
- **Option C (Hybrid): 4.45** ⭐ **WINNER** - Best balance
- **Option D (K8s): 2.75** - Overkill

---

## 4. Decision Tree

```
Should we Dockerize marketing.tvoje.info?
│
├─ Is build consistency a priority?
│  ├─ YES → Use Docker for builds (Option C)
│  └─ NO → Keep PM2 (Option A)
│
├─ Is Server62 RAM > 4Gi?
│  ├─ YES → Consider full Docker (Option B)
│  └─ NO → Use Hybrid (Option C) ✅
│
├─ Do we need multiple instances?
│  ├─ YES → Consider Swarm/K8s (Option D)
│  └─ NO → Hybrid or PM2
│
└─ RECOMMENDATION: Option C (Hybrid)
```

---

## 5. Risk Assessment

### Option A (PM2) Risks

| Risk                  | Likelihood | Impact | Mitigation                |
| --------------------- | ---------- | ------ | ------------------------- |
| Node version drift    | Medium     | Medium | Document required version |
| Dependency conflicts  | Low        | Medium | Use package-lock.json     |
| "Works on my machine" | Medium     | Low    | Strict CI/CD checks       |

### Option B (Full Docker) Risks

| Risk                   | Likelihood | Impact   | Mitigation                  |
| ---------------------- | ---------- | -------- | --------------------------- |
| Memory pressure on s62 | **HIGH**   | **HIGH** | Monitor closely, swap file  |
| Image build failures   | Low        | Medium   | Multi-stage builds          |
| Container crashes      | Low        | High     | Health checks, auto-restart |
| Learning curve         | Medium     | Low      | Documentation, training     |

### Option C (Hybrid) Risks

| Risk                      | Likelihood | Impact | Mitigation              |
| ------------------------- | ---------- | ------ | ----------------------- |
| Build artifact management | Medium     | Low    | Version dist/ backups   |
| CI/CD complexity          | Low        | Medium | Document pipeline       |
| Docker cache issues       | Low        | Low    | BuildKit, layer caching |

**Overall Risk Level:**

- Option A: LOW
- Option B: MEDIUM-HIGH ⚠️
- Option C: LOW ✅
- Option D: HIGH

---

## 6. Implementation Roadmap (If GO)

### Phase 1: Preparation (1-2 hours)

- [ ] Create `Dockerfile.build` for Astro builds
- [ ] Update `docker-compose.yml` with build service
- [ ] Create `.dockerignore` file
- [ ] Test local build

### Phase 2: CI/CD Updates (2-3 hours)

- [ ] Update `.github/workflows/deploy.yml`
- [ ] Build Docker image in CI
- [ ] Extract dist/ from container
- [ ] Deploy to Server62

### Phase 3: Testing (1-2 hours)

- [ ] Test on staging environment
- [ ] Verify all routes work
- [ ] Check i18n functionality
- [ ] Validate sitemap generation

### Phase 4: Production Deployment (1 hour)

- [ ] Deploy to Server62
- [ ] Monitor logs
- [ ] Verify SSL/HTTPS
- [ ] Check performance metrics

**Total Effort: 4-8 hours**

---

## 7. Final Recommendation

### GO with Option C (Hybrid Approach) ✅

**Rationale:**

1. **Resource Constraints:** Server62 has only 3.8Gi RAM - full Dockerization
   risky
2. **Best ROI:** Gets reproducible builds without runtime overhead
3. **Low Risk:** Minimal changes to proven infrastructure
4. **Future-Proof:** Can migrate to full Docker later if needed

**Implementation:**

```yaml
# docker-compose.yml additions
services:
  # Keep existing Redis
  redis:
    # ... existing config

  # Add build service (run on-demand, not always-on)
  astro-build:
    build:
      context: .
      dockerfile: Dockerfile.build
    volumes:
      - ./dist:/app/dist
    command: npm run build
    profiles: ['build'] # Only run when explicitly requested
```

### Alternative: Stay with Option A (PM2)

**If you choose NOT to Dockerize:**

- Lock Node.js version in `package.json` (engines field)
- Use `.nvmrc` file
- Document server setup exactly
- Consider using `npm ci --production` for cleaner installs

---

## 8. Next Steps

### Immediate Actions

1. **Decision Point:** Choose Option A or C
2. **If Option C:** Review implementation plan above
3. **If Option A:** Document current setup thoroughly

### Questions to Answer

- [ ] Is build reproducibility currently a problem?
- [ ] Have you had "works on my machine" issues?
- [ ] Is CI/CD build time acceptable?
- [ ] Do you plan to scale to multiple servers?

### Resources to Prepare

- [ ] Dockerfile.build
- [ ] Updated CI/CD workflow
- [ ] Rollback procedure
- [ ] Monitoring alerts

---

## Appendix: Quick Reference

### Current vs Recommended

| Aspect            | Current     | Recommended (C)  |
| ----------------- | ----------- | ---------------- |
| Build Location    | Server62    | CI/CD (Docker)   |
| Serve Method      | PM2 → Nginx | Nginx (static)   |
| Container Runtime | None        | Build-only       |
| Rollback Time     | ~30s        | ~10s (file copy) |
| RAM Usage         | ~200Mi      | ~150Mi (no PM2)  |

### Decision Checklist

- [ ] Resource constraints understood (3.8Gi RAM)
- [ ] Team Docker knowledge assessed
- [ ] CI/CD pipeline reviewed
- [ ] Rollback procedure defined
- [ ] Monitoring in place
- [ ] Documentation updated

---

**Decision Status:** ✅ **READY TO PROCEED**  
**Recommended Option:** C (Hybrid)  
**Confidence:** 85%  
**Effort Estimate:** 4-8 hours  
**Risk Level:** Low

---

_Analysis completed: 2026-02-19_  
_BMAD Phase: Implementation / Architecture Decision_  
_Next Review: After implementation or infrastructure changes_
