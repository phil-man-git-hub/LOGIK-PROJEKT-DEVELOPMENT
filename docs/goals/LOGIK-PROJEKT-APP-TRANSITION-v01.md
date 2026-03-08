# LOGIK-PROJEKT App Transition Plan (v01)

## Executive Summary

This document outlines how the existing LOGIK-PROJEKT PySide6 GUI application will transition to integrate with the new SQLite database architecture, file monitoring services, and web-based browsing capabilities described in the Database Architecture Plan (v01).

The current application is well-architected and will serve as the **producer workstation interface** for creating and managing projects. The transition maintains backward compatibility while adding new capabilities for multi-user collaboration, metadata tracking, and project portability.

---

## 1. Current Application State (As-Is)

### 1.1 Architecture Overview

```
PySide6 GUI Application (Producer Workstation)
├── app.py (Entry point, QApplication/QMainWindow setup)
├── src/ui/
│   ├── app_window.py (Main UI widget, panel orchestration, Worker thread)
│   ├── panels/ (Individual input/display panels)
│   │   ├── template_info_panel.py
│   │   ├── template_parameters_panel.py
│   │   ├── flame_options_panel.py
│   │   ├── projekt_template_panel.py
│   │   ├── template_summary_panel.py
│   │   └── projekt_summary_panel.py
│   ├── widgets/ (Reusable UI components)
│   └── themes/ (Styling)
├── src/core/
│   ├── app_logic.py (Business logic facade)
│   ├── projekt_manager/
│   │   ├── projekt_creator.py (Creates projects/file structures)
│   │   └── projekt_models.py
│   ├── template_manager/
│   │   ├── template_handler.py (Import/export templates)
│   │   ├── template_models.py
│   │   └── template_serializers.py
│   ├── functions/ (Utility functions organized by purpose)
│   │   ├── copy/ (Copy Flame configs, bookmarks, scripts)
│   │   ├── create/ (Create dirs, scripts, symbolic links, DB)
│   │   ├── get/ (Retrieve configs, paths, Flame versions)
│   │   └── io/ (Export/import templates and session data)
│   └── utils/ (General utilities: logging, validation, paths)
└── /PROJEKTS/ (Projects root directory, symbolic link)
    └── <YYYY_MM_DD-PROJECT_NAME>/
        ├── assets/
        ├── renders/
        └── ... (other project directories)
```

### 1.2 Current Workflow

1. **Producer** opens PySide6 GUI on workstation
2. **Input panels** collect project metadata (template info, Flame options, resolution, etc.)
3. **Summary panels** display consolidated project configuration
4. **User clicks "Create PROJEKT"**
5. **Worker thread** executes `projekt_creator.create_projekt()`
6. **Project is created** in `/PROJEKTS/<YYYY_MM_DD-PROJECT_NAME>/` with:
   - Directory structure (assets, renders, etc.)
   - Flame configuration files (wiretap nodes, startup scripts, etc.)
   - PostgreSQL database (via `create_projekt_pgsql_db.py`)
   - Flame archive script, launcher alias, etc.
7. **No metadata database** — project structure is in files/directories only

### 1.3 Strengths

- Clean separation of concerns (UI, logic, utilities)
- Multi-threaded operation (Worker thread prevents UI freezing)
- Modular UI panels (easy to add/modify components)
- Comprehensive project creation logic
- Thread-safe logging
- Well-documented codebase

### 1.4 Limitations (For New Features)

- No structured metadata database per project
- No file monitoring/change tracking
- No multi-user collaboration tracking
- No web-based project browsing
- No archived project metadata inspection
- Limited ability to query project structure without parsing files

---

## 2. Target Architecture (To-Be)

### 2.1 Enhanced Application Structure

