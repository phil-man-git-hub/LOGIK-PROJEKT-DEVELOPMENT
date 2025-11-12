# IDD Migration Guide

Guide for migrating to Issue-Driven Development from other issue tracking systems or workflows.

## Table of Contents

- [Overview](#overview)
- [Migration Strategies](#migration-strategies)
- [From Jira](#from-jira)
- [From Linear](#from-linear)
- [From Existing GitHub Workflows](#from-existing-github-workflows)
- [From Trello / Asana](#from-trello--asana)
- [Preserving History](#preserving-history)
- [Team Adoption](#team-adoption)
- [Rollback Plan](#rollback-plan)

---

## Overview

Migrating to IDD can be done gradually or all at once. This guide helps you choose the right approach and execute it successfully.

### Migration Checklist

- [ ] Assess current system
- [ ] Choose migration strategy
- [ ] Export existing data
- [ ] Set up IDD
- [ ] Import/migrate issues
- [ ] Train team
- [ ] Run parallel (optional)
- [ ] Complete cutover
- [ ] Verify and optimize

---

## Migration Strategies

### Strategy 1: Clean Start (Recommended for Small Teams)

**Best for:** New projects, small teams (<5 people), simple workflows

**Steps:**
1. Set up IDD in new repository or branch
2. Close all old issues
3. Create new issues using IDD templates
4. Start fresh with IDD workflows

**Pros:**
- ✅ Clean slate
- ✅ Fastest setup
- ✅ No data migration needed

**Cons:**
- ❌ Loses history
- ❌ Requires team training upfront

**Timeline:** 1-2 days

### Strategy 2: Gradual Adoption (Recommended for Large Teams)

**Best for:** Large teams, complex workflows, ongoing projects

**Steps:**
1. Set up IDD alongside existing system
2. Use IDD for new work only
3. Keep old system for reference
4. Gradually migrate active issues
5. Archive old system when ready

**Pros:**
- ✅ Low risk
- ✅ Gradual learning
- ✅ Preserves history

**Cons:**
- ❌ Maintains two systems temporarily
- ❌ Longer transition

**Timeline:** 2-4 weeks

### Strategy 3: Full Migration (For Complete Transfer)

**Best for:** Mandatory migration, preserving all history

**Steps:**
1. Export all data from old system
2. Set up IDD completely
3. Import/recreate all issues
4. Update links and references
5. Switch over completely

**Pros:**
- ✅ Preserves all history
- ✅ Complete cutover

**Cons:**
- ❌ More complex
- ❌ Requires downtime
- ❌ Data transformation needed

**Timeline:** 1-2 weeks

---

## From Jira

### Export from Jira

```bash
# Export issues via Jira API
curl -u email@example.com:api_token \
  "https://your-domain.atlassian.net/rest/api/3/search?jql=project=PROJ&maxResults=1000" \
  > jira-issues.json

# Or use Jira export feature
# Settings → System → Export → Export issues to CSV
```

### Convert Jira Issues to GitHub

```python
#!/usr/bin/env python3
"""
Convert Jira export to GitHub issues
"""
import json
import csv
from github import Github

# Load Jira export
with open('jira-issues.json') as f:
    jira_data = json.load(f)

# Connect to GitHub
g = Github('your_github_token')
repo = g.get_repo('owner/repo')

# Mapping
status_map = {
    'To Do': 'open',
    'In Progress': 'open',
    'Done': 'closed'
}

type_map = {
    'Story': 'enhancement',
    'Bug': 'bug',
    'Task': 'documentation'
}

# Convert each issue
for jira_issue in jira_data['issues']:
    fields = jira_issue['fields']
    
    # Create GitHub issue
    title = fields['summary']
    body = f"""
**Migrated from Jira:** {jira_issue['key']}

## Description
{fields.get('description', 'No description')}

## Original Reporter
{fields['reporter']['displayName']}

## Created
{fields['created']}

---
*This issue was migrated from Jira*
"""
    
    labels = [type_map.get(fields['issuetype']['name'], 'enhancement')]
    
    gh_issue = repo.create_issue(
        title=title,
        body=body,
        labels=labels
    )
    
    # Close if needed
    if status_map.get(fields['status']['name']) == 'closed':
        gh_issue.edit(state='closed')
    
    print(f"Migrated {jira_issue['key']} → #{gh_issue.number}")
```

### Mapping Guide

| Jira | GitHub IDD |
|------|-----------|
| **Issue Types** | |
| Story | enhancement label |
| Bug | bug label |
| Task | documentation label |
| Epic | Multiple issues + project |
| **Status** | |
| To Do | Open issue |
| In Progress | Open + in-progress label |
| Done | Closed issue |
| **Priority** | |
| Highest | priority:high label |
| High | priority:high label |
| Medium | priority:medium label |
| Low | priority:low label |
| **Components** | |
| Frontend | frontend label |
| Backend | backend label |

### Maintain Links

```python
# Create mapping file
jira_to_github = {
    'PROJ-123': 1,
    'PROJ-124': 2,
    # ...
}

# Update issue bodies with links
for jira_key, gh_number in jira_to_github.items():
    issue = repo.get_issue(gh_number)
    body = issue.body + f"\n\n**Related Jira Issues:** {jira_key}"
    issue.edit(body=body)
```

---

## From Linear

### Export from Linear

```bash
# Use Linear API
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: YOUR_LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ issues { nodes { id title description state { name } } } }"
  }' > linear-issues.json
```

### Convert Linear to GitHub

```python
#!/usr/bin/env python3
"""
Convert Linear export to GitHub issues
"""
import json
from github import Github

# Load Linear export
with open('linear-issues.json') as f:
    linear_data = json.load(f)

g = Github('your_github_token')
repo = g.get_repo('owner/repo')

# Convert
for issue in linear_data['data']['issues']['nodes']:
    title = issue['title']
    body = f"""
{issue['description']}

---
*Migrated from Linear: {issue['id']}*
"""
    
    # Determine state
    state = 'open'
    if issue['state']['name'] in ['Done', 'Completed']:
        state = 'closed'
    
    gh_issue = repo.create_issue(title=title, body=body)
    
    if state == 'closed':
        gh_issue.edit(state='closed')
    
    print(f"Migrated {issue['id']} → #{gh_issue.number}")
```

---

## From Existing GitHub Workflows

### Scenario 1: Basic Issues → IDD

You already use GitHub Issues but want IDD automation.

**Migration Steps:**

1. **Install IDD:**
```bash
./bin/setup-idd.sh
```

2. **Keep existing issues:**
```bash
# No need to migrate - they stay as-is
# Just add labels for IDD tracking
gh issue list --json number,title --jq '.[] | .number' | while read num; do
  gh issue edit $num --add-label "enhancement"
done
```

3. **Add IDD workflows:**
```bash
# Workflows work with existing issues
git add .github/workflows/
git commit -m "feat: add IDD workflows"
git push
```

4. **Sync existing issues:**
```bash
python3 bin/sync-issues-to-todo.py
```

### Scenario 2: Custom Workflows → IDD

You have custom GitHub Actions that need to coexist.

**Strategy: Keep Both**

```yaml
# Your existing workflow
name: Custom CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm test

# IDD workflows run independently
# No conflicts!
```

**Configure IDD to complement:**

```yaml
# idd-config.yml
workflows:
  issue_sync: true    # Enable
  auto_label: false   # Disable if you have custom labeling
  pr_validation: true # Enable
```

### Scenario 3: Project Boards → IDD

Migrating from GitHub Projects to IDD tracking.

**Option A: Keep Projects + Add IDD**
```
Projects for visual management
IDD for automation and tracking
```

**Option B: Replace with IDD**
```bash
# Export project data
gh project list
gh project view 1 --format json > project-export.json

# Create issues from project items
# Use IDD labels instead of columns
```

---

## From Trello / Asana

### Export from Trello

```javascript
// Use Trello API
// Settings → Power-Ups → API → Get your API key and token

fetch('https://api.trello.com/1/boards/{boardId}/cards?key={apiKey}&token={token}')
  .then(res => res.json())
  .then(cards => {
    // Save as trello-cards.json
  });
```

### Convert Trello to GitHub

```python
#!/usr/bin/env python3
import json
from github import Github

with open('trello-cards.json') as f:
    cards = json.load(f)

g = Github('your_token')
repo = g.get_repo('owner/repo')

# Trello list → GitHub label mapping
list_to_label = {
    'To Do': 'status:todo',
    'In Progress': 'status:in-progress',
    'Done': None  # Close issue
}

for card in cards:
    title = card['name']
    body = card.get('desc', 'No description')
    
    # Add Trello link
    body += f"\n\n*Migrated from Trello: {card['shortUrl']}*"
    
    gh_issue = repo.create_issue(title=title, body=body)
    
    # Apply label based on list
    if card['idList'] in list_to_label:
        label = list_to_label[card['idList']]
        if label:
            gh_issue.add_to_labels(label)
        else:
            gh_issue.edit(state='closed')
    
    print(f"Migrated: {title} → #{gh_issue.number}")
```

---

## Preserving History

### Keep Old System Read-Only

```bash
# Archive old issues with a label
gh issue list --state all --json number --jq '.[] | .number' | \
while read num; do
  gh issue edit $num --add-label "archived"
done

# Lock old issues (prevent further changes)
gh issue list --label archived --json number --jq '.[] | .number' | \
while read num; do
  gh issue lock $num
done
```

### Create Migration Index

```markdown
# MIGRATION_INDEX.md

## Old System → New System Mapping

| Old System | Issue ID | GitHub Issue | Status |
|------------|----------|--------------|--------|
| Jira | PROJ-123 | #1 | ✅ Migrated |
| Jira | PROJ-124 | #2 | ✅ Migrated |
| Trello | Card ABC | #3 | ✅ Migrated |

## Migration Date
Started: 2024-01-15
Completed: 2024-01-22

## Notes
- All issues migrated successfully
- Old system archived
- Links preserved in issue bodies
```

### Link References

```python
# Add cross-references to migrated issues
def add_migration_reference(old_id, new_number):
    issue = repo.get_issue(new_number)
    body = issue.body or ""
    body += f"\n\n**Migrated from:** {old_id}"
    issue.edit(body=body)
```

---

## Team Adoption

### Phase 1: Preparation (Week 1)

**Goals:**
- Team understands IDD benefits
- Key stakeholders buy-in
- Migration plan approved

**Activities:**
```
Day 1-2: Present IDD to team
Day 3-4: Gather feedback and concerns
Day 5: Create customized adoption plan
```

### Phase 2: Pilot (Week 2)

**Goals:**
- IDD working for one team/project
- Team comfortable with basics
- Issues identified and resolved

**Activities:**
```
Day 1: Set up IDD
Day 2: Train pilot team
Day 3-5: Pilot team uses IDD exclusively
Day 5: Review and adjust
```

### Phase 3: Rollout (Week 3-4)

**Goals:**
- All teams using IDD
- Old system read-only or archived
- Documentation complete

**Activities:**
```
Week 3: Gradual rollout to remaining teams
Week 4: Full adoption, archive old system
```

### Training Materials

**Create Custom Guide:**
```markdown
# [Your Company] IDD Guide

## Why We're Adopting IDD
- Better tracking
- Automated workflows
- Improved visibility

## How to Get Started
1. Read [QUICK_START.md]
2. Create your first issue
3. Link your commits
4. Create your first PR

## Company-Specific Configuration
- Use labels: customer-request, internal, etc.
- Tag issues with team name
- Follow our commit conventions

## Support
- #dev-tools Slack channel
- Office hours: Tuesdays 2-3pm
- Contact: devops@company.com
```

### Communication Plan

```markdown
## Week 1: Announcement
- Email to all engineering
- Slack announcement
- Demo video

## Week 2: Training
- Live training sessions
- Q&A sessions
- Documentation available

## Week 3: Launch
- Pilot team starts
- Daily check-ins
- Feedback collection

## Week 4: Expansion
- All teams adopt
- Old system archived
- Celebration!
```

---

## Rollback Plan

### Preparation

Before migrating, ensure you can rollback:

```bash
# 1. Backup current workflows
mkdir -p backup/.github
cp -r .github backup/

# 2. Document current state
gh issue list --state all > backup/issues-before.txt
gh pr list --state all > backup/prs-before.txt

# 3. Tag current commit
git tag pre-idd-migration
git push --tags
```

### Rollback Procedure

If you need to rollback:

```bash
# 1. Stop IDD workflows
mv .github/workflows .github/workflows.disabled

# 2. Restore previous workflows (if any)
cp -r backup/.github .

# 3. Remove IDD files
rm -rf bin/*.py
rm idd-config.yml

# 4. Commit
git add .
git commit -m "rollback: remove IDD"
git push

# 5. Communicate to team
echo "IDD rollback complete. Back to previous system."
```

### Rollback Decision Criteria

Consider rollback if:
- ❌ Critical workflows broken for >24 hours
- ❌ Team productivity significantly impacted
- ❌ Data loss or corruption
- ❌ Unfixable integration issues

Don't rollback for:
- ✅ Minor configuration issues
- ✅ Learning curve challenges
- ✅ Fixable bugs
- ✅ Individual team member resistance

---

## Migration Success Metrics

Track these metrics to measure success:

### Quantitative

```bash
# Issue creation rate
gh issue list --json createdAt --jq 'group_by(.createdAt[:10]) | length'

# PR linkage rate
gh pr list --json body --jq '[.[] | select(.body | contains("#"))] | length'

# Workflow success rate
gh run list --json conclusion --jq '[.[] | select(.conclusion=="success")] | length'

# Time to close issues
# (Measure before and after)
```

### Qualitative

- **Team Satisfaction** - Survey before/after
- **Process Clarity** - Can team explain IDD workflow?
- **Documentation Quality** - Is it being updated?
- **Adoption Rate** - % of team using IDD correctly

### Example Survey

```markdown
## IDD Adoption Survey

1. How often do you use IDD workflows?
   - [ ] Daily
   - [ ] Weekly
   - [ ] Rarely
   - [ ] Never

2. Rate your understanding of IDD (1-5):
   - [ ] 1 - Don't understand
   - [ ] 5 - Fully understand

3. What's working well?
   [Open text]

4. What needs improvement?
   [Open text]

5. Would you recommend IDD to other teams?
   - [ ] Yes
   - [ ] No
   - [ ] Not sure
```

---

## Migration Timeline Example

### Real-World Timeline (Medium Team, 10 developers)

**Week 1: Planning**
- Day 1-2: Assess current system, export data
- Day 3-4: Set up IDD in test repository
- Day 5: Train admin team

**Week 2: Pilot**
- Day 1: Select pilot team (2-3 people)
- Day 2: Train pilot team
- Day 3-5: Pilot team uses IDD
- End of week: Review and adjust

**Week 3: Gradual Rollout**
- Day 1-2: Team A adopts IDD
- Day 3-4: Team B adopts IDD
- Day 5: All teams using IDD

**Week 4: Complete Migration**
- Day 1-2: Migrate remaining issues
- Day 3: Archive old system
- Day 4-5: Optimization and documentation

**Result:** Full IDD adoption in 4 weeks with minimal disruption

---

## Support During Migration

### Designate Champions

- **IDD Champion:** Expert user, helps team
- **Technical Owner:** Maintains configuration
- **Training Lead:** Conducts sessions

### Office Hours

```markdown
## IDD Office Hours

When: Every Tuesday & Thursday, 2-3pm
Where: Zoom / Slack #idd-help
Who: [IDD Champions]

Come with:
- Questions
- Issues
- Feedback
- Ideas
```

### Quick Reference

Print and distribute:

```
┌─────────────────────────────────────┐
│     IDD Quick Reference Card        │
├─────────────────────────────────────┤
│ Create Issue: GitHub UI → Templates│
│ Link Commit: "feat: xyz (#123)"    │
│ Create PR: gh pr create            │
│ View TO-DO: cat TO-DO.md           │
│                                     │
│ Help: #idd-help Slack channel      │
└─────────────────────────────────────┘
```

---

## Conclusion

Migrating to IDD is an investment in better development workflows. Take it step-by-step, communicate clearly, and support your team through the transition.

**Key Takeaways:**
- ✅ Choose the right migration strategy
- ✅ Preserve important history
- ✅ Train your team thoroughly
- ✅ Have a rollback plan
- ✅ Measure success
- ✅ Iterate and improve

**Need migration help? Open an issue with the "migration" label!**
