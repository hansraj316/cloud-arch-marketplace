#!/usr/bin/env bash
# Factory build gate for cloud-arch-marketplace. Mirrors .github/workflows/daily-ci.yml
# and .claude/loop/gate.sh step for step. The factory runs the copy on main,
# never the branch under test, so changes here land as their own PR.
#
# factory-check: lint - ruff check scripts tests
# factory-check: format - black --check scripts tests
# factory-check: types - mypy scripts
# factory-check: tests - python -m pytest tests/
# factory-check: smoke - build_diagram.py renders assets/spec-example.json to .excalidraw and .drawio, then --validate
#
# Run all checks:   bash factory/checks.sh
# Run one check:    bash factory/checks.sh tests
set -euo pipefail
cd "$(git rev-parse --show-toplevel)/plugins/cloud-architecture-diagrams/skills/cloud-architecture-diagrams"

only="${1:-}"
run() { [ -z "$only" ] || [ "$only" = "$1" ]; }

if run lint; then
  echo "== lint"
  ruff check scripts tests
fi

if run format; then
  echo "== format"
  black --check scripts tests
fi

if run types; then
  echo "== types"
  mypy scripts
fi

if run tests; then
  echo "== tests"
  python -m pytest tests/ -q
fi

if run smoke; then
  echo "== smoke"
  smoke="$(mktemp -u "${TMPDIR:-/tmp}/factory-smoke.XXXXXX")"
  python scripts/build_diagram.py assets/spec-example.json --out-prefix "$smoke"
  test -s "$smoke.excalidraw"
  test -s "$smoke.drawio"
  rm -f "$smoke.excalidraw" "$smoke.drawio"
  python scripts/build_diagram.py assets/spec-example.json --validate
fi

echo "CHECKS PASS"
