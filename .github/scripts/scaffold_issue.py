#!/usr/bin/env python3
"""
Create an issue directory tree from a JSON template file.

Usage:
  python .github/scripts/scaffold_issue.py --template docs/idd/issues/github-issue-tree-template.json \
	--issue-id 001 --issue-title "Add IDD workflow"

This will create `docs/idd/issues/issue-001/` and the subdirs/files from the template,
replacing placeholders `{{issue_id}}` and `{{issue_title}}`.
"""
import argparse
import json
from pathlib import Path

def render(s: str, ctx: dict) -> str:
	# simple placeholder replacement
	for k, v in ctx.items():
		s = s.replace("{{%s}}" % k, v)
	return s

def create_node(node: dict, parent: Path, ctx: dict):
	name = render(node.get("name", ""), ctx)
	node_type = node.get("type")
	path = parent / name
	if node_type == "file" or (not node.get("children") and name):
		# create parent dir first
		path.parent.mkdir(parents=True, exist_ok=True)
		if not path.exists():
			content = f"# {ctx.get('IssueTitle', ctx.get('issue_title'))}\n\nIssue: {ctx.get('GitHubIssueID', ctx.get('issue_id'))}\n\n" \
					  + "This file was scaffolded from the issue template. Add details here.\n"
			path.write_text(content, encoding="utf-8")
	else:
		path.mkdir(parents=True, exist_ok=True)
		for child in node.get("children", []):
			create_node(child, path, ctx)

def main():
	p = argparse.ArgumentParser()
	p.add_argument("--template", required=True)
	p.add_argument("--issue-id", required=True)
	p.add_argument("--issue-title", required=True)
	p.add_argument("--out-base", default="docs/idd/issues")
	args = p.parse_args()

	tpl_path = Path(args.template)
	if not tpl_path.exists():
		raise SystemExit(f"Template not found: {tpl_path}")
	tpl = json.loads(tpl_path.read_text(encoding="utf-8"))

	issue_id = args.issue_id
	# normalize issue dir name
	issue_dir_name = f"issue-{issue_id}"
	out_base = Path(args.out_base)
	target = out_base / issue_dir_name
	if target.exists():
		print(f"Target already exists: {target}")
	else:
		ctx = {
			"issue_id": issue_id,
			"issue_title": args.issue_title,
			"GitHubIssueID": issue_id,
			"GitHubIssueName": args.issue_title,
			"IssueTitle": args.issue_title,
		}
		# create top-level dir
		target.mkdir(parents=True, exist_ok=True)
		for child in tpl.get("children", []):
			create_node(child, target, ctx)
		# create a README for the issue dir
		readme = target / "README.md"
		readme.write_text(f"# Issue {issue_id}: {args.issue_title}\n\nScaffolded issue directory.\n", encoding="utf-8")
		print(f"Scaffolded issue at: {target}")

if __name__ == "__main__":
	main()
