# Scripts Documentation

This directory contains automation scripts for the marketing.tvoje.info project.

## Script Inventory

| Script                          | Purpose                        | Creator      |
| ------------------------------- | ------------------------------ | ------------ |
| verify_agentic_platform.py      | Cross-agent integrity check    | Claude Code  |
| verify_api_keys.py              | API key verification (19 keys) | Kilo Code    |
| validate_kilo_configs.py        | YAML/JSON schema validation    | Kilo Code    |
| template_reference_manager.py   | Template metadata manager      | Claude Code  |
| populate_template_references.py | Populate template cross-refs   | Claude Code  |
| validate_template_references.py | Validate template refs         | Claude Code  |
| template_index.py               | Cross-reference table          | Claude Code  |
| new_plan.py                     | Plan creator from templates    | Cline + Kilo |
| generate_images.py              | AI image generation            | Claude Code  |
| orchestrate_flash.py            | Flash orchestration            | Kilo Code    |
| orchestrate_subagents.py        | Subagent orchestration         | Kilo Code    |
| swarm_audit.py                  | Swarm-based audit              | Kilo Code    |
| update_free_models.py           | Free model list updater        | Kilo Code    |
| search_npm.py                   | NPM package search             | Kilo Code    |
| setup_mcp_servers.py            | MCP server setup               | Kilo Code    |
| check_redis.py                  | Redis connectivity check       | Claude Code  |
| validate_env.py                 | .env validation                | Kilo Code    |
| protected/snapshot_config.py    | Config drift detection         | Kilo Code    |

## Usage

\`\`\`bash

# Verify platform

python scripts/verify_agentic_platform.py

# Create plan

python scripts/new_plan.py --list \`\`\`
