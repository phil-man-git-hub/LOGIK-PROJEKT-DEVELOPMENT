# LOGIK-PROJEKT Data-to-Database Mapping Plan (v01)

## Executive Summary

This document maps LOGIK-PROJEKT's existing data flows (described in the Data Maps and Data Flow Analysis) to the SQLite database schema defined in the Database Architecture Plan v01.

The goal is to show **exactly where and when** each piece of data from the application gets stored in the database, enabling:
- Complete metadata tracking for projects
- Multi-user collaboration history
- Project portability with full metadata
- Web-based browsing of project structure and relationships

---

## 1. Current Data Flows vs. Database Integration

### 1.1 Template Creation Workflow (Existing)

```
Template Info Panel    Template Parameters Panel
    ↓                           ↓
  ├─ serial_number        ├─ resolution
  ├─ client_name          ├─ bit_depth
  ├─ campaign_name        ├─ framerate
  ├─ description          ├─ scan_mode
  └─ calculated_name      ├─ start_frame
                          ├─ init_config
                          ├─ ocio_config
                          └─ cache settings
                            ↓
                    Template Summary Panel
                            ↓
                    Export to JSON Template
```

### 1.2 With Database Integration (New)

```
Template Info Panel    Template Parameters Panel
    ↓                           ↓
  └──────────────┬──────────────┘
                 ↓
        Template Summary Panel
                 ↓
         Export to JSON Template
                 ↓
       Project Created (create_projekt)
                 ↓
    Initialize SQLite Database ← NEW
                 ↓
    ┌─────────────────────────────────┐
    │   SQLite tables populated:       │
    │   ├─ projects                    │
    │   ├─ files                       │
    │   ├─ changelog                   │
    │   └─ tags                        │
    │                                  │
    │   Data sources:                  │
    │   ├─ Template metadata           │
    │   ├─ Flame options               │
    │   ├─ Environment variables       │
    │   └─ Project creation parameters │
    └─────────────────────────────────┘
                 ↓
        Monitor Service Starts ← NEW
        (Watches for file changes)
```

---

## 2. Detailed Data-to-Table Mapping

### 2.1 `projects` Table

**Purpose:** Store high-level project metadata.

**Data Sources:**
- Template Info (from imported JSON or summary)
- Flame Options (Flame software version)
- System environment (user, timestamp)
- Project creation time

**Population Point:** When `initialize_projekt_database()` is called during `create_projekt()`.

**Mapping:**

| Database Field | Data Source | Value | Notes |
|---|---|---|---|
| `project_id` | SQLite | AUTO INCREMENT | Primary key |
| `project_name` | `logik_projekt_name` from `projekt_summary_data_map.md` | `{flame_projekt_nickname}_{flame_software_sanitized_version}` | e.g., "MY_PROJECT_2026.2" |
| `created_by` | `current_user` from `system_info_utils.py` | System user running the app | Captured from environment |
| `created_date` | System timestamp | `datetime.utcnow().isoformat()` | When project created |
| `description` | `flame_projekt_description` from imported template | Text from JSON | Optional, from template |
| `status` | Hardcoded | `'active'` | Set to active on creation; can be changed to 'archived' later |

**Implementation Location:** `src/core/database_manager/db_schema.py` → `initialize_projekt_database()`

```python
def initialize_projekt_database(project_root: str, db_path: str, creator_name: str):
    """Initialize SQLite database with template and project metadata."""
    
    # Get template metadata from project context
    template_data = get_template_metadata_from_project(project_root)
    flame_options = get_flame_options_from_project(project_root)
    
    # Insert into projects table
    cursor.execute("""
        INSERT INTO projects (project_name, created_by, created_date, description, status)
        VALUES (?, ?, ?, ?, 'active')
    """, (
        template_data['logik_projekt_name'],
        creator_name,
        datetime.utcnow().isoformat(),
        template_data.get('flame_projekt_description', '')
    ))
```

---

