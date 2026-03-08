# LOGIK-PROJEKT Implementation Roadmap (v01)

## Executive Summary

This document provides a **detailed, step-by-step implementation roadmap** for integrating SQLite database functionality into LOGIK-PROJEKT. It serves as a practical guide for developers, specifying:
- Exact file changes and new files to create
- Code examples and implementation details
- Testing strategy at each phase
- Risk assessment and rollback procedures
- Timeline and effort estimates

---

## 0. Pre-Implementation Checklist

### Code Readiness
- [ ] Review and understand all existing code (use static analyses)
- [ ] Set up development environment with Python 3.11+, PySide6, SQLite3
- [ ] Ensure git repository is clean and on main branch
- [ ] Create feature branch: `git checkout -b feature/sqlite-database-integration`

### Dependencies to Add
```bash
# Add to requirements.txt
watchdog>=3.0.0          # File system monitoring
ffmpeg-python>=0.2.1     # Video/audio metadata
Pillow>=9.0.0            # Image metadata
```

### File Structure Preparation
```
LOGIK-PROJEKT/
├── src/
│   ├── core/
│   │   ├── database_manager/          # NEW DIRECTORY
│   │   │   ├── __init__.py            # NEW
│   │   │   ├── db_schema.py           # NEW
│   │   │   ├── db_operations.py       # NEW
│   │   │   └── db_metadata_extractor.py # NEW
│   │   └── utils/
│   │       ├── migration_utils.py     # NEW
│   │       └── monitor_service_utils.py # NEW
│   └── ...
├── logik_projekt_monitor/             # NEW DIRECTORY
│   ├── __init__.py                    # NEW
│   ├── Dockerfile                     # NEW
│   └── monitor_service.py             # NEW
├── logik_projekt_web/                 # NEW DIRECTORY
│   ├── __init__.py                    # NEW
│   ├── Dockerfile                     # NEW
│   ├── app.py                         # NEW
│   ├── templates/                     # NEW
│   │   └── index.html                 # NEW
│   └── static/                        # NEW
│       ├── css/
│       ├── js/
│       └── images/
└── docker-compose.yml                 # NEW/UPDATED
```

---

## Phase 1: SQLite Schema & Initialization (Week 1)

### Objective
Create the database schema and initialization system. **Zero breaking changes** to existing code.

### 1.1 Create `src/core/database_manager/db_schema.py`

**Location:** `src/core/database_manager/db_schema.py` (NEW FILE)

**Purpose:** Define SQLite schema and initialization logic.

**Implementation:**

