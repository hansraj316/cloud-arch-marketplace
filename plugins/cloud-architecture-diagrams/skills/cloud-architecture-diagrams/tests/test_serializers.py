"""Round-trip tests for the Excalidraw and draw.io serializers."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import build_diagram
from conftest import load_spec

SKILL_ROOT = Path(__file__).resolve().parent.parent


def _prims(tmp_path):
    spec = load_spec("spec-example.json")
    # Use an isolated icon cache so the test never writes into the repo.
    return build_diagram.build_primitives(spec, tmp_path / "_icons")


def test_to_excalidraw_emits_valid_json_with_files(tmp_path):
    prims = _prims(tmp_path)
    doc = json.loads(build_diagram.to_excalidraw(prims))
    assert doc["type"] == "excalidraw"
    assert isinstance(doc["elements"], list) and doc["elements"]
    # Bundled AWS/Azure icons embed as files; the example uses real icons.
    assert isinstance(doc["files"], dict)
    assert len(doc["files"]) > 0, "expected at least one embedded icon file"
    for f in doc["files"].values():
        assert f["dataURL"].startswith("data:image/svg+xml;base64,")


def test_to_drawio_parses_as_xml(tmp_path):
    prims = _prims(tmp_path)
    xml = build_diagram.to_drawio(prims)
    root = ET.fromstring(xml)
    assert root.tag == "mxfile"
    cells = root.findall(".//mxCell")
    assert len(cells) > 2  # cell 0, cell 1, plus content


def test_drawio_shapes_mode_parses(tmp_path):
    spec = load_spec("aws-spec-example.json")
    spec["drawio_shapes"] = True
    prims = build_diagram.build_primitives(spec, tmp_path / "_icons")
    xml = build_diagram.to_drawio(prims)
    ET.fromstring(xml)  # must not raise
