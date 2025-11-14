#

# -------------------------------------------------------------------------- #

# File Name:        create_nuke_source_script.py
# Version:          2.2.9
# Created:          2024-01-19
# Modified:         2024-11-09

# ========================================================================== #
# This section imports the necessary modules.
# ========================================================================== #

# import flame
import os
# import pdb; pdb.set_trace()
import re
import fileinput
from string import Template
# import logging
# from datetime import datetime

# ========================================================================== #
# This section defines functions to create nuke scripts.
# ========================================================================== #

# Define function to create a source script
def create_nuke_source_script(shot_name,
                         shots_dir,
                         shot_sources_dir,
                         shot_source_dir,
                         app_name,
                         task_type,
                         version_name,
                         shot_scripts_dir,
                         shot_source_version_openexr_sequences_info,
                         shot_source_version_start_frame,
                         shot_source_version_end_frame):

    """
    Create a source script for nuke based on layer and task.

    Parameters:
        shot_name (str): The name of the shot.
        shots_dir (str): The directory where shots are stored.
        shot_sources_dir (str): The directory for shot sources.
        shot_source_dir (str): The directory for shot source.
        app_name (str): The name of the application.
        task_type (str): The type of task.
        version_name (str): The name of the version.
        shot_scripts_dir (str): The directory for shot scripts.
        shot_source_version_openexr_sequences_info (list): Information about OpenEXR sequences.
        shot_source_version_start_frame (int): Start frame number of the source version.
        shot_source_version_end_frame (int): End frame number of the source version.

    Returns:
    None
    """

    # Define the directory for the specific app and task type
    source_scripts_app_task_dir = os.path.join(shots_dir,
                                               shot_scripts_dir,
                                               app_name,
                                               'sources',
                                               task_type)

    # Create the directory if it doesn't exist
    os.makedirs(source_scripts_app_task_dir, exist_ok=True)

    # Define the file path for the script
    source_scripts_app_task_file = f"{shot_source_dir}_{app_name}_{task_type}_{version_name}.nk"
    source_scripts_app_task_path = os.path.join(source_scripts_app_task_dir,
                                                source_scripts_app_task_file)

    # Append the Nuke script content to the file
    with open(source_scripts_app_task_path, 'a') as nuke_source_script_file:
        template_path = Path(__file__).resolve().parent / "templates" / "nuke_source_script_template.nk"
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        substitutions = {
            "SHOT_SOURCE_DIR": shot_source_dir,
            "APP_NAME": app_name,
            "TASK_TYPE": task_type,
            "VERSION_NAME": version_name,
            "SHOT_SOURCE_VERSION_START_FRAME": str(shot_source_version_start_frame),
            "SHOT_SOURCE_VERSION_END_FRAME": str(shot_source_version_end_frame),
            "SHOT_SOURCE_VERSION_SEQUENCE_DIR": shot_source_version_openexr_sequences_info[1]['shot_source_version_sequence_dir'],
            "SHOT_SOURCES_DIR": shot_sources_dir,
        }
        
        nuke_script_content = Template(template_content).substitute(substitutions)
        nuke_source_script_file.write(nuke_script_content)

        # # This section is for logging purposes
        # logging.debug(f"Nuke script created for:  {shot_source_dir}_{version_name}")

        print(f"Nuke Source script created:  {source_scripts_app_task_file}\n")

    # Define the directory for the specific app and task type
    shot_scripts_app_task_dir = os.path.join(shots_dir,
                                             shot_scripts_dir,
                                             app_name,
                                             'shot',
                                             task_type)

    # Create the directory if it doesn't exist
    os.makedirs(shot_scripts_app_task_dir, exist_ok=True)

    # Define the file path for the script
    shot_scripts_app_task_file = f"{shot_name}_{app_name}_{task_type}_{version_name}.nk"
    shot_scripts_app_task_path = os.path.join(shot_scripts_app_task_dir,
                                              shot_scripts_app_task_file)

    # Open the file for in-place editing
    with fileinput.FileInput(shot_scripts_app_task_path, inplace=True) as file:
        for line in file:
            # Replace 'NUKE_START_FRAME' with the value of 'shot_source_version_start_frame'
            line = line.replace('NUKE_START_FRAME', str(shot_source_version_start_frame))
            # Replace 'NUKE_END_FRAME' with the value of 'shot_source_version_end_frame'
            line = line.replace('NUKE_END_FRAME', str(shot_source_version_end_frame))
            print(line, end='')

    # Write the Nuke script content to the file
    with open(shot_scripts_app_task_path, 'a') as nuke_shot_script_file:
        template_path = Path(__file__).resolve().parent / "templates" / "nuke_source_script_template.nk"
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        substitutions = {
            "SHOT_SOURCE_DIR": shot_source_dir,
            "APP_NAME": app_name,
            "TASK_TYPE": task_type,
            "VERSION_NAME": version_name,
            "SHOT_SOURCE_VERSION_START_FRAME": str(shot_source_version_start_frame),
            "SHOT_SOURCE_VERSION_END_FRAME": str(shot_source_version_end_frame),
            "SHOT_SOURCE_VERSION_SEQUENCE_DIR": shot_source_version_openexr_sequences_info[1]['shot_source_version_sequence_dir'],
            "SHOT_SOURCES_DIR": shot_sources_dir,
        }
        
        nuke_script_content = Template(template_content).substitute(substitutions)
        nuke_shot_script_file.write(nuke_script_content)

        # # This section is for logging purposes
        # logging.debug(f"Nuke script appended for:  {shot_name}_{app_name}_{task_type}_{version_name}")

        print(f"Read/Write nodes appended:   {shot_source_dir}_{app_name}_{task_type}\n")

