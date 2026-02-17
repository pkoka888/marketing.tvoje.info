<task name="Keeper Sync">

<task_objective>
Synchronize local project configurations with portable VS Code templates while preserving customizations.
</task_objective>

<detailed_sequence_steps>
## Step 1: Analyze Current State
1. Run Keeper Analyze workflow
2. Identify templates with newer versions in source
3. Identify missing templates
4. Generate sync plan

## Step 2: Create Backup
1. Backup `.kilocode/` to `bak/keeper-sync-{timestamp}/`
2. Backup `.clinerules/` if exists
3. Verify backup completeness

## Step 3: User Confirmation
1. Present sync plan with diffs
2. Highlight protected files
3. Get user confirmation
4. If rejected, cancel sync

## Step 4: Apply Sync
For each template:
1. Copy from source `C:/Users/pavel/vscodeportable/agentic/`
2. Check if local version exists
3. If exists: merge, preserving local customizations
4. If missing: copy new file
5. Update only after user confirms

## Step 5: Protected File Handling
Never overwrite:
- `.clinerules/astro-portfolio.md`
- `.clinerules/tailwind-css.md`
- `.clinerules/accessibility-rules.md`
- `.clinerules/i18n-content.md`
- `.kilocode/rules/memory-bank/`

## Step 6: Update Knowledge
1. Update `knowledge/keeper-sources.md`
2. Document sync date and changes
3. Note any conflicts resolved

## Step 7: Verify and Report
1. Test imported rules if applicable
2. Verify no broken configurations
3. Present sync results
4. Provide rollback command: "Keeper rollback"
</detailed_sequence_steps>

</task>
