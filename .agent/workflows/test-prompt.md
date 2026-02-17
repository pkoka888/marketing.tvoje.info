<task name="Test Prompt">

<task_objective>
Guide the user through testing a prompt with sample inputs to validate its effectiveness, identify issues, and gather feedback for improvements. The output will be a comprehensive test report with results, analysis, and recommendations.
</task_objective>

<detailed_sequence_steps>
# Test Prompt Process - Detailed Sequence of Steps

## 1. Identify Prompt to Test

1. Ask the USER for the prompt to test.
2. Confirm the prompt content before proceeding.

## 2. Define Test Objectives

Ask the USER about:
- What aspects to test (clarity, output quality, consistency, etc.)
- The target AI model or system
- Success criteria for the test

## 3. Design Test Cases

Design comprehensive test cases:
1. Basic Functionality — standard input within expected parameters
2. Edge Cases — minimal/maximum/unusual input
3. Error Handling — invalid or ambiguous input
4. Complex Scenarios — multi-part requests
5. Consistency Testing — similar inputs with variations

## 4. Execute Test Cases

For each test case:
1. Prepare Input — format according to prompt requirements
2. Execute Prompt — submit to target AI model
3. Document Results — input, output, errors
4. Evaluate Output — does output meet expectations?

## 5. Analyze Test Results

Analyze across all test cases:
- Success Metrics: percentage of successful cases
- Issues Identified: patterns in failures
- Areas for Improvement: specific issues found

## 6. Generate Test Report

Create a report with:
- Executive Summary
- Detailed Test Results
- Analysis and Findings
- Recommendations

## 7. Present Test Report

Use the `attempt_completion` command to present the test report to the USER.

</detailed_sequence_steps>

</task>
