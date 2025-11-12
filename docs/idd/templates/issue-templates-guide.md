# GitHub Issue Templates Usage Guide
# Issue Filename Convention

To reduce cognitive load and improve organization, all issue files in `docs/idd/issues/` should use the following naming pattern:

`<issue_type>-<topic>.md`

**Examples:**
- `bug_report-snmp_timeout.md`
- `feature_request-codespaces_integration.md`
- `task-add_librenms_monitoring.md`
- `documentation-freeipa_certificate_workflow.md`
- `monitoring_alert-high_memory_lima.md`

**Rationale:**
- Placing the issue type first makes it easy to visually scan and filter issues by type.
- Consistent naming helps contributors and automation tools quickly locate and process issues.
- Reduces ambiguity and cognitive load for humans working with many issues.

**Enforcement:**
- Please follow this pattern when creating new issues manually or via automation.
- Future scripts and workflows may validate this convention automatically.


## Overview

This repository uses standardized issue templates to ensure consistent, high-quality issue reporting and tracking. Each template is designed for a specific type of issue and includes relevant fields and checklists.

## Available Templates

### 1. 🐛 Bug Report (`bug_report.md`)

**When to use:**
- Software is not working as expected
- Errors or exceptions occurring
- Unexpected behavior observed
- Performance issues

**Key sections:**
- Bug description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages/logs

**Auto-applied labels:** `bug`, `needs-triage`

**Example:**
```
Title: [BUG] LibreNMS not capturing CPU data from macOS devices
```

---

### 2. ✨ Feature Request (`feature_request.md`)

**When to use:**
- Proposing new functionality
- Suggesting enhancements
- Requesting new capabilities

**Key sections:**
- Feature description
- Problem/motivation
- Proposed solution
- Alternatives considered
- Implementation ideas
- Priority assessment

**Auto-applied labels:** `enhancement`, `needs-discussion`

**Example:**
```
Title: [FEATURE] Add automated certificate renewal for FreeIPA
```

---

### 3. ✅ Task (`task.md`)

**When to use:**
- General development work
- Maintenance tasks
- Refactoring work
- Implementation of planned features

**Key sections:**
- Task description and context
- Acceptance criteria (checkboxes)
- Implementation steps
- Dependencies
- Testing plan
- Effort estimate

**Auto-applied labels:** `task`

**Example:**
```
Title: Add whiskey.projekt.lab to LibreNMS monitoring
```

---

### 4. 📚 Documentation (`documentation.md`)

**When to use:**
- Creating new documentation
- Updating existing docs
- Fixing documentation errors
- Improving clarity

**Key sections:**
- Documentation type
- Current state assessment
- Target audience
- Content outline
- Examples/code samples needed
- Success criteria

**Auto-applied labels:** `documentation`

**Example:**
```
Title: [DOCS] Document FreeIPA certificate management workflow
```

---

### 5. 🚨 Monitoring Alert (`monitoring_alert.md`)

**When to use:**
- LibreNMS alerts
- Graylog alerts
- System monitoring issues
- Infrastructure alerts

**Key sections:**
- Alert information (source, severity, affected system)
- Alert details and timestamps
- Symptoms and impact
- Investigation findings
- Remediation steps
- Root cause analysis

**Auto-applied labels:** `monitoring`, `infrastructure`

**Example:**
```
Title: [ALERT] High memory usage on lima.projekt.lab
```

---

## How to Use Templates

### Via GitHub Web UI

