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

import argparse
import logging
import os
import re
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

# Labels that should never be pruned even if not present in labels.yml
PRUNE_EXEMPT = {"good first issue", "help wanted", "bug"}


def get_github_client() -> Github:
    """Initialize and return GitHub client."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        logging.error("GITHUB_TOKEN environment variable is required")
        sys.exit(1)
    return Github(token)


def get_repository_name() -> str:
    """Get repository name from environment."""
    repo_name = os.environ.get('GITHUB_REPOSITORY')
    if not repo_name:
        logging.error("GITHUB_REPOSITORY environment variable is required")
        sys.exit(1)
    return repo_name


def load_defined_labels(path: str) -> List[Dict]:
    """Load label definitions from the YAML file and normalize entries."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            labels = yaml.safe_load(f)
            if not isinstance(labels, list):
                logging.error("Expected '%s' to contain a list of labels.", path)
                sys.exit(1)

            cleaned = []
            seen = set()
            for l in labels:
                if not isinstance(l, dict):
                    logging.warning("Skipping invalid label entry (not a mapping): %r", l)
                    continue
                name = (l.get('name') or '').strip()
                if not name:
                    logging.warning("Skipping label with empty name: %r", l)
                    continue
                if name in seen:
                    logging.warning("Duplicate label definition for '%s' - skipping duplicate", name)
                    continue
                seen.add(name)
                color = (l.get('color') or '').strip()
                # Normalize by removing leading '#'
                color = color.lstrip('#')
                description = l.get('description') or ''
                cleaned.append({'name': name, 'color': color, 'description': description})
            return cleaned
    except FileNotFoundError:
        logging.error("Label definition file not found at '%s'", path)
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error("Error parsing YAML file '%s': %s", path, e)
        sys.exit(1)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Sync GitHub labels from a YAML file")
    parser.add_argument("--labels-file", default=LABELS_FILE, help="Path to labels YAML file")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without applying changes")
    parser.add_argument("--prune", action="store_true", help="Delete labels not present in labels file (use with care)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(message)s")
    logging.info("⌛ Starting GitHub label synchronization...")

    github_client = get_github_client()
    repo_name = get_repository_name()

    try:
        repo = github_client.get_repo(repo_name)
        logging.info("📁 Repository: %s", repo_name)

        # Get existing labels from the repository
        logging.info("🔍 Fetching existing labels from repository...")
        existing_labels = {label.name: label for label in repo.get_labels()}
        logging.info("✓ Found %d existing labels.", len(existing_labels))

        # Load desired labels from YAML file
        defined_labels = load_defined_labels(args.labels_file)
        logging.info("📄 Found %d labels defined in '%s'.", len(defined_labels), args.labels_file)

        stats = {'created': 0, 'updated': 0, 'unchanged': 0, 'skipped': 0, 'deleted': 0}

        # Sync labels
        defined_names = set()
        for label_def in defined_labels:
            name = label_def.get('name')
            color = (label_def.get('color') or '')
            description = label_def.get('description') or ''  # Description normalized

            if not name or not color:
                logging.warning("⚠️  Skipping invalid label definition: %r", label_def)
                stats['skipped'] += 1
                continue

            # GitHub API requires color without the '#' prefix; normalize short hex and case
            color = color.lstrip('#')
            # Expand 3-digit hex (e.g. f0a -> ff00aa)
            if len(color) == 3 and re.fullmatch(r"[0-9a-fA-F]{3}", color):
                color = ''.join([c*2 for c in color])
            if not re.fullmatch(r"[0-9a-fA-F]{6}", color):
                logging.warning("⚠️  Label '%s' has invalid color '%s' - skipping", name, color)
                stats['skipped'] += 1
                continue
            color = color.lower()

            defined_names.add(name)

            if name in existing_labels:
                # Label exists, check if it needs an update
                existing_label = existing_labels[name]
                existing_desc = existing_label.description or ""
                if existing_label.color != color or existing_desc != description:
                    logging.info("✏️  Updating label '%s'...", name)
                    if args.dry_run:
                        logging.info("    [DRY-RUN] Would edit: color=%s description=%s", color, description)
                    else:
                        existing_label.edit(name=name, color=color, description=description)
                    stats['updated'] += 1
                else:
                    stats['unchanged'] += 1
            else:
                # Label does not exist, create it
                logging.info("✨ Creating new label '%s'...", name)
                if args.dry_run:
                    logging.info("    [DRY-RUN] Would create: color=%s description=%s", color, description)
                else:
                    repo.create_label(name=name, color=color, description=description)
                stats['created'] += 1

        # Optionally prune labels not present in the YAML
        if args.prune:
            to_delete = [n for n in existing_labels if n not in defined_names and n.lower() not in PRUNE_EXEMPT]
            if to_delete:
                logging.info("🗑️  Labels to delete: %s", ', '.join(to_delete))
                for n in to_delete:
                    if args.dry_run:
                        logging.info("    [DRY-RUN] Would delete label: %s", n)
                        stats['deleted'] += 1
                    else:
                        try:
                            existing_labels[n].delete()
                            stats['deleted'] += 1
                        except GithubException as e:
                            logging.error("Failed to delete label '%s': %s", n, e)

        logging.info("\n✅ Sync complete!")
        if args.dry_run:
            logging.info("(dry-run mode — no changes applied)")
        logging.info("   - %d labels created", stats['created'])
        logging.info("   - %d labels updated", stats['updated'])
        logging.info("   - %d labels unchanged", stats['unchanged'])
        logging.info("   - %d definitions skipped", stats['skipped'])
        logging.info("   - %d labels deleted", stats['deleted'])

    except GithubException as e:
        logging.error("❌ An error occurred with the GitHub API: %s", getattr(e, 'data', e))
        sys.exit(1)
    except Exception as e:
        logging.error("❌ An unexpected error occurred: %s", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
