# Provider Fallback Checklist

## Pre-Fallback Verification

### Primary Provider (LiteLLM) Status

- [ ] LiteLLM proxy is running
- [ ] Health endpoint responds: `curl http://localhost:4000/health`
- [ ] GROQ_API_KEY is set
- [ ] Test completion works with groq-70b
- [ ] Test completion works with groq-8b

### Fallback Provider (Kilo Code) Status

- [ ] Kilo Code extension installed in VS Code
- [ ] Model z-ai/glm-5:free is accessible
- [ ] Test completion works with Kilo Code

## Fallback Decision Checklist

### Error Detection

- [ ] Identify error type (connection, auth, rate limit, etc.)
- [ ] Check error code against REFERENCE.md
- [ ] Log error with timestamp

### Quick Fix Attempt (2 minutes max)

- [ ] Restart LiteLLM proxy
- [ ] Verify API key is set
- [ ] Check port availability
- [ ] Test with different model

### Fallback Activation

- [ ] Quick fix failed or timed out
- [ ] Switch agent configuration to Kilo Code
- [ ] Log fallback event with timestamp
- [ ] Verify fallback is working

## Post-Fallback Tasks

### Immediate

- [ ] Continue operation with Kilo Code
- [ ] Note the time of fallback
- [ ] Document the error that caused fallback

### Investigation (When Time Permits)

- [ ] Review LiteLLM logs
- [ ] Check Groq API status
- [ ] Verify network connectivity
- [ ] Check for configuration issues

### Primary Restoration

- [ ] Fix underlying issue
- [ ] Test LiteLLM health endpoint
- [ ] Test completion with groq-70b
- [ ] Switch back to primary
- [ ] Log restoration event

## Monitoring Checklist

### Daily

- [ ] Check fallback event log
- [ ] Verify LiteLLM is running
- [ ] Test health endpoint

### Weekly

- [ ] Review fallback frequency
- [ ] Identify patterns in failures
- [ ] Update documentation if needed

### Monthly

- [ ] Audit API key validity
- [ ] Check Groq API usage limits
- [ ] Review and update fallback procedures

## Error Code Quick Reference

| Code               | Type    | Action                       |
| ------------------ | ------- | ---------------------------- |
| Connection Refused | Network | Check LiteLLM status         |
| 401                | Auth    | Verify API key               |
| 429                | Rate    | Wait or fallback             |
| 404                | Config  | Check model name             |
| 500                | Server  | Check logs                   |
| Timeout            | Network | Increase timeout or fallback |

## Fallback Event Log Template

```
Date: ___________
Time: ___________
Error Type: ___________
Error Code: ___________
Quick Fix Attempted: [ ] Yes [ ] No
Quick Fix Result: ___________
Fallback Activated: [ ] Yes [ ] No
Restoration Time: ___________
Root Cause: ___________
Resolution: ___________
```

## Contact Information

### Groq Support

- Console: https://console.groq.com
- Status: https://status.groq.com
- Documentation: https://console.groq.com/docs

### LiteLLM Support

- GitHub: https://github.com/BerriAI/litellm
- Documentation: https://docs.litellm.ai

### Kilo Code Support

- Extension: VS Code Marketplace
- Settings: `.kilocode/` directory

## Related Documentation

- [SKILL.md](./SKILL.md) - Main skill documentation
- [WORKFLOW.md](./WORKFLOW.md) - Detailed fallback workflow
- [../litellm-debug/SKILL.md](../litellm-debug/SKILL.md) - LiteLLM debugging
