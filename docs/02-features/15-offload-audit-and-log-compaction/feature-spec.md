# Feature Specification: Offload audit + log compaction

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-15`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-08

### Summary

Implement observability and lifecycle management for offloaded command output, then add compacting skills for long-lived logs so review remains efficient without losing source records.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** trace offload usage and keep historical logs reviewable
- **Current pain:** offload data exists in `.offload/` but lacks index/retention controls; large logs are hard to skim

### Why do they need it?

**As a** developer/PO

**I want to** audit offload artifacts and generate compact log views

**So that** I can debug quickly and preserve traceability with lower token cost

### User Value

- **Value proposition:** auditable offload storage plus concise log summaries
- **Expected impact:** lower context load and easier incident review
- **Priority:** P2 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Create an offload index capturing `id`, `command`, `work_item_id`, `agent_name`, `timestamp`, and `size_bytes` for each offloaded artifact.
- **Requirement 2:** Add deterministic list/get/purge utilities for indexed artifacts with retention support.
- **Requirement 3:** Implement compaction skills for `docs/03-logs/decision-log.md` and `docs/03-logs/implementation-log.md` that produce concise summaries without deleting source logs.
- **Requirement 4:** Keep offload and compaction actions traceable in docs/logs.

#### Edge Cases

- **Edge Case 1:** Index entry exists but backing `.offload/<id>.txt` file is missing.
- **Edge Case 2:** Purge policy removes artifacts still referenced by active work items.
- **Edge Case 3:** Compaction removes critical rationale or chronology.

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
- Compaction skills produce compact outputs with source references and no source-file deletion.
- Validation confirms compaction preserves key decisions/implementation traceability.

## Scope

### In Scope

- Offload metadata index and lifecycle commands
- Retention rules for `.offload/`
- Log-compaction skills and their usage guidance
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
- **Log sources:** `docs/03-logs/decision-log.md`, `docs/03-logs/implementation-log.md`

### Blocks

- **None**

## Risks & Considerations

- Aggressive retention can break reproducibility/debugging.
- Poor compaction heuristics can hide high-impact details.
