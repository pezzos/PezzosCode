from __future__ import annotations

import json
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

WORK_ITEM_RE = re.compile(r"^WI-\d{8}-\d{2}$")
PROPOSAL_SECTION_HEADER = "## Entries"
PROPOSAL_ENTRY_SEPARATOR = "---"
PROPOSAL_STATUS_PROPOSED = "Proposed"
PROPOSAL_PLACEHOLDER_UNKNOWN = "Unknown"
PROPOSAL_PLACEHOLDER_TBD = "TBD"
WORKFLOW_STATUS_FILENAME = "workflow-status.json"
WORKFLOW_HISTORY_FILENAME = "workflow-history.ndjson"


@dataclass(frozen=True)
class ProposalEntry:
    date: str
    work_item_id: str
    agent: str
    step: str
    failure_summary: str
    proposed_improvement: str
    proposed_patch_location: str
    risks: str
    status: str
    decision_log_ref: str


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


def workflow_status_path(root: Path, work_item_id: str) -> Path:
    return log_dir(root, work_item_id) / WORKFLOW_STATUS_FILENAME


def workflow_history_path(root: Path, work_item_id: str) -> Path:
    return log_dir(root, work_item_id) / WORKFLOW_HISTORY_FILENAME


def _utc_timestamp(timestamp: Optional[str] = None) -> str:
    if timestamp:
        return timestamp
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _default_workflow_status(
    metadata: RunMetadata,
    *,
    feature_id: str = "",
    feature_slug: str = "",
    mode: str = "",
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    ts = _utc_timestamp(timestamp)
    return {
        "work_item_id": metadata.work_item_id,
        "agent_name": metadata.agent_name,
        "run_id": metadata.run_id,
        "feature_id": feature_id,
        "feature_slug": feature_slug,
        "mode": mode,
        "started_at": ts,
        "updated_at": ts,
        "state": "RUNNING",
        "current_step": None,
        "current_attempt": None,
        "last_event": {},
        "steps": {},
        "open_steps": {},
    }


def _read_json_object(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"pc_runner: failed to read status {path}: {exc}") from exc
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_json_object(path: Path, payload: Mapping[str, Any]) -> None:
    serialized = json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    try:
        path.write_text(serialized, encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"pc_runner: failed to write status {path}: {exc}") from exc


def _parse_utc_timestamp(timestamp: str) -> Optional[datetime]:
    try:
        parsed = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc)


def _duration_ms(start_ts: str, end_ts: str) -> Optional[int]:
    start = _parse_utc_timestamp(start_ts)
    end = _parse_utc_timestamp(end_ts)
    if not start or not end:
        return None
    delta = int((end - start).total_seconds() * 1000)
    return max(delta, 0)


def init_workflow_tracking(
    metadata: RunMetadata,
    *,
    root: Optional[Path] = None,
    feature_id: str = "",
    feature_slug: str = "",
    mode: str = "",
    timestamp: Optional[str] = None,
) -> Tuple[Path, Path]:
    root_path = Path(root or Path(os.getcwd()))
    status_path = workflow_status_path(root_path, metadata.work_item_id)
    history_path = workflow_history_path(root_path, metadata.work_item_id)
    status_payload = _default_workflow_status(
        metadata,
        feature_id=feature_id,
        feature_slug=feature_slug,
        mode=mode,
        timestamp=timestamp,
    )
    _write_json_object(status_path, status_payload)
    if not history_path.exists():
        try:
            history_path.touch()
        except OSError as exc:
            raise RuntimeError(
                f"pc_runner: failed to create history {history_path}: {exc}"
            ) from exc
    return status_path, history_path


