# Research: pyside6_qt_line_edit

This document analyzes the module:

- [pyside6_qt_line_edit.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_line_edit.py)

## Purpose

Defines a custom line edit widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_line_edit`
- **Type:** Subclass of `QtWidgets.QLineEdit` (PySide6/PySide2)
- **Purpose:** Provides a styled, editable line input widget for Autodesk Flame UIs.
- **Constructor Args:**
  - `text` (str): Initial text to display
  - `width` (int, optional): Widget width, default 150
  - `max_width` (int, optional): Max widget width, default 2000
- **UI Behavior:**
  - Editable field, styled for Flame UI
  - Focus policy set to `ClickFocus` for user interaction
  - Custom stylesheet for consistent look and feel
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports both PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support

## Integration Points
- Used by other LOGIK-PROJEKT modules to provide editable text fields in custom UIs
- Can be instantiated for any text input requirement in Flame workflows
- Replaces legacy Flame line edit widgets for improved modularity and maintainability

## Research Notes
- Code is modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Changelist shows active development and migration from legacy Flame widgets
- Robust error handling and legacy compatibility
- UI logic is encapsulated and easily reusable
- No direct test coverage found; recommend adding automated UI tests for input handling and error cases
- No external dependencies beyond PySide6/PySide2
- No subprocess, file, or network operations in this class

## Changelist Summary
- Extensive changelist documents migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