```
Enhanced LOGIK-PROJEKT Ecosystem
├── Producer Workstation (PySide6 GUI + Docker)
│   ├── logik-projekt-app (Docker container)
│   │   ├── app.py (Enhanced entry point)
│   │   ├── src/ui/ (UI panels - largely unchanged)
│   │   ├── src/core/ (Core logic - enhanced with SQLite integration)
│   │   │   ├── projekt_manager/
│   │   │   │   ├── projekt_creator.py (UPDATED: Initialize SQLite DB)
│   │   │   │   └── projekt_models.py
│   │   │   ├── database_manager/ (NEW)
│   │   │   │   ├── db_schema.py (NEW: Database schema, migrations)
│   │   │   │   ├── db_operations.py (NEW: CRUD operations)
│   │   │   │   └── db_metadata_extractor.py (NEW: Extract metadata from files)
│   │   │   └── ... (existing utils, functions)
│   │   └── volume mounts: /PROJEKTS, /local_cache
│   │
│   └── logik-projekt-monitor (Docker container - NEW)
│       ├── monitor_service.py (NEW: File watcher)
│       ├── watchdog config
│       └── volume mounts: /PROJEKTS, /local_cache
│
├── Artist Workstations (Linux/macOS/Windows)
│   └── logik-projekt-monitor (runs locally or via Docker)
│       └── Detects file changes, updates SQLite DB
│
└── Web Browser Interface (NEW)
    ├── logik-projekt-web (Docker container)
    │   ├── Flask/FastAPI backend
    │   ├── SQLite database connection
    │   └── static assets (HTML/CSS/JS)
    └── User can browse:
        ├── Project structure / file tree
        ├── Media files with thumbnails
        ├── Video/audio playback
        ├── 3D model viewing
        ├── Changelog/history
        └── Metadata / relationships
```

### 2.2 Key Additions

| Component | Type | Purpose |
|-----------|------|---------|
| `database_manager/` | Python module | SQLite operations, schema, migrations |
| `logik-projekt-monitor` | Docker service | File system watcher + DB updates |
| `logik-projekt-web` | Docker service | Web UI for browsing projects |
| `local_cache/` | Volume mount | Local SQLite copy (for internet storage sync) |
| Project `.db` file | File | Per-project metadata (travels with project) |

---

## 3. Detailed Transition Plan

### 3.1 Phase 1: SQLite Integration into projekt_creator.py

**Objective:** When a project is created, initialize SQLite database alongside existing file structure.

**Changes to `src/core/projekt_manager/projekt_creator.py`:**

```python
# EXISTING CODE (unchanged)
def create_projekt(...):
    """Creates project directory structure, Flame configs, etc."""
    # ... existing logic for directory creation, Flame setup, etc.

# NEW CODE (additions)
    # After all existing directory creation, initialize SQLite DB
    db_path = os.path.join(project_root, 'db', f'{project_name}.db')
    initialize_projekt_database(project_root, db_path, creator_name)
```

**New Module: `src/core/database_manager/db_schema.py`**

```python
import sqlite3
from pathlib import Path

def initialize_projekt_database(project_root: str, db_path: str, creator_name: str):
    """
    Initialize a new SQLite database for a project.
    
    Args:
        project_root: Root directory of the project
        db_path: Full path to the .db file
        creator_name: Name of the user creating the project
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create all tables (from Database Architecture Plan v01)
    cursor.executescript("""
        CREATE TABLE projects (
            project_id INTEGER PRIMARY KEY,
            project_name TEXT UNIQUE NOT NULL,
            created_by TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            status TEXT DEFAULT 'active'
        );
        
        CREATE TABLE files (
            file_id INTEGER PRIMARY KEY,
            project_id INTEGER NOT NULL,
            relative_path TEXT NOT NULL,
            absolute_path TEXT,
            file_size INTEGER,
            file_hash TEXT,
            mime_type TEXT,
            created_date TIMESTAMP,
            modified_date TIMESTAMP,
            artist_name TEXT,
            file_type TEXT,
            FOREIGN KEY(project_id) REFERENCES projects(project_id)
        );
        
        CREATE TABLE assets (
            asset_id INTEGER PRIMARY KEY,
            file_id INTEGER NOT NULL,
            asset_type TEXT,
            duration REAL,
            width INTEGER,
            height INTEGER,
            frame_rate REAL,
            color_space TEXT,
            thumbnail_path TEXT,
            metadata JSON,
            FOREIGN KEY(file_id) REFERENCES files(file_id)
        );
        
        CREATE TABLE relationships (
            relationship_id INTEGER PRIMARY KEY,
            source_file_id INTEGER NOT NULL,
            target_file_id INTEGER NOT NULL,
            relationship_type TEXT,
            notes TEXT,
            FOREIGN KEY(source_file_id) REFERENCES files(file_id),
            FOREIGN KEY(target_file_id) REFERENCES files(file_id)
        );
        
        CREATE TABLE changelog (
            change_id INTEGER PRIMARY KEY,
            project_id INTEGER NOT NULL,
            file_id INTEGER,
            artist_name TEXT,
            change_type TEXT,
            change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details JSON,
            FOREIGN KEY(project_id) REFERENCES projects(project_id),
            FOREIGN KEY(file_id) REFERENCES files(file_id)
        );
        
        CREATE TABLE tags (
            tag_id INTEGER PRIMARY KEY,
            file_id INTEGER NOT NULL,
            tag_name TEXT,
            tag_value TEXT,
            FOREIGN KEY(file_id) REFERENCES files(file_id)
        );
    """)
    
    # Insert initial project record
    cursor.execute("""
        INSERT INTO projects (project_name, created_by, description, status)
        VALUES (?, ?, ?, 'active')
    """, (Path(project_root).name, creator_name, "Auto-created project database"))
    
    conn.commit()
    conn.close()
```

