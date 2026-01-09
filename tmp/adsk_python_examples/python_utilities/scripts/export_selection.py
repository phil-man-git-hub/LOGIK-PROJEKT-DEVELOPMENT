################################################################################
#
# Filename: export_selection.py
#
# Copyright (c) 2020 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

from __future__ import print_function

"""
Example of a custom UI action that exports a thumbnail and a movie for all
clips in a selection.
"""

import logging
import os
import shlex
import traceback
import errno


def make_dirs(directory):
    """
    Create a folder structure leading to a given directory without raising an
    error if the directory already exists.
    """
    try:
        os.makedirs(directory)
    except Exception as e:
        if e.errno == errno.EEXIST:
            pass


def show_overwrite_confirm_dialog(text, title):
    """
    Show a dialog box.
    """
    import flame

    dialog = flame.messages.show_in_dialog(
        title=title,
        message=text,
        type="warning",
        buttons=["Overwrite"],
        cancel_button="Cancel",
    )
    return dialog == "Overwrite"


def get_export_dir():
    """
    Show a file browser to allow the user to select a directory to export to.
    """
    import flame

    dir = flame.browser.show(
        title="Select a directory to export to ",
        default_path="/",
        multi_selection=False,
        select_directory=True,
    )

    return flame.browser.selection[0] if flame.browser.selection else None


def export_movie(clip, export_dir):
    """
    Export a clip as a QuickTime to export_dir
    """

    import flame

    # Build the presets path.
    #
    # By using flame.PyExporter.get_presets_dir(), we don't need to know where
    # the application stores its presets. Or we could also use any path that
    # leads to a Flame export preset file.
    #
    # Possible visibilities are:
    #   Autodesk:   Factory presets shipped with the application.
    #   Shared:     Shared presets for all applications (/opt/Autodesk/shared).
    #   Project:    Project specific presets.
    #   User:       User specific presets.
    #
    # Possible presets types are:
    #   Movie:                  Movie files (typically QuickTime & MXF)
    #   Image_Sequence:         Image sequences (Jpeg, Dpx, Exr)
    #   Audio:                  Audio files (wav)
    #   Sequence_Publish:       Complex sequence/timeline export (AAF, FCP X/7, EDL)
    #   Distribution_Package:   Distribution Package (IMF)
    #
    preset_dir = flame.PyExporter.get_presets_dir(
        flame.PyExporter.PresetVisibility.Autodesk, flame.PyExporter.PresetType.Movie
    )
    preset_path = os.path.join(
        preset_dir, "QuickTime", "QuickTime (8-bit Uncompressed).xml"
    )

    # Initialize the exporter instance we will use to do the export.
    #
    exporter = flame.PyExporter()

    # Set the exporter to use foreground export. By default it will send a
    # job to backburner to do the export.
    #
    exporter.foreground = True

    # Do the actual export.
    #
    exporter.export(clip, preset_path, export_dir)
    print("Exported %s to %s" % (clip.name.get_value(), export_dir))


def run_ffmpeg(audio_pipe_name, read_audio_cmd, read_frame_cmd, ffmpeg_cmd):
    """
    Make named pipe. Launch read_audio_cmd and pipe output to named pipe.
    Launch read_frame_cmd and pipe output to ffmpeg_cmd.
    """

    import errno
    import subprocess

    print(read_audio_cmd)
    print()
    print(read_frame_cmd)
    print()
    print(ffmpeg_cmd)
    print()

    # Remove left-over audio pipe if any
    try:
        os.unlink(audio_pipe_name)
    except OSError as err:
        # Suppress the exception if it is a file not found error.
        # Otherwise, re-raise the exception.
        if err.errno != errno.ENOENT:
            raise

    try:
        # Create new audio pipe
        os.mkfifo(audio_pipe_name, 0o644)

        # Launch read_frame command
        read_frame_args = shlex.split(read_frame_cmd)
        read_frame_process = subprocess.Popen(read_frame_args, stdout=subprocess.PIPE)

        try:
            # Launch ffmpeg command
            ffmpeg_args = shlex.split(ffmpeg_cmd)
            ffmpeg_process = subprocess.Popen(
                ffmpeg_args, stdin=read_frame_process.stdout, stderr=subprocess.STDOUT
            )
        except Exception as err:
            # Clean-up dangling read_frame process
            read_frame_process.kill()
            read_frame_process.wait()
            raise

        try:
            # Open audio pipe and run read_audio
            audio_pipe = os.open(audio_pipe_name, os.O_WRONLY)
            audio_args = shlex.split(read_audio_cmd)
            audio_process = subprocess.check_call(audio_args, stdout=audio_pipe)
        except Exception as err:
            # Clean-up dangling ffmpeg and read_frame processes
            ffmpeg_process.kill()
            ffmpeg_process.wait()
            read_frame_process.kill()
            read_frame_process.wait()
            raise
        finally:
            # Closing audio pipe so ffmpeg stops waiting for input
            os.close(audio_pipe)

        # Let read_frame and ffmpeg do their thing
        ffmpeg_process.wait()
        read_frame_process.wait()

    except Exception as err:
        logging.error(traceback.format_exc())
        raise

    finally:
        # Remove audio pipe
        os.unlink(audio_pipe_name)


