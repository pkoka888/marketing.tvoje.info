# AI Prompting in This Project - Simple User Guide

> **TL;DR**: This project uses **OpenCode** as the main AI agent, with additional rules from the `ai-prompts` library. Everything is configured automatically.

---

## What Happens Automatically

When you run OpenCode in this project, it already knows:

| Feature                  | How It's Applied                 |
| ------------------------ | -------------------------------- |
| Astro 4 coding standards | Via `opencode.json` → ai-prompts |
| Tailwind CSS 4 rules     | Via `opencode.json` → ai-prompts |
| Project structure        | Via `AGENTS.md`                  |
| Build/test commands      | Via `AGENTS.md`                  |

**You don't need to do anything manually!**

---

## Quick Start

### 1. Start OpenCode

```bash
cd C:\Users\pavel\projects\marketing.tvoje.info
opencode
```

OpenCode will automatically read:

1. `opencode.json` → loads Astro + Tailwind rules
2. `AGENTS.md` → loads project structure

### 2. Ask Questions

```
How do I create a new component?
```

The AI will follow Astro-specific patterns automatically.

### 3. Get Code Suggestions

```
Add a new hero section to the homepage
```

The AI will use the configured Tailwind + Astro rules.

---

## Visual: How Rules Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        YOU                                   │
│                  (ask question)                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                     OpenCode                                 │
│                   (AI Agent)                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌─────────────────┐     ┌─────────────────────────┐
│   AGENTS.md     │     │    opencode.json       │
│                 │     │                        │
│ - Tech stack    │     │ → ai-prompts/         │
│ - Project path  │     │   astro-4-rules       │
│ - Commands     │     │   tailwind-4-rules     │
└─────────────────┘     └─────────────────────────┘
```

---

## How to Add New Rules

### Option 1: Edit opencode.json (Recommended)

```json
{
  "instructions": [
    "AGENTS.md",
    "C:/Users/pavel/vscodeportable/agentic/ai-prompts/prompts/astro-4/rule-astro-coding-standards.md",
    "C:/Users/pavel/vscodeportable/agentic/ai-prompts/prompts/tailwind-4/rule-tailwind-v4.md"
  ]
}
```

### Option 2: Edit AGENTS.md Directly

Add project-specific rules:

```markdown
## My Custom Rules

When creating components:

- Always add TypeScript interfaces
- Include ARIA labels
- Follow our naming convention
```

---

## Other AI Tools in This Project

| Agent           | Config          | When to Use           |
| --------------- | --------------- | --------------------- |
| **OpenCode**    | `opencode.json` | Main AI assistant     |
| **Kilo Code**   | `.kilocode/`    | VS Code extension     |
| **Cline**       | `.clinerules/`  | Terminal headless     |
| **Antigravity** | `GEMINI.md`     | Planning/architecture |

---

## Common Tasks

### Task: Ask about project structure

```
What files are in src/components/?
```

### Task: Add a new feature

```
Create a new contact form component
```

### Task: Fix something

```
Fix the navigation mobile menu
```

### Task: Run tests

```
Run the test suite
```

---

## For VS Code Users

If you use **GitHub Copilot** in VS Code:

1. Create `.github/copilot-instructions.md` for project rules
2. Use prompt files: `.github/copilot-prompts/*.md`

> **Note**: VS Code has built-in prompting - no extra extension needed!

---

## Need Help?

- Full comparison: `C:\Users\pavel\vscodeportable\agentic\AI-PROMPTING-COMPARISON.md`
- OpenCode docs: https://opencode.ai/docs
- ai-prompts repo: https://github.com/instructa/ai-prompts

---

_Last updated: 2026-02-12_
