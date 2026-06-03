"""Workspace file skill."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..core.analysis import SourceDocument
from ..core.interfaces import AuditLog
from ..core.workspace import ensure_inside_workspace


ALLOWED_SUFFIXES = {".csv", ".md", ".txt"}


@dataclass(frozen=True)
class WorkspaceFile:
    """Allowed source file in a workspace."""

    path: Path
    relative_path: str
    kind: str
    size_bytes: int


class FileSkill:
    """List and read allowed files from a single workspace."""

    name = "file_skill"

    def __init__(self, workspace: Path, audit_log: AuditLog) -> None:
        self._workspace = workspace.resolve()
        self._audit_log = audit_log

    def permissions(self) -> list[str]:
        return [
            f"Read .md, .txt, and .csv files under {self._workspace}",
            "Ignore generated artifacts and hidden directories.",
        ]

    def list_files(self) -> list[WorkspaceFile]:
        files: list[WorkspaceFile] = []
        for path in sorted(self._workspace.rglob("*")):
            if not path.is_file():
                continue
            relative_parts = path.relative_to(self._workspace).parts
            if "artifacts" in relative_parts:
                continue
            if any(part.startswith(".") for part in relative_parts):
                continue
            if path.suffix.lower() not in ALLOWED_SUFFIXES:
                continue
            files.append(
                WorkspaceFile(
                    path=path,
                    relative_path=path.relative_to(self._workspace).as_posix(),
                    kind=_kind_for(path),
                    size_bytes=path.stat().st_size,
                )
            )
        self._audit_log.record(
            "file.list",
            details={
                "workspace": str(self._workspace),
                "count": len(files),
                "files": [file.relative_path for file in files],
            },
        )
        return files

    def read_file(self, path: Path) -> SourceDocument:
        resolved = ensure_inside_workspace(self._workspace, path)
        if resolved.suffix.lower() not in ALLOWED_SUFFIXES:
            raise ValueError(f"file type is not allowed: {resolved.suffix}")
        content = resolved.read_text(encoding="utf-8")
        relative_path = resolved.relative_to(self._workspace).as_posix()
        self._audit_log.record(
            "file.read",
            details={
                "path": relative_path,
                "bytes": len(content.encode("utf-8")),
            },
        )
        return SourceDocument(
            path=relative_path,
            kind=_kind_for(resolved),
            content=content,
        )


def _kind_for(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix == ".md":
        return "markdown"
    return "text"