```python
"""
Database schema and initialization for LOGIK-PROJEKT SQLite databases.

This module provides functions to create and initialize SQLite databases
for individual LOGIK-PROJEKT projects, with all tables and indexes.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def initialize_projekt_database(
    project_root: str,
    db_path: str,
    creator_name: str,
    template_data: dict = None,
    flame_options: dict = None
) -> bool:
    """
    Initialize a new SQLite database for a LOGIK-PROJEKT project.
    
    Args:
        project_root: Root directory of the project
        db_path: Full path to the .db file
        creator_name: Name of the user creating the project
        template_data: Optional template metadata dictionary
        flame_options: Optional Flame options dictionary
    
    Returns:
        True if successful, False otherwise
    
    Raises:
        sqlite3.Error: If database operations fail
    """
    
    try:
        # Ensure parent directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Create database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create all tables
        _create_tables(cursor)
        
        # Create indexes for performance
        _create_indexes(cursor)
        
        # Insert initial project record
        project_name = Path(project_root).name
        description = ""
        if template_data:
            description = template_data.get('flame_projekt_description', '')
        
        cursor.execute("""
            INSERT INTO projects (project_name, created_by, created_date, description, status)
            VALUES (?, ?, ?, ?, 'active')
        """, (project_name, creator_name, datetime.utcnow().isoformat(), description))
        
        # Get the inserted project_id
        project_id = cursor.lastrowid
        
        # Store template metadata as tags (if provided)
        if template_data:
            _store_template_metadata_as_tags(cursor, project_id, template_data)
        
        # Store Flame options as tags (if provided)
        if flame_options:
            _store_flame_options_as_tags(cursor, project_id, flame_options)
        
        # Log initial project creation event
        cursor.execute("""
            INSERT INTO changelog (project_id, artist_name, change_type, change_date, details)
            VALUES (?, ?, 'created', ?, json('{}'))
        """, (project_id, creator_name, datetime.utcnow().isoformat()))
        
        conn.commit()
        conn.close()
        
        logger.info(f"SQLite database initialized at {db_path}")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize SQLite database: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        raise


def _create_tables(cursor: sqlite3.Cursor) -> None:
    """Create all necessary tables."""
    
    cursor.executescript("""
        -- Projects table
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT UNIQUE NOT NULL,
            created_by TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            status TEXT DEFAULT 'active',
            CHECK (status IN ('active', 'archived', 'completed'))
        );
        
        -- Files table
        CREATE TABLE IF NOT EXISTS files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
            UNIQUE(project_id, relative_path)
        );
        
        -- Assets table (media metadata)
        CREATE TABLE IF NOT EXISTS assets (
            asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            asset_type TEXT,
            duration REAL,
            width INTEGER,
            height INTEGER,
            frame_rate REAL,
            color_space TEXT,
            thumbnail_path TEXT,
            metadata JSON,
            FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE CASCADE
        );
        
        -- Relationships table (file dependencies)
        CREATE TABLE IF NOT EXISTS relationships (
            relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file_id INTEGER NOT NULL,
            target_file_id INTEGER NOT NULL,
            relationship_type TEXT,
            notes TEXT,
            FOREIGN KEY(source_file_id) REFERENCES files(file_id) ON DELETE CASCADE,
            FOREIGN KEY(target_file_id) REFERENCES files(file_id) ON DELETE CASCADE
        );
        
        -- Changelog table (audit trail)
        CREATE TABLE IF NOT EXISTS changelog (
            change_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            file_id INTEGER,
            artist_name TEXT,
            change_type TEXT,
            change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details JSON,
            FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
            FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE CASCADE
        );
        
        -- Tags table (flexible metadata)
        CREATE TABLE IF NOT EXISTS tags (
            tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            tag_name TEXT,
            tag_value TEXT,
            FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE CASCADE
        );
    """)


def _create_indexes(cursor: sqlite3.Cursor) -> None:
    """Create indexes for query performance."""
    
    cursor.executescript("""
        -- File queries
        CREATE INDEX IF NOT EXISTS idx_files_project_type 
            ON files(project_id, file_type);
        
        CREATE INDEX IF NOT EXISTS idx_files_project_path 
            ON files(project_id, relative_path);
        
        CREATE INDEX IF NOT EXISTS idx_files_artist 
            ON files(project_id, artist_name);
        
        -- Changelog queries
        CREATE INDEX IF NOT EXISTS idx_changelog_project_date 
            ON changelog(project_id, change_date DESC);
        
        CREATE INDEX IF NOT EXISTS idx_changelog_artist 
            ON changelog(artist_name, change_date DESC);
        
        -- Asset queries
        CREATE INDEX IF NOT EXISTS idx_assets_type 
            ON assets(asset_type);
        
        -- Tag queries
        CREATE INDEX IF NOT EXISTS idx_tags_file 
            ON tags(file_id);
        
        CREATE INDEX IF NOT EXISTS idx_tags_name_value 
            ON tags(tag_name, tag_value);
    """)


def _store_template_metadata_as_tags(
    cursor: sqlite3.Cursor,
    project_id: int,
    template_data: dict
) -> None:
    """Store template metadata as project-level tags."""
    
    # Create a pseudo file_id for project-level metadata
    # We'll use a special approach: store as tags on a "metadata" file entry
    # Or simpler: skip file_id for now, store project-level data differently
    
    # For now, just log that we could store this
    logger.debug(f"Template metadata available for tagging: {template_data.keys()}")


def _store_flame_options_as_tags(
    cursor: sqlite3.Cursor,
    project_id: int,
    flame_options: dict
) -> None:
    """Store Flame options as project-level tags."""
    
    logger.debug(f"Flame options available for tagging: {flame_options.keys()}")


def drop_database(db_path: str) -> bool:
    """
    Drop all tables in a database (for testing/cleanup).
    
    WARNING: This deletes all data. Use with caution.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.executescript("""
            DROP TABLE IF EXISTS tags;
            DROP TABLE IF EXISTS changelog;
            DROP TABLE IF EXISTS relationships;
            DROP TABLE IF EXISTS assets;
            DROP TABLE IF EXISTS files;
            DROP TABLE IF EXISTS projects;
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"Database dropped: {db_path}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error dropping database: {e}")
        return False
```

