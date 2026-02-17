<task name="Optimize Prompt">

<task_objective>
Guide the user through optimizing an existing prompt to improve its effectiveness, clarity, and consistency. The output will be an optimized version of the prompt with a comparison to the original and explanation of improvements made.
</task_objective>

<detailed_sequence_steps>
# Optimize Prompt Process - Detailed Sequence of Steps

## 1. Identify Prompt to Optimize

1. Use the `ask_followup_question` command to ask the USER for the prompt they want to optimize.
2. Confirm the prompt content with the USER before proceeding with optimization.

## 2. Understand Optimization Goals

1. Use the `ask_followup_question` command to ask the USER about:
   - Specific issues they've experienced with the prompt
   - What they want to improve (clarity, consistency, output quality, etc.)
   - The target AI model or system

## 3. Analyze Current Prompt

Perform a comprehensive analysis of the current prompt:
- Strengths: What does the prompt do well?
- Weaknesses: Where is it unclear or ambiguous?
- Areas for Improvement: Clarity, structure, context, output spec

## 4. Create Optimized Prompt

Apply optimization techniques:
1. Clarification — replace vague terms with specific language
2. Structural Improvements — reorganize for better flow
3. Enhanced Instructions — add step-by-step guidance
4. Context Enhancement — add relevant background information
5. Output Optimization — define expected format clearly

## 5. Compare Original and Optimized

Create a comparison with:
- Side-by-Side comparison
- Improvements Summary
- Metrics Comparison (clarity, specificity, completeness before/after)

## 6. Present Final Result

1. Use the `attempt_completion` command to present the final optimized prompt to the USER.
2. Include the optimized prompt, comparison with original, and summary of improvements.

</detailed_sequence_steps>

</task>
