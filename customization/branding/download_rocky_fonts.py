#

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

# File Name:        download_rocky_fonts.py
# Version:          0.0.1
# Created:          2024-01-19
# Modified:         2024-08-31

# ========================================================================== #
# This section defines the import statements and directory paths.
# ========================================================================== #

# https://www.kodak.com/en/motion/page/laboratory-tools-and-techniques/


import os
import urllib.request
import zipfile

def download_and_extract(url, extract_to):
    local_filename = os.path.join(extract_to, url.split('/')[-1])
    print(f"Downloading {url}...\n")
    urllib.request.urlretrieve(url, local_filename)
    print(f"Downloaded {local_filename}\n")
   
    print(f"Extracting {local_filename}...\n")
    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {local_filename}\n")

def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
   
    # Create a new folder
    new_folder = os.path.join(script_dir, 'rocky-fonts')
    os.makedirs(new_folder, exist_ok=True)
    print(f"Creating folder: {new_folder}\n")
   
    # URLs of the zip files to download
    zip_urls = [
        'https://github.com/rocky-linux/rocky-fonts/archive/refs/heads/master.zip'
    ]
   
    # Download and extract each zip file
    for url in zip_urls:
        download_and_extract(url, new_folder)
        print(f"Completed processing {url}\n")

if __name__ == '__main__':
    main()

# ========================================================================== #
# 53 54 52 45 4E 47 54 48 2D 49 4E 2D 4E 55 4D 42 45 52 53 C2 A9 32 30 32 35 #
# ========================================================================== #

# Changelist:      

# -------------------------------------------------------------------------- #
# version:          0.0.1
# modified:         2024-08-31 - 16:51:09
# comments:         prep for release - code appears to be functional
# -------------------------------------------------------------------------- #
