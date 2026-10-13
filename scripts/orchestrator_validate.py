#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.returncode, completed.stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate native-role orchestration bootstrap end-to-end.")
    parser.add_argument(
        "--output-json",
        default=".orchestrator/validation_summary.json",
        help="Where to write validation summary JSON",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    checks: list[dict[str, str]] = []
    blockers: list[str] = []

    required_paths = [
        ".codex/config.toml",
        ".codex/agents/frontend-developer.toml",
        ".orchestrator/profile-catalog.json",
        ".orchestrator/native-role-manifest.json",
        ".orchestrator/skills-catalog.json",
        "scripts/orchestrator_guard.py",
        "scripts/runtime_profiles.py",
    ]
    for relative in required_paths:
        path = REPO_ROOT / relative
        ok = path.exists()
        checks.append({"name": relative, "status": "ok" if ok else "fail", "evidence": str(path)})
        if not ok:
            blockers.append(f"missing required path: {relative}")

    commands = [
        ["python3", "scripts/runtime_profiles.py", "summary"],
        ["python3", "scripts/runtime_profiles.py", "role", "frontend-developer"],
        ["python3", "scripts/orchestrator_guard.py", "init"],
        ["python3", "scripts/orchestrator_guard.py", "assert"],
        ["python3", "scripts/orchestrator_guard.py", "run-status"],
        ["python3", "scripts/orchestrator_guard.py", "policy-show"],
    ]
    for command in commands:
        code, output = run(command)
        checks.append(
            {
                "name": " ".join(command),
                "status": "ok" if code == 0 else "fail",
                "evidence": output.strip()[:800],
            }
        )
        if code != 0:
            blockers.append(f"command failed: {' '.join(command)}")

    payload = {
        "status": "ok" if not blockers else "partial",
        "checks": checks,
        "blockers": blockers,
        "recommendation": (
            "Proceed with native-role orchestration."
            if not blockers
            else "Fix bootstrap blockers before relying on native roles."
        ),
    }

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
