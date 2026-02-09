Logik-Projekt Monitor Service (skeleton)

This directory contains a small, safe-to-import skeleton of the monitor
service used to watch project directories and update the project SQLite DB.

Usage:

- To run locally (requires `watchdog` installed):

    python monitor_service.py --project /path/to/PROJECT --db /path/to/PROJECT/db/PROJECT.db --artist "Artist Name"

- Docker (example):

    docker build -t logik-projekt-monitor .
    docker run -v /path/to/PROJEKTS:/PROJEKTS -e PROJECT_NAME=MY_PROJECT -e ARTIST_NAME="Artist" logik-projekt-monitor

Notes:
- This is a skeleton for Phase 2. The full implementation will extract metadata, generate thumbnails, and handle sync.