### 2.2 `files` Table

**Purpose:** Track all files in the project (created by users/processes).

**Data Sources:**
- File system (via monitor service watching `/PROJEKTS/<project>/`)
- File metadata (size, type, modification time)
- Artist name (from monitor service argument)

**Population Points:**
1. **Initial population** (optional, during project creation):
   - If project creation copies initial files (templates, configs, etc.), monitor service detects them
   - Or, optional migration scan at initialization time
   
2. **Continuous population** (via monitor service):
   - As artists add/modify/delete files in the project directory

**Mapping:**

| Database Field | Data Source | Value | Notes |
|---|---|---|---|
| `file_id` | SQLite | AUTO INCREMENT | Primary key |
| `project_id` | projects table | Foreign key | Links to project |
| `relative_path` | Monitor service file watcher | Path relative to project root | e.g., `renders/shot_001_v01.exr` |
| `absolute_path` | Monitor service file watcher | Full filesystem path | `/PROJEKTS/MY_PROJECT/renders/shot_001_v01.exr` |
| `file_size` | OS file metadata | Bytes | `os.path.getsize()` |
| `file_hash` | Monitor service | SHA256 hash | For integrity checking |
| `mime_type` | Monitor service | MIME type | `mimetypes.guess_type()` |
| `created_date` | OS file metadata | ISO timestamp | File creation time |
| `modified_date` | OS file metadata | ISO timestamp | Last modification time |
| `artist_name` | Monitor service parameter | String | Artist or process that created file |
| `file_type` | Monitor service | Categorized type | 'image', 'video', 'audio', 'config', 'other' |

**Implementation Location:** `logik_projekt_monitor/monitor_service.py` → `ProjectMonitor._add_file()`

```python
def _add_file(self, filepath: str):
    """Monitor service detects new file and adds to DB."""
    rel_path = os.path.relpath(filepath, self.project_root)
    file_size = os.path.getsize(filepath)
    file_hash = self._calculate_hash(filepath)
    mime_type = self._detect_mime_type(filepath)
    file_type = self._detect_file_type(mime_type)
    now = datetime.utcnow().isoformat()
    
    cursor.execute("""
        INSERT INTO files (
            project_id, relative_path, absolute_path, file_size, file_hash,
            mime_type, created_date, modified_date, artist_name, file_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        self.project_id, rel_path, filepath, file_size, file_hash,
        mime_type, now, now, self.artist_name, file_type
    ))
```

---

### 2.3 `assets` Table

**Purpose:** Store metadata specific to media files (images, video, audio, 3D models).

**Data Sources:**
- Monitor service extracts metadata from media files
- ffmpeg for video/audio metadata
- Pillow for image metadata
- 3D model loaders for model metadata

**Population Points:**
- Monitor service detects media file → extract metadata → INSERT into assets table

**Mapping:**

| Database Field | Data Source | Value | Notes |
|---|---|---|---|
| `asset_id` | SQLite | AUTO INCREMENT | Primary key |
| `file_id` | files table | Foreign key | Links to file |
| `asset_type` | Monitor service | 'image', 'video', 'audio', '3d_model' | Categorized from MIME type |
| `duration` | ffmpeg / Pillow | Float seconds | For video/audio only |
| `width` | ffmpeg / Pillow / model loader | Integer pixels | For images/video/3D |
| `height` | ffmpeg / Pillow | Integer pixels | For images/video |
| `frame_rate` | ffmpeg | Float fps | For video only (e.g., 24.0, 29.97) |
| `color_space` | ffmpeg / Pillow | String | 'rec709', 'acescc', 'sRGB', etc. |
| `thumbnail_path` | Monitor service | Relative path | Path to generated thumbnail image |
| `metadata` | ffmpeg / Pillow | JSON | Flexible storage for additional metadata |

**Implementation Location:** `src/core/database_manager/db_metadata_extractor.py` (NEW)

