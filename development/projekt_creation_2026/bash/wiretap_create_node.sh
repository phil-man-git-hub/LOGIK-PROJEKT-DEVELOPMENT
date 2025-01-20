#! /bin/bash

set -ex

# -------------------------------------------------------------------------- #

initiative_name="projekt_creation_2026"

project_nickname="33333"

pr_version=pr214

workstation_name="juliet"

the_projekt_flame_name="${project_nickname}_${pr_version}_${workstation_name}"

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

xml_template_name="${pr_version}_projekt_template.xml"
path_to_xml_template="$path_to_xml_version_dir/$xml_template_name"

xml_file_name="projekt_template.xml"
path_to_xml_file="$path_to_xml_dir/$xml_file_name"

projekt_xml_path="$path_to_xml_file"

# Copy the projekt template to the xml file
cp -v $path_to_xml_template $path_to_xml_file

# replace the string '$WORKSTATION_NAME' with the workstation name
sed -i "s/\$WORKSTATION/$workstation_name/g" $path_to_xml_file

# Replace the string '$NICKNAME' with the project nickname
sed -i "s/\$NICKNAME/$project_nickname/g" $path_to_xml_file

# -------------------------------------------------------------------------- #

umask 000

# Create a logik projekt flame project node using wiretap
/opt/Autodesk/wiretap/tools/current/wiretap_create_node \
-h localhost:IFFFS \
-n /projects \
-t PROJECT \
-d "${the_projekt_flame_name}" \
-s XML \
-f "${projekt_xml_path}"


# # flame 2026 alpha pr211 wiretap_create_node problems
# Flame Family 2026 Alpha
# FLA26A-00036
# https://feedback.autodesk.com/project/feedback/view.html?cap=5afe6c84-5cb3-447a-b36c-cbd7f0688f84&uf=b676f017-4cfd-42af-b5d6-6c7bde7c0613&slsid=404a4766-98e6-47e4-846a-84cece277e91

# + projekt_xml_path=/home/pman/workspace/GitHub/phil-man-git-hub/LOGIK-PROJEKT-DEVELOPMENT/development/projekt_creation_2026/xml/projekt_template.xml
# + projekt_xml_path=/home/pman/workspace/GitHub/phil-man-git-hub/LOGIK-PROJEKT-DEVELOPMENT/development/projekt_creation_2026/xml/projekt_template.xml