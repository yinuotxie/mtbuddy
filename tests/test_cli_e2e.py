from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_cli_run_creates_report_action_csv_and_audit_log(tmp_path: Path) -> None:
    workspace = tmp_path / "demo"
    shutil.copytree(REPO_ROOT / "workspaces" / "demo", workspace)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mtbuddy",
            "run",
            "--executor",
            "local",
            "--workspace",
            str(workspace),
            "Summarize these files and create an action list",
            "--json",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    artifacts = payload["artifacts"]

    report_path = Path(artifacts["report"])
    action_items_path = Path(artifacts["action_items"])
    audit_path = Path(artifacts["audit_log"])

    assert report_path.exists()
    assert action_items_path.exists()
    assert audit_path.exists()

    report = report_path.read_text(encoding="utf-8")
    for section in (
        "# MTBUDDY Workspace Report",
        "## Executive Summary",
        "## Source Files",
        "## Key Decisions",
        "## Action Items",
        "## Data Notes",
        "## Audit Trail",
    ):
        assert section in report
    assert "OpenClaw, Hermes, OpenCode, and Codex-like OpenAI-compatible agents" in report
    assert "MTClaw Function Router" in report

    with action_items_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    assert set(rows[0]) == {"owner", "item", "due_date", "source", "priority", "status"}
    assert any(row["owner"] == "Travis" for row in rows)
    assert any("README" in row["item"] for row in rows)

    audit_entries = [
        json.loads(line)
        for line in audit_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    operations = [entry["operation"] for entry in audit_entries]
    for operation in (
        "run.start",
        "workspace.allow",
        "file.list",
        "file.read",
        "analysis.extract",
        "artifact.write",
        "doc.report",
        "sheet.action_items",
        "run.complete",
    ):
        assert operation in operations


def test_mtclaw_tool_entrypoint_lists_workspace_files(tmp_path: Path) -> None:
    workspace = tmp_path / "demo"
    shutil.copytree(REPO_ROOT / "workspaces" / "demo", workspace)

    completed = subprocess.run(
        [sys.executable, "-m", "mtbuddy.mtclaw_tools", "mtbuddy_list_files"],
        cwd=REPO_ROOT,
        input=json.dumps({"workspace": str(workspace)}),
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["result"] == "ok"
    assert {item["path"] for item in payload["files"]} == {
        "meeting-notes.md",
        "metrics.csv",
        "presentation-outline.md",
        "research-notes.txt",
    }
