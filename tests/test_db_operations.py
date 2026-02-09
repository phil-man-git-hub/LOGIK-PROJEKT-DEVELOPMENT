"""Tests for db operations (log_change)"""

import os
import tempfile
import sqlite3
import importlib.util
from pathlib import Path

# Load modules directly to avoid importing the entire package and its GUI deps
spec_schema = importlib.util.spec_from_file_location('db_schema', str(Path(__file__).parents[1] / 'src' / 'core' / 'database_manager' / 'db_schema.py'))
db_schema = importlib.util.module_from_spec(spec_schema)
spec_schema.loader.exec_module(db_schema)
initialize_projekt_database = db_schema.initialize_projekt_database

spec_ops = importlib.util.spec_from_file_location('db_operations', str(Path(__file__).parents[1] / 'src' / 'core' / 'database_manager' / 'db_operations.py'))
db_ops = importlib.util.module_from_spec(spec_ops)
spec_ops.loader.exec_module(db_ops)
log_change = db_ops.log_change


def test_log_change_inserts_changelog_entry():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test.db')
        initialize_projekt_database(project_root=tmpdir, db_path=db_path, creator_name='Tester')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT project_id FROM projects LIMIT 1')
        (project_id,) = cursor.fetchone()

        success = log_change(db_path=db_path, project_id=project_id, artist_name='Tester', change_type='modified', file_id=None, details={'note': 'unit test'})
        assert success is True

        cursor.execute('SELECT change_type, artist_name FROM changelog WHERE project_id = ?', (project_id,))
        rows = cursor.fetchall()
        assert any(row[0] == 'modified' and row[1] == 'Tester' for row in rows)

        conn.close()
