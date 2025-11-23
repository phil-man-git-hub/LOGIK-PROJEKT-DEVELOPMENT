################################################################################
#
# Filename: custom_action_object.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of how custom actions can be any callable python object.
"""


# The following example uses a callable object to tie the action name to the
# action callback so the same method can be specialized based on the action name.
#
def action_on_selection(action_id, selection):
    print("action_on_selection %s with %s" % (action_id, selection))


def get_media_panel_custom_ui_actions():
    action_ids = ["Action1", "Action2", "Action3", "Action4"]
    actions = {"name": "Examples / Custom Action Object", "actions": []}

    for action_id in action_ids:

        class Action(object):
            def __init__(self, action_id):
                self._action_id = action_id

            def __call__(self, selection):
                return action_on_selection(self._action_id, selection)

        actions["actions"].append({"name": action_id, "execute": Action(action_id)})

    return actions
