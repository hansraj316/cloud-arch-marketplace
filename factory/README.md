# Software factory in this repo

Issues labeled `factory` become small draft PRs. You merge; the factory never does.

## Install (once per machine)

```
gh auth login && gh auth setup-git
claude plugin marketplace add hansraj316/software-factory
claude plugin install software-factory@software-factory --scope project
uv tool install sddgrade --from git+https://github.com/hansraj316/sdd-grader.git@a9b081511a1b715028252cf64c85829cb6c2384f
```

## Use

```
/factory dry-run    # free: what a run would do, no model calls, no GitHub writes
/factory once       # one job
/factory run        # drain the queue within today's budget
/factory status
```

If `/factory` isn't found, use `/software-factory:factory run`.

## Files

- `config.json`: budget, label, protected paths, gate threshold. Protected.
- `checks.sh`: the build gate, mirroring CI, with `# factory-check:` names. Protected.
- `jobs/`, `worktrees/`, `ledger.jsonl`: local state, git-ignored.

Changes to anything in `factory/` land as their own PR that you merge; the
factory's agents can't edit them.
