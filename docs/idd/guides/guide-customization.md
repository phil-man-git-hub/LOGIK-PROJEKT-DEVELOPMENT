# IDD Customization Guide

Complete guide to customizing Issue-Driven Development for your team's specific needs.

## Table of Contents

- [Overview](#overview)
- [Configuration File](#configuration-file)
- [Project Settings](#project-settings)
- [Labels Configuration](#labels-configuration)
- [Workflows Configuration](#workflows-configuration)
- [AI Context System](#ai-context-system)
- [Documentation](#documentation)
- [Notifications](#notifications)
- [Advanced Customization](#advanced-customization)
- [Examples by Team Type](#examples-by-team-type)

---

## Overview

The IDD system is highly customizable through the `idd-config.yml` file. This guide explains every configuration option and provides examples for common scenarios.

### Configuration Hierarchy

```
idd-config.yml          # Main configuration
├── project             # Project metadata
├── files               # File paths
├── labels              # Label configuration
├── workflows           # Workflow toggles and schedules
├── stale               # Stale issue management
├── ai_context          # AI context system
├── documentation       # Auto-documentation
├── notifications       # Slack/email notifications
└── custom              # Your custom settings
```

---

## Configuration File

### Location

```bash
# Standard location (repository root)
./idd-config.yml

# Custom location (set environment variable)
export IDD_CONFIG_PATH=/path/to/custom-config.yml
```

### Format

```yaml
# YAML format
# Comments start with #
# Indentation matters (use 2 spaces)
# Booleans: true/false
# Lists: use - prefix
# Strings: optional quotes
```

### Validation

```bash
# Check syntax
python3 -c "import yaml; yaml.safe_load(open('idd-config.yml'))"

# Validate with IDD tool
python3 bin/validate-config.py idd-config.yml
```

---

## Project Settings

### Basic Configuration

```yaml
project:
  name: "My Project"              # Project display name
  repository: "owner/repo"        # GitHub repository
  description: "Brief description" # Project description
  main_branch: "main"             # Default branch (main/master)
  url: "https://github.com/owner/repo"  # Repository URL
```

### Examples

**Startup Project:**
```yaml
project:
  name: "Startup MVP"
  repository: "startup/mvp"
  description: "Minimum viable product"
  main_branch: "main"
```

**Enterprise Project:**
```yaml
project:
  name: "Enterprise Platform - Customer Portal"
  repository: "enterprise/customer-portal"
  description: "Customer-facing portal for enterprise clients"
  main_branch: "develop"  # Use develop branch
  url: "https://github.enterprise.com/enterprise/customer-portal"
```

---

## Labels Configuration

### Track Labels

Labels that will appear in TO-DO.md:

```yaml
labels:
  track:
    - "enhancement"      # New features
    - "bug"             # Bug fixes
    - "documentation"   # Documentation tasks
    - "infrastructure"  # Infrastructure work
    - "research"        # Research/investigation
```

**Small Team (minimal):**
```yaml
labels:
  track:
    - "task"
    - "bug"
```

**Large Team (comprehensive):**
```yaml
labels:
  track:
    - "enhancement"
    - "bug"
    - "documentation"
    - "infrastructure"
    - "research"
    - "security"
    - "performance"
    - "refactor"
    - "testing"
    - "design"
```

### Exempt from Stale

Labels that prevent issues from being marked stale:

```yaml
labels:
  exempt_from_stale:
    - "pinned"           # Pinned issues
    - "security"         # Security issues
    - "critical"         # Critical bugs
    - "in-progress"      # Currently being worked on
    - "blocked"          # Blocked by external factors
```

### Auto-Labeling Rules

Automatically apply labels based on content:

```yaml
labels:
  auto_label:
    feature:
      keywords: ["feature", "add", "implement", "create"]
      labels: ["enhancement"]
    
    bug:
      keywords: ["bug", "error", "fix", "broken", "crash"]
      labels: ["bug"]
    
    documentation:
      keywords: ["document", "docs", "guide", "readme"]
      labels: ["documentation"]
    
    performance:
      keywords: ["performance", "slow", "optimize", "speed"]
      labels: ["performance"]
```

**Custom Auto-Labels:**
```yaml
labels:
  auto_label:
    frontend:
      keywords: ["ui", "ux", "interface", "css", "html"]
      labels: ["frontend", "ui"]
    
    backend:
      keywords: ["api", "database", "server", "backend"]
      labels: ["backend", "api"]
    
    mobile:
      keywords: ["ios", "android", "mobile", "app"]
      labels: ["mobile"]
    
    security:
      keywords: ["security", "vulnerability", "exploit", "auth"]
      labels: ["security", "critical"]
```

### Smart Labels

Priority and effort estimation:

```yaml
labels:
  smart_labels:
    priority:
      high:
        keywords: ["urgent", "critical", "asap", "blocking"]
        label: "priority:high"
      medium:
        keywords: ["important", "soon"]
        label: "priority:medium"
      low:
        keywords: ["nice to have", "eventually", "someday"]
        label: "priority:low"
    
    effort:
      large:
        keywords: ["major", "complex", "large effort", "epic"]
        label: "effort:large"
      medium:
        keywords: ["moderate", "medium effort"]
        label: "effort:medium"
      small:
        keywords: ["quick", "small", "trivial", "easy"]
        label: "effort:small"
```

---

## Workflows Configuration

### Enable/Disable Workflows

```yaml
workflows:
  issue_sync: true         # Sync issues to TO-DO.md
  auto_label: true         # Auto-label issues
  pr_validation: true      # Validate pull requests
  commit_linking: true     # Link commits to issues
  stale_management: true   # Mark stale issues
  smart_labeling: true     # Apply smart labels
  auto_docs: true          # Generate documentation
```

**Minimal Setup:**
```yaml
workflows:
  issue_sync: true
  auto_label: false
  pr_validation: true
  commit_linking: true
  stale_management: false
  smart_labeling: false
  auto_docs: false
```

**Full Automation:**
```yaml
workflows:
  issue_sync: true
  auto_label: true
  pr_validation: true
  commit_linking: true
  stale_management: true
  smart_labeling: true
  auto_docs: true
```

### Schedule Configuration

```yaml
workflows:
  issue_sync:
    enabled: true
    schedule: "0 */6 * * *"  # Every 6 hours
    # Cron format: minute hour day month weekday
  
  stale_management:
    enabled: true
    schedule: "0 0 * * *"     # Daily at midnight
  
  auto_docs:
    enabled: true
    schedule: "0 0 * * 0"     # Weekly on Sunday
```

**Custom Schedules:**
```yaml
workflows:
  issue_sync:
    enabled: true
    schedule: "*/30 * * * *"  # Every 30 minutes (high frequency)
  
  stale_management:
    enabled: true
    schedule: "0 9 * * 1"     # Weekly on Monday at 9am
  
  auto_docs:
    enabled: true
    schedule: "0 0 1 * *"     # Monthly on the 1st
```

---

## Stale Management

### Configuration

```yaml
stale:
  enabled: true
  days_before_stale: 60        # Days before marking stale
  days_before_close: 7         # Days before closing stale issue
  stale_label: "stale"         # Label to apply
  
  # Custom messages
  stale_message: >
    This issue has been automatically marked as stale because it has not had
    recent activity. It will be closed if no further activity occurs.
  
  close_message: >
    This issue has been automatically closed due to inactivity.
  
  operations_per_run: 30       # API rate limiting
```

**Aggressive Stale Management (Fast-Moving Projects):**
```yaml
stale:
  enabled: true
  days_before_stale: 30
  days_before_close: 3
  exempt_labels:
    - "pinned"
    - "in-progress"
```

**Conservative (Long-Running Projects):**
```yaml
stale:
  enabled: true
  days_before_stale: 90
  days_before_close: 14
  exempt_labels:
    - "pinned"
    - "backlog"
    - "future"
```

---

## AI Context System

### Basic Configuration

```yaml
ai_context:
  enabled: true
  
  capture:
    auto_capture: true           # Automatic session capture
    capture_commits: true        # Capture commit history
    capture_issues: true         # Capture issue data
    capture_prs: true           # Capture PR data
    capture_reviews: true       # Capture code reviews
  
  search:
    index_sessions: true        # Index sessions for search
    index_snapshots: true       # Index snapshots
    index_insights: true        # Index insights
    index_documentation: true   # Index docs
  
  retention:
    max_sessions: 100           # Maximum sessions to keep
    max_age_days: 90           # Maximum age in days
    auto_cleanup: true         # Automatic cleanup
```

**Privacy-Conscious:**
```yaml
ai_context:
  enabled: true
  capture:
    auto_capture: false     # Manual capture only
    capture_commits: true
    capture_issues: false   # Don't capture issue content
    capture_prs: false
  retention:
    max_sessions: 50
    max_age_days: 30       # Keep for 30 days only
```

**Maximum Context:**
```yaml
ai_context:
  enabled: true
  capture:
    auto_capture: true
    capture_commits: true
    capture_issues: true
    capture_prs: true
    capture_reviews: true
    capture_discussions: true
  retention:
    max_sessions: 500      # Keep lots of history
    max_age_days: 365      # Keep for 1 year
```

---

## Documentation

### Auto-Documentation Configuration

```yaml
documentation:
  changelog:
    enabled: true
    include_commits: true       # Include commit history
    include_prs: true          # Include PR history
    include_issues: true       # Include closed issues
    days_to_include: 7         # Last 7 days
  
  stats:
    enabled: true
    include_code_stats: true   # LOC, files, etc.
    include_issue_stats: true  # Issue metrics
    include_pr_stats: true     # PR metrics
  
  readme:
    auto_update: true
    stats_marker: "<!-- IDD_STATS -->"
    changelog_marker: "<!-- IDD_CHANGELOG -->"
```

**Detailed Documentation:**
```yaml
documentation:
  changelog:
    enabled: true
    include_commits: true
    include_prs: true
    include_issues: true
    include_contributors: true
    days_to_include: 30        # Monthly changelog
    group_by_type: true        # Group by feat/fix/docs
  
  stats:
    enabled: true
    include_code_stats: true
    include_issue_stats: true
    include_pr_stats: true
    include_contributor_stats: true
    include_activity_graph: true
```

**Minimal Documentation:**
```yaml
documentation:
  changelog:
    enabled: true
    include_commits: false
    include_prs: true          # PRs only
    days_to_include: 7
  
  stats:
    enabled: false            # No stats
```

---

## Notifications

### Slack Integration

```yaml
notifications:
  slack:
    enabled: true
    webhook_url: "${SLACK_WEBHOOK_URL}"  # From environment
    channel: "#development"
    notify_on:
      - "issue_created"
      - "issue_closed"
      - "pr_opened"
      - "pr_merged"
      - "pr_closed"
```

**Minimal Notifications:**
```yaml
notifications:
  slack:
    enabled: true
    webhook_url: "${SLACK_WEBHOOK_URL}"
    channel: "#dev-alerts"
    notify_on:
      - "pr_merged"            # Only merged PRs
```

**Verbose Notifications:**
```yaml
notifications:
  slack:
    enabled: true
    webhook_url: "${SLACK_WEBHOOK_URL}"
    channel: "#dev-activity"
    notify_on:
      - "issue_created"
      - "issue_closed"
      - "issue_labeled"
      - "pr_opened"
      - "pr_merged"
      - "pr_closed"
      - "pr_reviewed"
      - "commit_pushed"
```

---

## Advanced Customization

### Custom Rules

```yaml
custom:
  # Team-specific settings
  team:
    working_hours: "9-17"
    timezone: "America/New_York"
    code_freeze: false
  
  # Automation rules
  automation:
    auto_close_invalid: false
    auto_merge_dependabot: false
    require_issue_link: true
  
  # Integration settings
  integrations:
    jira_enabled: false
    confluence_enabled: false
```

### Environment Variables

```bash
# .env file (git-ignored)
GITHUB_TOKEN=ghp_your_token
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
IDD_DEBUG=false
IDD_CONFIG_PATH=./idd-config.yml
TODO_FILE_PATH=./TO-DO.md
```

---

## Examples by Team Type

### Small Team (2-5 people)

```yaml
project:
  name: "Startup MVP"
  repository: "startup/mvp"

labels:
  track: ["task", "bug"]

workflows:
  issue_sync: true
  auto_label: true
  pr_validation: true
  commit_linking: true
  stale_management: false      # No stale management
  smart_labeling: false
  auto_docs: false

ai_context:
  enabled: true
  retention:
    max_sessions: 50

documentation:
  changelog:
    enabled: false             # Manual changelog
```

### Medium Team (5-20 people)

```yaml
project:
  name: "Product Platform"
  repository: "company/platform"

labels:
  track:
    - "enhancement"
    - "bug"
    - "documentation"

workflows:
  issue_sync: true
  auto_label: true
  pr_validation: true
  commit_linking: true
  stale_management: true       # Enable stale
  smart_labeling: true
  auto_docs: true

stale:
  days_before_stale: 60
  days_before_close: 7

documentation:
  changelog:
    enabled: true
    days_to_include: 14        # Bi-weekly
```

### Enterprise Team (20+ people)

```yaml
project:
  name: "Enterprise Platform"
  repository: "corp/platform"

labels:
  track:
    - "enhancement"
    - "bug"
    - "documentation"
    - "infrastructure"
    - "security"
    - "performance"
  
  smart_labels:
    priority:
      critical:
        keywords: ["critical", "urgent", "p0"]
        label: "priority:critical"
      high:
        keywords: ["high", "important", "p1"]
        label: "priority:high"

workflows:
  issue_sync: true
  auto_label: true
  pr_validation: true
  commit_linking: true
  stale_management: true
  smart_labeling: true
  auto_docs: true

pr_validation:
  require_conventional_commits: true
  require_linked_issue: true
  min_description_length: 50
  auto_assign_reviewers: true
  max_reviewers: 3

notifications:
  slack:
    enabled: true
    channel: "#engineering"
```

### Open Source Project

```yaml
project:
  name: "Open Source Library"
  repository: "org/library"

labels:
  track:
    - "enhancement"
    - "bug"
    - "documentation"
    - "good first issue"
    - "help wanted"

workflows:
  issue_sync: true
  auto_label: true
  pr_validation: true
  commit_linking: true
  stale_management: true
  smart_labeling: true
  auto_docs: true

stale:
  days_before_stale: 90        # Longer for OSS
  days_before_close: 14
  exempt_labels:
    - "good first issue"
    - "help wanted"
    - "pinned"

documentation:
  changelog:
    enabled: true
    include_contributors: true # Credit contributors
    days_to_include: 30
```

---

## Configuration Best Practices

### 1. Start Simple

Begin with minimal configuration:
```yaml
workflows:
  issue_sync: true
  pr_validation: true
```

Then add features as needed.

### 2. Use Environment Variables for Secrets

```yaml
# idd-config.yml
notifications:
  slack:
    webhook_url: "${SLACK_WEBHOOK_URL}"

# .env (git-ignored)
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

### 3. Document Your Customizations

```yaml
# Company-specific configuration
# Contact: devops@company.com
# Last updated: 2024-01-15

custom:
  company_standards:
    commit_format: "conventional"
    review_required: 2
```

### 4. Version Control Your Config

```bash
# Commit configuration
git add idd-config.yml
git commit -m "chore: update IDD configuration"

# Tag major changes
git tag idd-config-v1.0
```

### 5. Test Configuration Changes

```bash
# Validate syntax
python3 bin/validate-config.py idd-config.yml

# Test in branch
git checkout -b test-idd-config
# ... make changes ...
# ... test ...
git checkout main
```

---

## Troubleshooting Configuration

### Configuration Not Loading

```bash
# Check file location
ls -la idd-config.yml

# Check syntax
python3 -c "import yaml; print(yaml.safe_load(open('idd-config.yml')))"

# Check environment variable
echo $IDD_CONFIG_PATH
```

### Workflows Not Respecting Config

```bash
# Workflows read config from repository
# Ensure idd-config.yml is committed and pushed

git add idd-config.yml
git commit -m "chore: update config"
git push
```

### Labels Not Working

```bash
# Ensure labels exist in repository
gh label list

# Create missing labels
gh label create "priority:high" --color "d73a4a"
```

---

## Next Steps

After customizing configuration:

1. **Test thoroughly** - Validate all changes
2. **Document decisions** - Explain why you chose specific settings
3. **Train team** - Ensure everyone understands the configuration
4. **Monitor** - Watch for issues with new configuration
5. **Iterate** - Adjust based on team feedback

## Related Documentation

- [Setup Guide](SETUP_GUIDE.md) - Installation instructions
- [Best Practices](BEST_PRACTICES.md) - Usage guidelines
- [Architecture](ARCHITECTURE.md) - System design
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues

---

**Need help customizing? Open an issue with the "question" label!**
