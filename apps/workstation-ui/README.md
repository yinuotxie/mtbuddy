# MTBUDDY Workstation UI

This is the Tauri-ready workstation mock for MTBUDDY. It uses React,
TypeScript, Vite, and lucide icons for the front-end shell. The current UI is a
deterministic mock around the existing CLI artifacts, MTClaw bridge, and skill
registry so the product direction can be judged before wiring live execution.

## Run The Mock

```bash
npm install
npm run dev
```

Open the printed local URL, usually:

```text
http://127.0.0.1:5173/
```

## Verify

```bash
npm run build
npm run test:smoke
```

The smoke test starts Vite on a temporary local port, renders desktop and
mobile viewports with Playwright, verifies the expected workstation panels, and
writes screenshots to `/tmp`.

## Tauri Shell

The `src-tauri/` folder contains the desktop wrapper scaffold. Running the
desktop shell requires the Rust toolchain and Tauri Linux prerequisites:

```bash
npm run tauri:dev
npm run tauri:build
```

This worktree does not currently have `rustc` or `cargo`, so the verified path
for now is the Vite browser mock.
