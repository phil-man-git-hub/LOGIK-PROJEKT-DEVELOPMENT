# Changelog

## 2027.0.0 - 2025-11-13
### Goal
- Prepare LOGIK-PROJEKT for Autodesk Flame 2027.0.0 as a release-quality version, ensuring compatibility, automation, and repo hygiene for production and upstream workflows.

### Summary of Steps and Issues Addressed
- Started from a clean `prod-2027.0.0` branch to ensure a stable base for release work.
- Upgraded all version markers and documentation references to `2027.0.0` across the repo.
- Automated desktop app and runner script generation for both Linux and macOS, including:
  - Renaming runner scripts and templates for clarity and consistency.
  - Creating and updating `.desktop` entries for Linux.
  - Generating `.app` bundles for macOS.
- Improved cross-platform compatibility in shell scripts (macOS/Linux).
- Updated `.gitignore` to exclude local-only test artifacts (`.app`, `.desktop`, runner scripts) from production and upstream pushes.
- Validated and fixed CI workflows for Python 3.13 and new branch naming conventions.
- Ran and passed all unit tests and linters in the dev environment.
- Ensured all changes were staged, committed, and pushed to the working branch (`issue-20/scaffold`).
- Documented and automated local issue tracking and changelist updates.
- Verified successful execution of runner scripts and desktop app creation after synthetic mount fixes for `/PROJEKTS`.
- Confirmed no tracked local-only files remain after `.gitignore` update and untracking.
- Maintained detailed progress tracking and planning using a structured to-do list.

### Related GitHub Issues
- Issue-20: Scaffold, automation, and repo hygiene for 2027.0.0 release
- Issue: Update installation and runner scripts for Flame 2027.0.0
- Issue: Fix CI workflow errors and Python version compatibility
- Issue: Automate desktop entry and app bundle creation
- Issue: Exclude local test artifacts from production pushes
- Issue: Document changelog and release steps

## 0.1.0 - 2025-07-08
### Added
- Initial project structure and core application files.
- Separated UI from business logic.
- Centralized template handling.
- Implemented basic linting and formatting with Ruff.
