################################################################################
#
# Filename: path_of_selected_clips.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
Example of a simple custom action that can be run on a MediaHub Files object.
"""

from __future__ import print_function

import os


def print_path_of_selected_clips(selection):
    """
    Print the paths of the clip selected in the shell/terminal.
    """

    for item in selection:
        print(item.path)


def execute_command(command):
    import flame

    # Flame 2022.2+ provides a way to run a command line through the
    # Autodesk Flame Multi-Purpose Daemon. This way of starting new processes
    # is better since any native python subprocess command (os.system,
    # subprocess, Popen, etc) will call fork() which will duplicate the process
    # memory before calling exec(). This can be costly especially for a process
    # like Flame.
    #
    # Note: Environment variables will not be forwarded to the command executed.
    #
    print("Executing '%s'" % " ".join(command))
    if "execute_command" in dir(flame):
        flame.execute_command(command=" ".join(command), blocking=False, shell=False)
    else:
        import subprocess

        subprocess.call(command, close_fds=True, shell=False)


def get_default_file_browser():
    if os.uname()[0] == "Darwin":
        # On macOS, open will open a folder inside the Finder.
        #
        return "/usr/bin/open"
    else:
        # On linux, this is a bit more tricky, xdg-open can be used to open
        # the user prefered browser but it might not be configured correctly
        # out of the box.
        #
        # Check if nautilus is installed (which should be the case on all Flame
        # supported platforms) first and use it if it is. Fallback on xdg-open
        # otherwise.
        #
        for tool in ["/usr/bin/nautilus", "/usr/bin/xdg-open"]:
            if os.path.exists(tool):
                return tool

    raise Exception("No default file browser found")


def open_in_file_browser(selection):
    """
    Open the folder of the last item selected in the OS prefered file browser.
    """

    # Use the last path selected in case there is more than one selected.
    #
    path = selection[-1].path

    # Get the parent directory if the path is not itself a directory
    #
    if not os.path.isdir(path):
        path = os.path.dirname(path)

    # Use xdg-open or open to use the OS prefered file browser to open the
    # directory. This avoid having to hardcode a browser so user-defined
    # choice of tool to use is respected. This can mean however that this
    # won't open on some machine if this is not correctly configured.
    #
    if path:
        cmd = [
            get_default_file_browser(),
            path,
        ]
        execute_command(cmd)
    else:
        print("No selection or selection has no path")


def get_mediahub_files_custom_ui_actions():
    return [
        {
            "name": "Examples / MediaHub",
            "actions": [
                {
                    "name": "Print path of selected clips",
                    "execute": print_path_of_selected_clips,
                },
                {
                    "name": "Open in file browser",
                    "execute": open_in_file_browser,
                },
            ],
        }
    ]
