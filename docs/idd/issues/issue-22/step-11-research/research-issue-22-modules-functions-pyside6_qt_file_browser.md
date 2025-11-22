# Research: pyside6_qt_file_browser

This document analyzes the module:

- [pyside6_qt_file_browser.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/functions/pyside6_qt_file_browser.py)

## Purpose

Provides file browser functionality for Flame Python tools using PySide6/Qt.

## Key Functions & Features
### Main Function: `pyside6_qt_file_browser`

- **Purpose:** Opens a file browser dialog for selecting files or directories, supporting both Flame's native browser (2023.1+) and Qt's browser for legacy/compatibility.
- **Arguments:**
	- `title`: Window title (str)
	- `extension`: List of file extensions to filter (list)
	- `default_path`: Initial directory (str, default `/opt/Autodesk`)
	- `select_directory`: Enable directory selection (bool)
	- `multi_selection`: Enable multi-file selection (bool)
	- `include_resolution`: Show resolution controls in Flame browser (bool)
	- `use_flame_browser`: Use Flame's browser if available (bool)
	- `window_to_hide`: List of Qt windows to hide while browser is open (list)
- **Return:** Selected file path(s) (str or list), or None if cancelled

### UI Elements & Logic
- Uses `QtWidgets.QFileDialog` for Qt-based browsing
- Uses `flame.browser.show` for Flame-native browsing (2023.1+)
- Handles hiding/restoring Qt windows during file browser operation
- Filters by extension, supports directory/file mode, multi-selection

### Error Handling
- Type checks for all arguments, raises `TypeError` on invalid input
- Cleans up invalid default paths, falls back to `/opt/Autodesk`
- Prints status and cancellation messages

### Compatibility
- Supports both PySide6 and PySide2 imports for legacy environments
- Adapts to Flame version for browser selection

- Called by other modules for file selection in UI workflows
- Integrates with Flame Python API and PySide6 UI components
- Relies on `pyside6_qt_get_flame_version` to determine browser logic
- Used by UI modules and main scripts for file operations
- Function is well-documented with argument descriptions and usage example
- Extensive changelist documents refactoring, compatibility, and feature updates
- No hardcoded secrets or sensitive data detected
- Legacy support and robust error handling present
- No direct test coverage found; recommend adding automated tests for UI and browser logic
- Further analysis recommended for function signatures and UI logic
- No hardcoded secrets or sensitive data detected
