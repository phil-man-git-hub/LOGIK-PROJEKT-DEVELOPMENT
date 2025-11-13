# Research: pyside6_qt_window

This document analyzes the module:

- [pyside6_qt_window.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_window.py)

## Purpose

Defines a custom window widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_window`
- **Type:** Subclass of `QtWidgets.QWidget` (PySide6/PySide2)
- **Purpose:** Custom window widget for Autodesk Flame UIs, supporting styled, movable, and centered application windows.
- **Constructor Args:**
  - `window_title` (str): Title text for window
  - `window_layout` (`QLayout`): Layout object for window content
  - `window_width` (int): Window width
  - `window_height` (int): Window height
  - `window_bar_color` (str, optional): Color of left window bar (`blue`, `red`, `green`, `yellow`, `gray`, `teal`; default: `blue`)
- **UI Behavior:**
  - Frameless, always-on-top window
  - Centered on screen
  - Custom colored left bar and header line (via `paintEvent`)
  - Title label at top, content layout below
  - Movable by dragging window
  - Custom styling for background, tabs, and labels
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` or `ValueError` for invalid types/values
- **Compatibility:**
  - Supports PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support

### Methods
- `paintEvent`: Draws colored bar and header line
- `mousePressEvent`/`mouseMoveEvent`: Enables window dragging

## Integration Points
- Used by other LOGIK-PROJEKT modules for main application windows in custom UIs
- Can be instantiated for any workflow requiring a styled, movable window

## Research Notes
- Modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Robust error handling and legacy compatibility
- UI logic is encapsulated and reusable
- No direct test coverage found; recommend adding automated UI tests for window rendering and drag behavior
- No external dependencies beyond PySide6/PySide2
- No file or network operations in this class

## Changelist Summary
- Migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
