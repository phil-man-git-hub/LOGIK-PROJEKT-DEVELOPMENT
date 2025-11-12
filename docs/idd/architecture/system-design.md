# Issue-Driven Development: System Architecture

**Version:** 1.0  
**Last Updated:** November 5, 2025  
**Status:** Design Phase

---

## 🎯 Overview

This document describes the technical architecture of the Issue-Driven Development (IDD) system, including components, data flows, integration points, and implementation details.

---

## 📐 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Developer Interaction                     │
│  (Git commits, GitHub UI, CLI commands, AI assistant)           │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ├──────────────────┬──────────────────┬──────────────────┐
                 │                  │                  │                  │
                 ▼                  ▼                  ▼                  ▼
         ┌─────────────┐    ┌─────────────┐   ┌─────────────┐   ┌────────────┐
         │   GitHub    │    │  Git Hooks  │   │  CLI Tools  │   │  AI Agent  │
         │   Actions   │    │             │   │             │   │            │
         └──────┬──────┘    └──────┬──────┘   └──────┬──────┘   └──────┬─────┘
                │                  │                  │                  │
                └──────────────────┴──────────────────┴──────────────────┘
                                           │
                                           ▼
                         ┌────────────────────────────────┐
                         │   Automation Control Layer     │
                         │  (Workflow Orchestration)      │
                         └────────────────┬───────────────┘
                                          │
                 ┌────────────────────────┼────────────────────────┐
                 │                        │                        │
                 ▼                        ▼                        ▼
        ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
        │  Sync Engine   │      │  Context Mgr   │      │  Doc Generator │
        │                │      │                │      │                │
        │ • Issue→TODO   │      │ • Sessions     │      │ • Auto-docs    │
        │ • TODO→Issue   │      │ • Memory       │      │ • Changelogs   │
        │ • Conflicts    │      │ • Indexing     │      │ • Diagrams     │
        └────────┬───────┘      └────────┬───────┘      └────────┬───────┘
                 │                       │                       │
                 └───────────────────────┴───────────────────────┘
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │        Data Layer             │
                         │                               │
                         │ • GitHub API                  │
                         │ • Repository Files            │
                         │ • .ai-context/                │
                         │ • TO-DO.md                    │
                         └───────────────────────────────┘
```

---

## 🏗️ Core Components

### 1. Automation Control Layer

**Purpose:** Orchestrate all automation workflows and manage component interactions

**Components:**

#### 1.1 Workflow Orchestrator
- **Location:** `.github/workflows/`
- **Technology:** GitHub Actions YAML
- **Responsibilities:**
  - Trigger appropriate workflows on events
  - Coordinate multi-step processes
  - Handle errors and retries
  - Notify on failures

#### 1.2 Event Router
- **Location:** `.github/workflows/event-router.yml`
- **Responsibilities:**
  - Route GitHub events to appropriate handlers
  - Implement event filtering logic
  - Manage event priorities
  - Queue management for rate limiting

#### 1.3 State Manager
- **Location:** `.github/scripts/state_manager.py`
- **Responsibilities:**
  - Track workflow execution state
  - Prevent duplicate executions
  - Handle concurrent modifications
  - Implement idempotency

---

### 2. Synchronization Engine

**Purpose:** Bidirectional sync between GitHub Issues and TO-DO.md

**Location:** `.github/scripts/sync/`

#### 2.1 Issue Fetcher
**File:** `sync/issue_fetcher.py`

```python
class IssueFetcher:
    """Fetch issues from GitHub API with caching and rate limit handling"""
    
    def fetch_open_issues(self, labels=None, milestone=None):
        """Fetch open issues with optional filtering"""
        
    def fetch_issue_by_number(self, issue_number):
        """Fetch specific issue with full details"""
        
    def get_issue_timeline(self, issue_number):
        """Get issue history and events"""
```

**Features:**
- ETag-based conditional requests
- Response caching (5-minute TTL)
- Automatic rate limit handling
- Retry logic with exponential backoff

#### 2.2 TODO Parser
**File:** `sync/todo_parser.py`

```python
class TODOParser:
    """Parse and manipulate TO-DO.md structure"""
    
    def parse_sections(self):
        """Extract sections and task lists"""
        
    def identify_auto_sync_blocks(self):
        """Find <!-- BEGIN AUTO-SYNC --> regions"""
        
    def extract_manual_content(self):
        """Preserve manually-edited sections"""