**Impact:** Minimal. Existing `projekt_creator.py` logic unchanged; new function called at end.

---

### 3.2 Phase 2: File Monitoring Service (logik-projekt-monitor)

**Objective:** Run as a Docker service (or locally) to detect file changes and update SQLite DB.

**New Component: `logik_projekt_monitor/` directory**

```python
# logik_projekt_monitor/monitor_service.py

import sqlite3
import os
import hashlib
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ProjectMonitor(FileSystemEventHandler):
    """Monitors project directory for file changes, updates SQLite DB."""
    
    def __init__(self, project_root: str, db_path: str, artist_name: str):
        self.project_root = project_root
        self.db_path = db_path
        self.artist_name = artist_name
        self.project_id = self._get_project_id()
    
    def on_created(self, event):
        if not event.is_directory:
            self._add_file(event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            self._update_file(event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self._delete_file(event.src_path)
    
    def _add_file(self, filepath: str):
        """Add a new file to the database."""
        try:
            rel_path = os.path.relpath(filepath, self.project_root)
            file_size = os.path.getsize(filepath)
            file_hash = self._calculate_hash(filepath)
            mime_type = self._detect_mime_type(filepath)
            file_type = self._detect_file_type(mime_type)
            now = datetime.utcnow().isoformat()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO files (
                    project_id, relative_path, absolute_path, file_size, file_hash,
                    mime_type, created_date, modified_date, artist_name, file_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.project_id, rel_path, filepath, file_size, file_hash,
                mime_type, now, now, self.artist_name, file_type
            ))
            
            # Log the change
            cursor.execute("""
                INSERT INTO changelog (
                    project_id, file_id, artist_name, change_type, change_date, details
                ) VALUES (
                    ?, last_insert_rowid(), ?, 'created', ?, json('{}')
                )
            """, (self.project_id, self.artist_name, now))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error adding file {filepath}: {e}")
    
    def _update_file(self, filepath: str):
        """Update file metadata if it's already in the database."""
        try:
            rel_path = os.path.relpath(filepath, self.project_root)
            file_size = os.path.getsize(filepath)
            file_hash = self._calculate_hash(filepath)
            now = datetime.utcnow().isoformat()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if file exists
            cursor.execute(
                "SELECT file_id FROM files WHERE project_id = ? AND relative_path = ?",
                (self.project_id, rel_path)
            )
            result = cursor.fetchone()
            
            if result:
                file_id = result[0]
                cursor.execute("""
                    UPDATE files SET file_size = ?, file_hash = ?, modified_date = ?
                    WHERE file_id = ?
                """, (file_size, file_hash, now, file_id))
                
                cursor.execute("""
                    INSERT INTO changelog (
                        project_id, file_id, artist_name, change_type, change_date, details
                    ) VALUES (?, ?, ?, 'modified', ?, json('{}'))
                """, (self.project_id, file_id, self.artist_name, now))
                
                conn.commit()
            
            conn.close()
            
        except Exception as e:
            print(f"Error updating file {filepath}: {e}")
    
    def _delete_file(self, filepath: str):
        """Mark file as deleted in the database."""
        try:
            rel_path = os.path.relpath(filepath, self.project_root)
            now = datetime.utcnow().isoformat()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT file_id FROM files WHERE project_id = ? AND relative_path = ?",
                (self.project_id, rel_path)
            )
            result = cursor.fetchone()
            
            if result:
                file_id = result[0]
                cursor.execute(
                    "DELETE FROM files WHERE file_id = ?",
                    (file_id,)
                )
                
                cursor.execute("""
                    INSERT INTO changelog (
                        project_id, file_id, artist_name, change_type, change_date, details
                    ) VALUES (?, ?, ?, 'deleted', ?, json('{}'))
                """, (self.project_id, file_id, self.artist_name, now))
                
                conn.commit()
            
            conn.close()
            
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")
    
    def _get_project_id(self) -> int:
        """Retrieve project_id from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT project_id FROM projects LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 1
    
    def _calculate_hash(self, filepath: str) -> str:
        """Calculate SHA256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _detect_mime_type(self, filepath: str) -> str:
        """Detect MIME type of file."""
        import mimetypes
        mime, _ = mimetypes.guess_type(filepath)
        return mime or "application/octet-stream"
    
    def _detect_file_type(self, mime_type: str) -> str:
        """Categorize file type based on MIME type."""
        if mime_type.startswith("image/"):
            return "image"
        elif mime_type.startswith("video/"):
            return "video"
        elif mime_type.startswith("audio/"):
            return "audio"
        elif "json" in mime_type or "xml" in mime_type:
            return "config"
        else:
            return "other"


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Project root directory")
    parser.add_argument("--db", required=True, help="Path to SQLite DB file")
    parser.add_argument("--artist", default="Unknown", help="Artist name")
    args = parser.parse_args()
    
    observer = Observer()
    monitor = ProjectMonitor(args.project, args.db, args.artist)
    observer.schedule(monitor, path=args.project, recursive=True)
    observer.start()
    
    try:
        while True:
            observer.join(timeout=1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

**Docker Setup:**

```dockerfile
# logik_projekt_monitor/Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN pip install watchdog

