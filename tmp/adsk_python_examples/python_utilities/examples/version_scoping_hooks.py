################################################################################
#
# Filename: version_scoping_hooks.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Examples of how custom actions can be limited to appear in some software
versions only.
"""

from __future__ import print_function

# It is possible to define a minimum and/or maximum supported version of Flame.
# Both of these values are inclusive.

# There are 2 levels of scoping: hook and function.
# For the hook scoping, you can define a dictionary attribute minimumVersion and/or maximumVersion.
# For the function scoping, you add minimum_version and/or maximum_version
# to the function after defining it.
# Function scoping will not allow a hook to load while hook scoping will merely hide it.
# This means that you can't override a function scoping that is too narrow for your version with
# a broader hook scoping. However, the reverse is possible.

# The supported version formats are as follows (elements in square brackets are optional):
# MajorVersion[.MinorVersion][.PatchVersion]. IE: 2020.0.1, 2019.2 or 2012
# If a version group is ignored, then anything in the following group will pass.
# So, if you specify 2020.0, any patch version within 2020.0 will work.

# Here are some examples in action.

# Let's first define some hooks


def print_selection(selection):
    """
    General action that prints the tupple containing the selection
    """
    print(selection)


def get_action_custom_ui_actions():
    """
    Defines hooks that will appear in the action contextual menu.
    Returns a hook that will be displayed between version 2019.2.1.5
    and anything within 2021
    """
    return [
        {
            "name": "Examples / Version Scoping",
            "actions": [
                {
                    "name": "Print Selection",
                    "execute": print_selection,
                    "minimumVersion": "2018.2.1.5",
                    "maximumVersion": "2021",
                }
            ],
        }
    ]


def get_batch_custom_ui_actions():
    """
    Defines hooks that will appear in the batch contextual menu
    Returns a hook that will be displayed for any version above or equal to 2018.2.1
    """
    return [
        {
            "name": "Examples / Version Scoping",
            "actions": [
                {
                    "name": "Print Selection",
                    "execute": print_selection,
                    "minimumVersion": "2018.2.1",
                }
            ],
        }
    ]


def get_timeline_custom_ui_actions():
    """
    Defines hooks that will appear in the timeline contextual menu
    Returns a hook that will be displayed for any version
    up to 2021.2 and any of its patches
    """
    return [
        {
            "name": "Examples / Version Scoping",
            "actions": [
                {
                    "name": "Print Selection",
                    "execute": print_selection,
                    "maximumVersion": "2021.2",
                }
            ],
        }
    ]


# We can add version scoping by adding the 'minimumVersion' and/or
# 'maximumVersion' properties to the function we just defined

# Effectively raises the minimum scope of Actions to 2019 to 2021
get_action_custom_ui_actions.minimum_version = "2019"

# Effectively has no efffect on the scope of Batch
get_batch_custom_ui_actions.minimum_version = "2017.2"

# Effectively narrows the scope of Timeline to a single version
get_timeline_custom_ui_actions.minimum_version = "2019.2.2.52"
get_timeline_custom_ui_actions.maximum_version = "2019.2.2.52"

# Hooks that specify a Flame version will only be displayed
# if the Flame version is equal or greater than the one defined in minimum_version.
