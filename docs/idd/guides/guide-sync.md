# Issue ↔ TO-DO.md Synchronization Guide

**Status:** ✅ Active  
**Last Updated:** November 5, 2025  
**Part of:** IDD Foundation (Week 1)

---

## 📋 Overview

The Issue ↔ TO-DO.md synchronization system automatically keeps your TO-DO.md file in sync with GitHub Issues, eliminating manual updates and ensuring your task list is always current.

### Key Features

- **Automatic Updates**: TO-DO.md updates whenever issues change
- **Preserves Manual Content**: Only auto-sync sections are modified
- **Smart Categorization**: Issues grouped by type (IDD, Bug, Enhancement, etc.)
- **Hourly Sync**: Scheduled updates every hour
- **Manual Trigger**: Run sync on-demand via GitHub Actions

---

## 🏗️ Architecture

### Components

1. **Python Sync Script** (`.github/scripts/sync_issues_to_todo.py`)
   - Fetches open issues via GitHub API
   - Parses TO-DO.md structure
   - Updates auto-sync sections
   - Preserves manual content

2. **GitHub Actions Workflow** (`.github/workflows/issue-to-todo-sync.yml`)
   - Triggers on issue events
   - Runs hourly on schedule
   - Commits changes automatically
   - Handles errors gracefully

3. **TO-DO.md Structure**
   - Manual sections (edit freely)
   - Auto-sync sections (marked with HTML comments)
   - Clear boundaries and warnings

### Data Flow

```
GitHub Issues → GitHub API → Python Script → TO-DO.md → Git Commit → Push
     ↑                                                         ↓
     └─────────── GitHub Actions Workflow ────────────────────┘
```

---

## 🚀 Usage

### For Users

#### Viewing Synced Issues

Open `TO-DO.md` and scroll to the **"Auto-Synced Issues"** section:

```markdown
## 🔄 Auto-Synced Issues

<!-- BEGIN AUTO-SYNC: DO NOT EDIT MANUALLY -->

#### IDD Foundation
- [ ] #5 Implement Basic Issue ↔ TO-DO.md Synchronization `enhancement`

#### Bug
- [ ] #7 Fix network configuration script `bug` @username

<!-- Last synced: 2025-11-05 17:41:26 UTC -->
<!-- Total open issues: 2 -->
<!-- END AUTO-SYNC -->
```

#### Manual Sections

Edit any section **outside** the auto-sync markers freely:

```markdown
## 📋 Manual Tasks (Edit freely)
- [x] Completed task
- [ ] Task I'm working on
- [ ] Future task
```

#### Triggering Sync

Sync happens automatically when you:
- Create, close, or reopen an issue
- Add or remove issue labels
- Assign or unassign an issue
- Wait (hourly scheduled sync)

**Manual trigger:**
1. Go to Actions tab in GitHub
2. Select "Sync Issues to TO-DO" workflow
3. Click "Run workflow"

### For Developers

#### Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export GITHUB_TOKEN="your_github_token"
   export GITHUB_REPOSITORY="owner/repo"
   ```

3. **Run the script:**
   ```bash
   python .github/scripts/sync_issues_to_todo.py
   ```

#### Testing Changes

```bash
# Test locally before pushing
python .github/scripts/sync_issues_to_todo.py

# Check the diff
git diff TO-DO.md

# Revert if needed
git checkout TO-DO.md
```

---

## 📝 TO-DO.md Structure

### Adding Auto-Sync Sections

Add these markers where you want issues synced:

```markdown
## 🔄 Auto-Synced Issues

<!-- BEGIN AUTO-SYNC: DO NOT EDIT MANUALLY -->
<!-- Issues will appear here -->
<!-- END AUTO-SYNC -->
```

### Multiple Sync Sections

You can have multiple auto-sync sections (future enhancement):

```markdown
## 🚀 Sprint Issues
<!-- BEGIN AUTO-SYNC: sprint -->
<!-- Issues with label 'sprint' -->
<!-- END AUTO-SYNC -->

