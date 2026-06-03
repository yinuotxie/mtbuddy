"""Workspace safety helpers."""

from __future__ import annotations

from pathlib import Path


def resolve_workspace(path: Path) -> Path:
    workspace = path.expanduser().resolve()
    if not workspace.exists():
        raise FileNotFoundError(f"workspace does not exist: {workspace}")
    if not workspace.is_dir():
        raise NotADirectoryError(f"workspace is not a directory: {workspace}")
    return workspace


def ensure_inside_workspace(workspace: Path, candidate: Path) -> Path:
    resolved = candidate.expanduser().resolve()
    if not resolved.is_relative_to(workspace.resolve()):
        raise ValueError(f"path escapes workspace: {candidate}")
    return resolved
