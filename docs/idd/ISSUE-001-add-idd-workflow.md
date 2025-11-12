# ISSUE-001: Add IDD workflow

Summary

Add an IDD (Issue-Driven Development) GitHub Actions workflow to this repository to validate and automate repository governance for IDD content and artifacts.

Proposed workflow (file: `.github/workflows/idd-workflow.yml`)

- Job: `validate-docs`
  - Run markdown lint and link checks on files under `docs/idd/`.
- Job: `run-tests`
  - Execute `pytest tests/idd/` to run IDD-focused unit tests.
- Job: `label-dryrun`
  - Run `python .github/scripts/sync_labels.py --dry-run --labels-file .github/labels.yml` to validate label changes on PRs.
- Job: `generate-todo` (optional)
  - Run a script to extract or sync TO-DO items from `docs/idd/` into repository TODOs or issues.

Rationale

- Keep IDD documentation healthy (lint/links) and validate changes automatically.
- Prevent accidental label changes by validating them in CI before merge.
- Provide a reproducible developer environment and tests for contributors.

Context & validation already performed locally

- Files added in branch `prod-2027.0.0` (commit 5f2bb42):
  - `dev-requirements.txt` — developer dependencies (PyGithub, PyYAML, pytest)
  - `.github/workflows/labels-dryrun.yml` — GitHub Actions dry-run for label changes
  - `bin/setup-venv-3.13.3.sh` — helper to create a local Python 3.13.3 venv
  - `docs/idd/ai-comprehension.md` and `docs/idd/guides/guide-best-practices.md` — documentation
  - `tests/idd/test_load_defined_labels.py` — unit tests for label YAML parsing
- Created `.venv3.13.3` and installed dev deps inside it.
- Ran unit tests (2 passed) for label YAML loading and normalization.
- Ran `sync_labels.py --dry-run` and then executed a controlled real sync after review; prune dry-run showed no deletions.

Acceptance criteria

- Add `.github/workflows/idd-workflow.yml` implementing the above jobs.
- Jobs should run on push/PRs that touch `docs/idd/**`, `.github/labels.yml`, or `tests/idd/**`.
- The workflow should exit non-zero on lint/test failures or on label-dryrun mismatches.
- Optionally include a matrix to run under supported Python versions or a pinned interpreter.

Next steps

1. Open a PR referencing this file that adds `.github/workflows/idd-workflow.yml`.
2. Iterate on job steps (linters, link-checkers, test commands) in the PR until green.
3. Optionally add indicators/badges to README and link the workflow run to contributing docs.

Notes

- Repository Issues are disabled, so this repo-local issue file records the proposal and provides a traceable artifact.
- If you prefer a Discussion or a real GitHub issue, enable Issues in the repository settings and I can create one for you.
