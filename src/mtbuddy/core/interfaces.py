"""Stable interfaces for MTBUDDY skills, executors, artifacts, and logs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


@dataclass(frozen=True)
class SkillResult:
    """Normalized result from a skill execution."""

    name: str
    status: str
    data: dict[str, Any]


@dataclass(frozen=True)
class RunResult:
    """Artifacts produced by one workstation run."""

    workspace: Path
    request: str
    artifacts: dict[str, Path]

    def to_dict(self) -> dict[str, Any]:
        return {
            "workspace": str(self.workspace),
            "request": self.request,
            "artifacts": {
                key: str(value)
                for key, value in sorted(self.artifacts.items())
            },
        }


class AuditLog(Protocol):
    """Append-only operation log."""

    @property
    def path(self) -> Path:
        """Return the audit log file path."""

    def record(
        self,
        operation: str,
        *,
        status: str = "ok",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Record one auditable operation."""


class ArtifactStore(Protocol):
    """Workspace-local artifact writer."""

    @property
    def root(self) -> Path:
        """Return the artifact directory."""

    def write_text(self, relative_path: str, content: str) -> Path:
        """Write a UTF-8 artifact and return its path."""


class Skill(Protocol):
    """A deterministic, auditable MTBUDDY capability."""

    name: str

    def permissions(self) -> list[str]:
        """Return human-readable permission declarations."""


class Executor(Protocol):
    """Runs a natural-language task against a workspace."""

    name: str

    def run(self, workspace: Path, request: str) -> RunResult:
        """Execute a task and return produced artifacts."""


class LLMProvider(Protocol):
    """Abstract LLM surface for DeepSeek, AIBOOK local models, and tests."""

    name: str

    def complete(self, prompt: str) -> str:
        """Return a completion for a prompt."""
