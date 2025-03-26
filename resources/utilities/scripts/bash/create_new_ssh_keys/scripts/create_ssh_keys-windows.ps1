<#
.SYNOPSIS
    Generates SSH keys and creates an encrypted backup with enhanced security measures for Windows.
.DESCRIPTION
    This script will generate SSH keys (ED25519 and RSA) and create an encrypted backup.
    It includes secure password handling, proper error management, and helper scripts for decryption.
.NOTES
    Program Name:     Create-SSHKeys.ps1
    Version:          4.0.0 (Windows)
    Original Author:  Phil MAN - phil_man@mac.com
    Modified by:      Claude
    Created:          2024-03-12
    Modified:         2024-02-16

    Changelist:       Enhanced security, improved error handling, removed deprecated DSA keys,
                      added secure file operations, improved password handling, converted for Windows
#>

# Stop on error
$ErrorActionPreference = "Stop"

# Add Windows Forms
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# ========================================================================== #
# Functions and Setup
# ========================================================================== #

# Error handling function
function Handle-Error {
    param (
        [Parameter(Mandatory = $true)]
        [string]$ErrorMessage
    )
    
    [System.Windows.Forms.MessageBox]::Show(
        $ErrorMessage,
        "Error",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    )
    Cleanup
    exit 1
}

# Cleanup function
function Cleanup {
    # Securely delete sensitive files
    if (Test-Path -Path $tarFilePath) {
        Secure-Delete -Path $tarFilePath
    }
    
    # Clear sensitive variables
    if (Get-Variable -Name "myPassword" -ErrorAction SilentlyContinue) {
        Remove-Variable -Name "myPassword" -Scope Script
    }
    if (Get-Variable -Name "confirmPassword" -ErrorAction SilentlyContinue) {
        Remove-Variable -Name "confirmPassword" -Scope Script
    }
}

# Secure file deletion for Windows
function Secure-Delete {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Path
    )
    
    # Overwrite the file with random data 3 times
    for ($i = 0; $i -lt 3; $i++) {
        $randomBytes = New-Object byte[] (100MB)
        $rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
        $rng.GetBytes($randomBytes)
        
        [System.IO.File]::WriteAllBytes($Path, $randomBytes)
    }
    
    # Delete the file
    Remove-Item -Path $Path -Force
}

# Check dependencies
function Check-Dependencies {
    $deps = @("ssh-keygen", "openssl")
    $missing = @()
    
    foreach ($dep in $deps) {
        if (-not (Get-Command $dep -ErrorAction SilentlyContinue)) {
            $missing += $dep
        }
    }
    
    if ($missing.Count -gt 0) {
        $message = "Missing required dependencies: $($missing -join ', ')"
        [System.Windows.Forms.MessageBox]::Show(
            $message,
            "Error",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
        exit 1
    }
}

# Email validation function
function Validate-Email {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Email
    )
    
    $emailRegex = "^[[:alnum:]]([-._[:alnum:]]*[[:alnum:]])*@[[:alnum:]]([-._[:alnum:]]*[[:alnum:]])*\.[[:alpha:]]{2,}$"
    
    if ($Email -notmatch $emailRegex) {
        [System.Windows.Forms.MessageBox]::Show(
            "Invalid email format. Please ensure:`n- No special characters except . - _`n- Valid domain format`n- At least 2 character domain extension",
            "Error",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
        return $false
    }
    return $true
}

# Password strength validation
function Validate-PasswordStrength {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Password
    )
    
    $minLength = 12
    
    if ($Password.Length -lt $minLength) {
        [System.Windows.Forms.MessageBox]::Show(
            "Password must be at least $minLength characters long",
            "Error",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
        return $false
    }
    
    if (-not ($Password -cmatch "[A-Z]") -or 
        -not ($Password -cmatch "[a-z]") -or 
        -not ($Password -cmatch "[0-9]") -or 
        -not ($Password -cmatch "[^a-zA-Z0-9]")) {
        [System.Windows.Forms.MessageBox]::Show(
            "Password must contain:`n- Uppercase letters`n- Lowercase letters`n- Numbers`n- Special characters",
            "Error",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
        return $false
    }
    return $true
}

# Windows folder selection dialog
function Choose-Folder {
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "Choose Folder to Save New SSH Keys"
    $folderBrowser.RootFolder = [System.Environment+SpecialFolder]::MyComputer
    
    if ($folderBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        return $folderBrowser.SelectedPath
    }
    return $null
}

# Windows text input dialog
function Get-TextInput {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Prompt
    )
    
    $form = New-Object System.Windows.Forms.Form
    $form.Text = $Prompt
    $form.Size = New-Object System.Drawing.Size(400, 200)
    $form.StartPosition = "CenterScreen"
    
    $textBox = New-Object System.Windows.Forms.TextBox
    $textBox.Location = New-Object System.Drawing.Point(10, 40)
    $textBox.Size = New-Object System.Drawing.Size(365, 20)
    
    $label = New-Object System.Windows.Forms.Label
    $label.Location = New-Object System.Drawing.Point(10, 20)
    $label.Size = New-Object System.Drawing.Size(365, 20)
    $label.Text = $Prompt
    
    $okButton = New-Object System.Windows.Forms.Button
    $okButton.Location = New-Object System.Drawing.Point(140, 100)
    $okButton.Size = New-Object System.Drawing.Size(75, 23)
    $okButton.Text = "OK"
    $okButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
    
    $cancelButton = New-Object System.Windows.Forms.Button
    $cancelButton.Location = New-Object System.Drawing.Point(220, 100)
    $cancelButton.Size = New-Object System.Drawing.Size(75, 23)
    $cancelButton.Text = "Cancel"
    $cancelButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    
    $form.AcceptButton = $okButton
    $form.CancelButton = $cancelButton
    
    $form.Controls.Add($textBox)
    $form.Controls.Add($label)
    $form.Controls.Add($okButton)
    $form.Controls.Add($cancelButton)
    
    $result = $form.ShowDialog()
    
    if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
        return $textBox.Text
    }
    return $null
}

