# Story Planning Assets

This directory contains templates and resources for story planning.

## Contents

- `story-script-template.md.template` - Jinja2-style template for generating user story markdown files

## Usage

The template is used by the `create_story.py` script to generate story markdown files from JSON input.

## Template Variables

The template supports the following variables:

- `story_id` - Unique identifier for the story
- `title` - Story title
- `epic` - Epic the story belongs to
- `priority` - Story priority (e.g., P0, P1, P2)
- `effort` - Estimated effort (e.g., 2 days, 1 week)
- `user_type` - Type of user (e.g., "admin", "customer")
- `goal` - What the user wants to accomplish
- `benefit` - Why this is valuable
- `acceptance_criteria` - List of acceptance criteria
- `dependencies` - List of dependencies with types
- `prerequisites` - List of prerequisites
- `test_hooks` - Dictionary with unit, integration, e2e test lists
- `delivery_signals` - List of signals that indicate the story is done
- `architecture_refs` - List of architecture references
- `notes` - Additional notes
- `implementation_notes` - Implementation guidance

## Example JSON Input

```json
{
  "story_id": "AUTH-001",
  "title": "User Authentication",
  "epic": "user-management",
  "priority": "P0",
  "effort": "3 days",
  "user_type": "user",
  "goal": "log in to my account",
  "benefit": "I can access my personalized dashboard",
  "acceptance_criteria": [
    "User can enter email and password",
    "System validates credentials",
    "User is redirected to dashboard on success"
  ],
  "dependencies": [
    {"name": "user-registration", "type": "hard"}
  ],
  "prerequisites": [
    "auth-service",
    "database-schema"
  ],
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
  "architecture_refs": [
    "auth-architecture",
    "security-guidelines"
  ],
  "notes": "This story implements the core authentication flow",
  "implementation_notes": "Consider using JWT tokens for session management"
}
```

## Running the Script

```bash
python scripts/create_story.py story.json
```

This will generate a markdown file named `user-authentication.md` in the current directory.
