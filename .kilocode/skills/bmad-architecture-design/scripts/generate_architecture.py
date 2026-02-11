#!/usr/bin/env python3
"""
Architecture Document Generator

This script generates a comprehensive architecture document from structured data.
It reads a JSON configuration file and produces a markdown architecture document
based on the template in assets/architecture-script-template.md.template

Usage:
    python generate_architecture.py <input.json>
    python generate_architecture.py --interactive

Input JSON Structure:
{
    "project_name": "Project Name",
    "date": "YYYY-MM-DD",
    "author": "Author Name",
    "executive_summary": "Brief summary",
    "quality_attributes": [
        {"attribute": "Performance", "target": "Target", "measurement": "How measured"}
    ],
    "constraints": ["List of constraints"],
    "integration_points": ["List of integrations"],
    "components": [
        {
            "name": "Component Name",
            "responsibility": "What it does",
            "interfaces": ["List of interfaces"],
            "technology": "Technologies used"
        }
    ],
    "decisions": [
        {
            "id": "DECISION-001",
            "title": "Decision Title",
            "decision": "What was decided",
            "rationale": "Why this decision",
            "alternatives": [
                {"name": "Alternative 1", "pros_cons": "Pros/cons"}
            ],
            "trade_offs": "What was sacrificed",
            "risks": "Potential issues",
            "mitigation": "How risks are addressed"
        }
    ],
    "technology_stack": {
        "frontend": {"framework": "", "reason": ""},
        "backend": {"framework": "", "reason": ""},
        "data_layer": {"database": "", "reason": ""},
        "infrastructure": {"hosting": "", "reason": ""}
    }
}

Output:
    ARCHITECTURE.md - The generated architecture document
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime

TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "architecture-script-template.md.template"
OUTPUT_PATH = Path("ARCHITECTURE.md")


def read_template():
    """Read the markdown template file."""
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text()


def generate_quality_attributes_table(attributes):
    """Generate markdown table for quality attributes."""
    if not attributes:
        return "| Attribute | Target | Measurement |\n|-----------|--------|-------------|\n"
    
    lines = ["| Attribute | Target | Measurement |", "|-----------|--------|-------------|"]
    for attr in attributes:
        lines.append(f"| {attr.get('attribute', '')} | {attr.get('target', '')} | {attr.get('measurement', '')} |")
    return "\n".(lines) + "\n"


def generate_constraints_list(constraints):
    """Generate markdown list for constraints."""
    if not constraints:
        return "- [List of constraints]"
    return "\n".join(f"- {c}" for c in constraints)


def generate_integrations_list(integration_points):
    """Generate markdown list for integration points."""
    if not integration_points:
        return "- [List of external systems and dependencies]"
    return "\n".join(f"- {i}" for i in integration_points)


def generate_components_section(components):
    """Generate markdown section for component details."""
    if not components:
        return """### 6.1 [Component Name]
- **Responsibility**: [What this component does]
- **Interfaces**: [How it communicates]
- **Technology**: [What technologies used]"""
    
    sections = []
    for i, comp in enumerate(components, 1):
        sections.append(f"""### 6.{i} {comp.get('name', 'Component Name')}
- **Responsibility**: {comp.get('responsibility', '[What this component does]')}
- **Interfaces**: {', '.join(comp.get('interfaces', ['[How it communicates]']))}
- **Technology**: {comp.get('technology', '[What technologies used]')}""")
    return "\n\n".join(sections)


def generate_decisions_section(decisions):
    """Generate markdown section for architectural decisions."""
    if not decisions:
        return """### DECISION-001: [Decision Title]
- **Status**: Approved
- **Decision**: [What was decided]
- **Rationale**: [Why this decision]
- **Alternatives Considered**:
  - [Alternative 1]: [Pros/Cons]
  - [Alternative 2]: [Pros/Cons]
