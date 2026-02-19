"""Shared parsing/validation helpers for feature dev-tasks status lines."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Tuple

CANONICAL_STATUS_PATTERN = re.compile(r"^Status:\s*(.*?)\s*$", re.MULTILINE)
LEGACY_BOLD_STATUS_PATTERN = re.compile(r"^\*\*Status:\*\*\s*(.*?)\s*$", re.MULTILINE)
COMPLETED_STATUS_PATTERN = re.compile(
    r"\b(done|complete|completed|shipped)\b", re.IGNORECASE
)


def _canonical_status_values(content: str) -> List[str]:
    return [
        match.group(1).strip() for match in CANONICAL_STATUS_PATTERN.finditer(content)
    ]


def _legacy_status_values(content: str) -> List[str]:
    return [
        match.group(1).strip() for match in LEGACY_BOLD_STATUS_PATTERN.finditer(content)
    ]


def status_format_errors(content: str) -> List[str]:
    canonical_values = _canonical_status_values(content)
    legacy_values = _legacy_status_values(content)

    errors: List[str] = []
    if legacy_values:
        errors.append("legacy '**Status:**' format is not allowed (use 'Status:')")
    if not canonical_values:
        errors.append("missing canonical 'Status:' line")
        return errors

    if len(canonical_values) > 1:
        errors.append("multiple canonical 'Status:' lines found")
    if any(not value for value in canonical_values):
        errors.append("canonical 'Status:' line is missing a value")
    return errors


def parse_status_from_content(content: str) -> Tuple[Optional[str], Optional[str]]:
    canonical_values = _canonical_status_values(content)
    if not canonical_values:
        if _legacy_status_values(content):
            return None, "legacy '**Status:**' format is not allowed"
        return None, "Status line not found"

    value = canonical_values[0]
    if not value:
        return None, "Status line missing value"
    if len(canonical_values) > 1:
        return value, "Multiple Status lines found"
    return value, None


def parse_status_from_file(path: Path) -> Tuple[Optional[str], Optional[str]]:
    if not path.exists():
        return None, "dev-tasks.md missing"
    return parse_status_from_content(path.read_text(encoding="utf-8"))


def is_completed_status(status: Optional[str]) -> bool:
    if not status:
        return False
    return bool(COMPLETED_STATUS_PATTERN.search(status.strip()))
