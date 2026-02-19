# BMAD Story: Fix CRLF Line Endings

# Story ID: FIX-001

# Priority: MEDIUM

# Status: READY FOR IMPLEMENTATION

## Story

As a developer, I need consistent LF line endings across the repository so that
Git stops warning about CRLF conversions and scripts work correctly on all
platforms.

## Business Value

- **Developer Experience**: No more Git warnings
- **Cross-Platform**: Scripts work on Linux, macOS, Windows
- **Clean History**: No more "fix CRLF" commits
- **CI/CD**: Consistent builds across platforms

## Current Problem

### Symptoms

```
warning: in the working copy of '.kilocode/knowledge/memory-bank/agents-state.md',
CRLF will be replaced by LF the next time Git touches it
```

### Root Cause

Files were created on Windows with CRLF (`\r\n`) but `.gitattributes` specifies
LF (`\n`).

### Impact

- Annoying warnings on every commit
- Pre-commit hooks may fail
- Shell scripts may not execute on Linux

## Acceptance Criteria

- [ ] All text files normalized to LF
- [ ] No more CRLF warnings on commit
- [ ] Shell scripts have executable permissions
- [ ] .gitattributes properly configured
- [ ] Document line ending policy

## Implementation

### Step 1: Verify .gitattributes

File: `.gitattributes` (already exists)

```
# Standardize line endings to LF for all text files
* text=auto eol=lf

# Explicitly mark certain binary files
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.webp binary
*.ico binary
*.pdf binary
*.zip binary
*.7z binary
*.tgz binary
*.gz binary
*.exe binary
*.bin binary
*.pyc binary
```

**Status:** ✅ Already configured correctly

### Step 2: Normalize All Files

```bash
# Configure Git
git config core.autocrlf false
git config core.eol lf

# Normalize all files
git add --renormalize .

# Check what changed
git status

# Commit the normalization
git commit -m "chore: normalize line endings to LF

- Convert all CRLF to LF
- Update .gitattributes for consistency
- Ensure shell scripts are executable
- Fixes #FIX-001"
```

### Step 3: Update Editor Config

File: `.editorconfig` (create if missing)

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{js,ts,jsx,tsx,astro}]
indent_style = space
indent_size = 2

[*.{json,yml,yaml}]
indent_style = space
indent_size = 2

[*.{md,mdx}]
trim_trailing_whitespace = false

[*.{sh,bash}]
end_of_line = lf
```

### Step 4: Pre-Commit Hook Enhancement

Update: `scripts/pre-commit`

```bash
# Add to pre-commit hook
echo "Checking line endings..."
CRLF_FILES=$(find scripts/ -name "*.sh" -exec file {} \; 2>/dev/null | grep "CRLF" | wc -l)
if [ "$CRLF_FILES" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Found CRLF line endings in shell scripts${NC}"
    echo "Run: dos2unix scripts/*.sh"
    exit 1
fi
```

## Verification

### Test 1: Check Current Files

```bash
# Find files with CRLF
find . -type f -name "*.sh" -exec file {} \; | grep CRLF
find . -type f -name "*.md" -exec file {} \; | grep CRLF
find . -type f -name "*.json" -exec file {} \; | grep CRLF
```

### Test 2: Commit Test

```bash
# Make a small change
echo "# Test" >> README.md

# Stage and commit
git add README.md
git commit -m "test: verify LF line endings"

# Should see NO warnings about CRLF
```

## Definition of Done

- [ ] `git add --renormalize .` executed
- [ ] Normalization committed
- [ ] .editorconfig created
- [ ] No CRLF warnings on new commits
- [ ] All shell scripts executable
- [ ] CI/CD passes

## One-Command Fix

```bash
# Complete fix in one command
git config core.autocrlf false && \
git add --renormalize . && \
git commit -m "chore: normalize all line endings to LF" && \
echo "Done! Line endings fixed."
```

## Notes

- This is a one-time fix
- After this, all files will be LF
- Windows editors should respect .editorconfig
- Git will handle conversions automatically

---

**Next Action:** Run the one-command fix, commit, push
