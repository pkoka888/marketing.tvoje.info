# Usage Guide

This guide explains how to use the Kilo Code Comprehensive Template effectively.

## Table of Contents

- [Memory Bank](#memory-bank)
- [Prompt Consultant Mode](#prompt-consultant-mode)
- [Workflows](#workflows)
- [Rules](#rules)
- [Best Practices](#best-practices)

## Memory Bank

The Memory Bank system maintains project context across Kilo Code sessions, ensuring continuity and understanding of your project.

### How It Works

When you start a task, Kilo Code automatically reads all memory bank files from `.kilocode/rules/memory-bank/` and includes `[Memory Bank: Active]` at the beginning of responses. If the memory bank is missing or empty, you'll see `[Memory Bank: Missing]` with a warning.

### Memory Bank Files

| File | Purpose | Maintained By |
|-------|---------|----------------|
| `brief.md` | Project overview, goals, and scope | Developer (manual) |
| `product.md` | Product description and user experience | Kilo Code (suggested) |
| `context.md` | Current work focus and recent changes | Kilo Code (automatic) |
| `architecture.md` | System architecture and technical decisions | Kilo Code (suggested) |
| `tech.md` | Technologies and development setup | Kilo Code (suggested) |
| `tasks.md` | Documented repetitive tasks | Kilo Code (on request) |

### Initialization

To initialize the Memory Bank for a new project:

1. Switch to **Architect** mode
2. Run the command: `initialize memory bank`
3. Kilo Code will analyze your project and create initial memory bank files
4. Review the generated files and make corrections as needed
5. Update `brief.md` with your specific project details

### Updating the Memory Bank

The Memory Bank is updated automatically in these situations:

- After implementing significant changes
- When you explicitly request: `update memory bank`
- When context needs clarification

To manually update the Memory Bank:

1. Switch to **Architect** mode
2. Run the command: `update memory bank`
3. Kilo Code will review all project files and update the memory bank

### Adding Tasks

When you complete a repetitive task and want to document it:

1. Run the command: `add task` or `store this as a task`
2. Kilo Code will document the task in `tasks.md` with:
   - Task name and description
   - Files that need to be modified
   - Step-by-step workflow
   - Important considerations
   - Example implementation

### Best Practices

- **Keep `brief.md` accurate**: This is the foundation for all other memory bank files
- **Review updates**: Always review memory bank updates for accuracy
- **Be specific**: Include concrete details in memory bank files
- **Update regularly**: Keep the memory bank current with project changes
- **Use for context**: Reference memory bank files when working on complex tasks

## Prompt Consultant Mode

The Prompt Consultant mode provides specialized capabilities for prompt engineering tasks.

### When to Use

Use the Prompt Consultant mode when you need to:

- Analyze an existing prompt for effectiveness
- Create a new prompt for a specific use case
- Optimize an existing prompt for better results
- Test a prompt with sample inputs
- Document prompt versions and changes

### Switching to Prompt Consultant Mode

1. Click the mode selector in the Kilo Code panel
2. Select "Prompt Consultant" from the dropdown
3. Kilo Code will now use prompt engineering specialized instructions

### Prompt Consultant Capabilities

The Prompt Consultant mode can:

- **Analyze Prompts**: Evaluate clarity, specificity, and effectiveness
- **Create Prompts**: Generate new prompts following best practices
- **Optimize Prompts**: Improve existing prompts for better results
- **Test Prompts**: Validate prompts with sample inputs
- **Version Prompts**: Track changes and maintain prompt history

### Working with Prompts

When working with prompts in Prompt Consultant mode:

1. **Provide Context**: Explain the purpose and target audience of the prompt
2. **Specify Requirements**: Detail what the prompt should accomplish
3. **Consider Constraints**: Mention any limitations or requirements
4. **Review Suggestions**: Evaluate the consultant's recommendations
5. **Iterate**: Refine the prompt based on feedback

### Prompt Best Practices

The Prompt Consultant follows these best practices:

- **Be Specific**: Use clear, specific language
- **Provide Context**: Include relevant background information
- **Structure Clearly**: Use sections and formatting for organization
- **Define Output**: Specify the expected output format
- **Include Examples**: Provide examples when helpful
- **Test Thoroughly**: Validate prompts with sample inputs
- **Document Changes**: Track prompt versions and modifications

## Workflows

Workflows provide structured approaches to common tasks. They can be invoked using slash commands.

### Available Workflows

| Workflow | Command | Purpose |
|----------|----------|---------|
| Analyze Prompt | `/analyze-prompt` | Analyze an existing prompt for effectiveness |
| Create Prompt | `/create-prompt` | Create a new prompt following best practices |
| Optimize Prompt | `/optimize-prompt` | Optimize an existing prompt for better results |
| Test Prompt | `/test-prompt` | Test a prompt with sample inputs |

### Using Workflows

1. Type the workflow command in the Kilo Code chat
2. Follow the guided steps provided by the workflow
3. Provide the requested information at each step
4. Review the results and make adjustments as needed

### Creating Custom Workflows

To create a custom workflow:

1. Create a new markdown file in `.kilocode/workflows/`
2. Use kebab-case naming (e.g., `my-custom-workflow.md`)
3. Follow the workflow structure:
   ```markdown
   <task name="Workflow Name">
   
   <task_objective>
   Brief description of what the workflow accomplishes.
   </task_objective>
   
   <detailed_sequence_steps>
   ## Step 1: Description
   Detailed instructions for the step.
   
   ## Step 2: Description
   Detailed instructions for the step.
   
   ...
   </detailed_sequence_steps>
   
   </task>
   ```

## Rules

Rules provide behavior control for different modes and tasks.

### Rule Categories

| Category | Location | Purpose |
|-----------|-----------|---------|
| Memory Bank | `.kilocode/rules/memory-bank-instructions.md` | Memory bank system instructions |
| Architect | `.kilocode/rules-architect/` | Planning and architecture guidelines |
| Code | `.kilocode/rules-code/` | Implementation best practices |
| Debug | `.kilocode/rules-debug/` | Systematic debugging protocols |

### How Rules Work

Rules are automatically applied based on:

- **Mode**: Different rules apply to different modes (Architect, Code, Debug)
- **File Patterns**: Rules can be applied to specific file types
- **Always Apply**: Some rules apply to all tasks

### Customizing Rules

To customize rules for your project:

1. Edit the rule files in `.kilocode/rules*/` directories
2. Follow the existing structure and format
3. Test changes to ensure they work as expected
4. Document any customizations in the memory bank

## Best Practices

### Project Setup

1. **Initialize Memory Bank Early**: Set up the memory bank as soon as you start a project
2. **Customize Configuration**: Update `.env` and configuration files for your needs
3. **Review Rules**: Understand the rules that will be applied to your work
4. **Set Up Git**: Initialize version control from the start

### Daily Workflow

1. **Start with Memory Bank**: Begin each session by reviewing the memory bank
2. **Use Appropriate Mode**: Switch to the mode that matches your current task
3. **Leverage Workflows**: Use workflows for structured approaches to common tasks
4. **Update Context**: Keep the memory bank current with your progress

### Prompt Engineering

1. **Analyze First**: Always analyze existing prompts before creating new ones
2. **Iterate**: Refine prompts through multiple iterations
3. **Test Thoroughly**: Validate prompts with diverse inputs
4. **Document Changes**: Track prompt versions and modifications
5. **Share Knowledge**: Document successful prompt patterns in the memory bank

### Collaboration

1. **Keep Memory Bank Updated**: Ensure team members have current context
2. **Document Decisions**: Record important decisions in the memory bank
3. **Use Clear Prompts**: Create prompts that are easy for others to understand
4. **Share Workflows**: Contribute useful workflows to the team

## Troubleshooting

### Memory Bank Issues

**Problem**: `[Memory Bank: Missing]` appears

**Solution**:
- Run `initialize memory bank` in Architect mode
- Check that `.kilocode/rules/memory-bank/` directory exists
- Verify memory bank files are not empty

**Problem**: Memory bank information is outdated

**Solution**:
- Run `update memory bank` in Architect mode
- Manually update `context.md` with recent changes
- Review and correct other memory bank files as needed

### Prompt Consultant Issues

**Problem**: Prompt Consultant mode is not available

**Solution**:
- Verify the mode is added to `custom_modes.yaml`
- Restart VS Code or reload the Kilo Code extension
- Check for syntax errors in the YAML file

**Problem**: Prompt suggestions are not helpful

**Solution**:
- Provide more context and requirements
- Specify the target AI model and its capabilities
- Give examples of desired outputs
- Iterate on the prompt based on feedback

### Workflow Issues

**Problem**: Workflow command is not recognized

**Solution**:
- Verify the workflow file exists in `.kilocode/workflows/`
- Check the file name matches the command (kebab-case)
- Restart VS Code or reload the Kilo Code extension

## Additional Resources

- [Kilo Code Documentation](https://kilocode.ai/docs/)
- [Memory Bank Documentation](https://kilocode.ai/docs/advanced-usage/memory-bank)
- [Custom Modes Documentation](https://kilocode.ai/docs/advanced-usage/custom-modes/)
- [Prompt Engineering Guide](https://kilocode.ai/docs/guides/prompt-engineering/)
