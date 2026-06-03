# MTBUDDY

MTBUDDY is a local-first personal AI workstation for MTT AIBOOK. It turns a
natural-language work request into auditable local artifacts: reports, action
lists, structured notes, and later UI-visible task timelines.

For the competition track, MTBUDDY is built around this runtime story:

```text
MTBUDDY workstation UI or CLI
  -> MTBUDDY core: workspace, artifacts, audit log
  -> OpenClaw agent runtime
  -> MTClaw Function Router provider
  -> DeepSeek API now
  -> AIBOOK local model endpoint later
```

The first slice is CLI-first so the engine is deterministic and testable before
the Tauri desktop UI is built.

## What Works Now

- `mtbuddy run` CLI.
- Demo workspace under `workspaces/demo` with Markdown, text, and CSV inputs.
- Workspace allowlist and safe local file reads.
- Core interfaces for `Skill`, `Executor`, `ArtifactStore`, `AuditLog`, and
  `LLMProvider`.
- Deterministic `file_skill`, `doc_skill`, and `sheet_skill`.
- Local artifact output under `<workspace>/artifacts/`.
- Append-only JSONL audit log for every operation.
- OpenClaw executor seam.
- MTClaw Function Router tool definitions and wrapper scripts.
- End-to-end pytest coverage for the CLI and MTClaw tool entrypoint.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
```

## Run The Demo

```bash
mtbuddy run --executor local --workspace ./workspaces/demo \
  "Summarize these files and create an action list"
```

Expected artifacts:

```text
workspaces/demo/artifacts/report.md
workspaces/demo/artifacts/action-items.csv
workspaces/demo/artifacts/audit.jsonl
```

Use JSON output for automation:

```bash
mtbuddy run --executor local --workspace ./workspaces/demo \
  "Summarize these files and create an action list" --json
```

## Test

```bash
python -m pytest
```

The test suite copies the demo workspace to a temp directory, runs the real CLI,
and verifies the report sections, action CSV, and audit operations.

## OpenClaw And MTClaw

Automated tests use `--executor local` so they do not require OpenClaw, MTClaw,
DeepSeek, or AIBOOK hardware. The competition path uses OpenClaw and MTClaw:

```bash
mtbuddy run --executor openclaw --workspace ./workspaces/demo \
  "Summarize these files and create an action list"
```

That command expects the `openclaw` CLI to be installed and configured with a
`mtbuddy` agent whose model provider points at MTClaw Function Router.

MTClaw integration assets live in:

```text
integrations/mtclaw/functions.jsonl
integrations/mtclaw/scripts/
```

See [OpenClaw And MTClaw Integration](docs/openclaw-mtclaw.md) for the manual
DeepSeek/Function Router setup path.

## Project Plan

- [Project plan](docs/plan.md)
- [OpenClaw and MTClaw integration](docs/openclaw-mtclaw.md)
