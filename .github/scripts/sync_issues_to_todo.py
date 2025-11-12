#!/usr/bin/env python3
"""
Synchronize GitHub Issues to TO-DO.md

This script fetches open issues from GitHub and updates the TO-DO.md file
with the current issue list. It preserves manual sections and only updates
content between AUTO-SYNC markers.

Usage:
    python sync_issues_to_todo.py

Environment Variables:
    GITHUB_TOKEN: GitHub API token (required)
    GITHUB_REPOSITORY: Repository in format 'owner/repo' (required)
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Tuple, Optional

try:
    from github import Github, GithubException
except ImportError:
    print("Error: PyGithub is not installed. Install with: pip install PyGithub")
    sys.exit(1)


# Configuration
AUTO_SYNC_START = "<!-- BEGIN AUTO-SYNC: DO NOT EDIT MANUALLY -->"
AUTO_SYNC_END = "<!-- END AUTO-SYNC -->"
TODO_FILE = "TO-DO.md"

# Dashboard stats patterns to update
DASHBOARD_PATTERNS = {
    'open_issues': r'- 🔄 \*\*Open Issues:\*\* \d+',
    'completed_issues': r'- ✅ \*\*Completed Issues:\*\* \d+',
    'merged_prs': r'- 🚀 \*\*Merged PRs:\*\* \d+',
}


def get_github_client() -> Github:
    """Initialize and return GitHub client."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable is required")
        sys.exit(1)
    
    return Github(token)


def get_repository_name() -> str:
    """Get repository name from environment."""
    repo_name = os.environ.get('GITHUB_REPOSITORY')
    if not repo_name:
        print("Error: GITHUB_REPOSITORY environment variable is required")
        sys.exit(1)
    
    return repo_name


def fetch_open_issues(github_client: Github, repo_name: str) -> List[dict]:
    """
    Fetch all open issues from the repository.
    
    Args:
        github_client: Authenticated GitHub client
        repo_name: Repository name in format 'owner/repo'
    
    Returns:
        List of issue dictionaries with relevant information
    """
    try:
        repo = github_client.get_repo(repo_name)
        issues = repo.get_issues(state='open', sort='created', direction='asc')
        
        issue_list = []
        for issue in issues:
            # Skip pull requests (they appear as issues in the API)
            if issue.pull_request:
                continue
            
            issue_data = {
                'number': issue.number,
                'title': issue.title,
                'labels': [label.name for label in issue.labels],
                'assignee': issue.assignee.login if issue.assignee else None,
                'milestone': issue.milestone.title if issue.milestone else None,
                'url': issue.html_url,
                'created_at': issue.created_at,
            }
            issue_list.append(issue_data)
        
        return issue_list
    
    except GithubException as e:
        print(f"Error fetching issues: {e}")
        sys.exit(1)


def format_issue_line(issue: dict, repo_name: str) -> str:
    """
    Format an issue as a markdown checkbox line.
    
    Args:
        issue: Issue dictionary
        repo_name: Repository name in format 'owner/repo'
    
    Returns:
        Formatted markdown line
    """
    number = issue['number']
    title = issue['title']
    labels = issue['labels']
    assignee = issue['assignee']
    
    # Build the line
    parts = [f"- [ ] [#{number}](https://github.com/{repo_name}/issues/{number}) {title}"]
    
    # Add labels if present (filter out 'idd' as it's implied)
    relevant_labels = [l for l in labels if l != 'idd']
    if relevant_labels:
        label_str = ', '.join(relevant_labels)
        parts.append(f" `{label_str}`")
    
    # Add assignee if present
    if assignee:
        parts.append(f" @{assignee}")
    
    return ''.join(parts)


def group_issues_by_category(issues: List[dict]) -> dict:
    """
    Group issues by category based on labels.
    
    Args:
        issues: List of issue dictionaries
    
    Returns:
        Dictionary with category names as keys and issue lists as values
    """
    categories = {
        'IDD Foundation': [],
        'Enhancement': [],
        'Bug': [],
        'Documentation': [],
        'Infrastructure': [],
        'Other': []
    }
    
    for issue in issues:
        labels = issue['labels']
        
        # Categorize based on labels
        if 'idd' in labels:
            categories['IDD Foundation'].append(issue)
        elif 'bug' in labels:
            categories['Bug'].append(issue)
        elif 'enhancement' in labels:
            categories['Enhancement'].append(issue)
        elif 'documentation' in labels:
            categories['Documentation'].append(issue)
        elif 'infrastructure' in labels or 'monitoring' in labels:
            categories['Infrastructure'].append(issue)
        else:
            categories['Other'].append(issue)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}


