################################################################################
#
# Filename: wait_cursor.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of a python hook overriding the default wait cursor while running
so the user can use another GUI.
"""

from __future__ import print_function

import time

from PySide6.QtWidgets import QMessageBox


def show_dialog(text, title):
    """
    Show a dialog box using PySide/QT.
    """
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setDefaultButton(QMessageBox.Ok)
    msg_box.exec()


def show_selection_dialog(selection):
    """
    Display a dialog showing the selection in the media panel.
    """
    show_dialog(text=str(selection), title="This is the selection")


def sleep_a_while(selection):
    """
    Sleep 10 seconds
    """

    print("Starting long process")
    time.sleep(10)
    print("Finished long process")


def get_media_panel_custom_ui_actions():
    """
    Return custom UI actions to execute on media panel objects.
    """

    return [
        {
            "name": "Examples / Wait Cursor",
            "actions": [
                {
                    "name": "Show selection dialog",
                    "execute": show_selection_dialog,
                    #
                    # Since this action require user input, we want to
                    # show the normal cursor for the duration of the action.
                    #
                    "waitCursor": False,
                },
                {
                    "name": "Sleep 10 seconds",
                    "execute": sleep_a_while,
                    #
                    # Since this action is long we want to display
                    # the way cursor (This is the default behavior).
                    #
                    "waitCursor": True,
                },
            ],
        }
    ]


def render_ended(module_name, sequence_name, elapsed_time_in_seconds):
    """
    Display a dialog showing the statistics of the rendered sequence.
    """

    show_dialog(
        text="Rendered %s in %s seconds" % (sequence_name, elapsed_time_in_seconds),
        title="Render in %s" % module_name,
    )


# Since this action require user input, we want to show the normal cursor for
# the duration of the hook.
#
render_ended.wait_cursor = False
