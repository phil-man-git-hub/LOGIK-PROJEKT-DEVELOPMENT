# Research: pyside6_qt_clickable_line_edit

This document analyzes the module:

- [pyside6_qt_clickable_line_edit.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_clickable_line_edit.py)

## Purpose

Defines a clickable line edit widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_clickable_line_edit`
- **Type:** Subclass of `QtWidgets.QLineEdit` (PySide6/PySide2)
- **Purpose:** Provides a read-only, clickable line edit widget for Autodesk Flame UIs.
- **Constructor Args:**
  - `text` (str): Initial text to display
  - `connect` (callable): Function to execute on click
  - `width` (int, optional): Widget width (default 150)
  - `max_width` (int, optional): Max widget width (default 2000)
- **Signal:** `clicked` (emitted on left mouse button press)
- **UI Behavior:**
  - Read-only, styled for Flame UI
  - Emits `clicked` signal when pressed
  - Connects external function to click event
  - Custom stylesheet for consistent look
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports both PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support
- **Event Handling:**
  - Overrides `mousePressEvent` to emit `clicked` on left button
  - Falls back to default for other buttons

## Integration Points
- Used by other LOGIK-PROJEKT modules to create interactive, clickable fields in custom UIs
- Can be instantiated and connected to any callable for custom actions
- Replaces legacy Flame widgets for improved modularity and maintainability

## Research Notes
- Code is modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Changelist shows active development and migration from legacy Flame widgets
- Robust error handling and legacy compatibility
- UI logic is encapsulated and easily reusable
- No direct test coverage found; recommend adding automated UI tests for click event and signal emission
- No external dependencies beyond PySide6/PySide2
- No subprocess, file, or network operations in this class

## Changelist Summary
- Extensive changelist documents migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