- **Trade-offs**: [What was sacrificed]
- **Risks**: [Potential issues]
- **Mitigation**: [How risks are addressed]"""
    
    sections = []
    for decision in decisions:
        alt_lines = []
        for alt in decision.get('alternatives', []):
            alt_lines.append(f"  - {alt.get('name', 'Alternative')}: {alt.get('pros_cons', 'Pros/cons')}")
        
        sections.append(f"""### {decision.get('id', 'DECISION-001')}: {decision.get('title', 'Decision Title')}
- **Status**: Approved
- **Decision**: {decision.get('decision', '[What was decided]')}
- **Rationale**: {decision.get('rationale', '[Why this decision]')}
- **Alternatives Considered**:
{chr(10).join(alt_lines) if alt_lines else '  - [Alternative 1]: [Pros/Cons]'}
- **Trade-offs**: {decision.get('trade_offs', '[What was sacrificed]')}
- **Risks**: {decision.get('risks', '[Potential issues]')}
- **Mitigation**: {decision.get('mitigation', '[How risks are addressed]')}""")
    
    return "\n\n".join(sections)


def generate_tech_stack_section(tech_stack):
    """Generate markdown section for technology stack."""
    if not tech_stack:
        return """### 4.1 Frontend
- **Framework**: [Technology]
- **Reason**: [Rationale linked to drivers]

### 4.2 Backend
- **Framework**: [Technology]
- **Reason**: [Rationale linked to drivers]

### 4.3 Data Layer
- **Database**: [Technology]
- **Reason**: [Rationale linked to drivers]

### 4.4 Infrastructure
- **Hosting**: [Technology]
- **Reason**: [Rationale linked to drivers]"""
    
    frontend = tech_stack.get('frontend', {})
    backend = tech_stack.get('backend', {})
    data = tech_stack.get('data_layer', {})
    infra = tech_stack.get('infrastructure', {})
    
    return f"""### 4.1 Frontend
- **Framework**: {frontend.get('framework', '[Technology]')}
- **Reason**: {frontend.get('reason', '[Rationale linked to drivers]')}

### 4.2 Backend
- **Framework**: {backend.get('framework', '[Technology]')}
- **Reason**: {backend.get('reason', '[Rationale linked to drivers]')}

### 4.3 Data Layer
- **Database**: {data.get('database', '[Technology]')}
- **Reason**: {data.get('reason', '[Rationale linked to drivers]')}

