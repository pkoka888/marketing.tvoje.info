# Story Planning Scripts

This directory contains automation scripts for story planning and management.

## Contents

- `create_story.py` - Python script for generating user story markdown files from JSON input

## create_story.py

### Purpose

Automates the creation of user story markdown files from structured JSON input. This ensures consistency in story documentation and reduces manual formatting effort.

### Usage

```bash
python scripts/create_story.py <story_json_file>
```

### Input Format

The script expects a JSON file with the following structure:

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

### Output

The script generates a markdown file named after the story title (lowercase with hyphens) in the current directory.

Example: For the JSON above, it creates `user-authentication.md`.

### Validation

The script validates the following:

- **Required fields**: All required fields must be present
- **Data types**: Lists must be lists, dictionaries must be dictionaries
- **Test hooks**: Must include unit, integration, and e2e keys (warnings if missing)

### Error Handling

The script provides clear error messages for:

- Missing required fields
- Invalid JSON format
- File not found errors

### Example Workflow

1. Create a JSON file with story data:
   ```bash
   cat > story.json << 'EOF'
   {
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
       "unit": ["validate_email_format"],
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
     "architecture_refs": ["auth-architecture"]
   }
   EOF
   ```

2. Run the script:
   ```bash
   python scripts/create_story.py story.json
   ```

3. Review the generated markdown file:
   ```bash
   cat user-authentication.md
   ```

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Future Enhancements

Potential improvements to consider:

- Batch processing of multiple stories from a single JSON file
- Command-line options for custom output directory
- Support for additional template variables
- Integration with issue tracking systems (GitHub, Jira, etc.)
