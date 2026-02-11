# Architecture Documentation

This document describes the architecture of the Kilo Code Comprehensive Template.

## Overview

The Kilo Code Comprehensive Template is designed to provide a solid foundation for new projects using Kilo Code AI assistant. It integrates prompt engineering capabilities, memory bank system, and comprehensive documentation into a cohesive structure.

## Design Principles

The template follows these design principles:

1. **Modularity**: Each component (modes, skills, workflows, rules) is independent and can be customized
2. **Extensibility**: New modes, skills, and workflows can be added without modifying existing code
3. **Integration**: Seamless integration with Kilo Code's core features and agentic repositories
4. **Documentation-First**: Comprehensive documentation for setup, usage, and architecture
5. **Best Practices**: Follows Kilo Code conventions and prompt engineering best practices

## Directory Structure

```
templates/
├── .kilocode/                    # Kilo Code configuration
│   ├── mcp.json                  # MCP server configuration
│   ├── modes/                     # Custom modes
│   │   └── README.md            # Modes documentation
│   ├── skills/                    # Project-specific skills
│   │   └── README.md            # Skills documentation
│   ├── workflows/                 # Workflow definitions
│   │   ├── README.md            # Workflows documentation
│   │   ├── analyze-prompt.md    # Analyze prompt workflow
│   │   ├── create-prompt.md     # Create prompt workflow
│   │   ├── optimize-prompt.md   # Optimize prompt workflow
│   │   └── test-prompt.md      # Test prompt workflow
│   ├── rules/                     # General rules
│   │   └── memory-bank-instructions.md
│   ├── rules-architect/           # Architect mode rules
│   │   └── plan.md             # Planning workflow
│   ├── rules-code/                # Code mode rules
│   │   └── implement.md         # Implementation guidelines
│   ├── rules-debug/               # Debug mode rules
│   │   └── debug.md            # Debugging protocol
│   └── rules/memory-bank/         # Memory bank files
│       └── brief.md            # Project brief
├── .agent/                       # Agent configuration (optional)
├── README.md                     # Main documentation
├── SETUP.md                      # Setup instructions
├── USAGE.md                      # Usage guide
├── ARCHITECTURE.md              # This file
├── .env.template                 # Environment variables template
└── .gitignore                   # Git ignore patterns
```

## Components

### MCP Configuration (`.kilocode/mcp.json`)

The MCP (Model Context Protocol) configuration defines which MCP servers are available to Kilo Code.

**Default Servers**:
- `filesystem-projects`: Access to projects directory
- `filesystem-agentic`: Access to agentic repositories

**Extending MCP Servers**:
Add new servers by following the MCP server documentation at https://kilocode.ai/docs/advanced-usage/mcp-servers/

### Custom Modes (`.kilocode/modes/`)

Custom modes provide specialized behavior for different types of tasks.

**Prompt Consultant Mode**:
- Specialized for prompt engineering tasks
- Analyzes, creates, optimizes, and tests prompts
- Integrates with prompt consultant skill and workflows

**Adding New Modes**:
1. Create mode configuration in global `custom_modes.yaml`
2. Define role, tool groups, and custom instructions
3. Create corresponding skill file if needed
4. Create workflow files for common tasks

### Skills (`.kilocode/skills/`)

Skills provide detailed guidelines for specific domains or tasks.

**Prompt Consultant Skill**:
- Comprehensive prompt engineering guidelines
- Analysis frameworks
- Creation best practices
- Testing methodologies
- Optimization strategies

**Skill Structure**:
```markdown
---
name: skill-name
description: Brief description of the skill
---

# Skill Name

Detailed guidelines and instructions for the skill.
```

### Workflows (`.kilocode/workflows/`)

Workflows provide structured approaches to common tasks.

**Available Workflows**:
- `analyze-prompt.md`: Analyze an existing prompt
- `create-prompt.md`: Create a new prompt
- `optimize-prompt.md`: Optimize an existing prompt
- `test-prompt.md`: Test a prompt with sample inputs

**Workflow Structure**:
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

### Rules (`.kilocode/rules*/`)

Rules provide behavior control for different modes and tasks.

**Rule Categories**:

| Category | Location | Purpose |
|-----------|-----------|---------|
| Memory Bank | `.kilocode/rules/memory-bank-instructions.md` | Memory bank system instructions |
| Architect | `.kilocode/rules-architect/plan.md` | Planning and architecture guidelines |
| Code | `.kilocode/rules-code/implement.md` | Implementation best practices |
| Debug | `.kilocode/rules-debug/debug.md` | Systematic debugging protocols |

