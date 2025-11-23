################################################################################
#
# Filename: project_hook.py
#
# Copyright (c) 2018 Autodesk, Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
################################################################################

# Hook called when the user loads a project in the application.
# project_name : Name of the loaded project -- String.
def project_changed(project_name):
    pass


# Hook called when the user loads a project in the application.
# info [Dictionary] [Modifiable]
#    Information about project
#
#    Keys:
#
#    flameProjectName: [String]
#       Name of the flame project.
#
#    shotgunProjectName: [String] [Modifiable]
#       Name of the Flow Production Tracking project it is linked with.
#       Will be empty if there is no link yet.
#
def project_changed_dict(info):
    pass


# Hook called after a project has been saved
#
# project_name: the project that was saved -- String
# save_time    : time to save the project (in seconds) -- Float
# is_auto_save : true if save was automatically initiated,
#                false if user initiated -- Bool
def project_saved(project_name, save_time, is_auto_save):
    pass


# Hook called when the Create New Project panel is opened. This can be used to
# fill information in that UI before the user does.
#
#   info [Dictionary] [Modifiable]
#       Information about the project.
#
#       Keys:
#           project_name: [String] [Modifiable]
#               Name of the created project.
#
#           project_description: [String] [Modifiable]
#               Description of the created project.
#
#           project_nickname: [String] [Modifiable]
#               Nickname of the created project.
#
#           project_home: [String] [Modifiable]
#               Path of the created project home.
#
#           project_setups_dir: [String] [Modifiable]
#               Path of the created project setups.
#
#           project_media_dir: [String] [Modifiable]
#               Path of the created project media.
#
def project_init_creation(info):
    pass

# Hook called before a project is created. This can be used to validate
# information and potentially abort the creation process before it starts.
#
#   info [Dictionary] [Modifiable]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the created project.
#
#           project_description: [String]
#               Description of the created project.
#
#           project_nickname: [String]
#               Nickname of the created project.
#
#           project_home: [String]
#               Path of the created project home.
#
#           project_setups_dir: [String]
#               Path of the created project setups.
#
#           project_media_dir: [String]
#               Path of the created project media.
#
#           abort: [Boolean] [Modifiable]
#               Hook can set this to True if the creation should be aborted.
#
#           abort_message: [String] [Modifiable]
#               Error message to be displayed to the user when the creation
#               process has been aborted
#
def project_pre_creation(info):
    pass

# Hook called after a project is created.
#
#   info [Dictionary]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the created project.
#
#           project_uuid: [String]
#               Unique Identifier of the created project.
#
#           project_description: [String]
#               Description of the created project.
#
#           project_nickname: [String]
#               Nickname of the created project.
#
#           project_home: [String]
#               Path of the created project home.
#
#           project_setups_dir: [String]
#               Path of the created project setups.
#
#           project_media_dir: [String]
#               Path of the created project media.
#
def project_post_creation(info):
    pass

# Hook called before a project settings are edited. This can be used to validate
# information and potentially abort the edition process before it is applied.
#
#   info [Dictionary] [Modifiable]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the modified project.
#
#           project_uuid: [String]
#               Unique Identifier of the modified project.
#
#           project_description: [String]
#               Description of the modified project.
#
#           project_nickname: [String]
#               Nickname of the modified project.
#
#           project_home: [String]
#               Path of the modified project home.
#
#           project_setups_dir: [String]
#               Path of the modified project setups.
#
#           project_media_dir: [String]
#               Path of the modified project media.
#
#           abort: [Boolean] [Modifiable]
#               Hook can set this to True if the edition should be aborted.
#
#           abort_message: [String] [Modifiable]
#               Error message to be displayed to the user when the edition
#               process has been aborted
#
def project_pre_edition(info):
    pass

# Hook called after a project settings are edited.
#
#   info [Dictionary]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the modified project.
#
#           project_uuid: [String]
#               Unique Identifier of the modified project.
#
#           project_description: [String]
#               Description of the modified project.
#
#           project_nickname: [String]
#               Nickname of the modified project.
#
#           project_home: [String]
#               Path of the modified project home.
#
#           project_setups_dir: [String]
#               Path of the modified project setups.
#
#           project_media_dir: [String]
#               Path of the modified project media.
#
def project_post_edition(info):
    pass

# Hook called before a project is deleted. This can be used to validate
# information and potentially abort the deletion process before it is executed.
#
#   info [Dictionary] [Modifiable]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the project.
#
#           project_uuid: [String]
#               Unique Identifier of the project.
#
#           abort: [Boolean] [Modifiable]
#               Hook can set this to True if the deletion should be aborted.
#
#           abort_message: [String] [Modifiable]
#               Error message to be displayed to the user when the deletion
#               process has been aborted
#
def project_pre_delete(info):
    pass