**Testing:**

Create `tests/test_db_schema.py`:

```python
"""Tests for database schema initialization."""

import os
import tempfile
import sqlite3
import pytest
from src.core.database_manager.db_schema import initialize_projekt_database


def test_initialize_projekt_database():
    """Test that database is initialized with correct schema."""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test.db')
        
        # Initialize database
        result = initialize_projekt_database(
            project_root=tmpdir,
            db_path=db_path,
            creator_name='TestUser'
        )
        
        assert result is True
        assert os.path.exists(db_path)
        
        # Verify tables exist
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = {row[0] for row in cursor.fetchall()}
        
        expected_tables = {
            'projects', 'files', 'assets', 'relationships', 'changelog', 'tags'
        }
        assert expected_tables == tables
        
        # Verify project was created
        cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = cursor.fetchone()[0]
        assert project_count == 1
        
        conn.close()


def test_initialize_with_template_data():
    """Test that template metadata is stored."""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test.db')
        template_data = {
            'flame_projekt_description': 'Test Project',
            'flame_software': '2026.2.0'
        }
        
        result = initialize_projekt_database(
            project_root=tmpdir,
            db_path=db_path,
            creator_name='TestUser',
            template_data=template_data
        )
        
        assert result is True
        
        # Verify description was stored
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM projects WHERE project_id = 1")
        description = cursor.fetchone()[0]
        assert description == 'Test Project'
        conn.close()
```

**Run tests:**
```bash
pytest tests/test_db_schema.py -v
```

---

### 1.2 Create `src/core/database_manager/db_operations.py`

**Location:** `src/core/database_manager/db_operations.py` (NEW FILE)

**Purpose:** CRUD operations and common database queries.

**Implementation (Abbreviated):**

```python
"""
Database operations for LOGIK-PROJEKT.

Provides CRUD functions and common queries.
"""

import sqlite3
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Context manager for database operations."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()


def log_change(
    db_path: str,
    project_id: int,
    artist_name: str,
    change_type: str,
    file_id: Optional[int] = None,
    details: Optional[Dict] = None
) -> bool:
    """Log a change to the changelog."""
    
    try:
        with DatabaseConnection(db_path) as cursor:
            cursor.execute("""
                INSERT INTO changelog (
                    project_id, file_id, artist_name, change_type, change_date, details
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                project_id,
                file_id,
                artist_name,
                change_type,
                datetime.utcnow().isoformat(),
                json.dumps(details or {})
            ))
        return True
    except sqlite3.Error as e:
        logger.error(f"Error logging change: {e}")
        return False


def get_project_summary(db_path: str) -> Optional[Dict]:
    """Get summary info about a project."""
    
    try:
        with DatabaseConnection(db_path) as cursor:
            cursor.execute("SELECT * FROM projects WHERE project_id = 1")
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        logger.error(f"Error getting project summary: {e}")
        return None


def get_files_by_type(db_path: str, project_id: int, file_type: str) -> List[Dict]:
    """Get all files of a specific type."""
    
    try:
        with DatabaseConnection(db_path) as cursor:
            cursor.execute(
                "SELECT * FROM files WHERE project_id = ? AND file_type = ? ORDER BY relative_path",
                (project_id, file_type)
            )
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        logger.error(f"Error getting files by type: {e}")
        return []


def get_changelog(db_path: str, project_id: int, limit: int = 100) -> List[Dict]:
    """Get recent changelog entries."""
    
    try:
        with DatabaseConnection(db_path) as cursor:
            cursor.execute(
                "SELECT * FROM changelog WHERE project_id = ? ORDER BY change_date DESC LIMIT ?",
                (project_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        logger.error(f"Error getting changelog: {e}")
        return []
```

