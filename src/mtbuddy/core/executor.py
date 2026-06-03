"""Execution backends for MTBUDDY."""

from __future__ import annotations

from pathlib import Path

from ..skills.doc_skill import DocSkill
from ..skills.sheet_skill import SheetSkill
from .artifacts import WorkspaceArtifactStore
from .interfaces import RunResult
from .workflow import analyze_allowed_sources, create_audit_log
from .workspace import resolve_workspace


class LocalExecutor:
    """Deterministic executor for local development, tests, and offline demos."""

    name = "local"

    def run(self, workspace: Path, request: str) -> RunResult:
        resolved_workspace = resolve_workspace(workspace)
        audit_log = create_audit_log(resolved_workspace)
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
        analysis = analyze_allowed_sources(resolved_workspace, audit_log, request)
        report_path = DocSkill(artifact_store, audit_log).write_report(analysis)
        action_csv_path = SheetSkill(artifact_store, audit_log).write_action_items(analysis.action_items)
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
