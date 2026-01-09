#!/opt/Autodesk/python/2027.pr232/bin/python3
################################################################################
#
# Filename: export_hook.py
#
# Copyright (c) 2018 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

# Hooks in this files are called in the following order:
#
# preCustomExport (optional depending on getCustomExportProfiles)
#  preExport
#   preExportSequence
#    preExportAsset
#    postExportAsset  (could be done in backburner depending of useBackburnerPostExportAsset)
#    ...
#   postExportSequence
#   ...
#  postExport
# postCustomExport (optional depending on getCustomExportProfiles)

# Hook called before a custom export begins. This can be used to fill
# information that would have normally been extracted from the export window.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String] [Modifiable]
#       Host name where the exported files will be written to.
#       Defaults to localhost.
#
#    destinationPath: [String] [Modifiable]
#       Export path root.
#       Defaults to /tmp
#
#    presetPath: [String] [Modifiable]
#       Path to the preset used for the export.
#       Must be defined by this method.
#
#    useTopVideoTrack: [Boolean] [Modifiable]
#       Use only the top video track and ignore the other ones.
#       (False if not defined)
#
#    exportBetweenMarks: [Boolean] [Modifiable]
#       Export between the In  and Out marks, excluding the marked frames.
#       If there is no In, export from start of sequence to Out;
#       if there is no Out, export from the In to the end of the sequence.
#       (False if not defined)
#
#    isBackground: [Boolean] [Modifiable]
#       Perform the export in background.
#       (True if not defined)
#
#    includeSubtitles: [Boolean] [Modifiable]
#       Include the subtitles as part of the export.
#       (False if not defined)
#
#    exportSubtitlesAsFiles: [Boolean] [Modifiable]
#       Export the subtitles as files when True. Burn them in the image if False.
#       (True if not defined)
#
#    exportAllSubtitles: [Boolean] [Modifiable]
#       Use all subtitles tracks of a clip instead of only the current track.
#       (False if not defined)
#
#    abort: [Boolean] [Modifiable]
#       Hook can set this to True if the custom export process should be
#       aborted.
#
#    abortMessage: [String] [Modifiable]
#       Error message to be displayed to the user when the export process has
#       been aborted
#
# userData [Object] [Modifiable]
#   Object that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
#   This will usually be a dictionary.
#   The object can be modified but not reassigned.
#
def pre_custom_export(info, userData, *args, **kwargs):
    pass


# Hook called after a custom export ends.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files were written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    presetPath: [String]
#       Path to the preset used for the export.
#
# userData [Object] [Modifiable]
#   Object that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
#   This will usually be a dictionary.
#   The object can be modified but not reassigned.
#
def post_custom_export(info, userData, *args, **kwargs):
    pass


# Hook called before an export begins.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files will be written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    presetPath: [String]
#       Path to the preset used for the export.
#
#    abort: [Boolean] [Modifiable]
#       Hook can set this to True if the export process should be aborted.
#
#    abortMessage: [String] [Modifiable]
#       Error message to be displayed to the user when the export process has
#       been aborted
#
# userData [Object] [Modifiable]
#   Object that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
#   This will usually be a dictionary.
#   The object can be modified but not reassigned.
#
def pre_export(info, userData, *args, **kwargs):
    pass


# Hook called after an export ends.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files were written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    presetPath: [String]
#       Path to the preset used for the export.
#
# userData [Object] [Modifiable]
#   Object that could have been populated by previous export hooks.
#   This can be used by the hook to pass black box data around.
#   This will usually be a dictionary.
#   The object can be modified but not reassigned.
#
def post_export(info, userData, *args, **kwargs):
    pass


# Hook called before a sequence export begins.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files will be written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    sequenceName: [String]
#       Name of the exported sequence.
#
#    shotNames: [String]
#       Tuple of all shot names in the exported sequence. Multiple segments
#       could have the same shot name.
#
#    thumbnailFrameNb: [Int]
#       Frame index of the active thumbnail
#
#    abort: [Boolean] [Modifiable]
#       Hook can set this to True if the export sequence process should
#       be aborted. If other sequences are exported in the same export session
#       they will still be exported even if this export sequence is aborted.
#
#    abortMessage: [String] [Modifiable]
#       Error message to be displayed to the user when the export sequence
#       process has been aborted
#
# userData [Object] [Modifiable]
#   Object that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
#   This will usually be a dictionary.
#   The object can be modified but not reassigned.
#
def pre_export_sequence(info, userData, *args, **kwargs):
    pass


