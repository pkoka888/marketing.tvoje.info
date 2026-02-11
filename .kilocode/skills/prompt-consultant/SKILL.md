---
name: prompt-consultant
description: Comprehensive guidelines for prompt engineering and optimization, including analysis frameworks, creation best practices, testing methodologies, and optimization strategies.
---

# Prompt Consultant Guidelines

This file provides comprehensive guidance for prompt engineering tasks. Use these guidelines when working with prompts in the Prompt Consultant mode.

---

# 1. PROMPT ANALYSIS

## Analysis Framework

When analyzing an existing prompt, evaluate it across these dimensions:

### Clarity and Specificity
- **Language Precision**: Are terms specific and unambiguous?
- **Instruction Clarity**: Are instructions clear and actionable?
- **Scope Definition**: Is the scope well-defined and bounded?
- **Ambiguity Check**: Are there vague or unclear phrases?

### Structure and Organization
- **Logical Flow**: Does the prompt follow a logical progression?
- **Section Delineation**: Are sections clearly marked and organized?
- **Formatting Consistency**: Is formatting consistent throughout?
- **Pattern Adherence**: Does it follow established prompt patterns?

### Context and Background
- **Sufficient Context**: Is enough background information provided?
- **Relevance**: Is all context relevant to the task?
- **Audience Consideration**: Is the target audience considered?
- **Domain Knowledge**: Is necessary domain-specific context included?

### Output Specification
- **Format Definition**: Is the expected output format clearly defined?
- **Constraints Specified**: Are length, style, or other constraints specified?
- **Examples Provided**: Are examples of desired output included?
- **Evaluation Criteria**: Is it clear how output will be evaluated?

## Analysis Process

1. **Read and Understand**: Thoroughly read the prompt to understand its purpose and structure
2. **Identify Strengths**: Note what the prompt does well
3. **Identify Weaknesses**: Note areas for improvement
4. **Categorize Issues**: Group issues by severity (Critical, Major, Minor)
5. **Prioritize Improvements**: Rank improvements by impact and difficulty

## Analysis Output

Provide analysis in this structure:
- Executive Summary
- Detailed Analysis by Dimension
- Issues Identified (with severity)
- Recommendations (prioritized)
- Alternative Approaches

---

# 2. PROMPT CREATION

## Creation Framework

When creating a new prompt, follow this structured approach:

### Phase 1: Requirements Gathering
- **Purpose Definition**: What should the prompt accomplish?
- **Target Model**: Which AI model will be used?
- **Use Case**: What is the specific scenario or use case?
- **Constraints**: Are there any limitations or requirements?
- **Output Format**: What format should the output be in?

### Phase 2: Structure Selection
Choose the appropriate prompt structure:

#### Role-Based Prompts
- Define a clear role or persona
- Specify expertise and perspective
- Set tone and style guidelines
- Use for tasks requiring specific expertise

#### Task-Based Prompts
- Focus on a specific task or action
- Provide clear, actionable instructions
- Use for straightforward, well-defined tasks

#### Chain-of-Thought Prompts
- Guide the AI through reasoning steps
- Encourage explicit thinking process
- Use for complex problem-solving tasks

#### Few-Shot Prompts
- Provide examples for the AI to follow
- Include input-output pairs
- Use for pattern recognition tasks

#### Structured Prompts
- Use clear sections and formatting
- Organize information logically
- Use for complex, multi-part tasks

### Phase 3: Content Creation

Include these components:

1. **Role/Persona Definition** (if applicable)
   - Clear definition of the AI's role
   - Relevant expertise or perspective
   - Tone and style guidelines
   - Behavioral expectations

2. **Context and Background**
   - Relevant background information
   - Context for the task
   - Assumptions or constraints
   - Domain-specific knowledge

3. **Task Instructions**
   - Clear, specific instructions
   - Step-by-step guidance if needed
   - Actionable directives
   - Priority of tasks

4. **Output Specifications**
   - Expected output format
   - Length constraints
   - Style requirements
   - Examples of desired output

5. **Examples** (if applicable)
   - Few-shot examples
   - Input-output pairs
   - Edge cases to handle
   - Common scenarios

6. **Constraints and Guidelines**
   - What to avoid
   - Specific requirements
   - Quality criteria
   - Evaluation standards

### Phase 4: Review and Refine