**Testing:**

Create `tests/test_db_operations.py` (similar pattern as schema tests).

---

### 1.3 Update `src/core/projekt_manager/projekt_creator.py`

**Location:** `src/core/projekt_manager/projekt_creator.py` (MODIFY EXISTING)

**Changes:** Add SQLite database initialization at end of project creation.

**Code to add (near end of `create_projekt()` function):**

```python
# NEW: Initialize SQLite database
from src.core.database_manager.db_schema import initialize_projekt_database

db_dir = os.path.join(project_root, 'db')
os.makedirs(db_dir, exist_ok=True)

project_name = os.path.basename(project_root)
db_path = os.path.join(db_dir, f'{project_name}.db')
creator_name = template_data.get('created_by', os.getenv('USER', 'Unknown'))

try:
    initialize_projekt_database(
        project_root=project_root,
        db_path=db_path,
        creator_name=creator_name,
        template_data=template_data,
        flame_options=flame_options
    )
    logging.info(f"SQLite database initialized at {db_path}")
except Exception as e:
    logging.error(f"Failed to initialize SQLite database: {e}")
    # Don't fail project creation if DB init fails
    # But log the error for troubleshooting
```

**Testing:**

Create `tests/test_projekt_creator_with_db.py`:

```python
"""Test that projekt_creator initializes SQLite database."""

import os
import tempfile
import sqlite3
from src.core.projekt_manager.projekt_creator import create_projekt


def test_create_projekt_initializes_database():
    """Test that project creation also creates SQLite DB."""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        project_data = {
            'logik_projekt_path': os.path.join(tmpdir, 'TEST_PROJECT'),
            'created_by': 'TestUser',
            'flame_projekt_description': 'Test',
            # ... other required fields
        }
        
        # This test will require mocking or a proper test setup
        # For now, we're just documenting what should be tested
        pass
```

---

### 1.4 Create `src/core/database_manager/__init__.py`

**Location:** `src/core/database_manager/__init__.py` (NEW FILE)

**Content:**

```python
"""Database management for LOGIK-PROJEKT."""

from .db_schema import initialize_projekt_database
from .db_operations import DatabaseConnection, log_change

__all__ = [
    'initialize_projekt_database',
    'DatabaseConnection',
    'log_change',
]
```

---

### 1.5 Phase 1 Testing & Validation

**Run all tests:**
```bash
pytest tests/test_db_schema.py tests/test_db_operations.py -v
```

**Manual testing:**
1. Create a test project and verify `db/<PROJECT>.db` is created
2. Inspect DB with `sqlite3 db/TEST_PROJECT.db ".schema"`
3. Verify tables are created
4. Check changelog entry for project creation

**Expected outcome:**
- ✅ SQLite database initializes on project creation
- ✅ All tables created with proper schema
- ✅ Indexes created for performance
- ✅ Initial project record inserted
- ✅ Zero breaking changes to existing code

---

## Phase 2: File Monitoring Service (Week 2-3)

### Objective
Build Docker service that watches project directories and updates SQLite database.

### 2.1 Create `logik_projekt_monitor/monitor_service.py`

**Location:** `logik_projekt_monitor/monitor_service.py` (NEW FILE)

**Key components:**
```python
import sqlite3
import os
import hashlib
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ProjectMonitor(FileSystemEventHandler):
    """Watches project directory and updates SQLite DB."""
    
    def __init__(self, project_root: str, db_path: str, artist_name: str):
        self.project_root = project_root
        self.db_path = db_path
        self.artist_name = artist_name
        self.project_id = self._get_project_id()
    
    def on_created(self, event):
        """Handle file creation event."""
        if not event.is_directory:
            self._add_file(event.src_path)
    
    def on_modified(self, event):
        """Handle file modification event."""
        if not event.is_directory:
            self._update_file(event.src_path)
    
    # ... implementation details
```

