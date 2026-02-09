from __future__ import annotations

import os
from typing import Dict

COMPACTED_LOGS_DIR = os.path.join("docs", "03-logs", "compacted")
COMPACTED_LOG_OUTPUT_NAMES = {
    "decision": "decision-log-compact.json",
    "implementation": "implementation-log-compact.json",
    "validation": "validation-log-compact.json",
}


def compacted_logs_dir() -> str:
    return COMPACTED_LOGS_DIR


def compacted_log_output_paths() -> Dict[str, str]:
    return {
        key: os.path.join(compacted_logs_dir(), name)
        for key, name in COMPACTED_LOG_OUTPUT_NAMES.items()
    }
