#!/usr/bin/env python3
"""
Retrieve context for a specific GitHub issue from IDD documentation.

This script reads the issue documentation from docs/idd/issues/issue-<ID>/
and generates a consolidated context file for AI assistants.
"""

import argparse
import os
import sys
from pathlib import Path


def retrieve_issue_context(issue_id: int, output_file: str) -> None:
    """Retrieve and consolidate context for a specific issue."""
    
    # Locate issue directory
    issue_dir = Path(f"docs/idd/issues/issue-{issue_id}")
    
    if not issue_dir.exists():
        print(f"❌ Error: Issue directory not found: {issue_dir}")
        sys.exit(1)
    
    # Read key files
    context_parts = []
    context_parts.append(f"# Issue {issue_id} Context\n")
    context_parts.append("**Auto-generated from IDD documentation**\n\n")
    
    # Read README
    readme_file = issue_dir / f"issue-{issue_id}-README.md"
    if readme_file.exists():
        context_parts.append("## Overview\n")
        context_parts.append(readme_file.read_text())
        context_parts.append("\n")
    
    # Read to-do
    todo_file = issue_dir / "step-51-to-do" / f"to-do-issue-{issue_id}.md"
    if todo_file.exists():
        context_parts.append("## To-Do List\n")
        context_parts.append(todo_file.read_text())
        context_parts.append("\n")
    
    # Read research (first 50 lines to avoid overwhelming context)
    research_file = issue_dir / "step-11-research" / f"research-issue-{issue_id}.md"
    if research_file.exists():
        context_parts.append("## Research Summary\n")
        lines = research_file.read_text().split('\n')[:50]
        context_parts.append('\n'.join(lines))
        if len(research_file.read_text().split('\n')) > 50:
            context_parts.append("\n\n*(Research truncated - see full file for details)*\n")
        context_parts.append("\n")
    
    # Read memory
    memory_file = issue_dir / "step-61-memory" / f"memory-issue-{issue_id}.md"
    if memory_file.exists():
        context_parts.append("## Memory & Decisions\n")
        context_parts.append(memory_file.read_text())
        context_parts.append("\n")
    
    # Write output
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(''.join(context_parts))
    
    print(f"✅ Context retrieved for Issue #{issue_id}")
    print(f"📄 Output: {output_file}")
    print(f"📊 Size: {len(''.join(context_parts))} characters")


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve context for a GitHub issue from IDD documentation"
    )
    parser.add_argument(
        "--issue",
        type=int,
        required=True,
        help="Issue number (e.g., 22)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="Output file path"
    )
    
    args = parser.parse_args()
    retrieve_issue_context(args.issue, args.output)


if __name__ == "__main__":
    main()
