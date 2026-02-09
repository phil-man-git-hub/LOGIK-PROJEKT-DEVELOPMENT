#!/usr/bin/env python3
"""
Validate issue filenames in docs/idd/issues/ follow the <issue_type>-<topic>.md pattern.

Usage:
	python validate_issue_filenames.py

Returns non-zero exit code if any filenames do not match the pattern.
"""
import os
import re
import sys

ISSUE_DIR = "docs/idd/issues"
# Allow the documented issue filename prefixes plus the historical github-issue prefix
PATTERN = re.compile(r"^(bug_report|feature_request|task|documentation|monitoring_alert|github-issue)-[a-zA-Z0-9_\-]+\.md$")

def main():
	errors = []
	for fname in os.listdir(ISSUE_DIR):
		if not fname.endswith(".md"):
			continue
		if not PATTERN.match(fname):
			errors.append(fname)
	if errors:
		print("Invalid issue filenames:")
		for e in errors:
			print(f"  {e}")
		sys.exit(1)
	print("All issue filenames are valid.")
	sys.exit(0)

if __name__ == "__main__":
	main()
