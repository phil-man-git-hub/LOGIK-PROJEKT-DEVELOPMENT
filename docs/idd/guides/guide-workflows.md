# GitHub Actions Workflows Guide

**Status:** ✅ Active  
**Last Updated:** November 5, 2025  
**Part of:** IDD Foundation (Week 1)

---

## 📋 Overview

This repository uses several GitHub Actions workflows to automate issue management, PR validation, and labeling. These workflows are part of the Issue-Driven Development (IDD) infrastructure.

## 🔄 Active Workflows

### 1. Issue to TO-DO Sync (`issue-to-todo-sync.yml`)

**Purpose:** Automatically synchronizes GitHub Issues with TO-DO.md

**Triggers:**
- Issue opened, closed, reopened, labeled, unlabeled, assigned, unassigned
- Hourly schedule (`0 * * * *`)
- Manual workflow dispatch

**What it does:**
- Fetches all open issues via GitHub API
- Groups issues by category (IDD, Enhancement, Bug, etc.)
- Updates the AUTO-SYNC section in TO-DO.md
- Commits changes automatically

**Documentation:** [sync-guide.md](./sync-guide.md)

### 2. Auto Label (`auto-label.yml`)

**Purpose:** Automatically labels PRs and issues based on content and changes

**Triggers:**
- Pull request opened, edited, or synchronized
- Issue opened or edited

**What it does:**
- **Path-based labeling**: Labels PRs based on which files changed
- **Size labeling**: Adds size labels (XS/S/M/L/XL) based on lines changed
- **Type labeling**: Labels PRs based on conventional commit prefix in title
- **Template labeling**: Labels issues based on template used

**Examples:**
- PR changes files in `docs/` → gets `documentation` label
- PR title starts with `feat:` → gets `enhancement` label
- PR has 250 lines changed → gets `size/M` label
- Issue uses bug template → gets `bug` label

### 3. PR Validation (`pr-validation.yml`)

**Purpose:** Validates PRs meet quality standards before merge

**Triggers:**
- Pull request opened, edited, synchronized, reopened, or ready for review

**Checks:**
- ✅ Title follows conventional commit format
- ✅ PR is linked to an issue (has "Closes #N")
- ✅ Description is adequate (>50 characters)
- ✅ PR includes checklist
- ⚠️  PR size warning if >500 lines

**What it does:**
- Posts validation results as PR comment
- Updates comment on subsequent changes
- Calculates score and status
- Provides recommendations for improvements
- Fails workflow if critical checks don't pass

---

## 🏷️ Label System

### Label Categories

**Type Labels** (what kind of change):
- `bug` - Something isn't working
- `enhancement` - New feature
- `documentation` - Docs updates
- `chore` - Maintenance tasks
- `refactoring` - Code improvements
- `testing` - Test additions/updates
- `automation` - Workflow changes
- `breaking-change` - Breaking changes

**Area Labels** (what part of system):
- `idd` - Issue-Driven Development
- `infrastructure` - System admin
- `monitoring` - Monitoring/logging
- `network` - Network config
- `security` - Security/auth
- `storage` - Storage/backup
- `services` - Service management

**Size Labels** (PR size):
- `size/XS` - <10 lines
- `size/S` - 10-100 lines
- `size/M` - 100-500 lines
- `size/L` - 500-1000 lines
- `size/XL` - >1000 lines

**Priority Labels**:
- `priority/high` - Urgent
- `priority/medium` - Normal
- `priority/low` - When time permits

**Status Labels**:
- `status/blocked` - Blocked by dependency
- `status/in-progress` - Being worked on
- `status/needs-review` - Awaiting review
- `status/needs-testing` - Needs testing

### Creating Labels

Labels are defined in `.github/labels.yml`. To create them in GitHub:

```bash
# Using GitHub CLI
gh label create "automation" --color "0e8a16" --description "GitHub Actions and workflows"

# Or import from file (requires additional tooling)
# See: https://github.com/Financial-Times/github-label-sync
```

---

## 🎨 Path-Based Labeling Rules

The `.github/labeler.yml` file defines which labels to apply based on changed files:

| Pattern | Label Applied |
|---------|---------------|
| `docs/**`, `*.md` | `documentation` |
| `.github/workflows/**` | `automation` |
| `src/**/monitoring/**` | `monitoring` |
| `src/**/network/**` | `network` |
| `**/*.py` | `python` |
| `**/*.sh` | `scripts` |
| `tests/**` | `testing` |

### Customizing Rules

Edit `.github/labeler.yml`:

```yaml
# Add new label rule
my-feature:
  - changed-files:
    - any-glob-to-any-file: 'src/my-feature/**'
```

---

## ✅ PR Validation Checks

### 1. Title Format Check

**Requirement:** Title must follow conventional commit format

**Format:** `type(scope): description`

**Valid types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code restructuring
- `test` - Tests
- `chore` - Maintenance
- `ci` - CI/CD
- `perf` - Performance

**Examples:**
- ✅ `feat(monitoring): add LibreNMS integration`
- ✅ `fix: resolve network configuration bug`
- ✅ `docs: update installation guide`
- ❌ `Add monitoring` (no type)
- ❌ `fixed stuff` (no colon)