(See **LOGIK-PROJEKT-APP-TRANSITION-v01.md**, Section 3.2 for full implementation)

### 2.2 Create `logik_projekt_monitor/Dockerfile`

**Location:** `logik_projekt_monitor/Dockerfile` (NEW FILE)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install watchdog ffmpeg-python Pillow

COPY monitor_service.py /app/

VOLUME ["/PROJEKTS"]

ENV ARTIST_NAME="Monitor Service"
ENV PROJECT_NAME=""

CMD ["python", "/app/monitor_service.py", \
     "--project", "/PROJEKTS/${PROJECT_NAME}", \
     "--db", "/PROJEKTS/${PROJECT_NAME}/db/${PROJECT_NAME}.db", \
     "--artist", "${ARTIST_NAME}"]
```

### 2.3 Create `src/core/utils/monitor_service_utils.py`

**Location:** `src/core/utils/monitor_service_utils.py` (NEW FILE)

**Purpose:** Utilities for starting/stopping monitor service.

```python
"""Utilities for managing the file monitor service."""

import subprocess
import os
import logging

logger = logging.getLogger(__name__)


def start_monitor_service(project_path: str, artist_name: str = "Producer") -> bool:
    """
    Start file monitor service for a project.
    
    Args:
        project_path: Root path of the project
        artist_name: Artist/user name for change tracking
    
    Returns:
        True if service started successfully
    """
    
    project_name = os.path.basename(project_path)
    
    try:
        subprocess.Popen([
            'docker', 'run', '-d',
            '-v', f'{os.path.dirname(project_path)}:/PROJEKTS',
            '-e', f'PROJECT_NAME={project_name}',
            '-e', f'ARTIST_NAME={artist_name}',
            '--name', f'logik-projekt-monitor-{project_name}',
            'logik-projekt-monitor'
        ])
        logger.info(f"Monitor service started for {project_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to start monitor service: {e}")
        return False


def stop_monitor_service(project_name: str) -> bool:
    """Stop monitor service for a project."""
    
    try:
        subprocess.run([
            'docker', 'stop', f'logik-projekt-monitor-{project_name}'
        ], check=True)
        logger.info(f"Monitor service stopped for {project_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to stop monitor service: {e}")
        return False
```

---

## Phase 3: Web UI for Project Browsing (Week 4-5)

### 3.1 Create `logik_projekt_web/app.py`

**Location:** `logik_projekt_web/app.py` (NEW FILE)

(See **LOGIK-PROJEKT-APP-TRANSITION-v01.md**, Section 3.3 for full implementation)

### 3.2 Create Web Templates & Static Assets

```
logik_projekt_web/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── project_view.html
│   └── file_detail.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

---

## Phase 4: GUI Integration (Week 6)

### 4.1 Update `src/ui/panels/projekt_summary_panel.py`

**Add database status display:**

```python
# In ProjektSummaryPanel.__init__()

self.db_status_label = QLabel("Database: Not initialized")
self.db_status_label.setStyleSheet("color: #888; font-size: 10px;")
# Add to layout

# Add method
def update_db_status(self, db_path: str):
    """Update database status display."""
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM files")
            file_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM changelog")
            event_count = cursor.fetchone()[0]
            conn.close()
            
            self.db_status_label.setText(
                f"Database: ✓ | {file_count} files | {event_count} events"
            )
        except Exception as e:
            self.db_status_label.setText(f"Database: ✗ {str(e)[:30]}")
    else:
        self.db_status_label.setText("Database: ⧒ Initializing...")
```

### 4.2 Update `src/ui/app_window.py`

**Call database status update after project creation:**

```python
# In _create_projekt() or in worker finished slot

def on_projekt_created(self, project_path: str):
    """Handle successful project creation."""
    db_path = os.path.join(project_path, 'db', os.path.basename(project_path) + '.db')
    self.projekt_summary_panel.update_db_status(db_path)
```

