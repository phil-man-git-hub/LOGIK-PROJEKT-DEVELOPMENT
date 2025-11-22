# Research: pyside6_qt_get_flame_version

This document analyzes the module:

- [pyside6_qt_get_flame_version.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/functions/pyside6_qt_get_flame_version.py)

## Purpose

Retrieves the current Autodesk Flame version for use in LOGIK-PROJEKT automation and UI workflows.

## Key Functions & Features
### Main Function: `pyside6_qt_get_flame_version`

- **Purpose:** Retrieves the current Autodesk Flame version as a float for use in conditional logic and compatibility checks.
- **Arguments:** None
- **Return:** Float representing Flame version (e.g., 2022.1)

### Version Parsing Logic
- Calls `flame.get_version()` to get the version string
- Strips out `.pr` suffixes and truncates long version strings for normalization
- Converts the result to a float for easy comparison
- Prints the detected version for debugging

### Error Handling & Robustness
- Handles version strings with unexpected formats (e.g., `.pr` builds)
- No explicit exception handling for `flame.get_version()` errors; assumes valid return

### Compatibility
- Supports both PySide6 and PySide2 imports for legacy environments
- Used to gate features and UI logic based on Flame version

- Called by file browser, UI, and automation modules to select appropriate logic for Flame version
- Central to version-dependent feature toggling in LOGIK-PROJEKT
- Used by other modules to adapt behavior based on Flame version
- Function is concise and well-documented
- Extensive changelist documents refactoring and compatibility updates
- No hardcoded secrets or sensitive data detected
- Recommend adding exception handling for unexpected `flame.get_version()` results
- No direct test coverage found; recommend adding automated tests for version parsing
- Further analysis recommended for version parsing and compatibility logic
- No hardcoded secrets or sensitive data detected
