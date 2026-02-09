"""Simple, safe-to-import monitor service skeleton for Phase 2.

This module uses optional imports so it can be imported in CI without
having `watchdog` installed. Runtime behavior requires `watchdog`.
"""

from __future__ import annotations
import os
import hashlib
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Optional import of watchdog to keep tests lightweight
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except Exception:
    WATCHDOG_AVAILABLE = False


class ProjectMonitor:
    """Monitors a project directory and updates the project's SQLite DB.

    This is a small, test-friendly skeleton. Full implementation will use
    `watchdog` to watch file system events and update DB accordingly.
    """

    def __init__(self, project_root: str, db_path: str, artist_name: str = "Monitor"):
        self.project_root = Path(project_root)
        self.db_path = Path(db_path)
        self.artist_name = artist_name
        self._observer = None

    def start(self) -> None:
        if not WATCHDOG_AVAILABLE:
            raise RuntimeError("watchdog package is required to run the monitor service")

        # Placeholder for real observer setup
        self._observer = Observer()
        # Real implementation would schedule handlers and start observer
        self._observer.start()

    def stop(self) -> None:
        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._observer = None

    # Utility helpers used by monitor
    def _calculate_hash(self, filepath: Path, algorithm: str = "sha256") -> str:
        h = hashlib.new(algorithm)
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def _insert_file_record(self, rel_path: str) -> Optional[int]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        now = datetime.utcnow().isoformat()

        abs_path = str(self.project_root / rel_path)
        file_size = os.path.getsize(abs_path)
        file_hash = self._calculate_hash(Path(abs_path))

        cursor.execute("""INSERT INTO files (project_id, relative_path, absolute_path, file_size, file_hash, mime_type, created_date, modified_date, artist_name, file_type)
                          VALUES ((SELECT project_id FROM projects LIMIT 1), ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """,
                       (rel_path, abs_path, file_size, file_hash, None, now, now, self.artist_name, None))

        conn.commit()
        file_id = cursor.lastrowid
        conn.close()
        return file_id


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run monitor service (skeleton).")
    parser.add_argument("--project", required=True, help="Path to project root")
    parser.add_argument("--db", required=True, help="Path to project DB file")
    parser.add_argument("--artist", default="Monitor", help="Artist name that will be logged")
    args = parser.parse_args()

    monitor = ProjectMonitor(args.project, args.db, args.artist)
    if not WATCHDOG_AVAILABLE:
        print("watchdog not installed. This is a skeleton; install 'watchdog' to run the service.")
    else:
        print("Starting monitor (press Ctrl+C to stop)")
        try:
            monitor.start()
            while True:
                pass
        except KeyboardInterrupt:
            monitor.stop()