```python
def extract_asset_metadata(file_path: str, mime_type: str) -> dict:
    """Extract metadata from media files."""
    
    metadata = {}
    
    if mime_type.startswith('image/'):
        from PIL import Image
        img = Image.open(file_path)
        metadata = {
            'width': img.width,
            'height': img.height,
            'color_space': img.mode,  # 'RGB', 'RGBA', etc.
        }
    
    elif mime_type.startswith('video/'):
        # Use ffmpeg to extract metadata
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries',
            'stream=width,height,r_frame_rate,codec_color_space',
            '-of', 'json', file_path
        ], capture_output=True, text=True)
        
        probe_data = json.loads(result.stdout)
        if probe_data['streams']:
            stream = probe_data['streams'][0]
            metadata = {
                'width': stream.get('width'),
                'height': stream.get('height'),
                'frame_rate': eval(stream.get('r_frame_rate', '24/1')),
                'color_space': stream.get('codec_color_space', 'unknown'),
                'duration': stream.get('duration'),
            }
    
    elif mime_type.startswith('audio/'):
        # Extract audio metadata
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries',
            'stream=duration,sample_rate,channels',
            '-of', 'json', file_path
        ], capture_output=True, text=True)
        
        probe_data = json.loads(result.stdout)
        if probe_data['streams']:
            stream = probe_data['streams'][0]
            metadata = {
                'duration': stream.get('duration'),
                'sample_rate': stream.get('sample_rate'),
                'channels': stream.get('channels'),
            }
    
    return metadata
```

---

### 2.4 `relationships` Table

**Purpose:** Track dependencies and relationships between files.

**Data Sources:**
- Application logic (e.g., render output depends on source footage)
- User annotations (via web UI)
- File naming conventions (e.g., `shot_001_v01.exr` is a version of `shot_001_v00.exr`)

**Population Points:**
- (Future) Post-processing analysis or user annotations
- Version tracking (detect `v01`, `v02` patterns in filenames)

**Mapping:**

| Database Field | Data Source | Value | Notes |
|---|---|---|---|
| `relationship_id` | SQLite | AUTO INCREMENT | Primary key |
| `source_file_id` | files table | Foreign key | File that depends on or relates to target |
| `target_file_id` | files table | Foreign key | File that source depends on |
| `relationship_type` | Analysis / User input | String | 'depends_on', 'input_to', 'output_of', 'version_of' |
| `notes` | User input or analysis | Text | Optional notes about relationship |

**Implementation Location:** Future enhancement or plugin system.

**Example:**
- `shot_001_v02.exr` (source) "version_of" `shot_001_v01.exr` (target)
- `final_composite.exr` (source) "depends_on" `shot_001_v02.exr` (target)

---

### 2.5 `changelog` Table

**Purpose:** Track all changes to the project (who did what when).

**Data Sources:**
- Monitor service detects file changes (created, modified, deleted)
- User actions (project creation, template import, etc.)
- System events

**Population Points:**
1. **Project creation:**
   - INSERT: `{ change_type: 'created', artist_name: creator, details: {...} }`

2. **Template import:**
   - INSERT: `{ change_type: 'template_imported', artist_name: importer, details: {template_name, timestamp} }`

3. **File changes (via monitor service):**
   - `created`: New file added
   - `modified`: File updated
   - `deleted`: File removed

4. **User actions (via web UI):**
   - Tags added/removed
   - Relationships created
   - Annotations added

**Mapping:**

| Database Field | Data Source | Value | Notes |
|---|---|---|---|
| `change_id` | SQLite | AUTO INCREMENT | Primary key |
| `project_id` | projects table | Foreign key | Links to project |
| `file_id` | files table | Foreign key or NULL | NULL if change affects project, not specific file |
| `artist_name` | Monitor service or user context | String | Who made the change |
| `change_type` | Monitor service or system | String | 'created', 'modified', 'deleted', 'template_imported', etc. |
| `change_date` | System timestamp | ISO timestamp | When change occurred |
| `details` | Context-specific | JSON | Additional details (e.g., old size, new size, file hash) |

