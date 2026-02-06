from __future__ import annotations

import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

WORK_ITEM_RE = re.compile(r"^WI-\d{8}-\d{2}$")


@dataclass(frozen=True)
class RunMetadata:
    work_item_id: str
    agent_name: str
    run_id: str


def generate_run_id() -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{timestamp}-{uuid.uuid4().hex[:8]}"


def validate_work_item_id(work_item_id: str) -> None:
    if not work_item_id or not WORK_ITEM_RE.match(work_item_id):
        raise ValueError(
            "pc_runner: work_item_id is required and must match WI-YYYYMMDD-XX"
        )


def build_metadata(
    work_item_id: str, agent_name: str, run_id: Optional[str] = None
) -> RunMetadata:
    if not agent_name:
        raise ValueError("pc_runner: agent_name is required")
    if not run_id:
        run_id = generate_run_id()
    validate_work_item_id(work_item_id)
    return RunMetadata(work_item_id=work_item_id, agent_name=agent_name, run_id=run_id)


def log_dir(root: Path, work_item_id: str) -> Path:
    path = root / "logs" / work_item_id
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RuntimeError(
            f"pc_runner: failed to create log dir {path}: {exc}"
        ) from exc
    return path


def log_path(root: Path, work_item_id: str, step: str) -> Path:
    return log_dir(root, work_item_id) / f"{step}.log"


def format_prefix(metadata: RunMetadata, step: str) -> str:
    return f"[{metadata.work_item_id}][{metadata.agent_name}][{step}]"


def format_log_line(
    metadata: RunMetadata,
    step: str,
    message: str,
    *,
    timestamp: Optional[str] = None,
) -> str:
    ts = timestamp or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    prefix = format_prefix(metadata, step)
    return f"{ts} {prefix} {message}".rstrip() + "\n"


def log_message(
    metadata: RunMetadata,
    step: str,
    message: str,
    *,
    root: Optional[Path] = None,
    timestamp: Optional[str] = None,
) -> Path:
    root_path = Path(root or Path(os.getcwd()))
    path = log_path(root_path, metadata.work_item_id, step)
    line = format_log_line(metadata, step, message, timestamp=timestamp)
    try:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line)
    except OSError as exc:
        raise RuntimeError(f"pc_runner: failed to write log {path}: {exc}") from exc
    return path
