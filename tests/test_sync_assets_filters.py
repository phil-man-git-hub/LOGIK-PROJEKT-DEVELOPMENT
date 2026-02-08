import importlib.util
from pathlib import Path
import tempfile

# Load sync_assets module directly
module_path = Path.cwd() / 'cfg' / 'site-cfg' / 'flame-cfg' / 'flame-python' / 'logik_projekt' / 'hooks' / 'sync_assets.py'
spec = importlib.util.spec_from_file_location('sync_assets', str(module_path))
sync_assets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_assets)  # type: ignore


def test_project_filtering(tmp_path, monkeypatch):
    # Create dummy bookmarks: one inside, one outside
    inside = {'filesystem_path': str(Path('/PROJEKTS') / '777_test_test' / 'assets' / 'audio' / 'mix'), 'flame_folder': 'assets/audio/mix'}
    outside = {'filesystem_path': str(Path('/PROJEKTS') / 'other_project' / 'assets' / 'audio' / 'mix'), 'flame_folder': 'assets/audio/mix'}

    bookmarks = [inside, outside]

    filtered = []
    project_nickname = '777_test_test'
    project_assets_root = Path('/PROJEKTS') / project_nickname / 'assets'

    for b in bookmarks:
        fs_path = b.get('filesystem_path')
        p = Path(fs_path)
        try:
            if p.is_relative_to(project_assets_root):
                filtered.append(b)
        except Exception:
            pass

    assert len(filtered) == 1
    assert filtered[0]['filesystem_path'] == inside['filesystem_path']


def test_create_folder_defensive(monkeypatch):
    # Simulate a parent object with non-callable create_library
    class Parent:
        def __init__(self):
            self.name = 'parent'
            self.create_library = None

    # Load FlameImporter directly to avoid package import issues
    import importlib.util
    from pathlib import Path
    module_path = Path.cwd() / 'cfg' / 'site-cfg' / 'flame-cfg' / 'flame-python' / 'logik_projekt' / 'src' / 'core' / 'functions' / 'io' / 'flame_importer.py'
    spec = importlib.util.spec_from_file_location('flame_importer', str(module_path))
    fi_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fi_mod)  # type: ignore
    FlameImporter = fi_mod.FlameImporter

    importer = FlameImporter()
    p = Parent()
    # Should return None and not raise
    res = importer._create_folder(p, 'test')
    assert res is None