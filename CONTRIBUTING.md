# Contributing to LOGIK-PROJEKT

Thank you for your interest in contributing! To keep our codebase maintainable and our review process efficient, please follow these guidelines:

## Development Environment

To set up your development environment:

1. **Python 3.13.3**: Ensure you have Python 3.13.3 installed. You can use the provided setup script:
   ```bash
   ./bin/setup-venv-3.13.3.sh
   ```
2. **Virtual Environment**: Activate the virtual environment:
   ```bash
   source .venv3.13.3/bin/activate
   ```
3. **Dependencies**: Install development and project dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt
   ```

## Pull Request Guidelines

- **Break large changes into focused PRs:**
  - Submit small, logically grouped changes rather than large, multi-purpose PRs.
  - Each PR should address a single feature, bugfix, or refactor whenever possible.
  - Large changesets are harder to review, test, and merge. If your work is broad, split it into multiple PRs and reference them in each description.

- **PR Title and Issue Linking:**
  - Use the required PR title format (see PULL_REQUEST_TEMPLATE.md).
  - Link to a relevant issue using "Closes #N" or "Fixes #N" in the PR description.

- **Checklist Before Submitting:**
  - Ensure all code is documented and tested.
  - Update changelogs and release notes as needed.
  - Confirm CI checks pass before requesting review.

## General Contribution Process

1. Fork the repository and create your feature branch from `prod-2027.0.0` or the latest release branch.
2. Make your changes, keeping each PR focused and atomic.
3. Run tests and linters locally before pushing.
4. Open a pull request and fill out all required template sections.
5. Address review feedback promptly and keep PRs up to date with the base branch.

For more details, see the PR template and workflows in `.github/`.

---

If you have questions, open an issue or contact the maintainers.
