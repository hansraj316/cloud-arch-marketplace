# Loop state — feature integration

Single source of truth between loop passes. Every `/integrate-features` pass
reads this first and appends to the pass log before finishing. Keep entries
to one or two lines; prune the log when it passes ~30 entries.

## In flight

(nothing — all clear as of 2026-06-09)

## Backlog

(none — feed the loop by filing issues labeled `enhancement` or `feature`)

## Decisions

- Loop never merges to `main`; it drives PRs to merge-ready and reports.
- Gate = `.claude/loop/gate.sh` (mirror of daily-ci.yml); nothing pushes
  without a local GATE PASS.

## Pass log

- 2026-06-09 pass 1: diagnosed PR #4 (black 26.x reformat ×8, missing
  `--validate` CLI flag, mypy `_seed.n`), fixed all three, pushed `7a857a0`.
  Subscribed to PR #4/#5 activity; heartbeat monitor armed.
- 2026-06-09 pass 2: added loop scaffolding (`9b63d7f`); confirmed PR #4 CI
  green → merge-ready. PR #5 CI red as expected (inherits main's ruff
  errors); next pass: rebase #5 once #4 merges.
- 2026-06-09 pass 3: maintainer authorized merges. PR #4 squash-merged to
  main (`8eb49a1`); rebased #5 onto it, local GATE PASS, merged #5. Loop
  empty — next work comes from `enhancement`/`feature` issues.
