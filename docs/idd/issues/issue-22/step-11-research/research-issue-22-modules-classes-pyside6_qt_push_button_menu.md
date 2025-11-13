# Research: pyside6_qt_push_button_menu

This document analyzes the module:

- [pyside6_qt_push_button_menu.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_push_button_menu.py)

## Purpose

Defines a custom push button menu widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_push_button_menu`
- **Type:** Subclass of `QtWidgets.QPushButton` (PySide6/PySide2)
- **Purpose:** Provides a styled, interactive push button menu for Autodesk Flame UIs.
- **Constructor Args:**
  - `button_name` (str): Text displayed on button
  - `menu_options` (list): List of options shown when button is pressed
  - `menu_width` (int, optional): Width of widget (default 150)
  - `max_menu_width` (int, optional): Max width of widget (default 2000)
  - `menu_action` (callable, optional): Function to execute when menu selection changes
- **UI Behavior:**
  - Push button displays menu on click
  - Menu options are dynamically set
  - Button text updates to selected menu item
  - Custom styling for button and menu
  - No focus by default
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports both PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support
- **Event Handling:**
  - Menu selection updates button text and triggers optional callback
  - `update_menu` method allows dynamic menu updates

## Integration Points
- Used by other LOGIK-PROJEKT modules for menu selection in custom UIs
- Can be instantiated for any menu-driven selection requirement in Flame workflows
- Replaces legacy Flame push button menu widgets for improved modularity and maintainability

## Research Notes
- Code is modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Changelist shows active development and migration from legacy Flame widgets
- Robust error handling and legacy compatibility
- UI logic is encapsulated and easily reusable
- No direct test coverage found; recommend adding automated UI tests for menu selection and error cases
- No external dependencies beyond PySide6/PySide2
- No file or network operations in this class

## Changelist Summary
- Extensive changelist documents migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
