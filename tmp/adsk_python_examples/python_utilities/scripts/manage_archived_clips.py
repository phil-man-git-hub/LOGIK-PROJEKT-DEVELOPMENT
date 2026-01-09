################################################################################
#
# Filename: managed_archived_clips.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of a custom action that removes archived clip from a clip selection.
"""


def have_at_least_one_clip_in_selection(selection):
    """
    Returns True if the passed selection contains at least one clip object.
    """
    import flame

    for item in selection:
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            return True
    return False


def have_at_least_one_clip_archived_in_selection(selection):
    """
    Returns True if the passed selection contains at least one clip object that
    has been already archived.
    """
    import flame

    for item in selection:
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            if item.archive_date or item.archive_error:
                return True
    return False


def colour_based_on_archive_status(selection):
    """
    Set Archived clips to green but set clips Archived with error to red.
    """
    import flame

    for item in selection:
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            if item.archive_error:
                item.colour = (1.0, 0.0, 0.0)
            elif item.archive_date:
                item.colour = (0.0, 1.0, 0.0)


def remove_archived_clips(selection):
    """
    Remove all archived clips contained in selection.
    """
    import flame

    for item in selection:
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            if item.archive_date and not item.archive_error:
                flame.delete(item)


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Examples / Manage Archived Clips",
            "actions": [
                {
                    "name": "Apply Colour based on archive status",
                    "isEnabled": have_at_least_one_clip_archived_in_selection,
                    "isVisible": have_at_least_one_clip_in_selection,
                    "execute": colour_based_on_archive_status,
                },
                {
                    "name": "Remove Archived Clips",
                    "isEnabled": have_at_least_one_clip_archived_in_selection,
                    "isVisible": have_at_least_one_clip_in_selection,
                    "execute": remove_archived_clips,
                },
            ],
        }
    ]


def get_main_menu_custom_ui_actions():
    return get_media_panel_custom_ui_actions()
