# Cloud Architecture Diagrams — a portable Agent Skill

A Claude Code plugin that builds **editable cloud architecture diagrams** for
Azure/Microsoft, AWS, and GCP, exporting the **same diagram as both
`.excalidraw` and `.drawio`** with the official vendor icons embedded.

- ~3,900 icons bundled **offline**: AWS (809), Azure official (626), GCP (45),
  and the full Microsoft set (2,431 — Dynamics 365, Power Platform, Fabric,
  M365/Teams, Intune, Entra, Purview, …).
- Two inputs: describe the architecture in text, or upload a screenshot to
  recreate.
- Optional **native draw.io vector stencils** for AWS/GCP (`drawio_shapes`),
  while Excalidraw always uses embedded SVG.

This repository is a single-plugin **marketplace**, which is how Claude Code
plugins are distributed.

```
cloud-arch-marketplace/
├── .claude-plugin/
│   └── marketplace.json                 # lists the plugin
├── LICENSE                              # MIT (code only)
├── NOTICE.md                            # icon trademarks / attribution
└── plugins/
    └── cloud-architecture-diagrams/
        ├── .claude-plugin/
        │   └── plugin.json              # plugin manifest
        └── skills/
            └── cloud-architecture-diagrams/   # the skill (SKILL.md, scripts, assets…)
```

## Install in your agent

This is an [Agent Skill](https://agentskills.io) (`SKILL.md`), so the same skill
runs across several agents. Pick your tool:

### Claude Code

Add via Git (relative plugin paths only resolve for git-added marketplaces, not
raw `marketplace.json` URLs):

```
/plugin marketplace add hansraj316/cloud-arch-marketplace
/plugin install cloud-architecture-diagrams@cloud-arch-marketplace
```

Test from a local clone first if you like:

```
/plugin marketplace add /path/to/cloud-arch-marketplace
/plugin install cloud-architecture-diagrams@cloud-arch-marketplace
```

### GitHub Copilot CLI

Copilot reads the same `.claude-plugin/marketplace.json`:

```
copilot plugin marketplace add hansraj316/cloud-arch-marketplace
copilot plugin install cloud-architecture-diagrams
```

(Copilot also auto-discovers skills placed under `.github/skills`, `.claude/skills`,
or `~/.copilot/skills`.)

### OpenClaw (via ClawHub)

Published to ClawHub as a curated-icon build (trimmed to fit ClawHub's per-publish
file limits; the full ~3,900-icon set ships in this repo for Claude Code / Copilot /
Hermes):

```
openclaw skills install cloud-architecture-diagrams
# or:  clawhub install cloud-architecture-diagrams
```

Page: https://clawhub.ai/hansraj316/cloud-architecture-diagrams

### Hermes (Nous Research)

Hermes installs Agent Skills from GitHub taps and Claude-marketplace repos:

```
hermes skills tap add hansraj316/cloud-arch-marketplace
hermes skills install hansraj316/cloud-arch-marketplace/cloud-architecture-diagrams
```

Once installed in any of these, the skill activates automatically when you ask the
agent to draw or recreate an Azure/AWS/GCP architecture diagram.

## Use it

> "Draw an AWS 3-tier web app: users → CloudFront + ALB → EC2 auto-scaling →
> RDS, with S3 for static assets, all in a VPC. Give me .drawio and .excalidraw."

Claude asks which cloud if it's ambiguous, resolves the icons, builds the spec,
generates both files, and renders a preview to check.

## Publish

1. Push the **contents of this folder** to a git repo root (so
   `.claude-plugin/marketplace.json` is at the top).
2. Share the repo; users install with the commands above.
3. (Optional) Submit to Anthropic's community marketplace for wider discovery:
   run `claude plugin validate ./plugins/cloud-architecture-diagrams` first, then
   use the in-app form at `claude.ai/settings/plugins/submit` or
   `platform.claude.com/plugins/submit`.

## License & trademarks

Code/scripts: MIT (see `LICENSE`). Bundled vendor icons are **not** MIT — they
belong to AWS, Microsoft, and Google under their own icon-usage terms. This is
an independent tool, not affiliated with or endorsed by those companies. See
`NOTICE.md`.
