################################################################################
#
# Filename: custom_actions_hook.py
#
# Copyright (c) 2018 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

# Hook returning the custom ui actions to display to the user in the
# contextual menu.
#
#   Returns a tuple of group dictionaries.
#
#   A group dictionary defines a custom menu group where keys defines
#   the group.
#
#   Keys:
#
#       name: [String]
#           Name of the action group that will be created in the menu.
#
#       actions: [Tuple]
#           Tuple of action dictionary which menu items will be created
#           in the group.
#
#   An action dictionary where the keys define the action attributes
#
#   Keys:
#
#       name: [String]
#           Name of the action. Will also be used as the caption
#           if no caption is defined.
#
#       caption: [String] [Optional]
#           Caption of the menu item. Defaults to name if not defined.
#
#       isEnabled: [Boolean/Callable] [Optional]
#           Boolean or callable object that can be used to enable/disable an
#           action. True is assumed if not defined. The callback object takes
#           one parameter which is a tuple of selected Flame objects.
#
#       isVisible: [Boolean/Callable] [Optional]
#           Boolean or callable object that can be used to show/hide an action.
#           True is assumed if not defined. The callback object takes one
#           parameter which is a tuple of selected Flame objects.
#
#       execute: [Callable] [Optional]
#           Action to execute upon selection. The callback object takes one
#           parameter which is a tuple of selected Flame objects.
#
#       minimumVersion [String] [Optional]
#           Minimum application version (inclusive) that can use that action.
#           If application is older, the action will not be visible.
#
#       maximumVersion [String] [Optional]
#           Maximum application version (inclusive) that can use that action.
#           If application is newer, the action will not be visible.
#
#   For example: 2 menu groups: one with 1 custom action, the other with 2
#                custom actions.
#
#   def get_media_panel_custom_ui_actions():
#       def execute_action_1(selection):
#           pass
#
#       def execute_action_2(selection):
#           pass
#
#       def execute_action_3(selection):
#           pass
#
#       action_1 = {}
#       action_1["name"] = "Action Number 1"
#       action_1["execute"] = execute_action_1
#
#       group_1 = {}
#       group_1["name"] = "Custom Group 1"
#       group_1["actions"] = [action_1]
#
#       action_2 = {}
#       action_2["name"] = "Action Number 2"
#       action_2["execute"] = execute_action_2
#
#       action_3 = {}
#       action_3["name"] = "Action Number 3"
#       action_3["execute"] = execute_action_3
#
#       group_2 = {}
#       group_2["name"] = "Custom Group 2"
#       group_2["actions"] = [action_2, action_3]
#
#       return [group_1, group_2]
#
#   This could also be written as the following
#
#   def get_media_panel_custom_ui_actions():
#       def action_1(selection):
#           pass
#
#       def action_2(selection):
#           pass
#
#       def action_3(selection):
#           pass
#
#       return [
#            {
#               "name": "Custom Group 1",
#               "actions": [
#                   {
#                       "name": "Action Number 1",
#                       "execute": action_1
#                   }
#               ]
#           },
#           {
#               "name": "Custom Group 2",
#               "actions": [
#                   {
#                       "name": "Action Number 2",
#                       "execute": action_2
#                   },
#                   {
#                       "name": "Action Number 3",
#                       "execute": action_3
#                   }
#               ]
#           }
#       ]
#
def get_media_panel_custom_ui_actions():
    pass


# Hook returning the custom ui actions to display to the user in the
# flame main menu.
#
#   Returns a tuple of group dictionaries.
#
#   A group dictionary defines a custom menu group where keys defines
#   the group.
#
# Same Documentation as get_media_panel_custom_ui_actions() above
#
def get_main_menu_custom_ui_actions():
    pass


# Hook returning the custom ui actions to display to the user in the
# MediaHub Files menu.
#
#   Returns a tuple of group dictionaries.
#
#   A group dictionary defines a custom menu group where keys defines
#   the group.
#
# Same Documentation as get_media_panel_custom_ui_actions() above
#
def get_mediahub_files_custom_ui_actions():
    pass


# Hook returning the custom ui actions to display to the user in the
# MediaHub Projects menu.
#
#   Returns a tuple of group dictionaries.
#
#   A group dictionary defines a custom menu group where keys defines
#   the group.
#
# Same Documentation as get_media_panel_custom_ui_actions() above
#
def get_mediahub_projects_custom_ui_actions():
    pass


# Hook returning the custom ui actions to display to the user in the
# MediaHub Archives.
#
#   Returns a tuple of group dictionaries.
#
#   A group dictionary defines a custom menu group where keys defines
#   the group.
#
# Same Documentation as get_media_panel_custom_ui_actions() above
#
def get_mediahub_archives_custom_ui_actions():
    pass


# Hook returning the custom ui actions to display to the user in the
# Timeline contextual menus.
#
#   Returns a tuple of group dictionaries.
#
#   A group dictionary defines a custom menu group where keys defines
#   the group.
#
# Same Documentation as get_media_panel_custom_ui_actions() above
#
def get_timeline_custom_ui_actions():
    pass


# Hook returning the custom ui actions to display to the user in the
# Batch Menu.
#
#   Returns a tuple of group dictionaries.
#
#   A group dictionary defines a custom menu group where keys defines
#   the group.
#
# Same Documentation as get_media_panel_custom_ui_actions() above
#
def get_batch_custom_ui_actions():
    pass


# Hook returning the custom ui actions to display to the user in the
# Action Menu.
#
#   Returns a tuple of group dictionaries.
#
#   A group dictionary defines a custom menu group where keys defines
#   the group.
#
# Same Documentation as get_media_panel_custom_ui_actions() above
#
def get_action_custom_ui_actions():
    pass
