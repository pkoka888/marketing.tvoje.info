<task name="Analyze Prompt">

<task_objective>
Guide the user through a comprehensive analysis of an existing prompt to evaluate its clarity, specificity, effectiveness, and potential for improvement. The output will be a detailed analysis report with specific recommendations for optimization.
</task_objective>

<detailed_sequence_steps>
# Analyze Prompt Process - Detailed Sequence of Steps

## 1. Identify the Prompt to Analyze

1. Use the `ask_followup_question` command to ask the USER for the prompt they want to analyze.

2. If the prompt is in a file, use the `read_file` command to read the prompt content.

3. If the prompt is provided directly in the chat, proceed with the provided content.

4. Confirm the prompt content with the USER before proceeding with analysis.

## 2. Understand the Prompt Context

1. Use the `ask_followup_question` command to ask the USER about:
   - The intended purpose of the prompt
   - The target AI model or system
   - The expected output format
   - Any specific constraints or requirements
   - The target audience or use case

2. Document the context information for the analysis.

## 3. Perform Comprehensive Analysis

Analyze the prompt across the following dimensions:

### Clarity and Specificity
- Is the prompt clear and unambiguous?
- Does it use specific language rather than vague terms?
- Are the instructions precise and actionable?
- Is the scope well-defined?

### Structure and Organization
- Does the prompt have a logical structure?
- Are sections clearly delineated?
- Is the formatting consistent?
- Does it follow established prompt patterns?

### Context and Background
- Does the prompt provide sufficient context?
- Is relevant background information included?
- Are examples provided where helpful?
- Is the target audience considered?

### Output Specification
- Is the expected output format clearly defined?
- Are constraints on length or style specified?
- Are examples of desired output provided?
- Is the evaluation criteria clear?

### Potential Issues
- Are there ambiguous terms or phrases?
- Could the prompt be misinterpreted?
- Are there conflicting instructions?
- Is the prompt too long or too short?

### Strengths
- What does the prompt do well?
- What are its effective elements?
- What makes it successful in its current form?

## 4. Generate Analysis Report

Create a comprehensive analysis report with the following sections:

### Executive Summary
- Overall assessment of the prompt
- Key strengths identified
- Primary areas for improvement
- Overall effectiveness rating (1-10)

### Detailed Analysis
- Clarity and Specificity: Assessment and specific feedback
- Structure and Organization: Assessment and specific feedback
- Context and Background: Assessment and specific feedback
- Output Specification: Assessment and specific feedback

### Issues Identified
- List of specific issues found
- Severity of each issue (Critical, Major, Minor)
- Impact on prompt effectiveness

### Recommendations
- Prioritized list of improvements
- Specific suggestions for each improvement
- Expected impact of each improvement
- Implementation difficulty (Easy, Medium, Hard)

### Alternative Approaches
- Suggest 2-3 alternative prompt structures
- Explain the rationale for each alternative
- Compare with the original prompt

## 5. Present Findings to User

1. Use the `attempt_completion` command to present the analysis report to the USER.

2. Include specific, actionable recommendations.

3. Offer to help implement the recommended improvements.

4. Ask if the USER would like to:
   - Implement the recommended improvements
   - Create an optimized version of the prompt
   - Test the prompt with sample inputs
   - Analyze another prompt

</detailed_sequence_steps>

</task>
