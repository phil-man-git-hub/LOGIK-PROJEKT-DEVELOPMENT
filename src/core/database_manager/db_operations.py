"""Database operations: simple helpers and context manager."""

import sqlite3
import json
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Context manager for SQLite connection and cursor."""

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


def log_change(db_path: str, project_id: int, artist_name: str, change_type: str, file_id: Optional[int] = None, details: Optional[dict] = None) -> bool:
    try:
        with DatabaseConnection(db_path) as cursor:
            cursor.execute(
                """INSERT INTO changelog (project_id, file_id, artist_name, change_type, change_date, details)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    file_id,
                    artist_name,
                    change_type,
                    datetime.utcnow().isoformat(),
                    json.dumps(details or {}),
                ),
            )
        return True
    except sqlite3.Error as e:
        logger.error("Error logging change: %s", e)
        return False
