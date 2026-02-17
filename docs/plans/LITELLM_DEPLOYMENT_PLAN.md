# LiteLLM Deployment Plan

**Created:** 2026-02-16
**Status:** READY FOR DEPLOYMENT
**Purpose:** Deploy LiteLLM proxy to server62 for unified AI access

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Kilo Code     │────▶│   LiteLLM Proxy  │────▶│   Groq API     │
│   (local)       │     │   server62:4000  │     │   (primary)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                      │
                                                      ▼
                                               ┌─────────────────┐
                                               │  Fallback       │
                                               │  Providers      │
                                               └─────────────────┘
```

---

## Subagent Assignments

### Agent 1: Config Validator

**Purpose:** Verify LiteLLM config is correct
**Commands:**

```bash
python litellm/validate_config.py
```

### Agent 2: Server Deployer

**Purpose:** Deploy LiteLLM to server62 via SSH
**Steps:**

1. SSH to server62
2. Install Python 3.11+ if needed
3. Install litellm: `pip install litellm[proxy]`
4. Create .env with GROQ_API_KEY
5. Start proxy on port 4000
6. Configure PM2 for auto-restart

### Agent 3: Health Verifier

**Purpose:** Verify LiteLLM is responding
**Commands:**

```bash
curl http://server62:4000/health
curl -X POST http://server62:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"groq/llama-3.3-70b-versatile","messages":[{"role":"user","content":"test"}]}'
```

### Agent 4: Client Updater

**Purpose:** Update clients to use server62 LiteLLM
**Steps:**

1. Update local .env: `LITELLM_URL=http://server62:4000`
2. Test with Kilo Code
3. Verify fallback works

---

## Deployment Commands

### Step 1: Install on Server62

```bash
# SSH to server62
ssh admin@100.91.164.109 -p 20

# Install Python and LiteLLM
pip install litellm[proxy] uvicorn

# Create .env
echo "GROQ_API_KEY=gsk_xxx" > .env
echo "LITELLM_MASTER_KEY=change_me" >> .env

# Start LiteLLM
litellm --config proxy_config.yaml --port 4000 --host 0.0.0.0 &
```

### Step 2: Configure PM2

```bash
pm2 start "litellm --config proxy_config.yaml --port 4000" --name litellm
pm2 save
```

### Step 3: Verify

```bash
curl http://localhost:4000/health
```

---

## Provider Configuration

| Provider  | Status      | Model                   | Rate Limit |
| --------- | ----------- | ----------------------- | ---------- |
| Groq      | ✅ Primary  | llama-3.3-70b-versatile | 30 RPM     |
| Groq      | ✅ Fast     | llama-3.1-8b-instant    | 30 RPM     |
| OpenAI    | 🔄 Fallback | gpt-4o-mini             | Paid       |
| Anthropic | 🔄 Fallback | claude-3-haiku          | Paid       |
| Gemini    | 🔄 Fallback | gemini-1.5-flash        | Paid       |

---

## Verification Checklist

- [ ] Config validated
- [ ] LiteLLM installed on server62
- [ ] PM2 process running
- [ ] Health endpoint responds
- [ ] Chat completion works
- [ ] Fallback chain works
- [ ] Local clients updated

---

## Usage

### From Local Machine

```bash
# Direct Groq (no proxy)
curl -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"Hello"}]}'

# Via LiteLLM Proxy
curl -X POST http://server62:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"groq/llama-3.3-70b-versatile","messages":[{"role":"user","content":"Hello"}]}'
```

### From Kilo Code

Update .env:

```
LITELLM_URL=http://100.91.164.109:4000
```

---

## Fallback Behavior

If Groq fails (rate limit):

1. Try llama-3.1-8b-instant (different rate limit bucket)
2. Fall back to gpt-4o-mini (if configured)
3. Return error if all fail

---

## Troubleshooting

### Issue: Connection Refused

- Check if LiteLLM is running: `pm2 status`
- Check port: `netstat -tlnp | grep 4000`
- Check firewall: `sudo ufw allow 4000`

### Issue: Rate Limited

- Use fallback model: `groq/llama-3.1-8b-instant`
- Wait 1 minute
- Check Groq console for limits

### Issue: Invalid API Key

- Verify key: `echo $GROQ_API_KEY`
- Test directly: `curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models`
