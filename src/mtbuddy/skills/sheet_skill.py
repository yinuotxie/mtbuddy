"""CSV sheet generation skill."""

from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path

from ..core.analysis import ActionItem
from ..core.interfaces import ArtifactStore, AuditLog


class SheetSkill:
    """Write action items to CSV."""

    name = "sheet_skill"

    def __init__(self, artifact_store: ArtifactStore, audit_log: AuditLog) -> None:
        self._artifact_store = artifact_store
        self._audit_log = audit_log

    def permissions(self) -> list[str]:
        return ["Write action-item CSV files under the workspace artifacts directory."]

    def write_action_items(self, action_items: list[ActionItem]) -> Path:
        buffer = StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=["owner", "item", "due_date", "source", "priority", "status"],
            lineterminator="\n",
        )
        writer.writeheader()
        for action in action_items:
            writer.writerow(
                {
                    "owner": action.owner,
                    "item": action.item,
                    "due_date": action.due_date,
                    "source": action.source,
                    "priority": action.priority,
                    "status": action.status,
                }
            )
        path = self._artifact_store.write_text("action-items.csv", buffer.getvalue())
        self._audit_log.record(
            "sheet.action_items",
            details={
                "path": str(path),
                "count": len(action_items),
            },
        )
        return path
