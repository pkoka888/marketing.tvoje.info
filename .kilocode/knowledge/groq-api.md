# Groq API Documentation

> **Last Updated**: 2026-02-13
> **Source**: Official Groq Documentation (https://console.groq.com/docs/)
> **Purpose**: Reference for LiteLLM and Kilo Code provider-fallback skill

---

## Model Name Verification

### Current Configuration Status

| Model Name in Config           | Official API Name         | Status           |
| ------------------------------ | ------------------------- | ---------------- |
| `groq/llama-3.3-70b-versatile` | `llama-3.3-70b-versatile` | ✅ **CONFIRMED** |
| `groq/llama-3.1-8b-instant`    | `llama-3.1-8b-instant`    | ✅ **CONFIRMED** |

**No discrepancies found** - the current LiteLLM configuration uses correct model names.

---

## Production Models

### Text Generation Models

| Model ID                  | Speed (T/s) | Input Price | Output Price | Context Window | Max Completion |
| ------------------------- | ----------- | ----------- | ------------ | -------------- | -------------- |
| `llama-3.1-8b-instant`    | 560         | $0.05/1M    | $0.08/1M     | 131,072        | 131,072        |
| `llama-3.3-70b-versatile` | 280         | $0.59/1M    | $0.79/1M     | 131,072        | 32,768         |
| `openai/gpt-oss-120b`     | 500         | $0.15/1M    | $0.60/1M     | 131,072        | 65,536         |
| `openai/gpt-oss-20b`      | 1000        | $0.075/1M   | $0.30/1M     | 131,072        | 65,536         |

### Audio Models (Speech-to-Text)

| Model ID                 | Price       | Max File Size | Rate Limit (ASH) |
| ------------------------ | ----------- | ------------- | ---------------- |
| `whisper-large-v3`       | $0.111/hour | 100 MB        | 7,200 sec/hour   |
| `whisper-large-v3-turbo` | $0.04/hour  | -             | 7,200 sec/hour   |

### Production Systems (Agentic AI)

| Model ID             | Speed (T/s) | Context Window | Max Completion |
| -------------------- | ----------- | -------------- | -------------- |
| `groq/compound`      | 450         | 131,072        | 8,192          |
| `groq/compound-mini` | 450         | 131,072        | 8,192          |

---

## Preview Models

> **Warning**: Preview models are for evaluation only and may be discontinued at short notice.

| Model ID                                        | Speed (T/s) | Input Price | Output Price | Context Window | Max Completion |
| ----------------------------------------------- | ----------- | ----------- | ------------ | -------------- | -------------- |
| `meta-llama/llama-4-maverick-17b-128e-instruct` | 600         | $0.20/1M    | $0.60/1M     | 131,072        | 8,192          |
| `meta-llama/llama-4-scout-17b-16e-instruct`     | 750         | $0.11/1M    | $0.34/1M     | 131,072        | 8,192          |
| `qwen/qwen3-32b`                                | 400         | $0.29/1M    | $0.59/1M     | 131,072        | 40,960         |
| `moonshotai/kimi-k2-instruct-0905`              | 200         | $1.00/1M    | $3.00/1M     | 262,144        | 16,384         |
| `openai/gpt-oss-safeguard-20b`                  | 1000        | $0.075/1M   | $0.30/1M     | 131,072        | 65,536         |

### Text-to-Speech Models (Preview)

| Model ID                          | Price           | Context Window | Max Completion |
| --------------------------------- | --------------- | -------------- | -------------- |
| `canopylabs/orpheus-arabic-saudi` | $40.00/1M chars | 4,000          | 50,000         |
| `canopylabs/orpheus-v1-english`   | $22.00/1M chars | 4,000          | 50,000         |

### Guard Models (Preview)

| Model ID                              | Input Price | Output Price | Context Window | Max Completion |
| ------------------------------------- | ----------- | ------------ | -------------- | -------------- |
| `meta-llama/llama-prompt-guard-2-22m` | $0.03/1M    | $0.03/1M     | 512            | 512            |
| `meta-llama/llama-prompt-guard-2-86m` | $0.04/1M    | $0.04/1M     | 512            | 512            |

---

## Rate Limits

### Understanding Rate Limits

Rate limits are measured in:

- **RPM**: Requests per minute
- **RPD**: Requests per day
- **TPM**: Tokens per minute
- **TPD**: Tokens per day
- **ASH**: Audio seconds per hour
- **ASD**: Audio seconds per day

> **Note**: Cached tokens do not count towards rate limits. Rate limits apply at the organization level.

### Developer Plan Rate Limits

| Model ID                                        | RPM | RPD    | TPM    | TPD   | ASH   | ASD    |
| ----------------------------------------------- | --- | ------ | ------ | ----- | ----- | ------ |
| `llama-3.1-8b-instant`                          | 30  | 14,400 | 6,000  | 500K  | -     | -      |
| `llama-3.3-70b-versatile`                       | 30  | 1,000  | 12,000 | 100K  | -     | -      |
| `openai/gpt-oss-120b`                           | 30  | 1,000  | 8,000  | 200K  | -     | -      |
| `openai/gpt-oss-20b`                            | 30  | 1,000  | 8,000  | 200K  | -     | -      |
| `groq/compound`                                 | 30  | 250    | 70,000 | -     | -     | -      |
| `groq/compound-mini`                            | 30  | 250    | 70,000 | -     | -     | -      |
| `meta-llama/llama-4-maverick-17b-128e-instruct` | 30  | 1,000  | 6,000  | 500K  | -     | -      |
| `meta-llama/llama-4-scout-17b-16e-instruct`     | 30  | 1,000  | 30,000 | 500K  | -     | -      |
| `qwen/qwen3-32b`                                | 60  | 1,000  | 6,000  | 500K  | -     | -      |
| `moonshotai/kimi-k2-instruct-0905`              | 60  | 1,000  | 10,000 | 300K  | -     | -      |
| `whisper-large-v3`                              | 20  | 2,000  | -      | -     | 7,200 | 28,800 |
| `whisper-large-v3-turbo`                        | 20  | 2,000  | -      | -     | 7,200 | 28,800 |
| `canopylabs/orpheus-arabic-saudi`               | 10  | 100    | 1,200  | 3,600 | -     | -      |
| `canopylabs/orpheus-v1-english`                 | 10  | 100    | 1,200  | 3,600 | -     | -      |

### Rate Limit Headers

The API returns rate limit information in response headers:

| Header                           | Example Value | Description                     |
| -------------------------------- | ------------- | ------------------------------- |
| `retry-after`                    | 2             | Seconds until rate limit resets |
| `x-ratelimit-limit-requests`     | 14400         | Requests Per Day (RPD) limit    |
| `x-ratelimit-limit-tokens`       | 18000         | Tokens Per Minute (TPM) limit   |
| `x-ratelimit-remaining-requests` | 14370         | Remaining RPD                   |
| `x-ratelimit-remaining-tokens`   | 17997         | Remaining TPM                   |
| `x-ratelimit-reset-requests`     | 2m59.56s      | Time until RPD reset            |
| `x-ratelimit-reset-tokens`       | 7.66s         | Time until TPM reset            |

---

## API Reference

### Base URL

```
https://api.groq.com/openai/v1
```

### Authentication

All API requests require a Bearer token in the Authorization header:

```bash
Authorization: Bearer $GROQ_API_KEY
```

### List Available Models

```bash
curl -X GET "https://api.groq.com/openai/v1/models" \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json"
```

**Python:**

```python
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
models = client.models.list()
for model in models:
    print(model.id)
```

**JavaScript:**

```javascript
import Groq from 'groq-sdk';

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
const models = await groq.models.list();
console.log(models);
```

### Chat Completions

```bash
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
  }'
```

**Python:**

```python
from groq import Groq

client = Groq()

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ],
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=1024,
)

print(chat_completion.choices[0].message.content)
```

**JavaScript:**

```javascript
import Groq from 'groq-sdk';

const groq = new Groq();

const chatCompletion = await groq.chat.completions.create({
  messages: [{ role: 'user', content: 'Hello, how are you?' }],
  model: 'llama-3.3-70b-versatile',
  temperature: 0.7,
  max_tokens: 1024,
});

console.log(chatCompletion.choices[0].message.content);
```

### LiteLLM Integration

When using LiteLLM proxy, prefix model names with `groq/`:

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "groq/llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Audio Transcription (Whisper)

```python
from groq import Groq

client = Groq()

with open("audio.mp3", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3-turbo",
        response_format="json",
    )
    print(transcription.text)
```

---

## Error Handling

### HTTP Status Codes

| Status Code | Description                             |
| ----------- | --------------------------------------- |
| 200         | Success                                 |
| 400         | Bad Request - Invalid parameters        |
| 401         | Unauthorized - Invalid API key          |
| 403         | Forbidden - Insufficient permissions    |
| 404         | Not Found - Model or endpoint not found |
| 422         | Unprocessable Entity - Validation error |
| 429         | Too Many Requests - Rate limit exceeded |
| 500         | Internal Server Error                   |
| 503         | Service Unavailable                     |

### Rate Limit Exceeded (429)

When rate limits are exceeded, the API returns a 429 status code with a `retry-after` header.

**Handling Rate Limits:**

```python
import time
from groq import Groq, RateLimitError

client = Groq()

def chat_with_retry(messages, model="llama-3.3-70b-versatile", max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                messages=messages,
                model=model,
            )
        except RateLimitError as e:
            if attempt < max_retries - 1:
                retry_after = int(e.response.headers.get("retry-after", 60))
                time.sleep(retry_after)
            else:
                raise
```

### Common Error Responses

**Invalid API Key:**

```json
{
  "error": {
    "message": "Invalid API key provided",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

**Model Not Found:**

```json
{
  "error": {
    "message": "Model 'invalid-model' not found",
    "type": "invalid_request_error",
    "code": "model_not_found"
  }
}
```

**Rate Limit Exceeded:**

```json
{
  "error": {
    "message": "Rate limit exceeded. Please try again in 2 seconds.",
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded"
  }
}
```

---

## Best Practices

### 1. Model Selection

| Use Case              | Recommended Model         | Reason                               |
| --------------------- | ------------------------- | ------------------------------------ |
| Fast, cheap responses | `llama-3.1-8b-instant`    | Highest speed (560 T/s), lowest cost |
| Complex reasoning     | `llama-3.3-70b-versatile` | Best quality-to-speed ratio          |
| OpenAI compatibility  | `openai/gpt-oss-20b`      | OpenAI model with Groq speed         |
| Agentic workflows     | `groq/compound`           | Built-in tool use capabilities       |
| Audio transcription   | `whisper-large-v3-turbo`  | Fastest transcription                |

### 2. Rate Limit Management

- **Monitor headers**: Check `x-ratelimit-remaining-*` headers
- **Implement backoff**: Use exponential backoff on 429 errors
- **Cache responses**: Use prompt caching to reduce token usage
- **Batch requests**: Combine multiple requests when possible

### 3. Cost Optimization

- Use `llama-3.1-8b-instant` for simple tasks (10x cheaper than 70B)
- Enable prompt caching for repeated contexts
- Set appropriate `max_tokens` limits
- Use `whisper-large-v3-turbo` for audio (2.7x cheaper than v3)

### 4. Context Window Management

- Most models support 131,072 tokens context
- `kimi-k2-instruct-0905` supports 262,144 tokens
- Monitor token usage in responses
- Use streaming for long responses

### 5. Error Handling

```python
from groq import Groq, APIError, RateLimitError, APIConnectionError

def safe_chat(client, messages, model, **kwargs):
    try:
        return client.chat.completions.create(
            messages=messages,
            model=model,
            **kwargs
        )
    except RateLimitError as e:
        print(f"Rate limit hit. Retry after: {e.response.headers.get('retry-after')}s")
        raise
    except APIConnectionError as e:
        print(f"Connection error: {e}")
        raise
    except APIError as e:
        print(f"API error: {e}")
        raise
```

---

## SDK Libraries

### Official SDKs

| Language              | Package    | Installation           |
| --------------------- | ---------- | ---------------------- |
| Python                | `groq`     | `pip install groq`     |
| JavaScript/TypeScript | `groq-sdk` | `npm install groq-sdk` |

### OpenAI Compatibility

Groq API is OpenAI-compatible, so you can use OpenAI SDKs with a base URL change:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello"}],
)
```

---

## Changelog

### 2026-02-13

- Verified model names match current configuration
- Added new models: GPT-OSS 120B/20B, Llama 4 Maverick/Scout, Qwen3-32B
- Documented Compound systems for agentic AI
- Added Orpheus TTS models
- Updated rate limits for Developer plan

### Sources

- Models: https://console.groq.com/docs/models
- Rate Limits: https://console.groq.com/docs/rate-limits
- API Reference: https://console.groq.com/docs/api-reference
