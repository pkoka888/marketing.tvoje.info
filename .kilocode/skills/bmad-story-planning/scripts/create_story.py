#!/usr/bin/env python3
"""
Story Creation Script

This script automates the creation of user story markdown files
from JSON input. It validates required fields and generates
story markdown from the template.
"""

import json
import os
import sys
from pathlib import Path


def validate_story_data(story_data):
    """Validate that all required fields are present in story data."""
    required_fields = [
        'title',
        'story',
        'acceptance_criteria',
        'dependencies',
        'prerequisites',
        'test_hooks',
        'delivery_signals',
        'epic',
        'architecture_refs'
    ]
    
    missing_fields = [field for field in required_fields if field not in story_data]
    
    if missing_fields:
        print(f"Error: Missing required fields: {', '.join(missing_fields)}")
        return False
    
    # Validate that acceptance_criteria is a list
    if not isinstance(story_data.get('acceptance_criteria'), list):
        print("Error: 'acceptance_criteria' must be a list")
        return False
    
    # Validate that test_hooks is a dict with unit, integration, e2e keys
    test_hooks = story_data.get('test_hooks', {})
    if not isinstance(test_hooks, dict):
        print("Error: 'test_hooks' must be a dictionary")
        return False
    
    required_test_types = ['unit', 'integration', 'e2e']
    for test_type in required_test_types:
        if test_type not in test_hooks:
            print(f"Warning: '{test_type}' tests not specified in test_hooks")
    
    # Validate that dependencies is a list
    if not isinstance(story_data.get('dependencies'), list):
        print("Error: 'dependencies' must be a list")
        return False
    
    # Validate that prerequisites is a list
    if not isinstance(story_data.get('prerequisites'), list):
        print("Error: 'prerequisites' must be a list")
        return False
    
    # Validate that delivery_signals is a list
    if not isinstance(story_data.get('delivery_signals'), list):
        print("Error: 'delivery_signals' must be a list")
        return False
    
    # Validate that architecture_refs is a list
    if not isinstance(story_data.get('architecture_refs'), list):
        print("Error: 'architecture_refs' must be a list")
        return False
    
    return True


def generate_story_markdown(story_data, template_path):
    """Generate story markdown from template and story data."""
    
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace placeholders with actual data
    markdown = template.replace('{{ story_id }}', story_data.get('story_id', ''))
    markdown = markdown.replace('{{ title }}', story_data.get('title', ''))
    markdown = markdown.replace('{{ epic }}', story_data.get('epic', ''))
    markdown = markdown.replace('{{ priority }}', story_data.get('priority', ''))
    markdown = markdown.replace('{{ effort }}', story_data.get('effort', ''))
    markdown = markdown.replace('{{ user_type }}', story_data.get('user_type', 'user'))
    markdown = markdown.replace('{{ goal }}', story_data.get('goal', ''))
    markdown = markdown.replace('{{ benefit }}', story_data.get('benefit', ''))
    markdown = markdown.replace('{{ notes }}', story_data.get('notes', ''))
    markdown = markdown.replace('{{ implementation_notes }}', story_data.get('implementation_notes', ''))
    
    # Replace acceptance criteria
    acceptance_criteria = story_data.get('acceptance_criteria', [])
    criteria_section = ""
    for criterion in acceptance_criteria:
        criteria_section += f"- [ ] {criterion}\n"
    markdown = markdown.replace('{% for criterion in acceptance_criteria %}\n- [ ] {{ criterion }}\n{% endfor %}', criteria_section)
    
    # Replace dependencies
    dependencies = story_data.get('dependencies', [])
    deps_section = ""
    for dep in dependencies:
        if isinstance(dep, dict):
            dep_name = dep.get('name', dep)
            dep_type = dep.get('type', 'hard')
            deps_section += f"- **{dep_name}** ({dep_type})\n"
        else:
            deps_section += f"- **{dep}** (hard)\n"
    markdown = markdown.replace('{% for dependency in dependencies %}\n- **{{ dependency }}** ({{ dependency_type }})\n{% endfor %}', deps_section)
    
    # Replace prerequisites
    prerequisites = story_data.get('prerequisites', [])
    prereq_section = ""
    for prereq in prerequisites:
        prereq_section += f"- **{prereq}**\n"
    markdown = markdown.replace('{% for prerequisite in prerequisites %}\n- **{{ prerequisite }}**\n{% endfor %}', prereq_section)
    
    # Replace test hooks
    test_hooks = story_data.get('test_hooks', {})
    
    # Unit tests
    unit_tests = test_hooks.get('unit', [])
    unit_section = ""
    for test in unit_tests:
        unit_section += f"- `{test}`\n"
    markdown = markdown.replace('{% for test in unit_tests %}\n- `{{ test }}`\n{% endfor %}', unit_section)
    
    # Integration tests
    integration_tests = test_hooks.get('integration', [])
    integration_section = ""
    for test in integration_tests:
        integration_section += f"- `{test}`\n"
    markdown = markdown.replace('{% for test in integration_tests %}\n- `{{ test }}`\n{% endfor %}', integration_section)
    
    # E2E tests
    e2e_tests = test_hooks.get('e2e', [])
    e2e_section = ""
    for test in e2e_tests:
        e2e_section += f"- `{test}`\n"
    markdown = markdown.replace('{% for test in e2e_tests %}\n- `{{ test }}`\n{% endfor %}', e2e_section)
    
    # Replace delivery signals
    delivery_signals = story_data.get('delivery_signals', [])
    signals_section = ""
    for signal in delivery_signals:
        signals_section += f"- [ ] {signal}\n"
    markdown = markdown.replace('{% for signal in delivery_signals %}\n- [ ] {{ signal }}\n{% endfor %}', signals_section)
    
    # Replace architecture references
    architecture_refs = story_data.get('architecture_refs', [])
    refs_section = ""
    for ref in architecture_refs:
        refs_section += f"- **{ref}**\n"
    markdown = markdown.replace('{% for ref in architecture_refs %}\n- **{{ ref }}**\n{% endfor %}', refs_section)
    
    return markdown


