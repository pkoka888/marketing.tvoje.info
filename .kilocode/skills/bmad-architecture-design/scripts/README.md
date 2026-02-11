# Architecture Design Scripts

This directory contains helper scripts for the architecture design skill.

## Scripts

### generate_architecture.py

Generates a comprehensive architecture document from structured JSON data.

**Usage:**

```bash
# Interactive mode
python scripts/generate_architecture.py --interactive

# From JSON file
python scripts/generate_architecture.py architecture-data.json

# Custom output path
python scripts/generate_architecture.py architecture-data.json --output my-docs/ARCHITECTURE.md
```

**Input JSON Structure:**

```json
{
  "project_name": "My Project",
  "date": "2024-01-15",
  "author": "AI Agent",
  "executive_summary": "Brief project description",
  "quality_attributes": [
    {"attribute": "Performance", "target": "<2s LCP", "measurement": "Lighthouse"}
  ],
  "constraints": ["Budget < $10k", "GDPR compliance"],
  "integration_points": ["Payment gateway", "Email service"],
  "components": [
    {
      "name": "Frontend",
      "responsibility": "User interface",
      "interfaces": ["REST API"],
      "technology": "React, TypeScript"
    }
  ],
  "decisions": [
    {
      "id": "DECISION-001",
      "title": "Choose React for frontend",
      "decision": "Use React with TypeScript",
      "rationale": "Team expertise, ecosystem",
      "alternatives": [
        {"name": "Vue", "pros_cons": "Simpler but smaller ecosystem"}
      ],
      "trade_offs": "Learning curve for new team members",
      "risks": "Dependency on Meta",
      "mitigation": "Use well-established patterns"
    }
  ],
  "technology_stack": {
    "frontend": {"framework": "React", "reason": "Team expertise"},
    "backend": {"framework": "Node.js", "reason": "Unified language"},
    "data_layer": {"database": "PostgreSQL", "reason": "ACID compliance"},
    "infrastructure": {"hosting": "Vercel", "reason": "Native Next.js support"}
  }
}
```

**Interactive Mode Prompts:**

1. Project Name
2. Author
3. Executive Summary
4. Quality Attributes (multiple)
5. Constraints (multiple)
6. Integration Points (multiple)

## Requirements

- Python 3.7+
- No external dependencies

## Examples

See `assets/architecture-script-template.md.template` for the template used by this script.