def export_ffmpeg(clip, export_dir, foreground):
    """
    Export a clip to QuickTime using /usr/local/bin/ffmpeg
    """

    import subprocess
    import platform

    from adsk.libwiretapPythonClientAPI import (
        WireTapServerHandle,
        WireTapNodeHandle,
    )

    # Specify output dimensions here
    width = 1920
    height = 1080
    # Could alternatively use source dimensions
    # width = clip.width
    # height = clip.height

    # Specify output video codec and options here
    output_vcodec = "-vcodec qtrle"
    output_vcodec_is_rgb = True

    # Specify output audio codec and options here
    output_acodec = "-acodec adpcm_ima_qt"

    print()
    print("Export with ffmpeg")

    # Render clip (in foreground) if needed and commit library before extracting
    # clip information like the node id because they could change upon render
    # and commit.
    #
    # In a real workflow, you might want to consider copying the clip so it does
    # not get altered by the user while the export is ongoing.
    #
    clip.render()
    clip.commit()

    # Extract metadata from source clip
    storage_id = clip.get_wiretap_storage_id()
    print("Clip server: " + storage_id)

    node_id = clip.get_wiretap_node_id()
    print("Clip Id: " + node_id)

    clipname = clip.name.get_value()
    print("Clip Name: " + clipname)

    tc = "%s" % clip.start_time
    print("Timecode (Flame): " + tc)

    fps = clip.frame_rate
    print("Frame rate: %s" % clip.frame_rate)
    drop = fps.find(" DF") > 0

    tc = tc[:2] + ":" + tc[3:5] + ":" + tc[6:8] + (";" if drop else ":") + tc[9:]
    print("Timecode (FFmpeg): " + tc)

    fps = fps[0 : fps.find("fps") - 1]
    print("Clip fps: " + fps)

    print("Clip depth: %d" % clip.bit_depth)
    need_16_bpc = clip.bit_depth > 8

    audio_pipe_name = os.path.join(export_dir, "%s.audio.pipe" % clipname)
    print("Audio pipe: " + audio_pipe_name)

    output_file = os.path.join(export_dir, "%s.mov" % clipname)
    if os.path.exists(output_file):
        if not show_overwrite_confirm_dialog(
            "Do you want to overwrite %s?" % output_file,
            "An item with the same name already exists.",
        ):
            return
    print("Output file: " + output_file)
    print()

    # Prepare read_frame command
    read_frame_cmd = (
        "/opt/Autodesk/io/bin/read_frame -S '%s' -n '%s' -N -1 -W %d -H %d -b %d"
        % (storage_id, node_id, width, height, 48 if need_16_bpc else 24)
    )

    # Prepare transfer of clip's color metadata to ffmpeg
    color_space = (
        "-color_primaries %d -color_trc %d -colorspace %d "
        "-movflags write_colr "
        % (
            clip.colour_primaries,
            clip.transfer_characteristics,
            0 if output_vcodec_is_rgb else clip.matrix_coefficients,
        )
    )

    # Prepare ffmpeg command: will get its audio input from audio pipe above
    # and its video input from stdin (piped read_frame command)
    ffmpeg_cmd = (
        "/usr/local/bin/ffmpeg "
        +
        # Video input options
        "-f rawvideo -pix_fmt %s -s %dx%d -r '%s' -i - "
        +
        # Audio input options
        "-ar 48000 -f s16le -ac 2 -i '%s' "
        +
        # Video output options
        output_vcodec
        + " "
        +
        # Audio output options
        output_acodec
        + " "
        +
        # Metadata output options
        color_space
        + "-timecode '%s' "
        + "-metadata:s:v:0 reel_name='%s' "
        + "-metadata title='%s' "
        +
        # Output file
        "-y '%s'"
    ) % (
        "rgb48le" if need_16_bpc else "rgb24",
        width,
        height,
        fps,
        audio_pipe_name,
        tc,
        clip.tape_name,
        clipname,
        output_file,
    )

    # Prepare audio command
    read_audio_cmd = (
        "/opt/Autodesk/io/bin/read_audio -S " + storage_id + " -n " + node_id
    )

    # Run the commands
    if foreground:
        run_ffmpeg(audio_pipe_name, read_audio_cmd, read_frame_cmd, ffmpeg_cmd)

    else:
        # Background execution is performed via Backburner cmdjob.
        # Everything is packaged in a python command line for cmdjob consumption.

        cmdjob = (
            "/opt/Autodesk/backburner/cmdjob "
            + "-jobName:'FFmpeg - "
            + clipname
            + "' "
            + "-description:'"
            + clipname
            + " -> "
            + output_file
            + "' "
            + "-servers:"
            + platform.node().split(".")[0]
            + ' /opt/Autodesk/python/2027.pr232/bin/python3 -c "'
            + "import sys; import os;"
            + "sys.path.insert(1,'"
            + os.path.dirname(os.path.realpath(__file__))
            + "');"
            + "import export_selection;"
            + "export_selection.run_ffmpeg('"
            + audio_pipe_name
            + "','"
            + read_audio_cmd.replace("'", "\\'")
            + "','"
            + read_frame_cmd.replace("'", "\\'")
            + "','"
            + ffmpeg_cmd.replace("'", "\\'")
            + "')"
            + '"'
        )

        print(cmdjob)
        print()
        try:
            cmdjob_args = shlex.split(cmdjob)
            subprocess.check_call(cmdjob_args)
        except Exception as err:
            logging.error(traceback.format_exc())
            raise

    # Invalidate exported clip in WTG
    try:
        server = WireTapServerHandle("localhost:Gateway")
        node = WireTapNodeHandle(server, output_file + "@CLIP")
        if not node.setMetaData("Invalidate", ""):
            print("Unable to set metadata: " + node.lastError())
    finally:
        # Must destroy WireTapServerHandle and WireTapNodeHandle before
        # uninitializing the Wiretap Client API.
        #
        node = None
        server = None


