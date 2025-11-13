# Session Capture System - Usage Guide

**Script:** `bin/capture-session.py`  
**Purpose:** Automatically capture development session activity and generate AI context files

---

## Overview

The session capture system automatically documents your development work by:
- Detecting git commits within a date range
- Linking commits to GitHub Issues and PRs (when available)
- Extracting file changes and code statistics
- Generating structured markdown session files
- Maintaining a searchable session index

---

## Installation

### Prerequisites

1. **Python 3.9+**
2. **Git repository**
3. **AI context structure** (`.ai-context/` directory)
4. **Optional:** GitHub API token for issue/PR linking

### Python Dependencies

```bash
pip install PyGithub python-dotenv
```

Or install from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Basic Usage

### Capture Today's Session

```bash
python bin/capture-session.py
```

This will:
- Detect all commits made today
- Generate `.ai-context/memory/sessions/YYYY-MM-DD.md`
- Update `.ai-context/memory/sessions/index.json`

### Capture Specific Date

```bash
python bin/capture-session.py --date 2025-11-05
```

### Capture Multiple Days

```bash
# Capture last 7 days
python bin/capture-session.py --range 7

# Capture last 30 days
python bin/capture-session.py --range 30
```

---

## Configuration

### GitHub API Token (Optional)

For enhanced features (issue/PR linking), set your GitHub token:

```bash
# In .env file
GITHUB_TOKEN=ghp_your_token_here

# Or export as environment variable
export GITHUB_TOKEN=ghp_your_token_here

# Or pass directly
python bin/capture-session.py --token ghp_your_token_here
```

**Note:** Without a token, the script still works but won't link to GitHub issues/PRs.

### Repository Path

By default, the script uses the current directory. To specify a different repo:

```bash
python bin/capture-session.py --repo /path/to/repo
```

---

## Output Format

### Session File Structure

Each session file (`.ai-context/memory/sessions/YYYY-MM-DD.md`) contains:

```markdown
# Development Session: YYYY-MM-DD

## 📊 Session Summary
- Date, commits, issues, PRs, files changed
- Lines added/removed
- Net change

### Issues Addressed
- List of all issues referenced in commits

## 🎯 Issues
### Created / Closed
- Issues created or closed on this date

## 🔀 Pull Requests
### Merged
- PRs merged on this date

## 📝 Commits
### By Type (feat, fix, docs, etc.)
- Commit hash, subject, stats
- Files changed

## 📁 Key Files Modified
- Top 10 most frequently modified files

## 🔍 Context for Next Session
- Current state
- What's next
```

### Session Index

The index file (`.ai-context/memory/sessions/index.json`) maintains searchable metadata:

```json
{
  "sessions": [
    {
      "date": "2025-11-05",
      "file": "2025-11-05.md",
      "commits": 32,
      "issues_referenced": [1, 2, 3, 15],
      "issues_closed": [15],
      "prs_merged": [16],
      "commit_types": ["feat", "fix", "docs"],
      "files_changed": 138,
      "lines_changed": 10180,
      "generated": "2025-11-05T12:03:39.409428"
    }
  ]
}
```

---

## Command-Line Options

```
usage: capture-session.py [-h] [--date DATE] [--range RANGE] [--repo REPO] [--token TOKEN]

Capture development session activity and generate AI context files.

optional arguments:
  -h, --help     show this help message and exit
  --date DATE    Specific date to capture (YYYY-MM-DD). Default: today
  --range RANGE  Capture last N days
  --repo REPO    Path to git repository. Default: current directory
  --token TOKEN  GitHub API token. Default: GITHUB_TOKEN env var
```

---

## Examples

### Daily Workflow

At the end of each day, run:

```bash
python bin/capture-session.py
```

### Weekly Review

Capture the entire week:

```bash
python bin/capture-session.py --range 7
```

### Backfill History

Capture last 30 days of activity:

```bash
python bin/capture-session.py --range 30
```

### Specific Project Event

Capture activity from a specific date:

```bash
python bin/capture-session.py --date 2025-11-05
```

---

## Automation

### Daily Cron Job

Add to your crontab for automatic daily captures:

```bash
# Capture at end of workday (6 PM)
0 18 * * * cd /path/to/repo && python bin/capture-session.py
```

### GitHub Actions (Future Enhancement)

```yaml
name: Daily Session Capture

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:

jobs:
  capture:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Capture session
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python bin/capture-session.py --date $(date -d yesterday +%Y-%m-%d)
      - name: Commit session files
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .ai-context/memory/sessions/
          git commit -m "chore: capture session $(date -d yesterday +%Y-%m-%d)"
          git push
```

---

## Features

### What It Captures

✅ **Git Commits**
- All commits in date range
- Commit messages and types (conventional commits)
- Files changed
- Lines added/removed
- Author information

✅ **Issue References**
- Extracts issue numbers from commit messages (#N)
- Links to GitHub issues (with token)
- Tracks issue creation/closure dates

✅ **Pull Requests**
- PR merges on the date
- PR titles and links
- Related issues

✅ **Statistics**
- Total files changed
- Lines added/removed
- Net change
- Most frequently modified files

✅ **Context Metadata**
- Searchable index
- Topic categorization
- Issue index
- Commit type breakdown

### What It Doesn't Capture

❌ Code diffs (by design - keeps files manageable)  
❌ Uncommitted changes  
❌ Non-git activity  
❌ Branch operations (unless in commit messages)

---

## Troubleshooting

### "Sessions directory not found"

Ensure you have the AI context structure:

```bash
ls -la .ai-context/memory/sessions/
```

If missing, check that issue #15 (AI Context Structure) was completed.

### "No commits found"

This is normal if you haven't committed anything on the specified date. The script will still generate a session file with zero commits.

### GitHub API Rate Limiting

Without authentication: 60 requests/hour  
With token: 5,000 requests/hour

If you hit rate limits, wait an hour or use a GitHub token.

### SSL/TLS Warnings

You may see warnings about urllib3/OpenSSL on macOS:

```
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+
```

This is harmless and doesn't affect functionality.

---

## Integration with IDD Workflow

### Recommended Workflow

1. **Daily:** Capture today's session
   ```bash
   python bin/capture-session.py
   ```

2. **Weekly:** Review all sessions
   ```bash
   ls -l .ai-context/memory/sessions/*.md
   ```

3. **Monthly:** Archive old sessions (>90 days per retention policy)

4. **As Needed:** Regenerate specific dates
   ```bash
   python bin/capture-session.py --date 2025-11-05
   ```

### Commit Session Files

Session files should be committed to git:

```bash
git add .ai-context/memory/sessions/
git commit -m "chore: update session captures"
git push
```

---

## Future Enhancements

Planned improvements:

- [ ] GitHub Actions integration
- [ ] Branch activity detection
- [ ] Tag and release tracking
- [ ] Automated weekly summaries
- [ ] Context snippet auto-generation
- [ ] Email/Slack notifications
- [ ] Custom templates
- [ ] Multiple repository support

---

## Support

**Documentation:** `.ai-context/README.md`  
**Issues:** [GitHub Issues](https://github.com/phil-man-git-hub/WORKSTATION-CONFIGURATION/issues)  
**Roadmap:** `docs/idd/ROADMAP_ISSUE_DRIVEN_DEVELOPMENT.md`

---

**Last Updated:** 2025-11-05  
**Version:** 1.0  
**Script:** `bin/capture-session.py`
