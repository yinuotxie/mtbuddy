from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mtbuddy.integrations.agent_clients import (
    FunctionRouterAgentClient,
    OpenAICompatibleAgentClient,
    OpenClawAgentClient,
)


def test_openclaw_agent_client_is_openai_compatible_client() -> None:
    client = OpenClawAgentClient()

    assert isinstance(client, OpenAICompatibleAgentClient)
    assert client.name == "openclaw"


def test_function_router_client_uses_openai_compatible_chat_completion(
    monkeypatch,
    tmp_path: Path,
) -> None:
    captured: dict[str, Any] = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self) -> bytes:
            return json.dumps(
                {"choices": [{"message": {"content": "done"}}]}
            ).encode("utf-8")

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["headers"] = dict(request.header_items())
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = FunctionRouterAgentClient(
        base_url="http://127.0.0.1:18790/v1",
        model="function_router/function-router",
        api_key="secret",
        timeout_s=12,
    )

    response = client.run_workspace_task(tmp_path, "Summarize files")

    assert response.client == "function-router"
    assert response.content == "done"
    assert captured["url"] == "http://127.0.0.1:18790/v1/chat/completions"
    assert captured["timeout"] == 12
    assert captured["headers"]["Authorization"] == "Bearer secret"
    assert captured["body"]["model"] == "function_router/function-router"
    assert captured["body"]["stream"] is False
    assert captured["body"]["messages"][0]["role"] == "user"
    assert "Run MTBUDDY workspace task" in captured["body"]["messages"][0]["content"]
