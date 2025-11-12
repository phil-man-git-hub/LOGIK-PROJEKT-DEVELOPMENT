# Quick Decisions

**Purpose:** Track minor technical decisions that don't warrant full ADRs  
**Repository:** WORKSTATION-CONFIGURATION  
**Format:** Chronological log of decisions with reasoning

---

## Decision Log

### 2025-11-05

#### Use PyGithub >=2.1.1 for GitHub API
- **Context:** Need to interact with GitHub Issues programmatically
- **Decision:** PyGithub library for sync script
- **Reasoning:** Well-maintained, feature-complete, official recommendation
- **Alternative Considered:** Direct REST API (too verbose)
- **Impact:** Low - standard library choice

---

#### Session Files Named by Date (YYYY-MM-DD.md)
- **Context:** Need consistent session file naming
- **Decision:** Use ISO date format for session files
- **Reasoning:** Sortable, unambiguous, international standard
- **Alternative Considered:** Week numbers (less intuitive)
- **Impact:** Low - file naming convention

---

#### 90-Day Memory Retention
- **Context:** Balance context depth with repo size
- **Decision:** Keep 90 days of sessions, archive older
- **Reasoning:** 3 months covers most project cycles
- **Alternative Considered:** 180 days (too large), 30 days (too short)
- **Impact:** Medium - affects disk usage and context availability

---

#### Context Depth = 3 Levels
- **Context:** How deep should AI context include related items
- **Decision:** 3 levels (current issue → related PRs → referenced files)
- **Reasoning:** Balances completeness with performance
- **Alternative Considered:** 5 levels (too slow), 1 level (insufficient)
- **Impact:** Medium - affects AI context quality

---

#### Use .gitignore for Sensitive Data
- **Context:** Protect API tokens and personal info
- **Decision:** Comprehensive .gitignore in .ai-context/
- **Reasoning:** Standard security practice, prevents accidental commits
- **Alternative Considered:** External storage (breaks git-based approach)
- **Impact:** Critical - security requirement

---

#### JSON for Configuration Files
- **Context:** Need structured, machine-readable config
- **Decision:** Use JSON for config.json and index.json
- **Reasoning:** Widely supported, simple structure, Python-friendly
- **Alternative Considered:** YAML (more complex), TOML (less common)
- **Impact:** Low - configuration format choice

---

#### Markdown for Documentation
- **Context:** Need human-readable documentation format
- **Decision:** Use Markdown for all docs and session files
- **Reasoning:** Universal, git-friendly, rendered on GitHub
- **Alternative Considered:** ReStructuredText (less common), AsciiDoc (overkill)
- **Impact:** Low - documentation format standard

---

#### Feature Branch Naming: feature/issue-N-short-title
- **Context:** Need consistent branch naming
- **Decision:** Prefix with feature/, include issue number and short title
- **Reasoning:** Clear traceability, descriptive, follows git flow
- **Alternative Considered:** Just issue number (less descriptive)
- **Impact:** Low - branch naming convention

---

#### Commit Message Format: type(scope): description
- **Context:** Need consistent commit message structure
- **Decision:** Use conventional commits format
- **Reasoning:** Standard practice, enables automation, clear intent
- **Alternative Considered:** Free-form (less structured)
- **Impact:** Low - commit message convention

---

#### Auto-Sync Frequency: Every 5 Minutes
- **Context:** How often should TO-DO.md sync from Issues
- **Decision:** Every 5 minutes via GitHub Actions
- **Reasoning:** Near real-time, doesn't overwhelm API limits
- **Alternative Considered:** 1 minute (too frequent), 15 minutes (too slow)
- **Impact:** Low - workflow timing decision

---

#### Test Issue Numbers: #13+
- **Context:** Where to create test issues
- **Decision:** Create test issues in production repo, close immediately
- **Reasoning:** Tests real workflow, validates actual behavior
- **Alternative Considered:** Separate test repo (doesn't test integration)
- **Impact:** Low - testing approach

---

#### Dashboard Stats Update: On Every Sync
- **Context:** When should dashboard statistics refresh
- **Decision:** Every time sync script runs
- **Reasoning:** Always current, no manual intervention
- **Alternative Considered:** Manual updates (unreliable)
- **Impact:** Low - automation behavior

---

## Decision Format

Each entry should include:
- **Context:** Why was this decision needed?
- **Decision:** What did we decide?
- **Reasoning:** Why this choice?
- **Alternative Considered:** What else did we think about?
- **Impact:** Low/Medium/High/Critical - scope of change

## When to Use This File vs. ADR

**Use Quick Decisions for:**
- Tool/library selections (standard choices)
- File naming conventions
- Coding style preferences
- Workflow timing decisions
- Minor configuration choices

**Use full ADR for:**
- Architectural changes
- Major technology decisions
- Breaking changes
- Policy changes
- High-impact decisions affecting multiple components

---

**Maintained By:** Development team  
**Review Frequency:** As needed  
**Last Updated:** 2025-11-05
