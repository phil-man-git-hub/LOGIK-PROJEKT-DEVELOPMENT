################################################################################
#
# Filename: post_export_asset_using_snapshot.py
#
# Copyright (c) 2025 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Flame provides a post_export_asset Python hook used to trigger operations after
the media export has completed. 

This hook contains multiple keys in its dictionary, including an isSnapshot boolean
used to scope the hook to an Export Snapshot operation, excluding other media export operations.

The following example demonstrates how to automatically re-import a Snapshot made in the
Player into the Desktop.
"""

def post_export_asset(info, userData, *args, **kwargs):
    import flame
    import os

    # Apply the hook only when in the Timeline environment.
    if flame.get_current_tab() == "Timeline":

    # Apply the hook only when an Export Snapshot is performed.
        if info["isSnapshot"]:

            # Define the first reel of the first reel group in the Desktop as the destination.
            reel = flame.projects.current_project.current_workspace.desktop.reel_groups[0].reels[0]

            # Use the "destinationPath" and "resolvedPath" keys to get the complete file path
            # of the exported Snapshot
            clip = os.path.join(info["destinationPath"],info["resolvedPath"])

            # Import the exported Shapshot.
            flame.import_clips(clip, reel)
