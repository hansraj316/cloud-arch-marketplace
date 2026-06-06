"""Shared pytest fixtures/path setup for the skill test suite."""

import json
import sys
from pathlib import Path

import pytest

SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = SKILL_ROOT / "scripts"

# Make the scripts importable as top-level modules.
sys.path.insert(0, str(SCRIPTS))

# The scripts use PEP 604 unions (e.g. `str | None`) that are only valid at
# runtime on Python 3.10+. On older interpreters importing them raises
# TypeError, so skip the whole suite with a clear message rather than erroring.
if sys.version_info < (3, 10):
    collect_ignore_glob = ["*"]

    def pytest_collection_modifyitems(config, items):  # pragma: no cover
        skip = pytest.mark.skip(reason="requires Python >= 3.10 (PEP 604 unions)")
        for item in items:
            item.add_marker(skip)


def load_spec(name: str) -> dict:
    """Load a bundled example spec by filename."""
    return json.loads((SKILL_ROOT / "assets" / name).read_text("utf-8"))