Review the prompt against these criteria:
- [ ] Language is clear and unambiguous
- [ ] Instructions are specific and actionable
- [ ] Structure is logical and organized
- [ ] Context is sufficient and relevant
- [ ] Output format is clearly defined
- [ ] Examples are helpful and appropriate
- [ ] Constraints are specified
- [ ] No conflicting or redundant instructions

---

# 3. PROMPT TESTING

## Testing Framework

When testing a prompt, use this comprehensive approach:

### Test Case Design

#### Basic Functionality Tests
- Standard input within expected parameters
- Typical use case scenario
- Expected output format validation

#### Edge Case Tests
- Minimal input
- Maximum input
- Unusual but valid input
- Boundary conditions

#### Error Handling Tests
- Invalid input
- Missing required information
- Conflicting requirements
- Ambiguous input

#### Complex Scenario Tests
- Multi-part requests
- Nested requirements
- Context-heavy input
- Domain-specific terminology

#### Consistency Tests
- Similar inputs with variations
- Repeated inputs
- Different phrasing of same request

### Test Execution Process

1. **Prepare Input**: Format input according to prompt requirements
2. **Execute Prompt**: Submit input to the target AI model
3. **Record Output**: Document the output received
4. **Evaluate Output**: Assess against success criteria
5. **Document Results**: Record observations and issues

### Test Metrics

Track these metrics for each test:
- **Success Rate**: Percentage of successful test cases
- **Output Quality**: Rating of output quality (1-10)
- **Consistency**: Consistency across similar inputs
- **Error Handling**: Effectiveness of error handling
- **Time to Response**: Response time (if relevant)

### Test Report Structure

Provide test reports in this format:
- Executive Summary
- Detailed Test Results
- Analysis and Findings
- Recommendations
- Next Steps

---

# 4. PROMPT OPTIMIZATION

## Optimization Framework

When optimizing an existing prompt, follow this systematic approach:

### Analysis Phase

1. **Identify Issues**: Analyze the prompt for problems
2. **Categorize Issues**: Group by type (clarity, structure, context, output)
3. **Prioritize Issues**: Rank by impact and severity
4. **Set Goals**: Define optimization objectives

### Optimization Techniques

#### Clarification Techniques
- Replace vague terms with specific language
- Add missing context and background
- Define ambiguous terms
- Specify constraints clearly

#### Structural Improvements
- Reorganize for better flow
- Add clear section headers
- Use consistent formatting
- Implement logical progression

#### Enhanced Instructions
- Add step-by-step guidance
- Include examples and templates
- Specify output format clearly
- Add evaluation criteria

#### Context Enhancement
- Add relevant background information
- Include target audience considerations
- Specify persona or role
- Add domain-specific context

#### Output Optimization
- Define expected output format
- Specify length and style requirements
- Include examples of desired output
- Add quality criteria

### Optimization Process

1. **Analyze Current Prompt**: Identify strengths and weaknesses
2. **Develop Strategy**: Choose optimization techniques to apply
3. **Create Optimized Version**: Apply improvements systematically
4. **Compare Versions**: Document changes and expected impact
5. **Validate**: Test optimized version against original
6. **Iterate**: Refine based on testing results

### Optimization Documentation

Document optimizations with:
- Version number and date
- Changes made
- Rationale for each change
- Expected impact
- Testing results

---

# 5. BEST PRACTICES

## General Principles

### Clarity
- Use specific, unambiguous language
- Avoid vague terms like "some", "many", "good"
- Define technical terms when used
- Provide examples when helpful

### Specificity
- Be precise about what you want
- Specify constraints and limitations
- Define output format clearly
- Include evaluation criteria

### Structure
- Use clear sections and formatting
- Organize information logically
- Follow a consistent pattern
- Make the prompt scannable

### Context
- Provide relevant background information
- Consider the target audience
- Include domain-specific knowledge
- Set appropriate expectations

### Examples
- Use few-shot examples when appropriate
- Provide input-output pairs
- Include edge cases
- Show desired output format

## Common Pitfalls to Avoid

### Ambiguity
- ❌ "Write a good article"
- ✅ "Write a 500-word article about climate change with an introduction, three main sections, and a conclusion"

### Insufficient Context
- ❌ "Summarize this text"
- ✅ "Summarize this text for a non-technical audience, focusing on the main arguments and supporting evidence"

### Unclear Output Format
- ❌ "Provide information about X"
- ✅ "Provide information about X in JSON format with the following fields: name, description, and examples"

