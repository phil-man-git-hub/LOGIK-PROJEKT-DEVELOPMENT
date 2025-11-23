################################################################################
#
# Filename: import_using_qt_file_dialog.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
This script shows how a clip can be imported in Batch Group using a Qt File Dialog
or a Flame Browser through a custom action scoped to the Batch Schematic background.

You can modify the default path and destination of flame.batch.import_clip to your liking.
"""


def get_batch_custom_ui_actions():
    """
    Used to make a custom action Visible or Enabled to the Batch Schematic
    background.
    """

    def scope_background(selection):
        return len(selection) == 0

    def import_qt(selection):
        import flame
        import os
        from PySide6 import QtWidgets

        dlg = QtWidgets.QFileDialog()
        init_dir = os.path.expanduser("~")
        dlg.setDirectory(init_dir)
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        selected_files = []
        if dlg.exec():
            selected_files = dlg.selectedFiles()

        for selected_file in selected_files:
            path = selected_file.encode("utf-8")
            flame.batch.import_clip(path, flame.batch.reels[0].name.get_value())

    def import_flame_browser(selection):
        import flame

        flame.browser.show(
            title="Select Clips", extension="", default_path="/", multi_selection=True
        )

        flame.batch.import_clips(
            flame.browser.selection, flame.batch.reels[0].name.get_value()
        )

    return [
        {
            "name": "Examples / Dialog",
            "actions": [
                {
                    "name": "Import File using a Qt File Dialog",
                    "is_enabled": scope_background,
                    "execute": import_qt,
                },
                {
                    "name": "Import File using a Flame Browser",
                    "is_enabled": scope_background,
                    "execute": import_flame_browser,
                },
            ],
        }
    ]
