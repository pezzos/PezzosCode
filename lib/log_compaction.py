from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

COMPACTED_LOG_OUTPUT_NAMES = {
    "decision": "decision-log-compact.json",
    "implementation": "implementation-log-compact.json",
    "validation": "validation-log-compact.json",
}
COMPACTED_LLM_OUTPUT_NAMES = {
    "decision": "decision-log-compact.llm.json",
    "implementation": "implementation-log-compact.llm.json",
    "validation": "validation-log-compact.llm.json",
}
COMPACTION_REPORT_NAME = "compaction-report.json"
SEMANTIC_MAP_NAME = "semantic-map.json"
COMPACTED_LOGS_DIR_ENV = "PC_COMPACTED_LOGS_DIR"
COMPACTION_CONFIG_ENV = "PC_LOG_COMPACTION_CONFIG"
DEFAULT_COMPACTION_CONFIG_PATH = Path("tools") / "log-compaction-config.json"
DEFAULT_COMPACTED_LOGS_DIR = "docs/03-logs/compacted"
REPO_ROOT = Path(__file__).resolve().parents[1]


def resolve_compaction_config_path(root: Optional[Path] = None) -> Path:
    override = os.environ.get(COMPACTION_CONFIG_ENV)
    config_path = Path(override) if override else DEFAULT_COMPACTION_CONFIG_PATH
    if config_path.is_absolute():
        return config_path
    base_root = root or REPO_ROOT
    return base_root / config_path


def load_compaction_config(root: Optional[Path] = None) -> Dict[str, Any]:
    config_path = resolve_compaction_config_path(root)
    try:
        with open(config_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError:
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload


def log_sources(root: Optional[Path] = None) -> Dict[str, str]:
    config = load_compaction_config(root)
    sources = config.get("log_sources")
    if not isinstance(sources, dict):
        return {}
    return {str(key): str(value) for key, value in sources.items()}


def compacted_logs_dir(root: Optional[Path] = None) -> str:
    config = load_compaction_config(root)
    configured = config.get("compacted_logs_dir")
    if isinstance(configured, str) and configured.strip():
        return configured
    override = os.environ.get(COMPACTED_LOGS_DIR_ENV)
    if override and override.strip():
        return override
    return DEFAULT_COMPACTED_LOGS_DIR


def resolve_compacted_logs_dir(root: Optional[Path] = None) -> str:
    base = compacted_logs_dir(root)
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


def compacted_llm_output_paths(root: Optional[Path] = None) -> Dict[str, str]:
    output_root = resolve_compacted_logs_dir(root)
    return {
        key: os.path.join(output_root, name)
        for key, name in COMPACTED_LLM_OUTPUT_NAMES.items()
    }


def compaction_report_path(root: Optional[Path] = None) -> str:
    return os.path.join(resolve_compacted_logs_dir(root), COMPACTION_REPORT_NAME)


def semantic_map_path(root: Optional[Path] = None) -> str:
    return os.path.join(resolve_compacted_logs_dir(root), SEMANTIC_MAP_NAME)
