# cloud-arch-marketplace

Claude Code plugin marketplace with one plugin: `cloud-architecture-diagrams`
(builds editable Azure/AWS/GCP architecture diagrams as `.excalidraw` +
`.drawio` with vendor icons).

## Layout

- `.claude-plugin/marketplace.json` — marketplace manifest
- `plugins/cloud-architecture-diagrams/skills/cloud-architecture-diagrams/` —
  the skill: `SKILL.md`, `scripts/` (Python ≥3.10), `tests/`, `assets/`
- `.claude/loop/` — feature-integration loop: state file, gate, docs

## Quality gate

CI (`.github/workflows/daily-ci.yml`) runs on every push/PR and daily.
Run the same gate locally before any push:

```
.claude/loop/gate.sh
```

(ruff → black --check → mypy → pytest → build smoke test, executed inside
the skill directory). Requires `pip install ruff black mypy pytest`.

## Conventions

- Feature branches: `feat/<slug>`; CI fixes: `fix/ci-<date>`. PRs open as drafts.
- Never merge to `main` without the maintainer's explicit say-so.
- Use `git worktree` for parallel checkouts (e.g. fixing another PR's branch)
  instead of switching the main checkout.
- Bundled vendor icons are not MIT-licensed — don't add icon packs without
  updating `NOTICE.md`.
