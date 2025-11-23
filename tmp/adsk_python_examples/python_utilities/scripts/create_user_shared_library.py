################################################################################
#
# Filename: create_user_shared_library.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of how a python hook can be used to fetch the current user and used
in custom actions later on.
"""

from __future__ import print_function


def create_user_shared_library(selection):
    """
    Create a shared library based on the current user name
    """

    import flame

    user_name = flame.users.current_user.name
    flame.projects.current_project.create_shared_library(user_name)


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Examples / Create User Shared Library",
            "actions": [
                {
                    "name": "Create User Shared Library",
                    "execute": create_user_shared_library,
                    "minimumVersion": "2020.1",
                }
            ],
        }
    ]