def generate_sync_content(issues: List[dict], repo_name: str) -> str:
    """
    Generate the content to insert between AUTO-SYNC markers.
    
    Args:
        issues: List of issue dictionaries
        repo_name: Repository name in format 'owner/repo'
    
    Returns:
        Formatted markdown content
    """
    if not issues:
        return "<!-- No open issues at this time -->\n"
    
    lines = []
    
    # Group issues by category
    grouped = group_issues_by_category(issues)
    
    for category, category_issues in grouped.items():
        if category_issues:
            lines.append(f"\n#### {category}\n")
            for issue in category_issues:
                lines.append(format_issue_line(issue, repo_name))
    
    # Add metadata footer
    lines.append(f"\n<!-- Last synced: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} -->")
    lines.append(f"<!-- Total open issues: {len(issues)} -->")
    
    return '\n'.join(lines) + '\n'


def read_todo_file() -> str:
    """Read the current TO-DO.md file."""
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {TODO_FILE} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {TODO_FILE}: {e}")
        sys.exit(1)


def find_sync_section(content: str) -> Optional[Tuple[int, int]]:
    """
    Find the AUTO-SYNC section in the content.
    
    Args:
        content: File content
    
    Returns:
        Tuple of (start_pos, end_pos) or None if not found
    """
    start_match = re.search(re.escape(AUTO_SYNC_START), content)
    end_match = re.search(re.escape(AUTO_SYNC_END), content)
    
    if start_match and end_match:
        return (start_match.end(), end_match.start())
    
    return None


def update_todo_file(content: str, new_sync_content: str) -> str:
    """
    Update TO-DO.md with new sync content.
    
    Args:
        content: Current file content
        new_sync_content: New content to insert
    
    Returns:
        Updated file content
    """
    sync_section = find_sync_section(content)
    
    if not sync_section:
        print("Warning: AUTO-SYNC markers not found in TO-DO.md")
        print("Please add the following markers to enable auto-sync:")
        print(f"\n{AUTO_SYNC_START}")
        print("<!-- Issues will be synced here -->")
        print(f"{AUTO_SYNC_END}\n")
        return content
    
    start_pos, end_pos = sync_section
    
    # Build new content
    new_content = (
        content[:start_pos] +
        '\n' + new_sync_content +
        content[end_pos:]
    )
    
    return new_content


def update_dashboard_stats(content: str, open_issue_count: int, github_client: Github, repo_name: str) -> str:
    """
    Update dashboard statistics in the TO-DO.md file.
    
    Args:
        content: Current file content
        open_issue_count: Number of open issues (excluding PRs)
        github_client: Authenticated GitHub client
        repo_name: Repository name
    
    Returns:
        Updated content with current statistics
    """
    try:
        repo = github_client.get_repo(repo_name)
        
        # Get statistics - need to filter out PRs from closed issues
        all_closed = repo.get_issues(state='closed')
        closed_issues_only = sum(1 for issue in all_closed if not issue.pull_request)
        
        merged_prs = len([pr for pr in repo.get_pulls(state='closed') if pr.merged])
        
        # Update the patterns (match pattern more specifically to avoid duplicates)
        content = re.sub(
            r'- 🔄 \*\*Open Issues:\*\* \d+( \(auto-updated\))?',
            f"- 🔄 **Open Issues:** {open_issue_count} (auto-updated)",
            content
        )
        content = re.sub(
            DASHBOARD_PATTERNS['completed_issues'],
            f"- ✅ **Completed Issues:** {closed_issues_only}",
            content
        )
        content = re.sub(
            DASHBOARD_PATTERNS['merged_prs'],
            f"- 🚀 **Merged PRs:** {merged_prs}",
            content
        )
        
        return content
    
    except Exception as e:
        print(f"Warning: Could not update dashboard stats: {e}")
        return content


def write_todo_file(content: str) -> None:
    """Write updated content to TO-DO.md."""
    try:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Successfully updated {TODO_FILE}")
    except Exception as e:
        print(f"Error writing {TODO_FILE}: {e}")
        sys.exit(1)


def main():
    """Main execution function."""
    print("🔄 Starting issue → TO-DO.md sync...")
    
    # Initialize GitHub client
    github_client = get_github_client()
    repo_name = get_repository_name()
    
    print(f"📦 Repository: {repo_name}")
    
    # Fetch open issues
    print("📥 Fetching open issues...")
    issues = fetch_open_issues(github_client, repo_name)
    print(f"✓ Found {len(issues)} open issues")
    
    # Generate sync content
    print("📝 Generating sync content...")
    sync_content = generate_sync_content(issues, repo_name)
    
    # Read current TO-DO.md
    print(f"📖 Reading {TODO_FILE}...")
    current_content = read_todo_file()
    
    # Update TO-DO.md
    print(f"✏️  Updating {TODO_FILE}...")
    new_content = update_todo_file(current_content, sync_content)
    
    # Update dashboard statistics
    print("📊 Updating dashboard statistics...")
    new_content = update_dashboard_stats(new_content, len(issues), github_client, repo_name)
    
    # Check if there are changes
    if new_content == current_content:
        print("ℹ️  No changes needed - TO-DO.md is already up to date")
        return
    
    # Write updated file
    write_todo_file(new_content)
    
    print("\n✅ Sync complete!")
    print(f"   • {len(issues)} issues synced")
    print(f"   • Dashboard statistics updated")
    print(f"   • Updated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")


if __name__ == '__main__':
    main()
