# Feature Specification: build_diagram.py version flag

## Problem Statement

Rendering bug reports don't say which version of the diagram skill produced the output, so a maintainer can't tell whether a bug is already fixed.

## Scope

This change covers the build_diagram.py command line only: a new --version flag. Diagram rendering, the spec schema and the icon packs are unchanged.

## Stakeholders

- Diagram user: runs build_diagram.py and files rendering bugs; needs the version in one command.
- Maintainer: triages bug reports; needs every report to name a version.

## Glossary

- Plugin manifest: plugins/cloud-architecture-diagrams/.claude-plugin/plugin.json, which holds the skill's version field.
- Smoke render: the gate step that builds assets/spec-example.json to .excalidraw and .drawio files.

## User Scenarios & Testing

### User Story 1 - Print the skill version (Priority: P1)

As a diagram user filing a rendering bug, I want build_diagram.py to print the skill version so that I can include it in the bug report.

**Acceptance Scenarios**:

1. **Given** the skill is checked out, **When** the diagram user runs build_diagram.py --version, **Then** the version prints and the command exits successfully.

### Edge Cases

- Running with --version and a spec path prints only the version and builds no files.

## Requirements

### Functional Requirements

- FR-001: When called with --version, build_diagram.py shall print the version field of the plugin manifest.
- FR-002: When called with --version, build_diagram.py shall exit with code 0 without reading a spec file.
- FR-003: When called with a spec path and no --version, build_diagram.py shall write the same output files as the base branch writes.

## External Interfaces

- Command line: build_diagram.py gains one flag, --version. No other flag changes.
- Plugin manifest: read only, for its version field.

## Acceptance Criteria

- AC-001 [FR-001] [check: tests -> plugins/cloud-architecture-diagrams/skills/cloud-architecture-diagrams/tests/test_version.py] Given the plugin manifest version 1.2.3, when the diagram user runs build_diagram.py --version, then standard output is exactly "1.2.3".
- AC-002 [FR-002] [check: tests -> plugins/cloud-architecture-diagrams/skills/cloud-architecture-diagrams/tests/test_version.py] Given no spec path, when the diagram user runs build_diagram.py --version, then the exit code is 0.
- AC-003 [FR-003] [check: smoke] Given assets/spec-example.json, when the gate runs the smoke render, then both output files are non-empty and validation passes.

## Success Criteria

### Measurable Outcomes

- 2 new tests pass and 0 existing tests fail.
- The smoke render of assets/spec-example.json writes 2 non-empty files.

## Assumptions

- The plugin manifest holds the single version number for the skill.

## Out of Scope

- Changing how the version number is set or bumped.

## Revision History

| Version | Date | Change |
|---|---|---|
| 1 | 2026-11-21 | First draft from the sample issue |