def record_workflow_event(
    metadata: RunMetadata,
    *,
    step: str,
    event: str,
    attempt: Optional[int] = None,
    outcome: str = "",
    reason: str = "",
    state: Optional[str] = None,
    root: Optional[Path] = None,
    timestamp: Optional[str] = None,
) -> Mapping[str, Any]:
    root_path = Path(root or Path(os.getcwd()))
    ts = _utc_timestamp(timestamp)
    status_path = workflow_status_path(root_path, metadata.work_item_id)
    history_path = workflow_history_path(root_path, metadata.work_item_id)
    status = _read_json_object(status_path)
    if not status:
        status = _default_workflow_status(metadata, timestamp=ts)
    steps = status.setdefault("steps", {})
    if not isinstance(steps, dict):
        steps = {}
        status["steps"] = steps
    open_steps = status.setdefault("open_steps", {})
    if not isinstance(open_steps, dict):
        open_steps = {}
        status["open_steps"] = open_steps

    step_key = (step or "unknown").strip()
    step_state = steps.setdefault(step_key, {})
    if not isinstance(step_state, dict):
        step_state = {}
        steps[step_key] = step_state
    event_name = (event or "").strip().upper() or "INFO"

    duration = None
    if event_name == "START":
        step_state["runs"] = int(step_state.get("runs", 0)) + 1
        step_state["last_started_at"] = ts
        open_steps[step_key] = ts
        status["current_step"] = step_key
        status["current_attempt"] = attempt
        status["state"] = "RUNNING"
    else:
        start_ts = str(open_steps.pop(step_key, "")).strip()
        if start_ts:
            duration = _duration_ms(start_ts, ts)
        step_state["last_ended_at"] = ts
        if duration is not None:
            step_state["last_duration_ms"] = duration
        if status.get("current_step") == step_key:
            status["current_step"] = None
            status["current_attempt"] = None
        if state:
            status["state"] = state

    if attempt is not None:
        step_state["last_attempt"] = attempt
    step_state["last_event"] = event_name
    if outcome:
        step_state["last_outcome"] = outcome
    if reason:
        step_state["last_reason"] = reason

    event_payload: Dict[str, Any] = {
        "timestamp": ts,
        "work_item_id": metadata.work_item_id,
        "agent_name": metadata.agent_name,
        "run_id": metadata.run_id,
        "step": step_key,
        "event": event_name,
    }
    if attempt is not None:
        event_payload["attempt"] = attempt
    if outcome:
        event_payload["outcome"] = outcome
    if reason:
        event_payload["reason"] = reason
    if duration is not None:
        event_payload["duration_ms"] = duration

    status["updated_at"] = ts
    status["last_event"] = event_payload
    _write_json_object(status_path, status)
    try:
        with history_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event_payload, ensure_ascii=True, sort_keys=True))
            handle.write("\n")
    except OSError as exc:
        raise RuntimeError(f"pc_runner: failed to write history {history_path}: {exc}")
    return event_payload


OUTCOME_FAIL = {"FAIL", "FAILED", "ERROR"}
OUTCOME_STALL = {"STALL", "STALLED", "NEEDS REPLAN", "NEEDS_REPLAN"}