**Implementation Location:** 
- `logik_projekt_monitor/monitor_service.py` → File changes
- `src/core/database_manager/db_operations.py` → Project-level events

```python
def log_change(project_id: int, file_id: int, artist_name: str, 
               change_type: str, details: dict = None):
    """Log a change to the changelog table."""
    cursor.execute("""
        INSERT INTO changelog (project_id, file_id, artist_name, change_type, change_date, details)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        project_id,
        file_id,
        artist_name,
        change_type,
        datetime.utcnow().isoformat(),
        json.dumps(details or {})
    ))
```

---

### 2.6 `tags` Table

**Purpose:** Allow flexible tagging/annotations of files (user-defined metadata).

**Data Sources:**
- User input via web UI
- Application logic (auto-tagging based on file type, artist, etc.)

**Population Points:**
- User adds/edits tags via web interface
- Auto-tagging logic (e.g., "final_render", "approved", "archived")

**Mapping:**

| Database Field | Data Source | Value | Notes |
|---|---|---|---|
| `tag_id` | SQLite | AUTO INCREMENT | Primary key |
| `file_id` | files table | Foreign key | Links to file being tagged |
| `tag_name` | User input or auto-tagging | String | E.g., 'version', 'status', 'department' |
| `tag_value` | User input or auto-tagging | String | E.g., '01', 'approved', 'compositing' |

**Example Tagging Scheme:**

```
File: shot_001_v02.exr
├─ tag_name: 'version'       tag_value: '02'
├─ tag_name: 'status'        tag_value: 'approved'
├─ tag_name: 'artist'        tag_value: 'Flame Artist Name'
└─ tag_name: 'department'    tag_value: 'compositing'
```

---

## 3. Data Capture Points in Existing Workflow

### 3.1 Project Creation (from `projekt_creator.py`)

**Current Flow:**
```python
def create_projekt(template_data, project_path):
    # 1. Create directory structure
    # 2. Copy Flame configs
    # 3. Create startup scripts
    # 4. Create PostgreSQL database (existing)
```

**Enhanced Flow:**
```python
def create_projekt(template_data, project_path):
    # Existing logic...
    
    # NEW: Initialize SQLite database
    db_dir = os.path.join(project_path, 'db')
    os.makedirs(db_dir, exist_ok=True)
    
    project_name = os.path.basename(project_path)
    db_path = os.path.join(db_dir, f'{project_name}.db')
    creator_name = template_data.get('created_by', os.getenv('USER'))
    
    from src.core.database_manager.db_schema import initialize_projekt_database
    initialize_projekt_database(
        project_root=project_path,
        db_path=db_path,
        creator_name=creator_name,
        template_data=template_data,  # Pass template for metadata
        flame_options=flame_options     # Pass Flame options
    )
    
    # Log project creation to changelog
    log_change(
        project_id=1,  # First and only project in DB
        file_id=None,
        artist_name=creator_name,
        change_type='created',
        details={
            'template_name': template_data.get('logik_projekt_name'),
            'flame_version': template_data.get('flame_software'),
            'description': template_data.get('flame_projekt_description')
        }
    )
    
    # NEW: Start monitor service
    from src.core.utils.monitor_service_utils import start_monitor_service
    start_monitor_service(project_path, creator_name)
```

---

### 3.2 Template Data Captured

**At project creation time, populate `projects` table with:**

From `template_summary_data_map.md`:
- `template_serial_number` → (NOT in projects, but can be stored in tags)
- `template_client_name` → (NOT in projects, but can be stored in tags)
- `template_campaign_name` → (NOT in projects, but can be stored in tags)
- `template_calculated_name` → `projects.project_name`
- `template_description` → `projects.description`

