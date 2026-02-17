# Memory Bank - Agent Instructions

**IMPORTANT**: Do NOT load all Memory Bank files. Follow this protocol:

---

## At Task Start - Load These Only

1. **QUICK_REFERENCE.md** (required)
   - Current status, commands, models
   - ~1.5KB

2. **context.md** (required)
   - Recent changes, what's pending
   - ~1KB

3. **brief.md** (optional - for new features)
   - Project goals, scope
   - ~1.5KB

---

## DO NOT LOAD

These files are archived and too large:

- tech.md ❌
- architecture.md ❌
- servers.md ❌
- agents-state.md ❌
- verification-history.md ❌
- tasks-queue.md ❌

---

## For Specific Tasks

| Task           | Also Load           |
| -------------- | ------------------- |
| Code changes   | AGENTS.md           |
| Config updates | opencode.json       |
| Plans          | plans/PHASE\*.md    |
| Reports        | plans/reports/\*.md |

---

## Quick Reference

```
Memory Bank = 3 core files + QUICK_REFERENCE
Total size: ~6KB (vs previous 37KB)
```

---

## If Context Exceeds Limit

1. Load only QUICK_REFERENCE.md
2. Load specific plan file needed
3. Use AGENTS.md for rules