# ========================================================================== #
# C2 A9 32 30 32 34 2D 4D 41 4E 2D 4D 41 44 45 2D 4D 45 4B 41 4E 59 5A 4D 53 #
# ========================================================================== #

# Changelist:

# -------------------------------------------------------------------------- #
# version:               0.0.1
# modified:              2024-05-03 - 01:50:36
# comments:              Basic functionality defined and tested
# -------------------------------------------------------------------------- #
# version:               0.0.2
# modified:              2024-05-03 - 02:12:19
# comments:              Fixed some formatting and flame menus
# -------------------------------------------------------------------------- #
# version:               0.0.3
# modified:              2024-05-03 - 11:25:42
# comments:              Changed 'the_current_project' to 'the_current_projekt'
# -------------------------------------------------------------------------- #
# version:               0.0.4
# modified:              2024-05-03 - 11:38:31
# comments:              Standardizd 'logik-projekt' menu entries
# -------------------------------------------------------------------------- #
# version:               0.0.5
# modified:              2024-05-03 - 12:29:29
# comments:              Restored '_{version_name}' in script construction
# -------------------------------------------------------------------------- #
# version:               0.0.6
# modified:              2024-05-03 - 13:37:01
# comments:              Added validation for file existence
# -------------------------------------------------------------------------- #
# version:               1.0.0
# modified:              2024-05-06 - 14:35:57
# comments:              Complete re-write - tested on Lucid Link
# -------------------------------------------------------------------------- #
# version:               1.0.1
# modified:              2024-05-06 - 16:12:00
# comments:              Minor reformatting
# -------------------------------------------------------------------------- #
# version:               1.0.2
# modified:              2024-05-06 - 16:24:36
# comments:              added printf statements at logging.debug points
# -------------------------------------------------------------------------- #
# version:               1.0.3
# modified:              2024-05-06 - 17:02:53
# comments:              Added (*args, **kwargs) to main function
# -------------------------------------------------------------------------- #
# version:               1.0.4
# modified:              2024-05-06 - 21:50:39
# comments:              Updated docstrings, comments and formatting
# -------------------------------------------------------------------------- #
# version:               1.0.5
# modified:              2024-05-06 - 22:14:47
# comments:              Corrected Write node file path for Nuke Shot script.
# -------------------------------------------------------------------------- #
# version:               1.0.6
# modified:              2024-05-10 - 09:39:33
# comments:              Enabled production job_dir and disabled test job_dir
# -------------------------------------------------------------------------- #
# version:               2.0.0
# modified:              2024-05-10 - 21:14:44
# comments:              Refactored monolithic code and tested in flame 2025
# -------------------------------------------------------------------------- #
# version:               2.0.1
# modified:              2024-05-10 - 21:45:10
# comments:              Modified docstrings and formatting.
# -------------------------------------------------------------------------- #
# version:               2.0.2
# modified:              2024-05-14 - 12:53:36
# comments:              Renamed 'classes_and_functions' directory to 'modules'.
# -------------------------------------------------------------------------- #
# version:               2.1.2
# modified:              2024-05-15 - 12:35:57
# comments:              Renamed nuke script functions and started blender tools.
# -------------------------------------------------------------------------- #
# version:               2.2.2
# modified:              2024-05-18 - 18:00:56
# comments:              Added GNU GPLv3 Disclaimer.
# -------------------------------------------------------------------------- #
# version:               2.2.3
# modified:              2024-05-18 - 18:46:27
# comments:              Minor modification to Disclaimer.
# -------------------------------------------------------------------------- #
# version:               2.2.4
# modified:              2024-06-08 - 08:47:53
# comments:              Removed unused code and prep for after effects scripts.
# -------------------------------------------------------------------------- #
# version:               2.2.5
# modified:              2024-06-09 - 11:27:00
# comments:              Added After Effects script/openclip generators
# -------------------------------------------------------------------------- #
# version:               2.2.6
# modified:              2024-06-10 - 06:59:38
# comments:              Removed some double quotes from After Effects templates
# -------------------------------------------------------------------------- #
# version:               2.2.7
# modified:              2024-08-31 - 19:04:02
# comments:              prep for release.
# -------------------------------------------------------------------------- #
