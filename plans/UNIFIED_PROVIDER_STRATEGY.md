# Unified AI Provider Strategy

**Created**: 2026-02-16
**Purpose**: Unified orchestration across all AI agents

---

## Current Free/Tier Options

### By Agent/Platform

| Agent/Platform           | Free Model        | Context  | Limits           | Best For                  |
| ------------------------ | ----------------- | -------- | ---------------- | ------------------------- |
| **Kilo Code**            | MiniMax-M2.5      | 200K     | ~100 TPS         | Agentic coding, SWE-Bench |
| **Cline**                | kat-coder-pro     | 256K     | Unlimited (free) | VS Code coding agent      |
| **OpenCode**             | Groq llama-3.1-8b | 128K     | Limited          | General tasks             |
| **OpenRouter**           | 31 models         | Up to 1M | 50 req/day       | Research, fallback        |
| **NVIDIA NIM**           | Nemotron, Llama   | 128K     | 1000 credits     | Development               |
| **Antigravity** (Gemini) | Gemini Pro        | 1M       | Limited          | Orchestration             |

---

## Decision Matrix: When to Use What

### Simple Tasks (Free)

- File edits, small changes
- Documentation updates
- Format checking
- Simple research

**Use**: Kilo Code (MiniMax-M2.5) or Cline (kat-coder-pro)

### Complex Tasks (Free)

- Multi-file refactoring
- New component creation
- Complex research with web search
- Planning documents

**Use**: Kilo Code (MiniMax-M2.5) - best for agentic workflows

### Research Tasks

- Web research, benchmarking
- Best practices gathering

**Use**: OpenRouter (Qwen3, Gemini 2.0 Flash free) or Groq

### Orchestration

- Task planning
- Multi-agent coordination

**Use**: Gemini via Antigravity or MiniMax-M2.5 via Kilo Code

---

## Provider Comparison

| Provider          | Model                 | Speed    | Context | Cost         | Setup      |
| ----------------- | --------------------- | -------- | ------- | ------------ | ---------- |
| **MiniMax M2.5**  | 10B active / 230B MoE | 100 TPS  | 200K    | $0.30/1M in  | Kilo Code  |
| **GLM-5**         | 40B active / 744B MoE | ~50 TPS  | 200K    | ~$0.30/1M    | NVIDIA NIM |
| **KAT-Coder-Pro** | -                     | 60 TPS   | 256K    | FREE         | Cline      |
| **Qwen3**         | 8B-80B                | Variable | 262K    | FREE (50/d)  | OpenRouter |
| **Groq**          | Llama 3.3 70B         | Fast     | 128K    | Limited free | Direct API |

---

## Recommended Stack

### Primary (Free)

1. **Kilo Code** - MiniMax-M2.5 - Best for agentic coding
2. **Cline** - kat-coder-pro - Free unlimited for VS Code

### Fallback

3. **OpenRouter** - Qwen3 free tier (50 req/day)
4. **Groq** - For when others fail

### Orchestration

- **Antigravity** (Gemini) - For planning and high-level decisions
- **Kilo Code** - For execution

---

## Complexity Decision Guide

### Simple (Use Kilo/Cline)

- Single file edits
- Bug fixes
- Documentation
- Format changes
- Small refactors

### Complex (Use Kilo + Research)

- Multi-file changes
- New features
- Architecture decisions
- Research synthesis
- Planning documents

### Very Complex (Use Orchestration)

- Multi-agent coordination
- Strategic decisions
- PRD creation
- Architecture design

---

## Setup Checklist

- [ ] Kilo Code: Verify MiniMax-M2.5 access
- [ ] Cline: Verify kat-coder-pro works
- [ ] OpenRouter: Get API key for fallback
- [ ] Groq: Verify API works
- [ ] Antigravity: Gemini access confirmed

---

## Next Steps

1. Test Kilo Code with MiniMax-M2.5 for complex tasks
2. Use Cline for VS Code tasks
3. Keep Groq as emergency fallback
4. Document results in memory bank

---

_Last Updated: 2026-02-16_
