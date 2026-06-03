# MTBUDDY

MTBUDDY is a local-first personal AI workstation for MTT AIBOOK. It turns a
natural-language work request into auditable local artifacts: reports, action
lists, structured notes, and later UI-visible task timelines.

For the competition track, MTBUDDY is built around this runtime story:

```text
MTBUDDY workstation UI or CLI
  -> MTBUDDY core: workspace, artifacts, audit log
  -> OpenAI-compatible agent client
       -> OpenClaw as the flagship demo client
       -> Hermes / OpenCode / Codex-like direct clients through MTClaw
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
- Deterministic `pptx_skill` for creating a `.pptx` from a Markdown outline
  and reading slide text back for content QA.
- Local artifact output under `<workspace>/artifacts/`.
- Append-only JSONL audit log for every operation.
- OpenAI-compatible agent client abstraction.
- OpenClaw agent client.
- Direct MTClaw Function Router client.
- MTClaw Function Router tool definitions and wrapper scripts.
- End-to-end pytest coverage for the CLI and MTClaw tool entrypoint.
- Tauri-ready React workstation UI mock under `apps/workstation-ui`.

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

Create a PowerPoint artifact from the demo outline through the MTClaw tool
entrypoint:

```bash
printf '%s' '{"workspace":"./workspaces/demo","outline_path":"presentation-outline.md"}' \
  | python -m mtbuddy.mtclaw_tools mtbuddy_pptx_create_from_outline
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

## Workstation UI Mock

The first desktop UI pass is a Tauri-ready React mock. It runs in the browser
today and keeps the Tauri wrapper scaffold in place for Linux packaging once
Rust/Cargo and the Tauri system prerequisites are installed.

```bash
cd apps/workstation-ui
npm install
npm run dev
```

Build the UI mock:

```bash
cd apps/workstation-ui
npm run build
npm run test:smoke
```

The desktop shell commands are present, but not verified in this worktree
because `rustc` and `cargo` are not installed:

```bash
npm run tauri:dev
npm run tauri:build
```

## OpenAI-Compatible Agents And MTClaw

Automated tests use `--executor local` so they do not require OpenClaw, MTClaw,
DeepSeek, or AIBOOK hardware.

OpenClaw is the flagship competition path:

```bash
mtbuddy run --executor openclaw --workspace ./workspaces/demo \
  "Summarize these files and create an action list"
```

That command expects the `openclaw` CLI to be installed and configured with a
`mtbuddy` agent whose model provider points at MTClaw Function Router.

MTBUDDY can also call MTClaw directly through its OpenAI-compatible API:

```bash
export MTBUDDY_FUNCTION_ROUTER_BASE_URL=http://127.0.0.1:18790/v1
export MTBUDDY_FUNCTION_ROUTER_MODEL=function_router/function-router
mtbuddy run --executor function-router --workspace ./workspaces/demo \
  "Summarize these files and create an action list"
```

That same MTClaw provider surface can be used by Hermes, OpenCode, Codex-like
clients, or any agent/client that supports an OpenAI-compatible `base_url`.

MTClaw integration assets live in:

```text
integrations/mtclaw/functions.jsonl
integrations/mtclaw/scripts/
skills/pptx/SKILL.md
```

See [OpenAI-Compatible Agents And MTClaw Integration](docs/openclaw-mtclaw.md)
for the manual DeepSeek/Function Router setup path.

## Project Plan

- [Project plan](docs/plan.md)
- [OpenAI-compatible agents and MTClaw integration](docs/openclaw-mtclaw.md)
- [Workstation UI mock](docs/workstation-ui.md)
