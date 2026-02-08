import importlib.util
import json
from pathlib import Path


def load_module_from_path(path: str):
    spec = importlib.util.spec_from_file_location("scaffold_issue", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_scaffold_issue_logic(tmp_path):
    # Mock template
    template_content = {
        "name": "root",
        "type": "directory",
        "children": [
            {"name": "step-01-type", "type": "directory", "children": [
                {"name": "type-issue-{{issue_id}}.md", "type": "file"}
            ]},
            {"name": "README.md", "type": "file"}
        ]
    }
    template_path = tmp_path / "template.json"
    template_path.write_text(json.dumps(template_content))

    out_base = tmp_path / "issues"
    out_base.mkdir()

    module_path = Path(__file__).parents[2] / '.github' / 'scripts' / 'scaffold_issue.py'
    module = load_module_from_path(str(module_path))

    # Test main logic by calling create_node or similar if available, 
    # but since main() uses argparse, we can test the render and create_node functions directly.
    ctx = {"issue_id": "001", "issue_title": "Test Issue"}
    target = out_base / "issue-001"
    target.mkdir()
    
    for child in template_content["children"]:
        module.create_node(child, target, ctx)

    # Verify
    assert (target / "step-01-type").is_dir()
    assert (target / "step-01-type" / "type-issue-001.md").is_file()
    assert (target / "README.md").is_file()
    
    content = (target / "step-01-type" / "type-issue-001.md").read_text()
    assert "# Test Issue" in content
    assert "Issue: 001" in content
