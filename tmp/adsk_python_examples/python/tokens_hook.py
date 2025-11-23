################################################################################
#
# Filename: tokens_hook.py
#
# Copyright (c) 2018 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

# Hook returning the custom token list to display to the user in the token
# widgets.
#
#    context : Context of the token list -- String.
#              Possible context is: Browsing
#
#    Returns a tuple of token dictionaries.
#
#    A token dictionary defines a custom token where keys defines
#    the token.
#
#    Keys:
#
#    name: [String]
#       Name of the token, usually following the format '{name}'.
#
#    displayName: [String]
#       Display name of the token in token list
#
#    For example:
#
#    def getCustomTokenList():
#
#        return ({"name": "{Token1}",
#                 "displayName": "Token 1"},
#                {"name": "{Token2}",
#                 "displayName": "Token 2"})
#
#    The return value needs to be a tuple, if only one token is returned it
#    should be done like this:
#
#        return ({"name": "{Token1}",
#                 "displayName": "Token 1"}, )
#
#    Note: The token for Browsing should be wrapped in {}.
#
def get_custom_token_list(context):
    if context == "Browsing":
        return (
            {"name": "{width}", "displayName": "Width"},
            {"name": "{height}", "displayName": "Height"},
            {"name": "{shotName}", "displayName": "Shot Name"},
            {"name": "{sequence}", "displayName": "Sequence"},
            {"name": "{artist}", "displayName": "Artist"},
            {"name": "{task}", "displayName": "Task"},
        )
    return None
