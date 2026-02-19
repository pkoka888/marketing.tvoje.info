# User Guide: Marketing Portfolio with AI Agents

> **Quick Start**: This is your marketing portfolio website powered by multiple
> AI agents. This guide helps you use them effectively.

---

## 🎯 What is This Project?

**marketing.tvoje.info** is a modern marketing portfolio website built with:

- **Astro** - Static site generator
- **Tailwind CSS** - Styling
- **Multiple AI Agents** - Automate development, research, and content creation

---

## 🤖 AI Agents Overview

### Available Agents

| Agent          | Best For                    | Model (Free)                           |
| -------------- | --------------------------- | -------------------------------------- |
| **Kilo Code**  | Bulk coding, implementation | `x-ai/grok-code-fast-1:optimized:free` |
| **OpenCode**   | Standard tasks, research    | `big-pickle`                           |
| **Cline**      | Routine fixes, planning     | `minimax-m2.1:free`                    |
| **Gemini CLI** | Research, analysis          | `gemini-2.5-flash`                     |

### When to Use Which Agent

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ROUTING GUIDE                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Need code written?  ──────►  Kilo Code (free)           │
│                                                             │
│  Need research?  ──────────►  OpenCode @researcher       │
│                                                             │
│  Need audit/compliance?  ────►  Claude Code (paid)       │
│                                                             │
│  Need architecture?  ─────────►  Gemini CLI (free)        │
│                                                             │
│  Quick fix?  ─────────────────►  Cline (free)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Common Scenarios

### 1. Adding a New Feature

**Steps:**

1. Describe your idea in plain language
2. Agent creates a plan using TASK_PLAN template
3. Agent implements using free models (Kilo Code)
4. Verify with `npm run build`

**Prompt Example:**

> "Add a contact form with email validation. Use Astro form handling."

### 2. Researching Technologies

**Steps:**

1. Use OpenCode with `@researcher` persona
2. Ask specific questions
3. Agent searches web and compiles findings

**Prompt Example:**

> "@researcher Find best free AI image generation libraries for self-hosting in
> 2025"

### 3. Fixing Bugs

**Steps:**

1. Describe the bug
2. Cline or Kilo Code investigates
3. Uses free model for fix

**Prompt Example:**

> "Navigation menu doesn't work on mobile. Debug and fix."

### 4. Content Updates

**Steps:**

1. Describe what needs updating
2. Agent edits content files
3. Verify changes

**Prompt Example:**

> "Update the services section to include SEO consulting"

### 5. Generating Images

**Tools Available:**

- **NVIDIA Canvas** (free) - AI image generation
- **OpenAI DALL-E** (paid) - High quality
- **Stable Diffusion** (self-hosted option)

**Prompt Example:**

> "Generate hero image for marketing services section: professional, modern,
> blue tones"

---

## 💰 Cost Control (Important!)

### Free Models (Use First)

- Kilo Code: `grok-code-fast-1:optimized:free`
- OpenCode: `big-pickle`
- Cline: `minimax-m2.1:free`
- Gemini: `gemini-2.5-flash`

### Paid Models (Requires Approval)

- Claude Sonnet/Opus
- OpenAI o3
- Gemini 2.5 Pro

**Rule**: Always try free models first. Only use paid for complex reasoning.

---

## 📁 Project Structure

```
marketing.tvoje.info/
├── src/                    # Source code
│   ├── pages/            # Astro pages
│   ├── components/       # UI components
│   └── layouts/          # Page layouts
├── public/images/        # Images & graphics
├── plans/                # Feature plans & research
├── scripts/              # Automation scripts
├── litellm/              # AI proxy config
└── .kilocode/           # Agent configurations
```

---

## 🔧 Useful Commands

```bash
# Development
npm run dev              # Start local server
npm run build            # Production build

# Verification (run before commit)
python scripts/verify_agentic_platform.py
python scripts/validate_template_references.py

# List available templates
python scripts/new_plan.py --list
```

---

## 🔍 Research Findings: Free AI Image Generation

Based on web research (Feb 2026):

### Top Free Options

| Tool                     | Type         | Cost         | Notes                       |
| ------------------------ | ------------ | ------------ | --------------------------- |
| **Stable Diffusion 3.5** | Self-host    | Free         | Best open source, needs GPU |
| **FLUX.1**               | Self-host    | Free         | Newer, quality              |
| **ComfyUI**              | GUI/Workflow | Free         | Advanced, steep learning    |
| **OpenArt**              | Web          | Free tier    | Easy to start               |
| **Gemini 2.0**           | API          | Limited free | Google's offering           |

### Recommended for This Project

1. **For Quick Assets**: Use OpenArt (free tier)
2. **For Self-Hosting**: Stable Diffusion 3.5 + ComfyUI
3. **For Integration**: NVIDIA API (has free tier)

---

## 📋 Available Templates

Use these for structured planning:

| Template          | Use For                      |
| ----------------- | ---------------------------- |
| TASK_PLAN         | Implementation tasks         |
| RESEARCH_FINDINGS | Research documentation       |
| AUDIT_REPORT      | Security/compliance audits   |
| GAP_ANALYSIS      | Identifying missing features |
| TEST_RESULTS      | QA documentation             |
| LINT_FIX_STRATEGY | Code quality fixes           |

---

## 🆘 Troubleshooting

### "Out of credits"

- Switch to free model (see Cost Control section)
- Check `.kilocode/rules/cost-optimization`

### "Agent not responding"

- Try different agent
- Check `scripts/verify_agentic_platform.py`

### "Build failed"

- Run `npm run build` locally to see errors
- Check for missing dependencies

---

## 📞 Getting Help

1. **Read AGENTS.md** - Full agent framework docs
2. **Check CLAUDE.md** - Claude Code instructions
3. **Review plans/** - Feature documentation

---

_Last Updated: 2026-02-19_
