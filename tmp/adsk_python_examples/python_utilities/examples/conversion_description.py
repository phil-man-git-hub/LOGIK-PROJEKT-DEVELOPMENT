################################################################################
#
# Filename: conversion_description.py
#
# Copyright (c) 2025 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of how to use the project conversion hook to edit information in the
description of a converted project.
"""

import datetime


def project_init_conversion(info):
    info["project_name"] = info["project_name"] + " (Converted)"
    info["project_description"] = "Converted on {0}".format(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