From `template_parameters_data_map.md`:
- `template_resolution` → Tag: `resolution = "1920x1080"`
- `template_bit_depth` → Tag: `bit_depth = "10-bit"` or `"8-bit"`
- `template_framerate` → Tag: `framerate = "23.976"` or `"24"`
- `template_scan_mode` → Tag: `scan_mode = "interlaced"` or `"progressive"`
- `template_start_frame` → Tag: `start_frame = "1001"`
- `template_init_config` → Tag: `init_config = "flame-default"`
- `template_ocio_config` → Tag: `ocio_config = "ocio_name"`

---

### 3.3 Flame Options Captured

From `flame_options_data_map.md` (captured when project created):

**In `projects` table:**
- `created_by` ← `current_user` from system

**In tags (for querying/filtering):**
- Tag: `flame_version = "2026.2.0"`
- Tag: `flame_home_dir = "/opt/Autodesk/flame"`
- Tag: `flame_setups_dir = "/opt/Autodesk/flame/setups"`

---

### 3.4 Projekt Summary Data

From `projekt_summary_data_map.md`:

**In `projects` table:**
- `created_by` ← `current_user`
- `description` ← `flame_projekt_description`

**In tags:**
- `workstation = "hostname"` ← `current_workstation`
- `os = "Linux"` ← `current_os`
- `creator_group = "group_name"` ← `current_group`

---

## 4. Data Flow Diagram: Old vs. New

### 4.1 Old Flow (No Database)

```
┌─────────────────────────────────────┐
│  GUI Panels (PySide6)               │
│  ├─ Template Info                   │
│  ├─ Template Parameters             │
│  ├─ Template Summary                │
│  ├─ Projekt Template (import)       │
│  ├─ Flame Options                   │
│  └─ Projekt Summary                 │
└──────────────┬──────────────────────┘
               ↓
        ┌──────────────┐
        │ app_logic.py │
        │ (facade)     │
        └──────────────┘
               ↓
   ┌───────────┴───────────┐
   ↓                       ↓
Project Creator      Template Handler
   ↓                       ↓
Create Project       JSON Template File
   ↓
/PROJEKTS/<PROJECT>/
├─ Flame configs
├─ Scripts
└─ PostgreSQL DB
   (NO metadata about files)
```

### 4.2 New Flow (With SQLite)

```
┌─────────────────────────────────────┐
│  GUI Panels (PySide6)               │
│  ├─ Template Info                   │
│  ├─ Template Parameters             │
│  ├─ Template Summary                │
│  ├─ Projekt Template (import)       │
│  ├─ Flame Options                   │
│  └─ Projekt Summary                 │
└──────────────┬──────────────────────┘
               ↓
        ┌──────────────┐
        │ app_logic.py │
        │ (facade)     │
        └──────────────┘
               ↓
   ┌───────────┴───────────┐
   ↓                       ↓
Project Creator      Template Handler
   ↓                       ↓
Create Project       JSON Template File
   ↓
/PROJEKTS/<PROJECT>/
├─ Flame configs
├─ Scripts
├─ PostgreSQL DB
└─ db/
   └─ <PROJECT>.db ← NEW
      ├─ projects (template + system metadata)
      ├─ files (empty initially)
      ├─ assets (empty initially)
      ├─ relationships (empty initially)
      ├─ changelog (project creation event)
      └─ tags (template specs as tags)
          ↑
          │
          └─ Monitor Service Watches
             /PROJEKTS/<PROJECT>/
             ↓
             Detects file changes
             ↓
             Updates files, assets, changelog tables
             
   Monitor Service also syncs DB
   back to storage (Lucid Link, etc.)
```

---

## 5. Integration with Existing Application Logic

### 5.1 `projekt_creator.py` Changes

**Current:**
```python
from src.core.functions.create.create_projekt_pgsql_db import create_projekt_pgsql_db

def create_projekt(template_data, project_path):
    # ... existing code ...
    create_projekt_pgsql_db(project_path)  # Create PostgreSQL DB
```