### 2. Linked Issue Check

**Requirement:** PR must be linked to an issue

**Valid formats:**
- `Closes #123`
- `Fixes #456`
- `Resolves #789`

**Where to add:** In the PR description (body)

### 3. Description Check

**Requirement:** PR description must be at least 50 characters

**Why:** Ensures adequate context for reviewers

### 4. Checklist Check

**Requirement:** PR should include checklist items

**Provided by:** PR template automatically includes checklists

### 5. Size Warning

**Thresholds:**
- >500 lines: Warning
- >1000 lines: Strong warning to split PR

---

## 🔧 Workflow Configuration

### Permissions

All workflows require specific permissions:

```yaml
permissions:
  contents: write  # To commit TO-DO.md changes
  issues: write    # To label and comment on issues
  pull-requests: write  # To label and comment on PRs
```

### Triggers

Common trigger patterns:

```yaml
# On PR events
on:
  pull_request:
    types: [opened, edited, synchronize]

# On issue events
on:
  issues:
    types: [opened, closed, labeled]

# On schedule
on:
  schedule:
    - cron: '0 * * * *'  # Hourly

# Manual trigger
on:
  workflow_dispatch:
```

### Environment Variables

Workflows use these variables:

- `GITHUB_TOKEN` - Provided automatically by GitHub Actions
- `GITHUB_REPOSITORY` - Format: `owner/repo`

---

## 🧪 Testing Workflows

### Local Testing

**Validation (without running):**
```bash
# Check YAML syntax
yamllint .github/workflows/*.yml

# Validate workflow syntax with act
act --list
```

**Simulate workflows:**
```bash
# Install act: https://github.com/nektos/act
brew install act

# Run workflow locally
act pull_request -e test-event.json
```

### Testing in GitHub

1. **Create test PR:**
   ```bash
   git checkout -b test-workflows
   echo "test" >> README.md
   git add README.md
   git commit -m "test: validate workflows"
   git push origin test-workflows
   gh pr create --title "test: workflow validation" --body "Testing workflows"
   ```

2. **Check Actions tab:**
   - Go to repository → Actions tab
   - View workflow runs
   - Check logs for errors

3. **Verify results:**
   - Labels applied correctly?
   - Validation comment posted?
   - TO-DO.md synced?

---

## 🐛 Troubleshooting

### Workflow Not Triggering

**Checks:**
- Workflow file in `.github/workflows/`
- YAML syntax valid
- Correct trigger events specified
- Repository settings allow actions

**Debug:**
```bash
# View workflow runs
gh run list --workflow="auto-label.yml"

# View specific run
gh run view RUN_ID --log
```

### Labels Not Applied

**Checks:**
- Labels exist in repository
- `labeler.yml` patterns match changed files
- Workflow has `pull-requests: write` permission

**Fix:**
```bash
# Create missing labels
gh label create "automation" --color "0e8a16"
```

### Validation Always Fails

**Checks:**
- PR title format correct
- Description includes "Closes #N"
- Description length >50 chars

**View details:**
- Check PR validation comment
- Read workflow logs in Actions tab

---

## 📊 Monitoring Workflow Health

### Success Indicators

- ✅ Workflows complete successfully (green checkmarks)
- ✅ Labels applied automatically
- ✅ Validation comments posted
- ✅ TO-DO.md stays in sync
- ✅ No failed workflow runs

### Metrics to Track

- Workflow success rate
- Average execution time
- Label accuracy (false positives/negatives)
- PR validation pass rate

### Viewing Workflow Status

```bash
# List recent runs
gh run list --limit 20

# View specific workflow
gh run list --workflow="auto-label.yml"

# Check status
gh run view --log
```

---

## 🚀 Future Enhancements

### Planned

- [ ] Stale issue management workflow
- [ ] Documentation validation (markdown lint, link checking)
- [ ] Automatic PR size warnings
- [ ] Dependency update automation
- [ ] Release automation

### Ideas

- Auto-assign reviewers based on file changes
- Auto-milestone based on labels
- Slack/Discord notifications
- PR merge automation for bot PRs
- Performance benchmarking in CI

---

## 📚 Related Documentation

- [Issue-TO-DO Sync Guide](./sync-guide.md)
- [PR Template Guide](./templates/pr-template-guide.md)
- [Issue Templates Guide](./templates/issue-template-guide.md)
- [IDD Roadmap](./ROADMAP_ISSUE_DRIVEN_DEVELOPMENT.md)

---

## 💡 Best Practices

### For PR Authors

- ✅ Use conventional commit format in title
- ✅ Link PRs to issues with "Closes #N"
- ✅ Write clear descriptions
- ✅ Keep PRs focused and reasonably sized
- ✅ Complete checklists before requesting review

### For Maintainers

- ✅ Keep labels consistent and well-defined
- ✅ Monitor workflow health regularly
- ✅ Update labeler rules as project evolves
- ✅ Tune validation thresholds based on team needs
- ✅ Document workflow changes

---

**Last Updated:** November 5, 2025  
**Version:** 1.0.0  
**Maintainer:** @phil-man-git-hub
