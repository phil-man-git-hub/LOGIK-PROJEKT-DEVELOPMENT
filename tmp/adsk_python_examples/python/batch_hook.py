################################################################################
#
# Filename: batch_hook.py
#
# Copyright (c) 2018 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

# Hook called when a batch setup is loaded
#
# setupPath: File path of the setup being loaded.
#
def batch_setup_loaded(setupPath, *args, **kwargs):
    pass


# Hook called when a batch setup is saved
#
# setupPath: File path of the setup being saved.
#
def batch_setup_saved(setupPath, *args, **kwargs):
    pass


# Hook called before a batch iteration is created
#
# info [Dictionary] [Modifiable]
#    Information about the batch iteration,
#
#    Keys:
#
#    savePath:     [String] [Modifiable]
#       The path to which a corresponding batch setup file is saved on disk.
#
#    setupName:    [String] [Modifiable]
#       The name of the corresponding batch setup file saved on disk.
#
#    abort:        [Boolean] [Modifiable]
#       Set this variable to True if you want to abort the backup process.
#       If you do so, batchSetupIteratedPost will not be called.
#       False if undefined.
#
#    abortMessage: [String] [Modifiable]
#       Error message to describe why the abort happened.
#       A generic one will be used if left blank.
#
# userData [Dictionary] [Modifiable]
#   Object that will be carried over into the batchSetupIteratedPost hook.
#   This can be used by the hook to pass black box data around.
#
def batch_setup_iterated_pre(info, userData, *args, **kwargs):
    pass


# Hook called after a batch iteration is created
#
# info [Dictionary]
#    Information about the batch iteration,
#
#    Keys:
#
#    savePath:       [String]
#       The path to which a corresponding batch setup file is saved on disk.
#
#    setupName:      [String]
#       The name of the corresponding batch setup file saved on disk.
#
#    abort:          [Boolean]
#       Will be True if the save failed, it won't be defined otherwise.
#       Note: if the save was manually aborted, this hook will not be called.
#             so this variable only expresses actual errors.
#
#    abortMessage:   [String]
#       Error message to describe why the abort happened.
#
# userData [Dictionary]
#   Object that can be set from the batchSetupIteratedPre hook.
#   This can be used by the hook to pass black box data around.
#
def batch_setup_iterated_post(info, userData, *args, **kwargs):
    pass


# Hook called before a render begins.
#
# info [Dictionary] [Modifiable]
#    Information about the render,
#
#    Keys:
#
#    backgroundJobName: [String] [Modifiable]
#       Job name as shown in Backburner. Can be modified by the hook
#       before the job is actually sent.
#
#    aborted: [Boolean] [Modifiable]
#       Set this variable to True if you want to abort the process.
#
#    abortMessage: [String] [Modifiable]
#       Error message to describe why the abort happened.
#       A generic one will be used if left blank.
#
# userData [Dictionary] [Modifiable]
#   Object that will be carried over into the batchRenderEnd hook.
#   This can be used by the hook to pass black box data around.
#
def batch_render_begin(info, userData, *args, **kwargs):
    pass


# Hook called when a render ends.
#
# This function complements the above batchRenderBegin function.
#
# info [Dictionary]
#    Information about the render,
#
#    Keys:
#
#    backgroundJobName: [String]
#       Job name as shown in Backburner.
#
#    backgroundJobId: [String]
#       Id of the background job given by the backburner Manager upon
#       submission.
#
#    aborted: [Boolean]
#       Indicate if the render has been aborted by the user or by a render
#       error.
#
#    abortMessage: [String]
#       Error message to describe why the abort happened.
#
# userData [Dictionary] [Modifiable]
#   Object that will be carried over into the batchExportEnd hook.
#   This can be used by the hook to pass black box data around.
#
def batch_render_end(info, userData, *args, **kwargs):
    pass


# Hook called before a job is sent to Burn or Background Reactor.
#
# info [Dictionary] [Modifiable]
#    Information about the job,
#
#    Keys:
#
#    aborted: [Boolean] [Modifiable]
#       Set this variable to True if you want to abort the process.
#
#    abortMessage: [String] [Modifiable]
#       Error message to describe why the abort happened.
#       A generic one will be used if left blank.
#
# userData [Dictionary] [Modifiable]
#   Object that will be carried over into the batchRenderEnd hook.
#   This can be used by the hook to pass black box data around.
#
def batch_burn_begin(info, userData, *args, **kwargs):
    pass


# Hook called after a job is sent to Burn or Background Reactor.
#
# This function complements the above batch_burn_begin function.
#
# info [Dictionary]
#    Information about the job,
#
#    Keys:
#
#    aborted: [Boolean]
#       Indicate if the process has been aborted by the user or by an
#       error.
#
#    abortMessage: [String]
#       Error message to describe why the abort happened.
#
#    backgroundJobId: [String]
#       Id of the background job given by the backburner Manager upon
#       submission.
#
# userData [Dictionary] [Modifiable]
#   Object that will be carried over into the batchExportEnd hook.
#   This can be used by the hook to pass black box data around.
#
def batch_burn_end(info, userData, *args, **kwargs):
    pass