```

**Features:**
- Markdown AST parsing
- Auto-sync boundary detection
- Manual section preservation
- Conflict detection

#### 2.3 Sync Coordinator
**File:** `sync/coordinator.py`

```python
class SyncCoordinator:
    """Coordinate bidirectional synchronization"""
    
    def sync_issues_to_todo(self):
        """Update TO-DO.md from issues"""
        
    def sync_todo_to_issues(self):
        """Create/update issues from TO-DO.md changes (future)"""
        
    def resolve_conflicts(self):
        """Handle sync conflicts intelligently"""
```

**Sync Strategy:**
```
1. Fetch current issues from GitHub
2. Parse existing TO-DO.md
3. Identify changes (diff)
4. Apply changes to auto-sync sections
5. Preserve manual sections
6. Generate updated TO-DO.md
7. Commit if changes exist
```

**Conflict Resolution:**
- GitHub Issues are source of truth
- Manual TO-DO sections never overwritten
- Conflicts logged for review
- Rollback capability

---

### 3. AI Context Manager

**Purpose:** Capture, index, and retrieve development context for AI assistants

**Location:** `bin/context/`

#### 3.1 Session Capture
**File:** `bin/context/session_capture.py`

```python
class SessionCapture:
    """Capture development session information"""
    
    def detect_session_boundaries(self):
        """Detect session start/end via git activity"""
        
    def capture_git_activity(self):
        """Capture commits, branches, file changes"""
        
    def capture_issue_activity(self):
        """Capture issue/PR interactions"""
        
    def generate_session_summary(self):
        """Create markdown summary"""
```

**Data Captured:**
```python
{
    "session_id": "2025-11-05-001",
    "timestamp": {
        "start": "2025-11-05T14:30:00Z",
        "end": "2025-11-05T18:45:00Z",
        "duration_minutes": 255
    },
    "git_activity": {
        "commits": ["c8da09c", "cffee60", "07be5e7"],
        "branches": ["main"],
        "files_changed": 75,
        "insertions": 1250,
        "deletions": 180
    },
    "work_summary": {
        "topics": ["monitoring", "macos", "documentation"],
        "issues": ["#23", "#24"],
        "prs": [],
        "key_files": [
            "docs/monitoring/LIBRENMS_MACOS_MONITORING.md",
            "src/workstation-configuration/monitoring/configure_macos_snmp_for_librenms.sh"
        ]
    },
    "decisions": [
        {
            "decision": "Use SNMPv3 for macOS monitoring",
            "rationale": "Better security than SNMPv2c",
            "alternatives": ["SNMP v2c", "ICMP only"],
            "timestamp": "2025-11-05T15:30:00Z"
        }
    ],
    "context_for_next_session": {
        "summary": "Added macOS monitoring support to LibreNMS. Next: add remaining infrastructure devices (whiskey, alpha, tango, echo)",
        "blockers": [],
        "pending_tasks": ["#25", "#26"]
    }
}
```

#### 3.2 Memory Indexer
**File:** `bin/context/memory_indexer.py`

```python
class MemoryIndexer:
    """Index and search development context"""
    
    def index_session(self, session_data):
        """Add session to searchable index"""
        
    def search_by_topic(self, topic):
        """Find sessions related to topic"""
        
    def search_by_issue(self, issue_number):
        """Find sessions that worked on issue"""
        
    def get_recent_context(self, depth=3):
        """Get last N sessions for context loading"""
```

**Index Structure:**
```json
{
  "index_version": "1.0",
  "last_updated": "2025-11-05T18:45:00Z",
  "sessions": [
    {
      "id": "2025-11-05-001",
      "date": "2025-11-05",
      "topics": ["monitoring", "macos", "documentation"],
      "keywords": ["librenms", "snmpv3", "romeo", "automation"],
      "issues": ["#23", "#24"],
      "files": ["docs/monitoring/*", "src/monitoring/*"],
      "importance": 0.95,
      "summary": "Added macOS monitoring support..."
    }
  ],
  "topic_index": {
    "monitoring": ["2025-11-05-001", "2025-11-04-002"],
    "macos": ["2025-11-05-001"],
    "documentation": ["2025-11-05-001", "2025-11-04-001"]
  },
  "issue_index": {
    "23": ["2025-11-05-001"],
    "24": ["2025-11-05-001", "2025-11-04-002"]
  }
}
```

#### 3.3 Context Retriever
**File:** `bin/context/retriever.py`

```python
class ContextRetriever:
    """Retrieve relevant context for AI assistants"""
    
    def get_context_for_issue(self, issue_number):
        """Get all context related to an issue"""
        
    def get_recent_context(self, depth=3):
        """Get last N sessions"""
        
    def get_context_by_topic(self, topic):
        """Get context for specific topic"""
        
    def format_for_ai(self, context):
        """Format context for AI consumption"""
