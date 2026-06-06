"""Tests for the icon scorer/search (scripts/find_icon.py)."""

import json
from pathlib import Path

import find_icon

SKILL_ROOT = Path(__file__).resolve().parent.parent
INDEX = json.loads((SKILL_ROOT / "references" / "icon-index.json").read_text("utf-8"))


def test_s3_alias_beats_outposts_variant():
    """'S3' should resolve to canonical Simple Storage Service via CANON_ALIAS,
    outranking 'S3 on Outposts' which merely contains the literal token."""
    hits = find_icon.search("S3", 3, INDEX, ["aws"])
    assert hits[0]["name"].lower() == "amazon simple storage service"
    assert "outposts" not in hits[0]["name"].lower()


def test_arch_icon_ranks_above_res_icon_when_ambiguous():
    arch = {
        "name": "Amazon EC2",
        "search": "amazon ec2",
        "file": "assets/icons/aws/Arch_Amazon-EC2_48.svg",
    }
    res = {
        "name": "Amazon EC2",
        "search": "amazon ec2",
        "file": "assets/icons/aws/Res_Amazon-EC2_48.svg",
    }
    assert find_icon.score("compute", arch) > find_icon.score("compute", res)


def test_color_variant_outranks_bw_variant():
    color = {
        "name": "Power BI Color",
        "search": "power bi color",
        "category": "power-platform",
        "file": "x/Color.svg",
    }
    bw = {
        "name": "Power BI BW",
        "search": "power bi bw",
        "category": "power-platform",
        "file": "x/BW.svg",
    }
    assert find_icon.score("Power BI", color) > find_icon.score("Power BI", bw)


def test_search_respects_provider_filter():
    hits = find_icon.search("storage", 10, INDEX, ["aws"])
    assert hits, "expected at least one aws hit"
    assert all(h.get("provider") == "aws" for h in hits)

    gcp_hits = find_icon.search("BigQuery", 5, INDEX, ["gcp"])
    assert all(h.get("provider") == "gcp" for h in gcp_hits)


def test_score_is_numeric_and_ordered():
    hits = find_icon.search("Entra ID", 5, INDEX, ["microsoft"])
    scores = [h["score"] for h in hits]
    assert scores == sorted(scores, reverse=True)
