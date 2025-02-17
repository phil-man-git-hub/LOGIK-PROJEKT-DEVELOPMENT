#!/bin/bash

# -------------------------------------------------------------------------- #

# Program Name:     create_ssh_keys-macos.sh
# Version:          3.0.0
# Author:           Phil MAN - phil_man@mac.com
# Created:          2024-03-12
# Modified:         2024-11-25

# Changelist:       Added function to create/read 'project_setup_template'.

# Description:      This program will generate SSH keys and prompt the user
#                   to create an encrypted backup tar file.
#!/bin/zsh

# Enable strict error handling
set -euo pipefail

# -------------------------------------------------------------------------- #

# Program Name:     create_ssh_keys-macos.sh
# Version:          4.0.0
# Modified for:     macOS Compatibility

# ========================================================================== #
# Functions and Setup
# ========================================================================== #

# Error handling
handle_error() {
    local exit_code=$?
    local line_number=$1
    osascript -e 'display dialog "Error occurred in line '$line_number' (exit code '$exit_code')" buttons {"OK"} default button "OK" with icon stop'
    cleanup
    exit 1
}

trap 'handle_error ${LINENO}' ERR

# Cleanup function for secure deletion and memory clearing
cleanup() {
    if [[ -f "$tar_filepath" ]]; then
        secure_delete "$tar_filepath"
    fi
    unset my_password confirm_password 2>/dev/null
}

trap cleanup EXIT

# Secure file deletion for macOS
secure_delete() {
    local file="$1"
    if command -v srm >/dev/null 2>&1; then
        srm -f "$file"
    else
        rm -P "$file"
    fi
}

# -------------------------------------------------------------------------- #

# Check dependencies
check_dependencies() {
    local deps=("openssl" "ssh-keygen" "tar")
    for dep in "$deps[@]"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            osascript -e 'display dialog "Missing required dependency: '$dep'" buttons {"OK"} default button "OK" with icon stop'
            exit 1
        fi
    done
}

check_dependencies

# -------------------------------------------------------------------------- #

# Get user input
chosen_folder=$(osascript -e 'choose folder with prompt "Choose Folder to Save New SSH Keys"' | sed 's/:/\//g' | sed 's/^/\//' | sed 's/ /\\ /g')

[[ -z "$chosen_folder" ]] && osascript -e 'display dialog "Operation cancelled. Exiting." buttons {"OK"} default button "OK" with icon stop' && exit 1

# Define SSH key paths
readonly today=$(date +'%Y_%m_%d-%H_%M_%S')
ssh_keys_folder="$chosen_folder/ssh_keys-$today"
mkdir -p "$ssh_keys_folder" && chmod 700 "$ssh_keys_folder"

# Get and validate email
while true; do
    email_address=$(osascript -e 'text returned of (display dialog "Enter your email address:" default answer "" with icon note)')
    [[ -z "$email_address" ]] && exit 1
    [[ "$email_address" =~ "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" ]] && break
    osascript -e 'display dialog "Invalid email format. Try again." buttons {"OK"} default button "OK" with icon caution'
done

# Get password
password_match=0
while [[ "$password_match" -eq 0 ]]; do
    my_password=$(osascript -e 'text returned of (display dialog "Enter Secure Password:" default answer "" with hidden answer true with icon note)')
    confirm_password=$(osascript -e 'text returned of (display dialog "Confirm Password:" default answer "" with hidden answer true with icon note)')
    [[ "$my_password" == "$confirm_password" ]] && password_match=1 || osascript -e 'display dialog "Passwords do not match." buttons {"OK"} default button "OK" with icon caution'
done

# Generate SSH keys
sshkey_path_ed25519="$HOME/.ssh/id_ed25519-$today"
sshkey_path_rsa="$HOME/.ssh/id_rsa-$today"
ssh-keygen -t ed25519 -a 100 -C "$today - $email_address" -f "$sshkey_path_ed25519" -N "$my_password"
ssh-keygen -t rsa -b 4096 -E sha512 -a 100 -C "$today - $email_address" -f "$sshkey_path_rsa" -N "$my_password"
chmod 600 "$sshkey_path_ed25519" "$sshkey_path_rsa"
chmod 644 "$sshkey_path_ed25519.pub" "$sshkey_path_rsa.pub"

# Encrypt SSH keys
tar_filepath="$ssh_keys_folder/ssh_keys_$today.tar"
encrypted_tar_filepath="$ssh_keys_folder/encrypted_ssh_keys_$today.tar.enc"
tar -cvf "$tar_filepath" "$sshkey_path_ed25519" "$sshkey_path_rsa"
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -salt -in "$tar_filepath" -out "$encrypted_tar_filepath" -pass pass:"$my_password"
secure_delete "$tar_filepath"

# Ask to add keys to ssh-agent
if osascript -e 'button returned of (display dialog "SSH keys generated and encrypted. Add them to SSH agent?" buttons {"Yes", "No"} default button "Yes" with icon note)' | grep -q "Yes"; then
    eval "$(ssh-agent -s)"
    ssh-add "$sshkey_path_ed25519" "$sshkey_path_rsa" && osascript -e 'display dialog "Keys added successfully." buttons {"OK"} default button "OK" with icon note'
fi

osascript -e 'display dialog "Script finished successfully. Keys saved in: '$ssh_keys_folder'" buttons {"OK"} default button "OK" with icon note'