### 4.4 Infrastructure
- **Hosting**: {infra.get('hosting', '[Technology]')}
- **Reason**: {infra.get('reason', '[Rationale linked to drivers]')}"""


def fill_template(template, data):
    """Fill the markdown template with data from JSON."""
    replacements = {
        "[Project Name]": data.get('project_name', '[Project Name]'),
        "[YYYY-MM-DD]": data.get('date', datetime.now().strftime('%Y-%m-%d')),
        "[Agent Name]": data.get('author', '[Agent Name]'),
        "[Brief 2-3 sentence description]": data.get('executive_summary', '[Brief 2-3 sentence description]'),
        "[List technical, business, and regulatory constraints]": generate_constraints_list(data.get('constraints', [])),
        "[List external systems and dependencies]": generate_integrations_list(data.get('integration_points', [])),
        "[Insert or describe system context]": data.get('system_context', '[Insert or describe system context]'),
        "[Insert or describe component topology]": data.get('component_topology', '[Insert or describe component topology]'),
        "[Describe key data flows through the system]": data.get('data_flow', '[Describe key data flows through the system]'),
        "[Insert or describe auth strategy]": data.get('auth_strategy', '[Describe auth strategy]'),
        "[Describe encryption, PII handling]": data.get('data_protection', '[Describe encryption, PII handling]'),
        "[Describe firewall, SSL/TLS]": data.get('network_security', '[Describe firewall, SSL/TLS]'),
        "[Setup]": data.get('environment_strategy', '[Setup]'),
        "[Describe deployment pipeline]": data.get('cicd_pipeline', '[Describe deployment pipeline]'),
        "[List standards]": data.get('coding_standards', '[List standards]'),
        "[Coverage target]": data.get('testing_requirements', '[Coverage target]'),
        "[Describe observability requirements]": data.get('monitoring', '[Describe observability requirements]'),
        "[Link to PRD]": data.get('prd_link', '[Link to PRD]'),
        "[Link to UX requirements]": data.get('ux_link', '[Link to UX requirements]'),
        "[Link to compliance docs]": data.get('compliance_link', '[Link to compliance docs]'),
    }
    
    # Quality attributes table
    replacements["| Attribute | Target | Measurement |\n|-----------|--------|-------------|\n"] = generate_quality_attributes_table(data.get('quality_attributes', []))
    
    # Technology stack section
    replacements["### 4.1 Frontend\n- **Framework**: [Technology]\n- **Reason**: [Rationale linked to drivers]\n\n### 4.2 Backend\n- **Framework**: [Technology]\n- **Reason**: [Rationale linked to drivers]\n\n### 4.3 Data Layer\n- **Database**: [Technology]\n- **Reason**: [Rationale linked to drivers]\n\n### 4.4 Infrastructure\n- **Hosting**: [Technology]\n- **Reason**: [Rationale linked to drivers]"] = generate_tech_stack_section(data.get('technology_stack', {}))
    
    # Components section
    replacements["### 6.1 [Component Name]\n- **Responsibility**: [What this component does]\n- **Interfaces**: [How it communicates]\n- **Technology**: [What technologies used]"] = generate_components_section(data.get('components', []))
    
    # Decisions section
    replacements["### DECISION-001: [Decision Title]\n- **Status**: Approved\n- **Decision**: [What was decided]\n- **Rationale**: [Why this decision]\n- **Alternatives Considered**:\n  - [Alternative 1]: [Pros/Cons]\n  - [Alternative 2]: [Pros/Cons]\n- **Trade-offs**: [What was sacrificed]\n- **Risks**: [Potential issues]\n- **Mitigation**: [How risks are addressed]"] = generate_decisions_section(data.get('decisions', []))
    
    # Apply replacements
    result = template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)
    
    return result


def interactive_mode():
    """Run in interactive mode to collect architecture data."""
    print("Architecture Document Generator - Interactive Mode")
    print("=" * 50)
    
    data = {}
    
    data['project_name'] = input("Project Name: ").strip() or "[Project Name]"
    data['date'] = datetime.now().strftime('%Y-%m-%d')
    data['author'] = input("Author: ").strip() or "[Agent Name]"
    data['executive_summary'] = input("Executive Summary: ").strip() or "[Brief summary]"
    
    print("\nQuality Attributes (press Enter to skip):")
    attributes = []
    while True:
        attr = input("  Attribute (or Enter to finish): ").strip()
        if not attr:
            break
        target = input("  Target: ").strip()
        measurement = input("  Measurement: ").strip()
        attributes.append({"attribute": attr, "target": target, "measurement": measurement})
    data['quality_attributes'] = attributes
    
    print("\nConstraints (press Enter after each, empty line to finish):")
    constraints = []
    while True:
        constraint = input("  Constraint: ").strip()
        if not constraint:
            break
        constraints.append(constraint)
    data['constraints'] = constraints
    
    print("\nIntegration Points (press Enter after each, empty line to finish):")
    integrations = []
    while True:
        integration = input("  Integration: ").strip()
        if not integration:
            break
        integrations.append(integration)
    data['integration_points'] = integrations
    
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Generate architecture document from structured data"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Input JSON file with architecture data"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: ARCHITECTURE.md)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.interactive:
            data = interactive_mode()
        elif args.input_file:
            input_path = Path(args.input_file)
            if not input_path.exists():
                print(f"Error: Input file not found: {input_path}")
                sys.exit(1)
            data = json.loads(input_path.read_text())
        else:
            parser.print_help()
            print("\nError: Either provide an input file or use --interactive")
            sys.exit(1)
        
        template = read_template()
        document = fill_template(template, data)
        
        output_path = Path(args.output) if args.output else OUTPUT_PATH
        output_path.write_text(document)
        print(f"Architecture document generated: {output_path}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
