# Feature Specification: Offload audit + useful log compaction

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-15`

**Owner:** Developer/PO

**Last Updated:** 2026-02-10

### Summary

Implement observability and lifecycle management for offloaded command output, then add useful compact views for long-lived logs so continuous workflow improvement stays practical without losing source records.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** trace offload usage and keep historical logs reviewable for iterative workflow improvement
- **Current pain:** offload data exists in `.offload/` but lacks index/retention controls; decision/implementation/validation logs become too large to consume efficiently

### Why do they need it?

**As a** developer/PO

**I want to** audit offload artifacts and generate compact, useful log views

**So that** I can debug quickly and preserve traceability with lower token cost

### User Value

- **Value proposition:** auditable offload storage plus compact logs that preserve the context needed to improve the workflow
- **Expected impact:** lower context load, easier incident review, and more reliable improvement loops
- **Priority:** P2 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Create an offload index capturing `id`, `command`, `work_item_id`, `agent_name`, `timestamp`, and `size_bytes` for each offloaded artifact.
- **Requirement 2:** Add deterministic list/get/purge utilities for indexed artifacts with retention support.
- **Requirement 3:** Implement compaction skills for `docs/03-logs/decision-log.md`, `docs/03-logs/implementation-log.md`, and `docs/03-logs/validation-log.md` that produce concise summaries without deleting source logs.
- **Requirement 4:** Define a compact-output usefulness contract with required fields: source file, source section/date reference, work item reference (if available), concise outcome/rationale summary, and evidence reference(s) (for example offload id or step log path).
- **Requirement 5:** Store compact outputs in a non-destructive derived location (`docs/03-logs/compacted/`) and keep canonical logs unchanged.
- **Requirement 6:** Keep offload and compaction actions traceable in docs/logs.

#### Edge Cases

- **Edge Case 1:** Index entry exists but backing `.offload/<id>.txt` file is missing.
- **Edge Case 2:** Purge policy removes artifacts still referenced by active work items.
- **Edge Case 3:** Compaction removes critical rationale, chronology, or validation evidence.
- **Edge Case 4:** Compact artifact exists but points to stale/missing source sections after log growth.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Offload index is generated/maintained with required metadata fields.
- List/get/purge commands work on indexed artifacts and respect retention policy.
- Compaction skills produce compact outputs for decision/implementation/validation logs with required usefulness fields and no source-file deletion.
- Compact outputs are written to `docs/03-logs/compacted/` and preserve source references.
- Validation confirms compaction preserves key decision, implementation, and validation traceability.

## Scope

### In Scope

- Offload metadata index and lifecycle commands
- Retention rules for `.offload/`
- Log-compaction skills and their usage guidance for decision/implementation/validation logs
- Compact-output usefulness contract and derived output location
- Tests for index/retention/compaction invariants

### Out of Scope

- Remote artifact storage
- Destructive rewriting of canonical `docs/03-logs/*.md`
- New UI for offload browsing

## Dependencies

### Requires

- **Offload wrapper:** `tools/offload-proxy/pp`
- **Offload config:** `pp.yml`
- **Process docs:** `docs/04-process/output-offload.md`
- **Log sources:** `docs/03-logs/decision-log.md`, `docs/03-logs/implementation-log.md`, `docs/03-logs/validation-log.md`
- **Derived output location:** `docs/03-logs/compacted/`

### Blocks

- **None**

## Risks & Considerations

- Aggressive retention can break reproducibility/debugging.
- Poor compaction heuristics can hide high-impact details or strip evidence needed for learning loops.

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                                      | Risk                                                                                                                                                                                                                     | Action                                                                                                                                                                                                                                          |
| ---------- | -------- | ------- | -------------- | -------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-15-001 | High     | patcher | patch          | Yes      | Unredacted command capture in offload index                                | Requirement 1 requires persisting full `command` metadata, but no redaction control is defined in the provided spec/tasks. Secrets passed via CLI args can be stored in `.offload/index.jsonl` and propagated into logs. | Implement deterministic command scrubbing before index write (secret-pattern masking, sensitive-flag masking, length caps), scrub existing index entries, and add regression tests proving secret-like inputs are never persisted in cleartext. |
| SEC-15-002 | High     | patcher | patch          | Yes      | Purge can delete evidence referenced by active work items                  | Edge Case 2 explicitly states purge may remove artifacts still referenced by active work items, but no fail-closed safeguard is specified. This can destroy forensic evidence and undermine incident reconstruction.     | Add reference-aware purge protection that blocks deletion of referenced IDs by default, require explicit override for destructive purge, and emit immutable audit log entries for overrides.                                                    |
| SEC-15-003 | Medium   | patcher | automated-test | Yes      | Security-critical invariants are not enforced by current allowed test gate | The current Allowed Tests list in dev-tasks is narrowed to `tests.test_pc_feature`, so offload index/retention/compaction controls can regress without automated detection.                                              | Reinstate and enforce automated suites covering `tests/test_offload_index.py`, `tests/test_offload_retention.py`, and `tests/test_log_compaction.py`; fail workflow if these suites are omitted or skipped.                                     |
| SEC-15-004 | Medium   | patcher | patch          | Yes      | Compaction destination integrity is not fail-closed                        | Iteration logs show compacted artifacts were repeatedly written outside required `docs/03-logs/compacted/`. Uncontrolled output paths create shadow audit records and weaken traceability integrity.                     | Enforce strict output-path validation (only `docs/03-logs/compacted/` allowed), fail execution on path drift, and add tests asserting destination invariants.                                                                                   |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                             | Risk                                                                                                                                                                           | Action                                                                                                                                                              |
| ----------- | -------- | ------- | ---------------- | -------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-15-001 | High     | patcher | patch            | Yes      | Compaction output path is not reliable for users                  | Reporter iterations show compacted artifacts repeatedly written outside `docs/03-logs/compacted/`, so users cannot trust where to find the canonical compact view.             | Enforce fail-closed destination validation to `docs/03-logs/compacted/` only, fail execution on drift, and regenerate/migrate compact outputs to the required path. |
| PROD-15-002 | High     | patcher | automated-test   | Yes      | Acceptance quality is unproven by current test gate               | Current Allowed Tests emphasize `tests.test_pc_feature`, so offload index/retention/compaction regressions can slip through while feature-level user value is marked complete. | Reinstate and enforce automated suites for offload index, retention, and log compaction as mandatory completion gates.                                              |
| PROD-15-003 | High     | patcher | patch            | Yes      | Retention flow can delete actively referenced evidence            | If purge removes artifacts still referenced by active work items, users lose debugging context and incident traceability.                                                      | Add reference-aware purge protection by default, require explicit destructive override, and log override actions immutably.                                         |
| PROD-15-004 | High     | patcher | patch            | Yes      | Raw command capture risks exposing sensitive inputs               | Persisting unsanitized command metadata can leak secrets in index/log artifacts, creating user trust and safety risk.                                                          | Implement deterministic command scrubbing/masking before index write, scrub existing indexed entries, and add regression tests.                                     |
| PROD-15-005 | Medium   | human   | human-validation | Yes      | Compacted-log usefulness lacks explicit PO validation             | Automated checks alone do not prove summaries preserve rationale, chronology, and evidence quality needed for Developer/PO decision-making.                                    | Run human review on sampled compacted entries across decision/implementation/validation logs and record explicit sign-off against acceptance criteria.              |
| PROD-15-006 | Low      | patcher | patch            | No       | Recovery guidance for stale/missing compact references is unclear | When source sections shift or referenced artifacts are missing, users may not know the safe remediation path.                                                                  | Add deterministic user-facing remediation guidance (refresh/rebuild flow) for stale reference and missing artifact cases.                                           |

<!-- review-findings:end -->