```

**Usage Example:**
```bash
# Get context for current work
./bin/context/retriever.py --issue 25 --depth 3

# Output: Markdown formatted context
## Recent Context (Last 3 Sessions)

### Session 2025-11-05-001
Topics: monitoring, macos, documentation
Issues: #23, #24
Summary: Added macOS monitoring support...

[Full context details...]
```

---

### 4. Documentation Generator

**Purpose:** Auto-generate and maintain documentation

**Location:** `bin/docs/`

#### 4.1 Code Documentation
**File:** `bin/docs/code_doc_generator.py`

**Features:**
- Extract docstrings and comments
- Generate API documentation
- Create code reference guides
- Update on code changes

#### 4.2 Changelog Generator
**File:** `bin/docs/changelog_generator.py`

**Features:**
- Parse commit messages
- Group by type (feat/fix/docs/etc)
- Link to issues and PRs
- Format for CHANGELOG.md

**Format:**
```markdown
## [1.2.0] - 2025-11-05

### Added
- macOS monitoring support for LibreNMS (#23)
- Automated SNMPv3 configuration script
- Comprehensive documentation for macOS monitoring

### Changed
- Reorganized documentation into topic subdirectories (#24)
- Updated TO-DO.md structure for IDD

### Fixed
- None

### Deprecated
- None
```

#### 4.3 Diagram Generator
**File:** `bin/docs/diagram_generator.py`

**Features:**
- Generate architecture diagrams from code
- Create dependency graphs
- Update on structural changes
- Support multiple formats (PlantUML, Mermaid, etc.)

---

## 🔄 Data Flows

### Flow 1: Issue Created → TO-DO Updated

```
1. Developer creates issue in GitHub UI
   ├─ Title: "Add whiskey.projekt.lab to LibreNMS"
   ├─ Labels: monitoring, task
   └─ Milestone: Infrastructure Monitoring

2. GitHub webhook triggers issue.opened event

3. GitHub Actions workflow: issue-to-todo-sync.yml
   ├─ Checkout repository
   ├─ Run sync_issues_to_todo.py
   └─ Commit changes if any

4. sync_issues_to_todo.py execution:
   ├─ Fetch all open issues via API
   ├─ Parse TO-DO.md
   ├─ Find auto-sync section
   ├─ Generate updated task list
   ├─ Preserve manual sections
   └─ Write updated TO-DO.md

5. Commit and push:
   ├─ Message: "🤖 Auto-sync: Update TO-DO.md from issues"
   ├─ Author: github-actions[bot]
   └─ Push to main branch

6. Developer pulls latest changes:
   └─ TO-DO.md now includes new task
```

### Flow 2: Commit Made → Session Captured

```
1. Developer makes commits during work session:
   ├─ commit 1: Add SNMP configuration
   ├─ commit 2: Update documentation
   └─ commit 3: Fix typo

2. Git hook triggers on push (optional):
   └─ post-commit or post-push hook

3. Session capture script: bin/context/session_capture.py
   ├─ Detect session boundary (time gap or explicit trigger)
   ├─ Collect git activity:
   │   ├─ List of commits
   │   ├─ Files changed
   │   └─ Diff statistics
   ├─ Collect issue/PR activity:
   │   ├─ Issues referenced in commits
   │   └─ PRs created/updated
   ├─ Extract key decisions:
   │   └─ Parse commit messages for decisions
   └─ Generate session summary markdown

4. Update memory index:
   ├─ Add session to .ai-context/memory/sessions/
   ├─ Update .ai-context/memory/index.json
   └─ Update topic/issue indices

5. Session document created:
   └─ .ai-context/memory/sessions/2025-11-05-001.md
```

### Flow 3: PR Opened → Validation Run

```
1. Developer opens Pull Request

2. GitHub webhook triggers pull_request.opened event

3. GitHub Actions workflow: pr-validation.yml
   ├─ Check issue linking:
   │   ├─ Parse PR body for "Closes #XX" or "Related: #XX"
   │   └─ Fail if no issue references found
   ├─ Check changelog:
   │   ├─ Detect if feature/fix type
   │   ├─ Verify CHANGELOG.md updated
   │   └─ Warn if missing (not block)
   ├─ Check documentation:
   │   ├─ Detect code changes in src/
   │   ├─ Check for docs/ changes
   │   └─ Comment if docs likely needed
   └─ Run tests:
       ├─ Execute test suite
       └─ Report results

4. Post results as PR comment:
   └─ Checklist of validations passed/failed

5. Block merge if critical validations fail:
   └─ Require issue linking
```

---

## 🔐 Security & Privacy

### API Authentication

**GitHub Actions:**
```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
- Uses built-in GITHUB_TOKEN
- Scoped to repository
- Automatically rotated

**Personal Access Token (for higher rate limits):**
```yaml
env:
  GH_PAT: ${{ secrets.GH_PAT }}
```
- Stored in repository secrets
- Used for API-heavy operations
- Classic token with `repo` scope

### Sensitive Data Protection

**.gitignore additions:**
```
# AI Context - Sensitive Data
.ai-context/memory/sensitive/
.ai-context/credentials/
*.secret.md

# Local Development
.env.local
config.local.yml
```

**Data Sanitization:**
- Remove credentials from session captures
- Redact sensitive paths
- Sanitize error messages
- Filter environment variables

---

## ⚡ Performance Considerations

### API Rate Limiting

**GitHub API Limits:**
- **Authenticated:** 5,000 requests/hour
- **Unauthenticated:** 60 requests/hour
- **With GitHub App:** 15,000 requests/hour

**Mitigation Strategies:**
1. **Conditional Requests (ETags)**
   ```python
   headers = {'If-None-Match': etag}
   # Returns 304 Not Modified if no changes
   ```

2. **Response Caching**
   ```python
   cache_ttl = 300  # 5 minutes
   # Cache issue data to reduce API calls
   ```

3. **Batch Operations**
   ```python
   # Fetch all issues in one call instead of individual calls
   issues = repo.get_issues(state='open')
   ```

4. **GraphQL API**
   ```python
   # Use GraphQL for complex queries (single request)
   # Instead of multiple REST API calls
   ```

### Sync Performance

**Target Performance:**
- Issue fetch: <2 seconds
- TO-DO parse: <100ms
- Sync operation: <3 seconds total
- Session capture: <5 seconds

**Optimization:**
- Parallel API requests where possible
- Incremental updates (not full rewrites)
- Lazy loading of issue details
- Background processing for heavy operations

---

## 🧪 Testing Strategy

### Unit Tests

**Location:** `tests/idd/`

```
tests/idd/
├── test_sync_engine.py
├── test_context_manager.py
├── test_todo_parser.py
└── test_issue_fetcher.py
```

**Coverage Target:** >80%

### Integration Tests

**Location:** `tests/integration/`

```
tests/integration/
├── test_issue_to_todo_flow.py
├── test_session_capture_flow.py
└── test_pr_validation_flow.py
```

**Test Environment:**
- Use test repository or branch
- Mock GitHub API for reliability
- Simulate webhook events

### End-to-End Tests

**Manual Test Scenarios:**
1. Create issue → Verify TO-DO updated
2. Make commits → Verify session captured
3. Open PR → Verify validations run
4. Close issue → Verify TO-DO updated

---

## 📦 Deployment & Rollout

### Phase 1 Deployment (Week 1)

**Steps:**
1. Create `.github/` directory structure
2. Add issue templates
3. Deploy sync script
4. Enable first workflow (issue-to-todo)
5. Monitor for 48 hours
6. Fix issues if any
7. Enable additional workflows

**Rollback Plan:**
- Disable GitHub Actions workflows
- Revert TO-DO.md changes
- Document issues encountered
- Fix and redeploy

### Phase 2-4 Deployments

**Incremental Approach:**
- One feature at a time
- Monitor each for 24-48 hours
- Collect feedback
- Iterate and improve

---

## 🔮 Future Enhancements

### Potential Features

1. **Slack/Discord Integration**
   - Post issue updates to channels
   - Notify on PR reviews
   - Daily standup summaries

2. **Advanced Analytics**
   - Issue velocity tracking
   - Cycle time analysis
   - Burndown charts

3. **AI-Powered Suggestions**
   - Auto-suggest issue labels
   - Recommend reviewers
   - Predict issue complexity

4. **Mobile App Integration**
   - Quick issue triage
   - Context viewing on mobile
   - Voice-to-issue creation

5. **Cross-Repository Sync**
   - Sync related issues across repos
   - Shared context between projects
   - Dependency tracking

---

## 📞 Architecture Decisions

See [decision-records/](decision-records/) for detailed ADRs:

- [ADR-001: TO-DO.md as Mirror](decision-records/001-todo-as-mirror.md) (to be created)
- [ADR-002: Git-Based Memory](decision-records/002-git-based-memory.md) (to be created)
- [ADR-003: Hybrid Session Capture](decision-records/003-hybrid-session-capture.md) (to be created)

---

*Last Updated: November 5, 2025*  
*Version: 1.0*  
*Status: Design Complete, Implementation Starting*
