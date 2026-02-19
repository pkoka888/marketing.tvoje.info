# API Keys & Secrets Inventory

# Project: marketing.tvoje.info

# Generated: 2026-02-19

# Purpose: Comprehensive inventory of all credentials

## Summary

| Category           | Count  | In .env | In GitHub Secrets | Docker Needed |
| ------------------ | ------ | ------- | ----------------- | ------------- |
| AI/LLM API Keys    | 8      | 8       | 0                 | 0             |
| Service Tokens     | 2      | 2       | 1                 | 2             |
| Application Config | 8      | 8       | 0                 | 3             |
| **Total**          | **18** | **18**  | **1**             | **5**         |

---

## Detailed Inventory

### AI/LLM API Keys (8)

| Variable Name        | Source File | Purpose                  | Provider   | Required For    | Format                    |
| -------------------- | ----------- | ------------------------ | ---------- | --------------- | ------------------------- |
| `GEMINI_API_KEY`     | .env        | Google Gemini API access | Google AI  | Local dev only  | `AIzaSy...` (39 chars)    |
| `NVIDIA_API_KEY`     | .env        | NVIDIA NIM API access    | NVIDIA     | Local dev only  | `nvapi-...` (71 chars)    |
| `OPENAI_API_KEY`     | .env        | OpenAI API access        | OpenAI     | Local dev only  | `sk-proj-...` (164 chars) |
| `OPENROUTER_API_KEY` | .env        | OpenRouter API access    | OpenRouter | Local dev only  | `sk-or-v1-...` (96 chars) |
| `KILOCODE_API_KEY`   | .env        | Kilo Code API access     | Kilo Code  | Local dev only  | JWT format                |
| `ROUTEWAY_API_KEY`   | .env        | RouteWay API access      | RouteWay   | Local dev only  | `sk-...` (96 chars)       |
| `GROQ_API_KEY`       | .env        | Groq API access          | Groq       | LiteLLM on S62  | `gsk_...` (56 chars)      |
| `FIRECRAWL_API_KEY`  | .env        | Firecrawl web scraping   | Firecrawl  | **MCP Gateway** | `fc-...` (32 chars)       |

### Service Tokens (2)

| Variable Name  | Source File | Purpose           | Used By    | Required For    | Format               |
| -------------- | ----------- | ----------------- | ---------- | --------------- | -------------------- |
| `GITHUB_TOKEN` | .env        | GitHub API access | GitHub MCP | **MCP Gateway** | `ghp_...` (40 chars) |
| `GROQ_API_KEY` | .env        | Groq LLM API      | LiteLLM    | S62 LiteLLM     | `gsk_...` (56 chars) |

### Application Configuration (8)

| Variable Name               | Source File | Purpose              | Default                                         | Required For | Notes                   |
| --------------------------- | ----------- | -------------------- | ----------------------------------------------- | ------------ | ----------------------- |
| `PROJECT_NAME`              | .env        | Project identifier   | `marketing-tvoje-info`                          | **Docker**   | Used in Redis namespace |
| `PUBLIC_SITE_URL`           | .env        | Production URL       | `https://marketing.tvoje.info`                  | **Docker**   | Build-time variable     |
| `PUBLIC_FORMSPREE_ENDPOINT` | .env        | Contact form backend | Formspree URL                                   | Nginx config | Static site feature     |
| `PUBLIC_PLAUSIBLE_DOMAIN`   | .env        | Analytics domain     | `marketing.tvoje.info`                          | Nginx config | Analytics config        |
| `PUBLIC_PLAUSIBLE_API_HOST` | .env        | Analytics host       | `https://plausible.io`                          | Nginx config | Analytics config        |
| `REDIS_PASSWORD`            | .env        | Redis auth           | `marketing`                                     | **Docker**   | **CHANGE FOR PROD**     |
| `REDIS_URL`                 | .env        | Redis connection     | `redis://:marketing@host.docker.internal:36379` | Local dev    | Docker overrides this   |
| `JWT_SECRET`                | .env        | MCP Gateway auth     | _undefined_                                     | **Docker**   | **MUST SET FOR PROD**   |

### GitHub Actions Secrets Status

#### Current Secrets (deploy.yml uses)

