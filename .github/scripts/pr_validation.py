#!/usr/bin/env python3
"""
pr_validation.py
Validate PR quality for IDD workflow automation.
"""
import sys
import os
from github import Github

REPO = "phil-man-git-hub/WORKSTATION-CONFIGURATION"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN environment variable not set.")
    sys.exit(1)

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO)
pr_number = int(sys.argv[1])
pr = repo.get_pull(pr_number)

score = 0
if pr.body and len(pr.body) > 100:
    score += 25
if pr.changed_files > 0:
    score += 25
if pr.additions > 0:
    score += 25
if pr.deletions > 0:
    score += 25

print(f"PR #{pr_number} Quality Score: {score}/100")
if score < 50:
    sys.exit(1)
