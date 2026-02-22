# FINAL EXECUTION PLAN - Memory & MCP Consolidation

**Generated**: 2026-02-22

---

## ARCHITECTURE DECISION

### Where to put mcp-servers?

| Location                | Size | Pros                   | Cons            |
| ----------------------- | ---- | ---------------------- | --------------- |
| **.agent/mcp-servers/** | 29KB | Single source, unified | None            |
| Root /mcp-servers/      | 29KB | Visible, standard      | Scatters config |

**Decision**: Move to `.agent/mcp-servers/` for unified single source

---

## DISCOVERY RESULTS

### 1. MCP Servers Location: `.kilocode/mcp-servers/`

- mcp-wrapper.js (loads .env)
- redis-server.js
- wrapper.bat, wrapper.sh
- lib/package.json

### 2. Docker Redis Configuration

- docker-compose.dev.yml: redis-dev service on port 6379
- docker-compose.prod.yml: production Redis
- Currently using localhost:36379 (mapped)

### 3. Antigravity Files (24KB)

- mcp.json - 12 servers
- settings.json
- README.md
- skills/astro-portfolio/

---

## EXECUTION STEPS

### STEP 1: Archive Antigravity

```bash
mv .antigravity archive/antigravity-20260222
```

### STEP 2: Move MCP Servers

```bash
mv .kilocode/mcp-servers .agent/mcp-servers
```

### STEP 3: Create JSON Symlinks

```bash
# Windows cmd
mklink .clinerules\mcp.json .agent\mcp.json
mklink .kilocode\mcp.json .agent\mcp.json
```

### STEP 4: Update Wrapper Path

Edit `.agent/mcp-servers/mcp-wrapper.js` to point to correct paths

### STEP 5: Disable Memory MCP in KILOCODE

Remove memory server from symlinked config

### STEP 6: Add Missing to CLINE

Add time, bmad-mcp to `.agent/mcp.json`

---

## MEMORY ARCHITECTURE DECISION

### Everything-Claude-Code Pattern:

```
.claude/
├── settings.json           # Config
├── contexts/              # Session contexts
│   ├── dev.md
│   ├── research.md
│   └── review.md
├── memory/               # Cross-session memory
│   └── sessions/         # Session files
└── hooks/               # Persistence hooks
```

### Recommended for This Project:

```
.agent/
├── memory/
│   ├── canonical/       # Brief files (<5KB each)
│   │   ├── brief.md
│   │   ├── product.md
│   │   ├── tech.md
│   │   └── context.md
│   ├── contexts/        # Mode-specific
│   │   ├── dev.md
│   │   ├── research.md
│   │   └── review.md
│   └── sessions/        # Cross-session
├── mcp-servers/        # MCP wrappers (moved here)
│   ├── mcp-wrapper.js
│   └── redis-server.js
└── mcp.json            # SINGLE SOURCE
```

---

## DOCKER DECISION

### Redis Configuration

| Option       | Use For       | Status                        |
| ------------ | ------------- | ----------------------------- |
| Docker Redis | Production    | ✅ In docker-compose.prod.yml |
| Local Redis  | Development   | ✅ Running on localhost:36379 |
| MCP Redis    | Rate limiting | ⚠️ Optional - add if needed   |

**Decision**: Keep both - Docker for production, local for dev

---

## READY TO EXECUTE

Reply "yes execute full" to:

1. Archive .antigravity → archive/antigravity-20260222
2. Move .kilocode/mcp-servers → .agent/mcp-servers
3. Create symlinks for mcp.json
4. Disable Memory MCP
5. Push to remote