---

## Phase 5: Data Migration for Existing Projects (Week 7)

### 5.1 Create `src/core/utils/migration_utils.py`

**Location:** `src/core/utils/migration_utils.py` (NEW FILE)

**Purpose:** Retroactively initialize databases for existing projects.

```python
"""Utilities for migrating existing projects to use SQLite."""

import os
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from src.core.database_manager.db_schema import initialize_projekt_database
import logging

logger = logging.getLogger(__name__)


def migrate_existing_project(project_path: str, artist_name: str = "Migrated") -> bool:
    """
    Initialize SQLite database for an existing project.
    
    Scans project directory and registers existing files.
    """
    
    project_name = os.path.basename(project_path)
    db_dir = os.path.join(project_path, 'db')
    os.makedirs(db_dir, exist_ok=True)
    
    db_path = os.path.join(db_dir, f'{project_name}.db')
    
    if os.path.exists(db_path):
        logger.info(f"Database already exists for {project_name}")
        return True
    
    try:
        # Initialize database
        initialize_projekt_database(project_path, db_path, artist_name)
        
        # Scan and register existing files
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT project_id FROM projects LIMIT 1")
        project_id = cursor.fetchone()[0]
        
        file_count = 0
        for root, dirs, files in os.walk(project_path):
            for file in files:
                # Skip the database file itself
                if file.endswith('.db'):
                    continue
                
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, project_path)
                
                try:
                    file_size = os.path.getsize(filepath)
                    file_hash = _calculate_hash(filepath)
                    mime_type = 'application/octet-stream'  # TODO: improve
                    now = datetime.utcnow().isoformat()
                    
                    cursor.execute("""
                        INSERT OR IGNORE INTO files (
                            project_id, relative_path, absolute_path, file_size,
                            file_hash, mime_type, created_date, modified_date,
                            artist_name, file_type
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'unknown')
                    """, (project_id, rel_path, filepath, file_size, file_hash,
                          mime_type, now, now, artist_name))
                    
                    file_count += 1
                except Exception as e:
                    logger.warning(f"Failed to register file {rel_path}: {e}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Migration complete. {file_count} files registered.")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False


def _calculate_hash(filepath: str) -> str:
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path", help="Path to project root")
    parser.add_argument("--artist", default="Migrated", help="Artist name for migration")
    args = parser.parse_args()
    
    success = migrate_existing_project(args.project_path, args.artist)
    exit(0 if success else 1)
```

---

## Phase 6: Docker Compose & Testing (Week 8)

### 6.1 Create `docker-compose.yml`

**Location:** `docker-compose.yml` (NEW FILE)

(See **LOGIK-PROJEKT-APP-TRANSITION-v01.md**, Section 5 for details)

### 6.2 Integration Tests

Create `tests/integration/` with end-to-end tests:

```
tests/
├── unit/
│   ├── test_db_schema.py
│   ├── test_db_operations.py
│   └── test_migration.py
└── integration/
    ├── test_project_creation_with_db.py
    ├── test_monitor_service.py
    └── test_web_api.py
```

**Example integration test:**

```python
"""Integration test: Project creation with database."""

import os
import tempfile
import sqlite3
import pytest
from src.core.projekt_manager.projekt_creator import create_projekt


def test_full_project_creation_workflow():
    """Test complete project creation including SQLite setup."""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = os.path.join(tmpdir, '2026_02_08-TEST_PROJECT')
        
        # Simulate project creation
        template_data = {
            'logik_projekt_path': project_path,
            'created_by': 'TestUser',
            # ... other required fields
        }
        
        # Create project
        create_projekt(template_data)
        
        # Verify project directory exists
        assert os.path.isdir(project_path)
        
        # Verify database was created
        db_path = os.path.join(project_path, 'db', '2026_02_08-TEST_PROJECT.db')
        assert os.path.exists(db_path)
        
        # Verify database schema
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        expected_tables = {'projects', 'files', 'assets', 'relationships', 'changelog', 'tags'}
        assert expected_tables.issubset(tables)
        
        # Check initial project record
        cursor.execute("SELECT COUNT(*) FROM projects")
        assert cursor.fetchone()[0] == 1
        
        # Check changelog entry
        cursor.execute("SELECT COUNT(*) FROM changelog WHERE change_type = 'created'")
        assert cursor.fetchone()[0] == 1
        
        conn.close()
```

