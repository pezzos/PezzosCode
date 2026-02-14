#!/usr/bin/env python3
"""
Detect update mode for docs/00-context files.

Mode is computed per file by comparing each live context file with its template pair:
- template-fill: live file equals template file
- enrich-existing: live file differs from template file
"""

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path

FILES = (
    "vision.md",
    "system-map.md",
    "context-boundaries-operating-model.md",
    "users.md",
    "assumptions.md",
    "expected-features.md",
)


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        docs_dir = candidate / "docs" / "00-context"
        tmpl_dir = candidate / "tools" / "templates" / "docs" / "00-context"
        if docs_dir.is_dir() and tmpl_dir.is_dir():
            return candidate
    raise FileNotFoundError(
        "Could not find repo root containing docs/00-context and tools/templates/docs/00-context"
    )


def file_mode(
    repo_root: Path, filename: str, show_diff: bool, max_diff_lines: int
) -> dict[str, object]:
    live_path = repo_root / "docs" / "00-context" / filename
    tmpl_path = repo_root / "tools" / "templates" / "docs" / "00-context" / filename

    result: dict[str, object] = {
        "file": f"docs/00-context/{filename}",
        "template": f"tools/templates/docs/00-context/{filename}",
        "live_exists": live_path.exists(),
        "template_exists": tmpl_path.exists(),
        "mode": "unknown",
        "identical": False,
        "diff_preview": [],
    }

    if not live_path.exists() or not tmpl_path.exists():
        return result

    live_text = normalize_text(live_path.read_text(encoding="utf-8"))
    tmpl_text = normalize_text(tmpl_path.read_text(encoding="utf-8"))

    identical = live_text == tmpl_text
    result["identical"] = identical
    result["mode"] = "template-fill" if identical else "enrich-existing"

    if show_diff and not identical:
        diff_lines = list(
            difflib.unified_diff(
                tmpl_text.splitlines(),
                live_text.splitlines(),
                fromfile=str(result["template"]),
                tofile=str(result["file"]),
                lineterm="",
            )
        )
        result["diff_preview"] = diff_lines[:max_diff_lines]

    return result


def summarize_global_mode(modes: list[str]) -> str:
    unique = set(modes)
    if "unknown" in unique:
        return "unknown"
    if unique == {"template-fill"}:
        return "template-fill"
    if unique == {"enrich-existing"}:
        return "enrich-existing"
    return "mixed"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Detect context update mode from file diffs."
    )
    parser.add_argument(
        "--repo-root", default=".", help="Path inside the target repository."
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON."
    )
    parser.add_argument(
        "--show-diff",
        action="store_true",
        help="Include unified diff preview for changed files.",
    )
    parser.add_argument(
        "--max-diff-lines",
        type=int,
        default=80,
        help="Max diff lines shown per file when --show-diff is set.",
    )
    return parser


def print_table(report: dict[str, object]) -> None:
    print(f"repo_root: {report['repo_root']}")
    print(f"global_mode: {report['global_mode']}")
    print("")
    print("file | mode | identical | live_exists | template_exists")
    print("--- | --- | --- | --- | ---")
    for item in report["files"]:
        print(
            f"{item['file']} | {item['mode']} | {item['identical']} | "
            f"{item['live_exists']} | {item['template_exists']}"
        )
        diff_preview = item.get("diff_preview", [])
        if diff_preview:
            print("")
            print(f"# diff preview: {item['file']}")
            for line in diff_preview:
                print(line)
            print("")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = find_repo_root(Path(args.repo_root))
    file_reports = [
        file_mode(
            repo_root=repo_root,
            filename=filename,
            show_diff=args.show_diff,
            max_diff_lines=max(args.max_diff_lines, 0),
        )
        for filename in FILES
    ]
    report = {
        "repo_root": str(repo_root),
        "global_mode": summarize_global_mode(
            [str(item["mode"]) for item in file_reports]
        ),
        "files": file_reports,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_table(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
