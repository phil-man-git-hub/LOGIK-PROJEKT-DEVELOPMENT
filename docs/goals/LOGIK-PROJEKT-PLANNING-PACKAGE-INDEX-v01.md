# LOGIK-PROJEKT SQLite Integration - Complete Planning Package (v01)

**Last Updated:** February 8, 2026

---

## Overview

This package contains **four comprehensive planning documents** that define a complete roadmap for integrating SQLite databases into LOGIK-PROJEKT. The documents work together to provide:

1. **Strategic vision** (what and why)
2. **Architectural design** (how components interact)
3. **Data mapping** (where existing data lives in the new system)
4. **Implementation details** (exactly what code to write and how to test it)

---

## The Four Documents

### 📋 Document 1: Database Architecture Plan (v01)

**File:** [`LOGIK-PROJEKT-DB-PLAN-v01.md`](LOGIK-PROJEKT-DB-PLAN-v01.md)

**Purpose:** Strategic architecture and database design

**Contains:**
- Executive summary of improvements
- Overall system architecture (producer workstation, artist workstations, web UI)
- Complete SQLite schema with 6 tables
- Multi-user collaboration workflow
- Archive/restore capabilities
- Web UI features (file browser, media viewers, changelog)
- Technology stack choices
- 7-phase implementation roadmap (high-level)
- Success criteria

**Key Insight:**
> Each project gets its own SQLite database file (`/PROJEKTS/<PROJECT>/db/<PROJECT>.db`) that travels with the project and contains complete metadata, relationships, and audit trails.

**Use this document when:**
- Explaining the vision to stakeholders
- Understanding overall system design
- Making architectural decisions
- Reviewing schema design

---

### 🔄 Document 2: Application Transition Plan (v01)

**File:** [`LOGIK-PROJEKT-APP-TRANSITION-v01.md`](LOGIK-PROJEKT-APP-TRANSITION-v01.md)

**Purpose:** How the existing PySide6 GUI application evolves

**Contains:**
- Current application architecture (detailed breakdown)
- Enhanced architecture with database integration
- 4 key transition phases with code examples
- Data migration strategy for existing projects
- Docker setup for all components
- Backward compatibility guarantees
- Timeline and effort estimates
- Open questions for discussion

**Key Insight:**
> The existing LOGIK-PROJEKT application remains largely unchanged. SQLite initialization is added to `projekt_creator.py`, and a new database manager module is created. No breaking changes to UI or core logic.

**Use this document when:**
- Understanding how to modify existing code
- Planning the transition from current state to new state
- Setting up Docker containers
- Migrating existing projects
- Reviewing code changes needed

---

### 📊 Document 3: Data-to-Database Mapping Plan (v01)

**File:** [`LOGIK-PROJEKT-DATA-TO-DB-MAPPING-v01.md`](LOGIK-PROJEKT-DATA-TO-DB-MAPPING-v01.md)

**Purpose:** Detailed mapping of existing data flows to SQLite schema

**Contains:**
- Current vs. enhanced data flows (visual comparison)
- Table-by-table mapping of data sources
- Where each data element gets stored in the database
- Integration points with existing workflows
- Data validation and integrity checks
- Persistence strategies for internet storage
- Benefits analysis (what this enables)
- Open questions

**Key Insight:**
> Every piece of data currently scattered across panels, configs, and JSON files now has a home in the SQLite database, enabling comprehensive tracking, searching, and auditing.

**Use this document when:**
- Implementing database population logic
- Understanding what data goes where
- Designing database queries
- Debugging data consistency issues
- Explaining data relationships

---

### 🛠️ Document 4: Implementation Roadmap (v01)

**File:** [`LOGIK-PROJEKT-IMPLEMENTATION-ROADMAP-v01.md`](LOGIK-PROJEKT-IMPLEMENTATION-ROADMAP-v01.md)

**Purpose:** Detailed step-by-step implementation guide with code examples

**Contains:**
- Pre-implementation checklist
- Phase 1: Database schema & initialization (complete with code)
- Phase 2: File monitoring service (Docker + Python)
- Phase 3: Web UI for browsing
- Phase 4: GUI integration
- Phase 5: Data migration for existing projects
- Phase 6: Testing & Docker Compose
- Phase 7: Documentation
- Comprehensive testing strategy
- Risk assessment and rollback procedures
- Effort estimation (9 weeks, 110 hours total)
- Success criteria checklist
- Known limitations and future work

**Key Insight:**
> This is the actual implementation guide. It has real Python code examples, file paths, test cases, and a concrete 9-week timeline.

**Use this document when:**
- Writing actual code (copy/adapt the examples)
- Setting up the development environment
- Running tests
- Tracking progress against the timeline
- Troubleshooting implementation issues

---

## How These Documents Relate