**Enhanced:**
```python
from src.core.functions.create.create_projekt_pgsql_db import create_projekt_pgsql_db
from src.core.database_manager.db_schema import initialize_projekt_database  # NEW

def create_projekt(template_data, project_path, flame_options):
    # ... existing code ...
    
    # Create PostgreSQL DB (existing)
    create_projekt_pgsql_db(project_path)
    
    # NEW: Create and initialize SQLite DB
    db_dir = os.path.join(project_path, 'db')
    os.makedirs(db_dir, exist_ok=True)
    
    project_name = os.path.basename(project_path)
    db_path = os.path.join(db_dir, f'{project_name}.db')
    creator_name = os.getenv('USER', 'Unknown')
    
    initialize_projekt_database(
        project_root=project_path,
        db_path=db_path,
        creator_name=creator_name,
        template_data=template_data,
        flame_options=flame_options
    )
    
    # NEW: Start file monitor service
    from src.core.utils.monitor_service_utils import start_monitor_service
    start_monitor_service(project_path, creator_name)
```

---

### 5.2 `app_window.py` Changes (GUI)

**Current:**
```python
def _create_projekt(self):
    project_data = self.app_logic.get_projekt_summary_data()
    self.worker.create_projekt(project_data)
```

**Enhanced:**
```python
def _create_projekt(self):
    project_data = self.app_logic.get_projekt_summary_data()
    flame_options = self.flame_options_panel.get_flame_options()  # NEW
    project_data['flame_options'] = flame_options
    
    self.worker.create_projekt(project_data)
    
    # NEW: After project creation, update UI to show DB status
    if project_data.get('project_created'):
        self._update_db_status(project_data['logik_projekt_path'])
```

---

### 5.3 Enhanced Project Summary Display

**Current:**
- Shows: Project name, Flame version, directories, configuration

**Enhanced - Add:**
```python
# In projekt_summary_panel.py

self.db_status_label = QLabel("Database: Initializing...")

def _update_db_status(self, project_path):
    """Update display with SQLite database info."""
    db_path = os.path.join(project_path, 'db', os.path.basename(project_path) + '.db')
    
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
                f"Database: ✓ Active | {file_count} files tracked | {event_count} events"
            )
        except Exception as e:
            self.db_status_label.setText(f"Database: ✗ Error - {str(e)}")
    else:
        self.db_status_label.setText("Database: Not initialized")
```

---

## 6. Data Validation & Integrity

### 6.1 Database Constraints

```sql
-- Enforce referential integrity
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT UNIQUE NOT NULL,
    ...
);

CREATE TABLE files (
    file_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    ...
    FOREIGN KEY(project_id) REFERENCES projects(project_id)
);

-- Prevent orphaned relationships
CREATE TABLE relationships (
    ...
    FOREIGN KEY(source_file_id) REFERENCES files(file_id) ON DELETE CASCADE,
    FOREIGN KEY(target_file_id) REFERENCES files(file_id) ON DELETE CASCADE
);

-- Ensure unique file paths per project
CREATE UNIQUE INDEX idx_files_project_path 
ON files(project_id, relative_path);

-- Improve changelog queries
CREATE INDEX idx_changelog_project_date 
ON changelog(project_id, change_date DESC);

-- Improve file type queries
CREATE INDEX idx_files_type 
ON files(project_id, file_type);
```

---

### 6.2 Data Consistency Checks

**Monitor Service Validation:**
```python
def _validate_file_entry(self, filepath: str, entry: dict) -> bool:
    """Ensure file entry is valid before inserting to DB."""
    
    # Check file still exists
    if not os.path.exists(filepath):
        return False
    
    # Check hash consistency
    actual_hash = self._calculate_hash(filepath)
    if entry.get('file_hash') != actual_hash:
        logging.warning(f"Hash mismatch for {filepath}")
        return False
    
    # Check size consistency
    actual_size = os.path.getsize(filepath)
    if entry.get('file_size') != actual_size:
        logging.warning(f"Size mismatch for {filepath}")
        return False
    
    return True
```

