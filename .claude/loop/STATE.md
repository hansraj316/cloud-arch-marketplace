# Loop state — feature integration

Single source of truth between loop passes. Every `/integrate-features` pass
reads this first and appends to the pass log before finishing. Keep entries
to one or two lines; prune the log when it passes ~30 entries.

## In flight

- PR #4 `fix/ci-2026-06-09` — CI fix (ruff + black + `--validate` flag +
  mypy `_seed`). All gate steps pass locally as of `7a857a0`; awaiting CI
  confirmation, then merge-ready (maintainer merges).
- PR #5 `claude/amazing-hopper-y6nc7i` — loop-engineering setup. CI red until
  PR #4 merges into `main`; rebase afterwards.

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
