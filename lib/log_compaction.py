from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional

COMPACTED_LOGS_DIR = os.path.join("docs", "03-logs", "compacted")
COMPACTED_LOG_OUTPUT_NAMES = {
    "decision": "decision-log-compact.json",
    "implementation": "implementation-log-compact.json",
    "validation": "validation-log-compact.json",
}
COMPACTED_LOGS_DIR_ENV = "PC_COMPACTED_LOGS_DIR"
REPO_ROOT = Path(__file__).resolve().parents[1]


def compacted_logs_dir() -> str:
    return os.environ.get(COMPACTED_LOGS_DIR_ENV, COMPACTED_LOGS_DIR)


def resolve_compacted_logs_dir(root: Optional[Path] = None) -> str:
    base = compacted_logs_dir()
    if os.path.isabs(base):
        return base
    base_root = root or REPO_ROOT
    return str(base_root / base)


def compacted_log_output_paths(root: Optional[Path] = None) -> Dict[str, str]:
    output_root = resolve_compacted_logs_dir(root)
    return {
        key: os.path.join(output_root, name)
        for key, name in COMPACTED_LOG_OUTPUT_NAMES.items()
    }
