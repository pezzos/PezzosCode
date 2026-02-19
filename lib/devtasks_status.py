"""Shared parsing/validation helpers for feature dev-tasks status lines."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Tuple

CANONICAL_STATUS_PATTERN = re.compile(r"^Status:\s*(.*?)\s*$", re.MULTILINE)
LEGACY_BOLD_STATUS_PATTERN = re.compile(r"^\*\*Status:\*\*\s*(.*?)\s*$", re.MULTILINE)
ALLOWED_STATUS_VALUES = ("Not Started", "In Progress", "Done")
COMPLETED_STATUS_VALUE = "Done"


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
    for value in canonical_values:
        if value and value not in ALLOWED_STATUS_VALUES:
            errors.append(
                "invalid status value "
                f"'{value}' (allowed: {', '.join(ALLOWED_STATUS_VALUES)})"
            )
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
    if value not in ALLOWED_STATUS_VALUES:
        return value, (
            f"Invalid status value '{value}' "
            f"(allowed: {', '.join(ALLOWED_STATUS_VALUES)})"
        )
    return value, None


def parse_status_from_file(path: Path) -> Tuple[Optional[str], Optional[str]]:
    if not path.exists():
        return None, "dev-tasks.md missing"
    return parse_status_from_content(path.read_text(encoding="utf-8"))


def is_completed_status(status: Optional[str]) -> bool:
    if not status:
        return False
    return status.strip() == COMPLETED_STATUS_VALUE
