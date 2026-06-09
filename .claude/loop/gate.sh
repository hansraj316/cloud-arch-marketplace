#!/usr/bin/env bash
# Objective gate for the feature-integration loop — mirrors daily-ci.yml
# exactly. Loop passes must not push work that fails this script.
set -euo pipefail

cd "$(dirname "$0")/../../plugins/cloud-architecture-diagrams/skills/cloud-architecture-diagrams"

ruff check scripts tests
black --check scripts tests
mypy scripts
python -m pytest tests/ -q

smoke="$(mktemp -u /tmp/loop-gate-smoke.XXXXXX)"
python scripts/build_diagram.py assets/spec-example.json --out-prefix "$smoke"
test -s "$smoke.excalidraw"
test -s "$smoke.drawio"
python scripts/build_diagram.py assets/spec-example.json --validate

echo "GATE PASS"
