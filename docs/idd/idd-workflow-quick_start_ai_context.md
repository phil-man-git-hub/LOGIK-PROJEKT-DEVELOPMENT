# Quick Start: AI Context System

**Get started with the AI Memory & Context system in 5 minutes**

---

## 🚀 Overview

The AI Context System provides:
- **Persistent Memory** - Sessions auto-captured
- **Searchable History** - Full-text search with filters
- **Smart Context** - Intelligent assembly for AI
- **Token Management** - Stay within AI limits

---

## 📦 Prerequisites

- Python 3.9+
- Git repository
- AI context structure (already set up)

---

## ⚡ Quick Start (3 Steps)

### Step 1: Capture Today's Session

```bash
python bin/capture-session.py
```

**Output:**
```
📸 Capturing session for 2025-11-05...
  🔍 Detecting git commits...
  ✓ Found 32 commits
  📝 Generating session file...
  ✓ Created 2025-11-05.md
  📇 Updating session index...
  ✓ Updated index.json

✅ Session capture complete
```

### Step 2: Search for Context

```bash
python bin/search-context.py "IDD"
```

**Output:**
```
🔍 Found 1 session(s) with matches

1. Session: 2025-11-05
   Matches: 13
   Relevance: 223
   ...
```

### Step 3: Retrieve Context for AI

```bash
python bin/retrieve-context.py --topic "IDD" --mode focused
```

**Output:**
```
🔍 Assembling context...
✓ Assembled 2 sources (1788 tokens)

# AI Context Assembly
**Mode:** focused
**Sources:** 2
**Total Tokens:** ~1788
...
```

---

## 📖 Common Use Cases

### Daily Workflow

**Morning: Capture Yesterday**
```bash
python bin/capture-session.py --date $(date -v-1d +%Y-%m-%d)
```

**During Work: Search for Context**
```bash
python bin/search-context.py "monitoring setup"
```

**End of Day: Capture Today**
```bash
python bin/capture-session.py
```

### AI Pair Programming

**Get Context for AI Assistant**
```bash
# Save to file
python bin/retrieve-context.py --issue 15 -o context.md

# Then provide context.md to your AI assistant
```

**Search for Past Decisions**
```bash
python bin/search-context.py "dashboard stats" --type fix
```

### Code Review

**Get Full Context for PR**
```bash
python bin/retrieve-context.py --issue 15 --mode comprehensive
```

**Find Related Work**
```bash
python bin/search-context.py --issue 15
```

---

## 🎯 Common Commands

### Session Capture

```bash
# Today (default)
python bin/capture-session.py

# Specific date
python bin/capture-session.py --date 2025-11-05

# Last 7 days
python bin/capture-session.py --range 7
```

### Search

```bash
# Basic search
python bin/search-context.py "query"

# Search with filters
python bin/search-context.py "automation" --date-range 7

# Find by issue
python bin/search-context.py --issue 15

# Find by type
python bin/search-context.py --type feat

# JSON output
python bin/search-context.py "context" --format json
```

### Context Retrieval

```bash
# Focused mode (specific topic)
python bin/retrieve-context.py --topic "testing"

# Broad mode (balanced, default)
python bin/retrieve-context.py --mode broad

# Comprehensive mode (full context)
python bin/retrieve-context.py --mode comprehensive --days 30

# Limited tokens
python bin/retrieve-context.py --topic "IDD" --max-tokens 4000

# Save to file
python bin/retrieve-context.py --issue 15 -o context.md
```

---

## 💡 Pro Tips

### 1. Daily Automation

Add to your `.zshrc` or `.bashrc`:

```bash
alias capture-session='python ~/path/to/repo/bin/capture-session.py'
alias search-context='python ~/path/to/repo/bin/search-context.py'
alias get-context='python ~/path/to/repo/bin/retrieve-context.py'
```

### 2. Cron Jobs

Capture automatically at end of day:

```bash
# Add to crontab
0 18 * * * cd /path/to/repo && python bin/capture-session.py
```

### 3. Git Hooks

Capture on push (optional):

```bash
# .git/hooks/post-commit
#!/bin/bash
python bin/capture-session.py --date $(date +%Y-%m-%d) > /dev/null 2>&1
```

### 4. VS Code Tasks

Add to `.vscode/tasks.json`:

```json
{
  "label": "Capture Session",
  "type": "shell",
  "command": "python",
  "args": ["bin/capture-session.py"]
},
{
  "label": "Search Context",
  "type": "shell",
  "command": "python",
  "args": [
    "bin/search-context.py",
    "${input:searchQuery}"
  ]
}
```

---

## 🔧 Troubleshooting

### "Sessions directory not found"

**Problem:** AI context structure missing  
**Solution:**
```bash
ls -la .ai-context/memory/sessions/
```

If missing, check that issue #15 was completed.

### "No commits found"

**Problem:** No commits on specified date  
**Solution:** Normal if no work done that day. Script will create empty session.

### Search returns no results

**Problem:** No matching content  
**Solution:** Try broader terms or check date filters

### Token limit exceeded

**Problem:** Context too large for AI model  
**Solution:**
```bash
# Reduce token limit
python bin/retrieve-context.py --topic "xyz" --max-tokens 4000 --mode focused
```

---

## 📚 Learn More

### Detailed Guides
- **Session Capture:** `docs/idd/session-capture-guide.md`
- **Memory Search:** `docs/idd/memory-search-guide.md`
- **Context Retrieval:** `docs/idd/context-retrieval-guide.md`

### System Overview
- **AI Context README:** `.ai-context/README.md`
- **Week 2 Summary:** `docs/idd/WEEK_2_COMPLETION_SUMMARY.md`
- **IDD Roadmap:** `docs/idd/ROADMAP_ISSUE_DRIVEN_DEVELOPMENT.md`

---

## 🎓 Example Workflows

### Workflow 1: Start Work on Issue

```bash
# 1. Get context for issue
python bin/retrieve-context.py --issue 23 -o context.md

# 2. Read context
cat context.md

# 3. Do your work...

# 4. Capture session at end of day
python bin/capture-session.py
```

### Workflow 2: Research a Topic

```bash
# 1. Search for topic
python bin/search-context.py "monitoring" --date-range 30

# 2. Get comprehensive context
python bin/retrieve-context.py --topic "monitoring" --mode comprehensive

# 3. Review and use findings
```

### Workflow 3: AI Pair Programming

```bash
# 1. Get focused context
python bin/retrieve-context.py --topic "current task" --mode focused -o ai-context.md

# 2. Share ai-context.md with AI assistant

# 3. Work with AI using shared context

# 4. Capture session
python bin/capture-session.py
```

---

## ⚡ Performance

- **Session Capture:** < 1 second for single day
- **Search:** < 1 second for basic queries
- **Context Retrieval:** < 1 second for focused mode
- **Memory Usage:** Minimal (streaming)

---

## 🆘 Need Help?

1. **Check Guides:** See detailed documentation above
2. **View Examples:** Run with `--help` flag
3. **Read README:** `.ai-context/README.md`
4. **Check Issues:** [GitHub Issues](https://github.com/phil-man-git-hub/WORKSTATION-CONFIGURATION/issues)

---

## ✅ Next Steps

Once comfortable with basics:

1. **Automate Capture:** Set up daily cron job
2. **Integrate with AI:** Use context retrieval in your workflow
3. **Explore Modes:** Try focused, broad, comprehensive
4. **Customize:** Adjust token limits for your AI model
5. **Share Context:** Export for team members

---

**Last Updated:** November 5, 2025  
**System Version:** 1.0  
**Status:** Fully Operational ✅
