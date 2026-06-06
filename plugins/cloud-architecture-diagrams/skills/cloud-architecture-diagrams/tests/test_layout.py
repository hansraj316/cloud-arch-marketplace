"""Tests for the auto-layout pass (scripts/layout.py)."""

import layout


def _boxes_overlap(a, b, gap=0):
    return not (
        a["x"] + a["width"] + gap <= b["x"]
        or b["x"] + b["width"] + gap <= a["x"]
        or a["y"] + a["height"] + gap <= b["y"]
        or b["y"] + b["height"] + gap <= a["y"]
    )


def test_nodes_without_coords_get_assigned():
    spec = {
        "nodes": [
            {"id": "a", "title": "A"},
            {"id": "b", "title": "B"},
            {"id": "c", "title": "C"},
        ],
        "edges": [
            {"from": "a", "to": "b"},
            {"from": "b", "to": "c"},
        ],
    }
    assert layout.needs_layout(spec)
    layout.apply_layout(spec)
    for n in spec["nodes"]:
        for k in ("x", "y", "width", "height"):
            assert isinstance(n[k], (int, float)), f"{n['id']} missing {k}"


def test_computed_nodes_do_not_overlap():
    spec = {
        "nodes": [{"id": f"n{i}"} for i in range(8)],
        "edges": [
            {"from": "n0", "to": "n1"},
            {"from": "n0", "to": "n2"},
            {"from": "n1", "to": "n3"},
        ],
    }
    layout.apply_layout(spec)
    nodes = spec["nodes"]
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            assert not _boxes_overlap(a, b), f"{a['id']} overlaps {b['id']}"


def test_fixed_nodes_untouched():
    spec = {
        "nodes": [
            {"id": "fixed", "x": 999, "y": 888, "width": 100, "height": 50},
            {"id": "auto", "title": "Auto"},
        ],
        "edges": [{"from": "fixed", "to": "auto"}],
    }
    layout.apply_layout(spec)
    fixed = next(n for n in spec["nodes"] if n["id"] == "fixed")
    assert (fixed["x"], fixed["y"], fixed["width"], fixed["height"]) == (
        999,
        888,
        100,
        50,
    )


def test_chain_places_successive_layers_monotonic_x():
    spec = {
        "nodes": [{"id": "a"}, {"id": "b"}, {"id": "c"}],
        "edges": [
            {"from": "a", "to": "b"},
            {"from": "b", "to": "c"},
        ],
    }
    layout.apply_layout(spec)
    pos = {n["id"]: n for n in spec["nodes"]}
    assert pos["a"]["x"] < pos["b"]["x"] < pos["c"]["x"]


def test_disconnected_nodes_get_nonoverlapping_grid():
    spec = {
        "nodes": [{"id": f"d{i}"} for i in range(5)],
        "edges": [],
    }
    layout.apply_layout(spec)
    nodes = spec["nodes"]
    for n in nodes:
        assert "x" in n and "y" in n
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            assert not _boxes_overlap(a, b)


def test_fully_specified_spec_does_not_need_layout():
    spec = {
        "nodes": [
            {"id": "a", "x": 0, "y": 0, "width": 50, "height": 50},
            {"id": "b", "x": 100, "y": 0, "width": 50, "height": 50},
        ]
    }
    assert not layout.needs_layout(spec)
