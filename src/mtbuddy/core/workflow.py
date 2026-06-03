"""Shared workspace workflow helpers."""

from __future__ import annotations

from pathlib import Path

from ..skills.file_skill import FileSkill
from .analysis import SourceDocument, WorkspaceAnalysis, analyze_workspace
from .audit import JsonlAuditLog


AUDIT_LOG_RELATIVE_PATH = Path("artifacts") / "audit.jsonl"


def create_audit_log(workspace: Path) -> JsonlAuditLog:
    return JsonlAuditLog(workspace / AUDIT_LOG_RELATIVE_PATH)


def read_allowed_sources(workspace: Path, audit_log: JsonlAuditLog) -> list[SourceDocument]:
    file_skill = FileSkill(workspace, audit_log)
    return [file_skill.read_file(file.path) for file in file_skill.list_files()]


def analyze_allowed_sources(
    workspace: Path,
    audit_log: JsonlAuditLog,
    request: str,
) -> WorkspaceAnalysis:
    sources = read_allowed_sources(workspace, audit_log)
    audit_log.record(
        "analysis.extract",
        details={
            "source_count": len(sources),
            "request": request,
        },
    )
    return analyze_workspace(request, sources)
