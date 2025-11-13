# Research: pyside6_qt_flame_functions.py

This document analyzes the module:

- [pyside6_qt_flame_functions.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/pyside6_qt_flame_functions.py)

## Purpose

Provides utility functions for Flame automation, context management, and integration in LOGIK-PROJEKT.

## Key Functions & Features

### Module: `pyside6_qt_flame_functions`
- **Purpose:** Aggregates and exposes utility functions for Flame automation, context management, and integration in LOGIK-PROJEKT.
- **Structure:**
  - Dynamically adds the `functions` directory to `sys.path` for modular imports.
  - Imports and exposes the following utility functions:
    - `pyside6_qt_get_shot_name`: Retrieves shot name from context
    - `pyside6_qt_print`: Custom print function for Flame UI/logging
    - `pyside6_qt_get_flame_version`: Gets current Flame version
    - `pyside6_qt_file_browser`: Opens file browser dialog
    - `pyside6_qt_resolve_shot_name`: Resolves shot name from input/context
    - `pyside6_qt_resolve_path_tokens`: Resolves path tokens for file operations
    - `pyside6_qt_refresh_hooks`: Refreshes Flame hooks
    - `pyside6_qt_open_in_finder`: Opens path in Finder (macOS)
    - `pyside6_qt_load_config`: Loads configuration files
    - `pyside6_qt_save_config`: Saves configuration files
    - (Commented out: `pyside6_qt_output_config_ui`)
- **Role:** Provides backend logic for UI modules and main scripts, enabling modular, reusable automation features for Flame Python tools.

### Features
- Centralizes function imports for easier maintenance and refactoring.
- Ensures all utility functions are available for use in UI modules and workflows.
- Supports both PySide6 and PySide2 for legacy compatibility.

## Integration Points
- Used by UI modules and main scripts to provide backend logic.
- Enables modular, reusable automation features for Flame Python tools.
- Facilitates migration from legacy Flame functions to LOGIK-PROJEKT modular functions.

## Research Notes
- Modular, well-documented, and refactored for maintainability.
- No hardcoded secrets or sensitive data detected.
- Robust error handling and legacy compatibility in imported functions.
- No direct test coverage found; recommend adding automated tests for function signatures and side effects.
- No external dependencies beyond PySide6/PySide2.
- No file or network operations in this module (except in imported functions).

## Changelist Summary
- Migration from legacy Flame functions to LOGIK-PROJEKT modular PySide6 functions.
- Recent updates focus on compatibility, bug fixes, and workflow consistency.
- Legacy support for PySide2 added in v1.0.3.
- No breaking changes detected in recent versions.
