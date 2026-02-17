<task name="Optimize Prompt">

<task_objective>
Guide the user through optimizing an existing prompt to improve its effectiveness, clarity, and consistency. The output will be an optimized version of the prompt with a comparison to the original and explanation of improvements made.
</task_objective>

<detailed_sequence_steps>
# Optimize Prompt Process - Detailed Sequence of Steps

## 1. Identify Prompt to Optimize

1. Use the `ask_followup_question` command to ask the USER for the prompt they want to optimize.
   
2. If the prompt is in a file, use the `read_file` command to read the prompt content.
   
3. If the prompt is provided directly in the chat, proceed with the provided content.

4. Confirm the prompt content with the USER before proceeding with optimization.

## 2. Understand Optimization Goals

1. Use the `ask_followup_question` command to ask the USER about:
   - Specific issues they've experienced with the prompt
   - What they want to improve (clarity, consistency, output quality, etc.)
   - The target AI model or system
   - Any specific constraints or requirements
   - Priority areas for improvement

2. Document the optimization goals for the prompt.

## 3. Analyze Current Prompt

Perform a comprehensive analysis of the current prompt:

### Strengths Analysis
- What does the prompt do well?
- What are its effective elements?
- Why has it been successful (if applicable)?

### Weaknesses Analysis
- Where is the prompt unclear or ambiguous?
- What instructions are missing or incomplete?
- Are there conflicting or redundant instructions?
- Is the structure optimal for the task?

### Areas for Improvement
- Clarity and specificity
- Structure and organization
- Context and background
- Output specification
- Examples and guidance
- Constraints and guidelines

## 4. Develop Optimization Strategy

Based on the analysis, develop a strategy for optimization:

### Optimization Techniques to Consider

1. **Clarification**
   - Replace vague terms with specific language
   - Add missing context and background
   - Define ambiguous terms
   - Specify constraints clearly

2. **Structural Improvements**
   - Reorganize for better flow
   - Add clear section headers
   - Use consistent formatting
   - Implement logical progression

3. **Enhanced Instructions**
   - Add step-by-step guidance
   - Include examples and templates
   - Specify output format clearly
   - Add evaluation criteria

4. **Context Enhancement**
   - Add relevant background information
   - Include target audience considerations
   - Specify persona or role
   - Add domain-specific context

5. **Output Optimization**
   - Define expected output format
   - Specify length and style requirements
   - Include examples of desired output
   - Add quality criteria

1. Present the optimization strategy to the USER.
   
2. Use the `ask_followup_question` command to confirm the approach.

## 5. Create Optimized Prompt

Create an optimized version of the prompt following the strategy:

### Optimization Implementation

1. **Apply Clarifications**
   - Replace vague terms with specific language
   - Add missing context
   - Define ambiguous terms
   - Specify constraints

2. **Improve Structure**
   - Reorganize for better flow
   - Add clear section headers
   - Use consistent formatting
   - Implement logical progression

3. **Enhance Instructions**
   - Add step-by-step guidance
   - Include examples
   - Specify output format
   - Add evaluation criteria

4. **Add Context**
   - Include relevant background
   - Specify persona or role
   - Add domain-specific context

5. **Optimize Output**
   - Define expected format
   - Specify requirements
   - Include examples
   - Add quality criteria

## 6. Compare Original and Optimized

Create a comparison document:

### Side-by-Side Comparison
- Original prompt sections
- Optimized prompt sections
- Highlighted changes

### Improvements Summary
- List of specific improvements made
- Rationale for each improvement
- Expected impact on effectiveness

### Metrics Comparison
- Clarity rating (before/after)
- Specificity rating (before/after)
- Completeness rating (before/after)
- Overall effectiveness rating (before/after)

## 7. Validate Optimized Prompt

Validate the optimized prompt against best practices:

### Validation Checklist
- [ ] Language is clear and unambiguous
- [ ] Instructions are specific and actionable
- [ ] Structure is logical and organized
- [ ] Context is sufficient and relevant
- [ ] Output format is clearly defined
- [ ] Examples are helpful and appropriate
- [ ] Constraints are specified
- [ ] No conflicting or redundant instructions

1. Present the optimized prompt and comparison to the USER.
   
2. Use the `ask_followup_question` command to ask for feedback.

## 8. Finalize and Document

1. Incorporate USER feedback into the optimized prompt.
   
2. Make final adjustments.
   
3. Create documentation for the optimized prompt:
   - Version number and date
   - Changes made
   - Rationale for changes
   - Testing recommendations

## 9. Present Final Result

1. Use the `attempt_completion` command to present the final optimized prompt to the USER.
   
2. Include:
   - The optimized prompt
   - Comparison with original
   - Summary of improvements
   - Documentation of changes
   
3. Offer to:
   - Test the optimized prompt with sample inputs
   - Create additional variations
   - Optimize further based on testing results
   - Create prompts for related tasks

</detailed_sequence_steps>

</task>
