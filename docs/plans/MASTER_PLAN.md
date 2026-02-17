# Master Project Plan

**Last Updated:** 2026-02-16
**Status:** ACTIVE

---

## Project 1: Marketing Portfolio Deployment

### ✅ COMPLETED

- [x] Build system fixed (removed PM2, static deploy)
- [x] All DevOps content replaced with Marketing
- [x] Theme system (5 themes)
- [x] Bilingual support (EN/CS)
- [x] Build verification passed
- [x] No "DevOps" in output

### ⏳ PENDING

- [ ] Push to main → Deploy to VPS
- [ ] Verify live site
- [ ] Test theme switcher

---

## Project 2: LiteLLM Deployment

### ✅ COMPLETED

- [x] LiteLLM config created (litellm/proxy_config.yaml)
- [x] Provider fallback configured (Groq → OpenAI → Anthropic)
- [x] Deployment script created (scripts/deploy-litellm.sh)
- [x] GitHub Actions workflow created (.github/workflows/deploy-litellm.yml)

### ⏳ PENDING

- [ ] Run deploy-litellm.sh or trigger GitHub Actions
- [ ] Verify LiteLLM health
- [ ] Test chat completion
- [ ] Update local clients to use server62

---

## Subagent Orchestration

### Agent Registry

| Agent              | Role                 | Provider   | Status   |
| ------------------ | -------------------- | ---------- | -------- |
| **Cline**          | Build validation     | npm        | ✅ Ready |
| **Kilo Code**      | Content verification | Direct     | ✅ Ready |
| **Playwright**     | Visual testing       | Browser    | ✅ Ready |
| **GitHub Actions** | Deployment           | CI/CD      | ✅ Ready |
| **Groq**           | AI verification      | Direct API | ✅ Ready |

### Execution Order

```
1. Marketing Portfolio:
   Build → Content Check → Deploy → Verify

2. LiteLLM:
   Config → Deploy Script → Server Deploy → Verify → Update Clients
```

---

## Quick Commands

### Marketing Portfolio

```bash
# Build
npm run build

# Deploy to VPS
git add . && git commit -m "Marketing portfolio ready" && git push main
```

### LiteLLM

```bash
# Deploy to server62
export GROQ_API_KEY=xxx
export LITELLM_MASTER_KEY=yyy
./scripts/deploy-litellm.sh

# Or via GitHub Actions
# Navigate to: Actions → Deploy LiteLLM → Run workflow
```

---

## Next Steps (After Deployment)

1. **Verify Marketing Site**
   - Check https://marketing.tvoje.info
   - Test theme switcher
   - Verify bilingual toggle

2. **Verify LiteLLM**
   - Test health: `curl http://server62:4000/health`
   - Test chat: `curl -X POST http://server62:4000/v1/chat/completions -d '{"model":"groq/llama-3.3-70b-versatile","messages":[{"role":"user","content":"Hi"}]}'`

3. **Update Local Clients**
   - Set `LITELLM_URL=http://server62:4000` in .env

---

## Files Created/Modified

| File                                    | Purpose                  |
| --------------------------------------- | ------------------------ |
| `docs/plans/VERIFICATION_PLAN.md`       | Portfolio verification   |
| `docs/plans/LITELLM_DEPLOYMENT_PLAN.md` | LiteLLM deployment       |
| `scripts/deploy-litellm.sh`             | Server deployment script |
| `.github/workflows/deploy-litellm.yml`  | CI/CD for LiteLLM        |
| `litellm/proxy_config.yaml`             | LiteLLM configuration    |

---

## Provider Fallback Chain

```
Groq (Primary)
  ├── llama-3.3-70b-versatile (quality)
  ├── llama-3.1-8b-instant (fast)
  └── groq/compound (agentic)
      │
      ▼ Fallback
OpenAI (Paid)
  ├── gpt-4o-mini (fast)
  └── gpt-4o (quality)
      │
      ▼ Fallback
Anthropic (Paid)
  ├── claude-3-haiku (fast)
  └── claude-3-sonnet (quality)
      │
      ▼ Fallback
Gemini (Paid)
  └── gemini-1.5-flash (balanced)
```
