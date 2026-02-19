# Feature Specification: Commit gated by completed ticket docs

> **User intent & acceptance criteria**

---

## Overview

**Feature ID:** `F-18`

**Status:** Draft

**Owner:** Developer/PO

**Last Updated:** 2026-02-11

### Summary

Prevent commits when ticket documentation is incomplete.
The commit step must verify required execution-log, test, and final-report fields before allowing commit generation.

## User Intent

### Who is this for?

- Primary: Developer/PO relying on execution logs for auditability and handoff quality.

### Why do they need it?

- Incomplete ticket docs weaken confidence in what was changed, validated, and approved.

### User Value

- Stronger traceability for each work item.
- Clear pass/fail criteria before commit.
- Lower risk of undocumented behavior changes.

## Feature Requirements

### Functional Requirements

- [ ] Validate required work-item doc fields before commit is attempted.
- [ ] Block commit with explicit remediation when required sections are missing.
- [ ] Auto-fill deterministic sections where safe (for example, command metadata) without masking missing evidence.
- [ ] Keep role ownership rules (planner/tester/reporter logs) intact.
- [ ] Record commit-gate decision in feature/run logs.

### User Experience Requirements

#### Product Surfaces

- [x] CLI
- [ ] TUI
- [ ] API
- [ ] Web UI

### Non-Functional Requirements

- Commit-gate checks must be deterministic and idempotent.
- Failure messages must identify missing sections precisely.
- Gate evaluation must avoid touching out-of-scope files.

## Acceptance Criteria

### Definition of Done

- Commit is blocked when required execution-doc fields are missing.
- Commit proceeds only when docs satisfy protocol requirements.
- Validation evidence is recorded in logs.

### Test Scenarios

- Missing `Tests Run` section blocks commit and returns remediation.
- Missing final report fields blocks commit.
- Fully complete docs allow commit path to continue.

### Success Metrics

- Decrease in commits with incomplete ticket documentation.
- Faster review due to consistent final report/test evidence.

## Scope

### In Scope

- Commit precheck for execution-doc completeness.
- Deterministic error messaging for missing fields.
- Logging of commit-gate outcomes.

### Out of Scope

- New git workflow model beyond existing `tools/pc-commit` contract.
- Auto-authoring of narrative report content.

## Dependencies

### Requires

- `tools/pc-feature`
- `tools/pc-commit`
- `docs/04-process/ticket-execution-protocol.md`

### Blocks

- Reliable merge collection and release notes quality.

## Risks & Considerations

- Overly strict parsing could block valid commits.
- Overly permissive checks could allow incomplete records.

## Open Questions

- Should missing sections always be hard-blocking, or support feature-level override for manual emergency commits?

## Related Documents

- PRD: `docs/01-product/prd.md`
- Git Workflow: `docs/04-process/git-workflow.md`
- Protocol: `docs/04-process/ticket-execution-protocol.md`

## Automated Review Findings

<!-- review-findings:start -->

### Security Expert

| ID         | Severity | Owner   | Phase            | Blocking | Title                                                                  | Risk                                                                                                                                                                              | Action                                                                                                                                                                                                                                                                       |
| ---------- | -------- | ------- | ---------------- | -------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEC-18-001 | High     | human   | human-validation | Yes      | Commit-gate override policy is unresolved                              | The feature spec leaves emergency override behavior as an open question, which can introduce undocumented bypass paths that allow incomplete evidence to be committed.            | Fail closed by default in code and protocol: disallow overrides unless a PO-approved override model is explicitly documented. If approved later, require explicit override flag, approval artifact ID, reason, and audit logging; add tests proving no silent bypass exists. |
| SEC-18-002 | High     | patcher | patch            | Yes      | Auto-filled command metadata can leak secrets into git history         | The spec requires auto-filling deterministic command metadata but does not require secret redaction, so tokens/credentials in command lines can be committed to docs.             | Add mandatory redaction and fail-closed checks for secret patterns and high-entropy credential-like values before writing metadata; add automated fixtures with injected secrets to verify masking/blocking.                                                                 |
| SEC-18-003 | High     | patcher | automated-test   | Yes      | Gate validates section presence but not evidence authenticity          | Current acceptance/tests focus on missing/empty sections, allowing fabricated `Tests run` or final report text to satisfy the gate without real execution evidence.               | Require machine-verifiable evidence links (existing offload/log pointers with success exit code) for required sections; block on missing, stale, or mismatched artifacts; add negative tests for forged pointers.                                                            |
| SEC-18-004 | Medium   | patcher | patch            | Yes      | Out-of-scope file guard lacks explicit canonical path/symlink controls | The spec requires avoiding out-of-scope files but does not define canonicalization/symlink handling, leaving room for traversal or unintended file access during gate evaluation. | Enforce `realpath`-based repo-root allowlisting, reject symlinks and `..` escapes, and add regression tests for traversal/symlink scenarios.                                                                                                                                 |

### Product Manager (End-User Feedback)

| ID          | Severity | Owner   | Phase            | Blocking | Title                                                             | Risk                                                                                                                                                                 | Action                                                                                                                                                                                     |
| ----------- | -------- | ------- | ---------------- | -------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| PROD-18-001 | High     | human   | human-validation | Yes      | Override policy is unresolved for real incident workflows         | The open override question can create either dead-end blocking during urgent fixes or informal bypasses, both of which reduce trust in the workflow and audit trail. | PO must choose and document a single policy (fail-closed only, or controlled override with approval artifact ID, reason, and audit logging) and update acceptance criteria before release. |
| PROD-18-002 | High     | patcher | automated-test   | Yes      | Gate checks presence of sections but not authenticity of evidence | Users can pass commit gating with fabricated 'Tests run' or report text, creating false confidence for reviewers and downstream handoffs.                            | Require machine-verifiable evidence (offload/log pointer + success status), block stale/forged pointers, and add negative automated tests for spoofed evidence.                            |
| PROD-18-003 | High     | patcher | patch            | Yes      | Auto-filled command metadata can leak secrets                     | Command metadata may capture tokens/credentials and commit them to history, creating direct user and operational risk.                                               | Add mandatory redaction and fail-closed secret detection before metadata write; include fixtures with injected secrets to prove masking/blocking.                                          |
| PROD-18-004 | Medium   | patcher | patch            | Yes      | Out-of-scope guard lacks canonical path and symlink safety        | Path traversal/symlink cases can evaluate unintended files, causing confusing gate outcomes and potential exposure beyond intended scope.                            | Enforce realpath-based repo-root allowlisting, reject symlink/.. escapes, and add regression tests for traversal and symlink scenarios.                                                    |
| PROD-18-005 | Medium   | patcher | automated-test   | No       | Remediation UX quality is not contract-tested                     | Blocked users may receive inconsistent or non-actionable guidance, increasing retry loops and reducing workflow clarity.                                             | Add CLI contract tests asserting deterministic remediation output includes missing field, expected location, and exact next step per failure mode.                                         |

<!-- review-findings:end -->

## Change Log

| Date       | Version | Changes      | Author |
| ---------- | ------- | ------------ | ------ |
| 2026-02-11 | 0.1     | Initial spec | Codex  |
