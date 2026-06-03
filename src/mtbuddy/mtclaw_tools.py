"""JSON-stdin tool entrypoints for MTClaw Function Router wrappers."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

from .core.artifacts import WorkspaceArtifactStore
from .core.executor import LocalExecutor
from .core.workflow import analyze_allowed_sources, create_audit_log
from .core.workspace import resolve_workspace
from .skills.doc_skill import DocSkill
from .skills.file_skill import FileSkill
from .skills.pptx_skill import PptxSkill
from .skills.sheet_skill import SheetSkill


ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]

RUN_WORKSPACE_TOOL = "mtbuddy_run_workspace"
LIST_FILES_TOOL = "mtbuddy_list_files"
READ_FILE_TOOL = "mtbuddy_read_file"
GENERATE_REPORT_TOOL = "mtbuddy_generate_report"
WRITE_ACTION_CSV_TOOL = "mtbuddy_write_action_csv"
PPTX_CREATE_FROM_OUTLINE_TOOL = "mtbuddy_pptx_create_from_outline"
PPTX_READ_TEXT_TOOL = "mtbuddy_pptx_read_text"


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if len(args) != 1:
        return _error("usage: python -m mtbuddy.mtclaw_tools <tool_name>")

    tool_name = args[0]
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        return _error(f"invalid JSON input: {exc.msg}")

    try:
        result = dispatch(tool_name, payload)
    except Exception as exc:
        return _error(str(exc))

    print(json.dumps(result, sort_keys=True))
    return 0


def dispatch(tool_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        handler = TOOL_HANDLERS[tool_name]
    except KeyError as exc:
        raise ValueError(f"unknown MTBUDDY MTClaw tool: {tool_name}") from exc
    return handler(payload)


def _run_workspace(payload: dict[str, Any]) -> dict[str, Any]:
    workspace = _workspace_from(payload)
    request = str(payload.get("request") or "")
    if not request:
        raise ValueError("missing request")
    result = LocalExecutor().run(workspace, request)
    return {"result": "ok", "artifacts": result.to_dict()["artifacts"]}


def _list_files(payload: dict[str, Any]) -> dict[str, Any]:
    workspace, audit = _workspace_and_audit(payload)
    files = FileSkill(workspace, audit).list_files()
    return {
        "result": "ok",
        "files": [
            {
                "path": item.relative_path,
                "kind": item.kind,
                "size_bytes": item.size_bytes,
            }
            for item in files
        ],
    }


def _read_file(payload: dict[str, Any]) -> dict[str, Any]:
    workspace, audit = _workspace_and_audit(payload)
    relative_path = str(payload.get("path") or "")
    if not relative_path:
        raise ValueError("missing path")
    source = FileSkill(workspace, audit).read_file(workspace / relative_path)
    return {
        "result": "ok",
        "path": source.path,
        "kind": source.kind,
        "content": source.content,
    }


def _generate_report(payload: dict[str, Any]) -> dict[str, Any]:
    workspace, audit = _workspace_and_audit(payload)
    request = str(payload.get("request") or "Summarize this workspace")
    analysis = analyze_allowed_sources(workspace, audit, request)
    artifact_store = WorkspaceArtifactStore(workspace, audit)
    report_path = DocSkill(artifact_store, audit).write_report(analysis)
    return {"result": "ok", "report": str(report_path)}


def _write_action_csv(payload: dict[str, Any]) -> dict[str, Any]:
    workspace, audit = _workspace_and_audit(payload)
    request = str(payload.get("request") or "Create action items")
    analysis = analyze_allowed_sources(workspace, audit, request)
    artifact_store = WorkspaceArtifactStore(workspace, audit)
    csv_path = SheetSkill(artifact_store, audit).write_action_items(analysis.action_items)
    return {
        "result": "ok",
        "action_items": str(csv_path),
        "count": len(analysis.action_items),
    }


def _pptx_create_from_outline(payload: dict[str, Any]) -> dict[str, Any]:
    workspace, audit = _workspace_and_audit(payload)
    outline_path = str(payload.get("outline_path") or "")
    if not outline_path:
        raise ValueError("missing outline_path")
    output_name = str(payload.get("output_name") or "presentation.pptx")
    title = payload.get("title")
    artifact_store = WorkspaceArtifactStore(workspace, audit)
    pptx_path = PptxSkill(workspace, artifact_store, audit).create_from_outline(
        workspace / outline_path,
        output_name=output_name,
        title=str(title) if title else None,
    )
    return {"result": "ok", "presentation": str(pptx_path)}


def _pptx_read_text(payload: dict[str, Any]) -> dict[str, Any]:
    workspace, audit = _workspace_and_audit(payload)
    path = str(payload.get("path") or "")
    if not path:
        raise ValueError("missing path")
    artifact_store = WorkspaceArtifactStore(workspace, audit)
    return PptxSkill(workspace, artifact_store, audit).read_text(workspace / path)


def _workspace_and_audit(payload: dict[str, Any]):
    workspace = resolve_workspace(_workspace_from(payload))
    return workspace, create_audit_log(workspace)


def _workspace_from(payload: dict[str, Any]) -> Path:
    raw_workspace = payload.get("workspace")
    if not raw_workspace:
        raise ValueError("missing workspace")
    return Path(str(raw_workspace))


def _error(message: str) -> int:
    print(json.dumps({"error": message}, sort_keys=True))
    return 1


TOOL_HANDLERS: dict[str, ToolHandler] = {
    RUN_WORKSPACE_TOOL: _run_workspace,
    LIST_FILES_TOOL: _list_files,
    READ_FILE_TOOL: _read_file,
    GENERATE_REPORT_TOOL: _generate_report,
    WRITE_ACTION_CSV_TOOL: _write_action_csv,
    PPTX_CREATE_FROM_OUTLINE_TOOL: _pptx_create_from_outline,
    PPTX_READ_TEXT_TOOL: _pptx_read_text,
}


if __name__ == "__main__":
    raise SystemExit(main())
