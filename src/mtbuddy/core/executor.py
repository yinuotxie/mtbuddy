"""Execution backends for MTBUDDY."""

from __future__ import annotations

from pathlib import Path

from ..skills.doc_skill import DocSkill
from ..skills.file_skill import FileSkill
from ..skills.sheet_skill import SheetSkill
from .analysis import analyze_workspace
from .artifacts import WorkspaceArtifactStore
from .audit import JsonlAuditLog
from .interfaces import RunResult
from .workspace import resolve_workspace


class LocalExecutor:
    """Deterministic executor for local development, tests, and offline demos."""

    name = "local"

    def run(self, workspace: Path, request: str) -> RunResult:
        resolved_workspace = resolve_workspace(workspace)
        audit_log = JsonlAuditLog(resolved_workspace / "artifacts" / "audit.jsonl")
        audit_log.record(
            "run.start",
            details={
                "executor": self.name,
                "request": request,
                "workspace": str(resolved_workspace),
            },
        )
        audit_log.record("workspace.allow", details={"path": str(resolved_workspace)})

        artifact_store = WorkspaceArtifactStore(resolved_workspace, audit_log)
        file_skill = FileSkill(resolved_workspace, audit_log)
        doc_skill = DocSkill(artifact_store, audit_log)
        sheet_skill = SheetSkill(artifact_store, audit_log)

        files = file_skill.list_files()
        sources = [file_skill.read_file(file.path) for file in files]

        audit_log.record(
            "analysis.extract",
            details={
                "source_count": len(sources),
                "request": request,
            },
        )
        analysis = analyze_workspace(request, sources)
        report_path = doc_skill.write_report(analysis)
        action_csv_path = sheet_skill.write_action_items(analysis.action_items)
        audit_log.record(
            "run.complete",
            details={
                "report": str(report_path),
                "action_items": str(action_csv_path),
                "audit_log": str(audit_log.path),
            },
        )

        return RunResult(
            workspace=resolved_workspace,
            request=request,
            artifacts={
                "report": report_path,
                "action_items": action_csv_path,
                "audit_log": audit_log.path,
            },
        )
