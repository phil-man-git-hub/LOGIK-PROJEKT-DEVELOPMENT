#
# -------------------------------------------------------------------------- #

# DISCLAIMER:       This file is part of LOGIK-PROJEKT.
#                   Copyright © 2024 man-made-mekanyzms
              
#                   LOGIK-PROJEKT is free software.
#                   Contact: phil_man@mac.com

# -------------------------------------------------------------------------- #

# File Name:        logik_projekt_openclip_comp.py
# Version:          2.0.1
# Modified:         2025-11-14

import os
import sys

# Add the script's directory to the Python path to allow absolute imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from logik_projekt_openclip import LogikProjektOpenClipComp

# -------------------------------------------------------------------------- #

def projekt_comp_media_panel_clips(selection):
    script = LogikProjektOpenClipComp(selection)
    script.media_panel_projekt_clips()

# -------------------------------------------------------------------------- #

def projekt_comp_batch_clips(selection):
    script = LogikProjektOpenClipComp(selection)
    script.batch_projekt_clips()

# -------------------------------------------------------------------------- #

def setup(selection):
    script = LogikProjektOpenClipComp(selection)
    script.output_node_setup()

# -------------------------------------------------------------------------- #

# Scopes

def scope_clip(selection):
    import flame
    for item in selection:
        if isinstance(item, (flame.PyClip, flame.PyClipNode)):
            return True
    return False

# -------------------------------------------------------------------------- #

# Flame Menus

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
            'order': 0,
            'actions': [
                {
                    'name': 'projekt_comp selected clips',
                    'order': 0,
                    'separator': 'below',
                    'isVisible': scope_clip,
                    'execute': projekt_comp_batch_clips,
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
            'order': 0,
            'actions': [
                {
                    'name': 'configure projekt_comp',
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
            'order': 0,
            'actions': [
                {
                    'name': 'projekt_comp selected clips',
                    'order': 0,
                    'separator': 'below',
                    'isVisible': scope_clip,
                    'execute': projekt_comp_media_panel_clips,
                    'minimumVersion': '2025'
                }
            ]
        }
    ]