## 🐛 Active Bugs
<!-- BEGIN AUTO-SYNC: bug -->
<!-- Issues with label 'bug' -->
<!-- END AUTO-SYNC -->
```

---

## 🎨 Issue Categorization

Issues are automatically grouped by labels:

| Category | Labels | Example |
|----------|--------|---------|
| IDD Foundation | `idd` | Core automation features |
| Enhancement | `enhancement` | New features |
| Bug | `bug` | Bug fixes |
| Documentation | `documentation` | Docs updates |
| Infrastructure | `infrastructure`, `monitoring` | System work |
| Other | (no matching label) | Miscellaneous |

### Issue Format

```markdown
- [ ] [#123](url) Issue title `label1, label2` @assignee
```

---

## 🔧 Configuration

### Script Configuration

Edit `.github/scripts/sync_issues_to_todo.py`:

```python
# Markers for auto-sync sections
AUTO_SYNC_START = "<!-- BEGIN AUTO-SYNC: DO NOT EDIT MANUALLY -->"
AUTO_SYNC_END = "<!-- END AUTO-SYNC -->"

# File to update
TODO_FILE = "TO-DO.md"
```

### Workflow Configuration

Edit `.github/workflows/issue-to-todo-sync.yml`:

```yaml
# Change sync schedule (default: hourly)
schedule:
  - cron: '0 */2 * * *'  # Every 2 hours
  - cron: '0 9,17 * * *'  # 9 AM and 5 PM UTC

# Change Python version
python-version: '3.13'
```

### Category Customization

Edit the `group_issues_by_category()` function:

```python
categories = {
    'Priority': [],      # Add new category
    'Enhancement': [],
    'Bug': [],
    # ...
}

# Add categorization logic
if 'priority-high' in labels:
    categories['Priority'].append(issue)
```

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Script runs without errors
- [ ] Issues fetched correctly from GitHub
- [ ] TO-DO.md updated properly
- [ ] Manual sections preserved
- [ ] Categories correct
- [ ] Formatting consistent
- [ ] Git operations work

### Test Cases

1. **Empty issue list:**
   - Close all issues
   - Run sync
   - Verify placeholder message

2. **Multiple categories:**
   - Create issues with different labels
   - Run sync
   - Verify grouping

3. **Manual section preservation:**
   - Add content outside markers
   - Run sync
   - Verify manual content unchanged

4. **Concurrent edits:**
   - Edit TO-DO.md manually
   - Trigger sync
   - Check for conflicts

### Integration Testing

```bash
# Create test issue
gh issue create --title "Test sync" --label "test"

# Run sync
python .github/scripts/sync_issues_to_todo.py

# Verify in TO-DO.md
grep "Test sync" TO-DO.md

# Clean up
gh issue close $(gh issue list --label test --json number -q '.[0].number')
```

---

## 🐛 Troubleshooting

### Common Issues

#### Script fails with "GITHUB_TOKEN not found"

**Solution:** Set the environment variable:
```bash
export GITHUB_TOKEN=$(gh auth token)
```

#### AUTO-SYNC markers not found

**Solution:** Add markers to TO-DO.md:
```markdown
<!-- BEGIN AUTO-SYNC: DO NOT EDIT MANUALLY -->
<!-- END AUTO-SYNC -->
```

#### Workflow not triggering

**Checks:**
- Workflow file in `.github/workflows/`
- Workflow enabled in repository settings
- Repository permissions correct (`contents: write`, `issues: read`)

#### Changes not committing

**Checks:**
- GitHub Actions bot has write access
- No branch protection rules blocking bot commits
- Check workflow logs for errors

### Debug Mode

Add debug output to script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

View workflow logs:
1. Go to Actions tab
2. Click on workflow run
3. Expand steps to see output

---

## 🔒 Security Considerations

### GitHub Token

- **Automatic:** GitHub Actions provides `GITHUB_TOKEN` automatically
- **Local:** Use personal access token with minimal scopes
- **Never:** Commit tokens to repository

### Permissions

Minimal required permissions:
- `contents: write` - To update TO-DO.md
- `issues: read` - To fetch issue data

### Rate Limits

- GitHub API: 5,000 requests/hour (authenticated)
- Script uses ~1 request per sync
- Hourly sync well within limits

---

## 📊 Monitoring

### Success Indicators

- TO-DO.md stays current
- No workflow failures
- Manual edits preserved
- Commits include [skip ci] to prevent loops

### Workflow Status

Check in GitHub Actions:
- Recent runs green ✓
- No failed commits
- Reasonable execution time (<30s)

### Metrics

Track over time:
- Total open issues
- Issues by category
- Sync frequency
- Update latency

---

## 🚀 Future Enhancements

### Planned (Phase 2)

- [ ] Multiple sync sections with filters
- [ ] Custom grouping/sorting options
- [ ] Milestone-based organization
- [ ] Dependency tracking
- [ ] Priority indicators
- [ ] Assignee-based views

### Ideas

- Bidirectional sync (TO-DO → Issues)
- Visual dependency graphs
- Burndown charts
- Integration with project boards
- Slack/Discord notifications
- Custom issue templates per category

---

## 📚 Related Documentation

- [IDD Roadmap](../ROADMAP_ISSUE_DRIVEN_DEVELOPMENT.md)
- [Issue Templates Guide](./templates/issue-template-guide.md)
- [PR Template Guide](./templates/pr-template-guide.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)

---

## 💡 Tips & Best Practices

### DO ✓

- Let automation handle issue tracking
- Edit manual sections freely
- Create specific, well-labeled issues
- Use milestones for grouping
- Check sync status regularly

### DON'T ✗

- Edit content between AUTO-SYNC markers manually
- Delete AUTO-SYNC markers
- Disable the workflow without reason
- Create duplicate manual issue lists
- Ignore sync failures

---

## 🆘 Support

### Getting Help

1. Check this guide first
2. Review workflow logs in Actions
3. Check [Troubleshooting](#-troubleshooting) section
4. Create an issue with `help-wanted` label

### Contributing

Found a bug or have an enhancement idea?
1. Create an issue describing the problem/idea
2. Label appropriately (`bug`, `enhancement`)
3. Reference in PR if implementing

---

**Last Updated:** November 5, 2025  
**Version:** 1.0.0  
**Maintainer:** @phil-man-git-hub
