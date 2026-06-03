"""Command-line interface for MTBUDDY."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core.executor import LocalExecutor
from .integrations.openclaw import OpenClawExecutor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mtbuddy",
        description="MTBUDDY local-first personal AI workstation.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run",
        help="Run a workspace task and write auditable artifacts.",
    )
    run_parser.add_argument(
        "request",
        help="Natural-language task request.",
    )
    run_parser.add_argument(
        "--workspace",
        required=True,
        type=Path,
        help="Allowed local workspace directory.",
    )
    run_parser.add_argument(
        "--executor",
        choices=("local", "openclaw"),
        default="local",
        help="Execution backend. Use local for deterministic tests; openclaw for the competition stack.",
    )
    run_parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        executor = (
            LocalExecutor()
            if args.executor == "local"
            else OpenClawExecutor()
        )
        try:
            result = executor.run(args.workspace, args.request)
        except Exception as exc:  # pragma: no cover - exercised through CLI e2e
            print(f"mtbuddy: {exc}", file=sys.stderr)
            return 1

        payload = result.to_dict()
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print("MTBUDDY run complete")
            print(f"Workspace: {payload['workspace']}")
            print("Artifacts:")
            for name, path in payload["artifacts"].items():
                print(f"- {name}: {path}")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2
