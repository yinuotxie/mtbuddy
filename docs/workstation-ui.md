# MTBUDDY Workstation UI Mock

Last updated: 2026-06-03

## Purpose

The workstation UI should make MTBUDDY feel like an inspectable local workbench:
the user points it at a workspace, submits a task, watches skills execute, and
opens generated artifacts with an audit trail beside them.

The first mock is Tauri-ready but browser-verified. That keeps us moving without
requiring real MTT AIBOOK hardware, MTClaw installation, or a local Rust/Tauri
toolchain in this worktree.

## Product Shape

The mock uses three persistent work areas:

- Left rail: current workspace, allowed source files, registered skills, and
  the selected agent bridge.
- Center workbench: task request, executor switch, run metrics, and execution
  timeline.
- Right rail: artifact list, artifact preview, and run ledger.

This structure is deliberate. Judges should see the local files, the skill
routing, the generated files, and the audit evidence without digging through a
chat transcript.

## Runtime Direction

The current UI data is deterministic mock state. The live version should keep
the same boundaries:

```text
Tauri window
  -> React workstation UI
  -> local backend sidecar or localhost service
  -> MTBUDDY Python core
  -> LocalExecutor or AgentExecutor
  -> workspace artifacts and audit log
```

The executor switch in the UI maps to the existing CLI direction:

- `LocalExecutor`: deterministic offline mode for tests and demos.
- `MTClaw`: direct Function Router provider path.
- `OpenClaw`: flagship competition agent path through the MTClaw provider.

## Run

```bash
cd apps/workstation-ui
npm install
npm run dev
```

## Verify

```bash
cd apps/workstation-ui
npm run build
npm run test:smoke
```

The smoke test launches the mock locally, renders desktop and mobile viewports
with Playwright, checks for the expected artifact panels, and rejects horizontal
overflow.

## Desktop Shell

The `apps/workstation-ui/src-tauri` scaffold targets Tauri v2 and Linux bundles
(`appimage`, `deb`). Desktop commands are available:

```bash
npm run tauri:dev
npm run tauri:build
```

They require Rust/Cargo and Tauri Linux prerequisites, which are not installed
in the current worktree environment.
