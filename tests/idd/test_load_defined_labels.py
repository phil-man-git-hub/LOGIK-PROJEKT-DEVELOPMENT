import importlib.util
import sys
import yaml
from pathlib import Path


def load_module_from_path(path: str):
    spec = importlib.util.spec_from_file_location("sync_labels", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_yaml(tmp_path, content):
    p = tmp_path / "labels.yml"
    p.write_text(yaml.safe_dump(content))
    return str(p)


def test_load_defined_labels_happy_path(tmp_path):
    content = [
        {"name": "bug", "color": "#d73a4a", "description": "Bug reports"},
        {"name": "enhancement", "color": "0e8a16", "description": "New feature"}
    ]
    path = write_yaml(tmp_path, content)
    module = load_module_from_path(str(Path(__file__).parents[2] / '.github' / 'scripts' / 'sync_labels.py'))
    labels = module.load_defined_labels(path)
    assert isinstance(labels, list)
    assert len(labels) == 2
    assert labels[0]['name'] == 'bug'
    assert labels[0]['color'] == 'd73a4a'


def test_load_defined_labels_duplicates_and_invalid(tmp_path):
    content = [
        {"name": "bug", "color": "d73a4a"},
        {"name": "bug", "color": "d73a4a"},
        "not-a-map",
        {"color": "abcd00"},
    ]
    path = write_yaml(tmp_path, content)
    module = load_module_from_path(str(Path(__file__).parents[2] / '.github' / 'scripts' / 'sync_labels.py'))
    labels = module.load_defined_labels(path)
    # should keep only one valid label
    assert len(labels) == 1
    assert labels[0]['name'] == 'bug'