# Hook called after a sequence export ends.
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files were written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    sequenceName: [String]
#       Name of the exported sequence.
#
#    shotNames: [String]
#       Tuple of all shot names in the exported sequence. Multiple segment
#       could have the same shot name.
#
#    thumbnailFrameNb: [Int]
#       Frame index of the active thumbnail
#
# userData [Object] [Modifiable]
#   Object that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
#   This will usually be a dictionary.
#   The object can be modified but not reassigned.
#
def post_export_sequence(info, userData, *args, **kwargs):
    pass


# Hook called before an asset export begins.
#
# info [Dictionary] [Modifiable]
#    Information about the asset exported.
#
#    If the asset is a multi-channel media, the information might only apply to
#    the beauty layer.
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files will be written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    namePattern: [String]
#       List of optional naming tokens.
#
#    resolvedPath: [String] [Modifiable]
#       File pattern (relative to destinationPath) that will be exported
#       with all the tokens resolved.
#
#    assetName: [String]
#       Name of the exported asset.
#
#    sequenceName: [String]
#       Name of the sequence the asset is part of.
#
#    shotName: [String]
#       Name of the shot the asset is part of.
#
#    tapeName: [String]
#       Name of the tape the asset is part of.
#
#    assetType: [String]
#       Type of exported asset.
#       ('video', 'audio', 'movie,' 'batch', 'openClip', 'batchOpenClip', 'distributionPackage', 'subtitles')
#
#    width: [Long]
#       Frame width of the exported asset.
#
#    height: [Long]
#       Frame height of the exported asset.
#
#    aspectRatio: [Double]
#       Frame aspect ratio of the exported asset.
#
#    depth: [String]
#       Frame depth of the exported asset.
#       ('8-bits', '10-bits', '12-bits', '16 fp')
#
#    scanFormat: [String]
#       Scan format of the exported asset.
#       ('FIELD_1', 'FIELD_2', 'PROGRESSIVE')
#
#    colourSpace: [String]
#       Colour space of the exported asset.
#
#    fps: [Double]
#       Frame rate of exported asset.
#
#    sequenceFps: [Double]
#       Frame rate of the sequence the asset is part of.
#
#    sourceIn: [Integer]
#       The source in point as a frame, using the asset frame rate (fps key).
#
#    sourceOut: [Integer]
#       The source out point as a frame, using the asset frame rate (fps key).
#
#    recordIn: [Integer]
#       The record in point as a frame, using the sequence frame rate
#       (sequenceFps key).
#
#    recordOut: [Integer]
#       The record out point as a frame, using the sequence frame rate
#       (sequenceFps key).
#
#    handleIn: [Integer]
#       Head as a frame, using the asset frame rate (fps key).
#
#    handleOut: [Integer]
#       Tail as a frame, using the asset frame rate (fps key).
#
#    startFrame: [Integer]
#       If the source is a file sequence, startFrame is the index of the source's first frame.
#
#    track: [String]
#       ID of the sequence's track that contains the asset.
#
#    trackName: [String]
#       Name of the sequence's track that contains the asset.
#
#    subtitlesName: [String]
#       Name of the subtitles track or its position when unnamed.
#
#    segmentIndex: [Integer]
#       Asset index (1 based) in the track.
#
#    versionName: [String]
#       Current version name of export (Empty if unversioned).
#
#    versionNumber: [Integer]
#       Current version number of export (0 if unversioned).
#
#    useBackburner: [Boolean]
#       Use backburner to launch postExportAsset.
#
#    isSnapshot: [Boolean]
#       True if the export has been initiated by the Export Snapshot function in the Player.
#
#    abort: [Boolean] [Modifiable]
#       Hook can set this to True if the custom export process should be
#       aborted.
#
#    abortMessage: [String] [Modifiable]
#       Error message to be displayed to the user when the export process has
#       been aborted
#
# userData [Object] [Modifiable]
#   Object that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
#   This will usually be a dictionary.
#   The object can be modified but not reassigned.
#
def pre_export_asset(info, userData, *args, **kwargs):
    pass