def _coerce_str(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return ", ".join([str(item).strip() for item in value if str(item).strip()])
    return str(value).strip()


def _coerce_agents(value: object) -> str:
    if isinstance(value, (list, tuple, set)):
        cleaned = sorted({str(item).strip() for item in value if str(item).strip()})
        return ", ".join(cleaned)
    return _coerce_str(value)


def _normalize_outcome(value: object) -> str:
    if value is None:
        return ""
    cleaned = re.sub(r"[\s_-]+", " ", str(value)).strip().upper()
    return cleaned


def _missing_context_note(fields: Iterable[str]) -> str:
    missing = ", ".join(fields)
    return f"Missing context: {missing}" if missing else ""


def normalize_failure_summary(summary: str) -> str:
    cleaned = re.sub(r"\(missing context:.*?\)", "", summary or "", flags=re.IGNORECASE)
    compact = re.sub(r"\s+", " ", cleaned.strip().lower())
    return compact


def proposal_signature(
    work_item_id: str, step: str, failure_summary: str
) -> Tuple[str, str, str]:
    return (
        (work_item_id or "").strip().lower(),
        (step or "").strip().lower(),
        normalize_failure_summary(failure_summary),
    )


def _is_placeholder(value: str) -> bool:
    lowered = (value or "").strip().lower()
    if lowered.startswith("tbd"):
        return True
    if lowered.startswith("unknown"):
        return True
    return lowered in {
        "",
        "none noted",
        "none noted.",
        "n/a",
        "dec-tbd",
        "no failure summary provided.",
    }


def build_proposal_from_outcome(
    outcome: Mapping[str, object], *, date: Optional[str] = None
) -> Optional[ProposalEntry]:
    outcome_value = _normalize_outcome(
        outcome.get("outcome")
        or outcome.get("status")
        or outcome.get("result")
        or outcome.get("state")
    )
    if outcome_value not in OUTCOME_FAIL and outcome_value not in OUTCOME_STALL:
        return None

    missing_context = []
    work_item_id = _coerce_str(outcome.get("work_item_id") or outcome.get("work_item"))
    if not work_item_id:
        work_item_id = PROPOSAL_PLACEHOLDER_UNKNOWN
        missing_context.append("Work Item")

    agent = _coerce_agents(
        outcome.get("agent_names")
        or outcome.get("agents")
        or outcome.get("agent_name")
        or outcome.get("agent")
    )
    if not agent:
        agent = PROPOSAL_PLACEHOLDER_UNKNOWN
        missing_context.append("Agent")

    step = _coerce_str(
        outcome.get("step") or outcome.get("phase") or outcome.get("stage")
    )
    if not step:
        step = PROPOSAL_PLACEHOLDER_UNKNOWN
        missing_context.append("Step")

    failure_summary = _coerce_str(
        outcome.get("failure_summary")
        or outcome.get("summary")
        or outcome.get("error")
        or outcome.get("failure")
    )
    if not failure_summary:
        failure_summary = "No failure summary provided."
        missing_context.append("Failure Summary")

    missing_note = _missing_context_note(missing_context)
    if missing_note:
        failure_summary = f"{failure_summary} ({missing_note})"

    proposed_improvement = _coerce_str(
        outcome.get("proposed_improvement")
        or outcome.get("proposal")
        or outcome.get("improvement")
    )
    if not proposed_improvement:
        proposed_improvement = "TBD - investigate failure and propose remediation."

    proposed_patch_location = _coerce_str(
        outcome.get("proposed_patch_location")
        or outcome.get("patch_location")
        or outcome.get("patch")
        or outcome.get("files")
        or outcome.get("paths")
    )
    if not proposed_patch_location:
        proposed_patch_location = PROPOSAL_PLACEHOLDER_TBD

    risks = _coerce_str(
        outcome.get("risks")
        or outcome.get("tradeoffs")
        or outcome.get("risks_tradeoffs")
    )
    if not risks:
        risks = "None noted."

    decision_log_ref = _coerce_str(
        outcome.get("decision_log_ref") or outcome.get("decision_ref")
    )
    if not decision_log_ref:
        decision_log_ref = "DEC-TBD"

    date_value = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return ProposalEntry(
        date=date_value,
        work_item_id=work_item_id,
        agent=agent,
        step=step,
        failure_summary=failure_summary,
        proposed_improvement=proposed_improvement,
        proposed_patch_location=proposed_patch_location,
        risks=risks,
        status=PROPOSAL_STATUS_PROPOSED,
        decision_log_ref=decision_log_ref,
    )


def render_proposal_entry_block(proposal: ProposalEntry) -> str:
    lines = [
        f"### Proposal: {proposal.work_item_id} - {proposal.step}",
        f"**Date:** {proposal.date}",
        f"**Work Item:** {proposal.work_item_id}",
        f"**Agent:** {proposal.agent}",
        f"**Step:** {proposal.step}",
        f"**Failure Summary:** {proposal.failure_summary}",
        f"**Proposed Improvement:** {proposal.proposed_improvement}",
        f"**Proposed Patch Location:** {proposal.proposed_patch_location}",
        f"**Risks / Trade-offs:** {proposal.risks}",
        f"**Status:** {proposal.status}",
        f"**Decision Log Ref:** {proposal.decision_log_ref}",
    ]
    return "\n".join(lines).rstrip()


def render_proposal_entry(proposal: ProposalEntry) -> str:
    return (
        render_proposal_entry_block(proposal) + "\n" + PROPOSAL_ENTRY_SEPARATOR + "\n"
    )


def _parse_entry_fields(lines: Sequence[str]) -> Mapping[str, str]:
    fields = {}
    for line in lines:
        match = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", line.strip())
        if match:
            fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def _merge_failure_summary(existing: str, incoming: str) -> str:
    if _is_placeholder(existing) and not _is_placeholder(incoming):
        return incoming
    if "missing context:" in existing.lower() and not _is_placeholder(incoming):
        return incoming
    return existing


def _merge_agents(existing: str, incoming: str) -> str:
    if _is_placeholder(existing) and not _is_placeholder(incoming):
        return incoming
    if _is_placeholder(incoming):
        return existing
    existing_names = [
        part.strip() for part in (existing or "").split(",") if part.strip()
    ]
    incoming_names = [
        part.strip() for part in (incoming or "").split(",") if part.strip()
    ]
    merged: List[str] = []
    for name in existing_names + incoming_names:
        if name not in merged:
            merged.append(name)
    if not merged:
        return existing if existing else incoming
    return ", ".join(merged)


def _merge_status(existing: str, incoming: str) -> str:
    if _is_placeholder(existing) and not _is_placeholder(incoming):
        return incoming
    if existing:
        return existing
    return incoming


def _merge_proposal(existing: ProposalEntry, incoming: ProposalEntry) -> ProposalEntry:
    return ProposalEntry(
        date=existing.date if not _is_placeholder(existing.date) else incoming.date,
        work_item_id=existing.work_item_id,
        agent=_merge_agents(existing.agent, incoming.agent),
        step=existing.step if not _is_placeholder(existing.step) else incoming.step,
        failure_summary=_merge_failure_summary(
            existing.failure_summary, incoming.failure_summary
        ),
        proposed_improvement=(
            existing.proposed_improvement
            if not _is_placeholder(existing.proposed_improvement)
            else incoming.proposed_improvement
        ),
        proposed_patch_location=(
            existing.proposed_patch_location
            if not _is_placeholder(existing.proposed_patch_location)
            else incoming.proposed_patch_location
        ),
        risks=existing.risks if not _is_placeholder(existing.risks) else incoming.risks,
        status=_merge_status(existing.status, incoming.status),
        decision_log_ref=(
            existing.decision_log_ref
            if not _is_placeholder(existing.decision_log_ref)
            else incoming.decision_log_ref
        ),
    )


def merge_or_append_proposal(content: str, proposal: ProposalEntry) -> Tuple[str, str]:
    lines = content.splitlines()
    entries_index = None
    for idx, line in enumerate(lines):
        if line.strip() == PROPOSAL_SECTION_HEADER:
            entries_index = idx + 1
            break
    if entries_index is None:
        raise ValueError("pc_runner: missing entries section in proposal registry")

    prefix_lines = lines[:entries_index]
    tail_lines = lines[entries_index:]
    before_entries: list[str] = []
    suffix_lines: list[str] = []
    blocks: list[list[str]] = []
    current: list[str] = []

    for line in tail_lines:
        if line.strip() == PROPOSAL_ENTRY_SEPARATOR:
            if current:
                blocks.append(current)
                current = []
            continue
        if not current:
            if line.strip().startswith("<!--"):
                suffix_lines.append(line)
                continue
            if not line.strip():
                before_entries.append(line)
                continue
        current.append(line)
    if current:
        blocks.append(current)

    incoming_sig = proposal_signature(
        proposal.work_item_id, proposal.step, proposal.failure_summary
    )
    updated_blocks: list[str] = []
    action = "appended"
    matched = False

    for block in blocks:
        fields = _parse_entry_fields(block)
        existing = ProposalEntry(
            date=fields.get("Date", PROPOSAL_PLACEHOLDER_UNKNOWN),
            work_item_id=fields.get("Work Item", PROPOSAL_PLACEHOLDER_UNKNOWN),
            agent=fields.get("Agent", PROPOSAL_PLACEHOLDER_UNKNOWN),
            step=fields.get("Step", PROPOSAL_PLACEHOLDER_UNKNOWN),
            failure_summary=fields.get("Failure Summary", ""),
            proposed_improvement=fields.get(
                "Proposed Improvement", PROPOSAL_PLACEHOLDER_TBD
            ),
            proposed_patch_location=fields.get(
                "Proposed Patch Location", PROPOSAL_PLACEHOLDER_TBD
            ),
            risks=fields.get("Risks / Trade-offs", "None noted."),
            status=fields.get("Status", PROPOSAL_STATUS_PROPOSED),
            decision_log_ref=fields.get("Decision Log Ref", "DEC-TBD"),
        )
        existing_sig = proposal_signature(
            existing.work_item_id, existing.step, existing.failure_summary
        )
        if existing_sig == incoming_sig and not matched:
            matched = True
            merged = _merge_proposal(existing, proposal)
            if merged != existing:
                updated_blocks.append(render_proposal_entry_block(merged))
                action = "merged"
            else:
                updated_blocks.append("\n".join(block).rstrip())
                action = "skipped"
            continue
        updated_blocks.append("\n".join(block).rstrip())

    if not matched:
        updated_blocks.insert(0, render_proposal_entry_block(proposal))

    rebuilt_lines = prefix_lines + before_entries
    for block_text in updated_blocks:
        if block_text:
            rebuilt_lines.extend(block_text.splitlines())
            rebuilt_lines.append(PROPOSAL_ENTRY_SEPARATOR)
            rebuilt_lines.append("")

    rebuilt_lines.extend(suffix_lines)
    return "\n".join(rebuilt_lines).rstrip() + "\n", action


def update_possible_improvements(
    path: Path, proposal: ProposalEntry
) -> Tuple[str, str]:
    content = path.read_text(encoding="utf-8")
    updated, action = merge_or_append_proposal(content, proposal)
    if updated != content:
        path.write_text(updated, encoding="utf-8")
    return updated, action


def record_outcome_proposal(
    outcome_payload: Mapping[str, object],
    *,
    root: Path,
    runner_metadata: Optional[RunMetadata] = None,
    date: Optional[str] = None,
) -> Optional[str]:
    proposal = build_proposal_from_outcome(outcome_payload, date=date)
    if not proposal:
        return None
    path = root / "docs" / "possible-improvements.md"
    if not path.exists():
        if runner_metadata:
            log_message(
                runner_metadata,
                "feature",
                f"proposal skip missing {path}",
                root=root,
            )
        return None
    _, action = update_possible_improvements(path, proposal)
    if runner_metadata:
        log_message(
            runner_metadata,
            "feature",
            f"proposal {action} signature={proposal_signature(proposal.work_item_id, proposal.step, proposal.failure_summary)}",
            root=root,
        )
    return action
