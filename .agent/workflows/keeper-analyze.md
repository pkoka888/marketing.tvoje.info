<task name="Keeper Analyze">

<task_objective>
Scan portable VS Code environment for templates and compare with local project configurations.
</task_objective>

<detailed_sequence_steps>
## Step 1: Scan Source Directories
1. Scan `C:/Users/pavel/vscodeportable/agentic/kilocode-rules/rules/`
2. Scan `C:/Users/pavel/vscodeportable/agentic/kilocode-rules/rules-*/`
3. Scan `C:/Users/pavel/vscodeportable/agentic/prompts/.clinerules/`
4. Scan `C:/Users/pavel/vscodeportable/agentic/prompts/workflows/`
5. Scan `C:/Users/pavel/vscodeportable/agentic/bmad-skills/`
6. Scan `C:/Users/pavel/vscodeportable/agentic/bmad-workflow-automation/`
7. Note: `servers/` is read-only reference only

## Step 2: Build Source Inventory
1. Create inventory of all available templates
2. Note file counts per category
3. Identify version/timestamps if available
4. Store in temporary analysis report

## Step 3: Scan Local Project
1. Scan `.kilocode/` directory structure
2. Scan `.clinerules/` directory
3. List all local configurations
4. Note local versions

## Step 4: Compare and Report
1. Generate comparison table:
   | Template | Source | Local | Status |
2. Identify missing templates
3. Identify newer versions
4. Identify local customizations

## Step 5: Present Results
Present report with:
- Summary statistics
- Missing templates (with import suggestion)
- Newer versions (with sync suggestion)
- Protected local customizations
- Recommended actions
</detailed_sequence_steps>

</task>
