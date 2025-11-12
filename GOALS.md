# LOGIK-PROJEKT-DEV — Goals

Purpose

This repository (`LOGIK-PROJEKT-DEV`) is a personal fork and experimental workspace for developing and validating features, documentation, and workflows before any changes are proposed upstream to the LOGIK-PROJEKT project.

High-level goals

- Provide a safe sandbox for developing features targeted at Autodesk Flame 2027 (branch: `prod-2027.0.0`).
- Capture decisions, research, insights, and how-to guidance using the IDD (Issue-Driven Development) process.
- Ensure build artifacts (macOS app bundles, Linux desktop apps, large binaries) never accidentally propagate upstream or into release artifacts.
- Maintain a clean synchronization path with upstream LOGIK-PROJEKT so that final, vetted changes can be proposed as PRs or release branches.

Branching model (recommended)

- `dev-<series>` (default): day-to-day development and CI validation (e.g., `dev-2026.2.0`).
- `prod-2027.0.0`: long-lived experimental branch for Flame 2027 work where IDD activity is recorded and tested.
- `issue-<NNN>/*`: feature/topic branches scaffolded from issues (scaffolded automatically by CI).
- `release-<version>`: release/prep branches created when a version is ready to propose upstream.

Policy for build artifacts

- Do not build app bundles inside the repository working tree. Use a CI runner or an out-of-repo build directory.
- Add generated app artifact paths to `.gitignore` (and `.gitattributes` export-ignore if necessary).
- If an artifact was accidentally committed and must be removed, use a history rewrite tool (BFG or git-filter-repo) with caution.

IDD and automation

- Issues drive scaffolding and knowledge capture (we scaffold `docs/idd/issues/issue-<NNN>` on new issues via a workflow).
- The `scripts/scaffold_issue.py` creates starter files and a PR; the GitHub Action runs on the default branch.

Syncing with upstream

- Keep an `upstream` remote that points to the original LOGIK-PROJEKT repository.
- Regularly pull upstream into `dev-<series>` and rebase or merge `prod-2027.0.0` as appropriate.

Success criteria

- IDD workflow runs automatically on new issues and produces scaffolded issue branches.
- No app bundles or large binaries are present in main branches or release archives.
- Development on `prod-2027.0.0` is traceable, documented, and ready for PRs to upstream when appropriate.
