"""Tests for the spec validator (scripts/spec_schema.py)."""

import subprocess
import sys
from pathlib import Path

import pytest
import spec_schema
from conftest import load_spec

SKILL_ROOT = Path(__file__).resolve().parent.parent
BUILD = SKILL_ROOT / "scripts" / "build_diagram.py"


def test_valid_example_passes():
    spec = load_spec("spec-example.json")
    assert spec_schema.validate(spec) == []


def test_node_missing_required_coord_with_require_coords():
    spec = {"nodes": [{"id": "a", "title": "A", "x": 0, "y": 0, "width": 50}]}  # missing height
    errors = spec_schema.validate(spec, require_coords=True)
    assert any("a" in e and "height" in e for e in errors)


def test_dangling_edge_endpoint_flagged():
    spec = {
        "nodes": [{"id": "a", "x": 0, "y": 0, "width": 50, "height": 50}],
        "edges": [{"from": "a", "to": "ghost"}],
    }
    errors = spec_schema.validate(spec)
    assert any("dangling" in e and "ghost" in e for e in errors)


def test_duplicate_node_ids_flagged():
    spec = {
        "nodes": [
            {"id": "dup", "x": 0, "y": 0, "width": 50, "height": 50},
            {"id": "dup", "x": 60, "y": 0, "width": 50, "height": 50},
        ]
    }
    errors = spec_schema.validate(spec)
    assert any("duplicate node id 'dup'" in e for e in errors)


def test_wrong_type_width_flagged():
    spec = {"nodes": [{"id": "a", "x": 0, "y": 0, "width": "wide", "height": 50}]}
    errors = spec_schema.validate(spec, require_coords=True)
    assert any("width" in e and "number" in e for e in errors)


def test_missing_nodes_array_flagged():
    errors = spec_schema.validate({"title": "no nodes"})
    assert any("nodes" in e for e in errors)


def test_bad_dir_flagged():
    spec = {
        "nodes": [
            {"id": "a", "x": 0, "y": 0, "width": 50, "height": 50},
            {"id": "b", "x": 60, "y": 0, "width": 50, "height": 50},
        ],
        "edges": [{"from": "a", "to": "b", "dir": "sideways"}],
    }
    errors = spec_schema.validate(spec)
    assert any("dir" in e for e in errors)


def test_validate_or_raise():
    with pytest.raises(spec_schema.ValidationError):
        spec_schema.validate_or_raise({"edges": [{"from": "x", "to": "y"}]})


def _run_build(args, cwd):
    return subprocess.run(
        [sys.executable, str(BUILD), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_cli_validate_bad_spec_exits_nonzero_no_traceback(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"nodes": [], "edges": [{"from": "a", "to": "b"}]}')
    res = _run_build([str(bad), "--validate"], tmp_path)
    assert res.returncode != 0
    assert "Traceback" not in res.stderr
    assert "dangling" in res.stderr


def test_cli_validate_good_spec_exits_zero(tmp_path):
    good = SKILL_ROOT / "assets" / "spec-example.json"
    res = _run_build([str(good), "--validate"], tmp_path)
    assert res.returncode == 0
    assert "valid" in res.stdout.lower()
