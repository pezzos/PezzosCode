from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Mapping, Optional

OPENAI_ENV_VARS = (
    "OPENAI_API_KEY",
    "OPENAI_BILLING_API_KEY",
    "OPENAI_BASE_URL",
    "OPENAI_ORG_ID",
    "OPENAI_ORGANIZATION",
    "OPENAI_PROJECT",
)

DEFAULT_CONFIG = (
    'approval_policy = "never"\n'
    'sandbox_mode = "workspace-write"\n'
    "network_access = false\n"
)


class CodexEnvError(RuntimeError):
    pass


@dataclass(frozen=True)
class CodexEnvironment:
    env: dict[str, str]
    auth_src: Path
    auth_dst: Path
    codex_home: Path


def parse_last_refresh(path: Path) -> Optional[datetime]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    raw = payload.get("last_refresh")
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def source_auth_is_newer(auth_src: Path, auth_dst: Path) -> bool:
    src_refresh = parse_last_refresh(auth_src)
    dst_refresh = parse_last_refresh(auth_dst)
    if src_refresh and dst_refresh:
        return src_refresh > dst_refresh
    if src_refresh and not dst_refresh:
        return True
    if not src_refresh and dst_refresh:
        return False
    return auth_src.stat().st_mtime > auth_dst.stat().st_mtime


def auth_source_path() -> Path:
    return Path.home() / ".codex" / "auth.json"


def validate_chatgpt_auth(auth_path: Path, *, error_prefix: str) -> dict:
    if not auth_path.exists():
        raise CodexEnvError(
            f"{error_prefix}: required ChatGPT auth file missing at {auth_path}"
        )
    try:
        payload = json.loads(auth_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CodexEnvError(
            f"{error_prefix}: invalid auth.json at {auth_path}: {exc}"
        ) from exc
    except OSError as exc:
        raise CodexEnvError(
            f"{error_prefix}: failed to read auth.json at {auth_path}: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise CodexEnvError(f"{error_prefix}: invalid auth.json at {auth_path}")
    auth_mode = payload.get("auth_mode")
    if auth_mode != "chatgpt":
        raise CodexEnvError(
            f'{error_prefix}: auth.json at {auth_path} must use auth_mode "chatgpt"'
        )
    return payload


def sync_auth_file(
    auth_src: Path,
    auth_dst: Path,
    *,
    force: bool = False,
    error_prefix: str,
) -> bool:
    validate_chatgpt_auth(auth_src, error_prefix=error_prefix)
    should_copy = force or not auth_dst.exists()
    if not should_copy and auth_dst.exists():
        should_copy = source_auth_is_newer(auth_src, auth_dst)
    if not should_copy:
        return False
    auth_dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(auth_src, auth_dst)
    except OSError as exc:
        raise CodexEnvError(
            f"{error_prefix}: failed to copy auth.json to {auth_dst}: {exc}"
        ) from exc
    validate_chatgpt_auth(auth_dst, error_prefix=error_prefix)
    return True


def prepare_codex_env(
    root: Path,
    home_name: str,
    *,
    error_prefix: str,
    base_env: Optional[Mapping[str, str]] = None,
    config_text: str = DEFAULT_CONFIG,
) -> CodexEnvironment:
    env = dict(base_env or os.environ)
    for var_name in OPENAI_ENV_VARS:
        env.pop(var_name, None)

    codex_home = root / home_name
    try:
        codex_home.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise CodexEnvError(
            f"{error_prefix}: failed to create CODEX_HOME at {codex_home}: {exc}"
        ) from exc

    config_path = codex_home / "config.toml"
    if not config_path.exists():
        try:
            config_path.write_text(config_text, encoding="utf-8")
        except OSError as exc:
            raise CodexEnvError(
                f"{error_prefix}: failed to write config.toml at {config_path}: {exc}"
            ) from exc

    auth_src = auth_source_path()
    auth_dst = codex_home / "auth.json"
    sync_auth_file(auth_src, auth_dst, error_prefix=error_prefix)
    env["CODEX_HOME"] = str(codex_home)
    return CodexEnvironment(
        env=env,
        auth_src=auth_src,
        auth_dst=auth_dst,
        codex_home=codex_home,
    )
