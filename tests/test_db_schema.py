"""Tests for database schema initialization."""

import os
import tempfile
import sqlite3
import importlib.util
from pathlib import Path

# Load db_schema directly to avoid importing the entire package and its GUI deps
spec = importlib.util.spec_from_file_location('db_schema', str(Path(__file__).parents[1] / 'src' / 'core' / 'database_manager' / 'db_schema.py'))
db_schema = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_schema)
initialize_projekt_database = db_schema.initialize_projekt_database


def test_initialize_projekt_database_creates_db_and_tables():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test.db')
        assert not os.path.exists(db_path)

        result = initialize_projekt_database(project_root=tmpdir, db_path=db_path, creator_name='TestUser')
        assert result is True
        assert os.path.exists(db_path)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}

        expected_tables = {'projects', 'files', 'assets', 'relationships', 'changelog', 'tags'}
        assert expected_tables.issubset(tables)

        cursor.execute('SELECT COUNT(*) FROM projects')
        (project_count,) = cursor.fetchone()
        assert project_count == 1

        conn.close()
