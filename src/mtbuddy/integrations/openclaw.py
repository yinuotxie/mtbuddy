"""OpenClaw compatibility exports."""

from __future__ import annotations

from pathlib import Path

from ..core.interfaces import RunResult
from .agent_clients import OpenClawAgentClient
from .agent_executor import AgentExecutor


class OpenClawExecutor:
    """Backward-compatible executor wrapper around ``OpenClawAgentClient``."""

    name = "openclaw"

    def __init__(self, openclaw_bin: str = "openclaw", agent_name: str = "mtbuddy") -> None:
        self._executor = AgentExecutor(
            OpenClawAgentClient(openclaw_bin=openclaw_bin, agent_name=agent_name)
        )

    def run(self, workspace: Path, request: str) -> RunResult:
        return self._executor.run(workspace, request)
