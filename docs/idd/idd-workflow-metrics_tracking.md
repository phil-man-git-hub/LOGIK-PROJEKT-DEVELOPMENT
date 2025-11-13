# IDD Metrics Tracking

Framework for measuring and tracking Issue-Driven Development success.

## Table of Contents

- [Key Performance Indicators](#key-performance-indicators)
- [Metrics Collection](#metrics-collection)
- [Dashboard Examples](#dashboard-examples)
- [ROI Calculation](#roi-calculation)
- [Reporting](#reporting)
- [Continuous Improvement](#continuous-improvement)

---

## Key Performance Indicators

### Adoption Metrics

**Team Adoption Rate**
```
Formula: (Users actively using IDD / Total team members) × 100

Target: 100% within 4 weeks
Measure: Weekly

Good: > 90%
Fair: 70-90%
Poor: < 70%
```

**Issue Template Usage**
```
Formula: (Issues with templates / Total issues) × 100

Target: 95%
Measure: Weekly

Good: > 90%
Fair: 75-90%
Poor: < 75%
```

**Commit Convention Adherence**
```
Formula: (Commits with issue refs / Total commits) × 100

Target: 90%
Measure: Weekly

Good: > 85%
Fair: 70-85%
Poor: < 70%
```

### Efficiency Metrics

**Issue Response Time**
```
Formula: Average time from issue creation to first response

Target: < 30 minutes
Measure: Daily

Excellent: < 15 min
Good: 15-30 min
Fair: 30-60 min
Poor: > 60 min
```

**Issue Resolution Time**
```
Formula: Average time from issue creation to closure

Target: < 7 days
Measure: Weekly

Excellent: < 3 days
Good: 3-7 days
Fair: 7-14 days
Poor: > 14 days
```

**Stale Issue Count**
```
Formula: Count of issues inactive > stale threshold

Target: < 10
Measure: Daily

Excellent: 0-5
Good: 5-10
Fair: 10-20
Poor: > 20
```

**Manual Tracking Time**
```
Formula: Hours spent manually updating tracking docs per week

Target: 0 hours
Measure: Weekly (self-reported)

Excellent: 0 hours
Good: < 30 min
Fair: 30-60 min
Poor: > 1 hour
```

### Quality Metrics

**Issue Quality Score**
```
Formula: Weighted score based on:
- Has description (25%)
- Has labels (25%)
- Has assignee (25%)
- Has acceptance criteria (25%)

Target: > 80%
Measure: Weekly

Excellent: > 90%
Good: 80-90%
Fair: 70-80%
Poor: < 70%
```

**PR Quality Score**
```
Formula: Weighted score based on:
- Follows title convention (30%)
- References issue (30%)
- Has description (20%)
- Passes CI (20%)

Target: > 85%
Measure: Weekly

Excellent: > 90%
Good: 85-90%
Fair: 75-85%
Poor: < 75%
```

**Documentation Freshness**
```
Formula: Days since last auto-update of docs

Target: < 7 days
Measure: Weekly

Excellent: < 3 days
Good: 3-7 days
Fair: 7-14 days
Poor: > 14 days
```

---

## Metrics Collection

### Manual Collection

**Weekly Team Survey:**
```markdown
IDD Weekly Check-in

1. How many hours did you spend on manual tracking this week?
   □ 0 (automated)
   □ < 30 min
   □ 30-60 min
   □ > 1 hour

2. Are you using issue templates for new issues?
   □ Always
   □ Usually
   □ Sometimes
   □ Never

3. What's blocking you from using IDD more?
   [Free text]

4. What's working well?
   [Free text]
```

### Automated Collection

**GitHub CLI Scripts:**

```bash
#!/bin/bash
# metrics-collect.sh - Collect IDD metrics

REPO="owner/repo"
SINCE="1 week ago"

echo "=== IDD Metrics Report ==="
echo "Repository: $REPO"
echo "Period: Last 7 days"
echo ""

# Issue metrics
echo "## Issues"
TOTAL_ISSUES=$(gh issue list --repo "$REPO" --json number --jq 'length')
TEMPLATE_ISSUES=$(gh issue list --repo "$REPO" --json body --jq '[.[] | select(.body | contains("## Description"))] | length')
TEMPLATE_RATE=$((TEMPLATE_ISSUES * 100 / TOTAL_ISSUES))

echo "Total issues: $TOTAL_ISSUES"
echo "With templates: $TEMPLATE_ISSUES ($TEMPLATE_RATE%)"
echo ""

# Commit metrics
echo "## Commits"
TOTAL_COMMITS=$(git log --since="$SINCE" --oneline | wc -l)
ISSUE_COMMITS=$(git log --since="$SINCE" --oneline | grep -c "#[0-9]")
COMMIT_RATE=$((ISSUE_COMMITS * 100 / TOTAL_COMMITS))

echo "Total commits: $TOTAL_COMMITS"
echo "With issue refs: $ISSUE_COMMITS ($COMMIT_RATE%)"
echo ""

# PR metrics
echo "## Pull Requests"
TOTAL_PRS=$(gh pr list --repo "$REPO" --state merged --json number --jq 'length')
CONV_PRS=$(gh pr list --repo "$REPO" --state merged --json title --jq '[.[] | select(.title | test("^(feat|fix|docs|refactor)"))] | length')
PR_RATE=$((CONV_PRS * 100 / TOTAL_PRS))

echo "Total merged PRs: $TOTAL_PRS"
echo "Following convention: $CONV_PRS ($PR_RATE%)"
echo ""

# Stale issues
echo "## Stale Issues"
STALE_COUNT=$(gh issue list --repo "$REPO" --label "stale" --json number --jq 'length')
echo "Stale issues: $STALE_COUNT"
```

**Python Metrics Script:**

```python
#!/usr/bin/env python3
"""
metrics-tracker.py - Track IDD metrics over time
"""

import json
import os
from datetime import datetime, timedelta
from github import Github

def collect_metrics(repo_name: str) -> dict:
    """Collect current metrics."""
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo(repo_name)
    
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    
    # Issue metrics
    issues = list(repo.get_issues(state='all', since=week_ago))
    template_issues = [i for i in issues if '## Description' in (i.body or '')]
    
    # PR metrics
    pulls = list(repo.get_pulls(state='closed'))
    recent_pulls = [p for p in pulls if p.merged_at and p.merged_at > week_ago]
    
    # Response time (first comment on issue)
    response_times = []
    for issue in issues[:10]:  # Sample recent 10
        comments = list(issue.get_comments())
        if comments:
            response_time = (comments[0].created_at - issue.created_at).total_seconds() / 60
            response_times.append(response_time)
    
    avg_response = sum(response_times) / len(response_times) if response_times else 0
    
    return {
        'timestamp': now.isoformat(),
        'issues': {
            'total': len(issues),
            'with_templates': len(template_issues),
            'template_rate': len(template_issues) / len(issues) * 100 if issues else 0,
        },
        'prs': {
            'total_merged': len(recent_pulls),
        },
        'response_time_minutes': avg_response,
        'stale_count': len([i for i in issues if 'stale' in [l.name for l in i.labels]]),
    }

def save_metrics(metrics: dict, output_file: str = 'metrics-history.json'):
    """Append metrics to history file."""
    history = []
    if os.path.exists(output_file):
        with open(output_file) as f:
            history = json.load(f)
    
    history.append(metrics)
    
    with open(output_file, 'w') as f:
        json.dump(history, f, indent=2)

def main():
    repo = os.environ.get('GITHUB_REPOSITORY', 'owner/repo')
    metrics = collect_metrics(repo)
    save_metrics(metrics)
    
    print(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    main()
```

**Workflow Integration:**

```yaml
# .github/workflows/metrics-tracking.yml
name: Track IDD Metrics

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:

jobs:
  track-metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: pip install PyGithub
      
      - name: Collect metrics
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
        run: |
          python3 bin/metrics-tracker.py
      
      - name: Commit metrics
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add metrics-history.json
          git commit -m "chore: update metrics history" || exit 0
          git push
```

---

## Dashboard Examples

### Simple Text Dashboard

```bash
#!/bin/bash
# dashboard.sh - Display IDD metrics dashboard

cat << 'EOF'
┌─────────────────────────────────────────────────────────────────┐
│                    IDD Metrics Dashboard                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📊 ADOPTION METRICS                                            │
│  ├─ Team Adoption Rate:        95%  ████████████████░░░  ✅     │
│  ├─ Issue Template Usage:      88%  █████████████░░░░░░  ✅     │
│  └─ Commit Convention:         92%  ██████████████░░░░░  ✅     │
│                                                                  │
│  ⚡ EFFICIENCY METRICS                                          │
│  ├─ Avg Response Time:        18 min  ████████████████  ✅     │
│  ├─ Avg Resolution Time:      4 days  ██████████████░░  ✅     │
│  ├─ Stale Issue Count:        7       ████████████░░░░  ✅     │
│  └─ Manual Tracking:          0 hrs   ████████████████  ✅     │
│                                                                  │
│  📈 QUALITY METRICS                                             │
│  ├─ Issue Quality Score:      85%  █████████████░░░░░░  ✅     │
│  ├─ PR Quality Score:         91%  ██████████████░░░░░  ✅     │
│  └─ Doc Freshness:            2 days  ████████████████  ✅     │
│                                                                  │
│  📅 TREND: ↗️ All metrics improving week-over-week              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
EOF
```

### Markdown Dashboard

````markdown
# IDD Metrics Dashboard

**Last Updated:** 2024-11-05 09:00 UTC  
**Period:** Last 7 days

## 📊 Key Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Team Adoption | 95% | 100% | 🟢 |
| Issue Templates | 88% | 95% | 🟡 |
| Commit Convention | 92% | 90% | 🟢 |
| Response Time | 18 min | < 30 min | 🟢 |
| Stale Issues | 7 | < 10 | 🟢 |
| Manual Tracking | 0 hrs | 0 hrs | 🟢 |

## 📈 Trends

```
Week 1:  ████░░░░░░ 40%
Week 2:  ██████░░░░ 60%
Week 3:  ████████░░ 80%
Week 4:  ██████████ 100% ← Current
```

## 🎯 Goals for Next Week

- [ ] Increase template usage to 95%
- [ ] Reduce stale issues to < 5
- [ ] Maintain 100% team adoption

## 📊 Detailed Breakdown

### Issues Created: 23
- With templates: 20 (87%)
- Properly labeled: 21 (91%)
- With assignees: 19 (83%)

### Commits: 156
- With issue references: 144 (92%)
- Following convention: 140 (90%)

### Pull Requests: 18
- Following convention: 17 (94%)
- Referencing issues: 16 (89%)
- Merged within 24h: 14 (78%)
````

### JSON Dashboard (for tools)

```json
{
  "dashboard": {
    "generated_at": "2024-11-05T09:00:00Z",
    "period": "last_7_days",
    "metrics": {
      "adoption": {
        "team_adoption_rate": {
          "value": 95,
          "target": 100,
          "unit": "percent",
          "status": "good",
          "trend": "up"
        },
        "issue_template_usage": {
          "value": 88,
          "target": 95,
          "unit": "percent",
          "status": "fair",
          "trend": "up"
        },
        "commit_convention": {
          "value": 92,
          "target": 90,
          "unit": "percent",
          "status": "excellent",
          "trend": "stable"
        }
      },
      "efficiency": {
        "response_time": {
          "value": 18,
          "target": 30,
          "unit": "minutes",
          "status": "excellent",
          "trend": "down"
        },
        "stale_issues": {
          "value": 7,
          "target": 10,
          "unit": "count",
          "status": "good",
          "trend": "down"
        }
      },
      "quality": {
        "issue_quality": {
          "value": 85,
          "target": 80,
          "unit": "percent",
          "status": "good",
          "trend": "up"
        }
      }
    },
    "summary": {
      "total_metrics": 6,
      "excellent": 2,
      "good": 3,
      "fair": 1,
      "poor": 0,
      "overall_status": "good"
    }
  }
}
```

---

## ROI Calculation

### Time Savings Calculator

```python
#!/usr/bin/env python3
"""Calculate IDD ROI"""

def calculate_roi(team_size: int, hourly_rate: float = 50.0):
    """Calculate ROI for IDD adoption."""
    
    # Time spent before IDD (hours/week per person)
    before = {
        'issue_triage': 1.0,
        'todo_updates': 1.0,
        'documentation': 0.5,
        'stale_cleanup': 0.5,
    }
    total_before = sum(before.values())
    
    # Time spent after IDD (hours/week per person)
    after = {
        'issue_triage': 0.17,  # 10 min
        'todo_updates': 0,     # automated
        'documentation': 0,    # automated
        'stale_cleanup': 0,    # automated
    }
    total_after = sum(after.values())
    
    # Savings
    hours_saved_per_person_week = total_before - total_after
    hours_saved_team_week = hours_saved_per_person_week * team_size
    hours_saved_year = hours_saved_team_week * 52
    
    # Cost savings
    cost_saved_week = hours_saved_team_week * hourly_rate
    cost_saved_year = hours_saved_year * hourly_rate
    
    # Setup cost (one-time)
    setup_hours = 2
    setup_cost = setup_hours * hourly_rate
    
    # ROI
    roi_percent = (cost_saved_year - setup_cost) / setup_cost * 100
    
    print(f"=== IDD ROI Calculation ===")
    print(f"Team size: {team_size} people")
    print(f"Hourly rate: ${hourly_rate}")
    print()
    print(f"Time saved:")
    print(f"  Per person: {hours_saved_per_person_week:.1f} hrs/week")
    print(f"  Team total: {hours_saved_team_week:.1f} hrs/week")
    print(f"  Annual: {hours_saved_year:.0f} hrs/year")
    print()
    print(f"Cost savings:")
    print(f"  Per week: ${cost_saved_week:,.0f}")
    print(f"  Per year: ${cost_saved_year:,.0f}")
    print()
    print(f"Investment:")
    print(f"  Setup cost: ${setup_cost:.0f}")
    print(f"  ROI: {roi_percent:,.0f}%")
    print()
    print(f"Break-even: {setup_hours / hours_saved_team_week:.1f} weeks")

if __name__ == '__main__':
    calculate_roi(team_size=10, hourly_rate=50)
```

**Example Output:**
```
=== IDD ROI Calculation ===
Team size: 10 people
Hourly rate: $50

Time saved:
  Per person: 2.8 hrs/week
  Team total: 28.3 hrs/week
  Annual: 1,472 hrs/year

Cost savings:
  Per week: $1,417
  Per year: $73,650

Investment:
  Setup cost: $100
  ROI: 73,550%

Break-even: 0.1 weeks
```

---

## Reporting

### Weekly Report Template

```markdown
# IDD Weekly Report

**Week of:** November 4-10, 2024  
**Reporter:** @username

## 📊 Metrics Summary

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Team Adoption | 95% | 90% | +5% 🟢 |
| Issue Templates | 88% | 85% | +3% 🟢 |
| Response Time | 18 min | 22 min | -4 min 🟢 |
| Stale Issues | 7 | 10 | -3 🟢 |

## 🎉 Wins This Week

- Increased team adoption to 95%
- Response time improved by 18%
- Closed 15 stale issues
- All PRs followed convention

## 🚧 Challenges

- Still have 2 team members not using templates consistently
- Need to improve issue labeling (only 85%)

## 📝 Action Items

- [ ] Training session for template usage
- [ ] Create label guide for team
- [ ] Review stale threshold settings

## 💬 Team Feedback

> "Love how I don't have to update TO-DO anymore!" - @developer1
> "Need better examples for issue templates" - @developer2

## 📈 Next Week Goals

- Reach 100% team adoption
- Increase template usage to 95%
- Reduce stale issues to < 5
```

### Monthly Report Template

```markdown
# IDD Monthly Report - November 2024

## Executive Summary

Issue-Driven Development achieved 95% team adoption in month 1, saving the team approximately 113 hours of manual tracking time.

## Key Achievements

✅ 95% team adoption (target: 75%)
✅ Zero hours manual tracking (target: 0)
✅ 18min response time (target: < 30min)
✅ Full automation operational

## Metrics Trends

[Include chart showing 4-week trend]

## ROI

**Time Saved:** 113 hours  
**Cost Saved:** $5,650 (at $50/hr)  
**Setup Investment:** $100  
**ROI:** 5,550%

## Challenges Overcome

1. Initial resistance to change
   - Solution: Started with volunteers
   - Result: Positive experience led to full adoption

2. Configuration confusion
   - Solution: Provided team-specific examples
   - Result: Smooth customization

## Team Feedback

Positive: 90%
Neutral: 10%
Negative: 0%

Top feedback:
- "Saves so much time"
- "Love the automation"
- "Wish we did this sooner"

## Next Month Goals

- Maintain 100% adoption
- Add custom workflows
- Integrate with team tools
- Share success story publicly
```

---

## Continuous Improvement

### Monthly Review Process

**1. Collect Data** (Week 4 of month)
```bash
# Generate metrics
python3 bin/metrics-tracker.py

# Export to CSV
python3 bin/metrics-export.py --format csv
```

**2. Team Survey** (Week 4 of month)
```markdown
IDD Monthly Survey

1. How satisfied are you with IDD? (1-5)
2. What's working well?
3. What needs improvement?
4. What features would you like?
5. Time saved this month (estimate)?
```

**3. Analysis** (First week of next month)
- Review metrics trends
- Identify bottlenecks
- Celebrate wins
- Plan improvements

**4. Action Planning**
- Prioritize improvements
- Assign owners
- Set deadlines
- Update configuration

### A/B Testing

Test different configurations:

```yaml
# Test A: Aggressive stale management
stale_management:
  days_until_stale: 14
  days_until_close: 7

# Test B: Lenient stale management
stale_management:
  days_until_stale: 30
  days_until_close: 14
```

Measure:
- Issue closure rate
- False positive stale markings
- Team satisfaction

### Experimentation Framework

```python
def run_experiment(name: str, config_a: dict, config_b: dict, duration_days: int = 14):
    """
    Run A/B test on configuration.
    
    Args:
        name: Experiment name
        config_a: Control configuration
        config_b: Experimental configuration
        duration_days: How long to run test
    """
    # Split team into groups
    # Apply configs
    # Collect metrics
    # Compare results
    # Report findings
    pass
```

---

## Quick Reference

```
┌────────────────────────────────────────────────┐
│          IDD Metrics Tracking Card             │
├────────────────────────────────────────────────┤
│ Daily:                                         │
│  • Check stale count                           │
│  • Monitor response time                       │
│                                                 │
│ Weekly:                                        │
│  • Run metrics script                          │
│  • Review dashboard                            │
│  • Generate weekly report                      │
│  • Team check-in                               │
│                                                 │
│ Monthly:                                       │
│  • Full metrics analysis                       │
│  • Team survey                                 │
│  • Calculate ROI                               │
│  • Plan improvements                           │
│                                                 │
│ Quarterly:                                     │
│  • Executive report                            │
│  • Trend analysis                              │
│  • Strategic adjustments                       │
└────────────────────────────────────────────────┘
```

---

**Track, measure, and improve continuously! 📈**
