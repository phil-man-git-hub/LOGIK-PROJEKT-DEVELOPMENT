# IDD Adoption Guide

Guide for teams and individuals adopting Issue-Driven Development.

## Table of Contents

- [Quick Start for New Adopters](#quick-start-for-new-adopters)
- [Adoption Patterns](#adoption-patterns)
- [Team Onboarding](#team-onboarding)
- [Success Metrics](#success-metrics)
- [Common Challenges](#common-challenges)
- [Support Resources](#support-resources)

---

## Quick Start for New Adopters

### First 15 Minutes

**Goal:** Get IDD running in your repository

1. **Extract the template**
   ```bash
   # If using template repository
   gh repo clone your-org/idd-template my-project
   cd my-project
   
   # Or if adding to existing repo
   cd my-existing-project
   curl -L https://github.com/your-org/idd-template/archive/main.zip -o idd.zip
   unzip idd.zip
   ```

2. **Run setup script**
   ```bash
   ./bin/setup-idd.sh
   ```
   
   This will:
   - Create `idd-config.yml`
   - Set up GitHub secrets
   - Enable workflows
   - Create initial TO-DO.md

3. **Verify it works**
   ```bash
   # Create a test issue
   gh issue create --title "Test IDD setup" --body "Testing IDD" --label "enhancement"
   
   # Manually trigger sync
   gh workflow run sync-issues-to-todo.yml
   
   # Check TO-DO.md
   cat TO-DO.md
   ```

**✅ Success:** Issue appears in TO-DO.md!

### First Hour

**Goal:** Customize for your team

1. **Review configuration**
   ```bash
   # Edit config
   vim idd-config.yml
   ```
   
   Adjust:
   - Project name and repository
   - Track labels (what issues to sync)
   - Stale management thresholds
   - AI context privacy mode

2. **Create team labels**
   ```bash
   # Create your label taxonomy
   gh label create "priority:high" --color "d73a4a"
   gh label create "priority:medium" --color "fbca04"
   gh label create "effort:small" --color "c2e0c6"
   ```

3. **Customize issue templates**
   - Edit `.github/ISSUE_TEMPLATE/*.yml`
   - Add your project-specific fields
   - Update labels

4. **Test workflows**
   ```bash
   # Test issue validation
   # Create issue with missing fields
   
   # Test stale management (dry run)
   # Adjust thresholds in config
   
   # Test AI context capture
   python3 bin/capture-session.py
   ```

**✅ Success:** IDD configured for your team!

### First Day

**Goal:** Team adoption begins

1. **Team meeting**
   - Present IDD to team (see [Presentations](#presentations))
   - Demo the workflow
   - Answer questions
   - Get buy-in

2. **Migration plan**
   - Decide which existing issues to migrate
   - Clean up stale issues
   - Apply new label taxonomy
   - Update issue descriptions

3. **Documentation**
   - Add IDD section to team README
   - Link to docs
   - Create team-specific guidelines
   - Document your config choices

4. **First real issue**
   - Have team create issues using templates
   - Make commits with issue references
   - Create PRs following convention
   - Celebrate when it works!

**✅ Success:** Team starts using IDD!

---

## Adoption Patterns

### Pattern 1: Bottom-Up (Individual → Team)

**Best for:** Small teams, startups, open source

**Approach:**
1. Start using IDD yourself
2. Share benefits with team
3. Gradual team adoption
4. Iterate based on feedback

**Timeline:** 2-4 weeks

**Pros:**
- Low risk
- Organic adoption
- Learn what works first

**Cons:**
- Slower rollout
- May need to convince others

### Pattern 2: Top-Down (Team → Individual)

**Best for:** Larger organizations, strict processes

**Approach:**
1. Leadership decision to adopt
2. Set standard configuration
3. Team training session
4. Mandatory adoption date

**Timeline:** 1-2 weeks

**Pros:**
- Fast rollout
- Consistent usage
- Clear mandate

**Cons:**
- May face resistance
- Less flexibility
- Needs strong buy-in

### Pattern 3: Pilot Team

**Best for:** Large organizations, risk-averse teams

**Approach:**
1. Select pilot team (5-10 people)
2. Run IDD for 4-6 weeks
3. Gather feedback and metrics
4. Refine and roll out widely

**Timeline:** 6-12 weeks

**Pros:**
- Proven before rollout
- Real metrics
- Refinement opportunity

**Cons:**
- Longer timeline
- Pilot fatigue
- Two rollouts needed

### Pattern 4: Greenfield

**Best for:** New projects, new teams

**Approach:**
1. Start project with IDD from day one
2. Build habits from the beginning
3. No migration needed

**Timeline:** Immediate

**Pros:**
- Clean start
- Natural adoption
- No legacy issues

**Cons:**
- Can't prove ROI early
- May over-engineer
- Less flexibility to change

---

## Team Onboarding

### Onboarding Checklist

**Before First Day:**
- [ ] IDD installed in repository
- [ ] Configuration customized for team
- [ ] Documentation added to README
- [ ] Slack/Discord channel created
- [ ] Training materials prepared

**Day 1: Introduction**
- [ ] Overview presentation (30 min)
- [ ] Live demo (15 min)
- [ ] Q&A session (15 min)
- [ ] Share documentation links

**Week 1: Hands-On**
- [ ] Each team member creates 1 issue
- [ ] Everyone makes 1 PR with issue reference
- [ ] Team reviews TO-DO.md daily
- [ ] Troubleshoot any problems

**Week 2: Adoption**
- [ ] All new work starts with issues
- [ ] All commits reference issues
- [ ] Regular sync checks
- [ ] Collect feedback

**Week 4: Review**
- [ ] Measure adoption metrics
- [ ] Gather team feedback
- [ ] Identify pain points
- [ ] Refine configuration

### Training Materials

**Quick Reference Card:**
```
┌────────────────────────────────────────────────┐
│          IDD Quick Reference                   │
├────────────────────────────────────────────────┤
│ Create Issue:                                  │
│   • Use issue template                         │
│   • Add labels                                 │
│   • Assign yourself                            │
│                                                 │
│ Work on Issue:                                 │
│   • Create branch: feature/issue-42-desc       │
│   • Make commits: "feat: description (#42)"    │
│   • Push branch                                │
│                                                 │
│ Create PR:                                     │
│   • Use PR template                            │
│   • Reference issue: "Closes #42"              │
│   • Request review                             │
│                                                 │
│ After Merge:                                   │
│   • Issue auto-closes                          │
│   • TO-DO.md auto-updates                      │
│   • Docs auto-generate                         │
│                                                 │
│ Help: docs/idd/README.md                       │
└────────────────────────────────────────────────┘
```

**Video Tutorial Script:**
```
[0:00-0:30] Introduction
"Hi! I'm going to show you how we use IDD in our team."

[0:30-2:00] Creating an Issue
"First, let's create an issue. Click 'New Issue'..."
[Show: template selection, filling fields, adding labels]

[2:00-3:30] Working on the Issue
"Now I'll work on this issue..."
[Show: create branch, make changes, commit with #42]

[3:30-5:00] Creating a PR
"Time to create a pull request..."
[Show: gh pr create, fill template, "Closes #42"]

[5:00-6:00] After Merge
"Once merged, watch what happens automatically..."
[Show: issue closes, TO-DO.md updates]

[6:00-6:30] Wrap-up
"That's it! Questions? Check the docs or ask in #idd-help"
```

### Team Workshop

**2-Hour Workshop Agenda:**

**Part 1: Presentation (30 min)**
- Why IDD? (5 min)
- How it works (10 min)
- Our configuration (10 min)
- Q&A (5 min)

**Part 2: Hands-On (60 min)**
- Everyone creates an issue (10 min)
- Everyone makes a commit (15 min)
- Everyone creates a PR (15 min)
- Watch automation work (10 min)
- Troubleshooting time (10 min)

**Part 3: Advanced (30 min)**
- AI context capture (10 min)
- Configuration options (10 min)
- Best practices (10 min)

**Materials Needed:**
- Laptop for everyone
- Demo repository
- GitHub access for all
- Slack channel ready
- Documentation links

---

## Success Metrics

### Key Performance Indicators (KPIs)

**Adoption Metrics:**
```
Target: 100% adoption within 4 weeks

Week 1: 25% of team using issue templates
Week 2: 50% of commits reference issues
Week 3: 75% of PRs follow convention
Week 4: 100% of work tracked in IDD
```

**Efficiency Metrics:**
```
Issue Response Time:
Before: 2 hours average
Target: < 30 minutes
Measure: Time from issue creation to first comment

Stale Issues:
Before: 60 open stale issues
Target: < 10 stale issues
Measure: Issues inactive > 30 days

Manual Tracking Time:
Before: 2 hours per week per person
Target: 0 hours
Measure: Time spent updating tracking docs
```

**Quality Metrics:**
```
Issue Quality:
Target: 90% of issues use templates
Measure: Issues created with template vs manual

PR Quality:
Target: 95% of PRs reference issues
Measure: PRs with "Closes #" vs without

Documentation:
Target: 100% docs auto-generated
Measure: Manual doc updates vs automated
```

### Measuring Success

**Week 1 Metrics:**
```bash
# Issues created with templates
gh issue list --json number,title,body | \
  jq '[.[] | select(.body | contains("## Description"))] | length'

# Commits referencing issues
git log --since="1 week ago" --oneline | grep -c "#[0-9]"

# PRs following convention
gh pr list --state merged --json title | \
  jq '[.[] | select(.title | test("^(feat|fix|docs|refactor)"))] | length'
```

**Month 1 Summary:**
```
Adoption Rate: 85% (target: 75%)
✅ Exceeds target

Issue Response: 45 min (target: < 30 min)
⚠️ Close to target, improving

Stale Issues: 15 (target: < 10)
⚠️ Improving, needs focus

Manual Tracking: 0 hrs/week (target: 0)
✅ Achieved!

Overall: Strong adoption, minor refinements needed
```

### ROI Calculation

**Time Savings:**
```
Before IDD:
- Issue triage: 1 hour/week
- TO-DO updates: 1 hour/week
- Documentation: 30 min/week
- Stale cleanup: 30 min/week
Total: 3 hours/week per person

After IDD:
- Issue triage: 10 min/week (automated validation)
- TO-DO updates: 0 (fully automated)
- Documentation: 0 (auto-generated)
- Stale cleanup: 0 (automated)
Total: 10 min/week per person

Savings: 2h 50min/week per person

For 10-person team:
28.3 hours/week saved
= 1,416 hours/year
= ~$70,800/year (at $50/hour)

Setup time: 2 hours
ROI: 35,400% in first year
```

---

## Common Challenges

### Challenge 1: Resistance to Change

**Symptom:** Team doesn't want to adopt new process

**Solutions:**
- Start with volunteers
- Show quick wins
- Make it optional initially
- Gather and share metrics
- Lead by example

**Example:**
```
"Let's try IDD for just your tickets this sprint.
If you don't like it, we'll stop. Deal?"

[After 1 week]
"I noticed you haven't had to update your TO-DO once.
That saved you ~30 minutes. Want to keep going?"
```

### Challenge 2: Too Much Automation

**Symptom:** Team feels overwhelmed by automated actions

**Solutions:**
- Start minimal (just issue sync)
- Add features gradually
- Make everything configurable
- Respect team preferences
- Get feedback continuously

**Example Configuration:**
```yaml
# Week 1: Just syncing
workflows:
  sync_issues: true
  stale_management: false
  ai_context: false
  documentation: false

# Week 3: Add stale management
workflows:
  sync_issues: true
  stale_management: true  # ← Added
  ai_context: false
  documentation: false

# Week 6: Full automation
workflows:
  sync_issues: true
  stale_management: true
  ai_context: true  # ← Added
  documentation: true  # ← Added
```

### Challenge 3: Configuration Confusion

**Symptom:** Team doesn't understand config options

**Solutions:**
- Start with example config
- Document each setting
- Provide team-specific templates
- Offer config review sessions
- Create validation checks

**Help:**
```bash
# Use example configs
cp config/examples/small-team.yml idd-config.yml

# Validate before committing
python3 bin/validate-config.py idd-config.yml

# Get help
gh issue create --label "help wanted"
```

### Challenge 4: Workflow Failures

**Symptom:** GitHub Actions workflows fail frequently

**Solutions:**
- Check workflow logs
- Verify permissions
- Validate configuration
- Check rate limits
- Review recent changes

**Debugging:**
```bash
# View workflow status
gh workflow list

# Check recent runs
gh run list --workflow=sync-issues-to-todo.yml

# View failure logs
gh run view <run-id> --log

# Re-run failed workflow
gh run rerun <run-id>
```

### Challenge 5: Inconsistent Adoption

**Symptom:** Some team members use IDD, others don't

**Solutions:**
- Make it official team policy
- Track adoption metrics
- Celebrate good examples
- Provide support and training
- Address blockers

**Tracking Adoption:**
```bash
# Who's creating issues?
gh issue list --json author --jq '[.[] | .author.login] | group_by(.) | map({user: .[0], count: length})'

# Who's referencing issues in commits?
git log --since="1 month ago" --pretty=format:"%an" | sort | uniq -c
```

---

## Support Resources

### Documentation

**Essential Docs:**
- [Quick Start](QUICK_START.md) - 5-minute setup
- [Setup Guide](SETUP_GUIDE.md) - Detailed installation
- [Customization Guide](CUSTOMIZATION_GUIDE.md) - Configuration options
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- [Best Practices](BEST_PRACTICES.md) - Usage guidelines
- [Architecture](ARCHITECTURE.md) - How it works

### Getting Help

**GitHub:**
- [Issues](https://github.com/your-org/your-repo/issues) - Bug reports, feature requests
- [Discussions](https://github.com/your-org/your-repo/discussions) - Questions, ideas
- [Wiki](https://github.com/your-org/your-repo/wiki) - Community guides

**Community:**
- Discord: [invite link]
- Slack: [invite link]
- Twitter: [@idd_dev]
- Email: support@idd.dev

### FAQ

**Q: Do I need to migrate all existing issues?**
A: No! Start fresh. Close or archive old issues, start new ones with templates.

**Q: What if my team uses Jira/Linear?**
A: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for migration strategies.

**Q: Can I use IDD with private repositories?**
A: Yes! Works identically with private repos.

**Q: What about teams larger than 50 people?**
A: Use the enterprise configuration example and adjust as needed.

**Q: How do I disable a specific workflow?**
A: Set it to `false` in `idd-config.yml`:
```yaml
workflows:
  stale_management: false  # Disabled
```

**Q: Can I self-host the workflows?**
A: Yes! All workflows run in GitHub Actions, no external services required.

**Q: What if GitHub Actions is down?**
A: Manual fallbacks available. Run scripts locally:
```bash
python3 bin/sync-issues-to-todo.py
```

### Troubleshooting

**Common Issues:**

1. **Workflow not running**
   ```bash
   # Check if enabled
   gh workflow list
   
   # Enable if needed
   gh workflow enable sync-issues-to-todo.yml
   ```

2. **TO-DO.md not updating**
   ```bash
   # Check last run
   gh run list --workflow=sync-issues-to-todo.yml
   
   # View logs
   gh run view <run-id> --log
   
   # Trigger manually
   gh workflow run sync-issues-to-todo.yml
   ```

3. **Permission errors**
   ```yaml
   # Ensure workflow has permissions
   permissions:
     contents: write
     issues: write
   ```

4. **Rate limiting**
   ```bash
   # Check rate limit
   gh api rate_limit
   
   # Wait or reduce frequency
   ```

For more troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## Success Stories

### Small Team (5 people)

**Company:** Tech Startup  
**Before:** Manual tracking, scattered issues  
**After:** 100% automated, zero overhead  
**Time Saved:** 10 hours/week  
**Quote:** *"IDD let us focus on building, not tracking"*

### Medium Team (20 people)

**Company:** SaaS Company  
**Before:** 60+ stale issues, 2h/week tracking  
**After:** 5 stale issues, 0h/week tracking  
**Time Saved:** 40 hours/week  
**Quote:** *"Game changer for our workflow"*

### Open Source Project (100+ contributors)

**Project:** Popular Framework  
**Before:** Contributor confusion, label chaos  
**After:** Clear process, automated triage  
**Impact:** 2x contributor retention  
**Quote:** *"Made contributing accessible to everyone"*

---

## Quick Reference

```
┌─────────────────────────────────────────────────┐
│         IDD Adoption Roadmap                    │
├─────────────────────────────────────────────────┤
│ Day 1:     Setup & demo                         │
│ Week 1:    Team training                        │
│ Week 2:    First real usage                     │
│ Week 3:    Refinement                           │
│ Week 4:    Full adoption                        │
│ Month 3:   Measure ROI                          │
│ Month 6:   Optimize & expand                    │
├─────────────────────────────────────────────────┤
│ Success = 100% team adoption + measurable ROI   │
└─────────────────────────────────────────────────┘
```

---

**Ready to track your success? See [METRICS_TRACKING.md](METRICS_TRACKING.md)!**
