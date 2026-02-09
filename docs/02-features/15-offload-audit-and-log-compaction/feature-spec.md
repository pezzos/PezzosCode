# Feature Specification: Offload audit + useful log compaction

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-15`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-09

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
