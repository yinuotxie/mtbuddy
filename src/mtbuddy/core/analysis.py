"""Deterministic workspace analysis used by the first MTBUDDY slice."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path


@dataclass(frozen=True)
class SourceDocument:
    """Text content loaded from an allowed workspace file."""

    path: str
    kind: str
    content: str


@dataclass
class ActionItem:
    """Structured action item written to CSV and Markdown."""

    owner: str
    item: str
    due_date: str
    source: str
    priority: str = "medium"
    status: str = "open"


@dataclass
class WorkspaceAnalysis:
    """Summary-ready view of a workspace."""

    request: str
    sources: list[SourceDocument]
    executive_summary: str
    key_decisions: list[str] = field(default_factory=list)
    action_items: list[ActionItem] = field(default_factory=list)
    data_notes: list[str] = field(default_factory=list)


ACTION_PATTERNS = (
    re.compile(
        r"^\s*[-*]?\s*(?:Action|ACTION)\s*:\s*(?P<owner>[^-:;]+?)\s*[-:;]\s*(?P<item>.+?)(?:\s*(?:due|by)\s*(?P<due>[A-Za-z0-9 ,/-]+))?\s*$"
    ),
    re.compile(
        r"^\s*[-*]?\s*@(?P<owner>[A-Za-z][\w -]+)\s*:\s*(?P<item>.+?)(?:\s*(?:due|by)\s*(?P<due>[A-Za-z0-9 ,/-]+))?\s*$"
    ),
)
DECISION_PATTERN = re.compile(r"^\s*[-*]?\s*(?:Decision|DECISION)\s*:\s*(?P<decision>.+?)\s*$")


def analyze_workspace(request: str, sources: list[SourceDocument]) -> WorkspaceAnalysis:
    decisions: list[str] = []
    actions: list[ActionItem] = []
    data_notes: list[str] = []

    for source in sources:
        if source.kind == "csv":
            csv_actions, note = _analyze_csv(source)
            actions.extend(csv_actions)
            if note:
                data_notes.append(note)
            continue
        parsed_decisions, parsed_actions = _analyze_text(source)
        decisions.extend(parsed_decisions)
        actions.extend(parsed_actions)

    if not decisions:
        decisions.append("No explicit decisions were marked in the provided files.")
    if not actions:
        actions.append(
            ActionItem(
                owner="MTBUDDY",
                item="Review the workspace and add explicit action owners.",
                due_date="TBD",
                source="generated",
                priority="medium",
            )
        )

    executive_summary = (
        f"MTBUDDY reviewed {len(sources)} allowed source file(s), found "
        f"{len(decisions)} decision(s), and produced {len(actions)} action item(s) "
        "from the local workspace without external services."
    )
    return WorkspaceAnalysis(
        request=request,
        sources=sources,
        executive_summary=executive_summary,
        key_decisions=_dedupe(decisions),
        action_items=_dedupe_actions(actions),
        data_notes=data_notes or ["No CSV data files were present."],
    )


def _analyze_text(source: SourceDocument) -> tuple[list[str], list[ActionItem]]:
    decisions: list[str] = []
    actions: list[ActionItem] = []
    for raw_line in source.content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        decision_match = DECISION_PATTERN.match(line)
        if decision_match:
            decisions.append(f"{decision_match.group('decision')} ({source.path})")
            continue
        for pattern in ACTION_PATTERNS:
            action_match = pattern.match(line)
            if not action_match:
                continue
            owner = _clean(action_match.group("owner"))
            item = _clean(action_match.group("item"))
            due = _clean(action_match.group("due") or "TBD")
            actions.append(
                ActionItem(
                    owner=owner,
                    item=item,
                    due_date=due,
                    source=source.path,
                    priority=_priority_from_text(item),
                )
            )
            break
    return decisions, actions


def _analyze_csv(source: SourceDocument) -> tuple[list[ActionItem], str | None]:
    reader = csv.DictReader(StringIO(source.content))
    rows = list(reader)
    if not reader.fieldnames:
        return [], f"{source.path}: CSV had no header row."

    actions: list[ActionItem] = []
    for row in rows:
        owner = _first_present(row, "owner", "action_owner", "assignee", "team")
        item = _first_present(row, "action", "follow_up", "next_step", "item")
        if not item:
            continue
        actions.append(
            ActionItem(
                owner=owner or "Unassigned",
                item=item,
                due_date=_first_present(row, "due_date", "due", "target_date") or "TBD",
                source=source.path,
                priority=_first_present(row, "priority") or _priority_from_text(item),
                status=_first_present(row, "status") or "open",
            )
        )

    note = (
        f"{source.path}: {len(rows)} row(s), columns: "
        f"{', '.join(reader.fieldnames)}."
    )
    return actions, note


def _first_present(row: dict[str, str | None], *keys: str) -> str:
    normalized = {key.lower().strip(): value for key, value in row.items()}
    for key in keys:
        value = normalized.get(key)
        if value:
            return _clean(value)
    return ""


def _clean(value: str) -> str:
    return " ".join(value.strip().strip(".").split())


def _priority_from_text(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ("urgent", "blocker", "critical")):
        return "high"
    if any(word in lowered for word in ("nice to have", "later", "optional")):
        return "low"
    return "medium"


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _dedupe_actions(items: list[ActionItem]) -> list[ActionItem]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[ActionItem] = []
    for item in items:
        key = (item.owner.lower(), item.item.lower(), Path(item.source).name.lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped
