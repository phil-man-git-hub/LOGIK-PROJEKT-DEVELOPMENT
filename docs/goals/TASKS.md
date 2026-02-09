# SQLite Integration — TASKS

**Generated:** 2026-02-09
**Purpose:** Actionable task list derived from the Planning Package (v01) to guide development, testing, and rollout.

---

## Quick Summary ✅
- Goal: Add a per-project SQLite DB, a file monitor service, and a web UI for browsing project metadata.
- Timeline (from planning): 9 weeks total; immediate work starts with **Phase 1: Schema & Initialization**.

---

## How to use this file
- Pick a task, set `assignee`, and move it to your project board (or `TO-DO.md`).
- Tasks are grouped by phase and prioritized; each has acceptance criteria and rough estimates.

---

## Global Pre-reqs (Do first)
- [ ] Create feature branch `feature/sqlite-database-integration` (Est: 0.5d) — Priority: High
- [ ] Ensure dev environment: run `bash bin/setup-venv-3.13.3.sh` and `pip install -r requirements.txt` (Est: 0.25d) — Priority: High
- [ ] Add dependencies to `requirements.txt` (`watchdog`, `ffmpeg-python`, `Pillow`) and `dev-requirements.txt` (pytest, tox) (Est: 0.25d)

---

## Phase 1 — Core Infrastructure (Week 1) 🔧 (Priority: High)
Objective: Create DB schema & initialization, add tests and safe call in `projekt_creator`.

Tasks:
1. Create module `src/core/database_manager/` (Est: 0.5d)
   - Files: `__init__.py`, `db_schema.py`, `db_operations.py`, `db_metadata_extractor.py`
   - Acceptance: `initialize_projekt_database()` creates DB at `PROJECT/db/<PROJECT>.db` with tables and indexes.
2. Implement `initialize_projekt_database()` (Est: 1d)
   - Insert initial `projects` row and changelog entry.
   - Acceptance: Unit test `tests/test_db_schema.py` passes.
3. Add tests for schema and initialization (Est: 0.5d)
   - Tests: `tests/test_db_schema.py` and `tests/test_db_operations.py`.
4. Update `src/core/projekt_manager/projekt_creator.py` to call DB init (non-fatal on error) (Est: 0.25d)
   - Acceptance: Creating a project produces `db/<PROJECT>.db` and no regression in existing behavior.
5. CI job: run DB schema tests in CI (Est: 0.5d)

Dependencies: None outside repo.

---

## Phase 2 — File Monitoring Service (Week 2-3) 🚨 (Priority: High)
Objective: Watch project dirs for file changes, update DB, generate thumbnails/hashes.

Tasks:
1. Create `logik_projekt_monitor/` (Est: 1.5d)
   - Files: `monitor_service.py`, `Dockerfile`, `README.md` for usage
   - Acceptance: `monitor_service.py` can add/modify/delete `files` and `changelog` entries in DB.
2. Integrate `watchdog` and file hashing logic (Est: 1d)
3. Media metadata extraction & thumbnails (Est: 1.5d)
   - Use `ffmpeg-python` and `Pillow`.
   - Acceptance: `assets` table populated with width/height/duration/frame_rate and thumbnail path.
4. Add monitor start/stop helpers in `src/core/utils/monitor_service_utils.py` (Est: 0.5d)
5. Create integration tests that run monitor on a temp project and assert DB updates (Est: 1d)
6. Dockerize and add to `docker-compose.yml` (Est: 0.5d)

Dependencies: Phase 1 (DB schema) must be complete.

---

## Phase 3 — Web UI: Browse (Week 4-5) 🌐 (Priority: Medium)
Objective: Provide project browsing (tree, metadata list, viewers).

Tasks:
1. Create `logik_projekt_web/` skeleton (Est: 0.5d)
   - Files: `app.py`, `Dockerfile`, `templates/index.html`, `static/js/*`, `static/css/*`
2. Implement backend endpoints for: project summary, file list, file metadata, changelog (Est: 1.5d)
3. Basic frontend: directory tree, file list, image & video playback (Est: 2d)
4. Integration tests for API endpoints and UI smoke tests (Est: 1d)
5. Dockerize and add to `docker-compose.yml` (Est: 0.5d)

Dependencies: Phase 1 & 2 must be available (DB and monitor service producing data).

---

## Phase 4 — Web UI: Advanced Features (Week 6-8) ⚡ (Priority: Low→Medium)
Objective: 3D model viewer, relationship graphs, search, tags management.

Tasks:
1. Add 3D viewer support (glTF + Three.js) (Est: 2d)
2. Implement relationship/graph endpoints and UI (Est: 2d)
3. Add search & filter (server-side indexing, simple queries) (Est: 1.5d)
4. Tagging UI & server endpoints (Est: 1d)
5. Tests: API + UI behavior (Est: 1.5d)

Dependencies: Phase 3 complete.

---

## Migration & Utilities
- [ ] `src/core/utils/migration_utils.py` (Est: 1d) — migration tools for existing projects (opt-in)
  - Acceptance: Scans a project and populates DB without modifying original files.
- [ ] Add `tests/integration/test_migration.py` (Est: 1d)

---

## Testing / QA (continuous)
- Unit tests for each module (schema, operations, monitor internals) — High priority
- Integration tests that run monitor + inspect DB — High priority
- End-to-end tests that create a project, add files, and browse via web UI — Medium priority
- Define acceptance test checklist (Performance: DB query <100ms for typical queries; Monitor latency <1s)

---

## Dev & Ops Tasks
- Add `docker-compose.yml` entries for `logik-projekt-app`, `logik-projekt-monitor`, and `logik-projekt-web` — (Est: 0.5d)
- Add logging & telemetry hooks for monitor and web (Est: 0.5d)
- Add backup/example script: `tools/backup_db.py` (Est: 0.5d)

---

## Documentation & Onboarding
- Update `docs/goals/LOGIK-PROJEKT-PLANNING-PACKAGE-INDEX-v01.md` with: Developer Quick Start & links to TASKS.md — (Est: 0.25d) ✅
- Add README for `logik_projekt_monitor/` and `logik_projekt_web/` — (Est: 0.25d)
- Add `docs/goals/TASKS.md` link to project README — (Est: 0.1d)

---

## Acceptance Criteria (Summary)
- Database initializes for all new projects without breaking existing functionality.
- Monitor service reliably inserts/modifies/removes `files` and `changelog` records on file events.
- Web UI surfaces project metadata and supports basic media viewing.
- All critical tests pass in CI and performance goals are met (see planning doc metrics).

---

## Suggested Next Action (pick one)
- Start **Phase 1** and create a branch `feature/sqlite-database-integration` (Recommended). ✅
- Or, assign tasks to team members and create issues in your tracker for each task above.

---

For questions or to assign tasks, add comments in this file or open issues prefixed with `[sqlite-integration]`.
