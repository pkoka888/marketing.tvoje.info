# Root Cause Analysis: Infinite Context Condensation Loop

**Date**: 2026-02-16
**Incident ID**: INC-2026-02-16-001
**Severity**: P1 - High
**Status**: Analysis Complete

---

## Executive Summary

A Kilo Code session entered an infinite context condensation loop when tasked with a simple YAML modification. The AI correctly understood the task and required fix but failed to transition from "understanding" to "executing" action. The root cause was a combination of context window saturation from bloated Memory Bank files and a condensation mechanism that preserved semantic understanding without preserving executable state (the "next action" to take).

---

## Loop Characteristics

### Observable Symptoms

- **15+ consecutive condensation cycles** without progress (lines 5700-5730 in task log)
- **Identical summaries repeated verbatim** - each summary accurately captured the task
- **No tool execution between condensations** - only `read_file` calls, never `edit_file`
- **No `attempt_completion` called** - session never reached completion state
- **Escalating pattern** - multiple `[Reasoning]` blocks without intervening actions

### Loop Pattern (Repeated 10+ times)

```
[Reasoning]
Condensing conversation context...
# Conversation Summary
[Tool Use: read_file]
Files: [{ "path": ".github/workflows/ci.yml" }]
```

### Critical Observation

The AI's summary during condensation was **accurate and complete**:

- Correctly identified the task: Add `PUBLIC_SITE_URL` to accessibility job
- Correctly identified the location: Lines 80-81 in `.github/workflows/ci.yml`
- Correctly identified the next step: "Apply the modification to lines 80-81"

**Yet it never executed the modification.**

---

## Root Cause Analysis

### Primary Cause: Context Window Saturation + State Loss During Condensation

The infinite loop resulted from a **state machine failure** where:

1. **Context Window Pre-filled**: Before the task started, ~1936 lines of custom instructions (Memory Bank files, AGENTS.md, debug rules) consumed the majority of the context window.

2. **First Action Triggered Condensation**: The first `read_file` call pushed the context window over its limit, triggering automatic condensation.

3. **Condensation Preserved Understanding, Not Action State**: The condensation summary preserved:
   - What the task was (semantic understanding)
   - What file to modify (knowledge)
   - What the fix should look like (planning)

   But it **did not preserve**:
   - The fact that the file had already been read
   - The next action to take (edit_file, not read_file again)

4. **Loop Formation**: After condensation, the AI "woke up" with understanding but no memory of having already read the file, so it read it again → triggered condensation → repeat.

### Secondary Cause: Model Context Window Limitations

The model used (`z-ai/glm-5:free`) is a free-tier model with potentially limited context window capacity. This exacerbated the context saturation problem.

### Evidence from Task Log

**Lines 2041-2057** (First action → immediate condensation):

```
**Assistant:**
[Memory Bank: Active]
I'll read the current CI workflow file to locate the accessibility job's build step and add the missing environment variable.
[Tool Use: read_file]
Files: [{ "path": ".github/workflows/ci.yml" }]

---
**Assistant:**
[Reasoning]
Condensing conversation context...
```

**Lines 5770-5782** (Summary shows correct understanding but no action state):

```markdown
## 6. Pending Tasks and Next Steps:

- **Task: Add `PUBLIC_SITE_URL` environment variable to accessibility job**
  - Next step: Apply the modification to lines 80-81 in `.github/workflows/ci.yml`
```

The summary correctly states "Next step: Apply the modification" but the AI then calls `read_file` again instead of `edit_file`.

---

## Contributing Factors

### 1. Memory Bank Bloat

- **10 Memory Bank files** loaded at task start (mandatory per rules)
- **~1936 lines** of custom instructions before task content
- Files include: brief.md, product.md, context.md, architecture.md, tech.md, servers.md, agents-state.md, tasks-queue.md, verification-history.md, memory-bank-instructions.md

### 2. Redundant Rule Loading

- AGENTS.md loaded (8020 chars)
- Debug rules loaded (multiple files)
- Memory bank instructions loaded twice (once as standalone, once referenced)

### 3. Free-Tier Model Limitations

- Model: `z-ai/glm-5:free`
- Likely has smaller context window than paid models
- May have less sophisticated state management during condensation

### 4. No Action State Tracking

- Condensation mechanism preserves semantic content
- No explicit "current action" or "next action" state preserved
- AI "forgets" it already read the file after condensation

