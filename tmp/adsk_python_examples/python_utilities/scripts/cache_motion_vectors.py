################################################################################
#
# Filename: cache_motion_vectors.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
This script creates a Motion Vectors Maps for a Clip node located in the
Batch Schematic.
An Action node is connected to the clip and the Motion Vectors map is
created and cached.

The same can be done from the Desktop object in the Media Panel.
This version opens message dialog allowing you to select a clip.
A new Batch Group is created for the clip & the same recipe as the Batch version
above is applied.
"""


def get_batch_custom_ui_actions():
    def scope_node(selection):
        """Make the Custom Action available on a Batch Clip node only"""

        import flame

        for item in selection:
            if isinstance(item, flame.PyNode):
                if item.type == "Clip":
                    return True
        return False

    def create_motion(selection):
        """Create an Action node and a Motion Vectors Map"""

        import flame

        clip = flame.batch.current_node.get_value()
        action = flame.batch.create_node("Action")
        pos_x = clip.pos_x
        pos_y = clip.pos_y
        action.pos_x = pos_x + 400
        action.pos_y = pos_y
        media = action.add_media()
        media.pos_x = pos_x + 200
        media.pos_y = pos_y

        flame.batch.connect_nodes(clip, "Default", media, "Default")

        motion_map = action.create_node("Motion Vectors Map")

        start = flame.batch.start_frame.get_value()
        end = start + clip.duration.get_value()

        motion_map.cache_range(start, end)

    return [
        {
            "name": "Examples / Batch",
            "actions": [
                {
                    "name": "Cache Motion Vectors Map",
                    "isVisible": scope_node,
                    "execute": create_motion,
                }
            ],
        }
    ]


def get_media_panel_custom_ui_actions():
    def scope_desktop(selection):
        """Make the Custom Action available on the Desktop entry only"""

        import flame

        for item in selection:
            if isinstance(item, flame.PyDesktop):
                return True
        return False

    def create_batch_motion(selection):
        import flame

        flame.go_to("Batch")

        """Open a Flame browser so clips can be selected by the user"""
        flame.browser.show(
            title="Select Clip(s)",
            extension="",
            default_path="/",
            multi_selection=False,
        )

        """Create an Action node and a Motion Vectors Map for all selected clips"""
        for file in flame.browser.selection:
            back = flame.batch.create_batch_group("MyNewBatch")

            clip = back.import_clip(
                file.encode("utf-8"), flame.batch.reels[0].name.get_value()
            )

            back.duration = clip.duration
            back.name = clip.name
            back.expanded = False

            action = flame.batch.create_node("Action")
            pos_x = clip.pos_x
            pos_y = clip.pos_y
            action.pos_x = pos_x + 400
            action.pos_y = pos_y
            media = action.add_media()
            media.pos_x = pos_x + 200
            media.pos_y = pos_y

            flame.batch.connect_nodes(clip, "Default", media, "Default")

            motion_map = action.create_node("Motion Vectors Map")

            start = flame.batch.start_frame.get_value()
            end = start + clip.duration.get_value()

            motion_map.cache_range(start, end)

    return [
        {
            "name": "Examples / Batch",
            "actions": [
                {
                    "name": "Create Batch and Cache Motion Vectors Map",
                    "isVisible": scope_desktop,
                    "execute": create_batch_motion,
                }
            ],
        }
    ]
