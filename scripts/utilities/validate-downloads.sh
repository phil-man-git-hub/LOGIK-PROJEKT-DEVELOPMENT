#!/bin/bash
################################################################################
# validate-downloads.sh
# Enhanced script to validate Autodesk Flame downloads against MD5 checksums
# Features: robust error handling, logging, CLI args, interactive shell completion
################################################################################

# -------------------------------------------------------------------------- #
# STRICT EXECUTION MODE
# -------------------------------------------------------------------------- #

# Uncomment these settings for stricter bash execution
# set -e           # Exit on any errors
# set -u           # Exit if any variable is used without being defined
# set -o pipefail  # Exit if any command in a pipeline fails
# set -x           # Print each command before execution

set -euo pipefail
IFS=$'\n\t'

# -------------------------------------------------------------------------- #
# EXIT CODES
# -------------------------------------------------------------------------- #

readonly EXIT_SUCCESS=0
readonly EXIT_ERROR=1
readonly EXIT_INVALID_OS=2
readonly EXIT_INVALID_DIR=3
readonly EXIT_MISSING_DEPENDENCY=4
readonly EXIT_USER_CANCELLED=5
readonly EXIT_NO_FILES=6

# -------------------------------------------------------------------------- #
# LOGGING LEVELS
# -------------------------------------------------------------------------- #

readonly LOG_DEBUG=0
readonly LOG_INFO=1
readonly LOG_WARN=2
readonly LOG_ERROR=3

# Default log level can be overridden with LOG_LEVEL environment variable
LOG_LEVEL="${LOG_LEVEL:-$LOG_INFO}"
TEST_MODE="${TEST_MODE:-false}"
USE_CLI_MODE="${USE_CLI_MODE:-false}"

# -------------------------------------------------------------------------- #
# DETECT OPERATING SYSTEM
# -------------------------------------------------------------------------- #

detect_os() {
    case "$(uname)" in
        Darwin)  echo "macOS" ;;
        Linux)   echo "Linux" ;;
        MINGW*|MSYS*) echo "Windows" ;;
        *)       echo "unknown" ;;
    esac
}

readonly OPERATING_SYSTEM=$(detect_os)

if [[ "$OPERATING_SYSTEM" == "unknown" ]]; then
    echo "Error: Unsupported operating system." >&2
    exit "$EXIT_INVALID_OS"
fi

# -------------------------------------------------------------------------- #
# PATH DISCOVERY
# -------------------------------------------------------------------------- #

readonly THIS_SCRIPT=$(basename "$0")
readonly PROGRAM_NAME="${THIS_SCRIPT%.*}"
readonly PROGRAM_NAME_UC=$(echo "$PROGRAM_NAME" | tr '[:lower:]' '[:upper:]')
readonly THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find repo root by searching upward for scripts directory
find_repo_root() {
    local current_dir="$THIS_DIR"
    
    while [[ "$current_dir" != "/" ]]; do
        if [[ -d "$current_dir/scripts" ]]; then
            echo "$current_dir"
            return 0
        fi
        current_dir=$(dirname "$current_dir")
    done
    
    return 1
}

readonly REPO_DIR=$(find_repo_root || echo ".")
readonly SCRIPTS_DIR="$REPO_DIR/scripts"
readonly REPO_NAME=$(basename "$REPO_DIR")
readonly REPO_PATH=$(dirname "$REPO_DIR")
readonly PREFS_DIR="$REPO_DIR/prefs"
readonly LOGS_DIR="$REPO_DIR/logs"

# -------------------------------------------------------------------------- #
# CREATE DIRECTORIES IF NEEDED
# -------------------------------------------------------------------------- #

mkdir -p "$LOGS_DIR" "$PREFS_DIR"

# -------------------------------------------------------------------------- #
# LOGGING SETUP
# -------------------------------------------------------------------------- #

readonly PROGRAM_LOG="$LOGS_DIR/${PROGRAM_NAME}_$(date +%Y%m%d_%H%M%S).log"
touch "$PROGRAM_LOG"

# -------------------------------------------------------------------------- #
# LOGGING FUNCTIONS (no output redirection - simpler approach)
# -------------------------------------------------------------------------- #

log_to_file() {
    local level="$1"
    shift
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    printf "[%s] %s: %s\n" "$timestamp" "$level" "$*" >> "$PROGRAM_LOG"
}

