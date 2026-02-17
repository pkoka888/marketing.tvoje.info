# /condense

Manage the conversation context window using the official Kilo Code 2026 non-destructive condensation protocol.

## When to use
- Token usage exceeds 80% of the context window.
- The conversation history is long and affecting response latency.
- A major task phase is completed and a fresh baseline is needed.

## Protocol Steps

1. **Analyze History**: Identify key technical decisions, code snippets, and pending tasks.
2. **Draft Summary**: Create a technical recap including:
   - **Previous Conversation**: High-level flow.
   - **Current Work**: Detailed state before condensation.
   - **Key Technical Concepts**: Frameworks, patterns, and conventions.
   - **Relevant Files**: Paths and snippets.
   - **Next Steps**: Direct quotes of what to do next.
3. **Trigger Condense**: Use the `condense` tool with the drafted message.
4. **Verify Baseline**: Ensure the new summary accurately represents the state and allows for task continuation.

## Rules
- **Non-Destructive**: Tagged messages are hidden from the API but remain in the UI/Timeline.
- **Batched**: Do not condense too frequently (wait for at least 3-5 turn cycles).
- **Proactive**: If you notice context filling up, suggest this workflow to the user.
