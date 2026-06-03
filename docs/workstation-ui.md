# MTBUDDY Workstation UI Mock

Last updated: 2026-06-03

## Purpose

The workstation UI should feel like a simple daily work buddy first, and an
inspectable agent workstation second. The default screen should not expose
execution internals, audit panels, or artifact grids until the user starts a
task or opens details.

The current mock is Tauri-ready but browser-verified. That keeps us moving
without requiring real MTT AIBOOK hardware, MTClaw installation, or a local
Rust/Tauri toolchain in this worktree.

## Product Shape

The first screen follows a WorkBuddy-style layout:

- Left sidebar: new task, assistant, experts, skills, connectors, automation,
  and more.
- Center welcome: MTBUDDY greeting plus a simple work-mode switch.
- Bottom composer: category chips, prompt box, tool chips, send controls, and
  workspace picker.

Advanced MTBUDDY concepts still matter, but they belong behind task details:

- Skills should appear as composer chips and a sidebar destination.
- Connectors should appear as an option, not a first-screen architecture panel.
- Permissions should stay visible as a compact control.
- MTClaw/OpenClaw/runtime details should be shown only in setup or run details.
- Artifacts and audit logs should appear after a task produces outputs.

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

The simple home screen does not remove the existing engine direction:

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
with Playwright, checks the simple home-screen elements, and rejects horizontal
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
