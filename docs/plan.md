# MTBUDDY Project Plan

Last updated: 2026-06-03

## Product Thesis

MTBUDDY is not another chat UI. It is a personal AI workstation that accepts a
work request, routes it to skills, executes local tools, and returns verifiable
outputs. The competition angle is:

> A local-first "fast, accurate, decisive" personal AI workstation inspired by
> MTClaw, built for MTT AIBOOK and MTT AIOS.

The first build should prove the core workflow without requiring real MTT
AIBOOK hardware:

1. Understand a natural-language work request.
2. Decompose it into typed steps.
3. Route each step to a skill.
4. Execute local tools with permission and audit logs.
5. Deliver files the user can inspect.
6. Measure success with repeatable eval tasks.

## Current Constraints

- We do not have physical MTT AIBOOK hardware yet.
- MTClaw is a competition requirement, so the product must expose a real
  OpenAI-compatible agent path through MTClaw early.
- The first implementation still keeps `LocalExecutor` for deterministic tests
  and offline development.
- AIBOOK's local LLM surface appears OpenAI-compatible, so model access should
  be abstracted behind a provider interface.
- DeepSeek is the near-term cloud model provider while AIBOOK hardware is not
  available.

## Architecture Direction

```text
User request
  -> Workstation UI
  -> MTBUDDY core
  -> OpenAI-compatible agent client
       -> OpenClawAgentClient
       -> FunctionRouterAgentClient
       -> Hermes / OpenCode / Codex-like clients through MTClaw
  -> MTClaw Function Router provider
  -> Planner / Skill router
  -> Executor
       -> LocalExecutor
       -> AgentExecutor
  -> Artifact store
  -> Audit log
  -> Evaluation report
```

Core interfaces:

- `LLMProvider`: DeepSeek now, OpenAI-compatible API, Ollama, vLLM, future
  AIBOOK `musachat_local`.
- `Skill`: typed input, typed output, declared permissions, artifact contract.
- `Executor`: runs shell/browser/file/document actions with logs.
- `ArtifactStore`: stores generated documents, sheets, slides, reports, and
  source references.
- `EvalRunner`: runs fixed tasks and checks outputs.

## First Milestone: Proof Of Workstation

Goal: a local app that can complete one real work request end to end.

Recommended first demo:

> "Read this folder of mixed meeting notes and CSV files, summarize the key
> decisions, create an action list, generate a one-page report, and save the
> outputs."

Why this first:

- It exercises file access, reading, planning, document generation, and audit.
- It avoids brittle GUI automation in the first week.
- It creates visible deliverables for judges.
- It maps cleanly to future MTClaw skill routing.

Definition of done:

- User can submit the task from the CLI first, then the workstation UI.
- Agent creates a structured plan before execution.
- User sees requested permissions before filesystem changes.
- System reads local files from an allowed workspace.
- System writes a Markdown report and action-item CSV.
- Every tool call is recorded in an audit log.
- A small eval verifies that expected artifacts exist and include required
  sections.

## MVP Scope

### Include

- CLI-first core, then Tauri workstation UI.
- Chat/task panel with live execution timeline.
- Local file workspace picker.
- Basic planner and skill router.
- File skill: list, read, write, classify.
- Document skill: Markdown report generation.
- Sheet skill: CSV read/write and simple analysis.
- Audit log viewer.
- Eval runner with at least 10 fixed tasks.
- Linux packaging path documented from day one.

### Defer

- Full desktop GUI control.
- Voice wake word.
- Digital human avatar.
- Complex browser automation.
- Heavy local model hosting inside the app.

## Technology Recommendation

Use a pragmatic stack that can ship quickly and package cleanly:

- App shell: Tauri.
- Frontend: React + TypeScript.
- Backend: Python FastAPI or Node/TypeScript service.
- Skills: Python where document/data libraries are strongest.
- Packaging: Linux AppImage first, `.deb` second.
- Model interface: OpenAI-compatible API client.
- Local evals: pytest or vitest plus artifact checks.

