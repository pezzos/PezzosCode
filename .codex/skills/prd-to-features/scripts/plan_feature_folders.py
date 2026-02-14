#!/usr/bin/env python3
"""Preview PRD-to-features folder mapping without modifying files."""

from __future__ import annotations

import argparse
import importlib.util
import json
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_ROOT = Path(__file__).resolve().parents[4]
TOOL_PATH = DEFAULT_ROOT / "tools" / "prd-to-features"
PRD_PATH = Path("docs/01-product/prd.md")
FEATURES_DIR = Path("docs/02-features")


def load_prd_tool(root: Path):
    tool_path = root / "tools" / "prd-to-features"
    if not tool_path.exists():
        raise FileNotFoundError(f"Missing tool: {tool_path}")
    loader = SourceFileLoader("prd_to_features_preview", str(tool_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview feature folder actions from PRD without writing files."
    )
    parser.add_argument(
        "--root",
        default=str(DEFAULT_ROOT),
        help="Repository root (defaults to detected root).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output.",
    )
    return parser.parse_args()


def build_plan(root: Path) -> Dict[str, Any]:
    tool = load_prd_tool(root)
    prd_file = root / PRD_PATH
    features_root = root / FEATURES_DIR
    prd_text = prd_file.read_text(encoding="utf-8")
    prd_features = tool.parse_prd_features(prd_text)
    existing = tool.discover_existing_features(features_root)
    by_index = existing["by_index"]
    by_slug = existing["by_slug"]

    actions: List[Dict[str, str]] = []
    for feature in prd_features:
        desired_name = f"{feature.index:02d}-{feature.slug}"
        action = "create"
        reason = "missing in docs/02-features"

        if feature.index in by_index:
            found = by_index[feature.index]
            status, status_reason = tool.parse_dev_tasks_status(
                found.path / "dev-tasks.md"
            )
            if tool.status_is_done(status):
                action = "skip_done"
                reason = f"index exists as {found.path.name} with Status: Done"
            else:
                action = "update_or_skip"
                if status_reason:
                    reason = f"index exists as {found.path.name}; {status_reason}"
                else:
                    reason = f"index exists as {found.path.name}"
        elif feature.slug in by_slug:
            found = by_slug[feature.slug]
            action = "skip_slug_collision"
            reason = f"slug already exists as {found.path.name}"

        actions.append(
            {
                "priority": feature.priority,
                "title": feature.title,
                "index": f"{feature.index:02d}",
                "desired_folder": desired_name,
                "action": action,
                "reason": reason,
            }
        )

    return {
        "prd_path": str(PRD_PATH),
        "features_dir": str(FEATURES_DIR),
        "count": len(actions),
        "actions": actions,
    }


def render_text(plan: Dict[str, Any]) -> str:
    lines = [
        f"prd: {plan['prd_path']}",
        f"features_dir: {plan['features_dir']}",
        f"feature_count: {plan['count']}",
        "plan:",
    ]
    for item in plan["actions"]:
        lines.append(
            f"- [{item['priority']}] {item['index']} {item['desired_folder']}: "
            f"{item['action']} ({item['reason']})"
        )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not (root / TOOL_PATH.relative_to(DEFAULT_ROOT)).exists():
        print(f"Missing tool: {root / TOOL_PATH.relative_to(DEFAULT_ROOT)}")
        return 1
    plan = build_plan(root)
    if args.json:
        print(json.dumps(plan, indent=2, ensure_ascii=True))
    else:
        print(render_text(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
