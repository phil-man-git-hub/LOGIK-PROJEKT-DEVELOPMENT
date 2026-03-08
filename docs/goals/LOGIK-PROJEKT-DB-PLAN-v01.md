# LOGIK-PROJEKT Database Architecture Plan (v01)

## Executive Summary

Enhance LOGIK-PROJEKT from file/JSON/XML-based metadata to a lightweight SQLite database per project, enabling:
- Structured metadata and relationship tracking
- Multi-user distributed collaboration across global teams
- Project portability (archive/restore without losing metadata)
- Web-based browsing of project structure, media assets, and relationships
- Graceful handling of internet storage backends (Lucid Link, NAS, SAN, USB)

---

## 1. Current State

### Existing Strengths
- Directory-per-project organization (`/PROJEKTS/<YYYY_MM_DD-PROJECT_NAME>/`)
- Storage backend agnostic (`/PROJEKTS` as symbolic link)
- Project portability (move to USB, S3, Lucid Link, etc.)
- Simple, file-based approach with JSON/XML/shell/Python configs

### Limitations
- Metadata scattered across multiple file formats
- No relationship/dependency tracking
- Difficult to query project structure without parsing files
- No built-in multi-user change tracking
- Archived projects are opaque (can't browse metadata without restoring)

---

## 2. Proposed Architecture

### 2.1 Storage Layer

```
/PROJEKTS/<YYYY_MM_DD-PROJECT_NAME>/
├── db/
│   └── <YYYY_MM_DD-PROJECT_NAME>.db          (SQLite database - portable)
├── assets/                                      (project files/media)
│   ├── footage/
│   ├── images/
│   ├── audio/
│   ├── 3d_models/
│   └── ...
├── renders/
├── metadata/                                    (legacy? or consolidate to DB?)
└── ...
```

**Key Design Decisions:**
- **One SQLite database per project** (travels with the project)
- **Database stored in project directory** (not in central PostgreSQL)
- **Project files remain on storage backend** (Lucid Link, NAS, etc.)
- **Database is relatively small** (metadata only, not media files)

---

### 2.2 Deployment Architecture

```
Producer Workstation (Linux/macOS/Windows)
├── Docker
│   ├── logik-projekt-app (main application)
│   │   ├── Read/write access to /PROJEKTS (volume mount)
│   │   ├── Local cache for SQLite DB (/local_cache)
│   │   └── Runs project operations
│   │
│   └── logik-projekt-monitor (file watcher service)
│       ├── Monitors /PROJEKTS/<PROJECT>/ for changes
│       ├── Updates <PROJECT>.db on file changes
│       └── Syncs DB back to storage
│
└── Storage Backend
    ├── Local SSD/NAS
    ├── Lucid Link (internet storage)
    ├── SAN / DAS (direct attached)
    └── USB / Archive (portable)
```

---

### 2.3 Multi-User Collaboration Flow

```
Scenario: Producer creates project, Flame Artist adds media in another country

1. Producer Workstation (Country A)
   └─→ Creates /PROJEKTS/2026_02_08-MY_NEW_PROJEKT/
       └─→ Initializes 2026_02_08-MY_NEW_PROJEKT.db (empty schema)
       └─→ Data syncs to Lucid Link

2. Flame Artist Workstation (Country B)
   └─→ Mounts /PROJEKTS from Lucid Link
   └─→ Runs: logik-projekt-app --project 2026_02_08-MY_NEW_PROJEKT
   └─→ Adds files: renders/, footage/, images/, audio/
   └─→ Monitor service detects changes
   └─→ Monitor updates 2026_02_08-MY_NEW_PROJEKT.db
       └─→ INSERT file metadata (path, size, hash, artist, timestamp, etc.)
   └─→ DB syncs back to Lucid Link

3. Producer Workstation (Later)
   └─→ Pulls latest 2026_02_08-MY_NEW_PROJEKT.db from Lucid Link
   └─→ Sees all Flame Artist's changes in DB
   └─→ Can browse metadata/structure via web UI
   └─→ Can restore full project data if needed
```

---

## 3. SQLite Database Schema (Proposed)

### 3.1 Core Tables

```sql
-- Projects metadata
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT UNIQUE NOT NULL,
    created_by TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    status TEXT                    -- 'active', 'archived', 'completed'
);

-- File registry
CREATE TABLE files (
    file_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    relative_path TEXT NOT NULL,   -- path relative to project root
    absolute_path TEXT,            -- for convenience
    file_size INTEGER,
    file_hash TEXT,                -- MD5/SHA256 for integrity
    mime_type TEXT,
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    artist_name TEXT,              -- who created/modified
    file_type TEXT,                -- 'image', 'video', 'audio', '3d_model', 'document', etc.
    FOREIGN KEY(project_id) REFERENCES projects(project_id)
);

-- Asset metadata (images, video, audio, 3D)
CREATE TABLE assets (
    asset_id INTEGER PRIMARY KEY,
    file_id INTEGER NOT NULL,
    asset_type TEXT,               -- 'image', 'video', 'audio', '3d_model'
    duration REAL,                 -- for video/audio (seconds)
    width INTEGER, height INTEGER, -- for images/video
    frame_rate REAL,               -- for video
    color_space TEXT,              -- 'rec709', 'acescc', etc.
    thumbnail_path TEXT,           -- relative path to thumbnail
    metadata JSON,                 -- flexible metadata storage
    FOREIGN KEY(file_id) REFERENCES files(file_id)
);

-- Relationships/dependencies
CREATE TABLE relationships (
    relationship_id INTEGER PRIMARY KEY,
    source_file_id INTEGER NOT NULL,
    target_file_id INTEGER NOT NULL,
    relationship_type TEXT,        -- 'depends_on', 'input_to', 'output_of', 'version_of'
    notes TEXT,
    FOREIGN KEY(source_file_id) REFERENCES files(file_id),
    FOREIGN KEY(target_file_id) REFERENCES files(file_id)
);

-- Change log (who did what when)
CREATE TABLE changelog (
    change_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    file_id INTEGER,
    artist_name TEXT,
    change_type TEXT,              -- 'created', 'modified', 'deleted', 'moved'
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSON,
    FOREIGN KEY(project_id) REFERENCES projects(project_id),
    FOREIGN KEY(file_id) REFERENCES files(file_id)
);

-- Tags/annotations
CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY,
    file_id INTEGER NOT NULL,
    tag_name TEXT,
    tag_value TEXT,
    FOREIGN KEY(file_id) REFERENCES files(file_id)
);
```

---

## 4. Components & Services

### 4.1 logik-projekt-app (Main Application)

**Responsibilities:**
- Orchestrate project operations
- Read/write project files
- Commit metadata to SQLite DB
- Serve web UI for browsing
- Manage project lifecycle (create, archive, restore)

**Interfaces:**
- CLI for project operations
- Web API/UI for metadata browsing
- Docker volume mount to `/PROJEKTS`
- SQLite connection to local `.db` file

**Technology Stack:**
- Python (Flask/FastAPI)
- SQLite3 (via Python's sqlite3 module)
- Jinja2 templates (web UI)
- Optional: Gunicorn/uWSGI for serving

---

### 4.2 logik-projekt-monitor (File Watcher Service)

**Responsibilities:**
- Watch `/PROJEKTS/<PROJECT>/` for file changes
- Detect: new files, modifications, deletions, moves
- Update SQLite DB with file metadata
- Calculate file hashes for integrity
- Generate thumbnails (for images/video)
- Sync DB back to storage backend
- Handle conflicts (last-write-wins or merge strategies)

**Interfaces:**
- File system watcher (watchdog library)
- SQLite connection
- Optional: rsync/S3 sync for DB persistence

**Technology Stack:**
- Python (watchdog library)
- SQLite3
- ffmpeg/Pillow (for thumbnails, metadata extraction)
- Optional: rsync, boto3 (for S3)

---

### 4.3 Web UI / Browser

**Features:**
- Browse project directory structure
- View file metadata (size, artist, date, hash)
- Image viewer (with thumbnails)
- Video player (HTML5, with frame info)
- Audio player with waveform
- 3D model viewer (Three.js/Babylon.js for glTF/converted FBX)
- Relationship/dependency graph visualization
- Changelog/history view
- Search & filter by file type, artist, date, tags

**Technology Stack:**
- Frontend: HTML5, CSS, JavaScript (React or vanilla)
- Media viewers: Three.js, Babylon.js, HLS.js
- Backend: Flask/FastAPI serving static + API endpoints

---

## 5. Workflow Examples

### 5.1 Producer Creates New Project

```bash
$ docker run logik-projekt-app \
    --mode create \
    --project 2026_02_08-MY_NEW_PROJEKT \
    --storage /PROJEKTS

# Result:
# /PROJEKTS/2026_02_08-MY_NEW_PROJEKT/
#   ├── db/2026_02_08-MY_NEW_PROJEKT.db (empty, initialized)
#   ├── assets/
#   ├── renders/
#   └── ...

# DB is then synced to Lucid Link (or NAS, etc.)
```

---

### 5.2 Flame Artist Adds Media

```bash
# On Flame Artist's workstation
$ docker run logik-projekt-app \
    --mode work \
    --project 2026_02_08-MY_NEW_PROJEKT \
    --storage /PROJEKTS \
    --artist "Flame Artist Name"

# Flame Artist adds files:
# /PROJEKTS/2026_02_08-MY_NEW_PROJEKT/renders/shot_001_v01.exr
# /PROJEKTS/2026_02_08-MY_NEW_PROJEKT/renders/shot_001_v02.exr
# /PROJEKTS/2026_02_08-MY_NEW_PROJEKT/footage/source_clip_001.mov

# Monitor service detects changes:
# - Calculates file hashes
# - Extracts metadata (duration, resolution, color space)
# - Generates thumbnails
# - INSERTs into files table
# - INSERTs into changelog table
# - Syncs .db back to Lucid Link

# Producer later syncs DB and sees:
# SELECT * FROM files WHERE artist_name = 'Flame Artist Name';
# SELECT * FROM changelog ORDER BY change_date DESC;
```

---

### 5.3 Producer Archives & Restores Project

```bash
# Archive (move to S3 Deep Archive or USB)
$ docker run logik-projekt-app \
    --mode archive \
    --project 2026_02_08-MY_NEW_PROJEKT \
    --destination s3://my-archive/2026_02_08-MY_NEW_PROJEKT.tar.gz

# Result: Entire directory + .db file compressed and uploaded
# /PROJEKTS/2026_02_08-MY_NEW_PROJEKT/ can now be deleted to save space

# Later: Restore from archive
$ docker run logik-projekt-app \
    --mode restore \
    --project 2026_02_08-MY_NEW_PROJEKT \
    --source s3://my-archive/2026_02_08-MY_NEW_PROJEKT.tar.gz

# Result: /PROJEKTS/2026_02_08-MY_NEW_PROJEKT/ restored with all files + DB
```

---

### 5.4 Browse Archived Project Metadata (No Files)

```bash
# Without restoring full project, browse metadata via web UI
$ docker run logik-projekt-web \
    --mode browse-archive \
    --db-path /local/path/to/2026_02_08-MY_NEW_PROJEKT.db

# Web UI queries DB to show:
# - File structure
# - Thumbnails (embedded in DB or cached locally)
# - Changelog (who did what)
# - Relationships
# - Search

# User can decide: "Yes, restore this" or "No, delete archive"
```

---

## 6. Technology Stack (Proposed)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Database** | SQLite | Portable, file-based, travels with project, no server |
| **Backend** | Python + Flask/FastAPI | Lightweight, good SQLite support, easy to containerize |
| **File Monitoring** | watchdog (Python) | Cross-platform, reliable file system events |
| **Thumbnails** | Pillow, ffmpeg | Standard tools for image/video processing |
| **Web UI** | HTML5/CSS/JavaScript + React | Modern, responsive, no build step required (or minimal) |
| **3D Viewers** | Three.js or Babylon.js | Supports glTF (convert FBX/Alembic to glTF) |
| **Containerization** | Docker | Consistent across producer, artists, archival |
| **Storage Sync** | rsync, rclone, or boto3 | Flexible, supports multiple backends |

---

## 7. Implementation Phases

### Phase 1: Core Infrastructure (Weeks 1-2)
- [ ] Define SQLite schema (finalize tables, indexes)
- [ ] Create logik-projekt-app skeleton (Flask app, DB initialization)
- [ ] Implement file monitoring service (watchdog integration)
- [ ] Basic CLI: create project, initialize DB
- [ ] Docker setup for both services

### Phase 2: Data Layer (Weeks 3-4)
- [ ] Implement file registry (INSERT/UPDATE/DELETE files)
- [ ] Asset metadata extraction (ffmpeg, Pillow for media)
- [ ] Changelog tracking (who did what)
- [ ] File hash calculation (MD5/SHA256)
- [ ] Thumbnail generation

### Phase 3: Web UI - Browse (Weeks 5-6)
- [ ] Basic web UI (Flask templates or React)
- [ ] Directory tree viewer
- [ ] File list with metadata
- [ ] Image viewer
- [ ] Video player (HTML5)
- [ ] Audio player

### Phase 4: Web UI - Advanced (Weeks 7-8)
- [ ] 3D model viewer (Three.js/glTF)
- [ ] Relationship/dependency visualization
- [ ] Changelog browser
- [ ] Search & filter
- [ ] Tag management

### Phase 5: Archive/Restore (Weeks 9-10)
- [ ] Archive workflow (tar/compress + upload)
- [ ] Restore workflow (download + extract)
- [ ] Archive metadata browser (without full restore)
- [ ] Storage backend integration (S3, Lucid Link, rsync)

### Phase 6: Multi-User & Sync (Weeks 11-12)
- [ ] Conflict resolution strategy (last-write-wins, merge)
- [ ] DB sync mechanisms between workstations
- [ ] Change notification system
- [ ] Testing with multiple artists

### Phase 7: Polish & Testing (Weeks 13+)
- [ ] Performance optimization
- [ ] Error handling & recovery
- [ ] Documentation
- [ ] Beta testing with real workflows

---

## 8. Open Questions & Decisions

1. **Schema finalization**: Should we add more tables? (versions, approvals, annotations?)
2. **Thumbnail strategy**: Embed in DB (BLOB) or store as separate files?
3. **3D model conversion**: Auto-convert FBX/Alembic to glTF, or require pre-conversion?
4. **Conflict resolution**: Last-write-wins vs. merge vs. manual resolution?
5. **Change notifications**: Should monitor service notify other workstations of changes?
6. **Performance**: Index strategy for large projects (100k+ files)?
7. **Backwards compatibility**: How to migrate existing LOGIK-PROJEKT projects to SQLite?
8. **Central catalog**: Should we add optional PostgreSQL for global project search across multiple archived projects?

---

## 9. Success Criteria

- [ ] Single SQLite file per project that travels with the project
- [ ] Multi-user collaboration without file locking issues
- [ ] Web UI to browse project metadata + media
- [ ] Archive/restore without losing metadata
- [ ] Support for Lucid Link, NAS, SAN, USB storage backends
- [ ] Performance acceptable for projects with 10k+ files
- [ ] Docker-based, works on Linux/macOS/Windows producer workstations
- [ ] Flame artists can add media without conflicts

---

## Notes & References

- SQLite limitations with network filesystems: https://www.sqlite.org/howtocorrupt.html
- Watchdog library: https://github.com/gorakhargosh/watchdog
- Three.js / Babylon.js for 3D viewing
- FBX to glTF conversion tools (FBX2glTF, Babylon.js exporter)

---

**Version History**
- v01 (2026-02-08): Initial high-level plan created

