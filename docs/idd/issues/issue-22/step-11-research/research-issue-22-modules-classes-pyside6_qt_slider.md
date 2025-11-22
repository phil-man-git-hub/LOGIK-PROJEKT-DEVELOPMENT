# Research: pyside6_qt_slider

This document analyzes the module:

- [pyside6_qt_slider.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_slider.py)

## Purpose

Defines a custom slider widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_slider`
- **Type:** Subclass of `QtWidgets.QLineEdit` (PySide6/PySide2)
- **Purpose:** Custom slider widget for Autodesk Flame UIs, supporting integer and float values.
- **Constructor Args:**
  - `start_value` (int): Initial value
  - `min_value` (int): Minimum slider value
  - `max_value` (int): Maximum slider value
  - `value_is_float` (bool, optional): Use float values (default: False)
  - `slider_width` (int, optional): Width of slider (default: 110)
- **UI Behavior:**
  - Centered, read-only line edit with custom styling
  - Embedded horizontal slider (disabled, for display only)
  - Value changes update slider position
  - Supports both integer and float types
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support

### Methods
- `calculator()`: Provides a calculator interface for value input (partial implementation shown)
- Value change events update slider display

## Integration Points
- Used by other LOGIK-PROJEKT modules for slider input in custom UIs
- Can be instantiated for any workflow requiring numeric input via slider

## Research Notes
- Modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Robust error handling and legacy compatibility
- UI logic is encapsulated and reusable
- No direct test coverage found; recommend adding automated UI tests for slider and value handling
- No external dependencies beyond PySide6/PySide2
- No file or network operations in this class

## Changelist Summary
- Migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
