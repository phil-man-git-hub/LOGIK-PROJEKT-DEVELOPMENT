# Branching Strategy & Release Flow

This document describes the branching model and release process for LOGIK-PROJEKT. Our workflow is designed to support multiple concurrent versions while maintaining a clear path from development to production.

## Branch Types

### 1. Production Branches (`prod-YYYY.V.V`)
- **Purpose:** The canonical, stable state of a major release.
- **Rules:** 
  - Never commit directly to `prod-*`.
  - Only merged from `release-*` branches after successful validation.
  - Tags are created from these branches.

### 2. Release Branches (`release-YYYY.V.V`)
- **Purpose:** Final preparation for a release (version bumps, changelog updates, final testing).
- **Rules:**
  - Branch from `dev-*` or `prod-*`.
  - Used for stabilizing the release.
  - Merged into `prod-*` when ready.

### 3. Development Branches (`dev-YYYY.V.V`)
- **Purpose:** The main integration branch for ongoing development of a specific version.
- **Rules:**
  - Target for most feature PRs.
  - Should always be in a "mostly stable" state.

### 4. Feature & Fix Branches (`feature/issue-<N>-<desc>` or `fix/issue-<N>-<desc>`)
- **Purpose:** Individual work items.
- **Naming Convention:**
  - `feature/issue-123-short-description`
  - `fix/issue-456-short-description`
- **Rules:**
  - Always branch from the appropriate `dev-*` branch.
  - PR back into the same `dev-*` branch.

## Typical Workflow

### Development Flow (IDD)
1.  **Pick an Issue:** Find an open issue on GitHub.
2.  **Create Branch:** Branch from `dev-YYYY.V.V`.
    ```bash
    git checkout dev-2027.0.0
    git pull origin dev-2027.0.0
    git checkout -b feature/issue-123-add-magic
    ```
3.  **Develop:** Commit changes following [Conventional Commits](https://www.conventionalcommits.org/).
4.  **Sync:** Periodically pull from `dev-2027.0.0` to resolve conflicts early.
5.  **Pull Request:** Push your branch and open a PR into `dev-2027.0.0`.
    - Reference the issue: `Closes #123`.
    - Ensure CI passes.
6.  **Merge:** After review and approval, the branch is merged into `dev-2027.0.0`.

### Release Flow
1.  **Cut Release Branch:**
    ```bash
    git checkout dev-2027.0.0
    git checkout -b release-2027.0.0
    ```
2.  **Prepare:**
    - Update `VERSION` file.
    - Update `CHANGELOG.md`.
    - Run full test suite.
3.  **PR to Production:** Open a PR from `release-2027.0.0` to `prod-2027.0.0`.
4.  **Merge & Tag:**
    - Merge into `prod-2027.0.0`.
    - Tag the release: `v2027.0.0`.
    - (Optional) Backport to `dev-2027.0.0` if any fixes were made on the release branch.

## Maintenance of Older Versions
- Critical security fixes or major bugs may be backported to older `prod-*` and `dev-*` branches following the same PR pattern.
