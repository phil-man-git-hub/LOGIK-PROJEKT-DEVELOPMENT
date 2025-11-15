#
# -------------------------------------------------------------------------- #

# DISCLAIMER:       This file is part of LOGIK-PROJEKT.
#                   Copyright © 2024 man-made-mekanyzms
              
#                   LOGIK-PROJEKT is free software.
#                   Contact: phil_man@mac.com

# -------------------------------------------------------------------------- #

# File Name:        logik_projekt_openclip_multichannel.py
# Version:          2.0.1
# Modified:         2025-11-14

import os
import sys


import os
import sys
current_file = os.path.abspath(__file__)
src_parent = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
if src_parent not in sys.path:
	sys.path.insert(0, src_parent)
# Define script_dir for path logic
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the script's directory to the Python path to allow absolute imports
config_path = os.path.join(os.path.dirname(__file__), '../cfg/logik_projekt_openclip_multichannel/config.xml')
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from src.core.logik_projekt_openclip import LogikProjektOpenClipMultichannel

# -------------------------------------------------------------------------- #

def projekt_multichannel_media_panel_clips(selection):
    script = LogikProjektOpenClipMultichannel(selection)
    script.media_panel_projekt_clips()

# -------------------------------------------------------------------------- #

def projekt_multichannel_batch_clips(selection):
    script = LogikProjektOpenClipMultichannel(selection)
    script.batch_projekt_clips()

# -------------------------------------------------------------------------- #

def setup(selection):
    script = LogikProjektOpenClipMultichannel(selection)
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
            'order': 1,
            'actions': [
                {
                    'name': 'projekt_multichannel selected clips',
                    'order': 1,
                    'separator': 'below',
                    'isVisible': scope_clip,
                    'execute': projekt_multichannel_batch_clips,
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
            'order': 1,
            'actions': [
                {
                    'name': 'configure projekt_multichannel',
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
            'order': 1,
            'actions': [
                {
                    'name': 'projekt_multichannel selected clips',
                    'order': 1,
                    'separator': 'below',
                    'isVisible': scope_clip,
                    'execute': projekt_multichannel_media_panel_clips,
                    'minimumVersion': '2025'
                }
            ]
        }
    ]