#

# -------------------------------------------------------------------------- #

# DISCLAIMER:       This file is part of LOGIK-PROJEKT.
#                   Copyright © 2024 man-made-mekanyzms
                
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

# File Name:        download_aces_ocio_clf_files.py
# Version:          0.0.1
# Created:          2024-01-19
# Modified:         2024-08-31

# ========================================================================== #
# This section defines the import statements and directory paths.
# ========================================================================== #

# Standard library imports
import os
import datetime
import shutil
import subprocess
import sys
import tkinter
from tkinter import messagebox
import urllib.request

# ========================================================================== #
# This section defines common paths.
# ========================================================================== #

# Define script_name as the name of the script
script_name = os.path.basename(__file__)

# Define script_dir as the directory containing the script
script_dir = os.path.dirname(__file__)

# Define parent_dir as the parent directory of the script directory
parent_dir = os.path.dirname(script_dir)

# Define a log_dir for storing log files
log_dir = os.path.join(parent_dir, 'logs')

# Create the log directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Create a log file in the log_dir YYYY_MM_DD_HH_MM-OCIO_CLF_Download.log
log_file = os.path.join(
    log_dir,
    f"{datetime.now().strftime('%Y_%m_%d_%H_%M')}-OCIO_CLF_Download.log"
)

# Define ocio_colortoolkit_dir
ocio_colortoolkit_dir = os.path.join(parent_dir, 'ocio_colortoolkit')

 # Create the ocio_colortoolkit directory if it doesn't exist
os.makedirs(ocio_colortoolkit_dir, exist_ok=True)

# Define the temporary directory for downloading files
tmp_dir = os.path.join(parent_dir, 'tmp')

# Create the temp_download directory if it doesn't exist
os.makedirs(tmp_dir, exist_ok=True)

# print the script name and directory
print(f"Script Name: {script_name}")
print(f"Script Directory: {script_dir}")
print(f"Parent Directory: {parent_dir}")
print(f"OCIO Color Toolkit Directory: {ocio_colortoolkit_dir}")
print(f"Temporary Directory: {tmp_dir}")

# ========================================================================== #
# This section defines the primary functions for the script.
# ========================================================================== #

# Add a tkinter message dialog box with an OK button and a Cancel button.
# Prompt the user that the script requires internet access.
# Describe that the script will download and process the ACES OCIO CLF files.
# If the user clicks OK, proceed with the download.
# If the user clicks Cancel, exit the script.
def internet_access_prompt():
    # Create a new tkinter window
    root = tkinter.Tk()
    root.withdraw()
    # Display a message box with an OK and Cancel button
    result = messagebox.askokcancel(
        "Internet Access Required",
        "This script requires internet access to download the ACES OCIO CLF files.\n\nDo you want to proceed?"
    )
    # If the user clicks Cancel, exit the script
    if not result:
        sys.exit()

# Download the ACES OCIO CLF files from the GitHub repository.
def git_clone_clf_files():
    # URL of the GitHub repository
    repo_url = "https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES.git"
    # Branch to checkout
    branch = "main"
    # Local paths
    clone_path = os.path.join(temp_dir, "AcademySoftwareFoundation/OpenColorIO-Config-ACES")
    source_folder = os.path.join(clone_path, "opencolorio_config_aces/clf/transforms")
    # destination_folder = os.path.expanduser("~/resources/flame/opencolorio/AcademySoftwareFoundation/OpenColorIO-Config-ACES/opencolorio_config_aces/clf/transforms")
    destination_folder = os.path.join(ocio_colortoolkit_dir, "AcademySoftwareFoundation/OpenColorIO-Config-ACES/opencolorio_config_aces/clf/transforms")

    # Clone the repository
    subprocess.run(["git", "clone", "--branch", branch, repo_url, clone_path])

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Copy the folder to the desired location
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)

    # Clean up by removing the cloned repository
    shutil.rmtree(clone_path)

    print("Folder downloaded and moved successfully!")

# Download the ACES OCIO CLF files from the GitHub repository using wget.
def download_clf_files():
    # URL of the GitHub repository archive
    repo_url = "https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES/archive/refs/heads/main.zip"
    # Local paths
    zip_path = os.path.join(temp_dir, "OpenColorIO-Config-ACES-main.zip")
    extract_path = os.path.join(temp_dir, "OpenColorIO-Config-ACES-main")
    source_folder = os.path.join(extract_path, "opencolorio_config_aces/clf/transforms")
    destination_folder = os.path.join(ocio_colortoolkit_dir, "AcademySoftwareFoundation/OpenColorIO-Config-ACES/opencolorio_config_aces/clf/transforms")

    # Download the zip file
    urllib.request.urlretrieve(repo_url, zip_path)

    # Extract the zip file
    shutil.unpack_archive(zip_path, temp_dir)

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Copy the folder to the desired location
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)

    # Clean up by removing the downloaded zip file and extracted folder
    os.remove(zip_path)
    shutil.rmtree(extract_path)

    print("Folder downloaded and moved successfully!")


# ========================================================================== #
# This section defines how to handle the main script function.
# ========================================================================== #

if __name__ == "__main__":
    # Prompt the user for internet access
    internet_access_prompt()
    # # Git clone the ACES OCIO CLF files
    # git_clone_clf_files()
    # Download the ACES OCIO CLF files
    download_clf_files()


# ========================================================================== #
# C2 A9 32 30 32 34 2D 4D 41 4E 2D 4D 41 44 45 2D 4D 45 4B 41 4E 59 5A 4D 53 #
# ========================================================================== #

# Changelist:       

# -------------------------------------------------------------------------- #
# version:          0.0.1
# modified:         2024-08-31 - 16:51:09
# comments:         prep for release - code appears to be functional
# -------------------------------------------------------------------------- #
