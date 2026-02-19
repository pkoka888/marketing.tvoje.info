# Memory Bank Automation Guide

Research on automating Memory Bank management for AI agents (2025-2026).

---

## Automation Approaches

### 1. Framework-Based (Recommended for Production)

| Framework               | Best For                   | Memory Features                           |
| ----------------------- | -------------------------- | ----------------------------------------- |
| **Mem0**                | Scalable production agents | Auto-extraction, consolidation, retrieval |
| **LangMem** (LangChain) | LangGraph users            | Prompt optimization, behavior learning    |
| **Letta**               | Stateful agents            | Persistent memory, server mode            |
| **LlamaIndex**          | RAG-heavy apps             | Index-based retrieval                     |

### 2. Claude Code Plugins

| Plugin                          | Purpose                             |
| ------------------------------- | ----------------------------------- |
| **Claude Mem**                  | Real-time observation capture       |
| **claude-code-semantic-memory** | Transcript → embeddings → retrieval |
| **claude-memory-bank**          | Structured context management       |

### 3. Custom Scripts (For Our Use Case)

#### Compaction Script

```python
# scripts/memory_compact.py
import os
import json
from datetime import datetime

MEMORY_BANK = ".kilocode/rules/memory-bank"
ARCHIVE = f"{MEMORY_BANK}/.archive"
MAX_AGE_DAYS = 7

def compact_context():
    """Move old context entries to archive."""
    files = os.listdir(MEMORY_BANK)
    for f in files:
        if f.startswith('.') or f.endswith('.md'):
            path = os.path.join(MEMORY_BANK, f)
            mtime = os.path.getmtime(path)
            age_days = (datetime.now().timestamp() - mtime) / 86400
            if age_days > MAX_AGE_DAYS:
                archive_path = f"{ARCHIVE}/{datetime.now().strftime('%Y-%m')}/{f}"
                os.makedirs(os.path.dirname(archive_path), exist_ok=True)
                os.rename(path, archive_path)

def summarize_old_entries():
    """Use LLM to summarize archived entries."""
    # Implementation: read archived files, summarize with LLM, keep summary
    pass

if __name__ == "__main__":
    compact_context()
```

#### Auto-Update Script

```python
# scripts/memory_update.py
import os
import json
from datetime import datetime

def update_context():
    """Update context.md with current state."""
    context_file = ".kilocode/rules/memory-bank/context.md"

    # Read git status
    os.system("git status --porcelain > /tmp/git_status.txt")

    # Read package.json for dependencies
    # Read .clinerules for agent configs

    # Generate new context
    new_content = f"""# Context - Current State

**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}

## Current Work Focus

[Auto-generated based on git diff, plans/, active tasks]

## Recent Changes

[Auto-extracted from git log --oneline -10]
"""
    # Write to file
    pass

if __name__ == "__main__":
    update_context()
```

---

## Compaction Strategies

### Strategy Comparison

| Strategy    | When to Use        | Pros              | Cons                |
| ----------- | ------------------ | ----------------- | ------------------- |
| **Summary** | Long conversations | Preserves context | May lose nuance     |
| **Trim**    | Preserve recent    | Simple            | Loses early context |
| **Edit**    | Remove redundant   | Precise           | Requires logic      |
| **Native**  | OpenAI/Anthropic   | Automatic         | Provider-specific   |

### Implementation

```python
# Claude Code compaction approach
async def compact_messages(messages, model):
    """Summarize old messages, keep recent."""
    recent = messages[-10:]  # Keep last 10
    old = messages[:-10]

    summary = await model.invoke(f"""
    Summarize this conversation concisely, preserving:
    - Key decisions
    - Important findings
    - Unresolved issues

    Messages: {old}
    """)

    return [{"role": "system", "content": f"Summary: {summary}"}] + recent
```

---

## Context Retrieval

### Semantic Search

```python
# scripts/memory_retrieve.py
import subprocess

def retrieve_relevant_context(query, top_k=3):
    """Use embeddings to find relevant memory."""
    # 1. Embed query
    # 2. Search vector DB
    # 3. Return top results
    pass
```

### Just-in-Time Loading

```
OpenCode approach:
1. brief.md + context.md → always loaded
2. architecture.md → only for code tasks
3. tech.md → only for setup/build tasks
4. servers.md → only for server tasks
```

---

## Recommended Architecture for Our Project

```
┌─────────────────────────────────────────┐
│           Memory Bank                    │
├─────────────────────────────────────────┤
│ brief.md        → Always                │
│ context.md      → Always                │
│ architecture.md → Code tasks only       │
│ tech.md        → Build tasks only      │
│ servers.md     → Server ops only       │
│ tasks.md       → Workflow tasks        │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│       Automation Scripts                 │
├─────────────────────────────────────────┤
│ - memory_compact.py  (weekly)           │
│ - memory_update.py   (on context change)│
│ - memory_retrieve.py (semantic search)  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         Redis (Optional)                │
├─────────────────────────────────────────┤
│ - Session state                         │
│ - Cross-session memory                  │
│ - Agent coordination                    │
└─────────────────────────────────────────┘
```

---

## Implementation Priority

1. **Phase 1**: Create compaction script
   - Archive files older than 7 days
   - Weekly cron job

2. **Phase 2**: Auto-update context
   - Git diff → context changes
   - Run before each session

3. **Phase 3**: Semantic retrieval
   - Embed memory files
   - Query relevant context

4. **Phase 4**: Redis integration
   - Session state
   - Cross-agent memory

---

## Tools & Resources

- **Mem0**: https://docs.mem0.ai/
- **LangMem**: https://github.com/langchain-ai/langmem
- **Claude Mem**: https://claudetools.org/claude-mem
- **Semantic Memory**: https://github.com/zacdcook/claude-code-semantic-memory
- **Anthropic Compaction**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
