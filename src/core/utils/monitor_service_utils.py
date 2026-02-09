"""Helpers to start/stop the monitor Docker service for a project."""

import subprocess
import os
import logging

logger = logging.getLogger(__name__)


def start_monitor_service(project_path: str, artist_name: str = "Producer") -> bool:
    project_name = os.path.basename(project_path.rstrip('/'))
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
    try:
        subprocess.run(['docker', 'stop', f'logik-projekt-monitor-{project_name}'], check=True)
        logger.info(f"Monitor service stopped for {project_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to stop monitor service: {e}")
        return False
