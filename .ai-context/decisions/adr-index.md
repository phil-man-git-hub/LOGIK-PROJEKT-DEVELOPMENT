# Architecture Decision Records (ADR) Index

**Repository:** WORKSTATION-CONFIGURATION  
**Started:** November 5, 2025  
**Format:** Markdown-based ADRs

---

## What are ADRs?

Architecture Decision Records (ADRs) document significant architectural and technical decisions made during the project. They capture:
- **Context:** Why was a decision needed?
- **Decision:** What did we decide?
- **Consequences:** What are the impacts?
- **Status:** Proposed, Accepted, Deprecated, Superseded

---

## ADR List

### 2025-11-05

#### ADR-001: Adopt Issue-Driven Development
- **Status:** ✅ Accepted
- **Context:** Need better work tracking and documentation
- **Decision:** Use GitHub Issues as single source of truth
- **Consequences:** All work tracked, better visibility, automated sync
- **Related Issues:** #1, #3, #5, #7, #10, #11
- **File:** `adr-001-issue-driven-development.md` (to be created)

#### ADR-002: TO-DO.md as Mirror, Not Source
- **Status:** ✅ Accepted
- **Context:** Need quick-reference dashboard but GitHub Issues are primary
- **Decision:** TO-DO.md mirrors Issues, auto-synced, never manually edited in AUTO-SYNC sections
- **Consequences:** Robust sync required, but better long-term scalability
- **Related Issues:** #5, #10
- **File:** `adr-002-todo-mirror.md` (to be created)

#### ADR-003: Git-Based AI Memory System
- **Status:** ✅ Accepted
- **Context:** Need persistent AI context across sessions
- **Decision:** Store AI context in git repository, not external cloud
- **Consequences:** Transparent, shareable, no dependencies, requires .gitignore management
- **Related Issues:** #15
- **File:** `adr-003-git-based-ai-memory.md` (to be created)

#### ADR-004: Python for Automation Scripts
- **Status:** ✅ Accepted
- **Context:** Need maintainable automation scripts
- **Decision:** Use Python 3.11+ for all automation
- **Consequences:** Aligns with existing stack, excellent libraries, requires Python dependency
- **Related Issues:** #5, #7
- **File:** `adr-004-python-automation.md` (to be created)

#### ADR-005: Markdown Session Files
- **Status:** ✅ Accepted
- **Context:** Need human-readable and AI-parseable session format
- **Decision:** Use Markdown for session capture files
- **Consequences:** Universal format, readable, git-friendly, searchable
- **Related Issues:** #15
- **File:** `adr-005-markdown-sessions.md` (to be created)

---

## How to Create an ADR

### 1. Use the Template
Copy `adr-template.md` to create a new ADR:
```bash
cp .ai-context/decisions/adr-template.md \
   .ai-context/decisions/adr-NNN-short-title.md
```

### 2. Fill in Details
- **Title:** Short, descriptive name
- **Status:** Proposed → Accepted/Rejected → (Deprecated/Superseded)
- **Context:** Why is this decision needed?
- **Decision:** What are we deciding?
- **Consequences:** What are the trade-offs?
- **Alternatives:** What else did we consider?

### 3. Review & Update Index
- Add entry to this index file
- Link related issues
- Mark status clearly

### 4. Commit
```bash
git add .ai-context/decisions/adr-NNN-*.md
git add .ai-context/decisions/adr-index.md
git commit -m "docs(adr): add ADR-NNN for [decision]"
```

---

## ADR Statuses

- **Proposed** 📋: Under consideration
- **Accepted** ✅: Decision made and active
- **Deprecated** ⚠️: No longer recommended
- **Superseded** 🔄: Replaced by another ADR

---

## Quick Reference

### View All ADRs
```bash
ls -1 .ai-context/decisions/adr-*.md
```

### Search ADRs
```bash
grep -r "keyword" .ai-context/decisions/adr-*.md
```

### Recent Decisions
See `quick-decisions.md` for minor decisions that don't warrant full ADRs.

---

**Index Maintained By:** Manual updates when ADRs created  
**Review Frequency:** Monthly  
**Last Updated:** 2025-11-05
