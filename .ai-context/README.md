# AI Context System

**Version:** 1.0  
**Created:** November 5, 2025  
**Purpose:** Persistent AI memory and context management for development sessions

---

## Overview

This directory contains the AI context management system for the WORKSTATION-CONFIGURATION repository. It provides:

- **Session Capture:** Automatic documentation of development sessions
- **Context Snippets:** Topic-based knowledge organization
- **Decision Records:** Architecture and implementation decisions
- **Memory Index:** Searchable history of work done
- **Active Context:** Current work state for AI continuity

### Benefits

1. **Continuity Across Sessions:** AI assistants can pick up where you left off
2. **Knowledge Retention:** Important decisions and context preserved
3. **Faster Onboarding:** New developers/AI can quickly understand the project
4. **Better Documentation:** Automatic session capture reduces manual work
5. **Searchable History:** Find past decisions and reasoning quickly

---

## Directory Structure

```
.ai-context/
├── config.json                    # System configuration
├── README.md                      # This file
├── .gitignore                     # Sensitive data exclusions
│
├── memory/
│   ├── sessions/                  # Development session logs
│   │   ├── 2025-11-05.md         # Daily session capture
│   │   ├── 2025-11-06.md
│   │   └── index.json            # Searchable session index
│   │
│   ├── context-snippets/          # Topic-based context
│   │   ├── infrastructure.md     # Infrastructure knowledge
│   │   ├── monitoring.md         # Monitoring setup
│   │   ├── networking.md         # Network configuration
│   │   └── idd-implementation.md # IDD system details
│   │
│   └── active-context.json       # Current work state
│
└── decisions/
    ├── adr-index.md              # Architecture Decision Records index
    └── quick-decisions.md        # Minor decisions log
```

---

## File Descriptions

### Configuration Files

#### `config.json`
System-wide configuration including:
- Memory retention settings
- Session capture preferences
- Context snippet topics
- AI integration parameters

See inline documentation in `config.json` for details.

#### `.gitignore`
Protects sensitive information from being committed:
- API keys and tokens
- Private credentials
- Personal notes
- Temporary files

---

### Memory System

#### `memory/sessions/`
**Purpose:** Chronological record of development sessions

**Format:** One markdown file per session (usually daily)

**Contents:**
- Date and duration
- Issues worked on
- Files modified
- Key decisions made
- Commits and PRs
- Context for next session

**Example:**
```markdown
# Development Session: 2025-11-05

**Duration:** 14:00 - 18:30 UTC (4.5 hours)
**Focus:** IDD Foundation Phase completion

## Issues Addressed
- #10: Enhance TO-DO.md structure
- #11: Test and validate automation

## Key Accomplishments
- Implemented dashboard statistics
- Executed 10 critical tests
- Achieved 100% Week 1 completion

## Next Session
Continue with Week 2: AI Memory & Context
```

#### `memory/context-snippets/`
**Purpose:** Topic-based knowledge organization

**Format:** One markdown file per major topic

**Topics:**
- `infrastructure.md`: Server setup, VM configuration
- `monitoring.md`: LibreNMS, SNMP, alerts
- `networking.md`: Network topology, DNS, routing
- `idd-implementation.md`: IDD system architecture
- `certificate-management.md`: FreeIPA, SSL certificates

**Update Strategy:** Manual updates when significant changes occur

#### `memory/index.json`
**Purpose:** Searchable index of all sessions

**Format:** JSON with metadata for quick lookups

**Generated:** Automatically by session capture script

**Example:**
```json
{
  "sessions": [
    {
      "date": "2025-11-05",
      "file": "2025-11-05.md",
      "topics": ["idd", "testing", "automation"],
      "issues": ["#10", "#11"],
      "commits": ["77f97f7", "54bbde8"]
    }
  ],
  "last_updated": "2025-11-05T19:30:00Z",
  "total_sessions": 1
}
```

#### `memory/active-context.json`
**Purpose:** Current work state for AI continuity

**Updated:** After each significant milestone

**Contents:**
- Current phase/sprint
- Active issues
- Recent decisions
- Next actions
- Known blockers

---

### Decision System

#### `decisions/adr-index.md`
**Purpose:** Index of Architecture Decision Records (ADRs)

**Format:** List of ADRs with dates and status

**Example:**
```markdown
# Architecture Decision Records

## Index

- [ADR-001](./adr-001-issue-driven-development.md) - Adopt Issue-Driven Development (2025-11-05) ✅
- [ADR-002](./adr-002-todo-md-as-mirror.md) - TO-DO.md as Mirror Not Source (2025-11-05) ✅
```

#### `decisions/quick-decisions.md`
**Purpose:** Log of minor decisions that don't warrant full ADRs

**Format:** Chronological list with rationale

**Example:**
```markdown
## 2025-11-05
- **Decision:** Use Python 3.11+ for automation scripts
  **Rationale:** Already in use, excellent GitHub API libraries
  **Impact:** Low - aligns with existing stack
```

