# Research: pyside6_qt_tree_widget

This document analyzes the module:

- [pyside6_qt_tree_widget.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_tree_widget.py)

## Purpose

Defines a custom tree widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_tree_widget`
- **Type:** Subclass of `QtWidgets.QTreeWidget` (PySide6/PySide2)
- **Purpose:** Custom tree widget for Autodesk Flame UIs, supporting hierarchical data display and item selection.
- **Constructor Args:**
  - `tree_headers` (list of str): Column names for the tree
  - `connect` (callable, optional): Function to execute when an item is clicked
  - `tree_min_width` (int, optional): Minimum width (default: 100)
  - `tree_min_height` (int, optional): Minimum height (default: 100)
- **UI Behavior:**
  - Sets minimum size and column headers
  - Enables sorting and alternating row colors
  - Connects item click to provided function
  - Custom styling for tree, headers, selection, and scrollbars
- **Error Handling:**
  - Type checks for all constructor arguments
  - Raises `TypeError` for invalid types
- **Compatibility:**
  - Supports PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support

### Methods
- No custom methods beyond constructor; relies on Qt base class for tree management

## Integration Points
- Used by other LOGIK-PROJEKT modules for hierarchical data display in custom UIs
- Can be instantiated for any workflow requiring tree-based data navigation

## Research Notes
- Modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Robust error handling and legacy compatibility
- UI logic is encapsulated and reusable
- No direct test coverage found; recommend adding automated UI tests for tree population and selection behavior
- No external dependencies beyond PySide6/PySide2
- No file or network operations in this class

## Changelist Summary
- Migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
