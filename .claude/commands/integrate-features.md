---
description: One pass of the feature-integration loop — drive open feature work to merge-ready and pick up the next item from the backlog.
---

Run ONE integration pass over this repository, then report status. Designed to
be invoked repeatedly (e.g. `/loop 30m /integrate-features`); each pass must be
idempotent — never redo work a previous pass already finished.

See `.claude/loop/README.md` for how the pieces fit together.

## 0. Load state

Read `.claude/loop/STATE.md` — it lists work in flight, the backlog, and
standing decisions. Trust it over re-deriving everything, but spot-check
anything that drives an action (e.g. a PR marked merge-ready).

## 1. Sync

Fetch `origin/main` and rebase the current working branch on it if behind.

## 2. Drive open PRs to merge-ready

For every open PR (use the GitHub tools, oldest first):

- Check CI. If a check failed, read the job logs, reproduce locally, and fix
  on the PR's branch — check it out with `git worktree add`, never by
  switching the main checkout.
- Address unresolved review comments: apply clear-cut fixes; reply on the
  thread only when a suggestion is wrong or ambiguous.
- **Gate before every push**: run `.claude/loop/gate.sh` and require
  `GATE PASS`. Then have the `loop-verifier` agent review the diff; only push
  on `VERDICT: PASS`. A red gate or failed verdict is never pushed —
  re-diagnose instead of retrying blindly.
- If the PR is green, approved, and conflict-free, record it as
  **merge-ready** in STATE.md. Do NOT merge — merging to `main` is the
  maintainer's call unless they have explicitly said otherwise.

## 3. Pick up the next feature

Only if step 2 left nothing in flight that needs work:

- Take the top item from the STATE.md backlog, or the oldest open issue
  labeled `enhancement` / `feature`. If neither exists, the pass is idle —
  do not invent features.
- Implement on a new `feat/<slug>` branch, keeping changes small and matching
  the existing plugin layout (`plugins/cloud-architecture-diagrams/…`).
- Gate + verifier as in step 2, then push and open a **draft PR** that
  references the issue.

## 4. Record and report

- Append one or two lines to the STATE.md pass log (what was done, commit
  SHAs, what the next pass should look at) and update the in-flight/backlog
  sections. Commit STATE.md changes with the work they describe when on the
  same branch; otherwise note them for the next push.
- End with a short status: PRs touched and their state (fixed / merge-ready /
  blocked), feature picked up (if any). If the pass was idle, say "idle" in
  one line — don't pad it.
