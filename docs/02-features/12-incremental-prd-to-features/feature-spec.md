# Feature Specification: Incremental prd-to-features

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-12`

**Owner:** Developer/PO

**Last Updated:** 2026-02-09

### Summary

Rebaseline the feature to current workflow rules: `prd-to-features` must update in place, add only missing feature folders, never delete existing folders, and skip features already marked `Status: Done` in `dev-tasks.md`.

## User Intent

### Who is this for?

- **Primary users:** Developer/PO (single user)
- **User goals:** keep feature backlog stable while evolving PRD scope
- **Current pain:** earlier drafts are too generic and do not capture the current incremental/update-in-place contract, which increases implementation ambiguity

### Why do they need it?

**As a** developer/PO

**I want to** run PRD-to-features incrementally without destructive regeneration

**So that** existing feature work is preserved and only missing features are added

### User Value

- **Value proposition:** safe feature regeneration with predictable outcomes
- **Expected impact:** fewer accidental overwrites and less rework
- **Priority:** P1 - per PRD

## Feature Requirements

### Functional Requirements

#### Core Functionality

- **Requirement 1:** Read PRD prioritized feature list and map to indexed feature folders under `docs/02-features/`.
- **Requirement 2:** Add only missing feature folders; do not create duplicates.
- **Requirement 3:** Never delete existing feature folders.
- **Requirement 4:** Skip features whose `docs/02-features/<feature>/dev-tasks.md` has `Status: Done`.
- **Requirement 5:** When a folder already exists and is not `Done`, update only missing/incomplete sections (no full overwrite unless explicitly requested).
- **Requirement 6:** Report skipped/updated/created items with explicit reasons.

#### Edge Cases

- **Edge Case 1:** Existing folder without `dev-tasks.md`.
- **Edge Case 2:** Malformed or missing `Status:` line in `dev-tasks.md`.
- **Edge Case 3:** PRD feature label change causing slug/index mismatch against existing folders.
- **Edge Case 4:** Existing feature folders marked `Status: Done` but missing optional docs (must still skip regeneration).

### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI
- [ ] Desktop UI
- [ ] Mobile UI

## Acceptance Criteria

- Running `prd-to-features` on an existing project creates only missing feature folders.
- Existing folders are not deleted or duplicated.
- Features with `Status: Done` are skipped deterministically.
- Output summary lists `created`, `updated`, and `skipped` features with reasons.

## Scope

### In Scope

- Incremental feature generation contract
- Update-in-place behavior for existing non-done feature folders
- Done-feature skip behavior
- Reporting/traceability of generation decisions

### Out of Scope

- Rewriting completed feature folders
- Reindexing/renaming existing feature folders automatically
- Generating non-PRD features

## Dependencies

### Requires

- **PRD source:** `docs/01-product/prd.md`
- **Feature rules:** `docs/02-features/AGENTS.md`
- **Workflow policy:** `docs/04-process/human-orchestration-workflow.md`
- **Feature status source:** `docs/02-features/*/dev-tasks.md`

### Blocks

- **None**

## Risks & Considerations

- Loose status parsing can reintroduce done features.
- Aggressive overwrite behavior can erase feature-specific refinements.

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase          | Blocking | Title                                                             | Risk                                                                                                                                                                                                                                         | Action                                                                                                                                                                                             |
| ---------- | -------- | ------- | -------------- | -------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-12-001 | High     | patcher | patch          | Yes      | PRD-derived folder names are not constrained to a safe write root | The feature requires parsing PRD feature labels and creating folders, but the docs do not require path normalization/validation. A crafted label/slug (e.g., with ../ or absolute paths) could make patching write outside docs/02-features. | Enforce strict slug allowlist, reject path separators/dot segments/control chars, resolve realpath for every target, and hard-fail if target is not under docs/02-features before any read/write.  |
| SEC-12-002 | High     | patcher | patch          | Yes      | In-place update flow lacks symlink boundary protection            | The feature updates existing folders/files in place, but no control requires symlink checks. A symlinked feature folder or dev-tasks.md could redirect writes to unintended files.                                                           | Use lstat-based symlink detection on feature directories and managed files, refuse symlink targets, and fail-closed with explicit reporting; do not follow symlinks during update operations.      |
| SEC-12-003 | Medium   | patcher | patch          | Yes      | Malformed or missing Status parsing can fail open                 | Edge cases explicitly include malformed/missing Status, and risks mention loose parsing. If ambiguous status defaults to updatable, Done content can be modified unintentionally, breaking integrity guarantees.                             | Implement strict status parsing and fail-closed behavior for missing/invalid Status (skip + explicit reason) unless an explicit human override path is invoked.                                    |
| SEC-12-004 | Medium   | patcher | automated-test | Yes      | Security boundary tests are missing from required validation set  | Current test expectations cover idempotency/no-delete but do not explicitly require traversal/symlink abuse cases, so boundary regressions may ship undetected.                                                                              | Add automated tests for traversal attempts, absolute-path inputs, symlinked feature paths/files, and malformed-status fail-closed behavior; require these tests to pass before feature completion. |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                                    | Risk                                                                                                                                                                                          | Action                                                                                                                                                                                                                           |
| ----------- | -------- | ------- | ---------------- | -------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PROD-12-001 | High     | patcher | automated-test   | Yes      | Acceptance contract is marked Done without validation evidence           | Feature claims (add-only, no-delete, done-skip, update-in-place) are not backed by completed execution/test/report evidence, so users could trust unsafe behavior and lose backlog integrity. | Complete and record automated validation for idempotent reruns, no-delete guarantees, duplicate prevention, done-skip determinism, and update-only-missing-sections; attach results in validation/report logs before completion. |
| PROD-12-002 | High     | patcher | patch            | Yes      | Run summary does not yet prove recovery-grade workflow clarity           | Users need deterministic reasons and recovery guidance per item; without tested summary semantics, reruns after interruptions can become guesswork and increase accidental edits.             | Implement and test deterministic per-feature reason codes for created/updated/skipped plus recovery-safe messaging (resumed/skipped/repaired/newly executed and immediate remediation when blocked).                             |
| PROD-12-003 | High     | human   | human-validation | Yes      | Slug/index drift lacks explicit human decision gate                      | When PRD labels drift from existing folder slugs, silent or automatic mapping can update the wrong feature and break user trust in incremental updates.                                       | Require human confirmation for drift cases with an explicit mapping table and selected target before proceeding.                                                                                                                 |
| PROD-12-004 | Medium   | human   | human-validation | Yes      | Malformed/missing Status handling needs human override governance        | Security requires fail-closed parsing, but without a documented human override path, users may apply ad-hoc workarounds that produce inconsistent feature states.                             | Route any override of malformed/missing Status to explicit PO sign-off and log the approval rationale before any update is allowed.                                                                                              |
| PROD-12-005 | Medium   | patcher | automated-test   | No       | ‘Update only missing/incomplete sections’ is not acceptance-testable yet | Ambiguous edit scope can cause unexpected content changes even when no destructive intent exists.                                                                                             | Define concrete section-level invariants and add automated diff-based tests showing what must remain unchanged vs what may be filled in.                                                                                         |

<!-- review-findings:end -->
