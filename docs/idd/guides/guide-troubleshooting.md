# IDD Troubleshooting Guide

Solutions to common issues when setting up and using Issue-Driven Development.

## Table of Contents

- [Setup Issues](#setup-issues)
- [GitHub Actions](#github-actions)
- [Python Environment](#python-environment)
- [Script Errors](#script-errors)
- [Workflow Issues](#workflow-issues)
- [Permission Problems](#permission-problems)
- [FAQ](#faq)

---

## Setup Issues

### Setup script won't run

**Problem:** `./bin/setup-idd.sh: Permission denied`

**Solution:**
```bash
# Make script executable
chmod +x bin/setup-idd.sh

# Run again
./bin/setup-idd.sh
```

### Prerequisites check fails

**Problem:** Missing Git, Python, or GitHub CLI

**Solution:**
```bash
# macOS
brew install git python gh

# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install git python3 python3-pip
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt-get update
sudo apt-get install gh

# Verify
git --version
python3 --version
gh --version
```

### GitHub CLI not authenticated

**Problem:** `gh auth status` shows not logged in

**Solution:**
```bash
# Login interactively
gh auth login

# Select:
# - GitHub.com
# - HTTPS
# - Yes (authenticate Git)
# - Login with browser

# Verify
gh auth status

# Alternative: Use token
gh auth login --with-token < token.txt
```

### Python version too old

**Problem:** Python 3.8 or older

**Solution:**
```bash
# Check version
python3 --version

# macOS - Install Python 3.9+
brew install python@3.11

# Linux - Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.11

# Verify
python3.11 --version

# Update alternatives
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

---

## GitHub Actions

### Workflows not appearing

**Problem:** Workflows don't show in Actions tab

**Solutions:**

1. **Check Actions are enabled:**
```bash
# Via CLI
gh api repos/:owner/:repo --jq .has_issues

# Via UI
# Settings → Actions → General → Enable Actions
```

2. **Check workflow files:**
```bash
# Workflows must be in correct location
ls -la .github/workflows/

# Workflow files must have .yml or .yaml extension
```

3. **Check syntax:**
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/issue-to-todo-sync.yml'))"
```

4. **Push to default branch:**
```bash
# Workflows only appear after push to main/master
git push origin main
```

### Workflow runs fail immediately

**Problem:** Workflow fails at checkout step

**Solutions:**

1. **Check GITHUB_TOKEN permissions:**
```yaml
# Add to workflow file
permissions:
  contents: write
  issues: read
  pull-requests: read
```

2. **Check repository visibility:**
```bash
# Private repos need token with repo scope
gh auth refresh -s repo
```

3. **Check branch protection:**
```bash
# Workflows may need branch protection bypass
# Settings → Branches → Edit rule → Allow specified actors
```

### "Resource not accessible by integration" error

**Problem:** Workflow can't access resources

**Solution:**
```yaml
# Update workflow permissions
name: Issue Sync
on: [issues]

permissions:
  contents: write  # For committing TO-DO.md
  issues: read     # For reading issues

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      # ...
```

### Scheduled workflows don't run

**Problem:** Cron schedule not triggering

**Solutions:**

1. **Check schedule syntax:**
```yaml
on:
  schedule:
    - cron: "0 */6 * * *"  # Every 6 hours
    # Format: minute hour day month weekday
    # Use https://crontab.guru/ to verify
```

2. **Repository activity required:**
```
Scheduled workflows may not run if repository is inactive.
Push a commit to wake them up.
```

3. **Manual trigger:**
```bash
# Trigger manually
gh workflow run issue-to-todo-sync.yml

# Or add workflow_dispatch
on:
  schedule:
    - cron: "0 */6 * * *"
  workflow_dispatch:  # Add this for manual trigger
```

---

## Python Environment

### Virtual environment creation fails

**Problem:** `python3 -m venv .venv` fails

**Solutions:**

1. **Install venv module:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# macOS (usually included)
python3 -m pip install virtualenv
```

2. **Use alternative:**
```bash
# Use virtualenv instead
pip3 install virtualenv
virtualenv .venv
```

3. **Check disk space:**
```bash
df -h .
# Ensure at least 500MB free
```

### Package installation fails

**Problem:** `pip install -r requirements.txt` fails

**Solutions:**

1. **Upgrade pip:**
```bash
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. **Install build tools:**
```bash
# macOS
xcode-select --install

# Linux
sudo apt-get install build-essential python3-dev
```

3. **Install packages individually:**
```bash
pip install PyGithub
pip install python-dotenv
pip install GitPython
```

4. **Check network:**
```bash
# Test PyPI connection
curl https://pypi.org

# Use mirror if needed
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### "ModuleNotFoundError" when running scripts

**Problem:** `ModuleNotFoundError: No module named 'github'`

**Solutions:**

1. **Activate virtual environment:**
```bash
source .venv/bin/activate
python3 bin/sync-issues-to-todo.py
```

2. **Check installation:**
```bash
source .venv/bin/activate
pip list | grep -i github
# Should show PyGithub

# Reinstall if missing
pip install PyGithub
```

3. **Use absolute path:**
```bash
.venv/bin/python3 bin/sync-issues-to-todo.py
```

### Wrong Python version in venv

**Problem:** Virtual environment uses wrong Python

**Solution:**
```bash
# Specify Python version explicitly
python3.11 -m venv .venv

# Or recreate
rm -rf .venv
/usr/local/bin/python3 -m venv .venv
```

---

## Script Errors

### "Permission denied" when running scripts

**Problem:** Scripts aren't executable

**Solution:**
```bash
# Make all scripts executable
chmod +x bin/*.sh
chmod +x bin/*.py

# Or run with python explicitly
python3 bin/sync-issues-to-todo.py
```

### "No such file or directory" errors

**Problem:** Script can't find files

**Solutions:**

1. **Run from repository root:**
```bash
# Always run from repo root
cd /path/to/repo
python3 bin/sync-issues-to-todo.py
```

2. **Check file paths:**
```bash
# Verify files exist
ls -la bin/sync-issues-to-todo.py
ls -la idd-config.yml
```

3. **Use absolute paths:**
```yaml
# In idd-config.yml
files:
  todo_file: "/full/path/to/TO-DO.md"
```

### GitHub API rate limiting

**Problem:** "API rate limit exceeded"

**Solutions:**

1. **Use authenticated requests:**
```bash
# Ensure gh CLI is authenticated
gh auth status

# Scripts automatically use GITHUB_TOKEN
```

2. **Check rate limit:**
```bash
gh api rate_limit
```

3. **Wait for reset:**
```
Unauthenticated: 60 requests/hour
Authenticated: 5,000 requests/hour

Rate limit resets at the time shown in the error message.
```

4. **Use conditional requests:**
```python
# Scripts already implement this
# Just ensure you're authenticated
```

### TO-DO.md sync fails

**Problem:** `sync-issues-to-todo.py` crashes

**Solutions:**

1. **Check configuration:**
```bash
# Verify idd-config.yml exists
cat idd-config.yml | grep repository

# Test GitHub connection
gh issue list
```

2. **Check permissions:**
```bash
# Verify write access
touch TO-DO.md
echo "test" >> TO-DO.md
```

3. **Debug mode:**
```bash
# Run with debug output
python3 -u bin/sync-issues-to-todo.py 2>&1 | tee sync-debug.log
```

4. **Manual test:**
```bash
python3 <<EOF
from github import Github
import os

token = os.getenv('GITHUB_TOKEN') or os.popen('gh auth token').read().strip()
g = Github(token)
repo = g.get_repo('owner/repo')
print(f"✅ Connected to {repo.full_name}")
print(f"Open issues: {repo.open_issues_count}")
EOF
```

---

## Workflow Issues

### Issue templates not showing

**Problem:** Templates don't appear when creating issue

**Solutions:**

1. **Check file location:**
```bash
ls -la .github/ISSUE_TEMPLATE/
# Files must be in this directory
```

2. **Check file format:**
```bash
# Must be .yml or .yaml
# Must start with YAML front matter
head -5 .github/ISSUE_TEMPLATE/01_feature.yml
```

3. **Validate YAML:**
```bash
python3 -c "import yaml; print(yaml.safe_load(open('.github/ISSUE_TEMPLATE/01_feature.yml')))"
```

4. **Clear browser cache:**
```
GitHub caches templates. Hard refresh (Cmd+Shift+R / Ctrl+Shift+R)
```

### Commits not linking to issues

**Problem:** Commit-issue linking workflow not working

**Solutions:**

1. **Check commit message format:**
```bash
# Correct formats:
git commit -m "feat: add feature #123"
git commit -m "fix: resolve bug (closes #123)"
git commit -m "docs: update README, fixes #123"

# Pattern matches:
# #123
# closes #123
# fixes #123
# resolves #123
```

2. **Check workflow permissions:**
```yaml
# .github/workflows/commit-to-issue-link.yml
permissions:
  issues: write
  contents: read
```

3. **Check workflow runs:**
```bash
gh run list --workflow=commit-to-issue-link.yml
gh run view --log
```

### PR validation fails

**Problem:** PRs fail validation

**Solutions:**

1. **Check PR title format:**
```
Correct:
feat: add new feature
fix: resolve bug
docs: update documentation

Incorrect:
Add new feature
Fixes bug
Updated docs

Use: feat|fix|docs|style|refactor|test|chore|ci|perf
```

2. **Check PR description:**
```
Must be at least 20 characters.
Should describe what and why.
```

3. **Disable validation temporarily:**
```yaml
# .github/workflows/pr-validation.yml
# Comment out or disable workflow
```

### Stale bot marking active issues

**Problem:** Recently active issues marked as stale

**Solutions:**

1. **Adjust stale timeouts:**
```yaml
# idd-config.yml
stale:
  days_before_stale: 90  # Increase from 60
  exempt_labels:
    - "pinned"
    - "in-progress"  # Add this
```

2. **Add exempt labels:**
```bash
# Label important issues
gh issue edit 123 --add-label pinned
```

3. **Disable stale management:**
```yaml
# idd-config.yml
workflows:
  stale_management: false
```

---

## Permission Problems

### "Permission denied" on push

**Problem:** Can't push workflow changes

**Solution:**
```bash
# Check remote URL
git remote -v

# Should be:
# origin  https://github.com/owner/repo.git

# If SSH and failing:
git remote set-url origin https://github.com/owner/repo.git

# Re-authenticate
gh auth login
```

### "Forbidden" in GitHub Actions

**Problem:** Workflow can't access repository

**Solutions:**

1. **Enable workflow permissions:**
```
Settings → Actions → General → Workflow permissions
Select: Read and write permissions
```

2. **Update workflow:**
```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

### Can't create issues via API

**Problem:** Scripts can't create issues

**Solutions:**

1. **Check token scopes:**
```bash
gh auth status
# Should show: repo, workflow scopes

# Refresh with correct scopes
gh auth refresh -s repo -s workflow
```

2. **Check repository settings:**
```
Settings → General → Features
☑ Issues must be enabled
```

---

## FAQ

### Q: Why aren't my workflows running?

**A:** Common causes:
1. Actions not enabled in repository settings
2. Workflow files not in `.github/workflows/`
3. YAML syntax errors
4. Not pushed to default branch
5. Repository is archived or disabled

**Debug:**
```bash
gh workflow list              # List workflows
gh run list                   # See recent runs
gh run view --log            # View logs
```

### Q: How do I update IDD to the latest version?

**A:**
```bash
# Save your configuration
cp idd-config.yml idd-config.yml.backup

# Download latest template
git clone https://github.com/YOUR_ORG/github-idd-template.git temp-idd
cp -r temp-idd/.github/workflows/* .github/workflows/
cp -r temp-idd/bin/* bin/
rm -rf temp-idd

# Restore configuration
mv idd-config.yml.backup idd-config.yml

# Test
python3 bin/sync-issues-to-todo.py

# Commit
git add .
git commit -m "chore: update IDD to latest version"
git push
```

### Q: Can I use IDD with GitHub Enterprise?

**A:** Yes! Just ensure:
```bash
# Set GitHub Enterprise URL
gh config set gh_host github.enterprise.com

# Authenticate
gh auth login --hostname github.enterprise.com

# Update configuration
export GITHUB_API_URL=https://github.enterprise.com/api/v3
```

### Q: How do I disable specific workflows?

**A:**
```yaml
# Method 1: In idd-config.yml
workflows:
  stale_management: false

# Method 2: Rename workflow file
mv .github/workflows/stale-management.yml .github/workflows/stale-management.yml.disabled

# Method 3: Delete workflow file
rm .github/workflows/stale-management.yml
```

### Q: Why is my TO-DO.md not updating?

**A:** Check:
```bash
# 1. Workflow is enabled
gh workflow list | grep issue-to-todo-sync

# 2. Workflow has run
gh run list --workflow=issue-to-todo-sync.yml --limit 5

# 3. Script works locally
source .venv/bin/activate
python3 bin/sync-issues-to-todo.py

# 4. GitHub token has permissions
gh auth status

# 5. Manual trigger
gh workflow run issue-to-todo-sync.yml
```

### Q: Can I customize issue templates?

**A:** Yes:
```bash
# Edit templates
vim .github/ISSUE_TEMPLATE/01_feature.yml

# Validate syntax
python3 -c "import yaml; yaml.safe_load(open('.github/ISSUE_TEMPLATE/01_feature.yml'))"

# Commit and push
git add .github/ISSUE_TEMPLATE/01_feature.yml
git commit -m "chore: customize feature template"
git push
```

### Q: How do I migrate from another issue system?

**A:** See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed instructions.

### Q: The AI context system isn't capturing sessions

**A:**
```bash
# Check directory exists
ls -la .ai-context/

# Check script works
python3 bin/capture-session.py --test

# Check configuration
cat .ai-context/config.json

# Manual capture
python3 bin/capture-session.py
```

### Q: How do I get help?

**A:**
1. Check this troubleshooting guide
2. Read [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. Search existing issues
4. Open a new issue with "question" label
5. Include error messages and logs

---

## Getting Help

### Collect Debug Information

Before asking for help, collect:

```bash
#!/bin/bash
echo "IDD Debug Information"
echo "====================="
echo ""

echo "System:"
uname -a
echo ""

echo "Python:"
python3 --version
pip3 --version
echo ""

echo "Git:"
git --version
echo ""

echo "GitHub CLI:"
gh --version
gh auth status
echo ""

echo "IDD Files:"
ls -la .github/workflows/
ls -la bin/*.py
ls -la idd-config.yml
echo ""

echo "Python packages:"
source .venv/bin/activate 2>/dev/null
pip list | grep -E "PyGithub|GitPython|dotenv"
echo ""

echo "Recent workflow runs:"
gh run list --limit 5
```

### Support Channels

- **Documentation:** [docs/idd/](.)
- **GitHub Issues:** Use "question" or "bug" template
- **Discussions:** Community Q&A
- **Email:** (if provided)

---

**Still stuck? Open an issue with the "help-wanted" label! 💚**
