#!/usr/bin/env python3
"""Deterministic wrapper around tools/feature-status-audit."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[4]
TOOL_PATH = ROOT / "tools" / "feature-status-audit"
STATUS_LINE_RE = re.compile(r"^- (Done|Ongoing|To Do):\s*(.*)$")


def parse_summary(stdout: str) -> Dict[str, object]:
    summary: Dict[str, object] = {"feature": None, "status": {}, "checklist": []}
    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        if line.startswith("feature: "):
            summary["feature"] = line.split("feature: ", 1)[1].strip()
            continue
        match = STATUS_LINE_RE.match(line)
        if match:
            key = match.group(1)
            value = match.group(2)
            items = (
                [] if value == "none" else [item.strip() for item in value.split(",")]
            )
            summary["status"][key] = items
            continue
        if line.startswith("checklist (confirm): "):
            payload = line.split("checklist (confirm): ", 1)[1].strip()
            summary["checklist"] = (
                []
                if payload == "none"
                else [item.strip() for item in payload.split(",")]
            )
    return summary


def run_audit(feature: str | None) -> subprocess.CompletedProcess[str]:
    if not TOOL_PATH.exists():
        raise FileNotFoundError(f"tool not found: {TOOL_PATH}")
    cmd = [str(TOOL_PATH)]
    if feature:
        cmd.append(feature)
    return subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run feature-status-audit deterministically."
    )
    parser.add_argument(
        "--feature",
        default=None,
        help="Feature id (for example: 01). Defaults to tool auto-selection.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print parsed summary as JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = run_audit(args.feature)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        parsed = parse_summary(result.stdout)
        print(json.dumps(parsed, indent=2, ensure_ascii=True))
    else:
        if result.stdout:
            print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