---

## 7. Data Persistence & Sync (for Internet Storage)

### 7.1 Local Cache Strategy

For projects on internet storage (Lucid Link, S3, etc.):

```python
# In logik_projekt_app/entrypoint.sh

# 1. Download DB from remote storage
rsync -av /PROJEKTS/PROJECT_NAME/db/*.db /local_cache/

# 2. Start app with local DB
python app.py --db-path /local_cache/PROJECT_NAME.db

# 3. Start monitor service with local DB
python monitor_service.py --db /local_cache/PROJECT_NAME.db

# 4. On app close, sync DB back to remote
rsync -av /local_cache/PROJECT_NAME.db /PROJEKTS/PROJECT_NAME/db/
```

### 7.2 Sync Conflict Resolution

If two artists modify DB simultaneously (rare but possible):

```python
def sync_database_back_to_storage(local_db_path, remote_db_path):
    """Sync local DB back to remote storage with conflict resolution."""
    
    # Strategy: Last-write-wins (simple)
    # Alternative: Merge changelogs if both have new entries
    
    if os.path.exists(remote_db_path):
        # Check remote DB timestamp
        local_mtime = os.path.getmtime(local_db_path)
        remote_mtime = os.path.getmtime(remote_db_path)
        
        if local_mtime > remote_mtime:
            # Local is newer, upload it
            shutil.copy(local_db_path, remote_db_path)
        else:
            # Remote is newer, download it
            shutil.copy(remote_db_path, local_db_path)
    else:
        # Remote doesn't exist, upload local
        shutil.copy(local_db_path, remote_db_path)
```

---

## 8. Mapping Summary Table

**Quick reference: Where each data element lives**

| Data Element | Current Location | New SQLite Location | Notes |
|---|---|---|---|
| Project name | Project directory name | `projects.project_name` | Derived from template |
| Creator | Environment variable | `projects.created_by` | Captured at project creation |
| Creation timestamp | Filesystem | `projects.created_date` | Set at initialization |
| File list | Filesystem | `files` table | Populated by monitor service |
| File metadata | Filesystem | `files` + `assets` tables | Updated by monitor service |
| Change history | None (NEW) | `changelog` table | Tracks who did what when |
| Template specs | JSON template file | `tags` table | For easy querying |
| Flame options | Flame configuration | `tags` table | For reference |
| User tags/annotations | None (NEW) | `tags` table | User-added metadata |
| File relationships | None (NEW) | `relationships` table | For dependency tracking |

---

## 9. Benefits of This Mapping

### For Producer
- **Complete audit trail** of who created/modified what and when
- **Searchable project structure** via web UI or queries
- **Template version tracking** (which template was used, when)
- **Easy project archaeology** (what did we do in this project?)

### For Artists
- **Automatic metadata capture** (no extra work)
- **Version tracking** (detect v01, v02, v03 patterns)
- **Time tracking** (when did file creation start/end?)

### For Multi-User Teams
- **Collaboration history** (who worked when)
- **Change notifications** (see what others added)
- **Conflict detection** (two people modifying same file)

### For Archival/Restoration
- **Complete project snapshot** in `.db` file
- **Browse archived projects** without restoring files
- **Metadata preserved** even if files are deleted

---

## 10. Open Questions

1. **Auto-tagging strategy:** Should we automatically extract and tag template specs? Or let users do it?
2. **Asset metadata extraction:** Should monitor service call ffmpeg/Pillow for all media? (Performance impact?)
3. **Version detection:** Should we detect version patterns (v01, v02) and auto-create relationships?
4. **Sync frequency:** How often should monitor service sync DB back to remote storage? (Every file change? Every 5 minutes?)
5. **Backward compatibility:** For existing projects without DB, how aggressively should we suggest migration?

---

**Version History**
- v01 (2026-02-08): Initial data-to-database mapping plan created