- ✅ `PUBLIC_SITE_URL`
- ⚠️ `VPS_HOST` - Need to add S60_HOST
- ⚠️ `VPS_PORT` - Need to add S60_PORT
- ⚠️ `VPS_SSH_KEY` - Need S60_SSH_KEY
- ⚠️ `INTERNAL_HOST` - Not needed for S60
- ⚠️ `INTERNAL_PORT` - Not needed for S60

#### Required New Secrets for S60 Docker

```yaml
# Infrastructure
S60_HOST: '89.203.173.196'
S60_PORT: '2260'
S60_USER: 'sugent'
S60_SSH_KEY: '<private_key_content>'

# Application Secrets (NEW)
REDIS_PASSWORD: '<strong_32char_password>'
JWT_SECRET: '<strong_64char_secret>'

# Service Tokens (copy from .env)
GITHUB_TOKEN: 'ghp_...'
FIRECRAWL_API_KEY: 'fc-...'
```

---

## Docker Requirements

### Required in Container Environment

| Variable            | Source        | Set In           | Used By             |
| ------------------- | ------------- | ---------------- | ------------------- |
| `PROJECT_NAME`      | GitHub Secret | `.env` on server | Redis namespace     |
| `PUBLIC_SITE_URL`   | GitHub Secret | Build arg        | Astro build         |
| `REDIS_PASSWORD`    | GitHub Secret | `.env` on server | Redis + MCP Gateway |
| `JWT_SECRET`        | GitHub Secret | `.env` on server | MCP Gateway auth    |
| `GITHUB_TOKEN`      | GitHub Secret | `.env` on server | GitHub MCP          |
| `FIRECRAWL_API_KEY` | GitHub Secret | `.env` on server | Firecrawl MCP       |

### Command to Set Secrets

```bash
# Add to GitHub Secrets (Settings > Secrets > Actions)
gh secret set S60_HOST -b"89.203.173.196"
gh secret set S60_PORT -b"2260"
gh secret set S60_USER -b"sugent"
gh secret set S60_SSH_KEY < ~/.ssh/id_rsa
gh secret set REDIS_PASSWORD -b"$(openssl rand -base64 32)"
gh secret set JWT_SECRET -b"$(openssl rand -base64 64)"
gh secret set GITHUB_TOKEN -b"ghp_..."
gh secret set FIRECRAWL_API_KEY -b"fc_..."
```

---

## Security Notes

### ⚠️ HIGH PRIORITY

1. **REDIS_PASSWORD** is currently `marketing` (weak)
   - **Action:** Generate strong password for production
   - **Command:** `openssl rand -base64 32`

2. **JWT_SECRET** is not defined
   - **Action:** Generate before first deployment
   - **Command:** `openssl rand -base64 64`

3. **GITHUB_TOKEN** has wide permissions
   - **Risk:** If leaked, full repo access
   - **Mitigation:** Use fine-grained token with minimal permissions

### Key Rotation Schedule

| Key Type          | Rotation Frequency | Last Rotated | Next Rotation |
| ----------------- | ------------------ | ------------ | ------------- |
| AI/LLM Keys       | Quarterly          | Unknown      | 2026-05-19    |
| GitHub Token      | Bi-annually        | Unknown      | 2026-08-19    |
| Service Passwords | Annually           | N/A          | 2027-02-19    |

---

## Usage Matrix

### Local Development (.env)

- All 8 AI keys
- All 4 service config vars
- Weak Redis password (acceptable for local)

### GitHub Actions

- Build: `PUBLIC_SITE_URL`
- Deploy: SSH key + host vars
- Docker: All 6 Docker-required secrets

### S60 Production (Docker)

- Redis: Requires `REDIS_PASSWORD`
- MCP Gateway: Requires `JWT_SECRET`, `GITHUB_TOKEN`, `FIRECRAWL_API_KEY`
- Astro Build: Requires `PUBLIC_SITE_URL`, `PROJECT_NAME`

---

## Files Reference

| File                  | Keys Present | Notes                           |
| --------------------- | ------------ | ------------------------------- |
| `.env`                | 18           | Main secrets file (gitignored)  |
| `.env.example`        | 18           | Template with placeholders      |
| `litellm/.env`        | 1            | References `OPENROUTER_API_KEY` |
| `docker/.env.example` | 6            | Docker-specific subset          |

---

_Generated for Docker deployment to S60_ _Last updated: 2026-02-19_
