# LiteLLM Pre-Flight Checklist

## Before Starting LiteLLM

### Environment Setup

- [ ] Python 3.8+ installed
- [ ] LiteLLM package installed (`pip install litellm[proxy]`)
- [ ] Virtual environment created (optional but recommended)
- [ ] GROQ_API_KEY environment variable is set
- [ ] OPENAI_API_KEY set (if using OpenAI models)

### Configuration

- [ ] `proxy_server_config.yaml` exists
- [ ] YAML syntax is valid (no indentation errors)
- [ ] Model names are correctly formatted
- [ ] API keys reference environment variables correctly (`os.environ/GROQ_API_KEY`)
- [ ] Redis settings commented out if Redis not running

### Network

- [ ] Port 4000 is available (not in use)
- [ ] Windows Firewall allows port 4000 (or run as Admin)
- [ ] No Hyper-V port exclusion on 4000
- [ ] Terminal has Administrator privileges

## Startup Verification

### Initial Startup

- [ ] Navigate to correct directory
- [ ] Activate virtual environment (if using)
- [ ] Start with debug flag: `--debug`
- [ ] Server shows "Uvicorn running on http://..."
- [ ] No error messages in output

### Health Check

- [ ] `curl http://localhost:4000/health` returns `{"status": "healthy"}`
- [ ] `curl http://localhost:4000/v1/models` lists configured models
- [ ] Port 4000 shows LISTENING in `netstat -ano | findstr :4000`

### Model Testing

- [ ] Test groq-70b model with simple prompt
- [ ] Test groq-8b model with simple prompt
- [ ] Response returns without errors
- [ ] Response time is reasonable (<5 seconds)

## Common Issues Checklist

### Connection Refused

- [ ] Server is actually running (check terminal)
- [ ] Using correct host (127.0.0.1 vs 0.0.0.0)
- [ ] Firewall rule exists for port 4000
- [ ] No other process using port 4000

### 401 Unauthorized

- [ ] GROQ_API_KEY is set correctly
- [ ] API key format is correct (starts with `gsk_`)
- [ ] API key is valid at console.groq.com
- [ ] No extra spaces or newlines in key

### 404 Model Not Found

- [ ] Model name in request matches config
- [ ] Model alias is defined in model_list
- [ ] Config file was loaded correctly
- [ ] No typos in model name

### 429 Rate Limited

- [ ] Check Groq console for rate limits
- [ ] Implement request queuing
- [ ] Add rate limiting to config
- [ ] Wait and retry

### 500 Internal Error

- [ ] Check config file syntax
- [ ] Run with `--debug` flag
- [ ] Check for missing dependencies
- [ ] Verify Redis is running (if used)

## Production Readiness

### Security

- [ ] API keys stored in environment variables (not hardcoded)
- [ ] Master key set for proxy authentication
- [ ] HTTPS configured (if external access)
- [ ] Rate limiting configured

### Reliability

- [ ] Multiple API keys configured (fallback)
- [ ] Timeout settings configured
- [ ] Retry logic implemented
- [ ] Logging configured

### Monitoring

- [ ] Health check endpoint accessible
- [ ] Logs being written to file
- [ ] Error alerts configured
- [ ] Performance metrics tracked

### Deployment

- [ ] Service configured to auto-start
- [ ] Environment variables persisted
- [ ] Firewall rules permanent
- [ ] Backup configuration stored

## Quick Diagnostic Commands

```cmd
:: Check environment
echo %GROQ_API_KEY%

:: Check port
netstat -ano | findstr :4000

:: Check firewall
netsh advfirewall firewall show rule name="LiteLLM"

:: Test health
curl http://localhost:4000/health

:: List models
curl http://localhost:4000/v1/models

:: Test completion
curl -X POST http://localhost:4000/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\": \"groq-70b\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"
```

## Sign-off

- **Date**: \***\*\_\_\_\*\***
- **Technician**: \***\*\_\_\_\*\***
- **Status**: [ ] Pass [ ] Fail
- **Notes**: \***\*\_\_\_\*\***

## Related Documentation

- [SKILL.md](./SKILL.md) - Main skill documentation
- [REFERENCE.md](./REFERENCE.md) - Error code reference
- [WORKFLOW.md](./WORKFLOW.md) - Step-by-step debugging workflow