# Hook called after a project is deleted.
#
#   info [Dictionary]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the project.
#
#           project_uuid: [String]
#               Unique Identifier of the project.
#
def project_post_delete(info):
    pass

# Hook called when the Convert Legacy Project to Compatible Format window is
# opened. This can be used to fill information in that UI before the user does.
#
#   info [Dictionary] [Modifiable]
#       Information about the project.
#
#       Keys:
#           project_name: [String] [Modifiable]
#               Name of the converted project.
#
#           project_description: [String] [Modifiable]
#               Description of the converted project.
#
#           project_nickname: [String] [Modifiable]
#               Nickname of the converted project.
#
#           project_home: [String] [Modifiable]
#               Path of the converted project home.
#
#           project_setups_dir: [String] [Modifiable]
#               Path of the converted project setups.
#
#           project_media_dir: [String] [Modifiable]
#               Path of the converted project media.
#
#           copy_project: [Bool] [Modifiable]
#               Indicate if the project should be copied or converted in-place.
#               Might not be available when converting older project.
#
def project_init_conversion(info):
    pass

# Hook called before a project is converted to the current version. This can
# be used to validate information and potentially abort the conversion process
# before it starts.
#
#   info [Dictionary] [Modifiable]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the converted project.
#
#           project_description: [String]
#               Description of the converted project.
#
#           project_nickname: [String]
#               Nickname of the converted project.
#
#           project_home: [String]
#               Path of the converted project home.
#
#           project_setups_dir: [String]
#               Path of the converted project setups.
#
#           project_media_dir: [String]
#               Path of the converted project media.
#
#           copy_project: [Bool]
#               Indicate if the project was copied or restored in-place.
#
#           abort: [Boolean] [Modifiable]
#               Hook can set this to True if the conversion should be aborted.
#
#           abort_message: [String] [Modifiable]
#               Error message to be displayed to the user when the conversion
#               process has been aborted
#
def project_pre_conversion(info):
    pass

# Hook called after a project is converted to the current version.
#
#   info [Dictionary]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the converted project.
#
#           project_uuid: [String]
#               Unique Identifier of the converted project.
#
#           project_description: [String]
#               Description of the converted project.
#
#           project_nickname: [String]
#               Nickname of the converted project.
#
#           project_home: [String]
#               Path of the converted project home.
#
#           project_setups_dir: [String]
#               Path of the converted project setups.
#
#           project_media_dir: [String]
#               Path of the converted project media.
#
#           copy_project: [Bool]
#               Indicate if the project was copied or converted in-place.
#
def project_post_conversion(info):
    pass

# Hook called when the project restore window is opened. This can be used to
# fill information in that UI before the user does.
#
#   info [Dictionary] [Modifiable]
#       Information about the project.
#
#       Keys:
#           project_name: [String] [Modifiable]
#               Name of the restored project.
#
#           project_description: [String] [Modifiable]
#               Description of the restored project.
#
#           project_nickname: [String] [Modifiable]
#               Nickname of the restored project.
#
#           project_home: [String] [Modifiable]
#               Path of the restored project home.
#
#           project_setups_dir: [String] [Modifiable]
#               Path of the restored project setups.
#
#           project_media_dir: [String] [Modifiable]
#               Path of the restored project media.
#
def project_init_restore(info):
    pass

# Hook called before a project is restored from an archive. This can
# be used to validate information and potentially abort the restore process
# before it starts.
#
#   info [Dictionary] [Modifiable]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the restored project.
#
#           project_description: [String]
#               Description of the restored project.
#
#           project_nickname: [String]
#               Nickname of the restored project.
#
#           project_home: [String]
#               Path of the restored project home.
#
#           project_setups_dir: [String]
#               Path of the restored project setups.
#
#           project_media_dir: [String]
#               Path of the restored project media.
#
#           abort: [Boolean] [Modifiable]
#               Hook can set this to True if the restore should be aborted.
#
#           abort_message: [String] [Modifiable]
#               Error message to be displayed to the user when the restore
#               process has been aborted
#
def project_pre_restore(info):
    pass

# Hook called after a project is restored from an archive.
#
#   info [Dictionary]
#       Information about the project.
#
#       Keys:
#           project_name: [String]
#               Name of the restored project.
#
#           project_uuid: [String]
#               Unique Identifier of the restored project.
#
#           project_description: [String]
#               Description of the restored project.
#
#           project_nickname: [String]
#               Nickname of the restored project.
#
#           project_home: [String]
#               Path of the restored project home.
#
#           project_setups_dir: [String]
#               Path of the restored project setups.
#
#           project_media_dir: [String]
#               Path of the restored project media.
#
def project_post_restore(info):
    pass