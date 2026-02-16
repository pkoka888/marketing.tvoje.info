# Antigravity Subagent Delegation Guide

## Overview

This document defines how Antigravity should properly delegate tasks to subagents (Kilo Code, Groq, etc.) for optimal workflow execution.

---

## Subagent Registry

| Subagent      | Command        | Model                   | Best For                        | Status         |
| ------------- | -------------- | ----------------------- | ------------------------------- | -------------- |
| **Kilo Code** | `kilo run`     | z-ai/glm4.7             | Code implementation, file edits | Available      |
| **Groq**      | Direct API     | llama-3.3-70b-versatile | Fast inference, research        | Available      |
| **Cline**     | `cline` CLI    | minimax-m2.1:free       | Validation, testing             | Manual         |
| **LiteLLM**   | localhost:4000 | Multiple                | Unified API, model switching    | Requires setup |

---

## Delegation Principles

### 1. Task Classification

| Task Type              | Preferred Subagent | Rationale                   |
| ---------------------- | ------------------ | --------------------------- |
| Code implementation    | Kilo Code          | Can execute file operations |
| Research/SERP          | Antigravity (self) | Has native web search       |
| Fast text generation   | Groq (direct)      | Low latency                 |
| Quality validation     | Cline              | ESLint, testing             |
| Multi-model comparison | LiteLLM            | Model routing               |

### 2. Delegation Protocol

**Step 1: Assess**

- Is this task within my primary capability? → If yes, do it
- Does it require execution/ file operations? → Delegate to Kilo Code
- Does it require specific model? → Use appropriate subagent

**Step 2: Prepare**

- Create clear task brief for subagent
- Define expected output format
- Set success criteria
- Provide necessary context

**Step 3: Delegate**

- Use proper command syntax
- Wait for completion
- Validate output against criteria

**Step 4: Integrate**

- Merge subagent output
- Verify consistency
- Report final results

---

## Subagent Commands

### Kilo Code Delegation

```markdown
# Delegate to Kilo Code

Kilo Code: Execute the following task:
[TASK_DESCRIPTION]

Requirements:

- Use z-ai/glm4.7 model
- Report results in markdown
- If errors, attempt fixes before reporting failure

Output format:
[EXPECTED_OUTPUT_FORMAT]
```

### Groq Direct API

```python
# When using Groq for fast inference
# Note: Must set GROQ_API_KEY in environment
import os
os.environ['GROQ_API_KEY'] = 'gsk_...'

from litellm import completion
response = completion(
    model='groq/llama-3.3-70b-versatile',
    messages=[{'role': 'user', 'content': 'TASK'}]
)
```

### LiteLLM Proxy

```bash
# Start proxy
python litellm/start_litellm.py

# Test
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "groq/llama-3.3-70b-versatile", "messages": [...]}'
```

---

## Task Templates

### Template 1: Research Delegation

```markdown
# Research Task

Research: [TOPIC]
Sources to check:

- [SOURCE_1]
- [SOURCE_2]

Output: Markdown summary with:

- Key findings
- Data points
- Recommendations
```

### Template 2: Implementation Delegation

```markdown
# Implementation Task

Target: [FILE_PATH]
Change: [DESCRIPTION]

Requirements:

- Preserve existing code style
- Add tests if applicable
- Update documentation if needed

Validation: [HOW_TO_VERIFY]
```

### Template 3: Validation Delegation

```markdown
# Validation Task

Target: [FILE_PATH or CODE]
Criteria:

- [CRITERION_1]
- [CRITERION_2]

Output: Pass/Fail with details
```

---

## Error Handling

### Subagent Failure Protocol

| Error Type           | Action                          |
| -------------------- | ------------------------------- |
| Timeout              | Retry once, then escalate       |
| Auth Error           | Check API keys, report          |
| Implementation Error | Attempt fix, report if persists |
| Validation Fail      | Report specific failures        |

### Escalation Rules

If subagent fails:

1. Retry once with modified prompt
2. If still failing, attempt self-implementation if capable
3. If unable, report with full context and recommendations

---

## Examples

### Example 1: Research Task

**User**: "Research top 20 marketing agencies in Czech Republic"

**Antigravity Approach**:

1. Use native web search (has SERP capability)
2. Compile findings directly
3. No delegation needed - this is primary capability

### Example 2: Code Implementation

**User**: "Fix the build error in growth-funnel.md"

**Antigravity Approach**:

1. Analyze the error
2. Delegate to Kilo Code:

```
Kilo Code: Fix the content schema error in src/content/projects/growth-funnel.md
Error: category "growth" not in enum [devops, ai, web, infrastructure]
Fix: Change category to "web" and add missing year field
```

### Example 3: Complex Multi-Step

**User**: "Research and create PRD for marketing automation platform"

**Antigravity Approach**:

1. Use native search for research
2. Compile market data
3. Delegate implementation to Kilo Code if needed:

```
Kilo Code: Create PRD document at docs/prd-data/marketing-automation-prd.md
Based on research data in docs/prd-data/marketing-agencies-summary.md
Follow template: .agents/templates/prd/detailed-prd.md
```

---

## Configuration

### Environment Variables

```bash
# Groq (for direct API)
GROQ_API_KEY=gsk_...

# LiteLLM Proxy (optional)
LITELLM_PROXY_URL=http://localhost:4000

# Kilo Code (VS Code extension)
# Configure in VS Code settings
```

### Subagent Availability Check

```bash
# Check Groq
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"

# Check Kilo Code
# Available in VS Code with extension installed

# Check LiteLLM
curl http://localhost:4000/health
```

---

## Best Practices

1. **Don't over-delegate**: If you can do it efficiently, do it yourself
2. **Provide context**: Always give subagents sufficient background
3. **Validate output**: Never assume subagent output is correct
4. **Set clear criteria**: Define success metrics before delegation
5. **Handle failures gracefully**: Retry before escalating
6. **Document delegation**: Note what was delegated and why

---

## Quick Reference

| Need                  | Action                     |
| --------------------- | -------------------------- |
| Web research          | Use native capability      |
| Code editing          | Delegate to Kilo Code      |
| Fast text gen         | Use Groq direct            |
| Multi-model           | Use LiteLLM                |
| Validation            | Delegate to Cline          |
| Complex orchestration | Plan → Delegate → Validate |

---

_Last Updated: 2026-02-13_