COPY monitor_service.py /app/

VOLUME ["/PROJEKTS"]

ENV ARTIST_NAME="Monitor Service"

CMD ["python", "/app/monitor_service.py", \
     "--project", "/PROJEKTS/${PROJECT_NAME}", \
     "--db", "/PROJEKTS/${PROJECT_NAME}/db/${PROJECT_NAME}.db", \
     "--artist", "${ARTIST_NAME}"]
```

**Usage:**

```bash
# On Flame artist's workstation
docker run -d \
  -v /PROJEKTS:/PROJEKTS \
  -e PROJECT_NAME="2026_02_08-MY_NEW_PROJEKT" \
  -e ARTIST_NAME="Flame Artist Name" \
  logik-projekt-monitor
```

**Impact:** New component, doesn't affect existing code.

---

### 3.3 Phase 3: Web UI for Project Browsing (logik-projekt-web)

**Objective:** Provide web-based interface to browse project metadata, media files, and relationships.

**New Component: `logik_projekt_web/` directory**

```python
# logik_projekt_web/app.py (Flask backend)

from flask import Flask, jsonify, render_template, send_file
import sqlite3
import json
from pathlib import Path

app = Flask(__name__)

@app.route('/api/projects/<project_name>')
def get_project_metadata(project_name):
    """Return project metadata from SQLite DB."""
    db_path = f"/PROJEKTS/{project_name}/db/{project_name}.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM projects WHERE project_name = ?", (project_name,))
    project = dict(cursor.fetchone())
    
    cursor.execute("SELECT * FROM files WHERE project_id = ? ORDER BY relative_path", 
                   (project['project_id'],))
    files = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'project': project,
        'files': files
    })

@app.route('/api/projects/<project_name>/file-tree')
def get_file_tree(project_name):
    """Return hierarchical file tree."""
    db_path = f"/PROJEKTS/{project_name}/db/{project_name}.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT relative_path, file_type, file_size, artist_name, modified_date
        FROM files
        WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)
        ORDER BY relative_path
    """, (project_name,))
    
    files = cursor.fetchall()
    conn.close()
    
    # Build tree structure
    tree = {}
    for rel_path, file_type, size, artist, mod_date in files:
        parts = Path(rel_path).parts
        current = tree
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = {
            'type': file_type,
            'size': size,
            'artist': artist,
            'modified': mod_date
        }
    
    return jsonify(tree)

@app.route('/api/projects/<project_name>/changelog')
def get_changelog(project_name):
    """Return project changelog."""
    db_path = f"/PROJEKTS/{project_name}/db/{project_name}.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM changelog
        WHERE project_id = (SELECT project_id FROM projects WHERE project_name = ?)
        ORDER BY change_date DESC
        LIMIT 100
    """, (project_name,))
    
    changelog = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(changelog)

