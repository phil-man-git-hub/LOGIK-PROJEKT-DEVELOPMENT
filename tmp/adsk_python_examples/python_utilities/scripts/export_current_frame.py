##############################################################################
#
# Filename: export_current_frame.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of a custom action that exports the current frame of each selected
clips in a selection.
"""

import datetime
import os


def get_export_root():
    """
    Use the current location of the MediaHub Files tab if possible or /var/tmp
    if MediaHub File tab is not a valid location.

    The flame.mediahub module was added in Flame 2021.2 Update.
    """
    try:
        import flame

        path = flame.mediahub.files.get_path()
    except NameError:
        path = None
    return path if path else "/var/tmp"


def export_current_frame(clip):
    """
    Export the current frame of the clip using a pre-defined preset.
    """

    import flame

    # Build the presets path.
    #
    # By using flame.PyExporter.get_presets_dir(), we don't need to know where
    # the application stores its presets. Or we could also use any path that
    # leads to a Flame export preset file.
    #
    # Possible visibilities are:
    #   Autodesk:   Factory presets shipped with the application.
    #   Shared:     Shared presets for all applications (/opt/Autodesk/shared).
    #   Project:    Project specific presets.
    #   User:       User specific presets.
    #
    # Possible presets types are:
    #   Movie:              Movie files (typically QuickTime & MXF)
    #   Image_Sequence:     Image sequences (Jpeg, Dpx, Exr)
    #   Audio:              Audio files (wav)
    #   Sequence_Publish:   Complex sequence/timeline export (AAF, FCP X/7, EDL)
    #
    preset_dir = flame.PyExporter.get_presets_dir(
        flame.PyExporter.PresetVisibility.Autodesk,
        flame.PyExporter.PresetType.Image_Sequence,
    )
    preset_path = os.path.join(preset_dir, "Jpeg", "Jpeg (8-bit).xml")

    # Initialize the exporter instance we will use to do the export.
    #
    exporter = flame.PyExporter()

    # Set the exporter to use foreground export. By default it will send a
    # job to Backburner to do the export.
    #
    exporter.foreground = True

    # We will use marks to export only the current frame by duplicating the
    # clip and overriding the marks with the current time.
    #
    exporter.export_between_marks = True

    # Duplicate the clip to avoid modifying the clip itself.
    #
    duplicate_clip = flame.duplicate(clip)
    try:
        # Give the duplicate clip an unique name. We assume here that the preset
        # we will use have <name> in the destination path.
        #
        duplicate_clip.name = clip.name + datetime.datetime.now().strftime(
            "%Y_%m_%d__%H_%M_%S"
        )

        # Set in mark to current_time and out_mark at current_time + 1 so
        # only the current frame is exported
        #
        duplicate_clip.in_mark = clip.current_time.get_value()
        duplicate_clip.out_mark = clip.current_time.get_value() + 1

        exporter.export(duplicate_clip, preset_path, get_export_root())

    finally:
        # Be sure to clean up duplicated clip in case of error during the export
        #
        flame.delete(duplicate_clip)


def export_selection(selection):
    """
    Export the current frame of each clips in the selection using a
    pre-defined preset.
    """

    import flame

    # Iterate the selection.
    #
    for item in selection:

        # Check if the item in the selection is a sequence or a clip.
        #
        if isinstance(item, (flame.PySequence, flame.PyClip)):
            export_current_frame(item)


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Examples / Export",
            "actions": [
                {
                    "name": "Export Current Frame",
                    "execute": export_selection,
                },
            ],
        }
    ]


def get_main_menu_custom_ui_actions():
    return get_media_panel_custom_ui_actions()
