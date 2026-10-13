#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from runtime_profiles import (
    NATIVE_ROLE_MANIFEST_PATH,
    PROFILE_CATALOG_PATH,
    read_json,
    write_json,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
ORCH_ROOT = REPO_ROOT / ".orchestrator"
LOCKS_ROOT = ORCH_ROOT / "locks"
RUNS_ROOT = ORCH_ROOT / "runs"
COMPLIANCE_ROOT = ORCH_ROOT / "compliance"
WORKTREES_ROOT = ORCH_ROOT / "worktrees"

ORCHESTRATOR_LOCK = LOCKS_ROOT / "orchestrator.lock.json"
RUN_LOCK = LOCKS_ROOT / "run.lock.json"
POLICY_PATH = ORCH_ROOT / "policy.json"

DEFAULT_POLICY = {
    "role": "orchestrator",
    "mode": "audit",
    "parallel_policy": "prudent",
    "native_roles_required": True,
    "default_worker_output_schema": "coder_output_v1",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def current_thread_id() -> str:
    return os.environ.get("CODEX_THREAD_ID", "unknown")


def ensure_layout() -> None:
    for path in (ORCH_ROOT, LOCKS_ROOT, RUNS_ROOT, COMPLIANCE_ROOT, WORKTREES_ROOT):
        path.mkdir(parents=True, exist_ok=True)


def validate_native_role_inputs() -> list[str]:
    missing: list[str] = []
    if not PROFILE_CATALOG_PATH.exists():
        missing.append(str(PROFILE_CATALOG_PATH))
    if not NATIVE_ROLE_MANIFEST_PATH.exists():
        missing.append(str(NATIVE_ROLE_MANIFEST_PATH))
    return missing


def cmd_init(_: argparse.Namespace) -> int:
    ensure_layout()
    missing = validate_native_role_inputs()
    if missing:
        print(f"BLOCKED_NATIVE_ROLE_CONFIG_MISSING: {', '.join(missing)}")
        return 4

    policy = read_json(POLICY_PATH, DEFAULT_POLICY)
    if not isinstance(policy, dict):
        policy = DEFAULT_POLICY
    write_json(POLICY_PATH, policy)

    lock = {
        "status": "ACTIVE",
        "mode": "exclusive",
        "active_thread_id": current_thread_id(),
        "initialized_at": utc_now(),
        "updated_at": utc_now(),
    }
    write_json(ORCHESTRATOR_LOCK, lock)
    print(json.dumps(lock, indent=2, ensure_ascii=False))
    return 0


def cmd_assert(_: argparse.Namespace) -> int:
    lock = read_json(ORCHESTRATOR_LOCK, None)
    if not isinstance(lock, dict):
        print("BLOCKED_NOT_INITIALIZED")
        return 2
    owner = str(lock.get("active_thread_id", "unknown"))
    thread_id = current_thread_id()
    if owner not in {"", "unknown", thread_id} and thread_id != "unknown":
        print("BLOCKED_NOT_OWNER")
        return 3
    print("OK")
    return 0


def cmd_run_status(_: argparse.Namespace) -> int:
    manifest = read_json(NATIVE_ROLE_MANIFEST_PATH, {"roles": []})
    payload = {
        "orchestrator_lock": read_json(ORCHESTRATOR_LOCK, {}),
        "run_lock": read_json(RUN_LOCK, {}),
        "native_role_count": len(manifest.get("roles", [])) if isinstance(manifest, dict) else 0,
        "policy_mode": read_json(POLICY_PATH, DEFAULT_POLICY).get("mode", "audit"),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_policy_show(_: argparse.Namespace) -> int:
    print(json.dumps(read_json(POLICY_PATH, DEFAULT_POLICY), indent=2, ensure_ascii=False))
    return 0


def cmd_policy_set(args: argparse.Namespace) -> int:
    payload = read_json(POLICY_PATH, DEFAULT_POLICY)
    if not isinstance(payload, dict):
        payload = dict(DEFAULT_POLICY)
    payload["mode"] = args.mode
    write_json(POLICY_PATH, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_run_recover(args: argparse.Namespace) -> int:
    run_lock = read_json(RUN_LOCK, None)
    if not isinstance(run_lock, dict):
        print("no_run_lock")
        return 0
    updated_at = run_lock.get("updated_at")
    if not isinstance(updated_at, str):
        RUN_LOCK.unlink(missing_ok=True)
        print("recovered_missing_timestamp")
        return 0
    try:
        updated_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    except ValueError:
        RUN_LOCK.unlink(missing_ok=True)
        print("recovered_invalid_timestamp")
        return 0
    stale_after = timedelta(seconds=args.max_stale_seconds)
    if datetime.now(timezone.utc) - updated_dt >= stale_after:
        RUN_LOCK.unlink(missing_ok=True)
        print("recovered_stale_run_lock")
        return 0
    print("run_lock_active")
    return 0


def cmd_compliance_scan(args: argparse.Namespace) -> int:
    ensure_layout()
    worktree = Path(args.worktree).expanduser().resolve()
    payload: dict[str, Any] = {
        "run_id": args.run_id,
        "phase": args.phase,
        "worktree": str(worktree),
        "state": "unknown",
        "unauthorized_paths": [],
        "generated_at": utc_now(),
    }
    report_base = COMPLIANCE_ROOT / args.run_id
    write_json(report_base.with_suffix(".json"), payload)
    report_base.with_suffix(".md").write_text(
        "# Compliance Report\n\n"
        f"- Run ID: `{args.run_id}`\n"
        f"- Phase: `{args.phase}`\n"
        f"- Worktree: `{worktree}`\n"
        "- State: `unknown`\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage orchestrator locks and policy for native-role workflows.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("assert")
    sub.add_parser("run-status")
    sub.add_parser("policy-show")
    policy_set = sub.add_parser("policy-set")
    policy_set.add_argument("--mode", choices=("audit", "strict"), required=True)
    recover = sub.add_parser("run-recover")
    recover.add_argument("--max-stale-seconds", type=int, default=900)
    compliance = sub.add_parser("compliance-scan")
    compliance.add_argument("--run-id", required=True)
    compliance.add_argument("--phase", choices=("pre", "post"), required=True)
    compliance.add_argument("--worktree", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.cmd == "init":
        return cmd_init(args)
    if args.cmd == "assert":
        return cmd_assert(args)
    if args.cmd == "run-status":
        return cmd_run_status(args)
    if args.cmd == "policy-show":
        return cmd_policy_show(args)
    if args.cmd == "policy-set":
        return cmd_policy_set(args)
    if args.cmd == "run-recover":
        return cmd_run_recover(args)
    if args.cmd == "compliance-scan":
        return cmd_compliance_scan(args)
    raise RuntimeError(f"unsupported command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
