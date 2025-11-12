# IDD Setup Guide

Complete installation and configuration guide for Issue-Driven Development.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Configuration](#configuration)
- [GitHub Setup](#github-setup)
- [Workflow Activation](#workflow-activation)
- [Testing](#testing)
- [Integration](#integration)
- [Team Onboarding](#team-onboarding)

---

## Overview

Issue-Driven Development (IDD) is a comprehensive system that:

- **Centralizes Work** - All tasks tracked as GitHub Issues
- **Automates Workflows** - 7 GitHub Actions workflows
- **Captures Context** - AI-assisted development history
- **Enforces Standards** - Automated validation and formatting
- **Generates Docs** - Automatic CHANGELOG and stats

**Installation Time:** 10-30 minutes  
**Complexity:** Medium  
**Skills Required:** Git, Python basics, GitHub administration

---

## Prerequisites

### Required Software

| Software | Minimum Version | Check Command | Install |
|----------|----------------|---------------|---------|
| **Git** | 2.25+ | `git --version` | [git-scm.com](https://git-scm.com) |
| **Python** | 3.9+ | `python3 --version` | [python.org](https://python.org) |
| **GitHub CLI** | 2.0+ | `gh --version` | [cli.github.com](https://cli.github.com) |
| **pip** | 20.0+ | `pip3 --version` | Included with Python |

### GitHub Requirements

- ✅ GitHub repository (public or private)
- ✅ GitHub Actions enabled
- ✅ Admin or write access
- ✅ Branch protection (optional but recommended)

### System Requirements

- **OS:** macOS, Linux, or Windows with WSL
- **Disk:** 50MB for IDD system + Python packages
- **Memory:** Minimal (scripts use <100MB)
- **Network:** Internet access for GitHub API

### Validation Script

Run this to check prerequisites:

```bash
#!/bin/bash
echo "Checking prerequisites..."

# Git
if command -v git &> /dev/null; then
    echo "✅ Git: $(git --version)"
else
    echo "❌ Git not found"
fi

# Python
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python: $PY_VERSION"
else
    echo "❌ Python 3 not found"
fi

# GitHub CLI
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI: $(gh --version | head -1)"
    gh auth status 2>&1 | grep -q "Logged in" && echo "✅ GitHub authenticated" || echo "⚠️  GitHub not authenticated"
else
    echo "❌ GitHub CLI not found"
fi

# pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip: $(pip3 --version | cut -d' ' -f2)"
else
    echo "❌ pip not found"
fi
```

---

## Installation Methods

Choose the method that fits your situation:

### Method 1: Automated Setup (Recommended)

Best for: New projects or full IDD adoption

```bash
# 1. Clone or copy template
git clone https://github.com/YOUR_ORG/github-idd-template.git
cd your-project

# 2. Run setup script
./bin/setup-idd.sh

# 3. Follow prompts
# Project name: My Project
# Repository: owner/repo
# Description: My awesome project

# 4. Commit and push
git add .
git commit -m "feat: set up IDD"
git push
```

### Method 2: Manual Setup

Best for: Existing projects with custom workflows

```bash
# 1. Create directory structure
mkdir -p .github/{ISSUE_TEMPLATE,workflows}
mkdir -p bin docs/idd config
mkdir -p .ai-context/{sessions,search_index,context_snapshots,insights}

# 2. Copy issue templates
cp template/.github/ISSUE_TEMPLATE/*.yml .github/ISSUE_TEMPLATE/

# 3. Copy workflows
cp template/.github/workflows/*.yml .github/workflows/

# 4. Copy scripts
cp template/bin/*.py bin/
cp template/bin/setup-idd.sh bin/
chmod +x bin/*.sh

# 5. Copy configuration
cp template/config/idd-config.template.yml idd-config.yml

# 6. Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 7. Configure
vim idd-config.yml
# Update project name, repository, etc.

# 8. Initialize
python3 bin/sync-issues-to-todo.py
```

### Method 3: Gradual Adoption

Best for: Large teams, want to test first

```bash
# 1. Start with just issue templates
mkdir -p .github/ISSUE_TEMPLATE
cp template/.github/ISSUE_TEMPLATE/01_feature.yml .github/ISSUE_TEMPLATE/
git add .github/ISSUE_TEMPLATE/01_feature.yml
git commit -m "feat: add feature request template"
git push

# 2. Add TO-DO sync workflow
mkdir -p .github/workflows
cp template/.github/workflows/issue-to-todo-sync.yml .github/workflows/
cp template/bin/sync-issues-to-todo.py bin/
git add .github/workflows/issue-to-todo-sync.yml bin/sync-issues-to-todo.py
git commit -m "feat: add issue-TO-DO sync"
git push

# 3. Gradually add more workflows
# ... add one at a time and test

# 4. Eventually add AI context system
# ... when team is comfortable
```

### Method 4: Fork and Customize

Best for: Organizations wanting branded version

```bash
# 1. Fork template repository
gh repo fork YOUR_ORG/github-idd-template --clone

# 2. Customize for your organization
cd github-idd-template
vim README.md  # Add your branding
vim config/idd-config.template.yml  # Set defaults

# 3. Publish as internal template
gh repo edit --visibility private
git add .
git commit -m "chore: customize for ACME Corp"
git push

# 4. Teams use your fork
# Teams clone your customized template
```

---

## Configuration

### Basic Configuration

Edit `idd-config.yml`:

```yaml
# Minimal required configuration
project:
  name: "My Project"
  repository: "owner/repo"
  main_branch: "main"

files:
  todo_file: "TO-DO.md"

labels:
  track: ["enhancement", "bug", "documentation"]

workflows:
  issue_sync: true
  auto_label: true
```

### Advanced Configuration

```yaml
# Full configuration with all options
project:
  name: "My Project"
  repository: "owner/repo"
  main_branch: "main"
  url: "https://github.com/owner/repo"
  description: "Project description"

files:
  todo_file: "TO-DO.md"
  changelog: "docs/CHANGELOG.md"
  project_stats: "docs/PROJECT_STATS.md"
  readme: "README.md"

labels:
  track:
    - "enhancement"
    - "bug"
    - "documentation"
    - "infrastructure"
    - "research"
  
  exempt_from_stale:
    - "pinned"
    - "security"
    - "critical"
  
  auto_label:
    feature:
      keywords: ["feature", "add", "implement"]
      labels: ["enhancement"]
    bug:
      keywords: ["bug", "error", "fix"]
      labels: ["bug"]

workflows:
  issue_sync:
    enabled: true
    schedule: "0 */6 * * *"  # Every 6 hours
  
  auto_label:
    enabled: true
  
  pr_validation:
    enabled: true
  
  commit_linking:
    enabled: true
  
  stale_management:
    enabled: true
    schedule: "0 0 * * *"  # Daily
  
  smart_labeling:
    enabled: true
  
  auto_docs:
    enabled: true
    schedule: "0 0 * * 0"  # Weekly

stale:
  days_before_stale: 60
  days_before_close: 7
  stale_message: "This issue has been marked as stale..."

ai_context:
  enabled: true
  auto_capture: true
  retention_days: 90
  max_sessions: 100

documentation:
  changelog:
    enabled: true
    days_to_include: 7
  stats:
    enabled: true
  readme:
    auto_update: true
```

### Environment Variables

Create `.env` file (git-ignored):

```bash
# GitHub token (optional, uses GITHUB_TOKEN by default)
GITHUB_TOKEN=ghp_your_token_here

# Custom paths (optional)
IDD_CONFIG_PATH=./idd-config.yml
TODO_FILE_PATH=./TO-DO.md

# Debug mode (optional)
IDD_DEBUG=false
```

### Configuration Validation

Validate your configuration:

```bash
# Check syntax
python3 -c "import yaml; yaml.safe_load(open('idd-config.yml'))"

# Test GitHub connection
gh auth status

# Test Python dependencies
python3 -c "import github, git; print('✅ Dependencies OK')"

# Test scripts
python3 bin/sync-issues-to-todo.py --dry-run
```

---

## GitHub Setup

### 1. Authenticate GitHub CLI

```bash
# Login to GitHub
gh auth login

# Follow prompts:
# - GitHub.com
# - HTTPS
# - Authenticate with browser
# - Select scopes (repo, workflow)

# Verify
gh auth status
```

### 2. Configure Repository Secrets

No secrets required! IDD uses `GITHUB_TOKEN` which is automatically provided by GitHub Actions.

**Optional secrets** (for advanced features):

```bash
# Slack webhook (optional)
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/..."

# Custom token with extended permissions (optional)
gh secret set CUSTOM_GITHUB_TOKEN --body "ghp_..."
```

### 3. Enable GitHub Actions

```bash
# Check if Actions are enabled
gh api repos/:owner/:repo --jq .has_issues,.has_projects,.workflows

# Enable Actions (if disabled)
gh api -X PATCH repos/:owner/:repo -f allow_actions="true"
```

### 4. Configure Branch Protection

Recommended for teams:

```bash
# Protect main branch
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=pr-validation \
  --field required_pull_request_reviews[required_approving_review_count]=1 \
  --field restrictions=null \
  --field enforce_admins=false
```

Or via GitHub UI:
1. Go to Settings → Branches
2. Add rule for `main`
3. Enable:
   - Require pull request reviews (1 approval)
   - Require status checks (pr-validation)
   - Require conversation resolution

---

## Workflow Activation

### Automatic Activation

Workflows activate automatically when you push to GitHub:

```bash
git add .github/workflows/
git commit -m "feat: add IDD workflows"
git push
```

### Manual Workflow Triggers

Trigger workflows manually for testing:

```bash
# List all workflows
gh workflow list

# Run specific workflow
gh workflow run issue-to-todo-sync.yml

# Watch workflow execution
gh run watch

# View workflow runs
gh run list --limit 10
```

### Workflow Schedule

Default schedule for automated workflows:

| Workflow | Schedule | Description |
|----------|----------|-------------|
| issue-to-todo-sync | Every 6 hours | Syncs issues to TO-DO.md |
| stale-management | Daily at midnight | Marks stale issues |
| auto-docs | Weekly on Sunday | Generates documentation |
| auto-label | On issue create | Labels new issues |
| pr-validation | On PR open | Validates pull requests |
| commit-linking | On push | Links commits to issues |
| smart-labeling | On issue update | Applies smart labels |

### Customize Schedules

Edit workflow files:

```yaml
# .github/workflows/issue-to-todo-sync.yml
on:
  schedule:
    - cron: "0 */3 * * *"  # Change to every 3 hours
```

---

## Testing

### 1. Test Issue Templates

```bash
# Create test issue via CLI
gh issue create \
  --title "test: validate issue template" \
  --label "enhancement" \
  --body "Testing the feature request template"

# Verify in GitHub UI
gh issue view 1
```

### 2. Test Workflows

```bash
# Trigger issue sync
gh workflow run issue-to-todo-sync.yml

# Wait and check TO-DO.md
cat TO-DO.md

# Check workflow logs
gh run list --workflow=issue-to-todo-sync.yml
gh run view --log
```

### 3. Test Python Scripts

```bash
# Activate environment
source .venv/bin/activate

# Test issue sync
python3 bin/sync-issues-to-todo.py

# Test documentation generation
python3 bin/generate-docs.py

# Test context capture
python3 bin/capture-session.py --test

# Test context search
python3 bin/search-context.py "test" || echo "No results (expected for new repo)"
```

### 4. Test Pull Request Flow

```bash
# Create feature branch
git checkout -b test/pr-validation

# Make dummy change
echo "# Test" >> TEST.md
git add TEST.md
git commit -m "test: verify PR validation"

# Push and create PR
git push -u origin test/pr-validation
gh pr create --title "test: verify PR validation" --body "Testing PR workflow"

# Check PR validation
gh pr checks

# Clean up
gh pr close 1 --delete-branch
git checkout main
```

### 5. Validation Checklist

After setup, verify:

```bash
#!/bin/bash
echo "🔍 IDD Installation Validation"
echo ""

# Check files exist
echo "📁 Checking files..."
[ -f "idd-config.yml" ] && echo "✅ idd-config.yml" || echo "❌ idd-config.yml missing"
[ -f "TO-DO.md" ] && echo "✅ TO-DO.md" || echo "❌ TO-DO.md missing"
[ -d ".ai-context" ] && echo "✅ .ai-context/" || echo "❌ .ai-context/ missing"
[ -d ".github/workflows" ] && echo "✅ .github/workflows/" || echo "❌ .github/workflows/ missing"

# Check scripts
echo ""
echo "🐍 Checking scripts..."
[ -f "bin/sync-issues-to-todo.py" ] && echo "✅ sync-issues-to-todo.py" || echo "❌ Script missing"
[ -f "bin/generate-docs.py" ] && echo "✅ generate-docs.py" || echo "❌ Script missing"

# Check Python environment
echo ""
echo "🔧 Checking Python..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
    python3 -c "import github" && echo "✅ PyGithub installed" || echo "❌ PyGithub not installed"
    python3 -c "import git" && echo "✅ GitPython installed" || echo "❌ GitPython not installed"
else
    echo "⚠️  Virtual environment not found"
fi

# Check GitHub
echo ""
echo "🔗 Checking GitHub..."
gh auth status &> /dev/null && echo "✅ GitHub authenticated" || echo "❌ Not authenticated"

# Check workflows
echo ""
echo "⚙️  Checking workflows..."
WORKFLOW_COUNT=$(gh workflow list 2>/dev/null | wc -l)
echo "Found $WORKFLOW_COUNT workflows"

echo ""
echo "✅ Validation complete!"
```

---

## Integration

### With Existing Workflows

IDD can coexist with your existing workflows:

```yaml
# Keep your existing workflow
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test

# IDD workflows run independently
```

### With CI/CD Pipelines

Integrate IDD with your deployment:

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Deploy your app
      - name: Deploy
        run: ./deploy.sh
      
      # Update IDD documentation
      - name: Generate Docs
        run: |
          source .venv/bin/activate
          python3 bin/generate-docs.py
          
      # Commit generated docs
      - name: Commit docs
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/CHANGELOG.md docs/PROJECT_STATS.md
          git commit -m "docs: update generated documentation" || exit 0
          git push
```

### With Project Management Tools

**Jira Integration:**
```yaml
# .github/workflows/jira-sync.yml
name: Sync to Jira

on:
  issues:
    types: [opened, closed]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Create Jira issue
        uses: atlassian/gajira-create@v2
        with:
          project: PROJ
          issuetype: Task
          summary: ${{ github.event.issue.title }}
```

### With Slack/Discord

**Slack Notifications:**
```yaml
# In idd-config.yml
notifications:
  slack:
    enabled: true
    webhook_url: "${SLACK_WEBHOOK_URL}"
    notify_on:
      - "issue_created"
      - "pr_merged"
```

---

## Team Onboarding

### For Team Members

Share this onboarding guide:

```markdown
# Welcome to IDD!

## Your First Day

1. **Read the Quick Start** - [QUICK_START.md](QUICK_START.md)
2. **Clone the repository** - `git clone <repo-url>`
3. **Set up Python** - `source .venv/bin/activate`
4. **Create your first issue** - Use the templates!

## Creating Issues

1. Go to Issues → New Issue
2. Select a template
3. Fill in ALL fields
4. Use appropriate labels

## Creating Pull Requests

1. Branch name: `feature/issue-123-description`
2. Commit format: `feat: add feature (#123)`
3. PR title: Same as commit
4. PR body: `Closes #123`

## Best Practices

- ✅ Always link commits to issues
- ✅ Use conventional commit format
- ✅ Add tests for new features
- ✅ Update documentation
- ✅ Request reviews
```

### Training Sessions

**Week 1: Basics**
- Introduction to IDD
- Creating issues
- Using templates
- Understanding workflows

**Week 2: Advanced**
- AI context system
- Custom labels
- Workflow customization
- Troubleshooting

### Team Metrics

Track adoption:

```bash
# Issue usage
gh issue list --state all --json number,createdAt --jq 'length'

# PR linkage rate
gh pr list --state all --json number,body --jq '[.[] | select(.body | test("#\\d+"))] | length'

# Workflow runs
gh run list --json status --jq 'group_by(.status) | map({status: .[0].status, count: length})'
```

---

## Next Steps

After setup is complete:

1. ✅ **Customize** - Edit `idd-config.yml` for your team
2. ✅ **Document** - Add team-specific guidelines
3. ✅ **Train** - Onboard team members
4. ✅ **Monitor** - Watch workflow runs
5. ✅ **Iterate** - Adjust based on usage

### Additional Resources

- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues
- [Best Practices](BEST_PRACTICES.md) - Usage guidelines
- [Architecture](ARCHITECTURE.md) - System design
- [Customization](CUSTOMIZATION_GUIDE.md) - Advanced config

---

**Setup Time:** ⏱️ 10-30 minutes  
**Difficulty:** 🟡 Medium  
**Support:** Open an issue with the "question" label

**Happy developing! 🚀**
