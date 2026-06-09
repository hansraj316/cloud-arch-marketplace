---
description: One pass of the feature-integration loop — drive open feature work to merge-ready and pick up the next item from the backlog.
---

Run ONE integration pass over this repository, then report status. Designed to
be invoked repeatedly (e.g. `/loop /integrate-features`); each pass must be
idempotent — never redo work a previous pass already finished.

## 1. Sync

- Fetch `origin/main` and rebase the current working branch on it if behind.

## 2. Drive open PRs to merge-ready

For every open PR (use the GitHub tools, oldest first):

- Check CI. If a check failed, read the logs, reproduce locally where possible
  (`ruff check scripts tests`, `pytest` under
  `plugins/cloud-architecture-diagrams/skills/cloud-architecture-diagrams/`),
  fix on the PR's branch, and push.
- Address unresolved review comments: apply clear-cut fixes and push; reply on
  the thread only when a suggestion is wrong or ambiguous.
- If the PR is green, approved, and conflict-free, report it as **merge-ready**.
  Do NOT merge — merging to `main` is the maintainer's call unless they have
  explicitly said otherwise in this session.

## 3. Pick up the next feature

Only if step 2 left nothing in flight that needs work:

- Look for the next feature in open issues (prefer labels `enhancement` /
  `feature`, oldest first).
- If there are no feature issues, do nothing — do not invent features.
- Implement the feature on a new `feat/<slug>` branch, keeping changes small
  and matching the existing plugin layout (`plugins/cloud-architecture-diagrams/…`).
- Run the lint/test commands above before pushing, then open a **draft PR**
  that references the issue.

## 4. Report

End with a short status: PRs touched and their state (fixed / merge-ready /
blocked), feature picked up (if any), and what the next pass should look at.
If a pass has nothing to do, say "idle" in one line — don't pad it.
