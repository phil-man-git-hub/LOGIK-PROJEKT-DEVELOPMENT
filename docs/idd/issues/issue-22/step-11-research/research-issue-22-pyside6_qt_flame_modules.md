# Research: PySide6 Qt Flame Modules

This document links to and analyzes the following script:

- [pyside6_qt_flame_modules.py](../../../../../cfg/site-cfg/flame-cfg/flame-python/logik_projekt/openclip_tools/logik_projekt_openclip/scripts/pyside6_qt_flame_modules.py)

## Purpose

This script serves as an aggregator and integration layer for PySide6/Qt modules used in Autodesk Flame workflows. It centralizes UI components, utility functions, and configuration management for LOGIK-PROJEKT tools.

## Static Analysis Findings

### Imports & Dependencies
- **Standard Library:** ast, datetime, functools, importlib, os, re, shutil, subprocess, sys, typing, xml.etree.ElementTree
- **Third Party:** PySide6 (QtWidgets, QtCore, QtGui); falls back to PySide2 if unavailable
- **Project Modules:**
  - `modules.pyside6_qt_flame_classes` (UI widgets: button, label, line edit, etc.)
  - `modules.pyside6_qt_flame_functions` (utility functions: get shot name, print, file browser, config management, etc.)
  - `modules.pyside6_qt_output_config_ui` (output node config UI)

### Structure & Design
- Dynamically appends a `modules` directory to `sys.path` for local imports
- Imports a large set of UI classes and utility functions for use in Flame Python scripts
- Handles legacy support for PySide2
- Contains extensive changelist and version history in comments
- Refactored from monolithic code to modular design (see changelist)

### Integration Points
- Designed to be used in Autodesk Flame environments, providing custom UI and automation tools
- Replaces legacy Flame UI components with PySide6-based widgets
- Integrates with LOGIK-PROJEKT's modular toolset for batch groups, schematic reels, and node configuration

### Notable Features
- Modular import structure for maintainability and extensibility
- Handles environment setup and module path management
- Provides backward compatibility for older Flame/PySide2 setups
- Changelist documents ongoing refactoring and feature additions

## Research Notes
- Further analysis recommended on each imported module for specific functionality
- No hardcoded secrets, credentials, or sensitive data found
- Script is well-structured for extension and integration in complex Flame workflows