def export_thumbnail(clip, export_dir):
    """
    Export the first frame of a clip in jpeg.
    """

    import flame

    # Build the presets path.
    #
    # By using flame.PyExporter.get_presets_dir(), we don't need to know where
    # the application stores its presets. Or we could also use any path that
    # leads to a Flame export preset file.
    #
    # Possible visibilities are:
    #   Autodesk:   Factory presets shipped with the application.
    #   Shared:     Shared presets for all applications (/opt/Autodesk/shared).
    #   Project:    Project specific presets.
    #   User:       User specific presets.
    #
    # Possible presets types are:
    #   Movie:              Movie files (typically QuickTime & MXF)
    #   Image_Sequence:     Image sequences (Jpeg, Dpx, Exr)
    #   Audio:              Audio files (wav)
    #   Sequence_Publish:   Complex sequence/timeline export (AAF, FCP X/7, EDL)
    #
    preset_dir = flame.PyExporter.get_presets_dir(
        flame.PyExporter.PresetVisibility.Autodesk,
        flame.PyExporter.PresetType.Image_Sequence,
    )
    preset_path = os.path.join(preset_dir, "Jpeg", "Jpeg (8-bit).xml")

    # Initialize the exporter instance we will use to do the export.
    #
    exporter = flame.PyExporter()

    # Set the exporter to use foreground export. By default it will send a
    # job to backburner to do the export.
    #
    exporter.foreground = True

    # We want to do a single frame export so we will modify the clip in/out
    # marks to point to the first frame and we will use the export_between_marks
    # options to tell the exporter that we want to use in/out marks as the
    # range to export
    #
    exporter.export_between_marks = True

    # Backup the clip in/out marks so we can restore them to current value
    # after the export.
    #
    in_mark = clip.in_mark.get_value()
    out_mark = clip.out_mark.get_value()
    try:
        # Set in/out mark to only export first frame. out_mark is exclusive
        # by default.
        #
        clip.in_mark = 1
        clip.out_mark = 2

        # Do the actual export.
        #
        exporter.export(clip, preset_path, export_dir)
        print("Exported %s to %s" % (clip.name.get_value(), export_dir))
    finally:
        # Restore the clip original in/out marks.
        #
        clip.in_mark = in_mark
        clip.out_mark = out_mark


def export_movies(selection, export_root=None):
    """
    Export all clips in a selection as QuickTime.
    """

    import flame

    # Create the export root.
    #
    export_dir = export_root if export_root is not None else get_export_dir()
    if export_dir is None:
        return
    print("Creating %s" % (export_dir))
    make_dirs(export_dir)

    # Iterate the selection.
    #
    for item in selection:

        # Check if the item is a folder like object
        #
        if isinstance(
            item,
            (
                flame.PyReelGroup,
                flame.PyReel,
                flame.PyFolder,
                flame.PyLibrary,
                flame.PyDesktop,
            ),
        ):
            export_sub_dir = os.path.join(export_dir, item.name.get_value())
            print("Creating %s" % (export_sub_dir))
            make_dirs(export_sub_dir)
            export_movies(item.children, export_sub_dir)

        # Check if the item in the selection is a sequence or a clip
        #
        elif isinstance(item, (flame.PySequence, flame.PyClip)):
            export_movie(item, export_dir)


