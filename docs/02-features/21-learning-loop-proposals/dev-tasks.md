# Development Tasks: Learning loop proposals

> **LLM-executable tasks**

---

## Overview

Feature: Learning loop proposals

Priority: P1

Status: Not Started

Last Updated: 2026-02-16

Product Surfaces: CLI

## Ownership and Traceability

Source of truth: `dev-tasks.md` (tasks + execution log)

Roles (record names or agent ids):

- Orchestrator: Unassigned
- Planner: Unassigned
- Patcher: Unassigned
- Tester: Unassigned
- Reporter: Unassigned
- Product Owner: Unassigned

## Execution Log

Record each execution round here. Link any related logs in `docs/03-logs/`.

- No runs yet.

When execution starts, add a new work-item entry using
`docs/02-features/feature-template/dev-tasks.md` format.

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-21-001` Human gate is not specified as fail-closed
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Implement an explicit proposal state machine (`proposed|approved|rejected|applied`) and block any apply operation unless approval exists for the current proposal ID/hash.
- [ ] `SEC-21-002` Proposal content validation is undefined
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Enforce a strict schema for proposal payloads, allowlist operation types, reject unknown fields, and treat proposal text strictly as data (never executable input).
- [ ] `SEC-21-003` Secrets can leak from offloaded logs into proposals
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Add secret-redaction before proposal generation/storage/display, covering common key/token patterns and sensitive local path fragments.
- [ ] `SEC-21-004` Approval record is not bound to proposal integrity
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: patch
  - Blocking: Yes
  - Action: Persist proposal hash with approval metadata and verify hash equality at apply time; fail closed on mismatch and log a security event.
- [ ] `SEC-21-005` Security abuse-case tests are missing from required test scope
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add blocking automated tests for: unapproved proposal denied, tampered proposal denied, malicious payload rejected, and secret-redaction enforcement.
- [ ] `PROD-21-001` Proposal contract is not actionable for end users
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Define a required proposal schema for user review: problem evidence, suggested change, expected user impact, affected scope, confidence, and rollback note; reject incomplete proposals.
- [ ] `PROD-21-002` Human-gate decision flow is incomplete
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Specify and implement deterministic state transitions and CLI messages for approve/reject/defer/resubmit, explicitly aligned with fail-closed approval for the current proposal identity/integrity.
- [ ] `PROD-21-003` Required tests miss user-critical workflow branches
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add blocking automated tests for reject persistence, rerun idempotency/deduplication, approved-and-applied no-op behavior, and stale proposal handling, alongside required security abuse-case tests.
- [ ] `PROD-21-004` Acceptance criteria are not measurable for user value
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Add measurable acceptance criteria: deterministic ordering, proposal count limits, explicit rationale per proposal, and auditable link from failure evidence to proposal to human decision.
- [ ] `PROD-21-006` Proposal noise-control policy is undefined
  - Reviewer: Product Manager
  - Severity: Low
  - Phase: patch
  - Blocking: No
  - Action: Define deterministic prioritization and suppression rules (including max proposals per run and repeated-failure dedupe) to keep output reviewable.

### Human Validation Requests (Product Owner / end-user)

- [ ] `SEC-21-006` Human approval UX safety needs explicit validation
  - Reviewer: Security Expert
  - Severity: Low
  - Phase: human-validation
  - Action: Perform human validation that approval UI shows proposal ID/hash, impacted scope, explicit `y/n`, and no default-accept behavior.
- [ ] `PROD-21-005` Approval UX clarity needs explicit human validation
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: human-validation
  - Action: Require PO/end-user validation using realistic cases to confirm approval prompts clearly show proposal identity, impacted scope, and explicit y/n intent with no default-accept behavior.

<!-- review-backlog:end -->

## Task Breakdown

### Discovery and Spec Sync

- [ ] **TASK-001: Confirm requirements for `Learning loop proposals`**
  - Align acceptance criteria with PRD priority `P1`.
  - Document scope boundaries and non-goals before coding.
  - **Acceptance:** Scope and success criteria are explicit.

### Implementation

- [ ] **TASK-002: Implement `Learning loop proposals` capability**
  - Build minimum required behavior for surfaces: CLI.
  - Keep behavior deterministic and idempotent on reruns.
  - **Acceptance:** Primary workflow works end-to-end.

### Testing

- [ ] **TASK-003: Add tests before patch completion**
  - Add failing tests first, then implement the smallest passing patch.
  - Cover happy path and at least one edge condition.
  - **Acceptance:** Tests guard against regressions.

### Validation and Reporting

- [ ] **TASK-004: Validate and capture evidence**
  - Run allowed tests and record results.
  - Capture offload ids for noisy command output.
  - **Acceptance:** Validation evidence is complete and reproducible.

- [ ] **TASK-005: Finalize docs and logs**
  - Update feature docs and required `docs/03-logs/` entries.
  - Summarize tradeoffs and follow-ups in Final Report.
  - **Acceptance:** Plan -> Patch -> Test -> Report is fully documented.
