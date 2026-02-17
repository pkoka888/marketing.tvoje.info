<task name="Keeper Import">

<task_objective>
Import selected templates from portable VS Code environment to local project.
</task_objective>

<detailed_sequence_steps>
## Step 1: User Selection
1. User specifies templates to import (by category or specific files)
2. User can use Keeper Analyze results to identify missing items
3. Confirm selection before proceeding

## Step 2: Backup Current State
1. Create backup of `.kilocode/` directory
2. Create backup of `.clinerules/` directory
3. Store backups in `bak/keeper-{timestamp}/`
4. Verify backups are complete

## Step 3: Check Protected Files
1. Verify selected templates don't conflict with protected files
2. Protected: astro-portfolio.md, tailwind-css.md, accessibility-rules.md, i18n-content.md
3. Protected: `.kilocode/rules/memory-bank/`
4. If conflict, flag for user decision

## Step 4: Copy Templates
1. Copy from source to temporary location
2. Source: `C:/Users/pavel/vscodeportable/agentic/`
3. Destination: `.kilocode/` or `.clinerules/`
4. Adapt to project context if needed

## Step 5: Merge Configurations
1. If file exists locally, merge with template
2. Preserve local customizations
3. Add template improvements
4. Document merge decisions

## Step 6: Update Documentation
1. Update `knowledge/keeper-sources.md` with imported templates
2. Document source path and import date
3. Note any adaptations made

## Step 7: Present Results
1. Show imported files
2. Note any conflicts resolved
3. Provide rollback command if needed
4. Suggest next actions
</detailed_sequence_steps>

</task>
