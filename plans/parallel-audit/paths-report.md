# Hardcoded Paths Audit Report

## Critical (Must Fix - Breaks on Other Systems)

| File | Line | Path Found | Issue | Recommendation |
|------|------|------------|-------|----------------|
| .kilocode/mcp.json | 5-6 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .kilocode/mcp.json | 7 | `/c/Users/pavel/projects` | User-specific path - breaks on other accounts | Use `$HOME/projects` or relative path |
| .kilocode/mcp.json | 16-17 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .kilocode/mcp.json | 18 | `/c/Users/pavel/vscodeportable/agentic` | User-specific path - breaks on other accounts | Use `$HOME/vscodeportable` or relative path |
| .kilocode/mcp.json | 22 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-memory/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .kilocode/mcp.json | 26 | `/c/nvm4w/nodejs/node_modules/git-mcp/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .kilocode/mcp.json | 40-41 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .kilocode/mcp.json | 42 | `/c/Users/pavel/projects` | User-specific path - breaks on other accounts | Use `$HOME/projects` or relative path |
| .kilocode/mcp.json | 50-51 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .kilocode/mcp.json | 52 | `/c/Users/pavel/vscodeportable` | User-specific path - breaks on other accounts | Use `$HOME/vscodeportable` or relative path |
| .clinerules/mcp.json | 4-5 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .clinerules/mcp.json | 6 | `/c/Users/pavel/projects` | User-specific path - breaks on other accounts | Use `$HOME/projects` or relative path |
| .clinerules/mcp.json | 10 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-memory/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .clinerules/mcp.json | 14 | `/c/nvm4w/nodejs/node_modules/git-mcp/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .clinerules/mcp.json | 22-23 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .clinerules/mcp.json | 24 | `/c/Users/pavel/projects` | User-specific path - breaks on other accounts | Use `$HOME/projects` or relative path |
| .clinerules/mcp.json | 32-33 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .clinerules/mcp.json | 34 | `/c/Users/pavel/vscodeportable` | User-specific path - breaks on other accounts | Use `$HOME/vscodeportable` or relative path |
| opencode.json | 31-32 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| opencode.json | 33 | `/c/Users/pavel/projects` | User-specific path - breaks on other accounts | Use `$HOME/projects` or relative path |
| opencode.json | 41 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-memory/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| opencode.json | 49 | `/c/nvm4w/nodejs/node_modules/git-mcp/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| opencode.json | 57-58 | `/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| opencode.json | 59 | `/c/Users/pavel/vscodeportable` | User-specific path - breaks on other accounts | Use `$HOME/vscodeportable` or relative path |
| .github/workflows/deploy.yml | 19 | `89.203.173.196` | Hardcoded IP address | Use environment variable or secrets |
| .github/workflows/deploy.yml | 20 | `2260` | Hardcoded port | Use environment variable or secrets |
| .github/workflows/deploy.yml | 29 | `89.203.173.196` | Hardcoded IP address | Use environment variable or secrets |
| .github/workflows/deploy.yml | 30 | `2260` | Hardcoded port | Use environment variable or secrets |
| .github/workflows/deploy.yml | 39 | `89.203.173.196` | Hardcoded IP address | Use environment variable or secrets |
| .github/workflows/deploy.yml | 40 | `2260` | Hardcoded port | Use environment variable or secrets |
| .github/workflows/deploy.yml | 46 | `192.168.1.62` | Hardcoded internal IP | Use environment variable or secrets |
| .github/workflows/deploy.yml | 46 | `2262` | Hardcoded port | Use environment variable or secrets |
| .github/workflows/deploy.yml | 49 | `192.168.1.62` | Hardcoded internal IP | Use environment variable or secrets |
| .github/workflows/deploy.yml | 49 | `2262` | Hardcoded port | Use environment variable or secrets |
| .github/workflows/deploy.yml | 51 | `192.168.1.62` | Hardcoded internal IP | Use environment variable or secrets |
| .github/workflows/deploy.yml | 51 | `2262` | Hardcoded port | Use environment variable or secrets |
| .github/workflows/deploy.yml | 57 | `192.168.1.62` | Hardcoded internal IP | Use environment variable or secrets |
| .github/workflows/deploy.yml | 57 | `2262` | Hardcoded port | Use environment variable or secrets |
| .github/workflows/deploy-litellm.yml | 19 | `100.91.164.109` | Hardcoded IP address | Use environment variable or secrets |
| .github/workflows/deploy-litellm.yml | 23 | `100.91.164.109` | Hardcoded IP address | Use environment variable or secrets |

## High Priority (Should Fix)

| File | Line | Path Found | Issue | Recommendation |
|------|------|------------|-------|----------------|
| .kilocode/mcp.json | 30-31 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| .kilocode/mcp.json | 44-45 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| .kilocode/mcp.json | 54-55 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| .kilocode/mcp.json | 60 | `/c/nvm4w/nodejs/node_modules/bmad-mcp/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .kilocode/mcp.json | 72-73 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| .kilocode/mcp.json | 79 | `/c/nvm4w/nodejs/node_modules/@playwright/mcp/cli.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| .clinerules/mcp.json | 18-19 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| .clinerules/mcp.json | 28-29 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| .clinerules/mcp.json | 38-39 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| .clinerules/mcp.json | 44 | `/c/nvm4w/nodejs/node_modules/@playwright/mcp/cli.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| opencode.json | 63-64 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| opencode.json | 71-72 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| opencode.json | 77 | `/c/nvm4w/nodejs/node_modules/bmad-mcp/dist/index.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |
| opencode.json | 85-86 | `/c/Users/pavel/projects/marketing.tvoje.info/.kilocode/mcp-servers/mcp-wrapper.js` | Project-specific path | Use relative path from project root |
| opencode.json | 91 | `/c/nvm4w/nodejs/node_modules/@playwright/mcp/cli.js` | Git Bash path - won't work on Linux/macOS | Use relative path or environment variable |

## Acceptable (Git Bash / Unix Paths)

| File | Line | Path | Reason It's OK |
|------|------|------|----------------|
| Multiple files | Various | `/c/nvm4w/` | Git Bash convention for Windows paths - acceptable for Windows development environment |
| Multiple files | Various | `/c/Users/pavel/` | Git Bash convention for Windows user paths - acceptable for Windows development environment |

## Summary

- **Total issues found:** 54
- **Critical:** 42 (Hardcoded paths that break cross-platform compatibility)
- **High:** 12 (Project-specific paths that could be more flexible)
- **Acceptable:** 0 (All found paths need attention)

## Key Issues Identified

1. **Cross-Platform Compatibility**: All MCP configurations use Git Bash paths (`/c/...`) which won't work on Linux/macOS systems
2. **User-Specific Paths**: Multiple configurations reference `/c/Users/pavel/` which breaks when cloned by other users
3. **Hardcoded IPs and Ports**: GitHub workflows contain hardcoded IP addresses and ports that should be in secrets
4. **Project-Specific Paths**: Some paths reference the full project path instead of using relative paths

## Recommendations

1. **Use Environment Variables**: Replace user-specific paths with `$HOME` or similar environment variables
2. **Use Relative Paths**: For project-specific paths, use relative paths from the project root
3. **Move IPs to Secrets**: Store IP addresses and ports in GitHub secrets
4. **Platform Detection**: Consider using platform-specific configuration or wrapper scripts
5. **Standardize Path Format**: Choose one path format and stick to it across all configurations