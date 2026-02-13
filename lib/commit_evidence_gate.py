from __future__ import annotations

import re
from typing import Dict, List, Set, Tuple

REQUIRED_SECTIONS = ("Test Results", "Commit", "Final Report")
REQUIRED_FINAL_REPORT_FIELDS = (
    "What changed (files)",
    "Tests written (names) + results",
    "Docs/logs updated checklist",
    "make ci results",
    "Commands run (use pp for noisy output)",
    "Commit message",
)
COMPLETED_TICKET_STATUSES = {"completed", "pass"}
COMMIT_EVIDENCE_REMEDIATION = (
    'Remediation: complete required "Test Results", "Commit", and '
    '"Final Report" evidence before commit.'
)
MISSING_ENTRY_HEADER_ISSUE = (
    "missing work-item execution entry header (expected `### WI-YYYYMMDD-NN`)"
)

ENTRY_PATTERN = re.compile(r"^###\s+(WI-\d{8}-\d{2})\b.*$", re.MULTILINE)
SECTION_PATTERN = re.compile(r"^####\s+(.+?)\s*$", re.MULTILINE)
OUTCOME_PATTERN = re.compile(
    r"Outcome:\s*(PASS|FAIL|NEEDS REPLAN|SKIPPED)",
    re.IGNORECASE,
)
WORK_ITEM_PATTERN = re.compile(r"^WI-(\d{8})-(\d{2})$")


def normalize_ticket_status(value: str) -> str:
    return " ".join(str(value or "").strip().split()).lower()


def parse_labeled_line(text: str, label: str) -> str:
    pattern = re.compile(
        rf"^(?:-\s*)?{re.escape(label)}\s*:[ \t]*(.*?)\s*$",
        re.MULTILINE | re.IGNORECASE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def work_item_sort_key(work_item_id: str) -> Tuple[str, int]:
    match = WORK_ITEM_PATTERN.fullmatch(work_item_id or "")
    if not match:
        return ("00000000", 0)
    return (match.group(1), int(match.group(2)))


def collect_entry_blocks(content: str) -> List[Tuple[str, str]]:
    matches = list(ENTRY_PATTERN.finditer(content))
    if not matches:
        return []
    entries: List[Tuple[str, str]] = []
    for idx, marker in enumerate(matches):
        start = marker.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        entries.append((marker.group(1), content[start:end]))
    return entries


def select_entry_block(
    content: str, target_work_item_id: str = ""
) -> Tuple[str, str, str]:
    entries = collect_entry_blocks(content)
    if not entries:
        return ("", "", "")
    if target_work_item_id:
        for candidate_id, candidate_block in entries:
            if candidate_id == target_work_item_id:
                return candidate_id, candidate_block, ""
        return (
            target_work_item_id,
            "",
            f"requested work-item execution entry not found: {target_work_item_id}",
        )
    selected_id, selected_block = max(
        entries, key=lambda item: work_item_sort_key(item[0])
    )
    return selected_id, selected_block, ""


def parse_sections(block: str) -> Tuple[Dict[str, str], Set[str]]:
    sections: Dict[str, str] = {}
    duplicates: Set[str] = set()
    matches = list(SECTION_PATTERN.finditer(block))
    for idx, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(block)
        body = block[start:end].strip()
        if title in sections:
            duplicates.add(title)
        else:
            sections[title] = body
    return sections, duplicates


def commit_evidence_gate_issues_for_block(block: str) -> List[str]:
    issues: List[str] = []
    sections, duplicates = parse_sections(block)

    tests_run_field = parse_labeled_line(block, "Tests run")
    if not tests_run_field:
        issues.append("missing top execution field: Tests run")

    ticket_status_field = parse_labeled_line(block, "Outcome")
    normalized_ticket_status = normalize_ticket_status(ticket_status_field)
    if not normalized_ticket_status:
        issues.append("missing top execution field: Outcome")
    elif normalized_ticket_status not in COMPLETED_TICKET_STATUSES:
        issues.append(
            "active ticket status is not completed: "
            f"Outcome={ticket_status_field or '(empty)'}"
        )

    for section in REQUIRED_SECTIONS:
        if section in duplicates:
            issues.append(f"duplicate required section heading: {section}")
        body = sections.get(section, "").strip()
        if section not in sections:
            issues.append(f"missing required section: {section}")
            continue
        if not body:
            issues.append(f"required section is empty: {section}")
            continue
        if "(pending)" in body.lower():
            issues.append(f"required section still pending: {section}")

    test_results = sections.get("Test Results", "")
    if test_results and not OUTCOME_PATTERN.search(test_results):
        issues.append("Test Results is missing Outcome")

    commit_section = sections.get("Commit", "")
    if commit_section and not parse_labeled_line(commit_section, "Commit message"):
        issues.append("Commit section is missing Commit message")

    final_report = sections.get("Final Report", "")
    if final_report:
        for field in REQUIRED_FINAL_REPORT_FIELDS:
            if not parse_labeled_line(final_report, field):
                issues.append(f"Final Report is missing required field: {field}")

    return issues


def commit_evidence_gate_issues(
    content: str, *, work_item_id: str = ""
) -> Tuple[str, List[str]]:
    selected_id, block, selection_issue = select_entry_block(content, work_item_id)
    if selection_issue:
        return selected_id, [selection_issue]
    if not block:
        return selected_id, [MISSING_ENTRY_HEADER_ISSUE]
    return selected_id, commit_evidence_gate_issues_for_block(block)
