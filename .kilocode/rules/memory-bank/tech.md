# Technologies and Development Setup

## Tech Stack

### Core Technologies

| Category  | Technology     | Version | Purpose                                         |
| --------- | -------------- | ------- | ----------------------------------------------- |
| Framework | Astro          | 5.0     | Static site generation with island architecture |
| Styling   | Tailwind CSS   | 4.0     | Utility-first CSS framework                     |
| Language  | TypeScript     | 5.7+    | Type safety and developer experience            |
| Hosting   | Debian 13 VPS  | -       | Custom server with PM2                          |
| Forms     | Formspree      | -       | Contact form backend                            |
| Analytics | Plausible      | -       | Privacy-focused analytics                       |
| CI/CD     | GitHub Actions | -       | Automated builds and deployments                |

### Development Tools

| Tool                | Purpose            |
| ------------------- | ------------------ |
| npm                 | Package management |
| ESLint              | Code linting       |
| Prettier            | Code formatting    |
| TypeScript Compiler | Type checking      |

## Development Environment

### Prerequisites

- **Node.js**: 20+
- **npm**: Comes with Node.js
- **Git**: Version control
- **VS Code**: Recommended IDE with Kilo Code extension

### Installation

```bash
# Clone the repository
git clone https://github.com/pkoka888/marketing.tvoje.info.git
cd marketing.tvoje.info

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Available Scripts

| Command                | Description                                |
| ---------------------- | ------------------------------------------ |
| `npm run dev`          | Start development server at localhost:4321 |
| `npm run build`        | Build for production                       |
| `npm run preview`      | Preview production build                   |
| `npm run lint`         | Run ESLint                                 |
| `npm run typecheck`    | Run TypeScript checks                      |
| `npm run format`       | Format code with Prettier                  |
| `npm run format:check` | Check code formatting                      |

## Project Structure

```
marketing.tvoje.info/
├── .kilocode/                    # Kilo Code configuration
│   ├── mcp.json                  # MCP server configuration
│   ├── rules/memory-bank/       # Memory Bank files
│   ├── modes/                    # Custom modes
│   ├── skills/                   # Skills
│   ├── workflows/                # Workflows
│   └── rules-*/                  # Mode-specific rules
├── src/
│   ├── components/
│   │   ├── common/              # Header, Footer
│   │   ├── sections/            # Hero, About, Projects, etc.
│   │   └── ui/                  # Button, Card, Badge
│   ├── content/
│   │   └── projects/            # MDX project content
│   ├── i18n/                    # Internationalization
│   ├── layouts/                 # Page layouts
│   ├── pages/                   # Astro pages
│   │   ├── cs/                 # Czech pages
│   │   ├── projects/           # Project pages
│   │   └── index.astro         # Homepage
│   └── styles/                  # Global styles
├── public/                      # Static assets
├── plans/                       # Planning documents
├── tests/                       # Test files
├── astro.config.mjs             # Astro configuration
├── tailwind.config.mjs          # Tailwind configuration
├── tsconfig.json                # TypeScript configuration
└── package.json                 # npm dependencies
```

## Configuration Files

### astro.config.mjs

- Astro 5.0 configuration
- Integrations: Tailwind, MDX
- Output: static

### tailwind.config.mjs

- Custom color palette (blue, purple, green)
- Typography settings (Inter, JetBrains Mono)
- Responsive breakpoints
- Dark mode configuration

### tsconfig.json

- Strict TypeScript mode
- Path aliases for imports
- JSX support for Astro

### .env Variables

| Variable             | Purpose                     | Required             |
| -------------------- | --------------------------- | -------------------- |
| `PROJECT_NAME`       | Project identifier          | Yes                  |
| `PUBLIC_SITE_URL`    | Public site URL             | Yes                  |
| `VPS_IP`             | VPS IP address              | Yes (for deployment) |
| `FORMSPREE_ENDPOINT` | Formspree form endpoint     | Optional             |
| `PLAUSIBLE_API_KEY`  | Plausible analytics API key | Optional             |
| `REDIS_PASSWORD`     | Redis authentication        | Yes (for MCP)        |
| `REDIS_URL`          | Redis connection URL        | Yes (for MCP)        |
| `FIRECRAWL_API_KEY`  | Firecrawl API access        | Yes (for MCP)        |
| `GITHUB_TOKEN`       | GitHub API authentication   | Yes (for MCP)        |

## Build and Deployment

### Development Build

```bash
npm run dev
# Available at http://localhost:4321
```

### Production Build

```bash
npm run build
# Outputs to dist/ directory
```

### VPS Deployment

- Automatic on push to main branch
- SSH deployment to Debian 13 VPS
- PM2 process manager for application
- Custom domain: marketing.tvoje.info

### CI/CD Pipeline

1. Push to branch → GitHub Actions runs tests
2. Merge to main → SSH deploy to VPS
3. PM2 restarts application automatically

## Testing

### Test Commands

```bash
npm test              # Run all tests
npm run lint         # Linting
npm run typecheck    # Type checking
```

### Test Structure

- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests
- `tests/validation/` - Configuration validation

## Code Quality

### Linting

- ESLint with TypeScript config
- Airbnb style guide
- Prettier integration

### Formatting

- Prettier with standard config
- Automatic format on save

### Type Safety

- Strict TypeScript mode
- No `any` types allowed
- Full type inference

## Performance Targets

| Metric                   | Target | Tool               |
| ------------------------ | ------ | ------------------ |
| Lighthouse Performance   | ≥95    | Lighthouse CI      |
| Lighthouse Accessibility | ≥95    | Lighthouse CI      |
| LCP                      | <2.0s  | PageSpeed Insights |
| FID                      | <100ms | PageSpeed Insights |
| CLS                      | <0.1   | PageSpeed Insights |

## Accessibility Standards

- WCAG 2.2 AA compliance
- Semantic HTML5
- ARIA labels on interactive elements
- Keyboard navigation support
- Color contrast ratio ≥4.5:1

## Security Considerations

- No sensitive data in code
- Environment variables for secrets
- GDPR-compliant analytics (Plausible)
- CSP headers configured
- No user-generated content (static site)

## MCP Server Configuration

### Environment Wrapper

**Problem**: MCP configs used `${VAR_NAME}` syntax which doesn't work in Git
Bash.

**Solution**: Created `mcp-wrapper.js` that loads `.env` before starting
servers.

**Files**:

- `.kilocode/mcp-servers/mcp-wrapper.js` - Main wrapper script
- `.kilocode/mcp.json` - Updated to use wrapper for redis, firecrawl, github
- `.clinerules/mcp.json` - Same updates for Cline

**Usage**:

```bash
# Wrapper automatically loads .env and starts server
node .kilocode/mcp-servers/mcp-wrapper.js redis
node .kilocode/mcp-servers/mcp-wrapper.js firecrawl
node .kilocode/mcp-servers/mcp-wrapper.js github
```

**Benefits**:

- Secrets stay in `.env` only (not in config files)
- Works across Git Bash, PowerShell, CMD
- Validates required variables before starting
- No changes needed when rotating API keys

---

## Agentic IDE Integration

### Google Antigravity

**Installation**: `C:\Users\pavel\vscodeportable\Antigravity` (portable)

**Purpose**: High-capacity AI IDE with Gemini 3 Pro (free, 1M tokens/day)

**Key Features**:

- Agent-first paradigm (autonomous agents plan, execute, verify)
- Cross-interface synergy (Editor + Terminal + Browser)
- MCP support for external tools
- Swarm mode for parallel agents

**Configuration**:

- `.antigravity/mcp.json` - MCP servers
- `.antigravity/skills/` - Custom agent skills (global)
- `.agent/skills/` - Project-specific skills
- `GEMINI.md` - Project instructions (NOT AGENTS.md!)

**Documentation**:

- `.antigravity/README.md` - Full documentation
- `plans/INTEGRATION_PLAN.md` - Unified platform plan
- `plans/ANTIGRAVITY_REVIEW_PROMPT.md` - Review prompt

---

### Kilo Code

**Installation**: `npm install -g @kilocode/cli`

**Purpose**: Bulk coding with free models

**Configuration**:

- `.kilocode/mcp.json` - MCP servers
- `.kilocode/rules-*/` - Mode-specific rules
- `.kilocode/skills/` - Custom skills
- `.kilocode/workflows/` - Workflows
- `.kilocodemodes` - Mode definitions

**Commands**:

```bash
kilo agents list    # List available agents
kilo               # Start TUI
```

---

### OpenCode

**Installation**: `npm install -g opencode`

**Purpose**: Standard coding with Groq models

**Configuration**:

- `.opencode/` - Agents, commands, plugins
- `opencode.json` - Project config
- `AGENTS.md` - Project instructions

**Commands**:

```bash
opencode              # Start TUI
opencode run "task"  # Run task directly
opencode agent list  # List agents
```

---

### Cline (VS Code Extension)

**Installation**: VS Code Marketplace

**Purpose**: VS Code integration with free models

**Configuration**:

- `.clinerules/` - Project rules
- `.clinerules/skills/` - Skills
- `.clinerules/workflows/` - Workflows
- `.clinerules/hooks/` - Pre/post hooks

**Commands** (in VS Code):

- `Cmd+K` / `Ctrl+K` - Open agent

---

### Claude Code

**Installation**: `npm install -g @anthropic-ai/claude-code`

**Purpose**: Deep reasoning with Sonnet 4.5

**Configuration**:

- `.claude/` - Settings
- `CLAUDE.md` - Project instructions

**Commands**:

```bash
claude              # Start session
claude -p "task"   # Run task
```

---

### CLI Tools Comparison

| Tool        | Model              | Cost | Config File  | Skills Location     |
| ----------- | ------------------ | ---- | ------------ | ------------------- |
| Antigravity | Gemini 3 Pro       | Free | GEMINI.md    | .agent/skills/      |
| Kilo        | z-ai/glm4.7        | Free | .kilocode/   | .kilocode/skills/   |
| OpenCode    | groq/llama-3.3-70b | Free | AGENTS.md    | .opencode/skill/    |
| Cline       | minimax:free       | Free | .clinerules/ | .clinerules/skills/ |
| Claude      | claude-sonnet-4-5  | Paid | CLAUDE.md    | N/A                 |

**Best Practices**:

1. Break tasks into 15-30 min chunks
2. Produce artifacts (Plans, Walkthroughs, Diffs)
3. Review agent output early and often
4. Trust but verify - maintain human oversight
5. Use strong typing, avoid `any` types
