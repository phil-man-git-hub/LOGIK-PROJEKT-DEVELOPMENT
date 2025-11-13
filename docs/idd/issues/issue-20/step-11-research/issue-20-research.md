# Issue 20 — Research

**Title:** Update Installation Procedures for Release 2027.0.0

## Installation Procedure Research

**Scripts Involved:**
- create_desktop_apps.sh
- get_current_adsk_python.sh
- run_logik_projekt.sh.template
- current_adsk_python_version.pref

**Information Gathered:**
- Detect available Autodesk Python versions by scanning a base directory (default: /opt/Autodesk/python).
- Sort and select the highest available version using custom logic.
- Write the selected Python executable path to current_adsk_python_version.pref for use by other scripts.
- Log actions and results to dated log files in install/logs/.

**Files Modified/Created:**
- current_adsk_python_version.pref: updated with the path to the chosen Python executable.
- Log files: created in install/logs/ with details of the installation and version selection.
- macOS .app bundle: directories and files created for the application, including Info.plist and shell runner scripts.
- Linux shell script: generated from run_logik_projekt.sh.template with the correct Python path substituted.
- Linux desktop entry: .desktop file created and moved to ~/.local/share/applications/.

**How Information Is Gathered:**
- Directory scanning and sorting for Python versions.
- Reading and updating preference files.
- Logging via shell redirection and custom log_message function.

**How Files Are Modified/Created:**
- Shell commands (mkdir, cat, cp, sed, chmod, mv) are used to create, modify, and move files.
- Python executable path is substituted into templates for runner scripts.