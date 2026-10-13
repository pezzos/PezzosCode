from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
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
    if payload.get("auth_mode") != "chatgpt":
        raise CodexEnvError(
            f'{error_prefix}: auth.json at {auth_path} must use auth_mode "chatgpt"'
        )
    return payload


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
    codex_home.mkdir(parents=True, exist_ok=True)

    config_path = codex_home / "config.toml"
    if not config_path.exists():
        config_path.write_text(config_text, encoding="utf-8")

    auth_src = auth_source_path()
    validate_chatgpt_auth(auth_src, error_prefix=error_prefix)
    auth_dst = codex_home / "auth.json"
    try:
        shutil.copy2(auth_src, auth_dst)
    except OSError as exc:
        raise CodexEnvError(
            f"{error_prefix}: failed to copy auth.json to {auth_dst}: {exc}"
        ) from exc
    validate_chatgpt_auth(auth_dst, error_prefix=error_prefix)
    env["CODEX_HOME"] = str(codex_home)
    return CodexEnvironment(
        env=env,
        auth_src=auth_src,
        auth_dst=auth_dst,
        codex_home=codex_home,
    )
