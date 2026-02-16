# LiteLLM Configuration Guide

## Overview

This directory contains LiteLLM proxy configuration for unified LLM access across multiple providers.

## Quick Start

### 1. Install Dependencies

```bash
# Option A: Install using requirements.txt (recommended)
pip install -r litellm/requirements.txt

# Option B: Install litellm directly
pip install litellm>=1.0.0 python-dotenv pyyaml openai

# Verify installation
litellm --version
pip show litellm
```

**Note for Windows users with virtual environment:**

```bash
# If using the project's .venv
.venv\Scripts\pip install -r litellm\requirements.txt

# Verify the CLI is available
.venv\Scripts\litellm --help
```

### 2. Setup Environment

```bash
# Copy the example environment file
cp litellm/.env.example litellm/.env

# Edit .env and add your API keys
# Get keys from:
# - Groq: https://console.groq.com/keys
# - OpenAI: https://platform.openai.com/api-keys
# - Anthropic: https://console.anthropic.com/settings/keys
# - Google: https://aistudio.google.com/app/apikey
```

### 3. Start Proxy

```bash
# Using Python script (recommended)
python litellm/start_litellm.py

# Or directly with litellm CLI
litellm --config litellm/proxy_config.yaml --port 4000

# Or on Windows with venv
.venv\Scripts\litellm --config litellm\proxy_config.yaml --port 4000
```

### 3. Test

```bash
# Test Groq (fast, free tier available)
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "groq/llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Say hi"}]
  }'
```

## Configuration Files

| File                | Purpose                              |
| ------------------- | ------------------------------------ |
| `.env.example`      | Template for API keys                |
| `.env`              | Your actual API keys (DO NOT COMMIT) |
| `proxy_config.yaml` | LiteLLM model configuration          |
| `start_litellm.py`  | Python startup script                |
| `start_litellm.bat` | Windows batch startup script         |

## Available Models

### Groq (Recommended - Fast, Free Tier)

| Model                          | Description              |
| ------------------------------ | ------------------------ |
| `groq/llama-3.3-70b-versatile` | Best overall performance |
| `groq/llama-3.1-8b-instant`    | Fast, cost-effective     |
| `groq/llama-3.1-70b-versatile` | High capability          |

### OpenAI (Requires API Key)

| Model         | Description  |
| ------------- | ------------ |
| `gpt-4o-mini` | Fast, cheap  |
| `gpt-4o`      | Most capable |

### Anthropic (Requires API Key)

| Model             | Description |
| ----------------- | ----------- |
| `claude-3-haiku`  | Fast        |
| `claude-3-sonnet` | Balanced    |

### Google (Requires API Key)

| Model              | Description      |
| ------------------ | ---------------- |
| `gemini-1.5-flash` | Fast, multimodal |

## Common Issues

### "Invalid API Key" Error

1. Check your .env file has the correct key
2. Verify the key hasn't expired
3. Ensure GROQ_API_KEY is set in environment

### "Connection Timeout"

1. Check firewall settings
2. Verify port 4000 is available
3. Try without `--host 0.0.0.0`

### Model Not Found

1. Check the model name in proxy_config.yaml
2. Ensure corresponding API key is set in .env

## Integration with Antigravity

To use LiteLLM with Antigravity IDE:

1. Set `LITELLM_PROXY_URL=http://localhost:4000` in your environment
2. Use model names as defined in proxy_config.yaml
3. For Kilo Code: ensure GROQ_API_KEY is set in system environment

## Security Notes

- NEVER commit `.env` file to version control
- The `.env` file is in `.gitignore`
- Use GitHub Secrets for CI/CD
- Master key `sk-local-dev-1234` is for local development only

## API Key Sources

| Provider  | URL                   | Free Tier     |
| --------- | --------------------- | ------------- |
| Groq      | console.groq.com      | Yes (limited) |
| OpenAI    | platform.openapi.com  | No (paid)     |
| Anthropic | console.anthropic.com | No (paid)     |
| Google    | aistudio.google.com   | Yes (limited) |

## Testing API Keys

```bash
# Test Groq directly (without proxy)
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer YOUR_GROQ_KEY"

# Test via LiteLLM (after starting proxy)
python -c "
import os
os.environ['GROQ_API_KEY'] = 'YOUR_KEY'
from litellm import completion
r = completion(model='groq/llama-3.3-70b-versatile',
              messages=[{'role': 'user', 'content': 'Hi'}])
print(r.choices[0].message.content)
"
```

## Monitoring

LiteLLM proxy provides:

- Health endpoint: `http://localhost:4000/health`
- Metrics: `http://localhost:4000/metrics` (if Prometheus enabled)
- UI Dashboard: `http://localhost:4000/ui`