### 5. Missing Progress Guardrails

- No detection of repeated identical actions
- No "loop detection" mechanism to break cycles
- No maximum condensation count limit

---

## Recommendations for Prevention

### Immediate (P0)

1. **Add Loop Detection**
   - Track consecutive identical tool calls
   - Break loop after 3 consecutive identical actions
   - Log warning and prompt user for intervention

2. **Preserve Action State in Condensation**
   - Include explicit "NEXT_ACTION" field in condensation summary
   - Format: `NEXT_ACTION: edit_file(path=".github/workflows/ci.yml", ...)`
   - Ensure AI reads and executes NEXT_ACTION after condensation

### Short-Term (P1)

3. **Reduce Memory Bank Footprint**
   - Consolidate 10 memory bank files into 3-4 essential files
   - Remove redundant content (verification-history.md can be external)
   - Implement "lazy loading" for non-essential memory bank content

4. **Add Condensation Counter**
   - Track number of condensations in current session
   - Warn user after 5 condensations
   - Force user intervention after 10 condensations

5. **Model Selection for Complex Tasks**
   - Use larger context window models for tasks requiring extensive rules
   - Consider `z-ai/glm-5:free` only for simple tasks

### Medium-Term (P2)

6. **Implement Action Checkpointing**
   - Before condensation, write current action state to temporary storage
   - After condensation, restore action state from checkpoint
   - Ensure continuity of execution across condensation boundaries

7. **Context Budget Management**
   - Calculate context usage before task execution
   - Warn if pre-task context exceeds 50% of window
   - Suggest context reduction or model upgrade

8. **Add "Already Read" Tracking**
   - Track files that have been read in current session
   - Skip re-reading if content is in summary
   - Force action transition after read

### Long-Term (P3)

9. **Architectural Review of Memory Bank System**
   - Evaluate necessity of mandatory loading for all tasks
   - Implement task-specific memory bank subsets
   - Consider external memory bank with on-demand loading

10. **Condensation Algorithm Improvement**
    - Preserve execution state, not just semantic understanding
    - Include "action queue" in condensation output
    - Maintain tool call history in condensed form

---

## Appendix: Task Log Evidence

### Task Definition (Lines 1-46)

```
## Task: Fix GitHub Actions CI Workflow

**Priority**: P1 - High

### Problem Description
The CI workflow is failing because the accessibility job is missing the `PUBLIC_SITE_URL` environment variable that the build job has.

### Required Fix
Add the `PUBLIC_SITE_URL` environment variable to the accessibility job's build step.

**Location**: `.github/workflows/ci.yml`, around lines 80-81
```

### First AI Response (Lines 2041-2051)

```
[Memory Bank: Active]
I'll read the current CI workflow file to locate the accessibility job's build step and add the missing environment variable.
[Tool Use: read_file]
Files: [{ "path": ".github/workflows/ci.yml" }]
```

### Condensation Loop (Lines 5700-5730)

```
[Reasoning]
Condensing conversation context. The summary below captures the key information from the prior conversation.
[Reasoning]
Condensing conversation context. The summary below captures the key information from the prior conversation.
[Reasoning]
Condensing conversation context. The summary below captures the key information from the prior conversation.
... (repeated 15+ times)
```

### Accurate Summary That Should Have Led to Action (Lines 5731-5782)

````markdown
# Conversation Summary

## 1. Previous Conversation:

The user provided a specific, well-defined task to fix a GitHub Actions CI workflow issue...

## 6. Pending Tasks and Next Steps:

- **Task: Add `PUBLIC_SITE_URL` environment variable to accessibility job**
  - Next step: Apply the modification to lines 80-81 in `.github/workflows/ci.yml`
  - Required change:
    ```yaml
    - name: Build project
      run: npm run build
      env:
        PUBLIC_SITE_URL: https://portfolio.tvoje.info
    ```
````

---

## Conclusion

The infinite context condensation loop was caused by a fundamental mismatch between the condensation mechanism's design (preserve semantic understanding) and the execution model's requirements (need action state continuity). The AI "understood" the task perfectly but "forgot" it had already gathered the necessary information and needed to proceed to action.

**Primary Prevention**: Implement action state preservation in condensation summaries and loop detection for repeated identical actions.

---

**Document Version**: 1.0
**Author**: Kilo Code Debug Mode
**Review Date**: 2026-02-23
