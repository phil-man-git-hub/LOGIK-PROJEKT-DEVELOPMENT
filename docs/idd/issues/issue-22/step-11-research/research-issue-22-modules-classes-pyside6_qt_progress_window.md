# Research: pyside6_qt_progress_window

This document analyzes the module:

- [pyside6_qt_progress_window.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_progress_window.py)

## Purpose

Defines a custom progress window widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_progress_window`
- **Type:** Subclass of `QtWidgets.QDialog` (PySide6/PySide2)
- **Purpose:** Provides a styled, interactive progress window for Autodesk Flame UIs.
- **Constructor Args:**
  - `window_title` (str): Title text
  - `num_to_do` (int): Total number of operations
  - `text` (str, optional): Message to show in window
  - `window_bar_color` (str, optional): Color of window bar ('blue', 'red', 'green', 'yellow', 'gray', 'teal')
  - `enable_done_button` (bool, optional): Enable done button (default False)
  - `parent` (optional): Parent widget
- **UI Behavior:**
  - Modal dialog, centered on screen
  - Custom styling and color for progress bar and window bar
  - Displays progress bar, message, and done button
  - Paints colored left bar and header line
  - Supports drag to move window
- **Error Handling:**
  - Type and value checks for all constructor arguments
  - Raises `TypeError` or `ValueError` for invalid types or values
- **Compatibility:**
  - Supports both PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support
- **Event Handling:**
  - Custom paint event for colored bar and header
  - Mouse events for window movement
  - Button callback for done/close logic
  - Methods for updating progress and enabling/disabling done button

## Integration Points
- Used by other LOGIK-PROJEKT modules to display progress for batch operations, rendering, or other workflows
- Can be instantiated for any progress tracking requirement in Flame workflows
- Replaces legacy Flame progress windows for improved modularity and maintainability

## Research Notes
- Code is modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Changelist shows active development and migration from legacy Flame widgets
- Robust error handling and legacy compatibility
- UI logic is encapsulated and easily reusable
- No direct test coverage found; recommend adding automated UI tests for progress updates and error cases
- No external dependencies beyond PySide6/PySide2
- No file or network operations in this class

## Changelist Summary
- Extensive changelist documents migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
