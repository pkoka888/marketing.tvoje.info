#!/usr/bin/env python3
"""
Memory Bank Auto-Update Script

Updates context.md with current project state:
- Recent git changes
- Active tasks
- Current phase

Run before each agent session.
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

MEMORY_BANK = Path(".kilocode/rules/memory-bank")
CONTEXT_FILE = MEMORY_BANK / "context.md"


def run_cmd(cmd: str) -> str:
    """Run shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def get_git_changes() -> list:
    """Get recent git changes."""
    changes = []

    # Uncommitted changes
    status = run_cmd("git status --porcelain")
    if status:
        changes.append(f"Uncommitted: {status.split(chr(10))[0][:50]}")

    # Recent commits
    log = run_cmd("git log --oneline -5")
    if log:
        changes.append(f"Recent commits:\n{log}")

    return changes


def get_current_phase() -> str:
    """Detect current project phase."""
    plans = list(Path("plans").glob("PHASE*.md"))
    if plans:
        return plans[0].stem
    return "Unknown"


def get_active_tasks() -> list:
    """Get active tasks from plans."""
    tasks = []

    # Check for active plan files
    for plan in Path("plans").glob("*.md"):
        if plan.stem.startswith("TODO") or "action" in plan.stem.lower():
            tasks.append(plan.name)

    return tasks


def update_context():
    """Update context.md with current state."""
    if not CONTEXT_FILE.exists():
        print(f"Context file not found: {CONTEXT_FILE}")
        return

    # Read existing context
    existing = CONTEXT_FILE.read_text()

    # Extract header (keep first 5 lines)
    lines = existing.split("\n")
    header = "\n".join(lines[:5])

    # Build new content
    phase = get_current_phase()
    git_changes = get_git_changes()
    active_tasks = get_active_tasks()

    new_content = f"""{header}

---

## Current Work Focus

**{datetime.now().strftime("%Y-%m-%d")}**: Auto-updated

- Phase: {phase}
- Active tasks: {len(active_tasks) if active_tasks else "None"}

## Recent Git Changes

{(chr(10).join(git_changes)) if git_changes else "None"}

## Active Task Files

{(chr(10).join(active_tasks)) if active_tasks else "None"}
"""

    # Write back
    CONTEXT_FILE.write_text(new_content)
    print(f"Updated {CONTEXT_FILE}")


if __name__ == "__main__":
    update_context()