log_to_all() {
    local level="$1"
    shift
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    printf "[%s] %s: %s\n" "$timestamp" "$level" "$*" | tee -a "$PROGRAM_LOG"
}

log_debug() {
    [[ $LOG_LEVEL -le $LOG_DEBUG ]] && log_to_all "DEBUG" "$@" || log_to_file "DEBUG" "$@"
}

log_info() {
    [[ $LOG_LEVEL -le $LOG_INFO ]] && log_to_all "INFO" "$@" || log_to_file "INFO" "$@"
}

log_warn() {
    [[ $LOG_LEVEL -le $LOG_WARN ]] && log_to_all "WARN" "$@" || log_to_file "WARN" "$@"
}

log_error() {
    [[ $LOG_LEVEL -le $LOG_ERROR ]] && log_to_all "ERROR" "$@" >&2 || log_to_file "ERROR" "$@"
}

log_success() {
    log_info "✓ $*"
}

# -------------------------------------------------------------------------- #
# ERROR HANDLING
# -------------------------------------------------------------------------- #

die() {
    local message="$1"
    local exit_code="${2:-$EXIT_ERROR}"
    log_error "$message"
    exit "$exit_code"
}

trap_error() {
    local line_no=$1
    log_error "Script error on line $line_no"
    exit "$EXIT_ERROR"
}

trap_interrupt() {
    log_warn "Script interrupted by user"
    exit "$EXIT_USER_CANCELLED"
}

trap trap_error ERR
trap trap_interrupt INT TERM

# -------------------------------------------------------------------------- #
# DEPENDENCY CHECKING
# -------------------------------------------------------------------------- #

check_required_commands() {
    local commands=("basename" "dirname" "find" "cut" "awk" "date")
    
    case "$OPERATING_SYSTEM" in
        macOS)  commands+=("md5" "scutil") ;;
        Linux)  commands+=("md5sum") ;;
    esac
    
    for cmd in "${commands[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            log_error "Required command not found: $cmd"
            return 1
        fi
    done
    
    return 0
}

check_required_commands || die "Missing required dependencies" "$EXIT_MISSING_DEPENDENCY"

# -------------------------------------------------------------------------- #
# SYSTEM INFORMATION
# -------------------------------------------------------------------------- #

get_workstation_name() {
    case "$OPERATING_SYSTEM" in
        macOS)  scutil --get ComputerName ;;
        Linux)  hostname ;;
        *)      echo "UnknownWorkstation" ;;
    esac
}

readonly WORKSTATION_NAME=$(get_workstation_name)
readonly CURRENT_USER="$USER"
readonly PRIMARY_GROUP="$(id -gn)"

# -------------------------------------------------------------------------- #
# SEPARATOR
# -------------------------------------------------------------------------- #

readonly separator_plus="=========================================================================="

# -------------------------------------------------------------------------- #
# UTILITY FUNCTIONS
# -------------------------------------------------------------------------- #

print_usage() {
    cat << EOF
Usage: $THIS_SCRIPT [OPTIONS]

Validate Autodesk Flame downloads by comparing MD5 checksums.

OPTIONS:
    -d, --directory PATH      Use PATH as downloads directory
    -c, --cli                 Use command-line mode (no GUI dialogs)
    -q, --quiet              Suppress info output (errors only)
    -v, --verbose            Enable verbose/debug output
    -t, --test               Test mode (dry run, no actual validation)
    -h, --help               Show this help message

EXAMPLES:
    # Interactive GUI mode
    $THIS_SCRIPT

    # CLI mode with tab completion
    $THIS_SCRIPT --cli

    # Validate specific directory
    $THIS_SCRIPT --directory ~/Downloads

    # Verbose mode
    $THIS_SCRIPT -v --cli -d /path/to/downloads

ENVIRONMENT VARIABLES:
    LOG_LEVEL       Set to DEBUG for verbose output
    TEST_MODE       Set to true for dry run
    USE_CLI_MODE    Set to true to force CLI mode

EOF
}

validate_directory() {
    local dir="$1"
    
    # Expand tilde if present
    dir="${dir/#\~/$HOME}"
    # Remove trailing slashes
    dir="${dir%/}"
    
    if [[ -z "$dir" ]]; then
        log_error "Directory path is empty"
        return 1
    fi
    
    if [[ ! -d "$dir" ]]; then
        log_error "Directory does not exist: $dir"
        return 1
    fi
    
    if [[ ! -r "$dir" ]]; then
        log_error "Directory is not readable: $dir"
        return 1
    fi
    
    return 0
}

