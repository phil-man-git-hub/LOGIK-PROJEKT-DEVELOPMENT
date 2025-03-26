#!/bin/bash

# Enable strict error handling
set -euo pipefail

# -------------------------------------------------------------------------- #

# Program Name:     create_ssh_keys-macos.sh
# Version:          4.0.0
# Original Author:  Phil MAN - phil_man@mac.com
# Modified by:      Claude
# Created:          2024-03-12
# Modified:         2024-02-16

# Changelist:       Enhanced security, improved error handling, removed deprecated DSA keys,
#                   added secure file operations, improved password handling, converted for macOS

# Description:      This program will generate SSH keys and create an encrypted backup
#                   with enhanced security measures for macOS.

# ========================================================================== #
# Functions and Setup
# ========================================================================== #

# Error handling
handle_error() {
    local exit_code=$?
    local line_number=$1
    osascript -e "display dialog \"Error occurred in line $line_number (exit code $exit_code)\" buttons {\"OK\"} default button \"OK\" with icon stop"
    cleanup
    exit 1
}

trap 'handle_error ${LINENO}' ERR

# Cleanup function for secure deletion and memory clearing
cleanup() {
    # Securely delete sensitive files
    if [[ -f "$tar_filepath" ]]; then
        secure_delete "$tar_filepath"
    fi
    
    # Clear sensitive variables
    if [[ -v my_password ]]; then unset my_password; fi
    if [[ -v confirm_password ]]; then unset confirm_password; fi
    
    # Kill any remaining background processes
    jobs -p | xargs -r kill 2>/dev/null || true
}

trap cleanup EXIT

# Secure file deletion for macOS
secure_delete() {
    local file="$1"
    if command -v srm >/dev/null 2>&1; then
        srm -z "$file"
    else
        dd if=/dev/urandom of="$file" bs=1m count=10 conv=notrunc >/dev/null 2>&1
        rm -f "$file"
    fi
}

# -------------------------------------------------------------------------- #