### Missing Constraints
- ❌ "Create a list"
- ✅ "Create a list of 5-10 items, prioritized by importance"

### Conflicting Instructions
- ❌ "Be brief but comprehensive"
- ✅ "Be concise while covering all key points"

## Prompt Versioning

Maintain version history for prompts:
- Use semantic versioning (v1.0.0, v1.1.0, etc.)
- Document changes between versions
- Track testing results
- Note known limitations

## Prompt Documentation

Document prompts with:
- Name and purpose
- Target AI model
- Creation date
- Version number
- Usage instructions
- Testing recommendations
- Known limitations

---

# 6. INTEGRATION WITH RESOURCES

## Memory Bank Integration

When working with prompts, leverage the Memory Bank:

- Read memory bank files at the start of each task
- Update memory bank with prompt patterns and best practices
- Document successful prompt strategies in the memory bank
- Reference memory bank for project-specific context

## MCP Server Integration

Use available MCP servers for enhanced capabilities:

- **filesystem-projects**: Access to project files for context
- **filesystem-agentic**: Access to agentic repositories for reference patterns
- Additional MCP servers as configured

## Workflow Integration

Use workflows for structured approaches:
- `/analyze-prompt`: Analyze an existing prompt
- `/create-prompt`: Create a new prompt
- `/optimize-prompt`: Optimize an existing prompt
- `/test-prompt`: Test a prompt with sample inputs

---

# 7. QUALITY CHECKLIST

Before finalizing any prompt, verify:

## Content Quality
- [ ] Purpose is clearly defined
- [ ] Target audience is considered
- [ ] Context is sufficient and relevant
- [ ] Instructions are specific and actionable
- [ ] Output format is clearly specified

## Structure Quality
- [ ] Logical flow and organization
- [ ] Clear section delineation
- [ ] Consistent formatting
- [ ] Appropriate structure for task

## Completeness
- [ ] All necessary information included
- [ ] No missing instructions
- [ ] Constraints specified
- [ ] Examples provided when helpful

## Effectiveness
- [ ] Will produce desired results
- [ ] Examples are relevant and helpful
- [ ] Evaluation criteria defined
- [ ] Tested with sample inputs

---

# 8. TROUBLESHOOTING

## Common Issues

### Prompt Not Working as Expected
- Check for ambiguous language
- Verify sufficient context
- Ensure output format is specified
- Test with different inputs

### Inconsistent Outputs
- Review instructions for clarity
- Add more examples
- Specify constraints more precisely
- Test for edge cases

### AI Misunderstanding Intent
- Clarify the purpose
- Add more context
- Use more specific language
- Provide examples of desired output

### Prompt Too Long
- Remove redundant information
- Consolidate similar instructions
- Use concise language
- Focus on essential elements

---

# 9. ADVANCED TECHNIQUES

## Chain-of-Thought Prompting
Guide the AI through explicit reasoning:
- "Think step by step"
- "Explain your reasoning"
- "Show your work"
- Use for complex problem-solving

## Few-Shot Learning
Provide examples for pattern recognition:
- Include 3-5 examples
- Show variety in examples
- Cover edge cases
- Use for pattern-based tasks

## Self-Consistency
Request multiple outputs and compare:
- "Provide 3 different approaches"
- "Compare and contrast these options"
- Use for exploring alternatives

## Iterative Refinement
Refine prompts through multiple iterations:
- Start with a basic prompt
- Test and evaluate results
- Identify issues
- Refine and retest

## Prompt Chaining
Break complex tasks into multiple prompts:
- Identify sub-tasks
- Create prompts for each sub-task
- Chain outputs as inputs
- Use for complex, multi-step tasks

---

# 10. RESOURCES

## Reference Materials

- [Kilo Code Documentation](https://kilocode.ai/docs/)
- [Prompt Engineering Guide](https://kilocode.ai/docs/guides/prompt-engineering/)
- [Memory Bank Documentation](https://kilocode.ai/docs/advanced-usage/memory-bank)
- [Agentic Prompts Repository](C:/Users/pavel/vscodeportable/agentic/prompts/)

## Related Skills

- Translation: For multilingual prompt considerations
- Test: For testing prompt effectiveness
- Architect: For planning prompt strategies

## Workflows

- analyze-prompt.md: Analyze an existing prompt
- create-prompt.md: Create a new prompt
- optimize-prompt.md: Optimize an existing prompt
- test-prompt.md: Test a prompt with sample inputs