calculate_md5() {
    local file_path="$1"
    
    case "$OPERATING_SYSTEM" in
        macOS)
            md5 -r "$file_path" | awk '{print $1}'
            ;;
        Linux)
            md5sum "$file_path" | awk '{print $1}'
            ;;
        *)
            die "MD5 calculation not supported on $OPERATING_SYSTEM"
            ;;
    esac
}

# -------------------------------------------------------------------------- #
# DIRECTORY SELECTION - CLI MODE WITH COMPLETION
# -------------------------------------------------------------------------- #

select_directory_cli() {
    local default_path="${1:-$HOME/Downloads}"
    local chosen_dir=""
    
    echo "  Select downloads directory" >&2
    echo "  Default: $default_path" >&2
    echo "  (Press Enter to use default, or type a path with tab completion)" >&2
    echo "" >&2
    
    read -e -p "  Path: " chosen_dir < /dev/tty
    
    # If user just pressed enter, use default
    if [[ -z "$chosen_dir" ]]; then
        chosen_dir="$default_path"
    fi
    
    # Expand tilde
    chosen_dir="${chosen_dir/#\~/$HOME}"
    
    # Only output the path to stdout (which will be captured)
    echo "$chosen_dir"
}

# -------------------------------------------------------------------------- #
# DIRECTORY SELECTION - GUI MODE
# -------------------------------------------------------------------------- #

select_directory_gui() {
    local chosen_dir=""
    
    case "$OPERATING_SYSTEM" in
        macOS)
            # Use AppleScript via osascript with explicit display handling
            if command -v osascript &>/dev/null; then
                chosen_dir=$( { osascript -e 'tell application "System Events"
    activate
    set selected_folder to choose folder with prompt "Select ADSK Downloads Directory"
    return POSIX path of selected_folder
end tell' ; } 2>&1)
                
                if [[ $? -eq 0 && -n "$chosen_dir" && "$chosen_dir" != *"canceled"* ]]; then
                    echo "$chosen_dir"
                    return 0
                else
                    log_debug "osascript GUI cancelled or failed"
                    return 1
                fi
            else
                log_debug "osascript command not found"
                return 1
            fi
            ;;
        Linux)
            if command -v zenity &>/dev/null; then
                chosen_dir=$(zenity \
                    --file-selection \
                    --directory \
                    --title="Select ADSK Downloads Directory" \
                    --filename="$HOME/Downloads/" 2>/dev/null) || return 1
                echo "$chosen_dir"
                return 0
            else
                log_debug "zenity command not found"
                return 1
            fi
            ;;
        *)
            log_debug "GUI not supported on this OS"
            return 1
            ;;
    esac
}

select_directory() {
    local use_cli="${1:-false}"
    local chosen_dir=""
    
    if [[ "$use_cli" == "true" ]]; then
        chosen_dir=$(select_directory_cli "$HOME/Downloads")
    else
        # Try GUI first
        if chosen_dir=$(select_directory_gui 2>/dev/null); then
            echo "$chosen_dir"
            return 0
        else
            # GUI failed or cancelled, fall back to CLI
            echo "GUI not available, using command-line mode..." >&2
            chosen_dir=$(select_directory_cli "$HOME/Downloads")
        fi
    fi
    
    echo "$chosen_dir"
}

# -------------------------------------------------------------------------- #
# FILE COLLECTION
# -------------------------------------------------------------------------- #

collect_files() {
    local downloads_dir="$1"
    
    log_info "Scanning directory: $downloads_dir"
    
    local file_count=0
    while IFS= read -r -d '' file_path; do
        if [[ ! "$file_path" == *.md5 ]]; then
            file_list+=("$file_path")
            ((file_count++))
        fi
    done < <(find "$downloads_dir" -maxdepth 1 -type f -print0 2>/dev/null)
    
    if [[ $file_count -eq 0 ]]; then
        log_warn "No files found in $downloads_dir"
        return 1
    fi
    
    log_info "Found $file_count file(s) to validate"
    return 0
}

# -------------------------------------------------------------------------- #
# VALIDATION LOGIC
# -------------------------------------------------------------------------- #