@app.route('/api/projects/<project_name>/file/<path:relative_path>')
def get_file_details(project_name, relative_path):
    """Return detailed info for a file."""
    db_path = f"/PROJEKTS/{project_name}/db/{project_name}.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT f.*, a.duration, a.width, a.height, a.frame_rate, a.color_space
        FROM files f
        LEFT JOIN assets a ON f.file_id = a.file_id
        WHERE f.project_id = (SELECT project_id FROM projects WHERE project_name = ?)
        AND f.relative_path = ?
    """, (project_name, relative_path))
    
    file_details = dict(cursor.fetchone())
    conn.close()
    
    return jsonify(file_details)

@app.route('/')
def index():
    """Serve main web UI."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

**Docker Setup:**

```dockerfile
# logik_projekt_web/Dockerfile

FROM python:3.11

WORKDIR /app

RUN pip install flask

COPY app.py /app/
COPY templates/ /app/templates/
COPY static/ /app/static/

VOLUME ["/PROJEKTS"]

EXPOSE 5000

CMD ["python", "app.py"]
```

**Frontend HTML (Basic):**

```html
<!-- templates/index.html -->

<!DOCTYPE html>
<html>
<head>
    <title>LOGIK-PROJEKT Browser</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .project-info { background: #f0f0f0; padding: 10px; margin: 10px 0; }
        .file-tree { margin: 20px 0; }
        .changelog { margin: 20px 0; }
    </style>
</head>
<body>
    <h1>LOGIK-PROJEKT Browser</h1>
    
    <div id="project-info" class="project-info"></div>
    <div id="file-tree" class="file-tree"></div>
    <div id="changelog" class="changelog"></div>
    
    <script>
        // Load project from URL parameter or select
        const projectName = new URLSearchParams(window.location.search).get('project') || 'default';
        
        fetch(`/api/projects/${projectName}`)
            .then(r => r.json())
            .then(data => {
                document.getElementById('project-info').innerHTML = 
                    `<h2>${data.project.project_name}</h2>
                     <p>Created by: ${data.project.created_by}</p>
                     <p>Files: ${data.files.length}</p>`;
            });
        
        fetch(`/api/projects/${projectName}/file-tree`)
            .then(r => r.json())
            .then(data => {
                document.getElementById('file-tree').innerHTML = 
                    `<h3>Files</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
            });
        
        fetch(`/api/projects/${projectName}/changelog`)
            .then(r => r.json())
            .then(data => {
                document.getElementById('changelog').innerHTML = 
                    `<h3>Recent Changes</h3>
                     <ul>${data.map(c => 
                        `<li>${c.change_date}: ${c.change_type} by ${c.artist_name}</li>`
                     ).join('')}</ul>`;
            });
    </script>
</body>
</html>
```

**Usage:**

```bash
docker run -d \
  -v /PROJEKTS:/PROJEKTS \
  -p 5000:5000 \
  logik-projekt-web

# Then visit: http://localhost:5000/?project=2026_02_08-MY_NEW_PROJEKT
```

**Impact:** New component, doesn't affect existing code.

---

### 3.4 Phase 4: Updates to PySide6 GUI (logik-projekt-app)

**Objective:** Enhance GUI to show database-backed information; no breaking changes.

**Changes to `src/ui/panels/projekt_summary_panel.py`:**

```python
# Add new display showing SQLite info

