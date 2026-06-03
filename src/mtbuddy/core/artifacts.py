"""Workspace-local artifact storage."""

from __future__ import annotations

from pathlib import Path

from .interfaces import AuditLog


class WorkspaceArtifactStore:
    """Writes artifacts under ``<workspace>/artifacts`` only."""

    def __init__(self, workspace: Path, audit_log: AuditLog) -> None:
        self._workspace = workspace.resolve()
        self._root = self._workspace / "artifacts"
        self._audit_log = audit_log
        self._root.mkdir(parents=True, exist_ok=True)

    @property
    def root(self) -> Path:
        return self._root

    def write_text(self, relative_path: str, content: str) -> Path:
        destination = (self._root / relative_path).resolve()
        if not destination.is_relative_to(self._root.resolve()):
            raise ValueError(f"artifact path escapes workspace artifacts: {relative_path}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        self._audit_log.record(
            "artifact.write",
            details={
                "path": str(destination),
                "bytes": len(content.encode("utf-8")),
            },
        )
        return destination
