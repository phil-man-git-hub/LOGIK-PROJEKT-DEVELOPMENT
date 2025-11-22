#!/usr/bin/env python3
"""
Automatically create subfiles for every new GitHub Issue in docs/idd/issues/issue-<number>/.

Usage:
	python scripts/solve_github_issue.py <issue_number>

This script should be called by automation (e.g., GitHub Actions) when a new issue is created.
"""
import os
import sys

SUBFILES = [
	"feature-type.md",
	"how-to.md",
	"research.md",
	"insight.md",
	"cognition.md",
	"to-do.md",
	"memory.md",
]

def main():
	"""Main entry point for subfile creation."""
	if len(sys.argv) != 2:
		print("Usage: python scripts/solve_github_issue.py <issue_number>")
		sys.exit(1)

	issue_number = sys.argv[1]
	issue_dir = f"docs/idd/issues/issue-{issue_number}"

	os.makedirs(issue_dir, exist_ok=True)

	STARTER_CONTENT = {
		"feature-type.md": "# Feature Type\n\nThis document describes the type of feature proposed in Issue #{}: GitHub Actions workflow automation for subfile creation.\n",
		"how-to.md": "# How-To Guide\n\nInstructions for implementing and maintaining the GitHub Actions workflow for automated subfile creation (Issue #{}).\n\n## Step-by-Step Implementation\n1. Perform research for a high-level overview and record findings in the research document.\n2. Glean insight from research and record findings in the insight document.\n3. Combine research and insight into cognition and record findings in the cognition document.\n4. Add a detailed step-by-step how-to for implementing the topic and record findings in the how-to document.\n5. Add a new section to the to-do document called how-to and include detailed sub steps from the how-to document.\n",
		"research.md": "# Research\n\nRelevant research, references, and prior art for automating repository tasks with GitHub Actions (Issue #{}).\n\n## High-Level Overview\n(Research findings go here)\n",
		"insight.md": "# Insights\n\nKey insights, lessons learned, and important considerations for Issue #{} automation workflow.\n\n(Insight findings go here)\n",
		"cognition.md": "# Cognition\n\nCognitive strategies, decision points, and rationale for the automation approach in Issue #{}.\n\n(Combined research and insight go here)\n",
		"to-do.md": "# To-Do\n\n- [ ] Add memories to the memory document for this issue.\n\nChecklist and actionable tasks for completing Issue #{} automation workflow.\n\n## Preparatory To-Do Items\n- [ ] Perform research for a high-level overview and record findings in the research document for this issue.\n- [ ] Glean insight from the research, and if necessary perform deeper research, and record findings in the insight document for this issue.\n- [ ] Combine research and insight into cognition for the topic in relation to this repository and record findings in the cognition document for this issue.\n- [ ] Add a detailed step-by-step how-to for implementing the topic in relation to this repository and record findings in the how-to document for this issue.\n",
		"memory.md": "# Memory\n\nPersistent notes, decisions, and historical context for Issue #{} automation workflow.\n"
	}

	for subfile in SUBFILES:
		subdir_name = subfile.replace('.md', '')
		subdir_path = os.path.join(issue_dir, subdir_name)
		os.makedirs(subdir_path, exist_ok=True)
		subfile_path = os.path.join(subdir_path, subfile)
		if not os.path.exists(subfile_path):
			with open(subfile_path, "w") as f:
