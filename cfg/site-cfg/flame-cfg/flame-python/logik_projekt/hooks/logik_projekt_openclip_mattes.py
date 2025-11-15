#!/usr/bin/env python3
# -------------------------------------------------------------------------- #
# Filename:     logik_projekt_openclip_mattes.py
# Purpose:      Create OpenClip for LOGIK-PROJEKT mattes clips.
# Description:  Uses LOGIK-PROJEKT OpenClip core module to create OpenClips
# Author:       phil_man@mac.com
# Copyright:    Copyright (c) 2025
# Disclaimer:   Disclaimer at bottom of script.
# License:      GNU General Public License v3.0 (GPL-3.0).
#               https://www.gnu.org/licenses/gpl-3.0.en.html

# Version:      2027.0.0
# Status:       Development
# Type:         Application
# Created:      2025-07-01
# Modified:     2025-11-15

# Changelog:    Changelog at bottom of script.
# -------------------------------------------------------------------------- #

# -------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------- #

# Standard library imports
import os
import sys

# Ensure the parent directory of 'src' is in sys.path for canonical imports
current_file = os.path.abspath(__file__)
src_parent = os.path.dirname(os.path.dirname(current_file))
if src_parent not in sys.path:
    sys.path.insert(0, src_parent)

# Import the relevant OpenClip classes from the core module
from src.core.logik_projekt_openclip import (
    LogikProjektOpenClipComp,         # For comp hook
    LogikProjektOpenClipMattes,       # For mattes hook
    LogikProjektOpenClipMultichannel, # For multichannel hook
    LogikProjektOpenClipNeatVideo,    # For neat video hook
    LogikProjektOpenClipPrecomp       # For precomp hook
)

# -------------------------------------------------------------------------- #
# Configuration
# -------------------------------------------------------------------------- #

# Get the config directory relative to this script
cfg_dir = os.path.join(
    os.path.dirname(current_file),
    '../cfg/logik_projekt_openclip_mattes'
)
cfg_file = 'config.xml'
config_path = os.path.join(cfg_dir, cfg_file)

# # Define config path relative to this hook file
# config_path = os.path.join(os.path.dirname(__file__), '../cfg/logik_projekt_openclip_mattes/config.xml')

# -------------------------------------------------------------------------- #
# Functions
# -------------------------------------------------------------------------- #

def projekt_mattes_media_panel_clips(selection):
    script = LogikProjektOpenClipMattes(selection)
    script.media_panel_projekt_clips()

# -------------------------------------------------------------------------- #

def projekt_mattes_batch_clips(selection):
    script = LogikProjektOpenClipMattes(selection)
    script.batch_projekt_clips()

# -------------------------------------------------------------------------- #

def setup(selection):
    script = LogikProjektOpenClipMattes(selection)
    script.output_node_setup()

# -------------------------------------------------------------------------- #
# Scopes
# -------------------------------------------------------------------------- #

def scope_clip(selection):
    import flame
    for item in selection:
        if isinstance(item, (flame.PyClip, flame.PyClipNode)):
            return True
    return False

# -------------------------------------------------------------------------- #
# Flame Menus
# -------------------------------------------------------------------------- #

def get_batch_custom_ui_actions():
    return [
        {
            'name': 'logik-projekt',
            'hierarchy': [],
            'actions': []
        },
        {
            'name': 'create-openclip',
            'hierarchy': ['logik-projekt'],
            'order': 2,
            'actions': [
                {
                    'name': 'projekt_mattes selected clips',
                    'order': 2,
                    'separator': 'below',
                    'isVisible': scope_clip,
                    'execute': projekt_mattes_batch_clips,
                    'minimumVersion': '2025'
                }
            ]
        }
    ]

# -------------------------------------------------------------------------- #

def get_main_menu_custom_ui_actions():
    return [
        {
            'name': 'logik-projekt',
            'hierarchy': [],
            'actions': []
        },
        {
            'name': 'create-openclip',
            'hierarchy': ['logik-projekt'],
            'order': 2,
            'actions': [
                {
                    'name': 'configure projekt_mattes',
                    'execute': setup,
                    'minimumVersion': '2025'
                }
           ]
        }
    ]

# -------------------------------------------------------------------------- #

def get_media_panel_custom_ui_actions():
    return [
        {
            'name': 'logik-projekt',
            'hierarchy': [],
            'actions': []
        },
        {
            'name': 'create-openclip',
            'hierarchy': ['logik-projekt'],
            'order': 2,
            'actions': [
                {
                    'name': 'projekt_mattes selected clips',
                    'order': 2,
                    'separator': 'below',
                    'isVisible': scope_clip,
                    'execute': projekt_mattes_media_panel_clips,
                    'minimumVersion': '2025'
                }
            ]
        }
    ]


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
