#!/bin/bash

# -------------------------------------------------------------------------- #

# DISCLAIMER:       This file is part of LOGIK-PROJEKT.
#                   Copyright Strength In Numbers © 2025
               
#                   LOGIK-PROJEKT creates directories, files, scripts & tools
#                   for use with Autodesk Flame and other software.

#                   LOGIK-PROJEKT is free software.

#                   You can redistribute it and/or modify it under the terms
#                   of the GNU General Public License as published by the
#                   Free Software Foundation, either version 3 of the License,
#                   or any later version.

#                   This program is distributed in the hope that it will be
#                   useful, but WITHOUT ANY WARRANTY; without even the
#                   implied warranty of MERCHANTABILITY or FITNESS FOR A
#                   PARTICULAR PURPOSE.

#                   See the GNU General Public License for more details.

#                   You should have received a copy of the GNU General
#                   Public License along with this program.

#                   If not, see <https://www.gnu.org/licenses/>.
               
#                   Contact: phil_man@mac.com

# -------------------------------------------------------------------------- #

# File Name:        prepend_disclaimer_to_python_files.sh
# Version:          0.0.1
# Created:          2024-01-19
# Modified:         2024-08-31

# ========================================================================== #
# This section defines the primary functions for the script.
# ========================================================================== #

# Get the directory of the running script
path_to_here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set paths
parent_dir="$(dirname $(dirname "$path_to_here"))"
resources_dir="$parent_dir/resources"
docstrings_dir="$resources_dir/docstrings"
disclaimer_file="$docstrings_dir/disclaimer.txt"
disclaimer_log="$docstrings_dir/prepend_disclaimer_log.txt"
modules_dir="$parent_dir/modules/widgets"

# Ensure disclaimer_log exists
touch "$disclaimer_log"

# Start logging
echo "---- Starting disclaimer prepend process ----" >> "$disclaimer_log"
echo "Timestamp: $(date)" >> "$disclaimer_log"
echo "" >> "$disclaimer_log"

# Check if disclaimer_file exists
if [ ! -f "$disclaimer_file" ]; then
    echo "Error: Disclaimer file does not exist." | tee -a "$disclaimer_log"
    exit 1
fi

# Read disclaimer text
disclaimer_text=$(cat "$disclaimer_file")

# Iterate through each Python file in the directory and its subdirectories
find "$modules_dir" -type f -name "*.py" | while read -r python_file; do
    # Read the existing content of the Python file
    existing_content=$(cat "$python_file")
   
    # Combine the disclaimer and the existing content
    updated_content="$disclaimer_text"$'\n'"$existing_content"

    # Write the updated content back to the Python file
    if echo "$updated_content" > "$python_file"; then
        echo "Successfully updated: $python_file" | tee -a "$disclaimer_log"
    else
        echo "Failed to update: $python_file" | tee -a "$disclaimer_log"
    fi
done

# Finish logging
echo "" >> "$disclaimer_log"
echo "---- Disclaimer prepend process completed ----" >> "$disclaimer_log"
echo "Timestamp: $(date)" >> "$disclaimer_log"

# ========================================================================== #
# 53 54 52 45 4E 47 54 48 2D 49 4E 2D 4E 55 4D 42 45 52 53 C2 A9 32 30 32 35 #
# ========================================================================== #

# Changelist:      

# -------------------------------------------------------------------------- #
# version:          0.0.1
# created:          2024-08-31 - 12:34:56
# comments:         utilities to add text to python files.
# -------------------------------------------------------------------------- #
