# Feature Specification: End-to-end workflow smoke test with a synthetic feature

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-24`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-16

### Summary

Validate orchestrator gates and resume/log behavior before real feature runs.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO
- **User goals:** Deliver `End-to-end workflow smoke test with a synthetic feature` with deterministic behavior.
- **Current pain:** PRD intent exists, but feature-level execution details are missing.

### Why do they need it?

**As a** developer/PO

**I want to** implement `End-to-end workflow smoke test with a synthetic feature`

**So that** the prioritized PRD outcome is delivered reliably.

### User Value

- **Value proposition:** Converts PRD intent into executable feature scope.
- **Expected impact:** Validate orchestrator gates and resume/log behavior before real feature runs.
- **Priority:** P1.

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Implement `End-to-end workflow smoke test with a synthetic feature` according to PRD priority `P1`.
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

- `End-to-end workflow smoke test with a synthetic feature`
- Outcome from PRD: Validate orchestrator gates and resume/log behavior before real feature runs.
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

- Source notes: Validate orchestrator gates and resume/log behavior before real feature runs.
- Ambiguous acceptance criteria can cause rework if not clarified during planning.

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                          | Risk                                                                                                                                                                                                                             | Action                                                                                                                                                                                                                     |
| ---------- | -------- | ------- | -------------- | -------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-24-001 | High     | patcher | patch          | Yes      | No secret-redaction control for offloaded and structured logs  | Workflow C requires writing noisy output to `.offload/<id>.txt` and `logs/<WI>/<step>.log`, but the feature docs define no masking/redaction rule; credentials or tokens printed by tests/CLI can be stored and later committed. | Add a centralized sanitizer before any log/offload write (mask common secret patterns and sensitive env keys), and add regression tests that inject synthetic secrets and verify masked output in both destinations.       |
| SEC-24-002 | High     | patcher | patch          | Yes      | Path traversal risk in log/offload file generation             | The documented paths use runtime placeholders (`<WI>`, `<step>`, `<id>`) without explicit input constraints; unsanitized values can escape target directories or overwrite unintended files.                                     | Enforce strict allowlist validation for path segments, canonicalize and verify base-directory containment, reject invalid/absolute/traversal inputs, and add tests for `../`, absolute paths, and symlink escape attempts. |
| SEC-24-003 | High     | patcher | automated-test | Yes      | Fail-closed gate behavior is specified but not security-tested | Workflows require blocking at HIGH-risk approval, Plan Reviewer approval, and commit evidence gates, but tasks do not require explicit automated assertions that downstream stages cannot execute when gates are unmet.          | Add automated smoke tests that prove fail-closed behavior: blocked status (`Awaiting PO Approval` where applicable), non-zero exit, and no patch/test/commit stage execution until required approvals/evidence exist.      |
| SEC-24-004 | High     | patcher | patch          | Yes      | Resume-state tampering can bypass required checks              | Workflow D allows skipping completed stages on resume; without integrity checks tying state to real evidence, a modified state file can falsely mark review/test/report gates as complete.                                       | Harden resume metadata with integrity validation (state/evidence binding), fail closed on mismatch, and force re-run of guarded stages when validation fails.                                                              |
| SEC-24-005 | Medium   | patcher | automated-test | Yes      | Synthetic smoke run lacks explicit isolation guardrails        | The feature targets end-to-end execution but docs do not require isolation boundaries for synthetic runs, creating risk of unintended writes outside expected test artifacts.                                                    | Constrain synthetic execution to an isolated temp worktree and enforce an allowlisted command/file-write scope; add validation that reruns only touch expected artifacts.                                                  |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                         | Risk                                                                                                                                                              | Action                                                                                                                                                                     |
| ----------- | -------- | ------- | ---------------- | -------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-24-001 | High     | patcher | patch            | Yes      | Missing deterministic user-facing pass criteria               | The feature does not define the exact CLI signals a PO should use to confirm end-to-end success, so runs can look successful while gates/evidence are incomplete. | Define and implement a strict output contract for success/failure that includes stage status, resume state (resumed/skipped/repaired/new), and required evidence pointers. |
| PROD-24-002 | High     | patcher | automated-test   | Yes      | Idempotent rerun and resume behavior is not acceptance-tested | Without explicit repeated-run assertions, users may see duplicate, drifting, or inconsistent outcomes and lose trust in workflow safety.                          | Add automated tests for first run vs rerun vs interrupted-resume that assert deterministic outcomes, no duplicate stage effects, and stable evidence references.           |
| PROD-24-003 | High     | patcher | automated-test   | Yes      | Smoke coverage omits critical user workflow branches          | A single happy-path smoke can pass while key real-world branches (approval block, rejection loop, recovery flow) remain broken for end users.                     | Define a mandatory scenario matrix and automate it: happy path plus at least one negative/loop case for each critical gate and handoff.                                    |
| PROD-24-004 | Medium   | patcher | patch            | Yes      | PO clarification path is underspecified                       | The spec says to seek PO clarification on ambiguity but does not define blocked state, ownership, or logging, which can cause scope drift and rework.             | Add an explicit clarification gate with fail-closed status, owner routing, and required log evidence before execution can continue.                                        |
| PROD-24-005 | Medium   | human   | human-validation | Yes      | No required human sign-off for workflow clarity               | Even if automation passes, PO users may still misinterpret prompts, blocked states, and remediation actions during real operation.                                | Run and record a human-validation checklist covering gate prompts, blocked labels, remediation text, and final run summary readability before approval.                    |

<!-- review-findings:end -->
