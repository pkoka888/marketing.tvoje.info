# Security Architecture v1 - 2026 Best Practices

## API Key Status (Last Verified: 2026-02-18)

### ✅ Working Keys (9)

| Key                       | Status       | Purpose                                   |
| ------------------------- | ------------ | ----------------------------------------- |
| OPENROUTER_API_KEY        | ✅ OK        | Free LLM (minimax, glm4, qwen3, deepseek) |
| GROQ_API_KEY              | ✅ OK        | Fast LLM fallback                         |
| GEMINI_API_KEY            | ✅ OK (new!) | Google AI (gemini-2.5-flash/pro)          |
| OPENAI_API_KEY            | ✅ OK        | GPT-4o models                             |
| ROUTEWAY_API_KEY          | ✅ OK        | Alternative gateway (15+ free models)     |
| GITHUB_TOKEN              | ✅ OK        | CI/CD automation                          |
| PUBLIC_SITE_URL           | ✅ Present   | SEO                                       |
| PUBLIC_FORMSPREE_ENDPOINT | ✅ Present   | Forms                                     |
| PUBLIC_PLAUSIBLE_DOMAIN   | ✅ Present   | Analytics                                 |

### ⏭️ GitHub Secrets Only (by design)

| Key                | Location   | Rationale                   |
| ------------------ | ---------- | --------------------------- |
| TS_OAUTH_CLIENT_ID | GH Secrets | CI/CD only (Tailscale step) |
| TS_OAUTH_SECRET    | GH Secrets | CI/CD only                  |
| VPS_IP             | GH Secrets | Deploy workflows only       |
| VPS_USER           | GH Secrets | Deploy workflows only       |
| VPS_SSH_PORT       | GH Secrets | Deploy workflows only       |
| VPS_SSH_KEY        | GH Secrets | Private key — NEVER in .env |

### ❌ Keys Needing Attention

| Key               | Issue                                     | Recommendation        |
| ----------------- | ----------------------------------------- | --------------------- |
| NVIDIA_API_KEY    | Endpoint fixed (integrate.api.nvidia.com) | Verify key validity   |
| FIRECRAWL_API_KEY | 404                                       | Verify account status |

---

## Single Source of Truth Architecture

```
.env (gitignored)
    ↓
GitHub Secrets (CI/CD)
    ↓
Environment Variables (Runtime)
    ↓
All Configs (LiteLLM, MCP, Scripts)
```

### Key Files Using This Pattern

- `litellm/.env` - References ${VAR} from main .env
- `litellm/proxy_config.yaml` - Uses os.environ/VAR
- All MCP configs - Load from env vars

---

## 2026 Security Best Practices

### MCP Server Security

1. **Authentication**
   - OAuth 2.1 with mTLS for client authentication
   - Per-request authorization (not just session start)
   - Temporary scoped tokens with regular rotation
   - Fine-grained RBAC (Role-Based Access Control)

2. **Network Security**
   - Network segmentation (VPC subnets)
   - Service meshes for identity traffic
   - WAFs and API gateways
   - mTLS encryption for all service-to-service

3. **Operational Security**
   - Audit logging for all MCP calls
   - Rate limiting per client
   - Input validation and sanitization
   - Sandbox execution environments

### Script Protection

1. **Production Scripts** (non-editable by agents)
   - Mark with `# @protected` comment
   - Store in `scripts/protected/` directory
   - Add to `.gitignore` for production
   - Use file permissions (read-only)

2. **Version Control**
   - All production scripts in git with tags
   - Require PR review for changes
   - Add to .gitmodules for isolation

---

## Alternative LLM Providers (Free Models)

### Routeway (15+ Free Models)

```
nemotron-3-nano-30b-a3b:free
devstral-2-2512:free
kimi-k2-0905:free
minimax-m2:free
deepseek-r1:free
glm-4.5-air:free
llama-3.3-70b-instruct:free
llama-3.2-3b-instruct:free
```

Rate limits: 20 req/min, 200 req/day (free tier)

### OpenRouter (Current Primary)

```
minimax-minimax-m2.1
z-ai/glm-4.7:free
qwen/qwen3-coder:free
deepseek/deepseek-r1-0528:free
```

---

## Agent Authentication

### Cline

- OAuth (Google/GitHub) - tokens stored in IDE secret storage
- BYOK: Direct API keys from providers

### Kilo Code

- OAuth (Google) - browser-based flow
- Token-based (found in .env: KILOCODE_API_KEY)

---

## Recommendations

### Immediate Actions

1. ~~Add TS*OAUTH*\_ and VPS\_\_ keys to .env~~ → Kept in GH Secrets only (by design)
2. ~~Verify NVIDIA API endpoint~~ → Fixed to integrate.api.nvidia.com
3. Check Firecrawl account status
4. Verify `.env` is in `.gitignore` and was never committed

### Security Hardening

1. Create `scripts/protected/` for critical scripts
2. Add MCP server authentication config
3. Implement audit logging

### Future Enhancements

1. Add mTLS for LiteLLM
2. Implement RBAC for MCP tools
3. Add rate limiting per agent

---

## Version Control Plan

### For Project Artifacts

- Use semantic versioning (v1.0.0)
- Tag releases in git
- Require PR reviews

### For Agent Configurations

- Track changes in .kilocode/rules/
- Mirror to .agents/rules/ and .clinerules/
- Run verification script after changes

### For Secrets

- NEVER commit real secrets
- Use .env.example for template
- Sync from .env to GitHub Secrets