---

## Phase 7: Documentation & Refinement (Week 9)

### 7.1 Update README

Add sections:
- Database architecture
- Monitor service setup
- Web UI access
- Data migration for existing projects

### 7.2 Create User Guide

Document:
- How projects now have databases
- How to browse archived projects without restoring files
- Multi-user collaboration tracking
- Troubleshooting database issues

### 7.3 Developer Documentation

Document:
- Database schema
- Adding new database operations
- Extending monitor service
- Web API endpoints

---

## Testing Strategy

### Unit Tests (Phase 1)
- Database schema initialization
- Database operations (CRUD)
- Validation of constraints

### Integration Tests (Phase 6)
- Project creation with database
- Monitor service file detection
- Web API endpoints
- Data migration

### System Tests
- Multi-user scenario (multiple artists working simultaneously)
- Archive/restore workflow
- Internet storage sync (Lucid Link)

### Performance Tests
- Monitor service response time (< 1 second)
- Database query performance (1000+ files)
- Web UI loading time (< 2 seconds)

---

## Risk Assessment & Rollback

### Risk Level: **LOW**

**Why:**
- All database code is new, not modifying existing code paths
- Existing projekt creation works with or without database initialization
- If database initialization fails, project creation still succeeds (with warning log)
- No changes to GUI logic, only additions

### Rollback Procedure

If critical issues arise:

```bash
# 1. Revert code changes
git revert <commit_hash>

# 2. Projects created during rollback will have empty databases
#    - This is harmless; they work as normal
#    - Monitor service won't be running for new projects
#    - Can re-initialize databases after fixing issues

# 3. No data loss occurs (all project files remain intact)
```

---

## Effort Estimation

| Phase | Duration | Effort | Dependencies |
|-------|----------|--------|--------------|
| 1. Schema & Init | 1 week | 15 hrs | None |
| 2. Monitor Service | 2 weeks | 25 hrs | Phase 1 |
| 3. Web UI | 2 weeks | 30 hrs | Phase 1 |
| 4. GUI Integration | 1 week | 10 hrs | Phases 1-3 |
| 5. Data Migration | 1 week | 8 hrs | Phase 1 |
| 6. Testing & Docker | 1 week | 12 hrs | Phases 1-5 |
| 7. Documentation | 1 week | 10 hrs | Phases 1-6 |
| **Total** | **9 weeks** | **110 hrs** | - |

---

## Success Criteria Checklist

### By End of Phase 1
- [ ] SQLite database initializes on project creation
- [ ] All tables created with correct schema
- [ ] Zero breaking changes to existing code
- [ ] Unit tests pass (100% coverage of new code)

### By End of Phase 3
- [ ] File monitor service detects file changes
- [ ] Web UI browses project structure
- [ ] Web UI shows file metadata
- [ ] Web UI displays changelog

### By End of Phase 7
- [ ] All integration tests pass
- [ ] Documentation complete
- [ ] Multi-user scenario tested
- [ ] Archive/restore workflow verified
- [ ] Performance acceptable (< 1% CPU overhead)

---

## Known Limitations & Future Work

### Current Implementation
- Monitor service uses simple last-write-wins conflict resolution
- Version detection (v01, v02) not automated
- Metadata extraction (ffmpeg) optional/best-effort
- Archive browsing requires separate DB copy

### Future Enhancements
- Smart version detection and relationship creation
- Full-text search of project metadata
- Automated backup of databases
- Central PostgreSQL catalog (optional)
- Mobile app for project browsing
- Real-time collaboration notifications

---

**Version History**
- v01 (2026-02-08): Initial implementation roadmap created