validate_file() {
    local file_path="$1"
    local file_basename=$(basename "$file_path")
    
    log_info "Validating: $file_basename"
    
    local md5_file="$file_path.md5"
    
    # Add to report
    report_lines+=("  $((file_counter)). $file_basename")
    
    if [[ ! -e "$md5_file" ]]; then
        log_warn "No MD5 file found: ${file_basename}.md5"
        report_lines+=("")
        report_lines+=("     No corresponding .md5 file found.")
        report_lines+=("")
        report_lines+=("     Skipping $file_basename:")
        report_lines+=("")
        report_lines+=("$separator_plus")
        report_lines+=("")
        return 1
    fi
    
    local expected_md5
    expected_md5=$(cut -d' ' -f1 "$md5_file")
    
    if [[ -z "$expected_md5" ]]; then
        log_error "MD5 file is empty or malformed: $md5_file"
        report_lines+=("")
        report_lines+=("     MD5 file is empty or malformed.")
        report_lines+=("")
        report_lines+=("$separator_plus")
        report_lines+=("")
        return 1
    fi
    
    if [[ "$TEST_MODE" == "true" ]]; then
        log_debug "TEST MODE: Would validate $file_basename"
        report_lines+=("")
        report_lines+=("     TEST MODE: Validation skipped")
        report_lines+=("")
        report_lines+=("$separator_plus")
        report_lines+=("")
        return 0
    fi
    
    local calculated_md5
    calculated_md5=$(calculate_md5 "$file_path")
    
    log_debug "Expected MD5:   $expected_md5"
    log_debug "Calculated MD5: $calculated_md5"
    
    # Add to report
    report_lines+=("")
    report_lines+=("     Expected Checksum: $expected_md5")
    report_lines+=("     Actual Checksum:   $calculated_md5")
    
    if [[ "$calculated_md5" == "$expected_md5" ]]; then
        log_success "$file_basename - Checksum valid"
        report_lines+=("")
        report_lines+=("     Checksums match for $file_basename")
        report_lines+=("")
        report_lines+=("     This file is valid.")
        report_lines+=("")
        report_lines+=("$separator_plus")
        report_lines+=("")
        return 0
    else
        log_error "$file_basename - Checksum MISMATCH! File may be corrupted."
        report_lines+=("")
        report_lines+=("     Checksums DO NOT MATCH for $file_basename")
        report_lines+=("")
        report_lines+=("     This file may be corrupted.")
        report_lines+=("")
        report_lines+=("$separator_plus")
        report_lines+=("")
        return 1
    fi
}

# -------------------------------------------------------------------------- #
# MAIN PROCESSING
# -------------------------------------------------------------------------- #

print_banner() {
    cat << EOF

$separator_plus
  $PROGRAM_NAME_UC
$separator_plus
  Workstation: $WORKSTATION_NAME
  User:        $CURRENT_USER
  OS:          $OPERATING_SYSTEM
  Time:        $(date '+%Y-%m-%d %H:%M:%S')
$separator_plus

EOF
}

