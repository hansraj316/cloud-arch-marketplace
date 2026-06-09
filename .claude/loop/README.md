# Loop engineering setup

A small system that finds the work, hands it to the agent, checks the result,
records what happened, and decides the next move — on its own. (Pattern after
[@0xCodez's loop-engineering roadmap](https://x.com/0xcodez/status/2064374643729773029).)

## The pieces

| Building block | In this repo |
|---|---|
| Automation (heartbeat) | `/loop 30m /integrate-features` — or, in a remote session, PR-activity subscriptions plus a persistent heartbeat monitor |
| Skill (reused context) | `CLAUDE.md` (project context) + `.claude/commands/integrate-features.md` (the workflow itself) |
| State file | `.claude/loop/STATE.md` — read at the start of every pass, appended before it ends |
| Objective gate | `.claude/loop/gate.sh` — exact mirror of `daily-ci.yml`; nothing is pushed without `GATE PASS` |
| Worktrees | passes touch other branches via `git worktree add`, never by switching the main checkout |
| Connectors | GitHub MCP (PRs, CI logs, issues) |
| Verifier sub-agent | `.claude/agents/loop-verifier.md` — read-only reviewer; the maker never grades its own homework |

## Start the loop

```
/loop 30m /integrate-features
```

One pass manually: `/integrate-features`. Get a manual run reliable before
scheduling it.

## Feed the loop

File issues labeled `enhancement` or `feature`. With nothing in flight and an
empty backlog, a pass reports "idle" and costs almost nothing.

## Guardrails

- The loop never merges to `main` — it drives PRs to merge-ready and stops.
- Failing gate = nothing ships. No silent retries past a red gate
  (no Ralph Wiggum loops).
- Every pass leaves a one-line record in `STATE.md`, so any session — or a
  human — can reconstruct what the loop did and why.
