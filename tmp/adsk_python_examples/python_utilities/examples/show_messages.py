################################################################################
#
# Filename: messsages.py
#
# Copyright (c) 2022 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Examples of messages presented to the user in the message bar/console or a dialog box via a custom action.
"""


def countdown(selection):
    """
    Show a countdown within the message bar/console.
    """

    import flame
    import time

    for i in reversed(range(0, 10)):
        flame.messages.show_in_console("%d" % i, "info", 1)
        time.sleep(1)


def freespace(selection):
    """
    Show the current free space on / within the message bar/console.
    """

    import flame
    import shutil

    total, used, free = shutil.disk_usage("/")
    if free < 100000:
        flame.messages.show_in_console(
            "Total: %d, Used %d, Free %d" % (total, used, free), "warning", 10
        )
    else:
        flame.messages.show_in_console(
            "Total: %d, Used %d, Free %d" % (total, used, free), "info", 10
        )


def set_batch_duration(selection):
    """
    Display an error message inside a dialog box if no clip node is found in Batch.
    Test this in a Batch Group that doesn't have a clip node in it.
    """

    import flame

    batch_group = flame.batch

    clip = None
    for node in batch_group.nodes:
        if node.type == "Clip":
            clip = node
            break

    try:
        batch_group.duration = clip.duration

    except:
        dialog = flame.messages.show_in_dialog(
            title="No Clip Found",
            message="The Batch Group duration cannot be set because there is no clip in this Schematic",
            type="error",
            buttons=["Close"],
        )

        if dialog == "Close":
            pass


def get_main_menu_custom_ui_actions():
    return [
        {
            "name": "Examples / Messages",
            "actions": [
                {
                    "name": "Countdown",
                    "execute": countdown,
                },
                {
                    "name": "Freespace",
                    "execute": freespace,
                },
            ],
        }
    ]


def get_batch_custom_ui_actions():
    return [
        {
            "name": "Examples / Messages",
            "actions": [
                {
                    "name": "Set Batch Duration based on Clip",
                    "execute": set_batch_duration,
                }
            ],
        }
    ]


get_main_menu_custom_ui_actions.minimum_version = "2023.1"
get_batch_custom_ui_actions.minimum_version = "2023.1"
