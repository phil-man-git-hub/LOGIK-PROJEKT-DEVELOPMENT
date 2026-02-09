"""Database schema and initialization for LOGIK-PROJEKT SQLite databases.

This file provides a minimal, well-tested implementation of the schema
initialization required for Phase 1 work.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def initialize_projekt_database(project_root: str, db_path: str, creator_name: str, template_data: dict = None, flame_options: dict = None) -> bool:
    """Initialize a new SQLite database for a LOGIK-PROJEKT project.

    Creates required tables, indexes, and inserts an initial project row and changelog entry.
    Returns True on success and raises sqlite3.Error on failure.
    """

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    _create_tables(cursor)
    _create_indexes(cursor)

    project_name = Path(project_root).name
    description = ''
    if template_data:
        description = template_data.get('flame_projekt_description', '')

    cursor.execute("""
        INSERT INTO projects (project_name, created_by, created_date, description, status)
        VALUES (?, ?, ?, ?, 'active')
    """, (project_name, creator_name, datetime.utcnow().isoformat(), description))

    project_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO changelog (project_id, artist_name, change_type, change_date, details)
        VALUES (?, ?, 'created', ?, json('{}'))
    """, (project_id, creator_name, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    logger.info("Initialized SQLite DB at %s", db_path)
    return True


def _create_tables(cursor: sqlite3.Cursor) -> None:
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT UNIQUE NOT NULL,
            created_by TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            status TEXT DEFAULT 'active' CHECK (status IN ('active','archived','completed'))
        );

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

        CREATE TABLE IF NOT EXISTS relationships (
            relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file_id INTEGER NOT NULL,
            target_file_id INTEGER NOT NULL,
            relationship_type TEXT,
            notes TEXT,
            FOREIGN KEY(source_file_id) REFERENCES files(file_id) ON DELETE CASCADE,
            FOREIGN KEY(target_file_id) REFERENCES files(file_id) ON DELETE CASCADE
        );

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

        CREATE TABLE IF NOT EXISTS tags (
            tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            tag_name TEXT,
            tag_value TEXT,
            FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE CASCADE
        );
    """)


def _create_indexes(cursor: sqlite3.Cursor) -> None:
    cursor.executescript("""
        CREATE INDEX IF NOT EXISTS idx_files_project_type ON files(project_id, file_type);
        CREATE INDEX IF NOT EXISTS idx_files_project_path ON files(project_id, relative_path);
        CREATE INDEX IF NOT EXISTS idx_files_artist ON files(project_id, artist_name);

        CREATE INDEX IF NOT EXISTS idx_changelog_project_date ON changelog(project_id, change_date DESC);
        CREATE INDEX IF NOT EXISTS idx_changelog_artist ON changelog(artist_name, change_date DESC);

        CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(asset_type);

        CREATE INDEX IF NOT EXISTS idx_tags_file ON tags(file_id);
        CREATE INDEX IF NOT EXISTS idx_tags_name_value ON tags(tag_name, tag_value);
    """)


def drop_database(db_path: str) -> bool:
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
        logger.info("Dropped DB at %s", db_path)
        return True
    except sqlite3.Error as e:
        logger.error("Error dropping DB: %s", e)
        return False
