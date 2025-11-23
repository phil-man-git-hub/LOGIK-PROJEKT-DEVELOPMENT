################################################################################
#
# Filename: object_scoping.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Simple samples of utility methods used to scope custom actions to specific areas or objects.
"""


def scope_background(selection):
    """
    The following can be used to make a custom action Visible or Enabled
    for the Batch Schematic background.
    """
    return len(selection) == 0


def scope_object(selection):
    """
    The following can be used to make a custom action Visible or Enabled
    for a specific PyObject.

    PyNode can be replaced by any PyObject.
    Multiple PyObjects can be specified.
    """
    import flame

    for item in selection:
        if isinstance(item, flame.PyNode):
            return True
    return False


def scope_node(selection):
    """
    The following can be used to make a custom action Visible or Enabled
    for a specific node.

    The .type definition can be replaced by any Batch Node name.
    Multiple node names can be specified.
    """

    import flame

    for item in selection:
        if isinstance(item, flame.PyNode):
            if item.type == "Comp":
                return True
    return False
