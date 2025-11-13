# IDD Quick Start Guide
# Issue Filename Convention

All issue files in `docs/idd/issues/` must use the following naming pattern:

`<issue_type>-<topic>.md`

Examples:
- `feature_request-codespaces_integration.md`
- `bug_report-snmp_timeout.md`
- `documentation-freeipa_certificate_workflow.md`

This pattern is enforced by automation. Non-conforming filenames will be flagged by the validation workflow.


Get Issue-Driven Development running in your repository in **5 minutes**.

## Prerequisites ✓

Before you begin, ensure you have:

- ✅ Git installed (`git --version`)
- ✅ Python 3.9+ installed (`python3 --version`)
- ✅ GitHub CLI installed (`gh --version`)
- ✅ GitHub repository with Actions enabled
- ✅ Admin access to your repository

## Quick Installation

### Step 1: Get the Template

**Option A: Clone the template repository**
```bash
git clone https://github.com/YOUR_ORG/github-idd-template.git
cd your-project
```

**Option B: Copy to existing repository**
```bash
cd your-existing-repo

# Download and extract template
curl -L https://github.com/YOUR_ORG/github-idd-template/archive/main.tar.gz | tar xz
cp -r github-idd-template-main/* .
rm -rf github-idd-template-main
```

### Step 2: Run Setup

```bash
# Make setup script executable (if needed)
chmod +x bin/setup-idd.sh

# Run interactive setup
./bin/setup-idd.sh
```

The setup script will:
1. ✅ Validate prerequisites
2. ✅ Authenticate with GitHub
3. ✅ Create directory structure
4. ✅ Set up Python environment
5. ✅ Generate configuration
6. ✅ Initialize TO-DO.md

**Example Output:**
```
============================================================================
Checking Prerequisites
============================================================================

✅ All prerequisites satisfied

============================================================================
Configuration
============================================================================

Project name [your-repo]: My Awesome Project
Project description: A revolutionary web application

✅ Configuration file created: idd-config.yml

============================================================================
Setup Complete! 🎉
============================================================================
```

### Step 3: Commit and Push

```bash
# Review the changes
git status

# Commit everything
git add .
git commit -m "feat: set up Issue-Driven Development"

# Push to GitHub
git push
```

### Step 4: Verify Installation

```bash
# Check GitHub Actions are running
gh run list --limit 5

# Sync issues to TO-DO
python3 bin/sync-issues-to-todo.py

# Generate documentation
python3 bin/generate-docs.py
```

**You're done! 🎉**

## Quick Configuration

Edit `idd-config.yml` to customize:

```yaml
# Minimal configuration
project:
  name: "My Project"
  repository: "owner/repo"

labels:
  track: ["enhancement", "bug", "documentation"]

workflows:
  issue_sync: true
  auto_label: true
  pr_validation: true
```

## First Issue

Create your first issue using a template:

1. Go to your repository on GitHub
2. Click **Issues** → **New Issue**
3. Select **Feature Request** template
4. Fill in the details:
   ```
   Title: feat: Add user login
   Labels: enhancement, priority:high
   ```
5. Submit!

The issue will:
- ✅ Be automatically labeled
- ✅ Appear in `TO-DO.md` within 6 hours
- ✅ Be tracked by workflows

## First Pull Request

Create a PR that links to your issue:

```bash
# Create feature branch
git checkout -b feature/user-login

# Make changes
# ... edit files ...

# Commit with issue reference
git commit -m "feat: implement user login (#1)"

# Push and create PR
git push -u origin feature/user-login
gh pr create --title "feat: implement user login" --body "Closes #1"
```

The PR will:
- ✅ Be validated for format
- ✅ Link to the issue automatically
- ✅ Show in issue comments

## Common Commands

```bash
# Sync issues to TO-DO
python3 bin/sync-issues-to-todo.py

# Search development context
python3 bin/search-context.py "authentication"

# Capture current session
python3 bin/capture-session.py

# Generate documentation
python3 bin/generate-docs.py

# View workflow runs
gh run list

# View issues
gh issue list
```

## What's Working?

After setup, you should have:

### ✅ GitHub Configuration
- 5 issue templates available
- 7 GitHub Actions workflows active
- PR template ready

### ✅ Automation
- Issue-TO-DO sync (runs every 6 hours)
- Auto-labeling (on new issues)
- PR validation (on pull requests)
- Commit-issue linking (on pushes)
- Stale management (daily)
- Smart labeling (on issues)
- Auto documentation (weekly)

### ✅ AI Context System
- `.ai-context/` directory created
- Session capture ready
- Search index initialized
- Context retrieval available

### ✅ Scripts
- `sync-issues-to-todo.py` - Sync issues
- `capture-session.py` - Capture sessions
- `search-context.py` - Search context
- `retrieve-context.py` - Retrieve context
- `generate-docs.py` - Generate docs

## Quick Troubleshooting

### Setup script fails?

```bash
# Check prerequisites
python3 --version  # Should be 3.9+
gh --version       # Should be 2.0+
gh auth status     # Should show logged in

# Run setup with more info
bash -x ./bin/setup-idd.sh
```

### Workflows not running?

```bash
# Check Actions are enabled
gh api repos/:owner/:repo --jq .has_issues,.has_wiki

# Manually trigger workflow
gh workflow run issue-to-todo-sync.yml
```

### Python errors?

```bash
# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Test import
python3 -c "import github; print('✅ PyGithub installed')"
```

### Need help?

- 📚 **Detailed Guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- 🔧 **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 💬 **Open an Issue:** Use the "question" template
- 📖 **Read the Docs:** [docs/idd/](.)

## Next Steps

Now that IDD is set up:

1. **Read the detailed guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. **Customize configuration:** Edit `idd-config.yml`
3. **Learn best practices:** [idd-workflow-best_practices.md](idd-workflow-best_practices.md)
4. **Understand architecture:** [idd-workflow-architecture.md](idd-workflow-architecture.md)
5. **Train your team:** Share this guide!

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│             IDD Quick Reference                         │
├─────────────────────────────────────────────────────────┤
│ Create Issue:     gh issue create --template feature    │
│ Sync TO-DO:       python3 bin/sync-issues-to-todo.py   │
│ Search Context:   python3 bin/search-context.py "..."  │
│ Generate Docs:    python3 bin/generate-docs.py         │
│ Create PR:        gh pr create --title "..." --body "..." │
│ View Workflows:   gh run list                           │
│ Check Status:     gh workflow list                      │
└─────────────────────────────────────────────────────────┘
```

## Success Checklist

After following this guide, you should have:

- ✅ IDD template installed
- ✅ Configuration customized
- ✅ Changes committed and pushed
- ✅ GitHub Actions workflows running
- ✅ First issue created
- ✅ TO-DO.md synchronized
- ✅ Python scripts working
- ✅ Team members can create issues

**Congratulations! You're using Issue-Driven Development! 🚀**

## Learning Resources

- **5-Minute Videos** (coming soon)
- **Example Repository:** See a live IDD implementation
- **Community:** Join discussions on GitHub
- **Blog Posts:** Success stories and tips

## Feedback

This is your project now! Help improve IDD:

- 🐛 Found a bug? Open an issue
- 💡 Have an idea? Open a feature request
- 📖 Docs unclear? Open a documentation issue
- ⭐ Like IDD? Star the repository!

---

**Time to complete:** ⏱️ 5 minutes  
**Difficulty:** 🟢 Easy  
**Prerequisites:** Git, Python 3.9+, GitHub CLI

**Made with ❤️ for better development workflows**
