# Memory Bank - Quick Reference

**Last Updated**: 2026-02-17
**Purpose**: Essential info for agents at task start

---

## Project Status

| Area          | Status         |
| ------------- | -------------- |
| Build         | ✅ 24 pages    |
| Tests         | ✅ 10/10 pass  |
| Lighthouse    | ✅ 100 score   |
| Accessibility | ✅ WCAG 2.2 AA |
| Themes        | ✅ 7 working   |
| Production    | ✅ Live        |

---

## Quick Commands

```bash
npm run dev      # Start dev server
npm run build    # Production build
npm test         # Run tests
```

---

## Key Files

| Purpose | File                         |
| ------- | ---------------------------- |
| Configs | `opencode.json`, `AGENTS.md` |
| Models  | `.kilocode/models.json`      |
| Rules   | `.kilocode/rules/`           |
| Plans   | `plans/PHASE*.md`            |

---

## Models (Free First)

| Tool     | Model                             |
| -------- | --------------------------------- |
| Kilo     | `grok-code-fast-1:optimized:free` |
| OpenCode | `big-pickle`                      |
| Cline    | `minimax-m2.1:free`               |

---

## Current Work

- Phase 4: Fixes applied (Schema.org, themes)
- Manual: Search portal registration pending
- See: `USER_ACTION_PLAN.md`

---

## Never Use Gemini for

- Internal code searches
- File operations
- Routine tasks

Use only for: External research, complex architecture

---

## Verification

```bash
python scripts/verify_agentic_platform.py
```

---

## Notes

- Memory Bank = 3 core files (brief, context, product)
- Detailed docs moved to `.kilocode/knowledge/`
- See AGENTS.md for full rules
