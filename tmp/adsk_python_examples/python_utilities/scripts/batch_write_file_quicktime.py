################################################################################
#
# Filename: batch_write_file_quicktime.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of a hook that transcodes exported media from a Batch Write File node
to a Quicktime file as a post export process.
"""

import os


def batch_export_end(info, userData, *args, **kwargs):
    import flame

    # Build the path of the exported media
    #
    full_path = os.path.join(info["exportPath"], info["resolvedPath"])
    clips = flame.import_clips(full_path)

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
        flame.PyExporter.PresetVisibility.Autodesk, flame.PyExporter.PresetType.Movie
    )
    preset_path = os.path.join(
        preset_dir, "QuickTime", "QuickTime (8-bit Uncompressed).xml"
    )

    # Initialize the exporter instance we will use to do the export.
    #
    exporter = flame.PyExporter()

    # Set the exporter to use foreground export. By default it will send a
    # job to backburner to do the export.
    #
    exporter.foreground = True

    # Do the actual export.
    #
    exporter.export(clips, preset_path, output_directory=info["exportPath"])
