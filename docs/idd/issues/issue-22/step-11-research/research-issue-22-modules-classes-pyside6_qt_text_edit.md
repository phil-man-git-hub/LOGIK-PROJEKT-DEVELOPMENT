# Research: pyside6_qt_text_edit

This document analyzes the module:

- [pyside6_qt_text_edit.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_text_edit.py)

## Purpose

Defines a custom text edit widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_text_edit`
- **Type:** Subclass of `QtWidgets.QPlainTextEdit` (PySide6/PySide2)
- **Purpose:** Custom text edit widget for Autodesk Flame UIs, supporting read-only and editable modes.
- **Constructor Args:**
  - `text` (str): Initial text to display
  - `read_only` (bool, optional): If True, disables editing (default: False)
- **UI Behavior:**
  - Minimum size: 50x150 px
  - Displays initial text, optionally read-only
  - Custom styling for both read-only and editable states
  - Focus policy set to click focus
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support

### Methods
- No custom methods beyond constructor; relies on Qt base class for text management

## Integration Points
- Used by other LOGIK-PROJEKT modules for text input and display in custom UIs
- Can be instantiated for any workflow requiring multi-line text input or display

## Research Notes
- Modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Robust error handling and legacy compatibility
- UI logic is encapsulated and reusable
- No direct test coverage found; recommend adding automated UI tests for text input and read-only behavior
- No external dependencies beyond PySide6/PySide2
- No file or network operations in this class

## Changelist Summary
- Migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
