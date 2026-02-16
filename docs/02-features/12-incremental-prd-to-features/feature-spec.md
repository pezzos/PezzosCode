# Feature Specification: Incremental prd-to-features

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-12`

**Status:** Done

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

### Security Reviewer

| ID         | Severity | Risk                                                                           | Action                                                                                           |
| ---------- | -------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| SEC-12-001 | High     | Unvalidated input can trigger data corruption or unsafe behavior.              | Add explicit validation rules, error paths, and anti-bypass tests in feature-spec and dev-tasks. |
| SEC-12-003 | Medium   | Credentials or tokens may leak into code, logs, or config.                     | Document secret sources, redaction strategy, and prohibited storage locations.                   |
| SEC-12-004 | High     | Missing injection controls can expose command, SQL, or script injection paths. | Define escaping/parameterization requirements and add dedicated injection test scenarios.        |
| SEC-12-005 | Medium   | Unsafe defaults can bypass intended runtime protections.                       | Capture required config defaults, permission boundaries, and misconfiguration failure behavior.  |

### Product Manager

| ID          | Severity | Risk                                                                    | Action                                                                                       |
| ----------- | -------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| PROD-12-002 | Medium   | Implementation may diverge from intended user path and onboarding flow. | Add explicit user journey steps, entry points, and completion states.                        |
| PROD-12-005 | Low      | Human acceptance timing may be unclear before execution starts.         | Add a `Product Owner test checkpoint` task in dev-tasks before first make feature execution. |

<!-- review-findings:end -->
