# Current Context

## Current Work Focus
Keeper Agent implementation - bridging portable VS Code environment with project configurations.

## Recent Changes
- 2026-02-11: Initialized Memory Bank with brief.md, product.md, context.md, architecture.md, tech.md
- 2026-02-11: Documentation review completed (AGENTS.md, ARCHITECTURE.md, BEST_PRACTICES.md, README.md, SETUP.md, USAGE.md, SECURITY.md, TROUBLESHOOTING.md, PRD.md)
- 2026-02-11: Created Keeper Agent system (.kilocode/rules-keeper/, workflows/, knowledge/)
- 2026-02-11: Created Cline rules (.clinerules/): astro-portfolio.md, tailwind-css.md, accessibility-rules.md, i18n-content.md

## Current State
The project is in **Configuration Phase**. Key configurations exist:

### Core Components
- Core components in `src/components/`
- Pages in `src/pages/` with Czech/English support
- Content in `src/content/projects/`
- i18n translations in `src/i18n/`
- Layouts in `src/layouts/`

### Agent Configuration
- `.kilocode/` - Kilo Code rules and configurations
  - rules-keeper/ - Keeper Agent (analyze.md, sync.md)
  - workflows/ - Standard + Keeper workflows (keeper-analyze.md, keeper-import.md, keeper-sync.md)
  - knowledge/ - Keeper source reference (keeper-sources.md)
- `.clinerules/` - Cline rules (4 project-specific files)

### Source Templates
- Source: `C:\Users\pavel\vscodeportable\agentic\`
- Templates: kilocode-rules, prompts/.clinerules, bmad-skills, bmad-workflow-automation, servers (read-only)

## Known Issues
- None - Memory Bank and Keeper Agent are initialized

## Next Steps
1. Test Keeper Agent workflows ("Keeper analyze all")
2. Begin MVP implementation per PRD timeline
3. Set up development environment (npm install, npm run dev)
4. Configure Vercel deployment

## Environment Notes
- Windows 11 development environment
- Astro 5.0 + Tailwind CSS 4.0 + TypeScript
- Vercel hosting
- Formspree for forms
- Plausible for analytics

## Keeper Agent Commands
| Command | Purpose |
|---------|---------|
| "Keeper analyze all" | Scan portable dir for templates |
| "Keeper sync all" | Sync local with templates |
| "Keeper import workflows" | Import specific templates |
| "Keeper rollback" | Restore from backup |