# Hook called after an asset export ends.
#
# info [Dictionary] [Modifiable]
#    Information about the asset exported.
#
#    If the asset is a multi-channel media, the information might only apply to
#    the beauty layer.
#
#    Keys:
#
#    destinationHost: [String]
#       Host name where the exported files were written to.
#
#    destinationPath: [String]
#       Export path root.
#
#    namePattern: [String]
#       List of optional naming tokens.
#
#    resolvedPath: [String]
#       File pattern (relative to destinationPath) that will be exported
#       with all the tokens resolved.
#
#    assetName: [String]
#       Name of the exported asset.
#
#    sequenceName: [String]
#       Name of the sequence the asset is part of.
#
#    shotName: [String]
#       Name of the shot the asset is part of.
#
#    assetType: [String]
#       Type of exported asset.
#       ('video', 'audio', 'movie,' 'batch', 'openClip', 'batchOpenClip', 'distributionPackage', 'subtitles')
#
#    isBackground: [Boolean]
#       True if the export of the asset happened in the background.
#
#    isSnapshot: [Boolean]
#       True if the export has been initiated by the Export Snapshot function in the Player.
#
#    backburnerManager: [String]
#       Backburner Manager handling the background job.
#       Empty if job is done in foreground.
#
#    backgroundJobId: [String]
#       Id of the background job given by the backburner Manager upon
#       submission. Empty if job is done in foreground.
#
#    width: [Long]
#       Frame width of the exported asset.
#
#    height: [Long]
#       Frame height of the exported asset.
#
#    aspectRatio: [Double]
#       Frame aspect ratio of the exported asset.
#
#    depth: [String]
#       Frame depth of the exported asset.
#       ('8-bits', '10-bits', '12-bits', '16 fp')
#
#    scanFormat: [String]
#       Scan format of the exported asset.
#       ('FIELD_1', 'FIELD_2', 'PROGRESSIVE')
#
#    colourSpace: [String]
#       Colour space of the exported asset.
#
#    fps: [Double]
#       Frame rate of exported asset.
#
#    sequenceFps: [Double]
#       Frame rate of the sequence the asset is part of.
#
#    sourceIn: [Integer]
#       The source in point as a frame, using the asset frame rate (fps key).
#
#    sourceOut: [Integer]
#       The source out point as a frame, using the asset frame rate (fps key).
#
#    recordIn: [Integer]
#       The record in point as a frame, using the sequence frame rate
#       (sequenceFps key).
#
#    recordOut: [Integer]
#       The record out point as a frame, using the sequence frame rate
#       (sequenceFps key).
#
#    handleIn: [Integer]
#       Head as a frame, using the asset frame rate (fps key).
#
#    handleOut: [Integer]
#       Tail as a frame, using the asset frame rate (fps key).
#
#    startFrame: [Integer]
#       If the source is a file sequence, startFrame is the index of the source's first frame.
#
#    track: [String]
#       ID of the sequence's track that contains the asset.
#
#    trackName: [String]
#       Name of the sequence's track that contains the asset.
#
#    subtitlesName: [String]
#       Name of the subtitles track or its position when unnamed.
#
#    segmentIndex: [Integer]
#       Asset index (1 based) in the track.
#
#    versionName: [String]
#       Current version name of export (Empty if unversioned).
#
#    versionNumber: [Integer]
#       Current version number of export (0 if unversioned).
#
# userData [Object] [Modifiable]
#   Object that could have been populated by previous export hooks and that
#   will be carried over into the subsequent export hooks.
#   This can be used by the hook to pass black box data around.
#   This will usually be a dictionary.
#   The object can be modified but not reassigned.
#
def post_export_asset(info, userData, *args, **kwargs):
    pass


# :return: true or false whether post_export_asset should be called from a
# backburner job or directly from the application.
#
# :warning: Not generating a post_export_asset backburner job for exports that
# are using backburner could result in post_export_asset being called before the
# export job is complete.
#
def use_backburner_post_export_asset(*args, **kwargs):
    pass


# Indicates that the application is about to overwrite a file and the user will
# be prompted with a choice.  This method could be used to bypass the prompt.
#
# Valid return values are:
#    ask : User will be prompted for action.
#    overwrite : Overwrite this file.
#    overwrite_all : Overwrite all file from now on.
#    skip : Do not write the file.
#
def export_overwrite_file(path, *args, **kwargs):
    pass


# Hook returning the custom export profiles to display to the user in the
# contextual menu.
#
# profiles [Dictionary] [Modifiable]
#
#    A dictionary of userData dictionaries where the keys are the name
#    of the profiles to show in contextual menus.
#
def get_custom_export_profiles(profiles, *args, **kwargs):
    pass


if __name__ == "__main__":
    import sys

    # Call a hook from the command line:
    #
    #  exportHook.py <function> <args>
    #
    method = sys.argv[1]
    params = (eval(p) for p in sys.argv[2:])
    globals()[method](*params)
