"""JSON-stdin tool entrypoints for MTClaw Function Router wrappers."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .core.audit import JsonlAuditLog
from .core.analysis import analyze_workspace
from .core.artifacts import WorkspaceArtifactStore
from .core.executor import LocalExecutor
from .core.workspace import resolve_workspace
from .skills.doc_skill import DocSkill
from .skills.file_skill import FileSkill
from .skills.sheet_skill import SheetSkill


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
    if tool_name == "mtbuddy_run_workspace":
        workspace = _workspace_from(payload)
        request = str(payload.get("request") or "")
        if not request:
            raise ValueError("missing request")
        result = LocalExecutor().run(workspace, request)
        return {"result": "ok", "artifacts": result.to_dict()["artifacts"]}

    if tool_name == "mtbuddy_list_files":
        workspace = resolve_workspace(_workspace_from(payload))
        audit = JsonlAuditLog(workspace / "artifacts" / "audit.jsonl")
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

    if tool_name == "mtbuddy_read_file":
        workspace = resolve_workspace(_workspace_from(payload))
        relative_path = str(payload.get("path") or "")
        if not relative_path:
            raise ValueError("missing path")
        audit = JsonlAuditLog(workspace / "artifacts" / "audit.jsonl")
        source = FileSkill(workspace, audit).read_file(workspace / relative_path)
        return {
            "result": "ok",
            "path": source.path,
            "kind": source.kind,
            "content": source.content,
        }

    if tool_name == "mtbuddy_generate_report":
        workspace = resolve_workspace(_workspace_from(payload))
        request = str(payload.get("request") or "Summarize this workspace")
        audit = JsonlAuditLog(workspace / "artifacts" / "audit.jsonl")
        analysis = _build_analysis(workspace, audit, request)
        store = WorkspaceArtifactStore(workspace, audit)
        report_path = DocSkill(store, audit).write_report(analysis)
        return {"result": "ok", "report": str(report_path)}

    if tool_name == "mtbuddy_write_action_csv":
        workspace = resolve_workspace(_workspace_from(payload))
        request = str(payload.get("request") or "Create action items")
        audit = JsonlAuditLog(workspace / "artifacts" / "audit.jsonl")
        analysis = _build_analysis(workspace, audit, request)
        store = WorkspaceArtifactStore(workspace, audit)
        csv_path = SheetSkill(store, audit).write_action_items(analysis.action_items)
        return {
            "result": "ok",
            "action_items": str(csv_path),
            "count": len(analysis.action_items),
        }

    raise ValueError(f"unknown MTBUDDY MTClaw tool: {tool_name}")


def _build_analysis(workspace: Path, audit: JsonlAuditLog, request: str):
    file_skill = FileSkill(workspace, audit)
    sources = [file_skill.read_file(item.path) for item in file_skill.list_files()]
    audit.record("analysis.extract", details={"source_count": len(sources), "request": request})
    return analyze_workspace(request, sources)


def _workspace_from(payload: dict[str, Any]) -> Path:
    raw_workspace = payload.get("workspace")
    if not raw_workspace:
        raise ValueError("missing workspace")
    return Path(str(raw_workspace))


def _error(message: str) -> int:
    print(json.dumps({"error": message}, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