# Hook called before a write file node starts to export.  Note that for stereo
# exports this function is called twice, once for each channel
# (left first, right second).
#
# info [Dictionary] [Modifiable]
#    Information about the export,
#
#    Keys:
#
#    nodeName:   [String]
#       Name of the export node.
#
#    exportPath: [String] [Modifiable]
#       Export path as entered in the application UI.
#       Can be modified by the hook to change where the file are written.
#
#    namePattern: [String]
#       List of optional naming tokens as entered in the application UI.
#
#    resolvedPath: [String]
#       Full file pattern that will be exported with all the tokens resolved.
#
#    firstFrame: [Integer]
#       Frame number of the first frame that will be exported.
#
#    lastFrame: [Integer]
#       Frame number of the last frame that will be exported.
#
#    versionName: [String]
#       Current version name of export (Empty if unversioned).
#
#    versionNumber: [Integer]
#       Current version number of export (0 if unversioned).
#
#    shotName: [String]
#       Current shot name of export.
#
#    openClipNamePattern: [String]
#       List of optional naming tokens pointing to the open clip created if any
#       as entered in the application UI. This is only available if versioning
#       is enabled.
#
#    openClipResolvedPath: [String]
#       Full path to the open clip created if any with all the tokens resolved.
#       This is only available if versioning is enabled.
#
#    setupNamePattern: [String]
#       List of optional naming tokens pointing to the setup created if any
#       as entered in the application UI. This is only available if versioning
#       is enabled.
#
#    setupResolvedPath: [String]
#       Full path to the setup created if any with all the tokens resolved.
#       This is only available if versioning is enabled.
#
#    width: [Long]
#       Frame width of the exported media.
#
#    height: [Long]
#       Frame height of the exported media.
#
#    aspectRatio: [Double]
#       Frame aspect ratio of the exported media.
#
#    depth: [String]
#       Frame depth of the exported media.
#       ('8-bits', '10-bits', '12-bits', '16 fp')
#
#    scanFormat: [String]
#       Scan format of the exported media.
#       ('FIELD_1', 'FIELD_2', 'PROGRESSIVE')
#
#    colourSpace: [String]
#       Colour space of the exported media.
#
#    fps: [Double]
#       Frame rate of exported asset.
#
#    aborted: [Boolean] [Modifiable]
#       Set this variable to True if you want to abort the process.
#
#    abortMessage: [String] [Modifiable]
#       Error message to describe why the abort happened.
#       A generic one will be used if left blank.
#
# userData [Object] [Modifiable]
#   Object that will be carried over into the batchExportEnd hook.
#   This can be used by the hook to pass black box data around.
#
def batch_export_begin(info, userData, *args, **kwargs):
    pass


# Hook called when a write file node ends the export. Note that for stereo
# exports this function is called twice, once for each channel
# (left first, right second).
#
# This function complements the above batch_export_begin function.
#
# info [Dictionary]
#    Information about the export,
#
#    Keys:
#
#    nodeName:   [String]
#       Name of the export node.
#
#    exportPath: [String]
#       Export path as entered in the application UI.
#
#    namePattern: [String]
#       List of optional naming tokens as entered in the application UI.
#
#    resolvedPath: [String]
#       Full file pattern that will be exported with all the tokens resolved.
#
#    firstFrame: [Integer]
#       Frame number of the first frame that will be exported.
#
#    lastFrame: [Integer]
#       Frame number of the last frame that will be exported.
#
#    versionName: [String]
#       Current version name of export (Empty if unversioned).
#
#    versionNumber: [Integer]
#       Current version number of export (0 if unversioned).
#
#    shotName: [String]
#       Current shot name of export.
#
#    openClipNamePattern: [String]
#       List of optional naming tokens pointing to the open clip created if any
#       as entered in the application UI. This is only available if versioning
#       is enabled.
#
#    openClipResolvedPath: [String]
#       Full path to the open clip created if any with all the tokens resolved.
#       This is only available if versioning is enabled.
#
#    setupNamePattern: [String]
#       List of optional naming tokens pointing to the setup created if any
#       as entered in the application UI. This is only available if versioning
#       is enabled.
#
#    setupResolvedPath: [String]
#       Full path to the setup created if any with all the tokens resolved.
#       This is only available if versioning is enabled.
#
#    width: [Long]
#       Frame width of the exported media.
#
#    height: [Long]
#       Frame height of the exported media.
#
#    aspectRatio: [Double]
#       Frame aspect ratio of the exported media.
#
#    depth: [String]
#       Frame depth of the exported media.
#       ('8-bits', '10-bits', '12-bits', '16 fp')
#
#    scanFormat: [String]
#       Scan format of the exported media.
#       ('FIELD_1', 'FIELD_2', 'PROGRESSIVE')
#
#    fps: [Double]
#       Frame rate of exported asset.
#
#    backgroundJobId: [String]
#       Id of the background job given by the backburner Manager upon
#       submission. Empty if job is done in foreground.
#
#    aborted: [Boolean]
#       Indicate if the export has been aborted by the user or by a render
#       error.
#
#    abortMessage: [String]
#       Error message to describe why the abort happened.
#
# userData [Dictionary]
#   Object optionally filled by the batchExportBegin hook.
#   This can be used by the hook to pass black box data around.
#
def batch_export_end(info, userData, *args, **kwargs):
    pass