Preferred path:

1. Use a web UI during early iteration.
2. Wrap it in Tauri/Electron after the workflow is stable.
3. Keep skill execution in a backend process so the UI stays replaceable.

## Skill Roadmap

Build skills as boring, testable units.

1. `file_skill`
   - List files.
   - Read allowed file types.
   - Classify and rename in dry-run mode.
   - Write outputs to an artifact directory.

2. `doc_skill`
   - Generate Markdown reports.
   - Later export to DOCX/PDF.

3. `sheet_skill`
   - Read CSV/XLSX.
   - Produce summary statistics.
   - Write CSV/XLSX outputs.

4. `ppt_skill`
   - Generate outline first.
   - Export PPTX after doc and sheet flows are stable.

5. `rag_skill`
   - Local ingestion.
   - Chunking and retrieval.
   - Source citations.

6. `browser_research_skill`
   - Controlled web research.
   - Capture sources.
   - Produce traceable notes.

7. `openai_agent_mtclaw_adapter`
   - Register MTBUDDY tools with MTClaw Function Router.
   - Run the competition agent path through OpenClaw.
   - Support direct Function Router calls for any OpenAI-compatible client.
   - Maintain deterministic local tests through the `Executor` interface.

## Evaluation Plan

The eval suite is part of the product, not a later add-on.

Metrics:

- Task success rate.
- Time to completion.
- Tool-call count.
- Number of user confirmations.
- Artifact existence and structure.
- Source/reference coverage.
- Failure reason category.

Initial eval set:

- 3 file organization tasks.
- 3 document summary/report tasks.
- 2 CSV analysis tasks.
- 1 mixed folder-to-report task.
- 1 permission-denial safety task.

Each eval should have:

- Input fixture.
- User request.
- Expected artifacts.
- Automated checks.
- Human-readable result report.

## Repository Plan

Initial structure:

```text
docs/
  plan.md
  architecture.md
  evals.md
apps/
  workstation-ui/
services/
  agent-core/
skills/
  file/
  doc/
  sheet/
evals/
  fixtures/
  tasks/
  reports/
packages/
  linux/
```

Do not create all folders immediately unless they are used by the first slice.
The first implementation wave should introduce only the CLI core,
OpenAI-compatible agent client abstraction, OpenClaw / MTClaw integration
assets, file skill, document skill, sheet skill, and eval fixtures required for
the proof workflow.

## First Implementation Slice

1. Create the minimal app skeleton.
2. Add a local task workspace under `workspaces/demo`.
3. Implement `Skill` and `Executor` interfaces.
4. Implement `file_skill` read/list/write operations.
5. Implement `doc_skill` Markdown output.
6. Implement `sheet_skill` action-item CSV output.
7. Add audit logging for every operation.
8. Add the OpenAI-compatible agent client abstraction.
9. Add MTClaw Function Router tool definitions and wrappers.
10. Add one end-to-end eval fixture.
11. Run the eval from CLI.
12. Add UI only after CLI workflow passes.
13. Package only after the workflow is stable.

## Risks And Mitigations

- Risk: OpenAI-compatible agent runtimes or MTClaw are not installed in CI.
  - Mitigation: keep `LocalExecutor` as the deterministic test path and make
    agent clients fail fast with setup instructions.

- Risk: app looks like a generic assistant.
  - Mitigation: emphasize execution timeline, local artifacts, eval metrics, and
    AIBOOK/AIOS compatibility in docs and demo.

- Risk: too many skills, none complete.
  - Mitigation: first demo uses only file, doc, sheet, and audit.

- Risk: local file operations feel unsafe.
  - Mitigation: workspace allowlist, dry-run previews, explicit confirmations,
    and immutable audit logs.

## Immediate Next Step

Start with a CLI-first vertical slice:

```text
mtbuddy run --executor local --workspace ./workspaces/demo \
  "Summarize these files and create an action list"
```

This gives us a deterministic base for tests and evals. Once this works, build
the workstation UI around the same backend API.
