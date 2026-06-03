"""Executor that delegates to an OpenAI-compatible agent client."""

from __future__ import annotations

from pathlib import Path

from ..core.interfaces import RunResult
from ..core.workspace import resolve_workspace
from .agent_clients import OpenAICompatibleAgentClient


class AgentExecutor:
    """Run MTBUDDY through an OpenAI-compatible client using MTClaw tools."""

    def __init__(self, client: OpenAICompatibleAgentClient) -> None:
        self.client = client
        self.name = client.name

    def run(self, workspace: Path, request: str) -> RunResult:
        resolved_workspace = resolve_workspace(workspace)
        response = self.client.run_workspace_task(resolved_workspace, request)
        artifact_root = resolved_workspace / "artifacts"
        artifact_root.mkdir(parents=True, exist_ok=True)
        response_path = artifact_root / f"{response.client}-agent-response.json"
        response_path.write_text(response.to_json_text(), encoding="utf-8")
        return RunResult(
            workspace=resolved_workspace,
            request=request,
            artifacts={
                f"{response.client}_agent_response": response_path,
            },
        )
