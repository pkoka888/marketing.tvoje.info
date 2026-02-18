#!/usr/bin/env python3
"""
Memory Bank Compaction Script

Archives old Memory Bank entries and optionally summarizes them.
Run weekly via cron or manually.
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

MEMORY_BANK = Path(".kilocode/rules/memory-bank")
ARCHIVE = MEMORY_BANK / ".archive"
MAX_AGE_DAYS = 7


def get_file_age_days(file_path: Path) -> float:
    """Get file age in days."""
    mtime = os.path.getmtime(file_path)
    return (datetime.now().timestamp() - mtime) / 86400


def should_archive(file_path: Path) -> bool:
    """Check if file should be archived."""
    if file_path.name.startswith("."):
        return False
    if not file_path.suffix == ".md":
        return False
    if file_path.parent != MEMORY_BANK:
        return False
    age = get_file_age_days(file_path)
    return age > MAX_AGE_DAYS


def compact():
    """Move old files to archive."""
    if not MEMORY_BANK.exists():
        print(f"Memory Bank not found: {MEMORY_BANK}")
        return

    ARCHIVE.mkdir(parents=True, exist_ok=True)

    archived = []
    for md_file in MEMORY_BANK.glob("*.md"):
        if should_archive(md_file):
            month_dir = ARCHIVE / datetime.now().strftime("%Y-%m")
            month_dir.mkdir(parents=True, exist_ok=True)

            dest = month_dir / md_file.name
            shutil.move(str(md_file), str(dest))
            archived.append(f"{md_file.name} -> {dest}")

    if archived:
        print(f"Archived {len(archived)} files:")
        for a in archived:
            print(f"  - {a}")
    else:
        print("No files to archive.")


def list_archived():
    """List archived files."""
    if not ARCHIVE.exists():
        print("No archives found.")
        return

    print("\nArchived files:")
    for month_dir in sorted(ARCHIVE.iterdir(), reverse=True):
        if month_dir.is_dir():
            print(f"\n{month_dir.name}:")
            for f in month_dir.glob("*.md"):
                print(f"  - {f.name}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_archived()
    else:
        compact()
