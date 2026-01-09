################################################################################
#
# Filename: watch_folder.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

"""
This is an example on how to leverage the Idle event callback to perform
operations during Flame's UI idle time. This example will import clips from a
watch folder, one at the time when idle.
"""

from __future__ import print_function

import os
import errno

# This is the path of the folder we will import from.
#
watch_folder_src = None

# This is the Flame object we will import to.
#
watch_folder_dst = None

# This is the list of files we already imported. For this example, we do not
# persist this list but ideally we should.
#
already_imported = set()


def do_watch_folder():
    """
    This will create a folder from which files will be imported in a library.
    The import will be done while the UI is idle, one at the time to avoid
    interrupting the user interation as much as possible.
    """

    import flame

    # Create the watch folder if not already present.
    #
    global watch_folder_src
    if not watch_folder_src:
        watch_folder_src = "/var/tmp/watch_folder"
        try:
            os.makedirs(watch_folder_src)
            print("Created watch folder source: %s" % watch_folder_src)
        except os.error as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                print("Cannot create watch folder %s: %s" % (watch_folder_src, e))
                return
        print("Watching %s" % watch_folder_src)

    # Find or create a "Watch folder" library we will import to.
    #
    WATCH_FOLDER_DST_NAME = "Watch Folder"
    global watch_folder_dst
    if not watch_folder_dst:
        watch_folder_dst_list = flame.find_by_name(WATCH_FOLDER_DST_NAME)
        if not watch_folder_dst_list:
            project = flame.projects.current_project
            workspace = project.current_workspace
            watch_folder_dst = workspace.create_library(WATCH_FOLDER_DST_NAME)
            if not watch_folder_dst:
                print("Cannot find/create destination library")
                return
            print("Created watch folder destination: %s" % WATCH_FOLDER_DST_NAME)
        else:
            watch_folder_dst = watch_folder_dst_list[0]

    # Iterate on each file in the source watch folder.
    #
    for filename in os.listdir(watch_folder_src):
        path = os.path.join(watch_folder_src, filename)
        if path in already_imported:
            continue
        already_imported.add(path)

        print("Importing %s..." % path, end="")
        flame.import_clips(path, watch_folder_dst)
        print(" Done.")

        # Only do one at the time since we are blocking the UI interation during
        # that operation. Resechedule the function so next time the UI is idle,
        # we will import the next one.
        #
        flame.schedule_idle_event(do_watch_folder, delay=1)
        return

    # We imported everything we could.
    # Resechedule the function so next time the UI is idle, we will check if
    # anything new need to be imported.
    #
    flame.schedule_idle_event(do_watch_folder, delay=10)


def app_initialized(project_name):
    """
    Register the watch folder idle method on start up.
    """
    do_watch_folder()
