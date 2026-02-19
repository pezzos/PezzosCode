# Feature Specification: Learning loop proposals

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-21`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-16

### Summary

Post-run improvement proposals with human gate.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `Learning loop proposals` with deterministic behavior.
- **Current pain:** PRD intent exists, but feature-level execution details are missing.

### Why do they need it?

**As a** developer/PO

**I want to** implement `Learning loop proposals`

**So that** the prioritized PRD outcome is delivered reliably.

### User Value

- **Value proposition:** Converts PRD intent into executable feature scope.
- **Expected impact:** Post-run improvement proposals with human gate.
- **Priority:** P1.

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Implement `Learning loop proposals` according to PRD priority `P1`.
- **Requirement 2:** Keep behavior deterministic and idempotent on reruns.
- **Requirement 3:** Document boundaries, success criteria, and evidence paths.

#### Edge Cases

- Missing or ambiguous PRD details require explicit PO clarification.
- Existing implementation artifacts must not be overwritten destructively.

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Feature folder content is specific to this PRD item, not template placeholders.
- Functional behavior and tests are defined before patching.
- Scope boundaries and non-goals are explicit.
- Validation evidence is captured in work-item logs.

## Scope

### In Scope

- `Learning loop proposals`
- Outcome from PRD: Post-run improvement proposals with human gate.
- Feature-level documentation needed for Plan -> Patch -> Test -> Report.

### Out of Scope

- Unrelated product changes.
- New workflow automation beyond this feature.
- Destructive rewrites of completed feature folders.

## Dependencies

### Requires

- `docs/01-product/prd.md`
- `docs/02-features/AGENTS.md`
- `docs/04-process/ticket-execution-protocol.md`

### Blocks

- None currently identified.

## Risks & Considerations

- Source notes: Post-run improvement proposals with human gate.
- Ambiguous acceptance criteria can cause rework if not clarified during planning.

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase            | Blocking | Title                                                          | Risk                                                                                                                                                                                              | Action                                                                                                                                                              |
| ---------- | -------- | ------- | ---------------- | -------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------- | ------------------------------------------------------------------------------------------------ |
| SEC-21-001 | High     | patcher | patch            | Yes      | Human gate is not specified as fail-closed                     | The feature summary says proposals have a human gate, but the spec/tasks do not require a deny-by-default approval state. A patch could accidentally allow apply paths without explicit approval. | Implement an explicit proposal state machine (`proposed                                                                                                             | approved | rejected | applied`) and block any apply operation unless approval exists for the current proposal ID/hash. |
| SEC-21-002 | High     | patcher | patch            | Yes      | Proposal content validation is undefined                       | Workflow E transforms failures into proposals, but no schema/allowlist is defined. Malicious payloads could be interpreted as executable instructions or unsafe file operations.                  | Enforce a strict schema for proposal payloads, allowlist operation types, reject unknown fields, and treat proposal text strictly as data (never executable input). |
| SEC-21-003 | High     | patcher | patch            | Yes      | Secrets can leak from offloaded logs into proposals            | Workflow C offloads noisy command output and Learning Loop consumes failure context. Without redaction controls, tokens/credentials/path secrets can be persisted in proposal artifacts.          | Add secret-redaction before proposal generation/storage/display, covering common key/token patterns and sensitive local path fragments.                             |
| SEC-21-004 | Medium   | patcher | patch            | Yes      | Approval record is not bound to proposal integrity             | Docs require logs but do not require tamper detection between approved content and applied content. Approved proposals could be modified after approval.                                          | Persist proposal hash with approval metadata and verify hash equality at apply time; fail closed on mismatch and log a security event.                              |
| SEC-21-005 | Medium   | patcher | automated-test   | Yes      | Security abuse-case tests are missing from required test scope | Task-003 only mandates happy path + one edge case, so critical security regressions can pass feature completion unnoticed.                                                                        | Add blocking automated tests for: unapproved proposal denied, tampered proposal denied, malicious payload rejected, and secret-redaction enforcement.               |
| SEC-21-006 | Low      | human   | human-validation | No       | Human approval UX safety needs explicit validation             | Human gate exists, but docs do not require verification that approval prompts clearly show proposal identity/scope, increasing accidental approval risk.                                          | Perform human validation that approval UI shows proposal ID/hash, impacted scope, explicit `y/n`, and no default-accept behavior.                                   |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                 | Risk                                                                                                                                                                                    | Action                                                                                                                                                                                                |
| ----------- | -------- | ------- | ---------------- | -------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-21-001 | High     | patcher | patch            | Yes      | Proposal contract is not actionable for end users     | Current spec does not define the minimum proposal content needed for confident approval, so users can receive vague proposals that are hard to evaluate and easy to reject incorrectly. | Define a required proposal schema for user review: problem evidence, suggested change, expected user impact, affected scope, confidence, and rollback note; reject incomplete proposals.              |
| PROD-21-002 | High     | patcher | patch            | Yes      | Human-gate decision flow is incomplete                | The feature mentions a human gate but does not fully define approve/reject/defer/resubmit behavior, creating ambiguous outcomes and inconsistent reruns.                                | Specify and implement deterministic state transitions and CLI messages for approve/reject/defer/resubmit, explicitly aligned with fail-closed approval for the current proposal identity/integrity.   |
| PROD-21-003 | Medium   | patcher | automated-test   | Yes      | Required tests miss user-critical workflow branches   | With only happy-path plus one edge case, regressions can re-surface rejected proposals, duplicate proposals on rerun, or mishandle already-applied approvals.                           | Add blocking automated tests for reject persistence, rerun idempotency/deduplication, approved-and-applied no-op behavior, and stale proposal handling, alongside required security abuse-case tests. |
| PROD-21-004 | High     | patcher | patch            | Yes      | Acceptance criteria are not measurable for user value | The feature can be marked done through documentation completion without proving decision quality, predictability, or traceability for end users.                                        | Add measurable acceptance criteria: deterministic ordering, proposal count limits, explicit rationale per proposal, and auditable link from failure evidence to proposal to human decision.           |
| PROD-21-005 | Medium   | human   | human-validation | No       | Approval UX clarity needs explicit human validation   | Users may approve incorrect proposals if impact scope and proposal identity are not clearly understood under real failure scenarios.                                                    | Require PO/end-user validation using realistic cases to confirm approval prompts clearly show proposal identity, impacted scope, and explicit y/n intent with no default-accept behavior.             |
| PROD-21-006 | Low      | patcher | patch            | No       | Proposal noise-control policy is undefined            | Too many low-signal proposals can reduce trust and lead to blanket rejection, weakening the learning loop.                                                                              | Define deterministic prioritization and suppression rules (including max proposals per run and repeated-failure dedupe) to keep output reviewable.                                                    |

<!-- review-findings:end -->