---

## Usage

### For Developers

#### Starting a New Session
1. Review `memory/active-context.json` to understand current state
2. Check recent session files in `memory/sessions/`
3. Update context as you work
4. Run session capture script at end of day (when available)

#### Updating Context Snippets
When you make significant changes to a topic area:
```bash
# Edit the relevant context snippet
vim .ai-context/memory/context-snippets/monitoring.md

# Commit the update
git add .ai-context/memory/context-snippets/monitoring.md
git commit -m "docs(ai-context): update monitoring context with new hosts"
```

#### Recording Decisions
For major decisions, create an ADR:
```bash
# Create new ADR file
cp .ai-context/decisions/adr-template.md .ai-context/decisions/adr-003-my-decision.md

# Edit and commit
git add .ai-context/decisions/
git commit -m "docs(adr): add decision on [topic]"
```

For minor decisions, add to `quick-decisions.md`.

---

### For AI Assistants

#### Loading Context at Session Start
1. Read `memory/active-context.json` first
2. Load last 3 sessions from `memory/sessions/`
3. Load relevant context snippets based on current work
4. Check recent decisions from `decisions/`

#### Priority Order
As configured in `config.json`:
1. **active-context.json** - Most recent state
2. **recent-sessions** - Last 3 session files
3. **topic-snippets** - Relevant topics only
4. **decisions** - Recent ADRs and decisions

#### Context Window Management
With a 32K token context window (configurable):
- Reserve 20% for user queries and responses
- Use 80% for loaded context
- Prioritize recent and relevant information
- Summarize older sessions if needed

---

## Automation

### Session Capture (Coming in Task 2.2)
The `bin/capture-session.py` script will automatically:
- Detect git activity
- Extract commit messages
- Link related issues and PRs
- Generate session markdown files
- Update the search index

### Search & Retrieval (Coming in Task 2.3)
The `bin/search-context.py` script will enable:
- Full-text search across all sessions
- Filter by date, topic, or issue
- Quick context retrieval for AI
- Relevance-ranked results

---

## Best Practices

### DO:
- ✅ Commit session files regularly
- ✅ Update active-context.json after major milestones
- ✅ Create ADRs for significant architectural decisions
- ✅ Keep context snippets concise and current
- ✅ Use .gitignore to protect sensitive data

### DON'T:
- ❌ Commit API keys, tokens, or credentials
- ❌ Let context snippets grow too large (>50KB)
- ❌ Leave active-context.json stale
- ❌ Skip session capture for significant work
- ❌ Include diffs with sensitive information

---

## Configuration

### Key Settings in `config.json`

```json
{
  "memory": {
    "retention_days": 90,        // How long to keep sessions
    "context_depth": 3,          // How many past sessions to load
    "auto_capture": true         // Auto-generate session files
  },
  "sessions": {
    "include_diffs": false,      // Whether to include code diffs
    "include_issues": true,      // Link to GitHub issues
    "capture_git_activity": true // Detect commits/branches
  },
  "ai_integration": {
    "context_window_tokens": 32000,  // AI context window size
    "auto_summarize": true           // Summarize old sessions
  }
}
```

See `config.json` for full configuration options.

---

## Examples

### Example Session File
See `memory/sessions/2025-11-05.md` for today's session documenting Week 1 completion.

### Example Context Snippet
See `memory/context-snippets/idd-implementation.md` for IDD system knowledge.

### Example Active Context
See `memory/active-context.json` for current work state.

---

## Maintenance

### Weekly
- Review active-context.json and update if needed
- Check that .gitignore is protecting sensitive files
- Verify session index is up to date

### Monthly
- Archive old sessions (older than retention period)
- Review and update context snippets
- Clean up any stale or duplicate information

### Quarterly
- Review and consolidate ADRs
- Update system configuration if needed
- Evaluate and improve the context system

---

## Troubleshooting

### Issue: Context files too large
**Solution:** 
- Summarize old sessions
- Split large context snippets by subtopic
- Adjust `max_size_kb` in config.json

### Issue: AI not loading correct context
**Solution:**
- Check `active-context.json` is current
- Verify topic assignments in context snippets
- Review priority order in config.json

### Issue: Sensitive data committed
**Solution:**
- Update .gitignore immediately
- Remove from git history: `git filter-branch`
- Rotate any exposed credentials

---

## Version History

- **1.0** (2025-11-05): Initial AI context system implementation
  - Directory structure created
  - Configuration system established
  - Documentation completed

---

## Related Documentation

- [IDD Roadmap](../docs/idd/ROADMAP_ISSUE_DRIVEN_DEVELOPMENT.md)
- [System Architecture](../docs/idd/architecture/system-design.md) (coming soon)
- [Session Capture Guide](../docs/idd/session-capture-guide.md) (coming soon)

---

**Questions or suggestions?** Open an issue with the `ai-context` label.
