# Research: pyside6_qt_list_widget

This document analyzes the module:

- [pyside6_qt_list_widget.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_list_widget.py)

## Purpose

Defines a custom list widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_list_widget`
- **Type:** Subclass of `QtWidgets.QListWidget` (PySide6/PySide2)
- **Purpose:** Provides a styled, multi-select list widget for Autodesk Flame UIs.
- **Constructor Args:**
  - `min_width` (int, optional): Minimum widget width, default 200
  - `max_width` (int, optional): Maximum widget width, default 2000
  - `min_height` (int, optional): Minimum widget height, default 250
  - `max_height` (int, optional): Maximum widget height, default 2000
- **UI Behavior:**
  - Multi-select enabled (ExtendedSelection)
  - Alternating row colors for readability
  - Uniform item sizes for consistency
  - No focus by default
  - Custom scrollbar and tooltip styling
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports both PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support

## Integration Points
- Used by other LOGIK-PROJEKT modules to provide list selection in custom UIs
- Can be instantiated for any list management requirement in Flame workflows
- Replaces legacy Flame list widgets for improved modularity and maintainability

## Research Notes
- Code is modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Changelist shows active development and migration from legacy Flame widgets
- Robust error handling and legacy compatibility
- UI logic is encapsulated and easily reusable
- No direct test coverage found; recommend adding automated UI tests for selection and error cases
- No external dependencies beyond PySide6/PySide2
- No subprocess, file, or network operations in this class

## Changelist Summary
- Extensive changelist documents migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
