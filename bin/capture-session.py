#!/usr/bin/env python3
"""
Capture development session activity from git commits.

This script analyzes git commits for a specific date and generates
a session summary file in the Antigravity knowledge base.
"""

import argparse
import subprocess
from datetime import datetime
from pathlib import Path


def get_commits_for_date(date_str: str) -> list:
    """Get all commits for a specific date."""
    try:
        # Git log for specific date
        cmd = [
            "git", "log",
            f"--since={date_str} 00:00",
            f"--until={date_str} 23:59",
            "--pretty=format:%h|%an|%s|%ai"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                hash, author, subject, timestamp = line.split('|', 3)
                commits.append({
                    'hash': hash,
                    'author': author,
                    'subject': subject,
                    'timestamp': timestamp
                })
        return commits
    except subprocess.CalledProcessError:
        return []


def capture_session(date_str: str = None) -> None:
    """Capture session activity and generate summary."""
    
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    commits = get_commits_for_date(date_str)
    
    # Generate session file
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    session_file = Path(f".gemini/antigravity/sessions/{timestamp}-session-git-activity.md")
    session_file.parent.mkdir(parents=True, exist_ok=True)
    
    content = []
    content.append(f"# Session: Git Activity for {date_str}\n\n")
    content.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    if commits:
        content.append(f"## Commits ({len(commits)})\n\n")
        for commit in commits:
            content.append(f"- **{commit['hash']}**: {commit['subject']}\n")
            content.append(f"  - Author: {commit['author']}\n")
            content.append(f"  - Time: {commit['timestamp']}\n\n")
    else:
        content.append("## No Commits\n\n")
        content.append(f"No git commits found for {date_str}.\n")
    
    session_file.write_text(''.join(content))
    
    print(f"✅ Session captured for {date_str}")
    print(f"📄 Output: {session_file}")
    print(f"📊 Commits: {len(commits)}")


def main():
    parser = argparse.ArgumentParser(
        description="Capture development session activity from git commits"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date to capture (YYYY-MM-DD format, defaults to today)"
    )
    
    args = parser.parse_args()
    capture_session(args.date)


if __name__ == "__main__":
    main()
