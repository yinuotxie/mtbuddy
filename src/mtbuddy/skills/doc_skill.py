"""Markdown document generation skill."""

from __future__ import annotations

from pathlib import Path

from ..core.analysis import WorkspaceAnalysis
from ..core.interfaces import ArtifactStore, AuditLog


class DocSkill:
    """Generate deterministic Markdown reports."""

    name = "doc_skill"

    def __init__(self, artifact_store: ArtifactStore, audit_log: AuditLog) -> None:
        self._artifact_store = artifact_store
        self._audit_log = audit_log

    def permissions(self) -> list[str]:
        return ["Write Markdown reports under the workspace artifacts directory."]

    def write_report(self, analysis: WorkspaceAnalysis) -> Path:
        content = render_report(analysis)
        path = self._artifact_store.write_text("report.md", content)
        self._audit_log.record(
            "doc.report",
            details={
                "path": str(path),
                "sections": [
                    "Executive Summary",
                    "Source Files",
                    "Key Decisions",
                    "Action Items",
                    "Data Notes",
                    "Audit Trail",
                ],
            },
        )
        return path


def render_report(analysis: WorkspaceAnalysis) -> str:
    lines: list[str] = [
        "# MTBUDDY Workspace Report",
        "",
        "## Request",
        "",
        analysis.request,
        "",
        "## Executive Summary",
        "",
        analysis.executive_summary,
        "",
        "## Source Files",
        "",
    ]
    for source in analysis.sources:
        lines.append(f"- `{source.path}` ({source.kind})")

    lines.extend(["", "## Key Decisions", ""])
    for decision in analysis.key_decisions:
        lines.append(f"- {decision}")

    lines.extend(["", "## Action Items", ""])
    lines.append("| Owner | Item | Due Date | Priority | Status | Source |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for action in analysis.action_items:
        lines.append(
            f"| {_escape(action.owner)} | {_escape(action.item)} | {_escape(action.due_date)} | "
            f"{_escape(action.priority)} | {_escape(action.status)} | `{_escape(action.source)}` |"
        )

    lines.extend(["", "## Data Notes", ""])
    for note in analysis.data_notes:
        lines.append(f"- {note}")

    lines.extend(
        [
            "",
            "## Audit Trail",
            "",
            "Every file read, artifact write, and run lifecycle event is appended to `artifacts/audit.jsonl`.",
            "",
        ]
    )
    return "\n".join(lines)


def _escape(value: str) -> str:
    return value.replace("|", "\\|")
