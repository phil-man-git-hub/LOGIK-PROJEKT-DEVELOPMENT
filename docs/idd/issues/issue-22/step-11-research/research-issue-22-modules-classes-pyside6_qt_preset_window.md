# Research: pyside6_qt_preset_window

This document analyzes the module:

- [pyside6_qt_preset_window.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_preset_window.py)

## Purpose

Defines a custom preset window widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_preset_window`
- **Type:** Custom window class (uses multiple PySide6/PySide2 widgets)
- **Purpose:** Provides a styled, interactive preset management window for Autodesk Flame UIs.
- **Constructor Args:**
  - `window_title` (str): Title text
  - `script_name` (str): Name of the script
  - `script_path` (str): Path to the script
  - `setup_window` (callable): Setup window function/class
- **UI Behavior:**
  - Modal window, centered on screen
  - Custom styling and color for preset management
  - Displays current, default, and project presets
  - Buttons for new, edit, set, make default, duplicate, delete, rename, done
  - Push button menu for preset selection
  - XML-based config and preset management
  - Paints colored left bar and header line
  - Supports drag to move window
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
  - Exception handling for file and XML operations
  - User confirmation dialogs for destructive actions
- **Compatibility:**
  - Supports both PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support
  - Integrates with Flame's project and preset APIs
- **Event Handling:**
  - Custom paint event for colored bar and header
  - Mouse events for window movement
  - Button callbacks for all preset management actions
  - XML read/write for config and preset files

## Integration Points
- Used by other LOGIK-PROJEKT modules for preset selection, creation, editing, and management
- Can be instantiated for any preset management requirement in Flame workflows
- Replaces legacy Flame preset windows for improved modularity and maintainability

## Research Notes
- Code is modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Changelist shows active development and migration from legacy Flame widgets
- Robust error handling and legacy compatibility
- UI logic is encapsulated and easily reusable
- No direct test coverage found; recommend adding automated UI tests for preset management and error cases
- No external dependencies beyond PySide6/PySide2 and XML
- No network operations in this class

## Changelist Summary
- Extensive changelist documents migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
