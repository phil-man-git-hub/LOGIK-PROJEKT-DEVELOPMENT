################################################################################
#
# Filename: clean_batch_iteration.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
This script adds a Clean Batch Iterations custom action to different Media Panel
objects. When selelected, the content of a Batch Group's Iterations folder
is emptied.
"""


def get_media_panel_custom_ui_actions():
    def scope_desktop(selection):
        import flame

        for item in selection:
            if isinstance(item, (flame.PyDesktop)):
                return True
        return False

    def scope_batch_group(selection):
        import flame

        for item in selection:
            if isinstance(item, (flame.PyBatch)):
                return True
        return False

    def scope_library(selection):
        import flame

        for item in selection:
            if isinstance(item, (flame.PyLibrary)):
                return True
        return False

    def scope_folder(selection):
        import flame

        for item in selection:
            if isinstance(item, (flame.PyFolder)):
                return True
        return False

    def clean_desktop(selection):
        import flame

        workspace = flame.projects.current_project.current_workspace
        for batch_group in workspace.desktop.batch_groups:
            workspace.desktop.current_batch_group = batch_group
            for iteration in batch_group.batch_iterations:
                flame.delete(iteration, confirm=False)

    def clean_batch_group(selection):
        import flame

        for batch_group in selection:
            for iteration in batch_group.batch_iterations:
                flame.delete(iteration, confirm=False)

    def find_batch_group(folder):
        """
        Function to recursively find Batch Groups inside folders and libraries
        and delete all their iterations.
        """
        import flame

        for batch_group in folder.batch_groups:
            for iteration in batch_group.batch_iterations:
                flame.delete(iteration, confirm=False)
        for folders in folder.folders:
            find_batch_group(folders)

    def clean_library(selection):
        for top_library in selection:
            find_batch_group(top_library)

    def clean_folder(selection):
        for top_folder in selection:
            find_batch_group(top_folder)

    return [
        {
            "name": "Examples / Batch",
            "actions": [
                {
                    "name": "Clean Batch Iterations",
                    "isVisible": scope_desktop,
                    "execute": clean_desktop,
                    "minimumVersion": "2020.1",
                }
            ],
        },
        {
            "name": "Examples / Batch",
            "actions": [
                {
                    "name": "Clean Batch Iterations",
                    "isVisible": scope_batch_group,
                    "execute": clean_batch_group,
                }
            ],
        },
        {
            "name": "Examples / Batch",
            "actions": [
                {
                    "name": "Clean Batch Iterations",
                    "isVisible": scope_library,
                    "execute": clean_library,
                }
            ],
        },
        {
            "name": "Examples / Batch",
            "actions": [
                {
                    "name": "Clean Batch Iterations",
                    "isVisible": scope_folder,
                    "execute": clean_folder,
                }
            ],
        },
    ]
