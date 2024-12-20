#!/bin/bash

# -------------------------------------------------------------------------- #

initiative_name="projekt_creation_2026"

pr_version=pr213

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

path_to_xml_version_dir="$path_to_xml_dir/$pr_version"

xml_template_name="pr213_projekt_template.xml"
path_to_xml_template="$path_to_xml_version_dir/$xml_template_name"

xml_file_name="projekt_template.xml"
path_to_xml_file="$path_to_xml_dir/$xml_file_name"

xml_backup_name="$xml_file_name.$(date '+%Y_%m_%d-%H_%M_%S').bak"
path_to_xml_backup="$path_to_bak_dir/$pr_version/$xml_backup_name"

# -------------------------------------------------------------------------- #

# Create the backup directory if it does not exist
mkdir -pv "$path_to_bak_dir/$pr_version"

# Backup any existing file
cp -v "$path_to_xml_file" "$path_to_xml_backup"

# Copy the template to a new file
cp -v "$path_to_xml_template" "$path_to_xml_file"

# Prompt user for projekt_nackname
read -p "Enter the nickname for the projekt: " project_nickname

# Perform substitutions in new file
sed -i "s/\$WORKSTATION/juliet/g; s/\$NICKNAME/${project_nickname}/g" "$path_to_xml_file"

# -------------------------------------------------------------------------- #