1. Navigate to the [Issues page](https://github.com/phil-man-git-hub/WORKSTATION-CONFIGURATION/issues)
2. Click "New Issue"
3. Select the appropriate template
4. Fill in all required sections
5. Submit the issue

### Via GitHub CLI (`gh`)

```bash
# List available templates
gh issue create --help

# Create issue with specific template (interactive)
gh issue create

# Create issue with all details (non-interactive)
gh issue create \
  --title "Your issue title" \
  --body "Issue body content" \
  --label "bug" \
  --assignee "@me"
```

### Programmatically via API

```python
from github import Github

g = Github("your-token")
repo = g.get_repo("phil-man-git-hub/WORKSTATION-CONFIGURATION")

issue = repo.create_issue(
    title="Your issue title",
    body="Issue body content",
    labels=["bug", "needs-triage"]
)
```

---

## Best Practices

### Writing Good Issues

1. **Be Specific**
   - Use clear, descriptive titles
   - Provide concrete examples
   - Include relevant context

2. **Be Complete**
   - Fill in all template sections
   - Don't delete template structure
   - Add additional information if helpful

3. **Be Actionable**
   - Define clear acceptance criteria
   - Specify what "done" looks like
   - Break down into steps if complex

4. **Link Related Items**
   - Reference related issues
   - Link to relevant PRs
   - Note dependencies

### Title Conventions

**Good titles:**
```
[BUG] SNMP timeout when polling romeo.projekt.lab
Add support for Ubuntu 24.04 in deployment scripts
[DOCS] Update monitoring setup guide with TLS configuration
[ALERT] LibreNMS disk space critical on lima.projekt.lab
```

**Bad titles:**
```
It doesn't work
Help!
Question about something
Fix the thing
```

### Using Labels

**Standard labels:**
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `task` - General work item
- `monitoring` - Monitoring/infrastructure related
- `idd` - Issue-Driven Development implementation
- `good-first-issue` - Good for newcomers
- `needs-triage` - Needs initial review
- `needs-discussion` - Requires team discussion

**Phase labels:**
- `phase-1-foundation` - Phase 1 work
- `phase-2-ai-memory` - Phase 2 work
- `phase-3-automation` - Phase 3 work
- `phase-4-template` - Phase 4 work

**Priority labels:**
- `priority: critical` - Immediate attention required
- `priority: high` - Important, address soon
- `priority: medium` - Normal priority
- `priority: low` - Nice to have

---

## Issue Workflow

### Standard Lifecycle

```
1. Issue Created (from template)
   ↓
2. Needs Triage (automatic label)
   ↓
3. Triaged (labels, assignee, milestone set)
   ↓
4. In Progress (work begins, linked to branch)
   ↓
5. PR Created (linked to issue)
   ↓
6. PR Merged (issue auto-closes)
   ↓
7. Verified (tested in production)
```

### Branch Naming Convention

When working on an issue, create a branch with this pattern:

```bash
# For features
feature/issue-1-short-description

# For bug fixes
bugfix/issue-23-short-description

# For documentation
docs/issue-45-short-description

# For tasks
task/issue-67-short-description
```

### Commit Message Convention

Link commits to issues:

```bash
# Feature commit
git commit -m "feat: Add issue templates

Implements #1
- Created 5 standardized templates
- Added usage documentation
- Configured auto-labeling"

# Bug fix commit
git commit -m "fix: Resolve SNMP timeout on macOS

Fixes #23
- Increased timeout from 5s to 10s
- Added retry logic
- Updated error handling"

# Documentation commit
git commit -m "docs: Update monitoring setup guide

Related to #45
- Added TLS configuration section
- Included troubleshooting steps
- Updated screenshots"
```

**Keywords that auto-close issues:**
- `Fixes #123`
- `Closes #123`
- `Resolves #123`

**Keywords that link without closing:**
- `Related to #123`
- `Part of #123`
- `See #123`

---

## Automation

### Auto-Labeling

Issue templates automatically apply labels when created:

- Bug Report → `bug`, `needs-triage`
- Feature Request → `enhancement`, `needs-discussion`
- Task → `task`
- Documentation → `documentation`
- Monitoring Alert → `monitoring`, `infrastructure`

### Issue-TO-DO Sync

Open issues are automatically synced to `TO-DO.md` (once Phase 1 is complete):

```markdown
## Current Sprint
- [ ] #1 Create GitHub issue templates
- [ ] #2 Implement sync automation
- [ ] #3 Set up CI/CD workflows
```

### Stale Issue Management

Issues inactive for 30 days are marked stale and closed after 7 additional days (unless labeled `keep-open`).

---

## Customization

### Adding New Templates

1. Create new file in `.github/ISSUE_TEMPLATE/`
2. Use YAML frontmatter for metadata
3. Include relevant sections
4. Add to this documentation
5. Test the template

**Template structure:**
```markdown
---
name: Template Name
about: Short description
title: '[PREFIX] '
labels: ['label1', 'label2']
assignees: ''
---

## Section 1
Content...

## Section 2
Content...
```

### Modifying Existing Templates

1. Edit the template file
2. Update this documentation
3. Notify team of changes
4. Consider impact on existing issues

---

## Examples

### Example 1: Bug Report

```markdown
Title: [BUG] SNMP timeout when polling romeo.projekt.lab

## Bug Description
LibreNMS fails to poll romeo.projekt.lab (macOS 15.7.1) with SNMP timeout errors.

## Steps to Reproduce
1. Add romeo.projekt.lab to LibreNMS
2. Run discovery: `lnms device:poll romeo.projekt.lab`
3. Observe timeout in logs

## Expected Behavior
SNMP poll should complete within 5 seconds with full device data.

## Actual Behavior
Poll times out after 5 seconds, partial data collected.

## Environment
- OS: macOS 15.7.1
- LibreNMS: 25.11.0
- SNMP Version: v3
- Network: 1Gbps local

## Error Messages/Logs
```
SNMP['/usr/bin/snmpwalk' '-v3' ... -t 5 ... 
SNMP[ Timeout ]
```
```

### Example 2: Feature Request

```markdown
Title: [FEATURE] Add Slack notifications for monitoring alerts

## Feature Description
Send LibreNMS alerts to Slack channel for immediate team notification.

## Problem/Motivation
Currently, alerts only visible in LibreNMS UI. Team misses critical alerts.

## Proposed Solution
Integrate LibreNMS with Slack API:
- Configure webhook URL
- Map alert severity to Slack message format
- Include alert details and graphs

## User Story
As a system administrator, I want to receive critical alerts in Slack
so that I can respond immediately without checking LibreNMS dashboard.
```

---

## Support

**Questions about templates?**
- Open a discussion in [GitHub Discussions](https://github.com/phil-man-git-hub/WORKSTATION-CONFIGURATION/discussions)
- Ask in issue comments
- Refer to [IDD Documentation](../../docs/idd/)

**Found a template bug?**
- Create a bug report issue
- Tag with `documentation`, `templates`

---

*Last Updated: November 5, 2025*  
*Part of Issue-Driven Development (IDD) Implementation*
