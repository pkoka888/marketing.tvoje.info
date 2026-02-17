---
description: Project-wide 2026 agentic engineering standards and coding conventions
---

# General Project Rules

This file captures project-wide patterns and 2026-tier best practices for agentic engineering.

## 1. Project Context
- This is an Astro 5.0 marketing portfolio.
- Tech Stack: TypeScript, Tailwind CSS, Vercel/VPS deployment.

## 2. 2026 Advanced Protocol (STRICT)
- **Batch Read**: Reading multiple files at once is more efficient for the LLM. If other files are relevant to your task, read them simultaneously using `read_multiple_files` or consecutive tool calls.
- **Autonomous Condensation**: If token usage exceeds 80% or history is very long, switch to `maintenance` mode and use the `/condense` workflow.
- **Multi-Agent Synergy**: Always document the handoff when switching between Pro models (Architect/UX) and Free models (Dev/Analyst).
- **Structural Integrity**: All agentic artifacts (skills, workflows) must live in `.kilocode/`.

## 3. Communication
- Tone: Technical, concise, and objective.
- Use GitHub alerts for critical information.
- Proactively suggest updates to this file when a new pattern is discovered.

## 4. Coding Standards
- **Tailwind**: Use utility classes (e.g., `text-md text-vscode-descriptionForeground mb-2`).
- **Safety**: Never perform cleanup or delete operations without explicit user approval.
- **Verification**: Run `npm run test` and `npm run build` after changes.
