# Research: pyside6_qt_qdialog

This document analyzes the module:

- [pyside6_qt_qdialog.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_qdialog.py)

## Purpose

Defines a custom QDialog widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_qdialog`
- **Type:** Subclass of `QtWidgets.QDialog` (PySide6/PySide2)
- **Purpose:** Provides a styled, interactive dialog window for Autodesk Flame UIs.
- **Constructor Args:**
  - `window_title` (str): Title text
  - `window_layout` (QtWidgets.QLayout): Layout for window content
  - `window_width` (int): Width of window
  - `window_height` (int): Height of window
  - `window_bar_color` (str, optional): Color of left window bar (default 'blue')
- **UI Behavior:**
  - Modal dialog, centered on screen
  - Custom styling for tabs, background, and window bar
  - Displays title and custom layout
  - Paints colored left bar and header line
  - Supports drag to move window
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports both PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support
- **Event Handling:**
  - Custom paint event for colored bar and header
  - Mouse events for window movement

## Integration Points
- Used by other LOGIK-PROJEKT modules for custom dialog windows in UIs
- Can be instantiated for any dialog-driven workflow in Flame
- Replaces legacy Flame QDialog widgets for improved modularity and maintainability

## Research Notes
- Code is modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Changelist shows active development and migration from legacy Flame widgets
- Robust error handling and legacy compatibility
- UI logic is encapsulated and easily reusable
- No direct test coverage found; recommend adding automated UI tests for dialog rendering and error cases
- No external dependencies beyond PySide6/PySide2
- No file or network operations in this class

## Changelist Summary
- Extensive changelist documents migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
