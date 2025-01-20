#!/bin/bash

# -------------------------------------------------------------------------- #

initiative_name="projekt_creation_2026"

pr_version=pr214

# -------------------------------------------------------------------------- #

path_to_workspace="/home/pman/workspace/GitHub/phil-man-git-hub"
path_to_git_project="$path_to_workspace/LOGIK-PROJEKT-DEVELOPMENT"
path_to_dev_dir="$path_to_git_project/development"
path_to_initiative_dir="$path_to_dev_dir/$initiative_name"

# -------------------------------------------------------------------------- #

path_to_bak_dir="$path_to_initiative_dir/bak"
path_to_bash_dir="$path_to_initiative_dir/bash"
path_to_notes_dir="$path_to_initiative_dir/notes"
path_to_opt_dir="$path_to_initiative_dir/opt"
path_to_python_dir="$path_to_initiative_dir/python"
path_to_xml_dir="$path_to_initiative_dir/xml"

# -------------------------------------------------------------------------- #

path_to_adsk_dir="$path_to_opt_dir/Autodesk"
path_to_adsk_cfg_dir="$path_to_adsk_dir/cfg"
path_to_sysconfig_dir="$path_to_adsk_cfg_dir/sysconfig"
path_to_sysconfig_version_dir="$path_to_sysconfig_dir/$pr_version"

# -------------------------------------------------------------------------- #

sysconfig_template_name="pr213_sysconfig.cfg"
path_to_sysconfig_template="$path_to_sysconfig_version_dir/$sysconfig_template_name"

sysconfig_file_name="sysconfig.cfg"
path_to_sysconfig_file="$path_to_sysconfig_version_dir/$sysconfig_file_name"

sysconfig_backup_name="$sysconfig_file_name.$(date '+%Y_%m_%d-%H_%M_%S').bak"
path_to_sysconfig_backup="$path_to_bak_dir/$pr_version/$sysconfig_backup_name"

current_adsk_sysconfig_file="/opt/Autodesk/cfg/.current/sysconfig.cfg"

# -------------------------------------------------------------------------- #

# Create the backup directory if it does not exist
mkdir -pv "$path_to_bak_dir/$pr_version"

# Backup any existing file
cp -v "$current_adsk_sysconfig_file" "$path_to_sysconfig_backup"

# Copy the new file to the Autodesk cfg directory
sudo cp -v "$path_to_sysconfig_file" "$current_adsk_sysconfig_file"

# -------------------------------------------------------------------------- #
