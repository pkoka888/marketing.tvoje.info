<task name="Create Prompt">

<task_objective>
Guide the user through the process of creating a new, effective prompt following prompt engineering best practices. The output will be a well-structured prompt optimized for the specified use case and target AI model.
</task_objective>

<detailed_sequence_steps>
# Create Prompt Process - Detailed Sequence of Steps

## 1. Define Prompt Purpose

1. Use the `ask_followup_question` command to ask the USER for:
   - The primary purpose of the prompt
   - What the prompt should accomplish
   - The target AI model or system
   - The intended use case or scenario

2. Document the purpose information for prompt creation.

## 2. Gather Requirements

1. Use the `ask_followup_question` command to ask the USER about:
   - Expected output format (text, code, JSON, etc.)
   - Any specific constraints or limitations
   - Target audience or persona
   - Tone and style requirements
   - Length requirements (if any)
   - Any examples or templates to include

2. Document all requirements for the prompt.

## 3. Determine Prompt Structure

Based on the purpose and requirements, determine the appropriate prompt structure:

### Common Prompt Structures
- **Role-Based**: Define a role or persona for the AI
- **Task-Based**: Focus on a specific task or action
- **Chain-of-Thought**: Guide the AI through reasoning steps
- **Few-Shot**: Provide examples for the AI to follow
- **Structured**: Use clear sections and formatting

1. Recommend the most appropriate structure to the USER.

2. Use the `ask_followup_question` command to confirm the structure choice.

## 4. Draft the Prompt

Create a draft prompt following the chosen structure and best practices.

## 5. Review and Refine

Review the draft prompt against best practices and incorporate USER feedback.

## 6. Finalize the Prompt

1. Incorporate USER feedback into the prompt.
2. Make final adjustments based on best practices.
3. Ensure proper formatting and structure.
4. Create the final prompt file or provide the prompt content.

## 7. Present Final Prompt

1. Use the `attempt_completion` command to present the final prompt to the USER.
2. Include the prompt content and documentation.
3. Offer to test the prompt with sample inputs.

</detailed_sequence_steps>

</task>
