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

Create a draft prompt following the chosen structure and best practices:

### Prompt Components to Include

1. **Role/Persona Definition** (if applicable)
   - Clear definition of the AI's role
   - Relevant expertise or perspective
   - Tone and style guidelines

2. **Context and Background**
   - Relevant background information
   - Context for the task
   - Assumptions or constraints

3. **Task Instructions**
   - Clear, specific instructions
   - Step-by-step guidance if needed
   - Actionable directives

4. **Output Specifications**
   - Expected output format
   - Length constraints
   - Style requirements
   - Examples of desired output

5. **Examples** (if applicable)
   - Few-shot examples
   - Input-output pairs
   - Edge cases to handle

6. **Constraints and Guidelines**
   - What to avoid
   - Specific requirements
   - Quality criteria

## 5. Review and Refine

Review the draft prompt against best practices:

### Clarity Check
- Is the language clear and unambiguous?
- Are instructions specific and actionable?
- Is the scope well-defined?

### Completeness Check
- Is all necessary context included?
- Are constraints clearly specified?
- Is the output format defined?

### Effectiveness Check
- Will this produce the desired results?
- Are examples helpful and relevant?
- Is the structure appropriate for the task?

1. Present the draft prompt to the USER.
   
2. Use the `ask_followup_question` command to ask for feedback and refinements.

## 6. Finalize the Prompt

1. Incorporate USER feedback into the prompt.
   
2. Make final adjustments based on best practices.
   
3. Ensure proper formatting and structure.

4. Create the final prompt file or provide the prompt content.

## 7. Provide Documentation

Create documentation for the prompt including:

### Prompt Metadata
- Name and purpose
- Target AI model
- Creation date
- Version number

### Usage Instructions
- How to use the prompt
- Required inputs
- Expected outputs

### Testing Recommendations
- Suggested test cases
- Evaluation criteria
- Common issues to watch for

### Version History
- Initial version notes
- Known limitations
- Future improvement ideas

## 8. Present Final Prompt

1. Use the `attempt_completion` command to present the final prompt to the USER.
   
2. Include the prompt content and documentation.
   
3. Offer to:
   - Test the prompt with sample inputs
   - Create variations of the prompt
   - Optimize the prompt further
   - Create additional prompts for related tasks

</detailed_sequence_steps>

</task>