# Windows password input dialog
function Get-PasswordInput {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Prompt
    )
    
    $form = New-Object System.Windows.Forms.Form
    $form.Text = $Prompt
    $form.Size = New-Object System.Drawing.Size(400, 200)
    $form.StartPosition = "CenterScreen"
    
    $textBox = New-Object System.Windows.Forms.MaskedTextBox
    $textBox.Location = New-Object System.Drawing.Point(10, 40)
    $textBox.Size = New-Object System.Drawing.Size(365, 20)
    $textBox.PasswordChar = "*"
    
    $label = New-Object System.Windows.Forms.Label
    $label.Location = New-Object System.Drawing.Point(10, 20)
    $label.Size = New-Object System.Drawing.Size(365, 20)
    $label.Text = $Prompt
    
    $okButton = New-Object System.Windows.Forms.Button
    $okButton.Location = New-Object System.Drawing.Point(140, 100)
    $okButton.Size = New-Object System.Drawing.Size(75, 23)
    $okButton.Text = "OK"
    $okButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
    
    $cancelButton = New-Object System.Windows.Forms.Button
    $cancelButton.Location = New-Object System.Drawing.Point(220, 100)
    $cancelButton.Size = New-Object System.Drawing.Size(75, 23)
    $cancelButton.Text = "Cancel"
    $cancelButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    
    $form.AcceptButton = $okButton
    $form.CancelButton = $cancelButton
    
    $form.Controls.Add($textBox)
    $form.Controls.Add($label)
    $form.Controls.Add($okButton)
    $form.Controls.Add($cancelButton)
    
    $result = $form.ShowDialog()
    
    if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
        return $textBox.Text
    }
    return $null
}

# Windows confirmation dialog
function Show-Confirmation {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message
    )
    
    $result = [System.Windows.Forms.MessageBox]::Show(
        $Message,
        "Confirmation",
        [System.Windows.Forms.MessageBoxButtons]::YesNo,
        [System.Windows.Forms.MessageBoxIcon]::Question
    )
    
    return $result -eq [System.Windows.Forms.DialogResult]::Yes
}

# Windows information dialog
function Show-Info {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message
    )
    
    [System.Windows.Forms.MessageBox]::Show(
        $Message,
        "Information",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )
}

# ========================================================================== #
# Main Script
# ========================================================================== #

