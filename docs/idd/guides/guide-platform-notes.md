# IDD Platform-Specific Notes

Platform-specific instructions and considerations for Issue-Driven Development.

## Table of Contents

- [macOS](#macos)
- [Linux](#linux)
- [Windows / WSL](#windows--wsl)
- [GitHub Enterprise](#github-enterprise)
- [Self-Hosted Runners](#self-hosted-runners)
- [Docker](#docker)

---

## macOS

### Prerequisites Installation

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install prerequisites
brew install git python gh

# Verify
git --version       # Should be 2.25+
python3 --version   # Should be 3.9+
gh --version        # Should be 2.0+
```

### Path Configuration

```bash
# Add to ~/.zshrc or ~/.bash_profile
export PATH="/usr/local/bin:$PATH"
export PATH="/usr/local/opt/python@3.11/bin:$PATH"

# Reload
source ~/.zshrc
```

### Python Environment

```bash
# macOS includes Python 3.9+ by default (macOS 12+)
python3 --version

# Or use Homebrew Python
brew install python@3.11
python3.11 --version

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

### Git Configuration

```bash
# Set credential helper
git config --global credential.helper osxkeychain

# Configure line endings
git config --global core.autocrlf input
```

### GitHub CLI Setup

```bash
# Authenticate
gh auth login

# Set default editor
gh config set editor "code --wait"  # VS Code
# OR
gh config set editor "vim"          # Vim
```

### Common macOS Issues

**Issue: Command line tools not found**
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

**Issue: Permission denied on /usr/local**
```bash
# Fix Homebrew permissions
sudo chown -R $(whoami) /usr/local/bin /usr/local/lib
```

**Issue: Python SSL certificate error**
```bash
# Install certificates
cd /Applications/Python\ 3.11/
./Install\ Certificates.command
```

### Recommended Tools

- **Terminal:** iTerm2 (`brew install --cask iterm2`)
- **Editor:** VS Code (`brew install --cask visual-studio-code`)
- **Git GUI:** GitKraken or Tower
- **Python:** pyenv for version management (`brew install pyenv`)

---

## Linux

### Ubuntu / Debian

```bash
# Update package list
sudo apt-get update

# Install prerequisites
sudo apt-get install -y git python3 python3-pip python3-venv

# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
  sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
  sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

sudo apt-get update
sudo apt-get install gh

# Verify
git --version
python3 --version
gh --version
```

### Fedora / RHEL / CentOS

```bash
# Install prerequisites
sudo dnf install -y git python3 python3-pip

# Install GitHub CLI
sudo dnf install 'dnf-command(config-manager)'
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh

# Verify
git --version
python3 --version
gh --version
```

### Arch Linux

```bash
# Install prerequisites
sudo pacman -S git python python-pip github-cli

# Verify
git --version
python --version
gh --version
```

### Python Virtual Environment

```bash
# Install venv (if not included)
sudo apt-get install python3-venv  # Ubuntu/Debian
sudo dnf install python3-venv      # Fedora

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Permissions

```bash
# If running as non-root user
# Ensure write permissions to repository
chown -R $USER:$USER ~/your-repo

# If using system Python
# Use user install
pip3 install --user -r requirements.txt
```

### Systemd Service (Optional)

Run IDD sync as a service:

```bash
# Create service file
sudo tee /etc/systemd/system/idd-sync.service > /dev/null <<EOF
[Unit]
Description=IDD Issue Sync
After=network.target

[Service]
Type=oneshot
User=$USER
WorkingDirectory=/path/to/repo
ExecStart=/path/to/repo/.venv/bin/python3 /path/to/repo/bin/sync-issues-to-todo.py

[Install]
WantedBy=multi-user.target
EOF

# Create timer
sudo tee /etc/systemd/system/idd-sync.timer > /dev/null <<EOF
[Unit]
Description=IDD Issue Sync Timer

[Timer]
OnBootSec=5min
OnUnitActiveSec=6h

[Install]
WantedBy=timers.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable --now idd-sync.timer
sudo systemctl status idd-sync.timer
```

### Common Linux Issues

**Issue: ModuleNotFoundError despite pip install**
```bash
# Ensure using correct Python
which python3
python3 -m pip list | grep PyGithub

# Use absolute path
/usr/bin/python3 -m pip install -r requirements.txt
```

**Issue: Permission denied on git operations**
```bash
# Check SSH keys
ssh -T git@github.com

# Or use HTTPS
git remote set-url origin https://github.com/owner/repo.git
```

---

## Windows / WSL

### Windows Subsystem for Linux (Recommended)

**Install WSL 2:**
```powershell
# PowerShell (as Administrator)
wsl --install
wsl --set-default-version 2
```

**Install Ubuntu:**
```powershell
wsl --install -d Ubuntu
```

**Inside WSL, follow Linux instructions:**
```bash
# Update
sudo apt-get update && sudo apt-get upgrade

# Install prerequisites
sudo apt-get install -y git python3 python3-pip python3-venv

# Install GitHub CLI
# (See Linux section above)
```

### Native Windows

**Prerequisites:**

1. **Git for Windows:** https://git-scm.com/download/win
2. **Python:** https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH"
   - ✅ Install pip
3. **GitHub CLI:** https://cli.github.com/

**PowerShell Setup:**
```powershell
# Verify installations
git --version
python --version
gh --version

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

**Command Prompt Setup:**
```cmd
# Activate virtual environment
.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### Path Differences

```bash
# Linux/macOS
source .venv/bin/activate
python3 bin/sync-issues-to-todo.py

# Windows
.venv\Scripts\Activate.ps1  # PowerShell
.venv\Scripts\activate.bat  # Command Prompt
python bin\sync-issues-to-todo.py
```

### Line Ending Issues

```bash
# Configure Git for Windows
git config --global core.autocrlf true

# Or convert files
dos2unix bin/*.sh  # If available
```

### Windows-Specific Issues

**Issue: Script won't run**
```powershell
# Run with Python explicitly
python bin/sync-issues-to-todo.py

# Don't rely on shebang (#!) on Windows
```

**Issue: Long path names**
```powershell
# Enable long paths
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### Recommended Setup

1. **Use WSL 2** for best compatibility
2. **VS Code** with Remote-WSL extension
3. **Windows Terminal** for better terminal experience

---

## GitHub Enterprise

### Setup Differences

```bash
# Set GitHub Enterprise URL
gh config set gh_host github.enterprise.com

# Authenticate
gh auth login --hostname github.enterprise.com

# Configure Git
git config --global url."https://github.enterprise.com/".insteadOf "https://github.com/"
```

### Environment Variables

```bash
# .env file
GITHUB_API_URL=https://github.enterprise.com/api/v3
GITHUB_HOST=github.enterprise.com
```

### Script Configuration

Update scripts to use enterprise URL:

```python
# In Python scripts
from github import Github

# Use enterprise URL
g = Github(base_url="https://github.enterprise.com/api/v3", login_or_token=token)
```

### Workflow Configuration

```yaml
# .github/workflows/issue-to-todo-sync.yml
env:
  GITHUB_API_URL: https://github.enterprise.com/api/v3
```

### SSL Certificates

If using self-signed certificates:

```bash
# Disable SSL verification (not recommended for production)
export PYTHONHTTPSVERIFY=0
gh config set http_verify false

# Or add certificate to system trust store
sudo cp your-cert.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

### Proxy Configuration

```bash
# Set proxy
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1,.company.com

# Git proxy
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy http://proxy.company.com:8080

# Python pip proxy
pip install --proxy http://proxy.company.com:8080 -r requirements.txt
```

---

## Self-Hosted Runners

### Runner Setup

```bash
# Download runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure
./config.sh --url https://github.com/owner/repo --token YOUR_TOKEN

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start
```

### Workflow Configuration

```yaml
# Use self-hosted runner
jobs:
  sync:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v3
      - name: Run sync
        run: |
          source .venv/bin/activate
          python3 bin/sync-issues-to-todo.py
```

### Prerequisites on Runner

```bash
# Install on runner machine
# Python, Git, etc.
sudo apt-get install -y python3 python3-pip git

# Install GitHub CLI
# (See Linux section)

# Create working directory
sudo mkdir -p /opt/idd
sudo chown runner:runner /opt/idd

# Install IDD dependencies
cd /opt/idd
python3 -m venv .venv
source .venv/bin/activate
pip install PyGithub python-dotenv GitPython
```

### Security Considerations

- Use dedicated user for runner
- Limit runner permissions
- Use secrets for sensitive data
- Regular security updates
- Monitor runner logs

---

## Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Install git and GitHub CLI
RUN apt-get update && \
    apt-get install -y git curl && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
    dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
    tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy IDD files
COPY bin/ bin/
COPY idd-config.yml .

# Run sync
CMD ["python3", "bin/sync-issues-to-todo.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  idd-sync:
    build: .
    volumes:
      - ./TO-DO.md:/app/TO-DO.md
      - ./.ai-context:/app/.ai-context
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    restart: unless-stopped
```

### Running in Docker

```bash
# Build image
docker build -t idd:latest .

# Run sync
docker run --rm \
  -v $(pwd)/TO-DO.md:/app/TO-DO.md \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  idd:latest

# Or with compose
docker-compose run idd-sync
```

---

## Platform Comparison

| Feature | macOS | Linux | Windows | WSL |
|---------|-------|-------|---------|-----|
| **Setup Difficulty** | Easy | Easy | Medium | Easy |
| **Performance** | Excellent | Excellent | Good | Very Good |
| **Compatibility** | 100% | 100% | 95% | 100% |
| **Recommended** | ✅ Yes | ✅ Yes | ⚠️ Use WSL | ✅ Yes |

## Best Practices by Platform

### macOS
- Use Homebrew for package management
- Keep Xcode Command Line Tools updated
- Use pyenv for Python version management

### Linux
- Use package manager (apt, dnf, pacman)
- Consider systemd for automation
- Use pyenv or system Python

### Windows
- Use WSL 2 for best experience
- Keep Windows Terminal updated
- Use VS Code with Remote-WSL

### GitHub Enterprise
- Document enterprise-specific setup
- Test with self-signed certificates
- Configure proxy settings

### Self-Hosted Runners
- Regular security updates
- Monitor resource usage
- Use dedicated machines

---

**Need platform-specific help? Open an issue with the "platform" label!**
