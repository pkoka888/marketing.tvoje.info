# Kilo Free Models Configuration Guide

## Current Status

**Kilo Auth Credentials (2):**

- Kilo Gateway: ✅ Configured
- Nvidia: ✅ Configured

**Environment Variables (7):**

- NVIDIA_API_KEY ✅
- GROQ_API_KEY ✅
- OPENROUTER_API_KEY ✅
- GITHUB_TOKEN ✅
- GEMINI_API_KEY ✅
- OPENAI_API_KEY ✅

---

## Free Models Available

### 1. Kilo Gateway Free Models (Already Available)

| Model                   | Type | Best For                              |
| ----------------------- | ---- | ------------------------------------- |
| **MiniMax M2.1**        | Free | General-purpose, current agent config |
| Z.AI: GLM 4.7           | Free | Agent-centric applications            |
| MoonshotAI: Kimi K2.5   | Free | Advanced tool use, reasoning          |
| Giga Potato             | Free | Evaluation period (stealth)           |
| Arcee AI: Trinity Large | Free | Preview model                         |

### 2. OpenRouter Free Tier (Requires Account)

**Setup Required:**

1. Create free account at https://openrouter.ai/
2. Get API key from dashboard
3. Add to Kilo: `kilo auth add openrouter`

| Model               | Type | Best For                   |
| ------------------- | ---- | -------------------------- |
| Qwen3 Coder         | Free | Agentic coding, tool use   |
| Z.AI: GLM 4.5 Air   | Free | Lightweight agent tasks    |
| DeepSeek: R1 0528   | Free | Reasoning (parity with o1) |
| MoonshotAI: Kimi K2 | Free | Agentic capabilities       |

---

## Current Agent Configuration

**File:** `.kilocode/agents/bmad-solo.json`

```json
{
  "model": "kilo/minimax/minimax-m2.1:free",
  ...
}
```

This configuration is **CORRECT** and should work with the free MiniMax M2.1 model.

---

## Alternative Free Configurations

### Option 1: Use Kilo Gateway MiniMax (Current)

```
kilo/minimax/minimax-m2.1:free
```

### Option 2: Use Kilo Gateway GLM 4.7

```
kilo/zaigl/glm-4.7:free
```

### Option 3: Use Kilo Gateway Kimi K2.5

```
kilo/moonshot/kimi-k2.5:free
```

### Option 4: OpenRouter (requires setup)

```
openrouter/qwen/qwen3-coder:free
```

---

## Cost Optimization Strategy

### The 50% Rule

| Task Type             | Recommended Model      |
| --------------------- | ---------------------- |
| Code reviews          | Free (MiniMax/Gateway) |
| Documentation         | Free                   |
| Simple bug fixes      | Free                   |
| Boilerplate           | Free                   |
| Architecture planning | Budget (~$0.30/M)      |
| Complex debugging     | Premium                |

### Mode-Based Cost Control

| Mode         | Groups                             | Model Suggestion |
| ------------ | ---------------------------------- | ---------------- |
| architect    | read, edit, browser, mcp, condense | Budget           |
| bmad-dev     | read, edit, command, mcp           | Free             |
| bmad-analyst | read, edit, browser, mcp           | Free             |
| maintenance  | read, command, mcp, condense       | Free             |

---

## Troubleshooting

### If `minimax-m2.1:free` fails:

1. Check auth: `kilo auth list`
2. Try explicit provider: `kilo/minimax/minimax-m2.1`
3. Fallback to OpenRouter Qwen3 Coder

### To enable OpenRouter free models:

```bash
# Add OpenRouter account
kilo auth add openrouter

# Then use model:
openrouter/qwen/qwen3-coder:free
```

---

## Recommendations

1. **Current setup is correct** - `kilo/minimax/minimax-m2.1:free` should work
2. **Create OpenRouter account** for backup free models
3. **Use Groq** for fast inference (already configured with GROQ_API_KEY)
4. **Set up profiles** for easy model switching

---

## Quick Test Command

```bash
# Test Kilo with free model
kilo chat "Hello, respond with just 'OK' if you can read this" --model kilo/minimax/minimax-m2.1:free
```