```
Document 1: DB Architecture (v01)
    ↓ defines schema and overall design
    ├─→ Document 3: Data Mapping (v01)
    │   ↓ shows how to populate the database
    │   └─→ Document 4: Implementation Roadmap (v01)
    │       ↓ provides the actual code to write
    │
    └─→ Document 2: App Transition (v01)
        ↓ shows how to integrate with existing app
        └─→ Document 4: Implementation Roadmap (v01)
            ↓ provides code changes needed
```

**Reading Order:**

1. **Start here:** Document 1 (Database Architecture) → Understand the vision
2. **Then:** Document 3 (Data Mapping) → Understand data flows
3. **Then:** Document 2 (App Transition) → See where changes go
4. **Finally:** Document 4 (Implementation Roadmap) → Write the code

---

## Key Design Principles

### 1. **Zero Breaking Changes**
Every change is additive. Existing code paths remain untouched. If database initialization fails, projects still work normally.

### 2. **Portability**
The SQLite `.db` file travels with the project. Archive it, restore it, move it to another storage system—the database goes with it.

### 3. **Multi-User Collaboration**
Every file change is logged with artist name and timestamp. The database is the source of truth for who did what when.

### 4. **Flexible Storage**
Works with local SSD, NAS, SAN, Lucid Link, or any networked storage. The monitor service syncs the database back to whatever storage system is being used.

### 5. **Metadata Discovery**
The web UI lets you browse archived projects without restoring them. See who worked on what, what files exist, and when changes were made—all without the project files.

---

## Quick Facts

| Aspect | Details |
|--------|---------|
| **Database Type** | SQLite (file-based, no server) |
| **Database Location** | `/PROJEKTS/<PROJECT>/db/<PROJECT>.db` |
| **Database Size** | Typically < 10 MB per project (metadata only) |
| **Storage Agnostic** | Works with local, NAS, SAN, or internet storage |
| **Monitor Service** | Docker container watching project directory |
| **Web UI** | Flask-based API + JavaScript frontend |
| **GUI Changes** | Minimal (status display only) |
| **Backward Compatibility** | 100% (existing projects work as-is) |
| **Migration Path** | Optional tool to add DB to existing projects |
| **Timeline** | 9 weeks, ~110 hours development |
| **Risk Level** | Low (all new code, no modifications to critical paths) |

---

## Technology Stack

### Core
- **Python 3.11+** (3.13 recommended)
- **SQLite3** (builtin, file-based database)
- **PySide6** (`PySide6` package)

### Dependencies (pip)
- `watchdog`
- `ffmpeg-python`
- `Pillow`
- `Flask`

> For exact pinned versions and development tools, see `requirements.txt` (runtime) and `dev-requirements.txt` (development & tests).

### Media Viewers
- **Three.js** (3D model viewing)
- **HTML5 video/audio** (native media players)

---

## Project Scope

### What's Included
✅ SQLite database per project
✅ File monitoring (watchdog)
✅ Metadata tracking (file type, size, artist, timestamp)
✅ Media metadata extraction (images, video, audio)
✅ Audit trail (changelog of all changes)
✅ Multi-user collaboration tracking
✅ Web UI for browsing projects
✅ Archive/restore without file loss
✅ Docker containerization
✅ Migration tool for existing projects
✅ Comprehensive testing

### What's NOT Included (Future Work)
❌ Central PostgreSQL catalog (optional enhancement)
❌ Automated version detection (v01, v02 patterns)
❌ Real-time collaboration notifications
❌ Mobile app
❌ Full-text search
❌ Automatic backup system

---

## Critical Integration Points

### Where Database Gets Initialized
```
src/core/projekt_manager/projekt_creator.py
  └─ create_projekt() function
      └─ At end: calls initialize_projekt_database()
```

### Where Monitor Service Starts
```
src/core/utils/monitor_service_utils.py
  └─ start_monitor_service() function
      └─ Starts Docker container: logik-projekt-monitor
```

### Where GUI Shows Database Status
```
src/ui/panels/projekt_summary_panel.py
  └─ ProjektSummaryPanel class
      └─ update_db_status() method
```

### Where Data Gets Stored
```
projects table       ← Project metadata + creator
files table         ← All files in project
assets table        ← Media-specific metadata
changelog table     ← Audit trail (who, what, when)
relationships table ← File dependencies
tags table          ← Flexible metadata
```

---

## Metrics & Success Criteria

### Performance
- Monitor service response time: < 1 second
- Database query time: < 100ms for typical queries
- Web UI page load: < 2 seconds
- CPU overhead: < 1%

### Reliability
- Database initialization: 100% success rate
- Monitor service uptime: 99.9%
- Data consistency: 100% (no orphaned records)

### Usability
- Zero training required (existing users)
- Optional features (not forced on existing projects)
- Clear error messages if issues occur

### Adoption
- All new projects automatically get databases
- Existing projects can opt-in via migration tool
- Multi-team compatibility (same workflow, enhanced tracking)

---

## Implementation Status

### ✅ Complete (Planning Phase)
- Architecture design
- Schema definition
- Data mapping
- Code examples
- Testing strategy
- Timeline and estimates

