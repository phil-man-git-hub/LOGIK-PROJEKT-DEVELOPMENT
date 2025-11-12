#!/usr/bin/env python3
"""
Synchronize GitHub Labels

This script reads a YAML file with label definitions and ensures they exist in
the GitHub repository. It will create missing labels and update existing ones
if their color or description has changed.

Usage:
    python sync_labels.py

Environment Variables:
    GITHUB_TOKEN: GitHub API token (required)
    GITHUB_REPOSITORY: Repository in format 'owner/repo' (required)
"""

import os
import sys
from typing import List, Dict

try:
    import yaml
    from github import Github, GithubException
except ImportError:
    print("Error: PyGithub or PyYAML is not installed. Install with: pip install PyGithub PyYAML")
    sys.exit(1)

# Configuration
LABELS_FILE = ".github/labels.yml"


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


def load_defined_labels() -> List[Dict]:
    """Load label definitions from the YAML file."""
    try:
        with open(LABELS_FILE, 'r', encoding='utf-8') as f:
            # The file contains a list of dictionaries
            labels = yaml.safe_load(f)
            if not isinstance(labels, list):
                print(f"Error: Expected '{LABELS_FILE}' to contain a list of labels.")
                sys.exit(1)
            return labels
    except FileNotFoundError:
        print(f"Error: Label definition file not found at '{LABELS_FILE}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{LABELS_FILE}': {e}")
        sys.exit(1)


def main():
    """Main execution function."""
    print("\u231B Starting GitHub label synchronization...")

    github_client = get_github_client()
    repo_name = get_repository_name()

    try:
        repo = github_client.get_repo(repo_name)
        print(f"\U0001f4c1 Repository: {repo_name}")

        # Get existing labels from the repository
        print("\u0001f50d Fetching existing labels from repository...")
        existing_labels = {label.name: label for label in repo.get_labels()}
        print(f"\u2713 Found {len(existing_labels)} existing labels.")

        # Load desired labels from YAML file
        defined_labels = load_defined_labels()
        print(f"\U0001f4c4 Found {len(defined_labels)} labels defined in '{LABELS_FILE}'.")

        stats = {'created': 0, 'updated': 0, 'unchanged': 0}

        # Sync labels
        for label_def in defined_labels:
            name = label_def.get('name')
            color = label_def.get('color')
            description = label_def.get('description', '') # Description is optional

            if not name or not color:
                print(f"\u26a0\ufe0f Skipping invalid label definition: {label_def}")
                continue
            
            # GitHub API requires color without the '#' prefix
            color = color.lstrip('#')

            if name in existing_labels:
                # Label exists, check if it needs an update
                existing_label = existing_labels[name]
                if existing_label.color != color or existing_label.description != description:
                    print(f"\u270f\ufe0f Updating label '{name}'...")
                    existing_label.edit(name=name, color=color, description=description)
                    stats['updated'] += 1
                else:
                    stats['unchanged'] += 1
            else:
                # Label does not exist, create it
                print(f"\u2728 Creating new label '{name}'...")
                repo.create_label(name=name, color=color, description=description)
                stats['created'] += 1
        
        print("\n\u2705 Sync complete!")
        print(f"   - {stats['created']} labels created")
        print(f"   - {stats['updated']} labels updated")
        print(f"   - {stats['unchanged']} labels were already up-to-date")

    except GithubException as e:
        print(f"\n\u274c An error occurred with the GitHub API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\u274c An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
