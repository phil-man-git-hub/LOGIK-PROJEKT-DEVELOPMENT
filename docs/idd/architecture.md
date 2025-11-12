# IDD System Architecture

Comprehensive technical documentation for the Issue-Driven Development system.

## Table of Contents

- [System Overview](#system-overview)
- [Component Architecture](#component-architecture)
- [Workflow Orchestration](#workflow-orchestration)
- [AI Context System](#ai-context-system)
- [Data Flow](#data-flow)
- [Extension Points](#extension-points)
- [Security Model](#security-model)
- [Performance Considerations](#performance-considerations)

---

## System Overview

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         GitHub Repository                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Issues     │  │     PRs      │  │   Projects   │          │
│  │  Templates   │  │  Templates   │  │    Boards    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                   │
│         └──────────────────┼──────────────────┘                   │
│                            │                                      │
│  ┌─────────────────────────▼───────────────────────────┐         │
│  │           GitHub Actions Workflows                  │         │
│  ├─────────────────────────────────────────────────────┤         │
│  │                                                      │         │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │         │
│  │  │ Validate │  │ Auto     │  │  Stale   │         │         │
│  │  │ Issues   │  │ Label    │  │ Manager  │         │         │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘         │         │
│  │       │             │             │                │         │
│  │  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐         │         │
│  │  │ Sync     │  │ Context  │  │  Docs    │         │         │
│  │  │ TO-DO    │  │ Capture  │  │  Auto    │         │         │
│  │  └──────────┘  └──────────┘  └──────────┘         │         │
│  │                                                      │         │
│  └──────────────────────┬───────────────────────────────┘         │
│                         │                                         │
│  ┌──────────────────────▼──────────────────────┐                 │
│  │          Python Scripts Layer                │                 │
│  ├──────────────────────────────────────────────┤                 │
│  │  • sync-issues-to-todo.py                   │                 │
│  │  • capture-session.py                        │                 │
│  │  • generate-docs.py                          │                 │
│  │  • validate-config.py                        │                 │
│  └──────────────────────┬───────────────────────┘                 │
│                         │                                         │
│  ┌──────────────────────▼──────────────────────┐                 │
│  │         Configuration & Data Layer           │                 │
│  ├──────────────────────────────────────────────┤                 │
│  │  • idd-config.yml (settings)                │                 │
│  │  • TO-DO.md (synced issues)                 │                 │
│  │  • docs/ (auto-generated)                   │                 │
│  │  • .ai/ (context memory)                    │                 │
│  └──────────────────────────────────────────────┘                 │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

External Integrations:
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Slack     │     │   VS Code    │     │      AI      │
│ Notifications│     │   Copilot    │     │   Assistants │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Design Principles

1. **Issue-Centric**: Issues are the single source of truth
2. **Automation-First**: Reduce manual overhead through workflows
3. **AI-Augmented**: Provide rich context for AI assistants
4. **Git-Native**: Work within Git conventions
5. **Privacy-Conscious**: Respect code privacy settings
6. **Extensible**: Easy to customize and extend
7. **Observable**: Built-in metrics and monitoring

---

## Component Architecture

### 1. Issue Templates

**Purpose**: Standardize issue creation with required fields

**Location**: `.github/ISSUE_TEMPLATE/`

**Components**:
- `bug_report.yml` - Bug reports
- `feature_request.yml` - Feature requests
- `task.yml` - General tasks
- `research.yml` - Research spikes
- `config.yml` - Template configuration

**Key Features**:
```yaml
# Structure
name: Issue Type
description: Description of issue type
title: "[TYPE]: "
labels: ["label1", "label2"]
body:
  - type: markdown | input | textarea | dropdown | checkboxes
    attributes:
      label: Field Label
      description: Field Description
      required: true/false
```

**Integration Points**:
- GitHub Issue API
- Auto-label workflow
- Validation workflow

### 2. GitHub Actions Workflows

**Purpose**: Orchestrate automation and validation

**Location**: `.github/workflows/`

#### Workflow Inventory

| Workflow | Trigger | Purpose | Frequency |
|----------|---------|---------|-----------|
| `issue-validation.yml` | Issue opened/edited | Validate issue format | Per issue |
| `auto-label.yml` | Issue opened | Apply labels | Per issue |
| `sync-issues-to-todo.yml` | Schedule + manual | Sync issues to TO-DO.md | Daily |
| `stale-management.yml` | Schedule | Mark stale issues | Daily |
| `ai-context-capture.yml` | Schedule + manual | Capture session context | Daily |
| `docs-auto-generate.yml` | Push to main | Generate documentation | Per push |
| `pr-validation.yml` | PR opened | Validate PR format | Per PR |

#### Workflow Architecture

```yaml
# Standard workflow structure
name: Workflow Name
on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily
  workflow_dispatch:  # Manual trigger
  issues:
    types: [opened, edited]

jobs:
  job-name:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          pip install -r requirements.txt
          python3 bin/script-name.py
```

**Shared Secrets**:
- `GITHUB_TOKEN` - Automatic, scoped to repo
- `SLACK_WEBHOOK_URL` - Optional, for notifications

### 3. Python Scripts Layer

**Purpose**: Core automation logic

**Location**: `bin/`

#### Script Architecture

```python
# Standard script structure
#!/usr/bin/env python3
"""
Script description.
"""

import os
import sys
from github import Github
from pathlib import Path

def load_config() -> dict:
    """Load configuration from idd-config.yml"""
    pass

def main():
    """Main execution flow"""
    try:
        # Load config
        config = load_config()
        
        # Initialize GitHub client
        token = os.environ.get('GITHUB_TOKEN')
        g = Github(token)
        
        # Execute logic
        result = execute_task(g, config)
        
        # Return status
        sys.exit(0 if result else 1)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### Script Dependencies

```
github (PyGithub)
├── GitHub API client
├── Issues, PRs, repositories
└── Rate limiting handling

pyyaml
├── Configuration parsing
└── Data serialization

requests (optional)
├── Slack notifications
└── External webhooks
```

### 4. Configuration System

**Purpose**: Centralized settings management

**Location**: `idd-config.yml`

**Architecture**:

```yaml
# Configuration hierarchy
project:              # Top-level project settings
  name: string
  repository: string
  default_branch: string
  
labels:               # Label taxonomy
  track_labels: []    # Labels for tracking
  exempt_from_stale: []
  auto_label_rules: {}
  smart_labels: {}
  
workflows:            # Workflow toggles
  sync_issues: bool
  stale_management: bool
  ai_context: bool
  documentation: bool
  pr_validation: bool
  schedules: {}
  
stale_management:     # Stale issue config
  days_until_stale: int
  days_until_close: int
  exempt_labels: []
  
ai_context:           # AI context config
  enabled: bool
  privacy_mode: string
  capture_frequency: string
  context_files: []
  
documentation:        # Docs config
  auto_changelog: bool
  auto_stats: bool
  
notifications:        # Integration config
  slack_webhook_url: string
```

**Environment Variables**:
```bash
# Override config with env vars
export IDD_PROJECT_NAME="My Project"
export IDD_SLACK_WEBHOOK_URL="${SLACK_WEBHOOK}"
export GITHUB_TOKEN="${GITHUB_TOKEN}"
```

---

## Workflow Orchestration

### Execution Flow

```
Issue Created
    ↓
┌───────────────────────────────────┐
│ 1. Issue Validation Workflow      │
│    - Check required fields        │
│    - Validate format              │
│    - Comment if invalid           │
└───────┬───────────────────────────┘
        ↓
┌───────────────────────────────────┐
│ 2. Auto-Label Workflow            │
│    - Apply type labels            │
│    - Apply smart labels           │
│    - Apply keyword-based labels   │
└───────┬───────────────────────────┘
        ↓
┌───────────────────────────────────┐
│ 3. Sync to TO-DO.md (Scheduled)   │
│    - Query open issues            │
│    - Group by track label         │
│    - Update TO-DO.md              │
│    - Commit changes               │
└───────┬───────────────────────────┘
        ↓
Work on Issue
    ↓
┌───────────────────────────────────┐
│ 4. AI Context Capture (Scheduled) │
│    - Capture git log              │
│    - Capture file changes         │
│    - Update .ai/context.json      │
│    - Commit context               │
└───────┬───────────────────────────┘
        ↓
Create PR
    ↓
┌───────────────────────────────────┐
│ 5. PR Validation Workflow         │
│    - Check PR format              │
│    - Verify issue link            │
│    - Check commit messages        │
│    - Validate tests               │
└───────┬───────────────────────────┘
        ↓
Merge PR
    ↓
┌───────────────────────────────────┐
│ 6. Docs Auto-Generate Workflow    │
│    - Update CHANGELOG.md          │
│    - Generate stats               │
│    - Update README badges         │
│    - Commit docs                  │
└───────┬───────────────────────────┘
        ↓
Issue Closed
    ↓
┌───────────────────────────────────┐
│ 7. Stale Management (Scheduled)   │
│    - Mark inactive issues stale   │
│    - Close stale issues           │
│    - Skip exempt labels           │
└───────────────────────────────────┘
```

### Workflow Dependencies

```
Issue Templates
    ↓
Issue Validation → Auto-Label
    ↓                 ↓
Sync to TO-DO ←──────┘
    ↓
AI Context Capture
    ↓
Stale Management

PR Created
    ↓
PR Validation
    ↓
Merge → Docs Auto-Generate
```

---

## AI Context System

### Context Capture Architecture

```
┌─────────────────────────────────────────────────────┐
│              AI Context System                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  Session Capture (capture-session.py)      │    │
│  ├────────────────────────────────────────────┤    │
│  │  Input:                                     │    │
│  │    • Git log (last N commits)             │    │
│  │    • Git diff (uncommitted changes)        │    │
│  │    • File modifications                    │    │
│  │    • Issue references                      │    │
│  │  Output:                                    │    │
│  │    • .ai/context.json                      │    │
│  │    • .ai/session-YYYYMMDD.md              │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  Context Structure                          │    │
│  ├────────────────────────────────────────────┤    │
│  │  {                                          │    │
│  │    "session_id": "uuid",                   │    │
│  │    "timestamp": "ISO-8601",                │    │
│  │    "commits": [                            │    │
│  │      {                                      │    │
│  │        "sha": "abc123",                    │    │
│  │        "message": "feat: ...",             │    │
│  │        "author": "...",                    │    │
│  │        "timestamp": "...",                 │    │
│  │        "files": [...]                      │    │
│  │      }                                      │    │
│  │    ],                                       │    │
│  │    "changes": {                            │    │
│  │      "added": [...],                       │    │
│  │      "modified": [...],                    │    │
│  │      "deleted": [...]                      │    │
│  │    },                                       │    │
│  │    "issues": [                             │    │
│  │      {                                      │    │
│  │        "number": 42,                       │    │
│  │        "title": "...",                     │    │
│  │        "state": "...",                     │    │
│  │        "labels": [...]                     │    │
│  │      }                                      │    │
│  │    ],                                       │    │
│  │    "metrics": {                            │    │
│  │      "lines_added": 123,                   │    │
│  │      "lines_deleted": 45,                  │    │
│  │      "files_changed": 5                    │    │
│  │    }                                        │    │
│  │  }                                          │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Privacy Modes

| Mode | Code Captured | Context Provided |
|------|---------------|------------------|
| **None** | ❌ No code | Issue titles, commit messages only |
| **Minimal** | ⚠️ File paths | File names, structure, no content |
| **Standard** | ✅ Diffs only | Changed code only, no full files |
| **Full** | ✅ Everything | Full file content, complete context |

### Context Usage by AI Assistants

```python
# AI assistant reads context
context = load_context('.ai/context.json')

# Understand recent work
recent_commits = context['commits'][-10:]
active_issues = [i for i in context['issues'] if i['state'] == 'open']

# Provide intelligent suggestions
if 'feat:' in recent_commits[-1]['message']:
    suggest("Consider adding tests for new feature")

if len(active_issues) > 20:
    suggest("Consider closing or prioritizing stale issues")
```

---

## Data Flow

### Issue Synchronization Flow

```
GitHub Issues API
    ↓
Query open issues with specific labels
    ↓
Group issues by track label
    ↓
Format as Markdown sections
    ↓
Write to TO-DO.md
    ↓
Git commit and push
    ↓
TO-DO.md updated in repository
```

### Documentation Generation Flow

```
Git Repository
    ↓
Analyze commits (git log)
    ↓
Extract issue references (#123)
    ↓
Group by type (feat, fix, docs)
    ↓
Generate CHANGELOG.md
    ↓
Calculate metrics (issues closed, PRs merged)
    ↓
Update README.md badges
    ↓
Git commit and push
```

---

## Extension Points

### Adding Custom Workflows

```yaml
# .github/workflows/custom-workflow.yml
name: Custom Workflow
on:
  issues:
    types: [labeled]

jobs:
  custom-job:
    if: contains(github.event.issue.labels.*.name, 'custom-label')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Custom Action
        run: |
          # Your custom logic here
          python3 bin/custom-script.py
```

### Adding Custom Scripts

```python
# bin/custom-script.py
#!/usr/bin/env python3
"""Custom automation script."""

import os
from github import Github

def main():
    token = os.environ['GITHUB_TOKEN']
    g = Github(token)
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
    
    # Your custom logic
    issues = repo.get_issues(state='open')
    for issue in issues:
        # Process issues
        pass

if __name__ == '__main__':
    main()
```

### Adding Custom Labels

```yaml
# In idd-config.yml
labels:
  auto_label_rules:
    custom-keyword:
      - custom-label
  smart_labels:
    custom:
      - pattern: ".*urgent.*"
        label: priority:high
```

---

## Security Model

### Permissions Required

**GitHub Actions**:
```yaml
permissions:
  contents: write      # Commit files
  issues: write        # Create/modify issues
  pull-requests: write # Create/modify PRs
```

**API Token** (for local scripts):
```bash
# Generate at https://github.com/settings/tokens
# Required scopes:
#   - repo (full control)
#   - workflow (update workflows)
export GITHUB_TOKEN="ghp_xxxxx"
```

### Secret Management

```yaml
# Secrets stored in GitHub Settings
secrets:
  GITHUB_TOKEN:        # Auto-provided by GitHub Actions
  SLACK_WEBHOOK_URL:   # Optional Slack integration
  CUSTOM_API_KEY:      # Any custom integrations
```

**Best Practices**:
- Never commit secrets to repository
- Use environment variables
- Rotate tokens regularly
- Use minimal required permissions

### Privacy Considerations

**Code Privacy**:
- Private repositories: full content in context
- Public repositories: consider privacy mode
- Sensitive data: use `.gitignore` and context filters

**AI Context Privacy**:
```yaml
# idd-config.yml
ai_context:
  privacy_mode: "minimal"  # Don't capture code content
  exclude_patterns:
    - "*.env"
    - "*.key"
    - "secrets/*"
```

---

## Performance Considerations

### Rate Limiting

**GitHub API**:
- Authenticated: 5,000 requests/hour
- Actions: 1,000 requests/hour per workflow

**Strategies**:
```python
# Use conditional requests
if_modified_since = last_sync_time
issues = repo.get_issues(since=if_modified_since)

# Batch operations
for issue in issues[:100]:  # Process in batches
    process_issue(issue)
```

### Workflow Optimization

**Caching**:
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

**Conditional Execution**:
```yaml
jobs:
  job-name:
    if: contains(github.event.issue.labels.*.name, 'automation')
```

### Storage Optimization

**Context Files**:
- Rotate old session files (keep last 30 days)
- Compress historical context
- Exclude large binary files

```python
# Cleanup old sessions
import glob
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(days=30)
for file in glob.glob('.ai/session-*.md'):
    if file_date(file) < cutoff:
        os.remove(file)
```

---

## API Reference

### Python Scripts API

#### sync-issues-to-todo.py

```python
def sync_issues(
    repo: str,
    labels: List[str],
    output_file: str = 'TO-DO.md'
) -> bool:
    """
    Sync GitHub issues to TO-DO.md file.
    
    Args:
        repo: Repository in 'owner/repo' format
        labels: List of label names to include
        output_file: Output file path
        
    Returns:
        True if successful, False otherwise
    """
```

#### capture-session.py

```python
def capture_session(
    repo_path: str,
    privacy_mode: str = 'standard',
    output_dir: str = '.ai'
) -> Dict[str, Any]:
    """
    Capture current session context.
    
    Args:
        repo_path: Path to git repository
        privacy_mode: 'none'|'minimal'|'standard'|'full'
        output_dir: Directory for context files
        
    Returns:
        Context dictionary
    """
```

#### generate-docs.py

```python
def generate_changelog(
    repo: str,
    since_tag: Optional[str] = None
) -> str:
    """
    Generate CHANGELOG.md from commits.
    
    Args:
        repo: Repository in 'owner/repo' format
        since_tag: Generate since this tag
        
    Returns:
        Changelog markdown content
    """
```

### Configuration API

```python
from pathlib import Path
import yaml

def load_config(config_path: str = 'idd-config.yml') -> dict:
    """Load and validate configuration."""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    validate_config(config)
    return config

def validate_config(config: dict) -> bool:
    """Validate configuration structure."""
    required_keys = ['project', 'labels', 'workflows']
    return all(key in config for key in required_keys)
```

---

## Deployment Architecture

### Local Development

```
Developer Machine
    ↓
git clone repository
    ↓
./bin/setup-idd.sh (interactive setup)
    ↓
Edit idd-config.yml
    ↓
git add idd-config.yml
git commit -m "chore: configure IDD"
git push
    ↓
Workflows active in GitHub
```

### CI/CD Pipeline

```
Push to Repository
    ↓
GitHub Actions Runner
    ↓
┌─────────────────────────────┐
│ Workflow Execution          │
├─────────────────────────────┤
│ 1. Checkout code            │
│ 2. Setup Python             │
│ 3. Install dependencies     │
│ 4. Run script               │
│ 5. Commit results           │
│ 6. Push changes             │
│ 7. Send notifications       │
└─────────────────────────────┘
    ↓
Results visible in GitHub
```

---

## Monitoring and Observability

### Built-in Metrics

```yaml
# Automatically tracked in docs/stats.md
metrics:
  issues:
    total: 42
    open: 15
    closed: 27
    avg_time_to_close: "3.2 days"
  
  pull_requests:
    total: 38
    merged: 35
    closed: 3
    avg_time_to_merge: "1.5 days"
  
  commits:
    total: 156
    last_week: 23
    top_contributors: [...]
```

### Workflow Monitoring

```bash
# View workflow runs
gh run list --workflow=sync-issues-to-todo.yml

# View workflow logs
gh run view <run-id> --log

# Re-run failed workflow
gh run rerun <run-id>
```

---

## Troubleshooting Architecture Issues

### Common Issues

**Workflow Not Running**:
```yaml
# Check workflow syntax
gh workflow view sync-issues-to-todo.yml

# Check workflow permissions
permissions:
  contents: write  # ← Ensure this is set
```

**Script Failures**:
```bash
# Run locally to debug
export GITHUB_TOKEN="your-token"
export GITHUB_REPOSITORY="owner/repo"
python3 bin/sync-issues-to-todo.py
```

**Configuration Errors**:
```bash
# Validate configuration
python3 bin/validate-config.py idd-config.yml
```

---

**For more information, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**
