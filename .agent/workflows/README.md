# Workflows

This directory contains workflow definitions for common tasks in Kilo Code.

## Available Workflows

- `analyze-prompt.md` - Analyze an existing prompt for effectiveness and suggest improvements
- `create-prompt.md` - Create a new prompt following best practices
- `optimize-prompt.md` - Optimize an existing prompt for better performance
- `test-prompt.md` - Test a prompt with sample inputs and validate results

## Using Workflows

Workflows can be invoked using slash commands in Kilo Code. For example:
- `/analyze-prompt` - Start the prompt analysis workflow
- `/create-prompt` - Start the prompt creation workflow
- `/optimize-prompt` - Start the prompt optimization workflow
- `/test-prompt` - Start the prompt testing workflow

## Creating New Workflows

To create a new workflow:

1. Create a new markdown file in this directory
2. Use kebab-case naming (e.g., `my-new-workflow.md`)
3. Follow the workflow structure with task definition, objective, and detailed steps
4. Reference existing workflows for examples

## Workflow Structure

Each workflow file should contain:
- Task name and objective
- Detailed sequence of steps
- Tool references and formatting conventions
- Clear instructions for each step