### 🔨 Next Steps (Development Phase)
1. Set up development environment
2. Create database manager module
3. Implement database initialization
4. Build file monitor service
5. Create web UI
6. Integrate with GUI
7. Test and refine
8. Document for users

### 📅 Target Timeline
- **Start:** Week 1 (Database initialization)
- **Mid:** Week 5 (Web UI)
- **End:** Week 9 (Testing and documentation)

---

## Decision Points for Teams

### 1. Should we use Docker for monitor service?
**Recommended: YES**
- Isolation from host system
- Easy deployment and scaling
- Simplifies dependency management
- Can run on artist workstations or central server

### 2. Should monitor service be optional?
**Recommended: NO (always run)**
- Ensures complete audit trail
- Minimal overhead
- Starts automatically with project
- Can be disabled if needed

### 3. Should we migrate existing projects automatically?
**Recommended: NO (opt-in)**
- Let teams decide timing
- Provide clear migration tool
- No forced changes

### 4. Should database be required for projects to work?
**Recommended: NO**
- Graceful degradation
- Project works without database
- Database is optional enhancement
- Low risk if something breaks

### 5. Should web UI be served centrally or per-workstation?
**Recommended: Per-workstation**
- No shared infrastructure needed
- Each producer runs their own web UI on port 5000
- Simple deployment (Docker Compose)
- Scales to unlimited projects

---

## Getting Started

### For Decision Makers
1. Read **Document 1: Database Architecture Plan**
2. Review the "Key Design Principles" section above
3. Discuss with team: Does this vision align with our needs?
4. Review "Decision Points for Teams" and make choices

### For Architects
1. Read **Document 1: Database Architecture Plan**
2. Read **Document 3: Data-to-Database Mapping Plan**
3. Review ER diagrams and schema design
4. Discuss data validation and consistency strategy

### For Developers
1. Read **Document 2: App Transition Plan** (understand integration points)
2. Read **Document 4: Implementation Roadmap** (detailed code examples)
3. Set up development environment per checklist
4. Start with Phase 1 (database initialization)

### For QA/Testing
1. Read **Document 4: Implementation Roadmap** (Testing Strategy section)
2. Review test cases for each phase
3. Set up test environment
4. Create test plans for each phase

---

## FAQ

### Q: Will this break existing projects?
**A:** No. All code is additive. Existing projects work without changes. Optional migration tool adds databases to existing projects.

### Q: Can we disable the database?
**A:** Yes. If database initialization fails, projects still work. Monitor service can be disabled/stopped at any time.

### Q: What if an artist is working without internet (offline)?
**A:** The monitor service queues changes locally and syncs when connection returns (future enhancement). For now, works best with consistent connectivity.

### Q: Can we use PostgreSQL instead of SQLite?
**A:** Technically yes, but not recommended. SQLite travels with the project (portability). PostgreSQL would require a server infrastructure.

### Q: How much storage does the database add?
**A:** Minimal. A database for 10,000 files is typically < 5 MB. Scales logarithmically.

### Q: Can we search across all projects?
**A:** Yes (future work: central PostgreSQL catalog). Currently, databases are per-project. Adding a central index would enable global search.

---

## Contact & Support

For questions about this planning package:
- **Architecture questions:** See Document 1
- **Integration questions:** See Document 2
- **Data flow questions:** See Document 3
- **Code questions:** See Document 4
- **General questions:** See this summary document

---

## Document Revision History

| Version | Date | Changes |
|---------|------|---------|
| v01 | 2026-02-08 | Initial planning package created |

---

## Appendix: File Checklist

### Documents (4 files)
- [ ] LOGIK-PROJEKT-DB-PLAN-v01.md
- [ ] LOGIK-PROJEKT-APP-TRANSITION-v01.md
- [ ] LOGIK-PROJEKT-DATA-TO-DB-MAPPING-v01.md
- [ ] LOGIK-PROJEKT-IMPLEMENTATION-ROADMAP-v01.md

### Source Files to Read (Reference)
- [ ] LOGIK-PROJEKT_help_for_devs.md
- [ ] LOGIK-PROJEKT_data_flow_analysis.md
- [ ] app_py_process_flow_analysis.md
- [ ] Various data_map-*.md files

### New Directories to Create
- [ ] `src/core/database_manager/`
- [ ] `logik_projekt_monitor/`
- [ ] `logik_projekt_web/`
- [ ] `tests/unit/`
- [ ] `tests/integration/`

### New Files to Create (Phase 1)
- [ ] `src/core/database_manager/__init__.py`
- [ ] `src/core/database_manager/db_schema.py`
- [ ] `src/core/database_manager/db_operations.py`
- [ ] `src/core/database_manager/db_metadata_extractor.py`
- [ ] `src/core/utils/monitor_service_utils.py`
- [ ] `src/core/utils/migration_utils.py`

---

**Ready to start implementation? Begin with Document 1, then proceed to Document 4.**

