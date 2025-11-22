# Research: pyside6_qt_message_window

This document analyzes the module:

- [pyside6_qt_message_window.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/modules/classes/pyside6_qt_message_window.py)

## Purpose

Defines a custom message window widget for PySide6/Qt Flame UI integration.

## Key Classes & Features

### Class: `pyside6_qt_message_window`
- **Type:** Subclass of `QtWidgets.QDialog` (PySide6/PySide2)
- **Purpose:** Provides a styled, interactive message window for Autodesk Flame UIs.
- **Constructor Args:**
  - `message_type` (str): Type of message ('confirm', 'message', 'error', 'warning')
  - `message_title` (str): Title text
  - `message` (str): Message body
  - `time` (int, optional): Display time in seconds (default 3)
  - `parent` (optional): Parent widget
- **UI Behavior:**
  - Modal dialog, centered on screen
  - Custom styling and color for each message type
  - Displays message in both UI and Flame console
  - Confirm/cancel or ok button logic based on type
  - Paints colored left bar and header line
  - Supports drag to move window
- **Error Handling:**
  - Type and value checks for all constructor arguments
  - Raises `TypeError` or `ValueError` for invalid types or values
  - Exception handling for Flame message API
- **Compatibility:**
  - Supports both PySide6 and PySide2 (legacy)
  - Designed for Flame 2025+ but maintains legacy support
  - Integrates with Flame's message API (2023.1+)
- **Event Handling:**
  - Custom paint event for colored bar and header
  - Mouse events for window movement
  - Button callbacks for confirm/cancel logic

## Integration Points
- Used by other LOGIK-PROJEKT modules to display interactive messages, errors, and confirmations
- Can be instantiated for any message/confirmation requirement in Flame workflows
- Replaces legacy Flame message windows for improved modularity and maintainability

## Research Notes
- Code is modular, well-documented, and refactored for maintainability
- No hardcoded secrets or sensitive data detected
- Changelist shows active development and migration from legacy Flame widgets
- Robust error handling and legacy compatibility
- UI logic is encapsulated and easily reusable
- No direct test coverage found; recommend adding automated UI tests for message display and button logic
- No external dependencies beyond PySide6/PySide2 and Flame API
- No subprocess, file, or network operations in this class

## Changelist Summary
- Extensive changelist documents migration from legacy Flame widgets to LOGIK-PROJEKT modular PySide6 classes
- Recent updates focus on compatibility, bug fixes, and UI consistency
- Legacy support for PySide2 added in v1.0.3
- No breaking changes detected in recent versions
