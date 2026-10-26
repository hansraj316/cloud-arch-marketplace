# Cloud Architecture Diagrams

Build editable cloud architecture diagrams for Azure / Microsoft, AWS and GCP with the official vendor icons, exported as **both** `.excalidraw` and `.drawio` from one small spec. Describe the architecture in text, or paste a sketch or screenshot to recreate it.

- About 5,500 official icons bundled offline: AWS, Azure, GCP, the broad Microsoft set (Dynamics 365, Power Platform, Teams, Entra, Intune, Purview) and the Microsoft Fabric Fluent set.
- One spec of zones, nodes and edges renders both files identically, with icons embedded so they open offline at excalidraw.com or app.diagrams.net.
- Optional native draw.io vector stencils for AWS and GCP.
- Spec validation, an auto-layout engine for nodes without coordinates, and a PNG preview.

## How it works

The skill (`skills/cloud-architecture-diagrams/SKILL.md`) tells Claude to write a spec and run the bundled Python scripts with **Python 3.10 or newer**:

- `scripts/build_diagram.py` renders a spec to `.excalidraw` and `.drawio`, validates it, and can auto-lay it out.
- `scripts/find_icon.py` and `scripts/find_drawio_shape.py` search the bundled icon index by service name.
- `scripts/preview_png.py` renders a PNG preview of an `.excalidraw` file.

Everything above runs locally on the bundled files and makes no network calls. Two maintenance scripts, `scripts/build_icon_index.py` and `scripts/add_icon_pack.py`, are only for refreshing the icon set: the first downloads icon metadata and SVGs from msicons.com, the second imports a vendor icon pack you downloaded yourself. Neither runs during normal use.

The index in `references/icon-index.json` keeps one copy of each icon; where two providers ship the same file, both entries point at that one copy.

## Install

At the prompt of a Claude Code session:

```
/plugin install cloud-architecture-diagrams --marketplace hansraj316/cloud-arch-marketplace
```

Icons remain the trademarks of their vendors; see `NOTICE.md` at the repository root. Code is MIT licensed.
