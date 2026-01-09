#!/usr/bin/env python3
"""
Search through captured sessions and memory for specific content.

This script searches the Antigravity knowledge base for relevant context.
"""

import argparse
import re
from pathlib import Path


def search_context(query: str, search_type: str = "all") -> None:
    """Search through knowledge base for query."""
    
    base_dir = Path(".gemini/antigravity")
    
    if not base_dir.exists():
        print(f"❌ Error: Knowledge base not found: {base_dir}")
        return
    
    # Determine search directories
    search_dirs = []
    if search_type in ["all", "sessions"]:
        search_dirs.append(base_dir / "sessions")
    if search_type in ["all", "memory"]:
        search_dirs.append(base_dir / "memory")
    if search_type in ["all", "insights"]:
        search_dirs.append(base_dir / "insights")
    
    results = []
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
            
        for file_path in search_dir.glob("*.md"):
            content = file_path.read_text()
            
            # Case-insensitive search
            if re.search(query, content, re.IGNORECASE):
                # Count matches
                matches = len(re.findall(query, content, re.IGNORECASE))
                results.append({
                    'file': file_path,
                    'matches': matches,
                    'type': search_dir.name
                })
    
    # Sort by match count
    results.sort(key=lambda x: x['matches'], reverse=True)
    
    # Display results
    print(f"🔍 Search: '{query}'")
    print(f"📊 Found {len(results)} file(s) with matches\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['file'].name}")
        print(f"   Type: {result['type']}")
        print(f"   Matches: {result['matches']}")
        print(f"   Path: {result['file']}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Search through Antigravity knowledge base"
    )
    parser.add_argument(
        "query",
        type=str,
        help="Search query (regex supported)"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["all", "sessions", "memory", "insights"],
        default="all",
        help="Type of content to search"
    )
    
    args = parser.parse_args()
    search_context(args.query, args.type)


if __name__ == "__main__":
    main()