class ProjektSummaryPanel(QWidget):
    """Enhanced with SQLite database info."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # ... existing code ...
        
        # NEW: Add SQLite status section
        self.db_status_label = QLabel("Database: Not initialized")
        # Add to layout
    
    def update_database_status(self, db_path: str):
        """Update display with database info."""
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM files")
                file_count = cursor.fetchone()[0]
                conn.close()
                
                self.db_status_label.setText(
                    f"Database: ✓ Initialized ({file_count} files tracked)"
                )
            except:
                self.db_status_label.setText("Database: ✗ Error reading database")
        else:
            self.db_status_label.setText("Database: Not yet created")
```

**Changes to `src/core/projekt_manager/projekt_creator.py`:**

```python
# Add SQLite initialization to project creation

def create_projekt(template_data, project_path):
    """Create a project with SQLite database."""
    
    # ... existing project creation code ...
    
    # NEW: Initialize SQLite database
    from src.core.database_manager.db_schema import initialize_projekt_database
    
    db_dir = os.path.join(project_path, 'db')
    os.makedirs(db_dir, exist_ok=True)
    
    project_name = os.path.basename(project_path)
    db_path = os.path.join(db_dir, f'{project_name}.db')
    
    creator_name = template_data.get('created_by', 'Unknown')
    
    initialize_projekt_database(project_path, db_path, creator_name)
    
    # Log success
    logging.info(f"Initialized SQLite database at {db_path}")
```

**New CLI for Monitor Service:**

```python
# src/core/utils/monitor_service_utils.py (NEW)

import subprocess
import os

def start_monitor_service(project_path: str, artist_name: str = "Producer"):
    """Start file monitor service for a project."""
    project_name = os.path.basename(project_path)
    db_path = os.path.join(project_path, 'db', f'{project_name}.db')
    
    # Option 1: Run via Docker
    subprocess.Popen([
        'docker', 'run', '-d',
        '-v', f'{os.path.dirname(project_path)}:/PROJEKTS',
        '-e', f'PROJECT_NAME={project_name}',
        '-e', f'ARTIST_NAME={artist_name}',
        'logik-projekt-monitor'
    ])
    
    # Option 2: Run locally (for development)
    # subprocess.Popen([
    #     'python', 'logik_projekt_monitor/monitor_service.py',
    #     '--project', project_path,
    #     '--db', db_path,
    #     '--artist', artist_name
    # ])
```

**Impact:** Additive changes to existing code. No breaking changes.

---

## 4. Data Migration Strategy

### 4.1 For New Projects

Projects created via the GUI after the update will automatically have SQLite databases initialized.

### 4.2 For Existing Projects

Provide a migration tool to retroactively initialize databases for existing projects:

```python
# src/core/utils/migration_utils.py (NEW)

def migrate_existing_project(project_path: str, artist_name: str = "Migrated"):
    """Initialize SQLite database for existing project."""
    from src.core.database_manager.db_schema import initialize_projekt_database
    
    project_name = os.path.basename(project_path)
    db_dir = os.path.join(project_path, 'db')
    os.makedirs(db_dir, exist_ok=True)
    
    db_path = os.path.join(db_dir, f'{project_name}.db')
    
    if os.path.exists(db_path):
        print(f"Database already exists at {db_path}")
        return
    
    initialize_projekt_database(project_path, db_path, artist_name)
    
    # Scan project directory and register existing files
    import hashlib
    from datetime import datetime
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT project_id FROM projects LIMIT 1")
    project_id = cursor.fetchone()[0]
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, project_path)
            
            # Skip the .db file itself
            if rel_path.endswith('.db'):
                continue
            
            file_size = os.path.getsize(filepath)
            file_hash = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
            mime_type = 'application/octet-stream'  # TODO: improve detection
            
            cursor.execute("""
                INSERT OR IGNORE INTO files (
                    project_id, relative_path, absolute_path, file_size, file_hash,
                    mime_type, created_date, modified_date, artist_name, file_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'unknown')
            """, (project_id, rel_path, filepath, file_size, file_hash, mime_type,
                  datetime.utcnow().isoformat(), datetime.utcnow().isoformat(), artist_name))
    
    conn.commit()
    conn.close()
    
    print(f"Migration complete. Database initialized at {db_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path", help="Path to existing project")
    parser.add_argument("--artist", default="Migrated", help="Artist name for migration")
    args = parser.parse_args()
    
    migrate_existing_project(args.project_path, args.artist)
```

---

## 5. Docker Compose Setup

**Unified Docker Compose for complete stack:**

```yaml
# docker-compose.yml

version: '3.8'

services:
  logik-projekt-app:
    build: .
    container_name: logik-projekt-app
    environment:
      - DISPLAY=${DISPLAY}
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix  # For X11 display
      - /PROJEKTS:/PROJEKTS
      - ./local_cache:/local_cache
    ports:
      - "5001:5001"  # For future remote UI
    networks:
      - logik-projekt-net

  logik-projekt-monitor:
    build: ./logik_projekt_monitor
    container_name: logik-projekt-monitor
    environment:
      - PROJECT_NAME=${PROJECT_NAME}
      - ARTIST_NAME=${ARTIST_NAME:-Unknown}
    volumes:
      - /PROJEKTS:/PROJEKTS
      - ./local_cache:/local_cache
    depends_on:
      - logik-projekt-app
    networks:
      - logik-projekt-net

  logik-projekt-web:
    build: ./logik_projekt_web
    container_name: logik-projekt-web
    volumes:
      - /PROJEKTS:/PROJEKTS
    ports:
      - "5000:5000"
    depends_on:
      - logik-projekt-app
    networks:
      - logik-projekt-net

networks:
  logik-projekt-net:
    driver: bridge
```

---

## 6. File Structure Updates

```
LOGIK-PROJEKT/
├── src/
│   ├── app.py (unchanged)
│   ├── ui/ (largely unchanged)
│   └── core/
│       ├── app_logic.py (unchanged)
│       ├── projekt_manager/
│       │   ├── projekt_creator.py (UPDATED: call initialize_projekt_database)
│       │   └── projekt_models.py
│       ├── database_manager/ (NEW)
│       │   ├── __init__.py
│       │   ├── db_schema.py (NEW: schema, init)
│       │   ├── db_operations.py (NEW: CRUD)
│       │   └── db_metadata_extractor.py (NEW: metadata extraction)
│       ├── template_manager/ (unchanged)
│       ├── functions/ (unchanged)
│       └── utils/
│           ├── migration_utils.py (NEW)
│           ├── monitor_service_utils.py (NEW)
│           └── ... (existing)
├── logik_projekt_monitor/ (NEW)
│   ├── Dockerfile
│   └── monitor_service.py
├── logik_projekt_web/ (NEW)
│   ├── Dockerfile
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       └── js/
├── docker-compose.yml (NEW)
└── ... (existing)
```

---

## 7. Transition Timeline & Milestones

| Phase | Duration | Tasks | Deliverable |
|-------|----------|-------|-------------|
| **1** | 1 week | Implement db_schema.py, update projekt_creator.py | SQLite init on project creation |
| **2** | 2 weeks | Build logik-projekt-monitor service | File monitoring + DB updates |
| **3** | 2 weeks | Build logik-projekt-web API + frontend | Web browsing of projects |
| **4** | 1 week | Enhance PySide6 GUI with DB info | DB status in GUI |
| **5** | 1 week | Migration utility for existing projects | Backward compatibility |
| **6** | 1 week | Testing & bug fixes | Stable release |
| **7** | Ongoing | Documentation, performance tuning | Production ready |

---

## 8. Backward Compatibility & Safety

### 8.1 Guarantees

- **Existing projects remain unchanged** until explicitly migrated
- **GUI remains fully functional** for existing workflows
- **No breaking changes** to `projekt_creator.py` or core logic
- **Opt-in database features** (can disable monitoring service if not needed)

### 8.2 Rollback Strategy

- If issues arise, disable monitoring services
- Continue using projects as before (files untouched)
- No data loss at any stage

---

## 9. Open Questions & Decisions

1. **Local Cache Strategy**: For internet storage (Lucid Link), should monitor service sync DB back periodically (e.g., every 5 minutes)? Or on-demand?
2. **Conflict Resolution**: If two artists modify same file simultaneously, how to handle DB conflicts? Last-write-wins vs. manual merge?
3. **Performance**: For projects with 100k+ files, monitor service scalability? Consider batching DB updates?
4. **Web UI Hosting**: Run web UI in Docker on producer workstation? Or cloud-based?
5. **Metadata Extraction**: Should monitor service extract ffmpeg metadata (duration, codec) for video files? Adds complexity but valuable.
6. **Archive Browsing**: How to browse archived projects? Copy DB to web server separately? Or integrate with archive storage?

---

## 10. Success Criteria

- [ ] New projects automatically have SQLite database
- [ ] File monitoring service detects changes in real-time
- [ ] Web UI shows project structure, files, changelog
- [ ] Multi-user collaboration tracking works (artist names in changelog)
- [ ] Existing projects can be migrated
- [ ] No breaking changes to existing GUI or core logic
- [ ] Docker Compose brings up entire stack without errors
- [ ] Performance acceptable (monitor service lag < 1 second)

---

**Version History**
- v01 (2026-02-08): Initial transition plan created

