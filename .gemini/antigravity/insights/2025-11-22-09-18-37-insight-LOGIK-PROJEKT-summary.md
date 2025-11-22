# LOGIK-PROJEKT Summary

## Overview
**LOGIK-PROJEKT** is a comprehensive toolkit designed to automate and standardize the creation, business continuity, and lifecycle management of **Digital Content Creation (DCC)** projects, with a primary focus on **Autodesk Flame**. It empowers artists by handling technical setup, allowing them to focus on creative tasks.

## Key Features
*   **Automated Project Setup**: Generates standardized directory structures and Flame project configurations.
*   **Portal Root Directory**: Implements a strategy for business continuity and redundancy.
*   **Template Management**: Allows import/export of project templates for collaboration.
*   **Flame Integration**: Seamlessly integrates with Autodesk Flame 2025+, managing startup scripts, bookmarks, and workspace configurations.
*   **User-Friendly GUI**: Built with **PySide6**, guiding users through the configuration process.

## System Architecture
The application is structured as a modular Python application:

*   **Entry Point (`app.py`)**: Orchestrates the application startup, logging, theme application, and main window creation.
*   **User Interface (`src/ui/`)**:
    *   **`AppWindow`**: The central hub that manages panels and widgets.
    *   **Panels**: Modular components for different settings (e.g., `FlameOptionsPanel`, `ProjektSummaryPanel`).
    *   **Themes**: Uses a modular dark theme (`LogikProjektModularTheme`).
*   **Core Logic (`src/core/`)**:
    *   **`AppLogic`**: The bridge between UI and backend logic.
    *   **`ProjektManager`**: Handles the actual creation of filesystem structures and Flame projects.
    *   **`TemplateManager`**: Manages the serialization and deserialization of project templates.
*   **Utilities (`src/utils/`)**: Contains helper functions for file operations, system info, and Flame-specific tasks.

## Process Flow
1.  **Initialization**: `app.py` sets up the environment and launches `AppWindow`.
2.  **Configuration**: Users interact with UI panels to define project parameters (resolution, frame rate, directory paths).
3.  **Data Aggregation**: `AppWindow` collects data from all panels.
4.  **Execution**:
    *   **Export/Import**: `TemplateManager` handles JSON template operations.
    *   **Creation**: `ProjektCreator` builds the directory tree, generates Flame setup files (startup scripts, launcher scripts), and configures the database.

## Development Context
*   **Upstream**: `flamelogik/LOGIK-PROJEKT`
*   **Fork**: `LOGIK-PROJEKT-DEV`
*   **Documentation**: Extensive documentation exists in `docs/`, including deep dives into process flows (`docs/insights/process_flow`) and script analysis (`docs/insights/script-analysis`).