try {
    # Check dependencies
    Check-Dependencies
    
    # Define today's date
    $today = Get-Date -Format "yyyy_MM_dd-HH_mm_ss"
    
    # Prompt user to choose a folder
    $chosenFolder = Choose-Folder
    if ($null -eq $chosenFolder) {
        Handle-Error "Operation cancelled. Exiting."
    }
    
    # Create an enclosing folder
    $sshKeysFolder = Join-Path -Path $chosenFolder -ChildPath "ssh_keys-$today"
    New-Item -Path $sshKeysFolder -ItemType Directory -Force | Out-Null
    
    # Setup logging with reduced sensitive information
    $sshKeyCreationLog = Join-Path -Path $sshKeysFolder -ChildPath "$today-ssh_key_creation_log.txt"
    New-Item -Path $sshKeyCreationLog -ItemType File -Force | Out-Null
    
    # Get and validate email address
    do {
        $emailAddress = Get-TextInput "Enter your email address:"
        if ($null -eq $emailAddress) {
            Handle-Error "Operation cancelled. Exiting."
        }
    } while (-not (Validate-Email -Email $emailAddress))
    
    # Enhanced password collection with strength validation
    $passwordMatch = $false
    do {
        $myPassword = Get-PasswordInput "Enter Password (min 12 chars, mixed case, numbers, symbols):"
        if ($null -eq $myPassword) {
            Handle-Error "Operation cancelled. Exiting."
        }
        
        if (-not (Validate-PasswordStrength -Password $myPassword)) {
            continue
        }
        
        $confirmPassword = Get-PasswordInput "Confirm Password:"
        if ($null -eq $confirmPassword) {
            Handle-Error "Operation cancelled. Exiting."
        }
        
        if ($myPassword -eq $confirmPassword) {
            $passwordMatch = $true
        } else {
            [System.Windows.Forms.MessageBox]::Show(
                "Passwords do not match. Please try again.",
                "Error",
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Error
            )
        }
    } while (-not $passwordMatch)
    
    # Ensure .ssh directory exists
    $sshDir = "$env:USERPROFILE\.ssh"
    if (-not (Test-Path -Path $sshDir)) {
        New-Item -Path $sshDir -ItemType Directory | Out-Null
    }
    
    # Define SSH key paths
    $sshkeyPathEd25519 = "$sshDir\id_ed25519-$today"
    $sshkeyPathRsa = "$sshDir\id_rsa-$today"
    
    # Generate ED25519 key
    $ed25519Params = @(
        "-t", "ed25519",
        "-a", "100",
        "-C", "$today - $emailAddress",
        "-f", $sshkeyPathEd25519,
        "-N", "`"$myPassword`""
    )
    & ssh-keygen $ed25519Params | Out-File -FilePath $sshKeyCreationLog -Append
    
    # Generate RSA key
    $rsaParams = @(
        "-t", "rsa",
        "-b", "4096",
        "-E", "sha512",
        "-a", "100",
        "-C", "$today - $emailAddress",
        "-f", $sshkeyPathRsa,
        "-N", "`"$myPassword`""
    )
    & ssh-keygen $rsaParams | Out-File -FilePath $sshKeyCreationLog -Append
    
    # Define the filepaths for the tar files (using zip for Windows)
    $tarFilePath = Join-Path -Path $sshKeysFolder -ChildPath "ssh_keys_$today.zip"
    $encryptedTarFilename = "encrypted_ssh_keys_$today.zip.enc"
    $encryptedTarFilepath = Join-Path -Path $sshKeysFolder -ChildPath $encryptedTarFilename
    
    # Create a zip file of the private keys
    Compress-Archive -Path "$sshkeyPathEd25519", "$sshkeyPathRsa" -DestinationPath $tarFilePath
    
    # Convert password to secure string for OpenSSL
    $passwordBytes = [System.Text.Encoding]::UTF8.GetBytes($myPassword)
    $tempPasswordFile = [System.IO.Path]::GetTempFileName()
    [System.IO.File]::WriteAllBytes($tempPasswordFile, $passwordBytes)
    
    # Encrypt the zip file
    & openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -salt -in $tarFilePath -out $encryptedTarFilepath -pass "file:$tempPasswordFile"
    
    # Securely delete the temporary password file
    Secure-Delete -Path $tempPasswordFile
    
    # Verify encryption was successful
    if (-not (Test-Path -Path $encryptedTarFilepath)) {
        Handle-Error "Failed to create encrypted backup. Exiting."
    }
    
    # Copy public keys to the chosen folder
    Copy-Item -Path "$sshkeyPathEd25519.pub" -Destination $sshKeysFolder
    Copy-Item -Path "$sshkeyPathRsa.pub" -Destination $sshKeysFolder
    
    # Generate decryption script for Windows
    $decryptScript = @"
# PowerShell script to decrypt SSH keys
# Run this script in PowerShell to decrypt your SSH keys

# Add Windows Forms assembly
Add-Type -AssemblyName System.Windows.Forms

# Password input dialog
function Get-PasswordInput {
    `$form = New-Object System.Windows.Forms.Form
    `$form.Text = "Enter Password"
    `$form.Size = New-Object System.Drawing.Size(400, 200)
    `$form.StartPosition = "CenterScreen"
    
    `$textBox = New-Object System.Windows.Forms.MaskedTextBox
    `$textBox.Location = New-Object System.Drawing.Point(10, 40)
    `$textBox.Size = New-Object System.Drawing.Size(365, 20)
    `$textBox.PasswordChar = "*"
    
    `$label = New-Object System.Windows.Forms.Label
    `$label.Location = New-Object System.Drawing.Point(10, 20)
    `$label.Size = New-Object System.Drawing.Size(365, 20)
    `$label.Text = "Enter Password"
    
    `$okButton = New-Object System.Windows.Forms.Button
    `$okButton.Location = New-Object System.Drawing.Point(140, 100)
    `$okButton.Size = New-Object System.Drawing.Size(75, 23)
    `$okButton.Text = "OK"
    `$okButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
    
    `$cancelButton = New-Object System.Windows.Forms.Button
    `$cancelButton.Location = New-Object System.Drawing.Point(220, 100)
    `$cancelButton.Size = New-Object System.Drawing.Size(75, 23)
    `$cancelButton.Text = "Cancel"
    `$cancelButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    
    `$form.AcceptButton = `$okButton
    `$form.CancelButton = `$cancelButton
    
    `$form.Controls.Add(`$textBox)
    `$form.Controls.Add(`$label)
    `$form.Controls.Add(`$okButton)
    `$form.Controls.Add(`$cancelButton)
    
    `$result = `$form.ShowDialog()
    
    if (`$result -eq [System.Windows.Forms.DialogResult]::OK) {
        return `$textBox.Text
    }
    return `$null
}

# Define script path and current directory
`$scriptPath = `$MyInvocation.MyCommand.Path
`$currentDir = Split-Path -Parent `$scriptPath

# Change to the directory of the running script
Set-Location -Path `$currentDir

