#!/usr/bin/env python3
# -------------------------------------------------------------------------- #
# Filename:     copy_current_session_files.py
# Purpose:      Copies current session files to the project's setups directory.
# Description:  This script handles the copying of session-related files,
#               including preferences & logs, to a specified project directory.

# Author:       phil_man@mac.com
# Copyright:    Copyright (c) 2025
# Disclaimer:   Disclaimer at bottom of script.
# License:      GNU General Public License v3.0 (GPL-3.0).
#               https://www.gnu.org/licenses/gpl-3.0.en.html

# Version:      2027.0.0
# Status:       Production
# Type:         Utility
# Created:      2025-07-01
# Modified:     2025-11-13

# Changelog:    Changelog at bottom of script.
# -------------------------------------------------------------------------- #

import os
import logging
import sys
import shutil
import glob
import json
import re
from datetime import datetime
from pathlib import Path

from src.core.utils.path_utils import get_repository_root_dir
from src.core.functions.get.get_application_paths import GetApplicationPaths


def copy_current_session_files(
        logik_projekt_path: str,
        current_workstation: str,
        flame_projekt_nickname: str | None = None
):
    """
    Copies selected current session files to specific target directories
    with timestamped filenames.

    Args:
        logik_projekt_path (str): The absolute path to the LOGIK-PROJEKT
            project's root directory.
        current_workstation (str): The name of the current workstation.
        flame_projekt_nickname (str|None): Optional nickname for the Flame
            project. If None, the function will attempt to read it from
            the session variables JSON file in the session preferences.
    """
    logging.info("Copying current session files with timestamped names...")

    try:
        repository_root_dir = get_repository_root_dir()
        session_files_source = repository_root_dir / GetApplicationPaths.SESSION_PREFERENCES_DIR

        # Read flame_projekt_nickname from variables file if not provided
        if not flame_projekt_nickname:
            variables_path = session_files_source / "current_session-variables.json"
            try:
                with open(variables_path, "r", encoding="utf-8") as fh:
                    vars_data = json.load(fh)
                    flame_projekt_nickname = vars_data.get("flame_projekt_nickname")
                    logging.debug(f"Loaded flame_projekt_nickname from {variables_path}: {flame_projekt_nickname}")
            except FileNotFoundError:
                logging.warning(f"Variables file not found: {variables_path}; flame_projekt_nickname will remain unset.")
            except json.JSONDecodeError as e:
                logging.warning(f"Failed to parse variables file {variables_path}: {e}")

        # Timestamp to use in filenames
        timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

        # Helper to sanitize names for filenames
        def _sanitize(name: str) -> str:
            return re.sub(r"[^A-Za-z0-9_.-]", "_", name)

        # 1. Copy workstation-scoped files into cfg/workstation/<workstation>/
        workstation_files = [
            "current_session-adsk.json",
            "current_session-flame_launcher.sh",
            "current_session-variables.json",
            "current_session-wiretap_template.xml",
        ]

        workstation_dest = Path(logik_projekt_path) / "cfg" / "workstation" / current_workstation
        workstation_dest.mkdir(parents=True, exist_ok=True)

        for fname in workstation_files:
            src = session_files_source / fname
            if not src.exists():
                logging.warning(f"Source file missing, skipping: {src}")
                continue

            new_fname = fname.replace("current_session", f"{timestamp}-{current_workstation}")
            dst = workstation_dest / new_fname
            shutil.copy2(src, dst)
            logging.info(f"Copied {src} -> {dst}")

        # 2. Copy the template file into cfg/template/ and name using the project nickname
        template_src = session_files_source / "current_session-template.json"
        if template_src.exists():
            template_dest_dir = Path(logik_projekt_path) / "cfg" / "template"
            template_dest_dir.mkdir(parents=True, exist_ok=True)

            nickname = flame_projekt_nickname or "unknown_project"
            nickname = _sanitize(nickname)

            # Use the clean name format: <timestamp>-<nickname>.json
            template_dst_name = f"{timestamp}-{nickname}.json"
            template_dst = template_dest_dir / template_dst_name
            shutil.copy2(template_src, template_dst)
            logging.info(f"Copied template {template_src} -> {template_dst}")
        else:
            logging.warning(f"Template source not found: {template_src}")

        # 3. Preserve behavior: copy most recent .log into logs/<workstation>/
        log_dir = repository_root_dir / GetApplicationPaths.SESSION_LOGS_DIR
        log_files = glob.glob(str(log_dir / '**' / '*.log'), recursive=True)

        if not log_files:
            logging.warning("No session log files found.")
            return

        latest_log_file = max(log_files, key=os.path.getmtime)
        log_file_destination = Path(logik_projekt_path) / "logs" / current_workstation
        log_file_destination.mkdir(parents=True, exist_ok=True)

        if os.path.exists(latest_log_file):
            shutil.copy2(latest_log_file, log_file_destination)
            logging.info(f"Successfully copied {latest_log_file} to {log_file_destination}")
        else:
            logging.warning(f"Log file not found: {latest_log_file}")

    except FileNotFoundError as e:
        logging.error(f"Error finding project root: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during session file copy: {e}")


if __name__ == "__main__":
    # Example usage for direct script execution and testing
    if not (3 <= len(sys.argv) <= 4):
        print(
            "Usage: python copy_current_session_files.py "
            "<logik_projekt_path> <current_workstation> [flame_projekt_nickname]"
        )
        sys.exit(1)

    logik_path = sys.argv[1]
    workstation_name = sys.argv[2]
    flame_nickname = sys.argv[3] if len(sys.argv) == 4 else None

    # For testing, create the base directories if they don't exist
    if not os.path.exists(logik_path):
        print(f"Creating test directory: {logik_path}")
        os.makedirs(logik_path)

    copy_current_session_files(logik_path, workstation_name, flame_nickname)


# -------------------------------------------------------------------------- #

# DISCLAIMER:   This file is part of LOGIK-PROJEKT.

#               Copyright © 2025 STRENGTH IN NUMBERS

#               LOGIK-PROJEKT creates directories, files, scripts & tools
#               for use with Autodesk Flame and other software.

#               LOGIK-PROJEKT is free software.

#               You can redistribute it and/or modify it under the terms
#               of the GNU General Public License as published by the
#               Free Software Foundation, either version 3 of the License,
#               or any later version.

#               This program is distributed in the hope that it will be
#               useful, but WITHOUT ANY WARRANTY; without even the
#               implied warranty of MERCHANTABILITY or
#               FITNESS FOR A PARTICULAR PURPOSE.

#               See the GNU General Public License for more details.
#               You should have received a copy of the GNU General
#               Public License along with this program.

#               If not, see <https://www.gnu.org/licenses/gpl-3.0.en.html>.

#               Contact: phil_man@mac.com

# -------------------------------------------------------------------------- #
# C2 A9 32 30 32 35 53 54 52 45 4E 47 54 48 2D 49 4E 2D 4E 55 4D 42 45 52 53 #
# -------------------------------------------------------------------------- #

# Changelog:
# -------------------------------------------------------------------------- #
# Version:      2027.0.0
# Modified:     2025-11-13
# Changelist:   Updated version to 2026.2.0.
#               Verified compatibility with Autodesk Flame 2026.2.0.
#               No code changes required.
# -------------------------------------------------------------------------- #
