# Example Workflows: AI Context System

**Real-world usage patterns and workflows**

---

## 📖 Table of Contents

1. [Daily Development Workflow](#daily-development-workflow)
2. [Sprint Planning](#sprint-planning)
3. [Bug Investigation](#bug-investigation)
4. [Code Review](#code-review)
5. [Knowledge Transfer](#knowledge-transfer)
6. [AI Pair Programming](#ai-pair-programming)
7. [Documentation Writing](#documentation-writing)
8. [Onboarding New Team Members](#onboarding-new-team-members)

---

## 1. Daily Development Workflow

**Scenario:** You work on multiple issues throughout the day and want to maintain context.

### Morning Routine

```bash
# Capture yesterday's work
python bin/capture-session.py --date $(date -v-1d +%Y-%m-%d)

# Review what you worked on
python bin/search-context.py --date $(date -v-1d +%Y-%m-%d)

# Get context for today's work
python bin/retrieve-context.py --issue 23 --mode focused
```

### During Work

```bash
# Quick context check before switching tasks
python bin/search-context.py "monitoring setup" --date-range 7

# Get comprehensive view of current issue
python bin/retrieve-context.py --issue 23 --mode broad -o context.md
```

### End of Day

```bash
# Capture today's session
python bin/capture-session.py

# Review what was accomplished
python bin/search-context.py --date $(date +%Y-%m-%d)

# Update TO-DO with findings
cat .ai-context/memory/sessions/$(date +%Y-%m-%d).md
```

**Result:** Complete daily context preserved, easy resume tomorrow.

---

## 2. Sprint Planning

**Scenario:** Planning next sprint, need to review completed work and estimate new tasks.

### Review Last Sprint

```bash
# Get all work from last 14 days
python bin/search-context.py --date-range 14 --format json > sprint-review.json

# Find all features completed
python bin/search-context.py --type feat --date-range 14

# Find all bugs fixed
python bin/search-context.py --type fix --date-range 14
```

### Estimate New Work

```bash
# Get context on similar past work
python bin/search-context.py "AI context implementation"

# See detailed implementation
python bin/retrieve-context.py --topic "AI context" --mode comprehensive

# Compare to new requirements
```

### Generate Sprint Report

```bash
# Export comprehensive context
python bin/retrieve-context.py --days 14 --mode comprehensive -o sprint-report.md

# Share with team
cat sprint-report.md
```

**Result:** Data-driven sprint planning with historical context.

---

## 3. Bug Investigation

**Scenario:** Bug reported in monitoring system, need to find when/how feature was implemented.

### Step 1: Search for Related Work

```bash
# Search for monitoring work
python bin/search-context.py "monitoring" --date-range 30

# Example output:
# Found in 2025-10-15.md (3 matches, relevance: 89)
```

### Step 2: Get Detailed Context

```bash
# Get full context for that session
python bin/retrieve-context.py --date 2025-10-15 --mode comprehensive
```

### Step 3: Find Related Issues

```bash
# Search for issue number
python bin/search-context.py --issue 11

# Get all decisions made
cat .ai-context/decisions/quick-decisions.md | grep -A5 "monitoring"
```

### Step 4: Compare Current vs Original

```bash
# Get original implementation context
python bin/retrieve-context.py --topic "monitoring setup" --days 30 -o original.md

# Review changes
git log --grep="monitoring" --oneline
```

**Result:** Quick identification of when feature was added, what changed, why.

---

## 4. Code Review

**Scenario:** Reviewing PR #22, need full context to understand changes.

### Before Review

```bash
# Get context for the issue
python bin/retrieve-context.py --issue 21 --mode comprehensive -o pr-context.md

# Search for related work
python bin/search-context.py "context retrieval"

# Check recent decisions
cat .ai-context/decisions/quick-decisions.md
```

### During Review

```bash
# Open context file
code pr-context.md

# Check specific implementation decisions
python bin/search-context.py "scoring algorithm"

# Compare to similar code
python bin/search-context.py "session capture" --type feat
```

### After Review

```bash
# Capture review session
python bin/capture-session.py

# Add decision if needed
echo "## 2025-11-05: PR #22 Review Feedback" >> .ai-context/decisions/quick-decisions.md
```

**Result:** Informed code review with full historical context.

---

## 5. Knowledge Transfer

**Scenario:** Team member asks "How does the AI context system work?"

### Quick Overview

```bash
# Generate focused explanation
python bin/retrieve-context.py --topic "AI context system" --mode focused -o knowledge-transfer.md

# Share file
cat knowledge-transfer.md
```

### Detailed Walkthrough

```bash
# Get comprehensive context
python bin/retrieve-context.py --topic "AI context implementation" --mode comprehensive --days 30 -o detailed-guide.md

# Include all sessions
python bin/search-context.py --date-range 30 --format json > sessions.json
```

### Interactive Session

```bash
# Live demonstration
python bin/capture-session.py --help
python bin/search-context.py --help
python bin/retrieve-context.py --help

# Show real examples
python bin/search-context.py "IDD"
python bin/retrieve-context.py --issue 15 --mode focused
```

**Result:** Efficient knowledge transfer with concrete examples.

---

## 6. AI Pair Programming

**Scenario:** Working with AI assistant (ChatGPT, Claude, GitHub Copilot) on complex task.

### Setup Phase

```bash
# Get focused context for current task
python bin/retrieve-context.py --issue 23 --mode focused --max-tokens 4000 -o ai-context.md

# Verify token count
wc -w ai-context.md
```

### Share with AI

```markdown
I'm working on [task description]. Here's the context:

[Paste contents of ai-context.md]

Based on this context, help me with [specific question].
```

### During Work

```bash
# Get additional context as needed
python bin/search-context.py "specific topic" --date-range 7

# Update AI with new findings
python bin/retrieve-context.py --topic "new discovery" --mode focused -o update.md
```

### After Session

```bash
# Capture AI pair programming session
python bin/capture-session.py

# Document decisions made
echo "## 2025-11-05: AI Pair Programming - Issue #23" >> .ai-context/decisions/quick-decisions.md
echo "- Decided to use X approach because Y" >> .ai-context/decisions/quick-decisions.md
```

**Result:** AI assistant has full context, productive collaboration.

---

## 7. Documentation Writing

**Scenario:** Writing comprehensive documentation for Week 2 deliverables.

### Research Phase

```bash
# Get all Week 2 context
python bin/search-context.py --date-range 30 --format json > week2-data.json

# Get focused view per deliverable
python bin/retrieve-context.py --issue 15 --mode comprehensive -o issue-15-context.md
python bin/retrieve-context.py --issue 17 --mode comprehensive -o issue-17-context.md
python bin/retrieve-context.py --issue 19 --mode comprehensive -o issue-19-context.md
python bin/retrieve-context.py --issue 21 --mode comprehensive -o issue-21-context.md
```

### Writing Phase

```bash
# Reference context files while writing
code issue-*-context.md docs/idd/WEEK_2_COMPLETION_SUMMARY.md

# Search for specific details
python bin/search-context.py "line count"
python bin/search-context.py "testing results"
```

### Validation Phase

```bash
# Verify all facts
python bin/search-context.py "5582 lines"  # Confirm totals
python bin/search-context.py "100% success"  # Confirm test results

# Cross-reference
git log --oneline | grep -E "issue-(15|17|19|21)"
```

**Result:** Accurate, comprehensive documentation with verified facts.

---

## 8. Onboarding New Team Members

**Scenario:** New developer joining team, needs to understand project history.

### Week 1: Project Overview

```bash
# Generate project overview
python bin/retrieve-context.py --days 90 --mode comprehensive -o project-overview.md

# Create onboarding guide
cat project-overview.md > onboarding-guide.md
```

### Week 2: Deep Dive

```bash
# Show recent work
python bin/search-context.py --date-range 30

# Explain specific features
python bin/retrieve-context.py --topic "IDD workflow" --mode broad -o idd-guide.md
python bin/retrieve-context.py --topic "AI context system" --mode broad -o ai-context-guide.md
```

### Week 3: Hands-On

```bash
# New team member tries tools
python bin/capture-session.py
python bin/search-context.py "onboarding"
python bin/retrieve-context.py --topic "learning" --mode focused

# Review together
cat .ai-context/memory/sessions/$(date +%Y-%m-%d).md
```

### Week 4: Independence

```bash
# Team member uses tools independently
python bin/search-context.py "question about X"
python bin/retrieve-context.py --issue N --mode focused

# Captures own sessions
python bin/capture-session.py  # Daily habit established
```

**Result:** Smooth onboarding with self-service knowledge access.

---

## 🎯 Advanced Workflows

### Multi-Issue Context Assembly

**Scenario:** Working on feature that spans multiple issues.

```bash
# Get context for all related issues
for issue in 15 17 19 21; do
  python bin/retrieve-context.py --issue $issue --mode focused -o "context-$issue.md"
done

# Combine into single file
cat context-*.md > combined-context.md

# Review
code combined-context.md
```

### Time-Based Analysis

**Scenario:** Analyzing productivity patterns.

```bash
# Get last month's work
python bin/search-context.py --date-range 30 --format json > last-month.json

# Count by type
jq '[.[] | .matches[].metadata.commit_type] | group_by(.) | map({type: .[0], count: length})' last-month.json

# Analyze patterns
python -c "
import json
with open('last-month.json') as f:
    data = json.load(f)
    for session in data:
        print(f'{session[\"date\"]}: {len(session[\"matches\"])} matches')
"
```

### Context Export for Team

**Scenario:** Share context package with distributed team.

```bash
# Create export directory
mkdir -p exports/week2-context

# Export all relevant files
python bin/retrieve-context.py --days 7 --mode comprehensive -o exports/week2-context/overview.md
cp .ai-context/memory/sessions/*.md exports/week2-context/
cp .ai-context/decisions/*.md exports/week2-context/

# Create archive
tar -czf week2-context.tar.gz exports/week2-context/

# Share
# scp week2-context.tar.gz user@server:/path/
```

---

## 💡 Tips & Best Practices

### 1. Start Small
- Begin with daily capture only
- Add search as you need it
- Gradually incorporate retrieval

### 2. Be Consistent
- Capture daily at same time
- Use consistent search terms
- Maintain decision log

### 3. Optimize for Your Workflow
- Adjust token limits for your AI model
- Customize retention period
- Create aliases for common commands

### 4. Share Knowledge
- Export context for team members
- Document workflows that work
- Contribute improvements

### 5. Integrate with Tools
- Add VS Code tasks
- Create shell aliases
- Set up cron jobs

---

## 🔄 Feedback Loop

**Continuous Improvement:**

1. **Track Usage:** Which commands do you use most?
2. **Identify Gaps:** What context is missing?
3. **Refine Queries:** Which search terms work best?
4. **Adjust Settings:** Token limits, retention, modes
5. **Automate:** Scripts, aliases, hooks
6. **Share:** Workflows that work well

---

## 📚 Related Documentation

- **Quick Start:** `docs/idd/QUICK_START_AI_CONTEXT.md`
- **Session Capture Guide:** `docs/idd/session-capture-guide.md`
- **Memory Search Guide:** `docs/idd/memory-search-guide.md`
- **Context Retrieval Guide:** `docs/idd/context-retrieval-guide.md`
- **Week 2 Summary:** `docs/idd/WEEK_2_COMPLETION_SUMMARY.md`

---

**Last Updated:** November 5, 2025  
**Version:** 1.0  
**Status:** Complete ✅
