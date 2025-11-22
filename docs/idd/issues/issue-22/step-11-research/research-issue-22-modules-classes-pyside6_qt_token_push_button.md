# Research: pyside6_qt_token_push_button

This document analyzes the module:

- [pyside6_qt_token_push_button.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_token_push_button.py)

## Purpose

Defines a custom token push button widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_token_push_button`
- **Type:** Subclass of `QtWidgets.QPushButton` (PySide6/PySide2)
- **Purpose:** Custom push button widget for Autodesk Flame UIs, designed to insert tokens into a target `QLineEdit`.
- **Constructor Args:**
  - `button_name` (str): Text displayed on button
  - `token_dict` (dict): Dictionary of tokens, e.g. `{'Token Name': '<Token>'}`
  - `token_dest` (`QLineEdit`): Target line edit for token insertion
  - `button_width` (int, optional): Minimum width (default: 150)
  - `button_max_width` (int, optional): Maximum width (default: 300)
- **UI Behavior:**
  - Styled push button with attached dropdown menu
  - Menu items correspond to token names; selecting inserts token value into target line edit
  - Custom styling for button and menu
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support

### Methods
- Internal `token_action_menu()` builds the menu and connects actions to token insertion
- No public methods beyond constructor; relies on Qt base class for button/menu logic

## Integration Points
- Used by other LOGIK-PROJEKT modules for token-based actions in custom UIs
- Can be instantiated for any workflow requiring token insertion via button/menu

## Research Notes
- Modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Robust error handling and legacy compatibility
- UI logic is encapsulated and reusable
- No direct test coverage found; recommend adding automated UI tests for token insertion and menu behavior
- No external dependencies beyond PySide6/PySide2
- No file or network operations in this class

## Changelist Summary
- Migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
