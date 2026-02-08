# TO-DO — next actions

Immediate tasks

- [x] Create PR to add `.github/workflows/issue-scaffold.yml` to the repository default branch (e.g., `dev-2026.2.0`) so the scaffolding workflow runs on issue creation. (Verified: already present on prod-2027.0.0)
- [x] Add `.gitignore` entries to exclude macOS and Linux app bundles and other build artifacts.
- [x] Add `.gitattributes` export-ignore entries for any artifact directories if needed.
- [x] Finalize unit tests for `.github/scripts/scaffold_issue.py` and `sync_labels.py` and add them to CI.

Short-term improvements

- [x] Add contributor docs: `docs/idd/branching.md` describing branch workflow and release flow.
- [x] Add a `CONTRIBUTING.md` with instructions for running the dev venv (`.venv3.13.3`) and using `dev-requirements.txt`.
- [x] Add a PR template that references IDD issue files and encourages linking to the issue scaffolding directory.

Longer term

- [ ] Add branch protection rules for `prod-*` and `release-*` branches.
- [ ] Consider a release automation workflow to publish release artifacts off-runner (not in-repo).

Notes

- We already scaffolded issue-001 locally and created `.github/scripts/scaffold_issue.py`. Use the scaffolded `issue-019/scaffold` branch for testing PR flows.