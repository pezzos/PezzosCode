#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
ORCH_ROOT = REPO_ROOT / ".orchestrator"
CODEX_ROOT = REPO_ROOT / ".codex"

PROFILE_CATALOG_PATH = ORCH_ROOT / "profile-catalog.json"
NATIVE_ROLE_MANIFEST_PATH = ORCH_ROOT / "native-role-manifest.json"
CODEX_CONFIG_PATH = CODEX_ROOT / "config.toml"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_profile_catalog() -> dict[str, Any]:
    payload = read_json(PROFILE_CATALOG_PATH, {"version": 1, "profiles": []})
    if not isinstance(payload, dict) or not isinstance(payload.get("profiles"), list):
        return {"version": 1, "profiles": []}
    return payload


def load_role_manifest() -> dict[str, Any]:
    payload = read_json(NATIVE_ROLE_MANIFEST_PATH, {"schema_version": 1, "roles": []})
    if not isinstance(payload, dict) or not isinstance(payload.get("roles"), list):
        return {"schema_version": 1, "roles": []}
    return payload


def normalize_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = [part.strip() for part in value.split(",")]
    elif isinstance(value, list):
        items = [str(part).strip() for part in value]
    else:
        return []
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def alias_map(catalog: dict[str, Any] | None = None) -> dict[str, str]:
    catalog = catalog or load_profile_catalog()
    mapping: dict[str, str] = {}
    for entry in catalog.get("profiles", []):
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("name", "")).strip()
        if not name:
            continue
        mapping[name.casefold()] = name
        for alias in normalize_string_list(entry.get("aliases")):
            mapping[alias.casefold()] = name
    return mapping


def resolve_profile_name(token: str | None, catalog: dict[str, Any] | None = None) -> str | None:
    if not token:
        return None
    return alias_map(catalog).get(token.strip().casefold())


def role_map(manifest: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    manifest = manifest or load_role_manifest()
    output: dict[str, dict[str, Any]] = {}
    for role in manifest.get("roles", []):
        if isinstance(role, dict) and isinstance(role.get("name"), str):
            output[role["name"]] = role
    return output


def cmd_summary(_: argparse.Namespace) -> int:
    catalog = load_profile_catalog()
    manifest = load_role_manifest()
    payload = {
        "profile_count": len(catalog.get("profiles", [])),
        "role_count": len(manifest.get("roles", [])),
        "codex_config_present": CODEX_CONFIG_PATH.exists(),
        "role_classes": sorted(
            {
                str(role.get("role_class"))
                for role in manifest.get("roles", [])
                if isinstance(role, dict) and role.get("role_class")
            }
        ),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_role(args: argparse.Namespace) -> int:
    manifest = load_role_manifest()
    roles = role_map(manifest)
    resolved = args.name
    if resolved not in roles:
        resolved = resolve_profile_name(args.name) or args.name
    payload = roles.get(resolved)
    if payload is None:
        print(f"role_not_found: {args.name}")
        return 1
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect native role metadata in a bootstrapped repository.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("summary")
    role = sub.add_parser("role")
    role.add_argument("name")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.cmd == "summary":
        return cmd_summary(args)
    if args.cmd == "role":
        return cmd_role(args)
    raise RuntimeError(f"unsupported command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
