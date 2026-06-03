"""OpenAI-compatible agent clients for MTClaw-backed MTBUDDY runs."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..core.workspace import resolve_workspace


OPENCLAW_CLIENT_NAME = "openclaw"
FUNCTION_ROUTER_CLIENT_NAME = "function-router"
FUNCTION_ROUTER_DEFAULT_MODEL = "function_router/function-router"
FUNCTION_ROUTER_BASE_URL_ENV = "MTBUDDY_FUNCTION_ROUTER_BASE_URL"
FUNCTION_ROUTER_MODEL_ENV = "MTBUDDY_FUNCTION_ROUTER_MODEL"
FUNCTION_ROUTER_API_KEY_ENV = "MTBUDDY_FUNCTION_ROUTER_API_KEY"


@dataclass(frozen=True)
class AgentRunResponse:
    """Normalized response from an agent/client run."""

    client: str
    content: str
    raw: dict[str, Any] | str

    def to_json_text(self) -> str:
        payload = {
            "client": self.client,
            "content": self.content,
            "raw": self.raw,
        }
        return json.dumps(payload, indent=2, sort_keys=True)


class OpenAICompatibleAgentClient(ABC):
    """Agent/client that can use an OpenAI-compatible MTClaw provider."""

    name: str

    @abstractmethod
    def run_workspace_task(self, workspace: Path, request: str) -> AgentRunResponse:
        """Run a workspace task through this agent/client."""

    def build_workspace_message(self, workspace: Path, request: str) -> str:
        resolved_workspace = resolve_workspace(workspace)
        return (
            "Run MTBUDDY workspace task using the configured MTClaw Function Router tools. "
            f"Workspace: {resolved_workspace}. Request: {request}"
        )


class FunctionRouterAgentClient(OpenAICompatibleAgentClient):
    """Direct OpenAI-compatible client for MTClaw Function Router."""

    name = FUNCTION_ROUTER_CLIENT_NAME

    def __init__(
        self,
        *,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        timeout_s: float = 60.0,
    ) -> None:
        self.base_url = (base_url or os.environ.get(FUNCTION_ROUTER_BASE_URL_ENV) or "").rstrip("/")
        self.model = model or os.environ.get(FUNCTION_ROUTER_MODEL_ENV) or FUNCTION_ROUTER_DEFAULT_MODEL
        self.api_key = (
            api_key
            if api_key is not None
            else os.environ.get(FUNCTION_ROUTER_API_KEY_ENV, "")
        )
        self.timeout_s = timeout_s

    def run_workspace_task(self, workspace: Path, request: str) -> AgentRunResponse:
        if not self.base_url:
            raise RuntimeError(
                "MTClaw Function Router base URL is not configured. Set "
                f"{FUNCTION_ROUTER_BASE_URL_ENV}, for example http://127.0.0.1:18790/v1."
            )
        message = self.build_workspace_message(workspace, request)
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }
        response = self._post_json("/chat/completions", payload)
        content = _extract_openai_content(response)
        return AgentRunResponse(client=self.name, content=content, raw=response)

    def _post_json(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = urllib.request.Request(
            f"{self.base_url}{endpoint}",
            data=body,
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Function Router request failed: {exc.code} {error_body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Function Router request failed: {exc.reason}") from exc

        try:
            parsed = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Function Router returned invalid JSON") from exc
        if not isinstance(parsed, dict):
            raise RuntimeError("Function Router returned a non-object JSON response")
        return parsed


class OpenClawAgentClient(OpenAICompatibleAgentClient):
    """OpenClaw CLI client configured to use MTClaw as an OpenAI-compatible provider."""

    name = OPENCLAW_CLIENT_NAME

    def __init__(self, openclaw_bin: str = "openclaw", agent_name: str = "mtbuddy") -> None:
        self.openclaw_bin = openclaw_bin
        self.agent_name = agent_name

    def run_workspace_task(self, workspace: Path, request: str) -> AgentRunResponse:
        binary = shutil.which(self.openclaw_bin)
        if binary is None:
            raise RuntimeError(
                "OpenClaw CLI was not found. Install/configure OpenClaw or use --executor local."
            )

        completed = subprocess.run(
            [
                binary,
                "agent",
                "--agent",
                self.agent_name,
                "--message",
                self.build_workspace_message(workspace, request),
                "--local",
                "--json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or "OpenClaw agent run failed.")

        try:
            raw: dict[str, Any] | str = json.loads(completed.stdout)
        except json.JSONDecodeError:
            raw = completed.stdout
        return AgentRunResponse(
            client=self.name,
            content=_extract_openai_content(raw) if isinstance(raw, dict) else completed.stdout,
            raw=raw,
        )


def _extract_openai_content(response: dict[str, Any]) -> str:
    choices = response.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            delta = first.get("delta")
            if isinstance(delta, dict) and isinstance(delta.get("content"), str):
                return delta["content"]
    if isinstance(response.get("content"), str):
        return response["content"]
    return ""
