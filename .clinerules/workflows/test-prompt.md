<task name="Test Prompt">

<task_objective>
Guide the user through testing a prompt with sample inputs to validate its effectiveness, identify issues, and gather feedback for improvements. The output will be a comprehensive test report with results, analysis, and recommendations.
</task_objective>

<detailed_sequence_steps>
# Test Prompt Process - Detailed Sequence of Steps

## 1. Identify Prompt to Test

1. Use the `ask_followup_question` command to ask the USER for the prompt they want to test.
   
2. If the prompt is in a file, use the `read_file` command to read the prompt content.
   
3. If the prompt is provided directly in the chat, proceed with the provided content.

4. Confirm the prompt content with the USER before proceeding with testing.

## 2. Define Test Objectives

1. Use the `ask_followup_question` command to ask the USER about:
   - What aspects of the prompt to test (clarity, output quality, consistency, etc.)
   - The target AI model or system
   - Success criteria for the test
   - Any specific concerns or issues to investigate
   - Number of test cases to run

2. Document the test objectives for the testing process.

## 3. Design Test Cases

Design comprehensive test cases to validate the prompt:

### Test Case Categories

1. **Basic Functionality**
   - Standard input within expected parameters
   - Typical use case scenario
   - Expected output format

2. **Edge Cases**
   - Minimal input
   - Maximum input
   - Unusual but valid input
   - Boundary conditions

3. **Error Handling**
   - Invalid input
   - Missing required information
   - Conflicting requirements
   - Ambiguous input

4. **Complex Scenarios**
   - Multi-part requests
   - Nested requirements
   - Context-heavy input
   - Domain-specific terminology

5. **Consistency Testing**
   - Similar inputs with variations
   - Repeated inputs
   - Different phrasing of same request

1. Present the proposed test cases to the USER.
   
2. Use the `ask_followup_question` command to confirm or modify the test cases.

## 4. Execute Test Cases

For each test case:

### Test Execution Process

1. **Prepare Input**
   - Format input according to prompt requirements
   - Include all necessary context
   - Ensure input is complete and valid

2. **Execute Prompt**
   - Submit input to the target AI model
   - Record the output
   - Note any errors or issues

3. **Document Results**
   - Input provided
   - Output received
   - Time taken (if relevant)
   - Any errors or warnings

4. **Evaluate Output**
   - Does output meet expectations?
   - Is format correct?
   - Is content accurate?
   - Are there any issues?

1. Present test results to the USER as they are completed.
   
2. Use the `ask_followup_question` command to confirm results before proceeding.

## 5. Analyze Test Results

Analyze the test results across all test cases:

### Success Metrics
- Percentage of successful test cases
- Output quality ratings
- Consistency across similar inputs
- Error handling effectiveness

### Issues Identified
- Patterns in failures
- Common error types
- Edge cases not handled
- Inconsistencies in output

### Strengths Observed
- What the prompt handles well
- Where it performs consistently
- Effective elements identified
- Best test case results

### Areas for Improvement
- Specific issues found
- Missing functionality
- Inadequate instructions
- Context gaps

## 6. Generate Test Report

Create a comprehensive test report with the following sections:

### Executive Summary
- Overall test results
- Success rate
- Key findings
- Overall assessment

### Detailed Test Results
- Test case name
- Input provided
- Output received
- Evaluation (Pass/Fail)
- Notes and observations

### Analysis
- Success metrics
- Issues identified
- Strengths observed
- Areas for improvement

### Recommendations
- Prioritized list of improvements
- Specific suggestions for each issue
- Expected impact of improvements
- Implementation difficulty

### Next Steps
- Recommended actions
- Additional testing needed
- Follow-up tasks

## 7. Present Test Report

1. Use the `attempt_completion` command to present the test report to the USER.
   
2. Include:
   - Executive summary
   - Detailed test results
   - Analysis and findings
   - Recommendations
   
3. Offer to:
   - Implement the recommended improvements
   - Create an optimized version of the prompt
   - Run additional tests
   - Create test cases for related prompts

</detailed_sequence_steps>

</task>
