# Memory Bank Best Practices for AI Agents

Based on research from Anthropic, Claude Code, and industry best practices (2025-2026).

---

## Core Principles

### 1. Context is Finite - Treat It as Such

- LLMs have **limited attention budget** - more tokens = diluted focus
- **Context rot**: As context grows, model recall decreases
- Goal: **Smallest high-signal token set** that achieves desired outcome

### 2. Minimal Viable Context

- Start with minimal prompt, add complexity only when failures occur
- Every token should earn its place in context
- Remove redundant information proactively

### 3. Separation of Concerns

| Layer            | Purpose                | Example                        |
| ---------------- | ---------------------- | ------------------------------ |
| **Brief**        | High-level goals       | Project scope, target audience |
| **Product**      | User experience        | Features, success metrics      |
| **Context**      | Current state          | What's happening now           |
| **Architecture** | Technical decisions    | Stack, patterns, components    |
| **Tech**         | Implementation details | Commands, dependencies         |

---

## File Structure Best Practices

### Hierarchical Organization

```
memory-bank/
├── brief.md          # Project scope, goals, success criteria
├── product.md        # User experience, features
├── context.md        # Current work focus, recent changes
├── architecture.md   # System design, component relationships
├── tech.md           # Commands, dependencies, setup
├── servers.md        # Infrastructure references
└── tasks.md          # Documented workflows
```

### Section Guidelines

**brief.md** (50-100 lines max)

- Project name, purpose, target audience
- Success metrics (quantifiable)
- Scope: in/out of scope

**context.md** (30-50 lines max)

- Current work focus (timestamped)
- Recent changes (last 3-5 items)
- Active tasks
- Quick links

**architecture.md** (50-100 lines max)

- System diagram (text-based)
- Key technical decisions
- Component relationships
- Critical paths

**tech.md** (50-80 lines max)

- Commands to run
- Dependencies
- Tool usage patterns
- Setup instructions

---

## Content Optimization

### Write for Scanning

- Use headers, bullet points, tables
- Key information first
- Include timestamps for temporal context

### Use Semantic Grouping

- Group related info together
- Cross-reference between files with `@` references
- Keep related context in same file

### Avoid Redundancy

- Don't repeat info across files
- Use references instead: "See brief.md for scope"
- Trust that agent reads all files

### Include Action Triggers

- Explicit instructions: "If X, do Y"
- Decision trees for common scenarios
- Escalation paths

---

## Loading Strategy

### Per-Task Loading

1. **Start with brief.md** - foundation
2. **context.md** - current state
3. **Relevant domain files** - architecture/tech only if needed
4. **Never load everything** - be surgical

### Progressive Disclosure

- Initial: brief + context
- Deep work: + architecture + tech
- Domain expertise: + tasks, servers

---

## Maintenance

### Regular Pruning

- Archive old context to `.archive/`
- Remove stale references
- Update timestamps when context changes

### Compaction Triggers

- When context exceeds ~50% of token budget
- Before long-horizon tasks
- After milestone completion

### Versioning

- Keep changelog in context.md
- Note when significant changes occur
- Archive old states

---

## Anti-Patterns to Avoid

| Anti-Pattern              | Why It's Bad                     |
| ------------------------- | -------------------------------- |
| 10K+ line files           | Context rot, hard to scan        |
| Duplicate info            | Wastes tokens, creates confusion |
| No timestamps             | Can't assess relevance           |
| Dense paragraphs          | Hard to parse quickly            |
| Outdated info             | Misleads agent                   |
| All context always loaded | Attention dilution               |

---

## Claude Code Integration

Claude Code uses hybrid approach:

- `CLAUDE.md` loaded naively upfront (core instructions)
- Tools like glob/grep for just-in-time retrieval
- Memory tools for persistent notes

**Similar pattern for Memory Bank:**

- Core files always loaded (brief, context)
- Domain files loaded as needed
- Archive for long-term reference

---

## Summary

1. **Small files, focused content** - Each file has single responsibility
2. **Load minimally** - Only what's needed for current task
3. **Update frequently** - Keep context current
4. **Archive aggressively** - Move old info out of active context
5. **Trust the system** - Agent reads all specified files

---

## Sources

- Anthropic: "Effective context engineering for AI agents" (2025)
- Claude Code: CLAUDE.md best practices
- Industry: Context engineering guides (2025-2026)
