# Development Tasks: Feature gating + skill mining

> **LLM-executable tasks**

---

## Overview

**Feature:** Feature gating + skill mining

**Status:** Not Started

**Last Updated:** 2026-02-08

## Review Findings Backlog

<!-- review-backlog:start -->

### Patcher Tasks (must be handled during patch/test steps)

- [ ] `SEC-16-001` Sensitive data can be copied into skill proposals
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Implement fail-closed secret handling in miner output: detect credentials (token/key/password patterns + high-entropy strings), redact values, and store only minimal references (path + line/offset/hash) instead of raw secret-bearing text.
- [ ] `SEC-16-002` Repository-boundary enforcement is missing for mined inputs
  - Reviewer: Security Expert
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Constrain mining to an allowlisted repo-relative set after `realpath` validation, reject paths outside repo root, do not follow symlinks, skip binary files, and cap file size/line length before parsing.
- [ ] `SEC-16-003` Soft-warning implementation could accidentally bypass hard commit controls
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add regression tests proving existing hard-fail gates still return non-zero while sequencing warnings remain advisory-only; enforce additive warning behavior only.
- [ ] `SEC-16-004` Malformed status parsing can silently suppress governance signal
  - Reviewer: Security Expert
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: On parse ambiguity or missing status, emit deterministic `unknown status` warnings with affected feature IDs and remediation text; add tests for malformed, duplicate, and missing status fields.
- [ ] `SEC-16-005` Control-character and markdown injection in mined evidence
  - Reviewer: Security Expert
  - Severity: Low
  - Phase: patch
  - Blocking: No
  - Action: Normalize mined text before proposal generation: strip control characters, escape markdown where needed, and render evidence as plain text snippets.
- [ ] `PROD-16-001` Sequencing warning lacks deterministic recovery contract
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Implement a fixed warning template that always includes earlier incomplete feature IDs/statuses, remediation path, and next eligible feature/action; add deterministic output tests.
- [ ] `PROD-16-002` Skill-mining quality thresholds are under-specified
  - Reviewer: Product Manager
  - Severity: High
  - Phase: patch
  - Blocking: Yes
  - Action: Define bounded mining thresholds (minimum repeats, source diversity, dedupe/cooldown) and enforce them with tests for noisy vs high-signal datasets.
- [ ] `PROD-16-003` Soft-warning change may weaken perceived commit protection
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: automated-test
  - Blocking: Yes
  - Action: Add regression coverage proving existing hard-fail gates remain non-zero while sequencing warnings stay advisory-only (aligned with SEC-16-003).

### Human Validation Requests (Product Owner / end-user)

- [ ] `PROD-16-004` Human approval gate for mined proposals is not operationalized
  - Reviewer: Product Manager
  - Severity: Medium
  - Phase: human-validation
  - Action: Require PO/end-user validation for first proposal batch using a checklist (usefulness, duplication, maintenance cost, security/redaction evidence) with explicit approve/reject outcomes logged.
- [ ] `PROD-16-005` Warning usability is not yet validated in real commit scenarios
  - Reviewer: Product Manager
  - Severity: Low
  - Phase: human-validation
  - Action: Run human spot checks on warning clarity for single-feature and multi-feature commits and record comprehension feedback.

<!-- review-backlog:end -->

## Task Breakdown

- [ ] **Task 1 - Implement feature status parser**
  - Parse ordered feature folders and each `dev-tasks.md` `Status` value.
  - Handle malformed/missing status values with explicit fallback warnings.
  - Output: deterministic status map for gating checks.

- [ ] **Task 2 - Add precommit soft warning**
  - In `tools/pc-precommit`, warn when editing feature `N` while earlier features are not `Done`.
  - Ensure warning is advisory only and does not block commit.
  - Output: actionable sequencing warning with remediation hints.

- [ ] **Task 3 - Implement skill-mining proposal generator**
  - Detect repeated prompt/workflow patterns using bounded thresholds.
  - Emit candidate skill proposals with evidence references.
  - Output: reviewable skill proposals (no auto-install).

- [ ] **Task 4 - Add tests and docs/log sync**
  - Add tests for status parsing, warning behavior, and mining thresholds.
  - Update process docs and `docs/03-logs` entries with implementation/validation evidence.
  - Output: validated behavior and traceable documentation.

## Execution Log

- No runs yet.

## Allowed Tests (Planner must populate before Tester runs)

- `python -m unittest discover -s tests -p "test_*.py"`

## Related Documents

- Feature Spec: `docs/02-features/16-feature-gating-and-skill-mining/feature-spec.md`
- Tech Design: `docs/02-features/16-feature-gating-and-skill-mining/tech-design.md`
- Test Plan: `docs/02-features/16-feature-gating-and-skill-mining/test-plan.md`
- Planner Log: `docs/02-features/16-feature-gating-and-skill-mining/planner-log.md`
- Reporter Log: `docs/02-features/16-feature-gating-and-skill-mining/reporter-log.md`
- Validation Log: `docs/02-features/16-feature-gating-and-skill-mining/validation-log.md`

## Change Log

| Date       | Changes                                                                  | Author       |
| ---------- | ------------------------------------------------------------------------ | ------------ |
| 2026-02-09 | Aligned workflow baseline to remove change-budget fields/section wording | Codex        |
| 2026-02-08 | Rebased tasks to sequencing warning + skill mining flow                  | Codex        |
| 2026-02-05 | Initial task breakdown                                                   | Primary user |