**Rule Structure**:
```markdown
---
description: Rule description
globs: [file patterns]
alwaysApply: true/false
---
---
description: Additional description
globs: [file patterns]
alwaysApply: true/false
---
Rule content and instructions.
```

### Memory Bank (`.kilocode/rules/memory-bank/`)

The Memory Bank system maintains project context across sessions.

**Core Files**:
- `brief.md`: Project overview and goals (maintained by developer)
- `product.md`: Product description and user experience
- `context.md`: Current work focus and recent changes
- `architecture.md`: System architecture and technical decisions
- `tech.md`: Technologies and development setup

**Additional Files**:
- `tasks.md`: Documented repetitive tasks and workflows

**Memory Bank Workflow**:
1. **Initialization**: Analyze project and create initial files
2. **Regular Updates**: Update after significant changes
3. **Task Documentation**: Store repetitive tasks for future reference
4. **Context Loading**: Automatically load at start of each task

## Integration with Agentic Repositories

The template integrates with repositories from `C:/Users/pavel/vscodeportable/agentic/`:

### kilocode-rules

Provides opinionated configuration for Kilo Code, including:
- Structured prompts for behavior control
- Memory bank system
- Mode-specific rules (Architect, Code, Debug)
- Best practices for different development phases

### prompts

Provides Cline community prompts for reference and adaptation:
- `.clinerules/`: Custom rules for Cline
- `workflows/`: Workflow definitions
- Reference patterns for prompt engineering

## Data Flow

### Memory Bank Flow

```
User Request
    ↓
Kilo Code loads Memory Bank
    ↓
[Memory Bank: Active] in response
    ↓
Task execution with context
    ↓
Update Memory Bank (if significant changes)
```

### Prompt Consultant Flow

```
User Request (Prompt Engineering)
    ↓
Switch to Prompt Consultant Mode
    ↓
Load Prompt Consultant Skill
    ↓
Execute Workflow (if applicable)
    ↓
Analyze/Create/Optimize/Test Prompt
    ↓
Provide Results and Recommendations
```

### Workflow Flow

```
User invokes workflow command
    ↓
Load workflow definition
    ↓
Execute step-by-step instructions
    ↓
Collect user input at each step
    ↓
Generate final output
    ↓
Present results to user
```

## Extension Points

The template provides several extension points for customization:

### Adding New Modes

1. Create mode configuration in `custom_modes.yaml`
2. Define role, tool groups, and custom instructions
3. Create corresponding skill file in `.kilocode/skills/`
4. Create workflow files in `.kilocode/workflows/`

### Adding New Skills

1. Create skill directory in `.kilocode/skills/`
2. Create `SKILL.md` with skill guidelines
3. Reference skill in mode configuration if applicable

### Adding New Workflows

1. Create workflow file in `.kilocode/workflows/`
2. Follow workflow structure with task definition
3. Include detailed sequence steps
4. Test workflow thoroughly

### Adding New Rules

1. Create rule file in appropriate `rules-*/` directory
2. Define rule metadata (description, globs, alwaysApply)
3. Include rule content and instructions
4. Test rule application

## Security Considerations

- **Environment Variables**: Sensitive data should be stored in `.env` (not committed)
- **Git Ignore**: `.gitignore` excludes sensitive files from version control
- **MCP Servers**: Only connect to trusted MCP servers
- **Memory Bank**: Review memory bank files before committing to avoid exposing sensitive information

## Performance Considerations

- **Memory Bank Loading**: Memory bank files are loaded at the start of each task
- **Rule Application**: Rules are applied based on mode and file patterns
- **Workflow Execution**: Workflows guide step-by-step execution without performance overhead
- **MCP Server Communication**: MCP servers provide additional capabilities with minimal latency

## Future Enhancements

Potential future enhancements to the template:

1. **Additional Modes**: More specialized modes for different domains
2. **Enhanced Workflows**: More workflows for common tasks
3. **Integration Testing**: Automated testing of template components
4. **Documentation Generation**: Automatic documentation from code
5. **Prompt Library**: Collection of reusable prompt templates

## References

- [Kilo Code Documentation](https://kilocode.ai/docs/)
- [Memory Bank Documentation](https://kilocode.ai/docs/advanced-usage/memory-bank)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Prompt Engineering Guide](https://kilocode.ai/docs/guides/prompt-engineering/)
