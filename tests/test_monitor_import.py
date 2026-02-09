"""Ensure monitor_service can be imported safely when `watchdog` is not installed."""

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('monitor_service', str(Path(__file__).parents[1] / 'logik_projekt_monitor' / 'monitor_service.py'))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ProjectMonitor')
assert hasattr(mod, 'WATCHDOG_AVAILABLE')