# Enhanced dependency checking for macOS
check_dependencies() {
    local deps=("openssl" "ssh-keygen" "tar")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            missing+=("$dep")
        fi
    done
    
    if ((${#missing[@]} > 0)); then
        osascript -e "display dialog \"Missing required dependencies: ${missing[*]}\" buttons {\"OK\"} default button \"OK\" with icon stop"
        exit 1
    fi
}

# -------------------------------------------------------------------------- #

# Enhanced email validation with more comprehensive regex
validate_email() {
    local email="$1"
    local email_regex="^[[:alnum:]]([-._[:alnum:]]*[[:alnum:]])*@[[:alnum:]]([-._[:alnum:]]*[[:alnum:]])*\.[[:alpha:]]{2,}$"
    
    if [[ ! "$email" =~ $email_regex ]]; then
        osascript -e "display dialog \"Invalid email format. Please ensure:
- No special characters except . - _
- Valid domain format
- At least 2 character domain extension\" buttons {\"OK\"} default button \"OK\" with icon stop"
        return 1
    fi
    return 0
}

# Password strength validation (new function)
validate_password_strength() {
    local password="$1"
    local min_length=12
    
    if (( ${#password} < min_length )); then
        osascript -e "display dialog \"Password must be at least $min_length characters long\" buttons {\"OK\"} default button \"OK\" with icon stop"
        return 1
    fi
    
    if [[ ! "$password" =~ [[:upper:]] ]] || 
       [[ ! "$password" =~ [[:lower:]] ]] || 
       [[ ! "$password" =~ [[:digit:]] ]] || 
       [[ ! "$password" =~ [[:punct:]] ]]; then
        osascript -e "display dialog \"Password must contain:
- Uppercase letters
- Lowercase letters
- Numbers
- Special characters\" buttons {\"OK\"} default button \"OK\" with icon stop"
        return 1
    fi
    return 0
}

# macOS dialog for folder selection
choose_folder() {
    local folder
    folder=$(osascript -e 'tell application "System Events" to POSIX path of (choose folder with prompt "Choose Folder to Save New SSH Keys")')
    echo "$folder"
}

# macOS dialog for text entry
get_text_input() {
    local prompt="$1"
    local input
    input=$(osascript -e "tell application \"System Events\" to text returned of (display dialog \"$prompt\" default answer \"\" buttons {\"Cancel\", \"OK\"} default button \"OK\")")
    echo "$input"
}

# macOS dialog for password entry (with hidden text)
get_password_input() {
    local prompt="$1"
    local password
    password=$(osascript -e "tell application \"System Events\" to text returned of (display dialog \"$prompt\" default answer \"\" buttons {\"Cancel\", \"OK\"} default button \"OK\" with hidden answer)")
    echo "$password"
}

# macOS dialog for confirmation
show_confirmation() {
    local message="$1"
    local response
    response=$(osascript -e "tell application \"System Events\" to button returned of (display dialog \"$message\" buttons {\"No\", \"Yes\"} default button \"Yes\")")
    if [[ "$response" == "Yes" ]]; then
        return 0
    else
        return 1
    fi
}

# macOS dialog for information
show_info() {
    local message="$1"
    osascript -e "tell application \"System Events\" to display dialog \"$message\" buttons {\"OK\"} default button \"OK\" with icon note"
}

# macOS dialog for error
show_error() {
    local message="$1"
    osascript -e "tell application \"System Events\" to display dialog \"$message\" buttons {\"OK\"} default button \"OK\" with icon stop"
}

# ========================================================================== #
# Main Script
# ========================================================================== #

# Check dependencies
check_dependencies

# Define today's date in 'YYYY_MM_DD-HH_MM_SS' format
readonly today=$(date +'%Y_%m_%d-%H_%M_%S')

# Prompt user to choose a folder using macOS dialog
chosen_folder=$(choose_folder)

# Check if user cancelled the folder selection
if [ -z "$chosen_folder" ]; then
    show_error "Operation cancelled. Exiting."
    exit 1
fi

# Create an enclosing folder with secure permissions
ssh_keys_folder="$chosen_folder/ssh_keys-$today"
mkdir -p "$ssh_keys_folder"
chmod 700 "$ssh_keys_folder"

# Setup logging with reduced sensitive information
readonly ssh_key_creation_log="$ssh_keys_folder/$today-ssh_key_creation_log"
touch "$ssh_key_creation_log"
chmod 600 "$ssh_key_creation_log"

# Redirect stdout and stderr to ssh_key_creation_log, but exclude sensitive data
exec 1> >(sed 's/\(password\=\)[^ ]*/\1xxxxx/g' >> "$ssh_key_creation_log")
exec 2>&1

# Get and validate email address
while true; do
    email_address=$(get_text_input "Enter your email address:")
    
    if [ -z "$email_address" ]; then
        show_error "Operation cancelled. Exiting."
        exit 1
    fi

    if validate_email "$email_address"; then
        break
    fi
done

# Enhanced password collection with strength validation
password_match=0
while [ "$password_match" -eq 0 ]; do
    my_password=$(get_password_input "Enter Password (min 12 chars, mixed case, numbers, symbols):")
    
    if [ -z "$my_password" ]; then
        show_error "Operation cancelled. Exiting."
        exit 1
    fi

    if ! validate_password_strength "$my_password"; then
        continue
    fi
    
    confirm_password=$(get_password_input "Confirm Password:")
    
    if [ "$my_password" = "$confirm_password" ]; then
        password_match=1
    else
        show_error "Passwords do not match. Please try again."
    fi
done

# Ensure ~/.ssh directory exists with proper permissions
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Define SSH key paths - removed DSA, focusing on ED25519 and RSA
sshkey_path_ed25519="$HOME/.ssh/id_ed25519-$today"
sshkey_path_rsa="$HOME/.ssh/id_rsa-$today"

# -------------------------------------------------------------------------- #

# Enhanced key generation with better security parameters
ssh-keygen -t ed25519 -a 100 -C "$today - $email_address" -f "$sshkey_path_ed25519" \
    < <(echo -e "$my_password\n$my_password")
ssh-keygen -t rsa -b 4096 -E sha512 -a 100 -C "$today - $email_address" -f "$sshkey_path_rsa" \
    < <(echo -e "$my_password\n$my_password")

# Set proper permissions for generated keys
chmod 600 "$sshkey_path_ed25519" "$sshkey_path_rsa"
chmod 644 "$sshkey_path_ed25519.pub" "$sshkey_path_rsa.pub"

# Define the filepaths for the tar files
readonly tar_filepath="$ssh_keys_folder/ssh_keys_$today.tar"
readonly encrypted_tar_filename="encrypted_ssh_keys_$today.tar.enc"
readonly encrypted_tar_filepath="$ssh_keys_folder/$encrypted_tar_filename"
readonly decrypted_tar_filename="decrypted_ssh_keys_$today.tar"
readonly decrypted_tar_filepath="$ssh_keys_folder/$decrypted_tar_filename"

# Create a tar file of the private keys
tar -cvf "$tar_filepath" "$sshkey_path_ed25519" "$sshkey_path_rsa"

# -------------------------------------------------------------------------- #

# Enhanced encryption with AES-256-CBC and strong PBKDF2 parameters
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -salt \
    -in "$tar_filepath" \
    -out "$encrypted_tar_filepath" \
    < <(echo "$my_password")

# Verify encryption was successful
if ! [ -f "$encrypted_tar_filepath" ]; then
    show_error "Failed to create encrypted backup. Exiting."
    exit 1
fi

# Copy public keys to the chosen folder
cp "$sshkey_path_ed25519.pub" "$sshkey_path_rsa.pub" "$ssh_keys_folder/"

# Generate improved decryption script for macOS
cat <<'EOF' > "$ssh_keys_folder/decrypt.sh"
#!/bin/bash

set -euo pipefail

# Change to the directory of the running script
path_to_here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$path_to_here" || exit 1

# macOS dialog for password entry
my_password=$(osascript -e 'tell application "System Events" to text returned of (display dialog "Enter Password" default answer "" buttons {"Cancel", "OK"} default button "OK" with hidden answer)')

# Check if password is provided
if [ -z "$my_password" ]; then
    osascript -e 'tell application "System Events" to display dialog "Password cannot be empty. \nExiting." buttons {"OK"} default button "OK" with icon stop'
    exit 1
fi

# Decrypt with enhanced parameters
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 -salt \
    -in "encrypted_ssh_keys_*.tar.enc" \
    -out "decrypted_ssh_keys_$(date +'%Y_%m_%d-%H_%M_%S').tar" \
    < <(echo "$my_password")

# Clear password from memory
unset my_password

osascript -e 'tell application "System Events" to display dialog "Decryption completed successfully." buttons {"OK"} default button "OK" with icon note'
EOF

# Generate improved extraction script for macOS
cat <<'EOF' > "$ssh_keys_folder/extract.sh"
#!/bin/bash

set -euo pipefail

# Change to the directory of the running script
path_to_here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$path_to_here" || exit 1

# Extract the ssh keys from the tar file
tar -xvf "decrypted_ssh_keys_"*".tar"

# Secure delete the decrypted tar file for macOS
if command -v srm >/dev/null 2>&1; then
    srm -z "decrypted_ssh_keys_"*".tar"
else
    dd if=/dev/urandom of="decrypted_ssh_keys_"*".tar" bs=1m count=10 conv=notrunc >/dev/null 2>&1
    rm -f "decrypted_ssh_keys_"*".tar"
fi

osascript -e 'tell application "System Events" to display dialog "Extraction completed successfully." buttons {"OK"} default button "OK" with icon note'
EOF

# Set proper permissions for scripts
chmod 700 "$ssh_keys_folder/decrypt.sh" "$ssh_keys_folder/extract.sh"

# Secure deletion of the unencrypted tar file
secure_delete "$tar_filepath"

# Add SSH keys to SSH agent if requested
if show_confirmation "SSH keys generated and encrypted. \nDo you want to add them to the SSH agent?"; then
    if ssh-add "$sshkey_path_ed25519" "$sshkey_path_rsa"; then
        show_info "SSH keys successfully added to SSH agent."
    else
        osascript -e 'tell application "System Events" to display dialog "Failed to add SSH keys to SSH agent.\nYou can add them manually later using ssh-add." buttons {"OK"} default button "OK" with icon caution'
    fi
else
    show_info "SSH keys were not added to SSH agent.\nYou can add them manually later using ssh-add."
fi

# Final cleanup
cleanup

# Show summary of actions
show_info "Script finished successfully.\n\nKeys were generated in: $ssh_keys_folder\n\nEncrypted backup created: $encrypted_tar_filename\n\nUse decrypt.sh and extract.sh scripts to restore keys when needed."

# ========================================================================== #
# C2 A9 32 30 32 34 2D 4D 41 4E 2D 4D 41 44 45 2D 4D 45 4B 41 4E 59 5A 4D 53 #
# ========================================================================== #

# Changelist:

# -------------------------------------------------------------------------- #
# version:               1.0.0
# modified:              2024-03-10 - 10:20:24
# comments:              Initial commit
# -------------------------------------------------------------------------- #
# version:               2.0.0
# modified:              2024-10-15 - 10:47:35
# comments:              Added decrypt/extract scripts for all 3 major OSes.
# -------------------------------------------------------------------------- #
# version:               3.0.0
# modified:              2024-11-25 - 09:34:35
# comments:              Split monolithic script into OS specific versions
# -------------------------------------------------------------------------- #
# version:               4.0.0
# modified:              2024-12-14 - 10:20:24
# comments:              Enhanced security, improved error handling, removed deprecated DSA keys,
# -------------------------------------------------------------------------- #
# version:               4.0.0 (macOS)
# modified:              2024-02-16
# comments:              Converted to macOS, replaced Zenity with AppleScript dialogs