# Get encrypted file
`$encryptedFile = Get-ChildItem -Path "encrypted_ssh_keys_*.zip.enc" | Select-Object -First 1

if (-not `$encryptedFile) {
    [System.Windows.Forms.MessageBox]::Show(
        "No encrypted SSH key file found.",
        "Error",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    )
    exit 1
}

# Prompt for password
`$password = Get-PasswordInput

if ([string]::IsNullOrEmpty(`$password)) {
    [System.Windows.Forms.MessageBox]::Show(
        "Password cannot be empty. Exiting.",
        "Error",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    )
    exit 1
}

# Create temporary password file
`$passwordBytes = [System.Text.Encoding]::UTF8.GetBytes(`$password)
`$tempPasswordFile = [System.IO.Path]::GetTempFileName()
[System.IO.File]::WriteAllBytes(`$tempPasswordFile, `$passwordBytes)

# Output filename
`$today = Get-Date -Format "yyyy_MM_dd-HH_mm_ss"
`$outputFile = "decrypted_ssh_keys_`$today.zip"

# Decrypt the file
`$processStartInfo = New-Object System.Diagnostics.ProcessStartInfo
`$processStartInfo.FileName = "openssl"
`$processStartInfo.Arguments = "enc -d -aes-256-cbc -pbkdf2 -iter 100000 -salt -in `"`$(`$encryptedFile.FullName)`" -out `"`$outputFile`" -pass file:`"`$tempPasswordFile`""
`$processStartInfo.RedirectStandardOutput = `$true
`$processStartInfo.RedirectStandardError = `$true
`$processStartInfo.UseShellExecute = `$false
`$processStartInfo.CreateNoWindow = `$true