main() {
    print_banner
    log_info "$PROGRAM_NAME started"
    
    local use_cli_mode="$USE_CLI_MODE"
    local chosen_downloads_dir=""
    
    # Parse command-line arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -d|--directory)
                chosen_downloads_dir="$2"
                shift 2
                ;;
            -c|--cli)
                use_cli_mode=true
                shift
                ;;
            -q|--quiet)
                LOG_LEVEL=$LOG_ERROR
                shift
                ;;
            -v|--verbose)
                LOG_LEVEL=$LOG_DEBUG
                shift
                ;;
            -t|--test)
                TEST_MODE=true
                shift
                ;;
            -h|--help)
                print_usage
                exit "$EXIT_SUCCESS"
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit "$EXIT_ERROR"
                ;;
        esac
    done
    
    # Select directory if not provided
    if [[ -z "$chosen_downloads_dir" ]]; then
        chosen_downloads_dir=$(select_directory "$use_cli_mode")
    fi
    
    # Expand and validate
    chosen_downloads_dir="${chosen_downloads_dir/#\~/$HOME}"
    chosen_downloads_dir="${chosen_downloads_dir%/}"
    
    validate_directory "$chosen_downloads_dir" || \
        die "Invalid directory: $chosen_downloads_dir" "$EXIT_INVALID_DIR"
    
    log_info "Downloads directory: $chosen_downloads_dir"
    log_info ""
    
    # Initialize global file list array
    local file_list=()
    
    # Collect files
    collect_files "$chosen_downloads_dir" || \
        die "Failed to collect files" "$EXIT_NO_FILES"
    
    # Print file list
    log_info "Files to validate:"
    local count=1
    for file_path in "${file_list[@]}"; do
        log_info "  $count. $(basename "$file_path")"
        ((count++))
    done
    log_info ""
    
    # Validate each file
    local valid_count=0
    local invalid_count=0
    local file_counter=1
    local report_lines=()
    
    # Add header to report
    report_lines+=("")
    report_lines+=("$separator_plus")
    report_lines+=("")
    report_lines+=("  The list of files is:")
    for file_path in "${file_list[@]}"; do
        report_lines+=("")
        report_lines+=("    $file_counter. $(basename "$file_path")")
        ((file_counter++))
    done
    report_lines+=("")
    report_lines+=("$separator_plus")
    report_lines+=("")
    
    # Reset counter for validation
    file_counter=1
    
    for file_path in "${file_list[@]}"; do
        if validate_file "$file_path" report_lines; then
            ((valid_count++))
        else
            ((invalid_count++))
        fi
        ((file_counter++))
    done
    
    # Add summary to report
    report_lines+=("")
    report_lines+=("$separator_plus")
    report_lines+=("")
    report_lines+=("VALIDATION SUMMARY")
    report_lines+=("")
    report_lines+=("Total files:     ${#file_list[@]}")
    report_lines+=("Valid:           $valid_count")
    report_lines+=("Invalid/Missing: $invalid_count")
    report_lines+=("")
    report_lines+=("$separator_plus")
    report_lines+=("")
    
    # Write detailed report to downloads directory
    local report_timestamp=$(date +%Y%m%d_%H%M%S)
    local report_file="$chosen_downloads_dir/VALIDATION_REPORT_${report_timestamp}.txt"
    
    {
        echo ""
        echo "$separator_plus"
        echo ""
        echo "  VALIDATION REPORT"
        echo ""
        echo "  date: $(date '+%Y-%m-%d')"
        echo "  time: $(date '+%H:%M:%S')"
        echo "  now:  $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "$separator_plus"
        echo ""
        printf '%s\n' "${report_lines[@]}"
    } > "$report_file"
    
    log_success "Validation report written to: $report_file"
    
    # Print summary to terminal
    log_info ""
    log_info "================================================================================"
    log_info "VALIDATION SUMMARY"
    log_info "================================================================================"
    log_info "Total files:     ${#file_list[@]}"
    log_info "Valid:           $valid_count"
    log_info "Invalid/Missing: $invalid_count"
    log_info "================================================================================"
    log_info ""
    
    if [[ $invalid_count -eq 0 ]]; then
        log_success "All files validated successfully!"
        exit "$EXIT_SUCCESS"
    else
        log_error "$invalid_count file(s) failed validation"
        exit "$EXIT_ERROR"
    fi
}

# -------------------------------------------------------------------------- #
# SCRIPT ENTRY POINT
# -------------------------------------------------------------------------- #

main "$@"

# -------------------------------------------------------------------------- #
# 53 54 52 45 4E 47 54 48 2D 49 4E 2D 4E 55 4D 42 45 52 53 C2 A9 32 30 32 35 #
# -------------------------------------------------------------------------- #
# Changelist:
# -------------------------------------------------------------------------- #
# version:          0.0.1
# created:          2024-01-19 - 12:34:56
# comments:         scripts to create flame projekts, presets & templates.
# -------------------------------------------------------------------------- #
# version:          0.1.0
# modified:         2024-04-20 - 16:20:00
# comments:         refactored monolithic program into separate functions.
# -------------------------------------------------------------------------- #
# version:          0.5.0
# modified:         2024-05-24 - 20:24:00
# comments:         merged flame_colortoolkit with projekt.
# -------------------------------------------------------------------------- #
# version:          0.6.0
# modified:         2024-05-25 - 15:00:03
# comments:         started conversion to python3.
# -------------------------------------------------------------------------- #
# version:          0.7.0
# modified:         2024-06-21 - 18:21:03
# comments:         started gui design with pyside6.
# -------------------------------------------------------------------------- #
# version:          0.9.9
# modified:         2024-08-31 - 16:51:09
# comments:         prep for release - code appears to be functional
# -------------------------------------------------------------------------- #
# Version:          1.9.9
# modified:         2024-12-25 - 09:50:16
# comments:         Preparation for future features
# -------------------------------------------------------------------------- #
# Version:          2027.0.0
# modified:         2025-11-20 - 11:57:00
# comments:         Improved validate-downloads.sh with CLI and GUI modes.
# -------------------------------------------------------------------------- #