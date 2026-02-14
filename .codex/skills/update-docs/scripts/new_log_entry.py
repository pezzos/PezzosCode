#!/usr/bin/env python3
"""Render deterministic docs/03-logs entry templates."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

LOG_KIND_TO_PATH = {
    "implementation": "docs/03-logs/implementation-log.md",
    "decision": "docs/03-logs/decision-log.md",
    "bug": "docs/03-logs/bug-log.md",
    "validation": "docs/03-logs/validation-log.md",
    "insight": "docs/03-logs/insights.md",
}

TEMPLATES = {
    "implementation": [
        "**Feature/Bug:** <scope>",
        "",
        "**Changed Files:**",
        "",
        "- `<path>`",
        "",
        "**What Changed:**",
        "",
        "- <change>",
        "",
        "**Why:**",
        "",
        "- <reason>",
    ],
    "decision": [
        "**Date:** <YYYY-MM-DD>",
        "",
        "**Status:** Proposed",
        "",
        "**Decision:**",
        "<what was decided>",
        "",
        "**Rationale:**",
        "<why this option was chosen>",
        "",
        "**Implications:**",
        "",
        "- <impact>",
    ],
    "bug": [
        "**Date Discovered:** <YYYY-MM-DD>",
        "",
        "**Severity:** <Critical|High|Medium|Low>",
        "",
        "**Status:** Fixed",
        "",
        "**Symptoms:**",
        "<what failed>",
        "",
        "**Root Cause:**",
        "<cause>",
        "",
        "**Fix:**",
        "<fix summary>",
    ],
    "validation": [
        "- `<command>` (PASS/FAIL)",
        "- Verified:",
        "  - <check>",
    ],
    "insight": [
        "**Context:** <where this insight applies>",
        "",
        "**What we learned:**",
        "<insight>",
        "",
        "**Evidence:**",
        "",
        "- <evidence>",
        "",
        "**Action:**",
        "",
        "- <recommended practice>",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate docs log entry templates.")
    parser.add_argument(
        "--kind",
        choices=sorted(TEMPLATES.keys()),
        required=True,
        help="Log entry kind.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Entry title shown in the heading.",
    )
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Entry date in YYYY-MM-DD format (defaults to UTC today).",
    )
    parser.add_argument(
        "--show-target",
        action="store_true",
        help="Print suggested destination log file before the entry.",
    )
    return parser.parse_args()


def render_entry(kind: str, date: str, title: str) -> str:
    lines = [f"### {date} - {title}", ""]
    lines.extend(TEMPLATES[kind])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    if args.show_target:
        print(f"# target: {LOG_KIND_TO_PATH[args.kind]}")
        print()
    print(render_entry(args.kind, args.date, args.title), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
