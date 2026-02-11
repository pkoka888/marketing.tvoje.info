# Agent Configuration Plan

**Created:** 2026-02-11
**Purpose:** Define project-specific agents, skills, workflows, and rules

## Template Sources
- `C:\Users\pavel\vscodeportable\agentic\prompts\.clinerules\` - 27 specialized rules
- `C:\Users\pavel\vscodeportable\agentic\prompts\workflows\` - Workflow templates
- `C:\Users\pavel\vscodeportable\agentic\kilocode-rules\` - Core Kilo Code rules

## Missing Components to Create

### 1. Project-Specific Rules (.kilocode/rules/)
- [ ] `memory-bank-instructions.md` - Memory Bank system instructions
- [ ] `astro-portfolio.md` - Astro 5.0 best practices for this project
- [ ] `tailwind-css.md` - Tailwind CSS 4.0 patterns
- [ ] `accessibility-rules.md` - WCAG 2.2 AA requirements
- [ ] `i18n-content.md` - Czech/English content management

### 2. Ask Mode Rules (.kilocode/rules-ask/)
- [ ] `ask.md` - Ask mode specific rules

### 3. Project-Specific Workflows (.kilocode/workflows/)
- [ ] `implement-portfolio-section.md` - For implementing sections
- [ ] `audit-accessibility.md` - For WCAG compliance checks
- [ ] `optimize-performance.md` - For Lighthouse optimization

### 4. Cline Rules (.clinerules/)
- [ ] Create `.clinerules/` directory
- [ ] `astro-portfolio.md` - Astro portfolio rules
- [ ] `tailwind-styles.md` - Tailwind styling patterns
- [ ] `bilingual-content.md` - CZ/EN content rules

## Implementation Order
1. Copy essential rules from templates
2. Create project-specific Astro/Tailwind rules
3. Create workflow templates
4. Add Ask mode rules
5. Test configuration

## References
- Template: `agentic/prompts/.clinerules/`
- Template: `agentic/prompts/workflows/`
- Existing: `.kilocode/rules-code/implement.md`