`$process = New-Object System.Diagnostics.Process
`$process.StartInfo = `$processStartInfo
`$process.Start() | Out-Null
`$process.WaitForExit()

# Clean up the temporary password file
if (Test-Path -Path `$tempPasswordFile) {
    # Overwrite with random data
    `$randomBytes = New-Object byte[] (1MB)
    `$rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
    `$rng.GetBytes(`$randomBytes)
    [System.IO.File]::WriteAllBytes(`$tempPasswordFile, `$randomBytes)
    # Delete the file
    Remove-Item -Path `$tempPasswordFile -Force
}

# Clear the password from memory
`$password = `$null
[System.GC]::Collect()

if (Test-Path -Path `$outputFile) {
    [System.Windows.Forms.MessageBox]::Show(
        "Decryption completed successfully.",
        "Success",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )
} else {
    [System.Windows.Forms.MessageBox]::Show(
        "Decryption failed. Check your password and try again.",
        "Error",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    )
}
"@
    
    $decryptScriptPath = Join-Path -Path $sshKeysFolder -ChildPath "Decrypt-SSHKeys.ps1"
    Set-Content -Path $decryptScriptPath -Value $decryptScript
    
    # Generate extraction script for Windows
    $extractScript = @"
# PowerShell script to extract SSH keys
# Run this script in PowerShell to extract your decrypted SSH keys

# Add Windows Forms assembly
Add-Type -AssemblyName System.Windows.Forms

# Define script path and current directory
`$scriptPath = `$MyInvocation.MyCommand.Path
`$currentDir = Split-Path -Parent `$scriptPath

# Change to the directory of the running script
Set-Location -Path `$currentDir

# Get decrypted file
`$decryptedFile = Get-ChildItem -Path "decrypted_ssh_keys_*.zip" | Select-Object -First 1

if (-not `$decryptedFile) {
    [System.Windows.Forms.MessageBox]::Show(
        "No decrypted SSH key file found. Run the Decrypt-SSHKeys.ps1 script first.",
        "Error",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    )
    exit 1
}

# Extract the zip file
Expand-Archive -Path `$decryptedFile.FullName -DestinationPath . -Force

# Secure delete the decrypted zip file
`$randomBytes = New-Object byte[] (100MB)
`$rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
`$rng.GetBytes(`$randomBytes)
[System.IO.File]::WriteAllBytes(`$decryptedFile.FullName, `$randomBytes)
Remove-Item -Path `$decryptedFile.FullName -Force

[System.Windows.Forms.MessageBox]::Show(
    "Extraction completed successfully.",
    "Success",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Information
)
"@
    
    $extractScriptPath = Join-Path -Path $sshKeysFolder -ChildPath "Extract-SSHKeys.ps1"
    Set-Content -Path $extractScriptPath -Value $extractScript
    
    # Secure deletion of the unencrypted zip file
    Secure-Delete -Path $tarFilePath
    
    # Add SSH keys to SSH agent if requested
    if (Show-Confirmation "SSH keys generated and encrypted. Do you want to add them to the SSH agent?") {
        try {
            & ssh-add $sshkeyPathEd25519
            & ssh-add $sshkeyPathRsa
            Show-Info "SSH keys successfully added to SSH agent."
        } catch {
            [System.Windows.Forms.MessageBox]::Show(
                "Failed to add SSH keys to SSH agent.`nYou can add them manually later using ssh-add.",
                "Warning",
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Warning
            )
        }
    } else {
        Show-Info "SSH keys were not added to SSH agent.`nYou can add them manually later using ssh-add."
    }
    
    # Final cleanup
    Cleanup
    
    # Show summary of actions
    Show-Info "Script finished successfully.`n`nKeys were generated in: $sshKeysFolder`n`nEncrypted backup created: $encryptedTarFilename`n`nUse Decrypt-SSHKeys.ps1 and Extract-SSHKeys.ps1 scripts to restore keys when needed."
    
} catch {
    Handle-Error "An unexpected error occurred: $_"
}

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
# version:               4.0.0 (Windows)
# modified:              2024-02-16
# comments:              Converted to PowerShell for Windows, replaced Zenity with Windows Forms