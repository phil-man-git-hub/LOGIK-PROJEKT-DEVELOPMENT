#!/usr/bin/env bash
set -eu
repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_dir"
git fetch origin --prune >/dev/null 2>&1 || true
base_ref=origin/prod-2027.0.0
branches=(
  "issue-22-improve-flame-python-scripts"
  "issue-019/scaffold"
  "pman"
  "release-2026.2.0"
  "origin/development-2026-UC"
  "origin/issue-019/scaffold"
  "origin/issue-020/scaffold"
  "origin/issue-022/scaffold"
  "origin/issue-22-improve-flame-python-scripts"
)
echo "Simulating merges into $base_ref using git merge-tree"
printf "\n% -48s | %s\n" "BRANCH" "RESULT"
printf "%0.s-" {1..80}
printf "\n"
for b in "${branches[@]}"; do
  # resolve ref
  if [[ "$b" == origin/* ]]; then
    ref="refs/remotes/${b#origin/}"
  else
    if git show-ref --verify --quiet "refs/heads/$b"; then
      ref="refs/heads/$b"
    elif git show-ref --verify --quiet "refs/remotes/origin/$b"; then
      ref="refs/remotes/origin/$b"
    else
      printf "%-48s | %s\n" "$b" "REF NOT FOUND (skipped)"
      continue
    fi
  fi
  merge_base=$(git merge-base "$base_ref" "$ref" || true)
  if [ -z "$merge_base" ]; then
    printf "%-48s | %s\n" "$b" "NO COMMON ANCESTOR"
    continue
  fi
  tree_a=$(git rev-parse "$base_ref^{tree}")
  tree_b=$(git rev-parse "$ref^{tree}")
  out=$(git merge-tree "$merge_base" "$tree_a" "$tree_b" 2>/dev/null || true)
  if echo "$out" | grep -q "<<<<<<<"; then
    printf "%-48s | %s\n" "$b" "MERGE CONFLICT(s)";
  else
    printf "%-48s | %s\n" "$b" "mergeable (no conflicts)";
  fi
done
