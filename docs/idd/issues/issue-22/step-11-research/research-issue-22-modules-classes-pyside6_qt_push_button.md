# Research: pyside6_qt_push_button

This document analyzes the module:

- [pyside6_qt_push_button.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_push_button.py)

## Purpose

Defines a custom push button widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_push_button`
- **Type:** Subclass of `QtWidgets.QPushButton` (PySide6/PySide2)
- **Purpose:** Provides a styled, interactive push button for Autodesk Flame UIs.
- **Constructor Args:**
  - `button_name` (str): Text displayed on button
  - `button_checked` (bool): Initial checked state
  - `connect` (callable, optional): Function to execute when button is pressed
  - `button_width` (int, optional): Width of button (default 150)
- **UI Behavior:**
  - Push button with checkable state
  - Button text and checked state are configurable
  - Custom styling for checked/unchecked/hover/disabled states
  - No focus by default
  - Connects external function to click event
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports both PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support
- **Event Handling:**
  - Click event triggers optional callback
  - Button state and appearance update dynamically

## Integration Points
- Used by other LOGIK-PROJEKT modules for button actions in custom UIs
- Can be instantiated for any button-driven action in Flame workflows
- Replaces legacy Flame push button widgets for improved modularity and maintainability

## Research Notes
- Code is modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Changelist shows active development and migration from legacy Flame widgets
- Robust error handling and legacy compatibility
- UI logic is encapsulated and easily reusable
- No direct test coverage found; recommend adding automated UI tests for button actions and error cases
- No external dependencies beyond PySide6/PySide2
- No file or network operations in this class

## Changelist Summary
- Extensive changelist documents migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
