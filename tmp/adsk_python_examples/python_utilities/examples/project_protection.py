################################################################################
#
# Filename: project_protection.py
#
# Copyright (c) 2025 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of how to use the project hooks abort mechanism to prevent
from modifiying a project.
"""

restricted_project_names = ["final", "final_final"]


def check(info):
    info["abort"] = info["project_name"] in restricted_project_names
    info["abort_message"] = "This project is flagged as restricted."


def project_pre_edition(info):
    check(info)


def project_pre_delete(info):
    check(info)


def project_pre_conversion(info):
    check(info)
