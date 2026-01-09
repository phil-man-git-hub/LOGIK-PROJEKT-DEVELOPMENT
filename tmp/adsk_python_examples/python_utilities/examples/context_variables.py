################################################################################
#
# Filename: context_variables.py
#
# Copyright (c) 2025 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Simple samples of utility methods used to manage OCIO Context Variables.

These examples are working with the 'OCIO Example' preset that contains a View
named 'Shot Based CC' which includes a Look using multiple Context Variables.

These functions are setting the 'SHOT' Context Variable to the Shot Name of the Segment or Clip Node.
The 'SHOT' Context Variable is used to alter the path pointing to a specific .cc file per shot.
"""


def add_cmfx_with_shot_based_cc(selection):
    """
    Example setting the Shot Name to the Background Index on selected Segments and use it as the 'SHOT'
    Context Variable value inside the Source Colour Management Timeline effect in View Transform mode.
    """
    import flame

    # Sanitize the selection list
    segments = []
    for item in selection:
        if isinstance(item, flame.PySegment):
            segments.append(item)
        elif isinstance(item, flame.PySequence):
            for version in item.versions:
                for track in version.tracks:
                    segments = segments + track.segments

    # Check if Segments have existing Source Colour Management effects.
    # Ask user if they want to keep or overwrite existing effects.
    # User can also cancel the whole process.
    found = False
    overwrite_setups = False
    for segment in segments:
        if found:
            break
        for fx in segment.effects:
            if fx.type == "Source Colour Mgmt":
                found = True
                answer = flame.messages.show_in_dialog(
                    title="Overwrite existing Source Colour Management setups",
                    message="One or more selected segments already have a Source Colour Management FX."
                    "\n\nDo you want to overwrite the existing effect ?",
                    type="warning",
                    buttons=["Keep", "Overwrite"],
                    cancel_button="Cancel",
                )
                if answer == "Cancel":
                    return
                if answer == "Overwrite":
                    overwrite_setups = True
                break

    # Iterate on all Segments to:
    # - Set the Shot Name to the Background Index if the Segment doesn't have a Shot Name.
    # - Add a Source Colour Management effect.
    # - Set the Colour Management mode to View Transform.
    # - Set the proper Input Colour Space and View.
    # - Set the SHOT Context Variable to the Shot Name of the Segment.
    for segment in segments:
        name = segment.name.get_value()
        shot_name = segment.shot_name.get_value()

        if not shot_name:
            segment.tokenized_shot_name = "<background segment>"
            shot_name = segment.shot_name.get_value()

        clmgt = None
        for fx in segment.effects:
            if fx.type == "Source Colour Mgmt":
                clmgt = fx
                break

        if clmgt and not overwrite_setups:
            print(
                f"Skipping segment named '{name}' because it has an existing Source Colour Management effect."
            )
            continue
        if not clmgt:
            clmgt = segment.create_effect("Source Colour Mgmt")

        clmgt.mode = "View Transform"
        clmgt.tagged_colour_space = "From Source"
        clmgt.view = "Shot Based CC"

        clmgt.context_variables_from_project = False
        clmgt.set_context_variable("SHOT", shot_name)


def add_cmnode_with_shot_based_cc(selection):
    """
    Example adding a Colour Management node in View Transform mode to a Clip node
    and use its associated Shot Name to set the 'SHOT' Context Variable value.
    """
    import flame

    # Sanitize the selection list
    clip_nodes = []
    for item in selection:
        if isinstance(item, flame.PyClipNode):
            clip_nodes.append(item)
        elif isinstance(item, flame.PyBatch):
            clip_nodes = clip_nodes + [
                n for n in item.nodes if isinstance(n, flame.PyClipNode)
            ]

    # Iterate on all Clip Nodes to:
    # - Add a Colour Management node connected to the Clip node.
    # - Set the Colour Management node in View Transform mode.
    # - Set the proper Input Colour Space and View.
    # - Set the CCC_ID Context Variable to the Shot Name coming from the Clip node.
    for clip_node in clip_nodes:
        node_name = clip_node.name.get_value()
        node_bit_depth = clip_node.resolution.get_value().bit_depth
        shot_name = clip_node.shot_name.get_value()

        batch = clip_node.parent
        clmgt = batch.create_node("Colour Mgmt")
        batch.connect_nodes(clip_node, "Default", clmgt, "Default")

        clmgt.mode = "View Transform"
        clmgt.tagged_colour_space = "From Source"
        clmgt.view = "Shot Based CC"
        clmgt.bit_depth = node_bit_depth

        if not shot_name:
            print(
                f"The Clip node named '{node_name}' has no Shot Name. Using default Context Variables."
            )
            continue

        clmgt.context_variables_from_project = False
        clmgt.set_context_variable("SHOT", shot_name)


def is_clip_node(selection):
    """
    Returns True if the selection has a PyClipNode.
    """
    import flame

    for item in selection:
        if isinstance(item, flame.PyClipNode):
            return True
    return False


def is_segment(selection):
    """
    Returns True if the selection has a PySegment.
    """
    import flame

    for item in selection:
        if isinstance(item, flame.PySegment):
            return True
    return False


def is_sequence(selection):
    """
    Returns True if the selection has a PySequence.
    """
    import flame

    for item in selection:
        if isinstance(item, flame.PySequence):
            return True
    return False


def is_batch(selection):
    """
    Returns True if the selection has a PyBatch.
    """
    import flame

    for item in selection:
        if isinstance(item, flame.PyBatch):
            return True
    return False


def get_timeline_custom_ui_actions():
    """
    Add hooks to the Timeline.
    """
    return [
        {
            "name": "Examples / Context Variables",
            "actions": [
                {
                    "name": "Add Colour Management effect with Shot Based CC",
                    "isVisible": is_segment,
                    "execute": add_cmfx_with_shot_based_cc,
                    "minimumVersion": "2026.0",
                }
            ],
        }
    ]


def get_batch_custom_ui_actions():
    """
    Add hooks to Batch.
    """
    return [
        {
            "name": "Examples / Context Variables",
            "actions": [
                {
                    "name": "Add Colour Management node with Shot Based CC",
                    "isVisible": is_clip_node,
                    "execute": add_cmnode_with_shot_based_cc,
                    "minimumVersion": "2026.0",
                }
            ],
        }
    ]


def get_media_panel_custom_ui_actions():
    """
    Add hooks to the Media Panel.
    """
    return [
        {
            "name": "Examples / Context Variables",
            "actions": [
                {
                    "name": "Add Colour Management effect with Shot Based CC",
                    "isVisible": is_sequence,
                    "execute": add_cmfx_with_shot_based_cc,
                    "minimumVersion": "2026.0",
                },
                {
                    "name": "Add Colour Management node with Shot Based CC",
                    "isVisible": is_batch,
                    "execute": add_cmnode_with_shot_based_cc,
                    "minimumVersion": "2026.0",
                },
            ],
        }
    ]