def create_story_file(story_data, output_dir):
    """Create story markdown file in the specified directory."""
    
    # Generate filename from title
    title = story_data.get('title', 'story')
    # Convert to lowercase, replace spaces with hyphens
    filename = title.lower().replace(' ', '-') + '.md'
    output_path = Path(output_dir) / filename
    
    # Get template path
    script_dir = Path(__file__).parent
    template_path = script_dir / 'assets' / 'story-script-template.md.template'
    
    # Generate markdown
    markdown = generate_story_markdown(story_data, template_path)
    
    # Write story file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"Created story file: {output_path}")
    return output_path


def main():
    """Main function to process command line arguments."""
    
    if len(sys.argv) < 2:
        print("Usage: python create_story.py <story_json_file>")
        print("\nStory JSON file format:")
        print(json.dumps({
            "title": "User Authentication",
            "story": "As a user, I want to log in so that I can access my account",
            "acceptance_criteria": [
                "User can enter email and password",
                "System validates credentials",
                "User is redirected to dashboard on success"
            ],
            "dependencies": ["user-registration"],
            "prerequisites": ["auth-service"],
            "test_hooks": {
                "unit": ["validate_email_format", "validate_password_strength"],
                "integration": ["test_login_flow"],
                "e2e": ["test_complete_user_journey"]
            },
            "delivery_signals": [
                "All acceptance criteria pass",
                "Code is reviewed and approved",
                "Tests pass (unit, integration, e2e)",
                "Documentation is updated",
                "Feature is deployed to staging"
            ],
            "epic": "user-management",
            "architecture_refs": ["auth-architecture"],
            "notes": "This story implements the core authentication flow",
            "implementation_notes": "Consider using JWT tokens for session management"
        }, indent=2))
        sys.exit(1)
    
    # Read JSON file
    json_file = sys.argv[1]
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {json_file}")
        print(f"Details: {e}")
        sys.exit(1)
    
    # Validate story data
    if not validate_story_data(story_data):
        sys.exit(1)
    
    # Determine output directory
    # Default to current directory if not specified
    output_dir = Path.cwd()
    
    # Create story file
    create_story_file(story_data, output_dir)
    
    print("\nStory created successfully!")


if __name__ == "__main__":
    main()
