# Issue: Update Installation Procedures for Release 2027.0.0

## Summary
Upgrade all installation scripts, templates, and related files from version `2026.2.0` to `2027.0.0` to support the new release. This includes renaming files, updating version markers, and modifying logic to ensure compatibility and clarity for users installing LOGIK-PROJEKT 2027.0.0.

## Tasks
- [ ] Update all version markers in installation scripts and templates from `2026.2.0` to `2027.0.0`.
- [ ] Rename `run_logikprojekt_linux.sh.template` to `run_logik_projekt.sh.template` (if desired for clarity and cross-platform use).
- [ ] Update all references in scripts (e.g., `create_desktop_apps.sh`) to use the new template filename.
- [ ] Review and update logic in `create_desktop_apps.sh` and `get_current_adsk_python.sh` for compatibility with 2027.0.0.
- [ ] Update documentation to reflect new installation steps and file names.
- [ ] Test installation on both macOS and Linux to ensure all scripts work as expected.
- [ ] Update changelog and release notes to document installation changes for 2027.0.0.

## Acceptance Criteria
- All installation scripts and templates reference `2027.0.0`.
- No broken references to old filenames or version markers.
- Installation works on supported platforms (macOS, Linux).
- Documentation is clear and up-to-date.
- Changelog and release notes reflect all changes.

## Related Files
- `install/create_desktop_apps.sh`
- `install/get_current_adsk_python.sh`
- `install/run_logik_projekt.sh.template` (renamed)
- `install/current_adsk_python_version.pref`
- `docs/idd/ISSUE-update-installation-for-2027.0.0.md`
- `CHANGELOG.md`
- `release_notes/`

---
*Created by automation on 2025-11-13 for LOGIK-PROJEKT-DEV release upgrade.*
