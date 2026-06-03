"""OpenClaw executor seam for the competition runtime."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from ..core.interfaces import RunResult
from ..core.workspace import resolve_workspace


class OpenClawExecutor:
    """Run a task through OpenClaw, configured to use MTClaw as provider."""

    name = "openclaw"

    def __init__(self, openclaw_bin: str = "openclaw") -> None:
        self._openclaw_bin = openclaw_bin

    def run(self, workspace: Path, request: str) -> RunResult:
        resolved_workspace = resolve_workspace(workspace)
        binary = shutil.which(self._openclaw_bin)
        if binary is None:
            raise RuntimeError(
                "OpenClaw CLI was not found. Install/configure OpenClaw or use --executor local."
            )

        message = (
            "Run MTBUDDY workspace task using the configured MTClaw Function Router tools. "
            f"Workspace: {resolved_workspace}. Request: {request}"
        )
        completed = subprocess.run(
            [
                binary,
                "agent",
                "--agent",
                "mtbuddy",
                "--message",
                message,
                "--local",
                "--json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or "OpenClaw agent run failed.")

        output_path = resolved_workspace / "artifacts" / "openclaw-response.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            parsed = json.loads(completed.stdout)
            output_path.write_text(json.dumps(parsed, indent=2, sort_keys=True), encoding="utf-8")
        except json.JSONDecodeError:
            output_path.write_text(completed.stdout, encoding="utf-8")

        return RunResult(
            workspace=resolved_workspace,
            request=request,
            artifacts={
                "openclaw_response": output_path,
            },
        )
