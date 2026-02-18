#!/usr/bin/env python3
"""
Memory Bank Retrieval Script

Search Memory Bank for relevant context using simple keyword matching.
For semantic search, integrate with embeddings (optional).

Usage:
    python scripts/memory_retrieve.py "query"
"""

import sys
import re
from pathlib import Path
from collections import defaultdict

MEMORY_BANK = Path(".kilocode/rules/memory-bank")


def extract_keywords(query: str) -> list:
    """Extract keywords from query."""
    # Remove stop words and get meaningful terms
    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "to",
        "for",
        "of",
        "in",
        "on",
    }
    words = re.findall(r"\w+", query.lower())
    return [w for w in words if w not in stop_words and len(w) > 2]


def score_file(content: str, keywords: list) -> int:
    """Score file relevance based on keyword matches."""
    content_lower = content.lower()
    score = 0
    for kw in keywords:
        score += content_lower.count(kw)
    return score


def search_memory(query: str, max_results: int = 3) -> list:
    """Search Memory Bank files for relevant content."""
    keywords = extract_keywords(query)
    if not keywords:
        print("No keywords extracted from query.")
        return []

    print(f"Searching for: {keywords}")

    results = []

    # Search all md files
    for md_file in MEMORY_BANK.glob("*.md"):
        if md_file.name.startswith("."):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            score = score_file(content, keywords)
            if score > 0:
                results.append((md_file, score, content))
        except Exception as e:
            print(f"Error reading {md_file}: {e}")

    # Sort by score
    results.sort(key=lambda x: x[1], reverse=True)

    return results[:max_results]


def format_result(file_path: Path, content: str, max_lines: int = 30) -> str:
    """Format search result for display."""
    lines = content.split("\n")
    # Get first N lines
    preview = "\n".join(lines[:max_lines])

    return f"""
---
## {file_path.name}

{preview}
{"..." if len(lines) > max_lines else ""}
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/memory_retrieve.py <query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    results = search_memory(query)

    if not results:
        print("No relevant results found.")
        return

    print(f"\nFound {len(results)} relevant file(s):\n")

    for file_path, score, content in results:
        print(format_result(file_path, content))


if __name__ == "__main__":
    main()