def export_thumbnails(selection, export_root=None):
    """
    Export the first frames of all clips as jpeg.
    """

    import flame

    # Create the export root.
    #
    export_dir = export_root if export_root is not None else get_export_dir()
    if export_dir is None:
        return
    print("Creating %s" % export_dir)
    make_dirs(export_dir)

    # Iterate the selection.
    #
    for item in selection:

        # Check if the item is a folder like object
        #
        if isinstance(
            item,
            (
                flame.PyReelGroup,
                flame.PyReel,
                flame.PyFolder,
                flame.PyLibrary,
                flame.PyDesktop,
            ),
        ):
            export_sub_dir = os.path.join(export_dir, item.name.get_value())
            print("Creating %s" % (export_sub_dir))
            make_dirs(export_sub_dir)
            export_thumbnails(item.children, export_sub_dir)

        # Check if the item in the selection is a sequence or a clip
        #
        elif isinstance(item, (flame.PySequence, flame.PyClip)):
            export_thumbnail(item, export_dir)


def export_thumbnail_movie(selection):
    """
    Export all clips in a selection as QuickTime and Jpeg.
    """

    export_root = get_export_dir()
    export_movies(selection, export_root)
    export_thumbnails(selection, export_root)


def export_ffmpegs(selection, export_dir, foreground):
    """
    Export all clips in a selection with ffmpeg.
    """

    import flame

    # Iterate the selection.
    #
    for item in selection:
        # Check if the item is a folder like object
        #
        if isinstance(
            item,
            (
                flame.PyReelGroup,
                flame.PyReel,
                flame.PyFolder,
                flame.PyLibrary,
                flame.PyDesktop,
            ),
        ):
            export_sub_dir = os.path.join(export_dir, item.name.get_value())
            print("Creating %s" % (export_sub_dir))
            make_dirs(export_sub_dir)
            export_ffmpegs(item.children, export_sub_dir, foreground)

        # Check if the item in the selection is a sequence or a clip
        #
        elif isinstance(item, (flame.PySequence, flame.PyClip)):
            export_ffmpeg(item, export_dir, foreground)


def export_ffmpegs_fg(selection):
    """
    Export all clips in a selection with ffmpeg in foreground.
    """

    # Create the export root.
    #
    export_dir = get_export_dir()
    if export_dir is None:
        return
    print("Creating %s" % export_dir)
    make_dirs(export_dir)
    export_ffmpegs(selection, export_dir, foreground=True)


def export_ffmpegs_bg(selection):
    """
    Export all clips in a selection with ffmpeg in foreground.
    """

    # Create the export root.
    #
    export_dir = get_export_dir()
    if export_dir is None:
        return
    print("Creating %s" % export_dir)
    make_dirs(export_dir)
    export_ffmpegs(selection, export_dir, foreground=False)


def get_media_panel_custom_ui_actions():
    return [
        {
            "name": "Examples / Export",
            "actions": [
                {
                    "name": "Export selection (thumbnail + movie)",
                    "execute": export_thumbnail_movie,
                    #
                    # Since this action require user input, we want to
                    # show the normal cursor for the duration of the action.
                    #
                    "waitCursor": False,
                },
                {
                    "name": "Export selection (thumbnail)",
                    "execute": export_thumbnails,
                    #
                    # Since this action require user input, we want to
                    # show the normal cursor for the duration of the action.
                    #
                    "waitCursor": False,
                },
                {
                    "name": "Export selection (movie)",
                    "execute": export_movies,
                    #
                    # Since this action require user input, we want to
                    # show the normal cursor for the duration of the action.
                    #
                    "waitCursor": False,
                },
                {
                    "name": "Export selection using ffmpeg in foreground",
                    "execute": export_ffmpegs_fg,
                    #
                    # Since this action require user input, we want to
                    # show the normal cursor for the duration of the action.
                    #
                    "waitCursor": False,
                },
                {
                    "name": "Export selection using ffmpeg in background",
                    "execute": export_ffmpegs_bg,
                    #
                    # Since this action require user input, we want to
                    # show the normal cursor for the duration of the action.
                    #
                    "waitCursor": False,
                },
            ],
        }
    ]


def get_main_menu_custom_ui_actions():
    return get_media_panel_custom_ui_actions()


# Collection call using children attribute introduced in 2022
get_media_panel_custom_ui_actions.minimum_version = "2022"
get_main_menu_custom_ui_actions.minimum_version = "2022"
