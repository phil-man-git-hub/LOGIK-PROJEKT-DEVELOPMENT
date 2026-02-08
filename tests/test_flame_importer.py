import os
import importlib.util
from pathlib import Path

# Load the flame_importer module directly from the file to avoid package import issues
module_path = Path.cwd() / 'cfg' / 'site-cfg' / 'flame-cfg' / 'flame-python' / 'logik_projekt' / 'src' / 'core' / 'functions' / 'io' / 'flame_importer.py'
spec = importlib.util.spec_from_file_location('flame_importer', str(module_path))
flame_importer_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flame_importer_mod)  # type: ignore
FlameImporter = flame_importer_mod.FlameImporter


class DummyProj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_get_project_attribute_direct(tmp_path, monkeypatch):
    proj = DummyProj(project_path=str(tmp_path))
    importer = FlameImporter()
    # Ensure flame module missing doesn't affect this logic
    importer.flame = None
    assert importer.get_project_attribute(proj, 'project_path') == str(tmp_path)


def test_get_project_attribute_derived_from_folder(tmp_path):
    proj = DummyProj(project_folder=str(tmp_path))
    importer = FlameImporter()
    importer.flame = None
    assert importer.get_project_attribute(proj, 'project_path') == str(tmp_path)


def test_get_project_attribute_constructed_from_name(monkeypatch):
    proj = DummyProj(name='dummy_project')
    importer = FlameImporter()
    importer.flame = None
    # Constructed candidate should be returned even if it doesn't exist
    expected = f"/var/opt/Autodesk/flame/projects/dummy_project"
    assert importer.get_project_attribute(proj, 'project_path') == expected
